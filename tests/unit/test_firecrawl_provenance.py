import unittest


class ProvenanceVerificationTests(unittest.TestCase):
    def test_accepts_exact_reviewed_arm64_image_identity(self):
        from web_ingestion.supply_chain.provenance import verify_image_records

        provenance = {
            "platform": "linux/arm64",
            "images": {
                "api": {
                    "reference": "ghcr.io/firecrawl/firecrawl:2.10.19",
                    "manifest_digest": "sha256:" + "a" * 64,
                    "local_image_id": "sha256:" + "1" * 64,
                }
            },
        }
        images = [{
            "Id": "sha256:" + "1" * 64,
            "RepoTags": ["ghcr.io/firecrawl/firecrawl:2.10.19"],
            "Architecture": "arm64",
            "Os": "linux",
        }]

        self.assertEqual(verify_image_records(provenance, images), [])

    def test_rejects_wrong_architecture_or_identity(self):
        from web_ingestion.supply_chain.provenance import verify_image_records

        provenance = {
            "platform": "linux/arm64",
            "images": {
                "api": {
                    "reference": "ghcr.io/firecrawl/firecrawl:2.10.19",
                    "manifest_digest": "sha256:" + "a" * 64,
                    "local_image_id": "sha256:" + "1" * 64,
                }
            },
        }
        images = [{
            "Id": "sha256:" + "2" * 64,
            "RepoTags": ["ghcr.io/firecrawl/firecrawl:2.10.19"],
            "Architecture": "amd64",
            "Os": "linux",
        }]

        errors = verify_image_records(provenance, images)
        self.assertTrue(any("architecture" in error for error in errors))
        self.assertTrue(any("image_id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
