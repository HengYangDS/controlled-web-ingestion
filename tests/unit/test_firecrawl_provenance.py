import unittest

DIGEST = "sha256:" + "a" * 64
IMAGE_ID = "sha256:" + "1" * 64


def provenance(reference="ghcr.io/firecrawl/firecrawl:2.10.19"):
    return {
        "schema": "firecrawl-isolated-image-provenance-v2",
        "platform": "linux/arm64",
        "images": {
            "api": {"reference": reference, "manifest_digest": DIGEST, "local_image_id": IMAGE_ID}
        },
    }


def record(repo_digest, *, image_id=IMAGE_ID, architecture="arm64"):
    return {
        "Id": image_id,
        "RepoDigests": [repo_digest],
        "Architecture": architecture,
        "Os": "linux",
    }


class ProvenanceVerificationTests(unittest.TestCase):
    def test_accepts_exact_reviewed_arm64_image_identity(self):
        from web_ingestion.supply_chain.provenance import verify_image_records

        images = [record(f"ghcr.io/firecrawl/firecrawl@{DIGEST}")]
        self.assertEqual(verify_image_records(provenance(), images), [])

    def test_docker_hub_official_images_match_their_short_repository_digest(self):
        from web_ingestion.supply_chain.provenance import pinned_reference, verify_image_records

        reviewed = provenance("docker.io/library/redis:8.10.2-alpine")
        self.assertEqual(
            pinned_reference(reviewed["images"]["api"]), f"docker.io/library/redis@{DIGEST}"
        )
        self.assertEqual(verify_image_records(reviewed, [record(f"redis@{DIGEST}")]), [])

    def test_rejects_wrong_architecture_or_identity(self):
        from web_ingestion.supply_chain.provenance import verify_image_records

        images = [
            record(
                f"ghcr.io/firecrawl/firecrawl@{DIGEST}",
                image_id="sha256:" + "2" * 64,
                architecture="amd64",
            )
        ]
        errors = verify_image_records(provenance(), images)
        self.assertTrue(any("architecture" in error for error in errors))
        self.assertTrue(any("image_id" in error for error in errors))

    def test_rejects_a_tag_only_image_and_an_older_record_schema(self):
        from web_ingestion.supply_chain.provenance import verify_image_records

        tagged = {**record("unused"), "RepoDigests": [], "RepoTags": ["ghcr.io/x:2.10.19"]}
        self.assertTrue(verify_image_records(provenance(), [tagged])[0].startswith("api: missing"))
        older = {**provenance(), "schema": "firecrawl-isolated-image-provenance-v1"}
        self.assertIn("schema", verify_image_records(older, [])[0])


if __name__ == "__main__":
    unittest.main()
