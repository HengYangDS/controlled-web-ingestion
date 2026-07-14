"""Filesystem-only receipt staging and explicit promotion."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .schema import require_valid_named
from .policy import (
    FORBIDDEN_PERSISTENCE_FIELDS,
    STAGE_OPERATIONAL_FIELDS,
    STAGE_REQUIRED_FIELDS,
    PromotionError,
    is_allowed_content_type,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_stage_record(record: dict[str, object]) -> None:
    missing = sorted(STAGE_REQUIRED_FIELDS - record.keys())
    if missing:
        raise PromotionError(f"stage record missing fields: {', '.join(missing)}")
    forbidden = sorted(FORBIDDEN_PERSISTENCE_FIELDS & record.keys())
    if forbidden:
        raise PromotionError(f"stage record has forbidden fields: {', '.join(forbidden)}")
    digest = record.get("content_sha256")
    if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise PromotionError("stage record needs a lowercase SHA-256 content digest")
    if "route" in record:
        operational_missing = sorted(STAGE_OPERATIONAL_FIELDS - record.keys())
        if operational_missing:
            raise PromotionError(f"operational stage record missing fields: {', '.join(operational_missing)}")
        if not isinstance(record.get("purpose"), str) or not str(record["purpose"]).strip():
            raise PromotionError("operational stage record needs a non-empty purpose")


class StageStore:
    """A filesystem-only staging ledger with explicit, non-RAG promotion."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.staging_dir = root / "staging"
        self.promotion_dir = root / "promoted"

    def stage(self, record: dict[str, object]) -> Path:
        validate_stage_record(record)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        persisted = dict(record)
        persisted["promotion_state"] = "staged"
        persisted["staged_at"] = utc_now()
        require_valid_named(persisted, "stage-receipt")
        normalized = json.dumps(persisted, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        path = self.staging_dir / f"{hashlib.sha256(normalized.encode('utf-8')).hexdigest()}.json"
        path.write_text(json.dumps(persisted, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def promote(self, stage_path: Path, *, explicit_confirmation: bool) -> Path:
        if not explicit_confirmation:
            raise PromotionError("explicit confirmation is required for promotion")
        try:
            record = json.loads(stage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PromotionError(f"cannot read staged record: {type(exc).__name__}") from exc
        if not isinstance(record, dict):
            raise PromotionError("staged record must be a JSON object")
        validate_stage_record(record)
        if record.get("promotion_state") != "staged":
            raise PromotionError("only staged records may be promoted")
        if record.get("status") != "success":
            raise PromotionError("only successful records may be promoted")
        if record.get("dedupe_decision") == "duplicate":
            raise PromotionError("duplicate content may not be promoted")
        if record.get("policy_decision") != "admitted":
            raise PromotionError("policy must admit the record before promotion")
        if record.get("robots_decision") != "allowed":
            raise PromotionError("robots policy must allow the record before promotion")
        if not is_allowed_content_type(str(record.get("content_type"))):
            raise PromotionError("content type is not eligible for promotion")
        self.promotion_dir.mkdir(parents=True, exist_ok=True)
        record["promotion_state"] = "promoted"
        record["promoted_at"] = utc_now()
        require_valid_named(record, "promotion-receipt")
        output = self.promotion_dir / stage_path.name
        output.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return output
