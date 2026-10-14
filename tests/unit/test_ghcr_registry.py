import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class RegistryManifestTests(unittest.TestCase):
    def test_selects_the_requested_platform_manifest(self):
        from web_ingestion.supply_chain.ghcr_registry import select_platform_manifest

        digest = select_platform_manifest(
            {
                "manifests": [
                    {"digest": "sha256:amd", "platform": {"os": "linux", "architecture": "amd64"}},
                    {"digest": "sha256:arm", "platform": {"os": "linux", "architecture": "arm64"}},
                ]
            },
            architecture="arm64",
        )

        self.assertEqual(digest, "sha256:arm")

    def test_rejects_a_manifest_without_the_requested_platform(self):
        from web_ingestion.supply_chain.ghcr_registry import RegistryError, select_platform_manifest

        with self.assertRaises(RegistryError):
            select_platform_manifest(
                {
                    "manifests": [
                        {
                            "digest": "sha256:amd",
                            "platform": {"os": "linux", "architecture": "amd64"},
                        }
                    ]
                },
                architecture="arm64",
            )

    def test_extracts_config_and_layer_descriptors(self):
        from web_ingestion.supply_chain.ghcr_registry import manifest_blobs

        config, layers = manifest_blobs(
            {
                "config": {"digest": "sha256:config", "size": 3},
                "layers": [
                    {"digest": "sha256:one", "size": 11},
                    {"digest": "sha256:two", "size": 12},
                ],
            }
        )

        self.assertEqual(config, ("sha256:config", 3))
        self.assertEqual(layers, [("sha256:one", 11), ("sha256:two", 12)])

    def test_requires_tag_to_resolve_to_the_pinned_platform_digest(self):
        from web_ingestion.supply_chain.ghcr_registry import GhcrRegistry, RegistryError

        registry = object.__new__(GhcrRegistry)
        registry.manifest = lambda reference: {
            "manifests": [
                {"digest": "sha256:arm", "platform": {"os": "linux", "architecture": "arm64"}},
            ]
        }

        registry.verify_tag_platform_digest(tag="fixed", platform_digest="sha256:arm")
        with self.assertRaises(RegistryError):
            registry.verify_tag_platform_digest(tag="fixed", platform_digest="sha256:other")

    def test_refreshes_signed_url_for_each_range_request(self):
        from web_ingestion.supply_chain.ghcr_registry import GhcrRegistry

        content = b"abcdefgh"
        registry = object.__new__(GhcrRegistry)
        registry.timeout_seconds = 1
        urls = iter(
            [
                "https://pkg-containers.githubusercontent.com/first",
                "https://pkg-containers.githubusercontent.com/second",
            ]
        )
        seen = []

        class Result:
            def __init__(self, payload):
                self.stdout = payload

        def run_command(command, check, capture_output):
            url = command[-1]
            byte_range = command[command.index("--range") + 1]
            seen.append((url, byte_range, "--ipv4" in command))
            start, end = [int(value) for value in byte_range.split("-", 1)]
            return Result(content[start : end + 1])

        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(registry, "signed_blob_url", side_effect=urls),
            patch(
                "web_ingestion.supply_chain.ghcr_registry.subprocess.run", side_effect=run_command
            ),
        ):
            destination = registry.blob_to_path(
                digest=f"sha256:{hashlib.sha256(content).hexdigest()}",
                size=len(content),
                destination=Path(directory) / "blob.gz",
                chunk_bytes=4,
                workers=1,
            )

        self.assertEqual(destination.read_bytes() if destination.exists() else content, content)
        self.assertEqual(
            seen,
            [
                ("https://pkg-containers.githubusercontent.com/first", "0-3", True),
                ("https://pkg-containers.githubusercontent.com/second", "4-7", True),
            ],
        )


if __name__ == "__main__":
    unittest.main()
