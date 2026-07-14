import gzip
import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path


class DockerArchiveTests(unittest.TestCase):
    def test_builds_a_docker_load_archive_from_verified_config_and_gzip_layer(self):
        from web_ingestion.supply_chain.ghcr_archive import build_docker_archive

        config = b'{"architecture":"arm64","rootfs":{"type":"layers","diff_ids":[]}}'
        layer_tar = io.BytesIO()
        with tarfile.open(fileobj=layer_tar, mode="w") as archive:
            info = tarfile.TarInfo("fixture.txt")
            body = b"fixture layer"
            info.size = len(body)
            archive.addfile(info, io.BytesIO(body))
        compressed = gzip.compress(layer_tar.getvalue())

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blob = root / "layer.gz"
            blob.write_bytes(compressed)
            archive_path = root / "image.tar"
            build_docker_archive(
                config_bytes=config,
                config_digest=f"sha256:{hashlib.sha256(config).hexdigest()}",
                layer_blobs=[(f"sha256:{hashlib.sha256(compressed).hexdigest()}", blob)],
                repository="ghcr.io/example/fixture",
                tag="fixed",
                output=archive_path,
            )

            with tarfile.open(archive_path) as archive:
                manifest = json.load(archive.extractfile("manifest.json"))
                self.assertEqual(manifest[0]["RepoTags"], ["ghcr.io/example/fixture:fixed"])
                layer_path = manifest[0]["Layers"][0]
                extracted = archive.extractfile(layer_path).read()
                with tarfile.open(fileobj=io.BytesIO(extracted)) as layer:
                    self.assertEqual(layer.extractfile("fixture.txt").read(), b"fixture layer")

    def test_rejects_a_blob_that_does_not_match_declared_digest(self):
        from web_ingestion.supply_chain.ghcr_archive import ImageArchiveError, build_docker_archive

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blob = root / "layer.gz"
            blob.write_bytes(gzip.compress(b"not-a-tar"))
            with self.assertRaises(ImageArchiveError):
                build_docker_archive(
                    config_bytes=b"{}",
                    config_digest=f"sha256:{hashlib.sha256(b'{}').hexdigest()}",
                    layer_blobs=[("sha256:" + "0" * 64, blob)],
                    repository="ghcr.io/example/fixture",
                    tag="fixed",
                    output=root / "image.tar",
                )


if __name__ == "__main__":
    unittest.main()
