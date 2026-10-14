import hashlib
import tempfile
import unittest
from pathlib import Path


class RangeFetchTests(unittest.TestCase):
    def test_plans_complete_non_overlapping_ranges(self):
        from web_ingestion.supply_chain.ghcr_ranges import byte_ranges

        self.assertEqual(
            byte_ranges(total_bytes=11, chunk_bytes=4),
            [(0, 3), (4, 7), (8, 10)],
        )

    def test_reassembles_verified_blob_from_retriable_range_fetcher(self):
        from web_ingestion.supply_chain.ghcr_ranges import fetch_blob_by_ranges

        content = b"official-registry-payload"
        calls = []

        def fetch(start: int, end: int) -> bytes:
            calls.append((start, end))
            if (start, end) == (0, 7) and calls.count((start, end)) == 1:
                raise TimeoutError("transient truncation")
            return content[start : end + 1]

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "blob.gz"
            result = fetch_blob_by_ranges(
                total_bytes=len(content),
                expected_sha256=hashlib.sha256(content).hexdigest(),
                destination=destination,
                fetch_range=fetch,
                chunk_bytes=8,
                workers=2,
                max_retries=2,
            )
            self.assertEqual(result, destination)
            self.assertEqual(destination.read_bytes(), content)
            self.assertEqual(calls.count((0, 7)), 2)

    def test_refuses_to_publish_a_digest_mismatch(self):
        from web_ingestion.supply_chain.ghcr_ranges import BlobIntegrityError, fetch_blob_by_ranges

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "blob.gz"
            with self.assertRaises(BlobIntegrityError):
                fetch_blob_by_ranges(
                    total_bytes=3,
                    expected_sha256="0" * 64,
                    destination=destination,
                    fetch_range=lambda start, end: b"abc"[start : end + 1],
                    chunk_bytes=2,
                    workers=1,
                    max_retries=1,
                )
            self.assertFalse(destination.exists())

    def test_reuses_complete_parts_after_an_interrupted_attempt(self):
        from web_ingestion.supply_chain.ghcr_ranges import fetch_blob_by_ranges

        content = b"abcdefgh"
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "blob.gz"
            parts = Path(directory) / ".blob.gz.parts"
            parts.mkdir()
            (parts / "00000000.part").write_bytes(content[:4])

            def fetch(start: int, end: int) -> bytes:
                calls.append((start, end))
                return content[start : end + 1]

            fetch_blob_by_ranges(
                total_bytes=len(content),
                expected_sha256=hashlib.sha256(content).hexdigest(),
                destination=destination,
                fetch_range=fetch,
                chunk_bytes=4,
                workers=1,
                max_retries=1,
            )
            self.assertEqual(calls, [(4, 7)])
            self.assertEqual(destination.read_bytes(), content)
            self.assertFalse(parts.exists())

    def test_retains_verified_parts_after_a_later_range_fails_for_resumption(self):
        from web_ingestion.supply_chain.ghcr_ranges import BlobIntegrityError, fetch_blob_by_ranges

        content = b"abcdefgh"
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "blob.gz"

            def fetch(start: int, end: int) -> bytes:
                if start == 4:
                    raise TimeoutError("transport interrupted")
                return content[start : end + 1]

            with self.assertRaises(BlobIntegrityError):
                fetch_blob_by_ranges(
                    total_bytes=len(content),
                    expected_sha256=hashlib.sha256(content).hexdigest(),
                    destination=destination,
                    fetch_range=fetch,
                    chunk_bytes=4,
                    workers=1,
                    max_retries=1,
                )
            self.assertEqual(
                (Path(directory) / ".blob.gz.parts" / "00000000.part").read_bytes(), b"abcd"
            )
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
