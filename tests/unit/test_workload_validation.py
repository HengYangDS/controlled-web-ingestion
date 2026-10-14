import json
import tempfile
import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from web_ingestion import validation
from web_ingestion.contracts import HttpFetch, IngestionError
from web_ingestion.controller import IngestionController
from web_ingestion.policy import RobotsDecision
from web_ingestion.schema import load_named_schema, validate_document

CLEAN = {"containers": 0, "volumes": 0, "networks": 0, "published_listener": 0}
STATIC_BODY = "Useful fixture body with sufficient quality."


class FakeHttpClient:
    """Serve one public fixture page and refuse the private loopback target."""

    def fetch_robots(self, _url, **_options):
        return RobotsDecision(True, "robots_allowed", None)

    def fetch(self, url, **_options):
        if url.startswith("http://127.0.0.1"):
            raise IngestionError("blocked_ip:127.0.0.1")
        return HttpFetch(
            requested_url=url,
            final_url=url,
            status_code=200,
            headers={"Content-Type": "text/html"},
            body=b"<html><body>fixture</body></html>",
            redirect_chain=(url,),
        )


def fixture_controller(**options):
    return IngestionController(
        http_client=FakeHttpClient(), static_extractor=lambda _: STATIC_BODY, **options
    )


def fixture_firecrawl(request, stage_root):
    def handler(admitted):
        return f"Rendered {admitted.mode} fixture body", "Fixture", admitted.url, admitted.max_pages

    return fixture_controller(browser_handler=handler).ingest(request, stage_root=stage_root)


@contextmanager
def fixture_runtime():
    yield "http://127.0.0.1:13002"


def public_target(url, **_options):
    return SimpleNamespace(allowed=True, canonical_url=url, reason="public_http_target")


class ValidationRunTests(unittest.TestCase):
    def run_validation(self, **overrides):
        fakes = {
            "IngestionController": fixture_controller,
            "stage_with_firecrawl": fixture_firecrawl,
            "firecrawl_runtime": fixture_runtime,
            "verify_reviewed_images": lambda: {"api": "ghcr.io/firecrawl/firecrawl@sha256:a"},
            "project_resources": lambda: dict(CLEAN),
            "published_ports": lambda: ["127.0.0.1:13002"],
            "service_rejects_loopback": lambda _endpoint: {"status_code": 400, "rejected": True},
            **overrides,
        }
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.multiple(validation, **fakes),
            patch("web_ingestion.controller.validate_target", side_effect=public_target),
        ):
            evidence = validation.validate_authorized_workloads(Path(directory) / "e.json")
            return json.loads(evidence.read_text(encoding="utf-8"))

    def test_complete_run_writes_schema_valid_body_redacted_evidence(self):
        document = self.run_validation()

        self.assertEqual(validate_document(document, load_named_schema("evidence")), [])
        self.assertEqual(document["status"], "passed")
        self.assertEqual(document["receipts"]["duplicate_static"]["status"], "duplicate")
        self.assertEqual(document["receipts"]["crawl"]["quality"]["discovered_count"], 10)
        self.assertEqual(document["isolation"]["in_run_rejection"], "blocked_ip:127.0.0.1")
        self.assertIsNone(document["rag_bridge"]["sink"])
        self.assertEqual(
            sorted(document["declarations"]),
            [
                "system/policies/authorized-workloads.json",
                "system/projections/firecrawl-isolated-compose.yaml",
                "system/supply-chain/firecrawl-provenance.json",
            ],
        )

    def test_an_escaped_listener_blocks_the_evidence(self):
        with self.assertRaisesRegex(validation.ValidationFailure, "escaped loopback"):
            self.run_validation(published_ports=lambda: ["0.0.0.0:13002"])

    def test_a_service_that_scrapes_loopback_blocks_the_evidence(self):
        accepted = {"status_code": 200, "rejected": False}
        with self.assertRaisesRegex(validation.ValidationFailure, "accepted loopback"):
            self.run_validation(service_rejects_loopback=lambda _endpoint: accepted)

    def test_leftover_resources_block_the_evidence(self):
        with self.assertRaisesRegex(validation.ValidationFailure, "not clean"):
            self.run_validation(project_resources=lambda: {**CLEAN, "volumes": 1})


class ReceiptAssertionTests(unittest.TestCase):
    def write(self, directory, record):
        path = Path(directory) / "receipt.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def test_route_status_and_forbidden_fields_are_enforced(self):
        record = {
            "route": "firecrawl",
            "status": "success",
            "policy_decision": "admitted",
            "robots_decision": "allowed",
            "dedupe_decision": "unique",
            "quality": {"discovered_count": 1},
            "content_sha256": "0" * 64,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(directory, record)
            with self.assertRaisesRegex(validation.ValidationFailure, "route/status"):
                validation.assert_receipt(path, route="trafilatura", status="success", discovered=1)
            with self.assertRaisesRegex(validation.ValidationFailure, "discovery"):
                validation.assert_receipt(path, route="firecrawl", status="success", discovered=10)
            self.write(directory, {**record, "markdown": "kept body"})
            with self.assertRaisesRegex(validation.ValidationFailure, "forbidden"):
                validation.assert_no_forbidden_persistence(Path(directory))

    def test_allowlist_drift_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "workloads.json"
            document = json.loads(validation.ALLOWLIST.read_text(encoding="utf-8"))
            document["workloads"] = document["workloads"][:2]
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(validation.ValidationFailure, "drifted"):
                validation.load_workloads(path)


class LoopbackProbeTests(unittest.TestCase):
    def probe(self, status):
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802 - stdlib handler contract
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(status)
                self.end_headers()

            def log_message(self, format, *args):  # noqa: A003 - suppress test-server logs
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            return validation.service_rejects_loopback(f"http://127.0.0.1:{server.server_port}")
        finally:
            server.shutdown()
            server.server_close()

    def test_refusal_and_acceptance_are_both_recorded(self):
        self.assertEqual(self.probe(400)["rejected"], True)
        self.assertEqual(self.probe(200)["rejected"], False)

    def test_an_unreachable_service_counts_as_refusal(self):
        result = validation.service_rejects_loopback("http://127.0.0.1:9")
        self.assertEqual((result["rejected"], "transport_error" in result), (True, True))


if __name__ == "__main__":
    unittest.main()
