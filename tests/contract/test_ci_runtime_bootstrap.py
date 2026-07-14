import unittest
from pathlib import Path


class CiRuntimeBootstrapTests(unittest.TestCase):
    def test_ci_uses_a_semantic_python_runtime_bootstrap(self):
        root = Path(__file__).resolve().parents[2]
        bootstrap = root / "tools" / "ci" / "scripts" / "with-python-runtime.sh"
        self.assertTrue(bootstrap.is_file())
        text = bootstrap.read_text(encoding="utf-8")
        self.assertIn("UV_CACHE_DIR", text)
        self.assertIn("UV_PROJECT_ENVIRONMENT", text)
        self.assertIn("build/runtime", text)
        runner = root / "tools" / "ci" / "run_tests.py"
        runner_text = runner.read_text(encoding="utf-8")
        self.assertIn("sys.executable", runner_text)
        self.assertNotIn('[args.python, "-m", "unittest"', runner_text)
        projection = (root / ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertIn("tools/ci/scripts/with-python-runtime.sh", projection)
        self.assertNotIn('image: "python:${PYTHON_VERSION}-slim"', projection)
        self.assertNotIn('zricethezav/gitleaks:v8.30.0', projection)
        self.assertGreaterEqual(projection.count('command -v "python${PYTHON_VERSION}"'), 2)
        self.assertIn('export PATH="/opt/homebrew/bin:$PATH"', projection)
        self.assertIn('gitleaks version', projection)


if __name__ == "__main__":
    unittest.main()
