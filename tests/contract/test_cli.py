import unittest


class CliContractTests(unittest.TestCase):
    def test_ingest_parser_requires_explicit_operational_arguments(self):
        from web_ingestion.cli import build_parser

        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["ingest", "--url", "https://example.com/"])

        args = parser.parse_args(
            [
                "ingest",
                "--url",
                "https://example.com/",
                "--purpose",
                "fixture",
                "--mode",
                "static",
                "--max-pages",
                "1",
                "--timeout-seconds",
                "30",
                "--stage-root",
                "/tmp/stage",
            ]
        )
        self.assertEqual(args.mode, "static")
        self.assertEqual(args.max_pages, 1)

    def test_validate_workloads_requires_an_explicit_evidence_path(self):
        from web_ingestion.cli import build_parser

        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["validate-workloads"])
        args = parser.parse_args(["validate-workloads", "--evidence", "/tmp/evidence.json"])
        self.assertEqual(str(args.evidence), "/tmp/evidence.json")


BROWSER_ARGS = [
    "ingest",
    "--url",
    "https://example.com/",
    "--purpose",
    "fixture",
    "--mode",
    "browser",
    "--max-pages",
    "1",
    "--timeout-seconds",
    "30",
    "--stage-root",
    "/tmp/stage",
]


class BrowserRouteTests(unittest.TestCase):
    def test_browser_request_is_staged_through_the_disposable_runtime(self):
        import io
        import json
        from contextlib import redirect_stdout
        from pathlib import Path
        from unittest.mock import patch

        from web_ingestion.cli import main
        from web_ingestion.contracts import IngestionOutcome

        outcome = IngestionOutcome("request", "firecrawl", Path("/tmp/stage/staging/r.json"), "")
        with (
            patch("web_ingestion.cli.IngestionController.preflight") as preflight,
            patch("web_ingestion.cli.stage_with_firecrawl", return_value=outcome) as runtime,
            redirect_stdout(io.StringIO()) as printed,
        ):
            self.assertEqual(main(BROWSER_ARGS), 0)

        preflight.assert_called_once()
        request, stage_root = runtime.call_args.args
        self.assertEqual((request.mode, stage_root), ("browser", Path("/tmp/stage")))
        self.assertEqual(json.loads(printed.getvalue())["route"], "firecrawl")

    def test_browser_request_is_admitted_before_the_runtime_can_start(self):
        from unittest.mock import patch

        from web_ingestion import IngestionError
        from web_ingestion.cli import main

        private = [*BROWSER_ARGS]
        private[2] = "http://127.0.0.1/"
        with (
            patch(
                "web_ingestion.cli.IngestionController.preflight",
                side_effect=IngestionError("blocked_ip:127.0.0.1"),
            ),
            patch("web_ingestion.cli.stage_with_firecrawl") as runtime,
        ):
            with self.assertRaisesRegex(IngestionError, "blocked_ip"):
                main(private)
        runtime.assert_not_called()


if __name__ == "__main__":
    unittest.main()
