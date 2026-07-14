import copy
import unittest


class SchemaContractTests(unittest.TestCase):
    def stage_receipt(self):
        return {
            "candidate": "trafilatura",
            "request_id": "a" * 24,
            "purpose": "test schema validation",
            "route": "trafilatura",
            "requested_url": "https://example.com/",
            "final_url": "https://example.com/",
            "source_url": "https://example.com/",
            "content_sha256": "a" * 64,
            "status": "success",
            "content_type": "text/html",
            "fetched_at": "2026-07-14T00:00:00+00:00",
            "parser_version": "trafilatura@m2",
            "robots_decision": "allowed",
            "policy_decision": "admitted",
            "redirect_chain": ["https://example.com/"],
            "dedupe_decision": "unique",
            "budget": {"max_pages": 1, "timeout_seconds": 30},
            "quality": {"characters": 12, "title_present": False, "discovered_count": 1},
            "promotion_state": "staged",
            "staged_at": "2026-07-14T00:00:00+00:00",
        }

    def test_stage_schema_accepts_a_redacted_receipt(self):
        from web_ingestion.schema import validate_named

        self.assertEqual(validate_named(self.stage_receipt(), "stage-receipt"), [])

    def test_stage_schema_recursively_rejects_body_like_fields(self):
        from web_ingestion.schema import validate_named

        invalid = copy.deepcopy(self.stage_receipt())
        invalid["quality"]["markdown"] = "must never persist"
        errors = validate_named(invalid, "stage-receipt")
        self.assertTrue(any("forbidden recursive key" in error for error in errors), errors)

    def test_bridge_schema_requires_a_null_default_sink(self):
        from web_ingestion.schema import validate_named

        valid = {
            "bridge_state": "prepared",
            "prepared_at": "2026-07-14T00:00:00+00:00",
            "promotion_receipt": "receipt.json",
            "content_sha256": "a" * 64,
            "source_url": "https://example.com/",
            "purpose": "test schema validation",
            "sink": None,
        }
        self.assertEqual(validate_named(valid, "bridge-manifest"), [])
        valid["sink"] = "direct-rag"
        self.assertTrue(validate_named(valid, "bridge-manifest"))


if __name__ == "__main__":
    unittest.main()
