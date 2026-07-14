import hashlib
import json
import tempfile
import unittest
from pathlib import Path


class TargetPolicyTests(unittest.TestCase):
    def test_admits_public_https_target_with_resolved_public_address(self):
        from web_ingestion.policy import TargetPolicy, validate_target

        decision = validate_target(
            "https://example.com/articles?id=7",
            policy=TargetPolicy(),
            resolver=lambda host: ["93.184.216.34"],
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.canonical_url, "https://example.com/articles?id=7")
        self.assertEqual(decision.reason, "public_http_target")

    def test_rejects_loopback_and_private_redirect_hops(self):
        from web_ingestion.policy import TargetPolicy, validate_redirect_chain

        decision = validate_redirect_chain(
            ["https://example.com/start", "http://127.0.0.1:8888/admin"],
            policy=TargetPolicy(),
            resolver=lambda host: ["93.184.216.34"],
        )

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "blocked_ip:127.0.0.1")

    def test_rejects_a_public_name_that_resolves_to_private_space(self):
        from web_ingestion.policy import TargetPolicy, validate_target

        decision = validate_target(
            "https://public-looking.example/path",
            policy=TargetPolicy(),
            resolver=lambda host: ["10.0.0.7"],
        )

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "blocked_ip:10.0.0.7")

    def test_canonicalizes_fragment_and_tracking_without_dropping_semantic_query(self):
        from web_ingestion.policy import canonicalize_url

        self.assertEqual(
            canonicalize_url("HTTPS://Example.COM:443/a/../article?b=2&utm_source=x&a=1#part"),
            "https://example.com/article?a=1&b=2",
        )


class RobotsPolicyTests(unittest.TestCase):
    def test_records_deny_and_crawl_delay_for_the_benchmark_agent(self):
        from web_ingestion.policy import evaluate_robots

        robots = """\
User-agent: ControlledWebIngestion
Disallow: /private
Crawl-delay: 3
\nUser-agent: *
Disallow:
"""
        denied = evaluate_robots(robots, "https://example.com/private/report")
        allowed = evaluate_robots(robots, "https://example.com/public/report")

        self.assertFalse(denied.allowed)
        self.assertEqual(denied.reason, "robots_disallow")
        self.assertTrue(allowed.allowed)
        self.assertEqual(allowed.crawl_delay_seconds, 3.0)


class StagingPromotionTests(unittest.TestCase):
    def test_staging_keeps_provenance_and_explicit_promotion_is_required(self):
        from web_ingestion.policy import PromotionError
        from web_ingestion.staging import StageStore

        with tempfile.TemporaryDirectory() as directory:
            store = StageStore(Path(directory))
            record = {
                "candidate": "crawl4ai",
                "requested_url": "https://example.com/",
                "final_url": "https://example.com/",
                "source_url": "https://example.com/",
                "content_sha256": hashlib.sha256(b"body held only in memory").hexdigest(),
                "status": "success",
                "content_type": "text/html",
                "fetched_at": "2026-07-13T00:00:00+00:00",
                "parser_version": "crawl4ai@fixture",
                "robots_decision": "allowed",
                "policy_decision": "admitted",
            }
            stage_path = store.stage(record)
            staged = json.loads(stage_path.read_text())

            self.assertNotIn("body", staged)
            self.assertEqual(staged["promotion_state"], "staged")
            with self.assertRaises(PromotionError):
                store.promote(stage_path, explicit_confirmation=False)

            promotion_path = store.promote(stage_path, explicit_confirmation=True)
            promoted = json.loads(promotion_path.read_text())
            self.assertEqual(promoted["promotion_state"], "promoted")
            self.assertNotIn("rag", promoted)
            self.assertNotIn("mcp", promoted)

    def test_refuses_to_promote_failed_or_robots_denied_records(self):
        from web_ingestion.policy import PromotionError
        from web_ingestion.staging import StageStore

        with tempfile.TemporaryDirectory() as directory:
            store = StageStore(Path(directory))
            staged = store.stage({
                "candidate": "fixture",
                "requested_url": "https://example.com/private",
                "final_url": "https://example.com/private",
                "source_url": "https://example.com/private",
                "content_sha256": hashlib.sha256(b"").hexdigest(),
                "status": "skipped",
                "content_type": "text/html",
                "fetched_at": "2026-07-13T00:00:00+00:00",
                "parser_version": "fixture",
                "robots_decision": "denied",
                "policy_decision": "rejected",
            })
            with self.assertRaises(PromotionError):
                store.promote(staged, explicit_confirmation=True)


class ContentTypePolicyTests(unittest.TestCase):
    def test_accepts_html_text_and_pdf_but_rejects_executable_content(self):
        from web_ingestion.policy import is_allowed_content_type

        self.assertTrue(is_allowed_content_type("text/html; charset=utf-8"))
        self.assertTrue(is_allowed_content_type("application/pdf"))
        self.assertTrue(is_allowed_content_type("text/plain"))
        self.assertFalse(is_allowed_content_type("application/octet-stream"))


if __name__ == "__main__":
    unittest.main()
