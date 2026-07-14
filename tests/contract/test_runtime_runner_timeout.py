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


if __name__ == "__main__":
    unittest.main()
