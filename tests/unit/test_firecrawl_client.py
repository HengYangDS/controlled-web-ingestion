import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import cast


class _FirecrawlHandler(BaseHTTPRequestHandler):
    @property
    def fixture(self) -> "_FirecrawlServer":
        return cast("_FirecrawlServer", self.server)

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
        self.fixture.requests.append((self.path, body))
        if self.path == "/v1/scrape":
            self._json(
                200,
                {
                    "success": True,
                    "data": {
                        "markdown": "# Fixture",
                        "metadata": {"title": "Fixture", "sourceURL": body["url"]},
                    },
                },
            )
            return
        if self.path == "/v1/crawl":
            self._json(200, {"success": True, "id": "crawl-1"})
            return
        self._json(404, {"success": False})

    def do_GET(self):  # noqa: N802 - stdlib handler contract
        self.fixture.requests.append((self.path, {}))
        if self.path == "/v1/crawl/crawl-1":
            if self.fixture.crawl_status != "completed":
                self._json(200, {"success": True, "status": self.fixture.crawl_status})
                return
            self._json(
                200,
                {
                    "success": True,
                    "status": "completed",
                    "data": [
                        {
                            "markdown": "# One",
                            "metadata": {"title": "One", "sourceURL": "https://example.com/"},
                        },
                        {
                            "markdown": "# Two",
                            "metadata": {"title": "Two", "sourceURL": "https://example.com/two"},
                        },
                    ],
                },
            )
            return
        self._json(404, {"success": False})

    def do_DELETE(self):  # noqa: N802 - stdlib handler contract
        self.fixture.requests.append((self.path, {}))
        self._json(200, {"success": True})


class _FirecrawlServer(ThreadingHTTPServer):
    """One test's fixture server: its own request log, and a close that waits for its handlers."""

    # server_close() joins only handler threads that are not daemons, so no request of one test can
    # still be recording when the next test starts.
    daemon_threads = False

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _FirecrawlHandler)
        self.requests: list[tuple[str, dict]] = []
        self.crawl_status = "completed"

    def handle_error(self, request, client_address):
        # A client that gives up on purpose, as the crawl-timeout test does, has closed its socket.
        if isinstance(sys.exception(), (BrokenPipeError, ConnectionResetError)):
            return
        super().handle_error(request, client_address)


class FirecrawlClientTests(unittest.TestCase):
    def setUp(self):
        self.server = _FirecrawlServer()
        thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        )
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(self._close_server)
        self.endpoint = f"http://127.0.0.1:{self.server.server_port}"

    def _close_server(self):
        """Stop serving and wait for every handler thread, so that the request log is final."""
        self.server.shutdown()
        self.server.server_close()

    def test_scrape_uses_loopback_api_and_returns_only_needed_result_fields(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        result = FirecrawlClient(self.endpoint).scrape("https://example.com/")

        self.assertEqual(result.title, "Fixture")
        self.assertEqual(result.final_url, "https://example.com/")
        self.assertEqual(result.content, "# Fixture")
        self.assertEqual(self.server.requests[0][0], "/v1/scrape")

    def test_crawl_polls_to_completion_and_applies_page_limit_client_side(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        result = FirecrawlClient(self.endpoint).crawl("https://example.com/", max_pages=1)

        self.assertEqual(result.discovered_count, 1)
        self.assertEqual(result.content, "# One")
        self.assertEqual(self.server.requests[0][1]["limit"], 1)
        self.assertEqual(self.server.requests[0][1]["maxConcurrency"], 1)
        self.assertEqual(self.server.requests[0][1]["maxDiscoveryDepth"], 1)
        self.assertFalse(self.server.requests[0][1]["allowBackwardLinks"])
        self.assertTrue(self.server.requests[0][1]["ignoreSitemap"])
        self.assertEqual(self.server.requests[0][1]["scrapeOptions"]["timeout"], 10_000)
        self.assertEqual(
            [path for path, _ in self.server.requests], ["/v1/crawl", "/v1/crawl/crawl-1"]
        )

    def test_crawl_timeout_cancels_the_remote_job(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        self.server.crawl_status = "scraping"
        with self.assertRaisesRegex(TimeoutError, "crawl-1"):
            FirecrawlClient(self.endpoint, timeout_seconds=0.2).crawl(
                "https://example.com/", max_pages=1, poll_interval_seconds=0.02
            )
        # The client gave up without waiting for its last requests; let them finish first.
        self._close_server()

        self.assertEqual(
            [path for path, _ in self.server.requests][-1],
            "/v1/crawl/crawl-1",
        )

    def test_cancel_uses_the_crawl_identifier(self):
        from web_ingestion.adapters.firecrawl import FirecrawlClient

        FirecrawlClient(self.endpoint).cancel("crawl-1")

        self.assertEqual(self.server.requests, [("/v1/crawl/crawl-1", {})])
