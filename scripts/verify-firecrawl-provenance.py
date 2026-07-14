#!/usr/bin/env python3
"""Fail closed when local Firecrawl images drift from reviewed provenance."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from firecrawl_provenance import verify_image_records


def main() -> int:
    provenance = json.loads((ROOT / "ops" / "firecrawl-provenance.json").read_text(encoding="utf-8"))
    references = [entry["reference"] for entry in provenance["images"].values()]
    output = subprocess.run(
        ["docker", "image", "inspect", *references], check=True, capture_output=True, text=True
    ).stdout
    errors = verify_image_records(provenance, json.loads(output))
    if errors:
        print(json.dumps({"status": "rejected", "errors": errors}, sort_keys=True))
        return 1
    print(json.dumps({"status": "verified", "references": references}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
