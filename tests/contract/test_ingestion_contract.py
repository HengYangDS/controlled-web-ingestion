import json
import tempfile
import unittest
from pathlib import Path


class RequestContractTests(unittest.TestCase):
    def test_requires_purpose_mode_budget_and_timeout(self):
        from web_ingestion import IngestionError, IngestionRequest

        with self.assertRaisesRegex(IngestionError, "purpose"):
            IngestionRequest(
                url="https://example.com/",
                purpose=" ",
                mode="static",
                max_pages=1,
                timeout_seconds=30,
            )
        with self.assertRaisesRegex(IngestionError, "max_pages"):
            IngestionRequest(
                url="https://example.com/",
                purpose="fixture",
                mode="static",
                max_pages=11,
                timeout_seconds=30,
            )
        with self.assertRaisesRegex(IngestionError, "timeout"):
            IngestionRequest(
                url="https://example.com/",
                purpose="fixture",
                mode="static",
                max_pages=1,
                timeout_seconds=0,
            )

    def test_enforces_the_route_specific_page_budget(self):
        from web_ingestion import IngestionError, IngestionRequest

        for mode in ("static", "browser"):
            with self.subTest(mode=mode), self.assertRaisesRegex(IngestionError, "max_pages_for_mode"):
                IngestionRequest(
                    url="https://example.com/",
                    purpose="fixture",
                    mode=mode,
                    max_pages=2,
                    timeout_seconds=30,
                )


class SafeTransportTests(unittest.TestCase):
    def test_rejects_a_redirect_before_following_it_into_private_space(self):
        from web_ingestion import IngestionError, RawHttpResponse, SafeHttpClient

        calls = []

        def resolver(host: str):
            return ["93.184.216.34"]

        def transport(url: str, *, timeout_seconds: float, max_bytes: int):
            calls.append(url)
            return RawHttpResponse(
                url=url,
                status_code=302,
                headers={"Location": "http://127.0.0.1:9999/private"},
                body=b"",
            )

        client = SafeHttpClient(resolver=resolver, transport=transport)
        with self.assertRaisesRegex(IngestionError, "blocked_ip:127.0.0.1"):
            client.fetch("https://example.com/start", timeout_seconds=5, max_bytes=1024)
        self.assertEqual(calls, ["https://example.com/start"])


class _FakeHttpClient:
    def __init__(self, *, robots_allowed=True, content_type="text/html"):
        from web_ingestion.policy import RobotsDecision
        from web_ingestion import HttpFetch

        self.robots = RobotsDecision(robots_allowed, "robots_allowed" if robots_allowed else "robots_disallow", None)
        self.response = HttpFetch(
            requested_url="https://example.com/",
            final_url="https://example.com/final",
            status_code=200,
            headers={"Content-Type": content_type},
            body=b"<html><title>Fixture</title><body>Useful fixture body with sufficient quality.</body></html>",
            redirect_chain=("https://example.com/", "https://example.com/final"),
        )

    def fetch_robots(self, url: str, *, timeout_seconds: float):
        return self.robots

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int):
        return self.response


class ControllerReceiptTests(unittest.TestCase):
    def _request(self):
        from web_ingestion import IngestionRequest

        return IngestionRequest(
            url="https://example.com/",
            purpose="validate the controlled static route",
            mode="static",
            max_pages=1,
            timeout_seconds=30,
        )

    def test_stages_body_redacted_receipt_with_operational_fields(self):
        from web_ingestion import IngestionController

        controller = IngestionController(
            http_client=_FakeHttpClient(),
            static_extractor=lambda _: "Useful fixture body with sufficient quality.",
        )
        with tempfile.TemporaryDirectory() as directory:
            outcome = controller.ingest(self._request(), stage_root=Path(directory))
            persisted = json.loads(outcome.stage_receipt.read_text(encoding="utf-8"))

        self.assertEqual(outcome.route, "trafilatura")
        self.assertEqual(persisted["status"], "success")
        self.assertEqual(persisted["purpose"], "validate the controlled static route")
        self.assertEqual(persisted["dedupe_decision"], "unique")
        self.assertEqual(persisted["redirect_chain"], ["https://example.com/", "https://example.com/final"])
        self.assertNotIn("body", persisted)
        self.assertNotIn("content", persisted)
        self.assertNotIn("html", persisted)

    def test_duplicate_content_is_staged_but_cannot_be_promoted(self):
        from web_ingestion.policy import PromotionError
        from web_ingestion.staging import StageStore
        from web_ingestion import IngestionController

        controller = IngestionController(
            http_client=_FakeHttpClient(),
            static_extractor=lambda _: "Useful fixture body with sufficient quality.",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            controller.ingest(self._request(), stage_root=root)
            duplicate = controller.ingest(self._request(), stage_root=root)
            persisted = json.loads(duplicate.stage_receipt.read_text(encoding="utf-8"))

            self.assertEqual(persisted["status"], "duplicate")
            self.assertEqual(persisted["dedupe_decision"], "duplicate")
            with self.assertRaises(PromotionError):
                StageStore(root).promote(duplicate.stage_receipt, explicit_confirmation=True)

    def test_robots_denial_and_unapproved_content_type_fail_closed(self):
        from web_ingestion import IngestionController, IngestionError

        denied = IngestionController(http_client=_FakeHttpClient(robots_allowed=False))
        wrong_type = IngestionController(http_client=_FakeHttpClient(content_type="application/octet-stream"))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(IngestionError, "robots_disallow"):
                denied.ingest(self._request(), stage_root=Path(directory))
            with self.assertRaisesRegex(IngestionError, "content_type"):
                wrong_type.ingest(self._request(), stage_root=Path(directory))

    def test_firecrawl_result_target_is_revalidated_before_staging(self):
        from web_ingestion import IngestionController, IngestionError, IngestionRequest

        request = IngestionRequest(
            url="https://example.com/",
            purpose="validate returned Firecrawl source target",
            mode="browser",
            max_pages=1,
            timeout_seconds=30,
        )
        controller = IngestionController(
            http_client=_FakeHttpClient(),
            browser_handler=lambda _: ("fixture content", "Fixture", "http://127.0.0.1/private", 1),
        )
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(IngestionError, "firecrawl_result_target:blocked_ip"):
                controller.ingest(request, stage_root=Path(directory))

    def test_firecrawl_result_cannot_exceed_the_approved_page_budget(self):
        from web_ingestion import IngestionController, IngestionError, IngestionRequest

        request = IngestionRequest(
            url="https://example.com/",
            purpose="validate returned Firecrawl page budget",
            mode="browser",
            max_pages=1,
            timeout_seconds=30,
        )
        controller = IngestionController(
            http_client=_FakeHttpClient(),
            browser_handler=lambda _: ("fixture content", "Fixture", "https://example.com/final", 2),
        )
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(IngestionError, "discovered_count_exceeds_page_budget"):
                controller.ingest(request, stage_root=Path(directory))


if __name__ == "__main__":
    unittest.main()

class RoutingManifestTests(unittest.TestCase):
    def test_routing_manifest_preserves_the_expected_disposable_boundary(self):
        root = Path(__file__).resolve().parents[2]
        routing = json.loads((root / "system" / "projections" / "routing.json").read_text(encoding="utf-8"))

        self.assertEqual(routing["modes"]["static"]["route"], "trafilatura")
        self.assertEqual(routing["modes"]["browser"]["service"], "disposable_loopback_only")
        self.assertEqual(routing["modes"]["crawl"]["max_pages"], 10)
        self.assertIn("direct_rag_write", routing["excluded"])


class AuthorizedWorkloadTimingTests(unittest.TestCase):
    def test_ten_page_serial_firecrawl_workload_reserves_the_full_bounded_runtime(self):
        root = Path(__file__).resolve().parents[2]
        workloads = json.loads((root / "system" / "policies" / "authorized-workloads.json").read_text(encoding="utf-8"))
        crawl = next(item for item in workloads["workloads"] if item["id"] == "crawl-quotes")

        self.assertEqual(crawl["mode"], "crawl")
        self.assertEqual(crawl["max_pages"], 10)
        self.assertEqual(crawl["timeout_seconds"], 120)
