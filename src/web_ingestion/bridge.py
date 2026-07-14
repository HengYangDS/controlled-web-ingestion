"""Explicit, sinkless bridge preparation."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .schema import require_valid_named


class BridgeError(ValueError):
    """A record may not cross the promotion-to-delivery boundary."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RagBridge:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.manifest_dir = root / "rag-bridge"

    @staticmethod
    def _load_promoted(receipt: Path) -> dict[str, Any]:
        try:
            record = json.loads(receipt.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise BridgeError(f"cannot read promotion receipt: {type(exc).__name__}") from exc
        if not isinstance(record, dict) or record.get("promotion_state") != "promoted":
            raise BridgeError("a promoted receipt is required")
        digest = record.get("content_sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise BridgeError("promoted receipt has no valid content digest")
        return record

    def prepare(self, receipt: Path, *, explicit_confirmation: bool) -> Path:
        if not explicit_confirmation:
            raise BridgeError("explicit confirmation is required for bridge preparation")
        record = self._load_promoted(receipt)
        manifest = {"bridge_state": "prepared", "prepared_at": utc_now(), "promotion_receipt": receipt.name, "content_sha256": record["content_sha256"], "source_url": record.get("source_url"), "purpose": record.get("purpose"), "sink": None}
        require_valid_named(manifest, "bridge-manifest")
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        output = self.manifest_dir / f"{receipt.stem}.json"
        output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return output

    def deliver_from_memory(self, receipt: Path, content: str, *, sink: Callable[[dict[str, Any]], None], explicit_confirmation: bool) -> dict[str, Any]:
        if not explicit_confirmation:
            raise BridgeError("explicit confirmation is required for delivery")
        record = self._load_promoted(receipt)
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if digest != record["content_sha256"]:
            raise BridgeError("in-memory content digest does not match promoted receipt")
        sink({"content": content, "content_sha256": digest, "source_url": record.get("source_url"), "purpose": record.get("purpose")})
        return {"status": "delivered", "delivered_at": utc_now(), "content_sha256": digest, "source_url": record.get("source_url"), "purpose": record.get("purpose")}
