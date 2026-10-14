import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


class RuntimeRunnerTimeoutTests(unittest.TestCase):
    def test_disposable_compose_start_and_teardown_are_process_group_bounded(self):
        root = Path(__file__).resolve().parents[2]
        helper = root / "tools" / "runtime" / "compose_with_timeout.py"
        runner = root / "tools" / "runtime" / "firecrawl-isolated-benchmark.sh"
        self.assertTrue(helper.is_file())
        helper_text = helper.read_text(encoding="utf-8")
        self.assertIn("start_new_session=True", helper_text)
        self.assertIn("killpg", helper_text)
        runner_text = runner.read_text(encoding="utf-8")
        self.assertGreaterEqual(runner_text.count("compose_with_timeout.py"), 2)
        self.assertIn("--timeout-seconds", runner_text)

    def test_isolated_runner_bounds_the_entire_detached_compose_startup_group(self):
        root = Path(__file__).resolve().parents[2]
        runner_text = (root / "tools" / "runtime" / "firecrawl-isolated-benchmark.sh").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'STARTUP_TIMEOUT_SECONDS="${FIRECRAWL_STARTUP_TIMEOUT_SECONDS:-120}"', runner_text
        )
        self.assertIn(
            '--pid-file "$COMPOSE_UP_PID_FILE" --timeout-seconds "$STARTUP_TIMEOUT_SECONDS"',
            runner_text,
        )
        self.assertIn('docker compose --project-name "$PROJECT"', runner_text)
        self.assertIn("up --detach", runner_text)

    def test_timeout_helper_records_the_detached_child_group_for_interruption_cleanup(self):
        root = Path(__file__).resolve().parents[2]
        helper = root / "tools" / "runtime" / "compose_with_timeout.py"
        with tempfile.TemporaryDirectory() as directory:
            pid_file = Path(directory) / "child.pid"
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(helper),
                    "--pid-file",
                    str(pid_file),
                    "--timeout-seconds",
                    "5",
                    "--",
                    sys.executable,
                    "-c",
                    "import time; time.sleep(2)",
                ]
            )
            for _ in range(40):
                if pid_file.is_file():
                    break
                time.sleep(0.01)
            self.assertTrue(pid_file.is_file())
            child_pid = int(pid_file.read_text(encoding="utf-8").strip())
            os.kill(child_pid, 0)
            self.assertEqual(process.wait(timeout=5), 0)
            self.assertFalse(pid_file.exists())

    def test_runner_stops_an_inflight_detached_compose_group_before_teardown(self):
        root = Path(__file__).resolve().parents[2]
        runner_text = (root / "tools" / "runtime" / "firecrawl-isolated-benchmark.sh").read_text(
            encoding="utf-8"
        )

        self.assertIn('COMPOSE_UP_PID_FILE="$WORK/compose-up.pid"', runner_text)
        self.assertIn("stop_inflight_compose_up()", runner_text)
        self.assertIn('kill -TERM -- "-$compose_pid"', runner_text)
        self.assertIn('--pid-file "$COMPOSE_UP_PID_FILE"', runner_text)


if __name__ == "__main__":
    unittest.main()
