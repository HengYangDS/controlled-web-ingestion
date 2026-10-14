import tomllib
import unittest
from pathlib import Path


class CiRuntimeBootstrapTests(unittest.TestCase):
    def test_ci_runs_owner_commands_through_locked_uv(self):
        root = Path(__file__).resolve().parents[2]
        self.assertFalse(any((root / "tools" / "ci").rglob("*.sh")))
        runner = root / "tools" / "ci" / "run_tests.py"
        runner_text = runner.read_text(encoding="utf-8")
        self.assertIn("sys.executable", runner_text)
        self.assertNotIn('[args.python, "-m", "unittest"', runner_text)
        profile = tomllib.loads((root / ".ethos" / "profile.toml").read_text(encoding="utf-8"))
        python_gates = [
            gate
            for gate in profile["proof"]["gates"]
            if gate.get("command", [])[:5] == ["uv", "run", "--locked", "--offline", "python"]
        ]
        self.assertEqual(len(python_gates), 4)
        projection = (root / ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertEqual(projection.count('uv run --locked --python "$python_bin" python'), 4)
        self.assertIn('UV_CACHE_DIR: "$CI_PROJECT_DIR/build/runtime/tool-cache/uv"', projection)
        self.assertNotIn('image: "python:${PYTHON_VERSION}-slim"', projection)
        self.assertNotIn("zricethezav/gitleaks:v8.30.0", projection)
        self.assertGreaterEqual(projection.count('command -v "python${PYTHON_VERSION}"'), 2)
        self.assertIn('export PATH="/opt/homebrew/bin:$PATH"', projection)
        self.assertIn("gitleaks version", projection)

    def test_github_actions_is_an_independent_pinned_ci_plane(self):
        root = Path(__file__).resolve().parents[2]
        workflow = root / ".github" / "workflows" / "verify.yml"
        self.assertTrue(workflow.is_file())
        projection = workflow.read_text(encoding="utf-8")
        self.assertIn("pull_request:", projection)
        self.assertIn("workflow_dispatch:", projection)
        self.assertIn("permissions:", projection)
        self.assertIn("contents: read", projection)
        self.assertIn("actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683", projection)
        self.assertIn("actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065", projection)
        self.assertIn("astral-sh/setup-uv@22695119d769bdb6f7032ad67b9bca0ef8c4a174", projection)
        self.assertIn(
            "gitleaks/gitleaks-action@ff98106e4c7b2bc287b24eaf42907196329070c7", projection
        )
        self.assertIn('GITLEAKS_VERSION: "8.30.0"', projection)
        self.assertIn("gitleaks git --no-banner --redact=100 --exit-code 1 .", projection)
        self.assertNotIn("@v", projection)
        self.assertIn("tools/ci/run_tests.py", projection)
        self.assertIn("tools/ci/validate_schemas.py", projection)
        self.assertIn("tools/ci/check_documentation.py", projection)
        self.assertIn("tools/ci/check_source_topology.py", projection)
        self.assertEqual(projection.count("uv run --locked --python python python"), 5)
        self.assertIn("build/runtime/tool-cache/uv", projection)
        self.assertNotIn("unittest discover", projection)
        self.assertNotIn("bash -n", projection)


if __name__ == "__main__":
    unittest.main()
