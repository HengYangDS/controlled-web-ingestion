#!/usr/bin/env python3
"""The single explicit command-line entry point for Web-Ingestion."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from admission import StageStore
from firecrawl_client import FirecrawlClient
from rag_bridge import RagBridge
from web_ingestion import IngestionController, IngestionRequest


ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / "scripts" / "firecrawl-isolated-benchmark.sh"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    ingest = subcommands.add_parser("ingest", help="admit, collect, and stage one request")
    ingest.add_argument("--url", required=True)
    ingest.add_argument("--purpose", required=True)
    ingest.add_argument("--mode", required=True, choices=("static", "browser", "crawl"))
    ingest.add_argument("--max-pages", type=int, required=True)
    ingest.add_argument("--timeout-seconds", type=float, required=True)
    ingest.add_argument("--stage-root", required=True, type=Path)

    promote = subcommands.add_parser("promote", help="explicitly promote one staging receipt")
    promote.add_argument("--stage-root", required=True, type=Path)
    promote.add_argument("--receipt", required=True, type=Path)
    promote.add_argument("--confirm", action="store_true")

    bridge = subcommands.add_parser("prepare-rag", help="prepare a body-redacted bridge manifest only")
    bridge.add_argument("--bridge-root", required=True, type=Path)
    bridge.add_argument("--receipt", required=True, type=Path)
    bridge.add_argument("--confirm", action="store_true")
    return parser


def _request(args: argparse.Namespace) -> IngestionRequest:
    return IngestionRequest(
        url=args.url,
        purpose=args.purpose,
        mode=args.mode,
        max_pages=args.max_pages,
        timeout_seconds=args.timeout_seconds,
    )


def run_isolated_firecrawl(request: IngestionRequest, stage_root: Path) -> Path:
    """Invoke only the fixed disposable runner with a serialized request file."""
    request_file = stage_root / ".firecrawl-request.json"
    request_file.parent.mkdir(parents=True, exist_ok=True)
    request_file.write_text(json.dumps({
        "url": request.url,
        "purpose": request.purpose,
        "mode": request.mode,
        "max_pages": request.max_pages,
        "timeout_seconds": request.timeout_seconds,
        "stage_root": str(stage_root),
    }), encoding="utf-8")
    try:
        completed = subprocess.run(
            ["bash", str(RUNNER), "--web-ingest-request", str(request_file)],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        request_file.unlink(missing_ok=True)
    for line in reversed(completed.stdout.splitlines()):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        receipt = payload.get("stage_receipt")
        if isinstance(receipt, str):
            return Path(receipt)
    raise RuntimeError("controlled Firecrawl runner did not return a stage receipt")


def _internal_firecrawl_stage(request_file: Path) -> int:
    """Called only inside the disposable runner, after it has bound loopback API."""
    payload = json.loads(request_file.read_text(encoding="utf-8"))
    request = IngestionRequest(
        url=payload["url"],
        purpose=payload["purpose"],
        mode=payload["mode"],
        max_pages=int(payload["max_pages"]),
        timeout_seconds=float(payload["timeout_seconds"]),
    )
    endpoint = os.environ.get("FIRECRAWL_ENDPOINT")
    if not endpoint:
        raise RuntimeError("internal Firecrawl stage requires a runner-supplied loopback endpoint")
    client = FirecrawlClient(endpoint, timeout_seconds=request.timeout_seconds)

    def browser_handler(admitted: IngestionRequest):
        if admitted.mode == "crawl":
            result = client.crawl(admitted.url, max_pages=admitted.max_pages)
        else:
            result = client.scrape(admitted.url)
        return result.content, result.title, result.final_url, result.discovered_count

    outcome = IngestionController(browser_handler=browser_handler).ingest(
        request,
        stage_root=Path(payload["stage_root"]),
    )
    print(json.dumps({"stage_receipt": str(outcome.stage_receipt), "route": outcome.route}, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    values = list(sys.argv[1:] if argv is None else argv)
    if values[:1] == ["--internal-firecrawl-stage"]:
        if len(values) != 2:
            raise SystemExit("--internal-firecrawl-stage requires exactly one request file")
        return _internal_firecrawl_stage(Path(values[1]))
    args = build_parser().parse_args(values)
    if args.command == "ingest":
        request = _request(args)
        if request.mode == "static":
            outcome = IngestionController().ingest(request, stage_root=args.stage_root)
            print(json.dumps({"stage_receipt": str(outcome.stage_receipt), "route": outcome.route}, sort_keys=True))
            return 0
        # Fail at the outer admission boundary before allocating the disposable
        # Firecrawl service. The isolated child repeats this check defensively.
        IngestionController().preflight(request)
        receipt = run_isolated_firecrawl(request, args.stage_root)
        print(json.dumps({"stage_receipt": str(receipt), "route": "firecrawl"}, sort_keys=True))
        return 0
    if args.command == "promote":
        output = StageStore(args.stage_root).promote(args.receipt, explicit_confirmation=args.confirm)
        print(json.dumps({"promotion_receipt": str(output)}, sort_keys=True))
        return 0
    if args.command == "prepare-rag":
        output = RagBridge(args.bridge_root).prepare(args.receipt, explicit_confirmation=args.confirm)
        print(json.dumps({"bridge_manifest": str(output)}, sort_keys=True))
        return 0
    raise AssertionError(f"unknown command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
