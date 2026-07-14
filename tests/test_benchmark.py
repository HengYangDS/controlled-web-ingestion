import hashlib
import os
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from benchmark import REQUIRED_FIELDS, validate_record


def valid_record():
    return {
        "candidate": "synthetic",
        "case": "static",
        "requested_url": "https://example.com/",
        "final_url": "https://example.com/",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "status": "success",
        "content_sha256": hashlib.sha256(b"fixture").hexdigest(),
        "title": "Example Domain",
        "source_url": "https://example.com/",
        "discovered_count": 0,
        "error": None,
        "resources": {"elapsed_ms": 1},
        "artifacts": [],
    }


class RecordContractTests(unittest.TestCase):
    def test_required_fields_are_exposed(self):
        self.assertEqual(
            REQUIRED_FIELDS,
            {
                "candidate", "case", "requested_url", "final_url", "started_at",
                "ended_at", "status", "content_sha256", "title", "source_url",
                "discovered_count", "error", "resources", "artifacts",
            },
        )

    def test_accepts_body_redacted_complete_record(self):
        self.assertEqual(validate_record(valid_record()), [])

    def test_rejects_raw_body_and_bad_digest(self):
        record = valid_record()
        record["body"] = "must never be persisted"
        record["content_sha256"] = "not-a-digest"
        errors = validate_record(record)
        self.assertTrue(any("forbidden field body" in error for error in errors))
        self.assertTrue(any("content_sha256" in error for error in errors))

    def test_rejects_missing_field(self):
        record = valid_record()
        del record["resources"]
        self.assertIn("missing required field resources", validate_record(record))


if __name__ == "__main__":
    unittest.main()

class NormalizationTests(unittest.TestCase):
    def test_normalizes_content_without_persisting_it(self):
        from benchmark import normalized_record

        record = normalized_record(
            candidate="fixture",
            case="static",
            requested_url="https://example.com/",
            final_url="https://example.com/",
            content="secret page body must not be written",
            title="Example Domain",
            discovered_count=1,
            started_at="2026-07-13T00:00:00+00:00",
            ended_at="2026-07-13T00:00:01+00:00",
            resources={"elapsed_ms": 1000},
        )

        self.assertEqual(record["content_sha256"], hashlib.sha256(b"secret page body must not be written").hexdigest())
        self.assertNotIn("content", record)
        self.assertNotIn("body", record)
        self.assertEqual(validate_record(record), [])

    def test_normalizes_unsupported_case_to_empty_digest(self):
        from benchmark import normalized_record

        record = normalized_record(
            candidate="fixture",
            case="crawl",
            requested_url="https://example.com/",
            final_url="https://example.com/",
            content=None,
            title=None,
            discovered_count=0,
            started_at="2026-07-13T00:00:00+00:00",
            ended_at="2026-07-13T00:00:00+00:00",
            resources={"elapsed_ms": 0},
            status="unsupported",
            error="recursive crawl is outside this reader baseline",
        )

        self.assertEqual(record["content_sha256"], hashlib.sha256(b"").hexdigest())
        self.assertEqual(record["status"], "unsupported")
        self.assertEqual(validate_record(record), [])

class CrawlBudgetTests(unittest.TestCase):
    def test_schedules_only_same_origin_unique_links_within_page_budget(self):
        from benchmark import bounded_same_origin_links

        links = bounded_same_origin_links(
            base_url="https://quotes.toscrape.com/",
            hrefs=["/page/2/", "/page/2/#fragment", "https://example.com/", "/page/3/", "/page/4/"],
            already_requested={"https://quotes.toscrape.com/"},
            remaining=2,
        )

        self.assertEqual(
            links,
            ["https://quotes.toscrape.com/page/2/", "https://quotes.toscrape.com/page/3/"],
        )

class CrawleeConfigurationTests(unittest.TestCase):
    def test_uses_explicit_single_request_concurrency_settings(self):
        from benchmark import crawlee_concurrency_settings

        settings = crawlee_concurrency_settings()
        self.assertEqual(settings.min_concurrency, 1)
        self.assertEqual(settings.max_concurrency, 1)
        self.assertEqual(settings.desired_concurrency, 1)

class RuntimeBoundTests(unittest.TestCase):
    def test_times_out_a_slow_async_operation(self):
        import asyncio
        from benchmark import run_with_timeout

        async def slow() -> str:
            await asyncio.sleep(0.05)
            return "late"

        with self.assertRaises(asyncio.TimeoutError):
            asyncio.run(run_with_timeout(slow(), timeout_seconds=0.001))


class FirecrawlAdapterTests(unittest.TestCase):
    def test_requires_an_explicit_loopback_endpoint(self):
        from benchmark import run_firecrawl

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "FIRECRAWL_ENDPOINT"):
                run_firecrawl({"name": "static", "url": "https://example.com/", "max_pages": 1})

    def test_maps_crawl_case_to_the_client_page_budget(self):
        from benchmark import run_firecrawl
        from firecrawl_client import FirecrawlResult

        class StubClient:
            def __init__(self, endpoint: str):
                self.endpoint = endpoint

            def crawl(self, url: str, *, max_pages: int):
                self.url = url
                self.max_pages = max_pages
                return FirecrawlResult("# fixture", "Fixture", url, max_pages)

        with patch("firecrawl_client.FirecrawlClient", StubClient), patch.dict(os.environ, {"FIRECRAWL_ENDPOINT": "http://127.0.0.1:13002"}):
            content, title, final_url, count = run_firecrawl({"name": "crawl", "url": "https://example.com/", "max_pages": 3})

        self.assertEqual(content, "# fixture")
        self.assertEqual(title, "Fixture")
        self.assertEqual(final_url, "https://example.com/")
        self.assertEqual(count, 3)
