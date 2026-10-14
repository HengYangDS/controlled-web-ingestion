"""The single explicit command-line entry point for Controlled Web Ingestion."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .bridge import RagBridge
from .contracts import IngestionRequest
from .controller import IngestionController
from .runtime import stage_with_firecrawl
from .staging import StageStore
from .validation import validate_authorized_workloads


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
    bridge = subcommands.add_parser(
        "prepare-rag", help="prepare a body-redacted bridge manifest only"
    )
    bridge.add_argument("--bridge-root", required=True, type=Path)
    bridge.add_argument("--receipt", required=True, type=Path)
    bridge.add_argument("--confirm", action="store_true")
    validate = subcommands.add_parser(
        "validate-workloads",
        help="run the reviewed workload set and write one body-redacted evidence record",
    )
    validate.add_argument("--evidence", required=True, type=Path)
    return parser


def request_from_args(args: argparse.Namespace) -> IngestionRequest:
    return IngestionRequest(
        url=args.url,
        purpose=args.purpose,
        mode=args.mode,
        max_pages=args.max_pages,
        timeout_seconds=args.timeout_seconds,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(list(sys.argv[1:] if argv is None else argv))
    if args.command == "ingest":
        request = request_from_args(args)
        if request.mode == "static":
            outcome = IngestionController().ingest(request, stage_root=args.stage_root)
        else:
            # Admission runs before the disposable topology is allocated.
            IngestionController().preflight(request)
            outcome = stage_with_firecrawl(request, args.stage_root)
        print(
            json.dumps(
                {"stage_receipt": str(outcome.stage_receipt), "route": outcome.route},
                sort_keys=True,
            )
        )
        return 0
    if args.command == "promote":
        print(
            json.dumps(
                {
                    "promotion_receipt": str(
                        StageStore(args.stage_root).promote(
                            args.receipt, explicit_confirmation=args.confirm
                        )
                    )
                },
                sort_keys=True,
            )
        )
        return 0
    if args.command == "prepare-rag":
        print(
            json.dumps(
                {
                    "bridge_manifest": str(
                        RagBridge(args.bridge_root).prepare(
                            args.receipt, explicit_confirmation=args.confirm
                        )
                    )
                },
                sort_keys=True,
            )
        )
        return 0
    if args.command == "validate-workloads":
        print(
            json.dumps(
                {"evidence": str(validate_authorized_workloads(args.evidence))}, sort_keys=True
            )
        )
        return 0
    raise AssertionError(f"unknown command {args.command}")
