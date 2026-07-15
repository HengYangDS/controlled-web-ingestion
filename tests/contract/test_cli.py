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


if __name__ == "__main__":
    unittest.main()


class IsolatedFirecrawlInvocationTests(unittest.TestCase):
    def test_uses_the_fixed_runner_not_a_generic_shell_command(self):
        import json
        import subprocess
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        from web_ingestion import IngestionRequest
        from web_ingestion.cli import run_isolated_firecrawl

        request = IngestionRequest(
            url="https://example.com/",
            purpose="fixture",
            mode="browser",
            max_pages=1,
            timeout_seconds=30,
        )
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "staging" / "receipt.json"
            receipt.parent.mkdir()
            receipt.write_text("{}", encoding="utf-8")
            completed = subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=json.dumps({"stage_receipt": str(receipt)}) + "\n",
                stderr="",
            )
            with patch(
                "web_ingestion.cli.subprocess.run", return_value=completed
            ) as run:
                actual = run_isolated_firecrawl(request, Path(directory))

        command = run.call_args.args[0]
        self.assertEqual(
            command[0:2],
            [
                "bash",
                str(
                    Path(__file__).resolve().parents[2]
                    / "tools"
                    / "runtime"
                    / "firecrawl-isolated-benchmark.sh"
                ),
            ],
        )
        self.assertIn("--web-ingest-request", command)
        self.assertNotIn("sh", command[2:])
        self.assertEqual(actual.name, "receipt.json")


class BrowserPreflightTests(unittest.TestCase):
    def test_browser_request_is_admitted_before_the_runner_can_start(self):
        from unittest.mock import patch

        from web_ingestion.cli import main
        from web_ingestion import IngestionError

        with (
            patch(
                "web_ingestion.cli.IngestionController.preflight",
                side_effect=IngestionError("blocked_ip:127.0.0.1"),
            ),
            patch("web_ingestion.cli.run_isolated_firecrawl") as runner,
        ):
            with self.assertRaisesRegex(IngestionError, "blocked_ip"):
                main(
                    [
                        "ingest",
                        "--url",
                        "http://127.0.0.1/",
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
                )
        runner.assert_not_called()
