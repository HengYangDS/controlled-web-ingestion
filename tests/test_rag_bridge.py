import hashlib
import json
import tempfile
import unittest
from pathlib import Path


class RagBridgeTests(unittest.TestCase):
    def _promoted_receipt(self, root: Path, *, digest: str) -> Path:
        path = root / "promoted.json"
        path.write_text(json.dumps({
            "promotion_state": "promoted",
            "content_sha256": digest,
            "purpose": "fixture",
            "source_url": "https://example.com/",
        }), encoding="utf-8")
        return path

    def test_prepare_requires_an_explicitly_promoted_receipt(self):
        from rag_bridge import BridgeError, RagBridge

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = root / "staged.json"
            receipt.write_text(json.dumps({"promotion_state": "staged"}), encoding="utf-8")
            with self.assertRaises(BridgeError):
                RagBridge(root).prepare(receipt, explicit_confirmation=True)

    def test_delivery_requires_confirmation_and_matching_in_memory_content(self):
        from rag_bridge import BridgeError, RagBridge

        content = "body remains only in memory"
        digest = hashlib.sha256(content.encode()).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self._promoted_receipt(root, digest=digest)
            bridge = RagBridge(root)
            with self.assertRaises(BridgeError):
                bridge.deliver_from_memory(receipt, content, sink=lambda _: None, explicit_confirmation=False)
            with self.assertRaises(BridgeError):
                bridge.deliver_from_memory(receipt, "tampered", sink=lambda _: None, explicit_confirmation=True)

    def test_delivery_passes_a_redacted_receipt_and_in_memory_content_to_explicit_sink(self):
        from rag_bridge import RagBridge

        content = "body remains only in memory"
        digest = hashlib.sha256(content.encode()).hexdigest()
        delivered = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = self._promoted_receipt(root, digest=digest)
            result = RagBridge(root).deliver_from_memory(
                receipt,
                content,
                sink=delivered.append,
                explicit_confirmation=True,
            )

        self.assertEqual(result["status"], "delivered")
        self.assertEqual(delivered[0]["content"], content)
        self.assertNotIn("content", result)
        self.assertEqual(result["content_sha256"], digest)
