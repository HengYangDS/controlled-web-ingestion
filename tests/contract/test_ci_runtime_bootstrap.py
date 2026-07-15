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

    def test_github_actions_is_an_independent_pinned_ci_plane(self):
        root = Path(__file__).resolve().parents[2]
        workflow = root / ".github" / "workflows" / "verify.yml"
        self.assertTrue(workflow.is_file())
        projection = workflow.read_text(encoding="utf-8")
        self.assertIn("pull_request:", projection)
        self.assertIn("workflow_dispatch:", projection)
        self.assertIn("permissions:", projection)
        self.assertIn("contents: read", projection)
        self.assertIn('actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683', projection)
        self.assertIn('actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065', projection)
        self.assertIn('astral-sh/setup-uv@22695119d769bdb6f7032ad67b9bca0ef8c4a174', projection)
        self.assertIn('gitleaks/gitleaks-action@ff98106e4c7b2bc287b24eaf42907196329070c7', projection)
        self.assertIn('GITLEAKS_VERSION: "8.30.0"', projection)
        self.assertIn("tools/ci/run_security_checks.sh", projection)
        self.assertNotIn("@v", projection)
        self.assertIn("tools/ci/run_tests.py", projection)
        self.assertIn("tools/ci/validate_schemas.py", projection)
        self.assertIn("tools/ci/check_documentation.py", projection)
        self.assertIn("tools/ci/check_source_topology.py", projection)
        self.assertIn("tools/ci/run_security_checks.sh", projection)
        self.assertNotIn("unittest discover", projection)
        self.assertNotIn("bash -n", projection)


if __name__ == "__main__":
    unittest.main()
