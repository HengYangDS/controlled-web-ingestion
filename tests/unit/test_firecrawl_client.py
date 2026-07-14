import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class _FirecrawlHandler(BaseHTTPRequestHandler):
    requests: list[tuple[str, dict]] = []
    crawl_status: str = "completed"

    def log_message(self, format, *args):  # noqa: A003 - suppress test-server logs
        return

    def _json(self, status: int, payload: dict) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):  # noqa: N802 - stdlib handler contract
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        self.requests.append((self.path, body))
        if self.path == "/v1/scrape":
            self._json(200, {"success": True, "data": {"markdown": "# Fixture", "metadata": {"title": "Fixture", "sourceURL": body["url"]}}})
            return
        if self.path == "/v1/crawl":
            self._json(200, {"success": True, "id": "crawl-1"})
            return
        self._json(404, {"success": False})

    def do_GET(self):  # noqa: N802 - stdlib handler contract
        self.requests.append((self.path, {}))
        if self.path == "/v1/crawl/crawl-1":
            if self.crawl_status != "completed":
                self._json(200, {"success": True, "status": self.crawl_status})
                return
            self._json(200, {"success": True, "status": "completed", "data": [
                {"markdown": "# One", "metadata": {"title": "One", "sourceURL": "https://example.com/"}},
                {"markdown": "# Two", "metadata": {"title": "Two", "sourceURL": "https://example.com/two"}},
            ]})
            return
        self._json(404, {"success": False})

    def do_DELETE(self):  # noqa: N802 - stdlib handler contract
        self.requests.append((self.path, {}))
        self._json(200, {"success": True})


class FirecrawlClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _FirecrawlHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.endpoint = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)
        cls.server.server_close()

    def setUp(self):
        _FirecrawlHandler.requests.clear()
        _FirecrawlHandler.crawl_status = "completed"

    def test_scrape_uses_loopback_api_and_returns_only_needed_result_fields(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        result = FirecrawlClient(self.endpoint).scrape("https://example.com/")

        self.assertEqual(result.title, "Fixture")
        self.assertEqual(result.final_url, "https://example.com/")
        self.assertEqual(result.content, "# Fixture")
        self.assertEqual(_FirecrawlHandler.requests[0][0], "/v1/scrape")

    def test_crawl_polls_to_completion_and_applies_page_limit_client_side(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        result = FirecrawlClient(self.endpoint).crawl("https://example.com/", max_pages=1)

        self.assertEqual(result.discovered_count, 1)
        self.assertEqual(result.content, "# One")
        self.assertEqual(_FirecrawlHandler.requests[0][1]["limit"], 1)
        self.assertEqual(_FirecrawlHandler.requests[0][1]["maxConcurrency"], 1)
        self.assertEqual(_FirecrawlHandler.requests[0][1]["maxDiscoveryDepth"], 1)
        self.assertFalse(_FirecrawlHandler.requests[0][1]["allowBackwardLinks"])
        self.assertTrue(_FirecrawlHandler.requests[0][1]["ignoreSitemap"])
        self.assertEqual(_FirecrawlHandler.requests[0][1]["scrapeOptions"]["timeout"], 10_000)
        self.assertEqual([path for path, _ in _FirecrawlHandler.requests], ["/v1/crawl", "/v1/crawl/crawl-1"])


    def test_crawl_timeout_cancels_the_remote_job(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        _FirecrawlHandler.crawl_status = "scraping"
        with self.assertRaisesRegex(TimeoutError, "crawl-1"):
            FirecrawlClient(self.endpoint, timeout_seconds=0.01).crawl(
                "https://example.com/", max_pages=1, poll_interval_seconds=0.001
            )

        self.assertEqual(
            [path for path, _ in _FirecrawlHandler.requests][-1],
            "/v1/crawl/crawl-1",
        )

    def test_cancel_uses_the_crawl_identifier(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        FirecrawlClient(self.endpoint).cancel("crawl-1")

        self.assertEqual(_FirecrawlHandler.requests, [("/v1/crawl/crawl-1", {})])


if __name__ == "__main__":
    unittest.main()
