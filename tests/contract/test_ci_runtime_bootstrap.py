import re
import tomllib
import unittest
from pathlib import Path


def _locked_tools(root):
    """Return the tool versions that mise, the toolchain owner, declares."""
    config = (root / ".config" / "mise" / "config.toml").read_text(encoding="utf-8")
    return tomllib.loads(config)["tools"]


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
        self.assertEqual(len(python_gates), 5)
        projection = (root / ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertEqual(
            projection.count('uv run --locked --python "python${PYTHON_VERSION}" python'), 4
        )
        self.assertIn("UV_PYTHON_DOWNLOADS: never", projection)
        network = (
            'UV_HTTP_RETRIES: "10"',
            'UV_HTTP_TIMEOUT: "120"',
            'UV_CONCURRENT_DOWNLOADS: "8"',
        )
        for setting in network:
            self.assertIn(setting, projection)
        images = re.findall(r"(?m)^\s+(?:image|name): (\S+)$", projection)
        self.assertEqual(len(images), 4)
        pinned = re.compile(r"ghcr\.io/\S+@sha256:[0-9a-f]{64}")
        self.assertTrue(all(pinned.fullmatch(image) for image in images))
        tools = _locked_tools(root)
        uv_images = [image for image in images if image.startswith("ghcr.io/astral-sh/uv:")]
        self.assertEqual(len(uv_images), 3)
        self.assertTrue(
            all(
                image.startswith(f"ghcr.io/astral-sh/uv:{tools['uv']}-python3.")
                for image in uv_images
            )
        )
        gitleaks = tools["github:gitleaks/gitleaks"]
        self.assertIn(f"ghcr.io/gitleaks/gitleaks:v{gitleaks}@sha256:", projection)
        self.assertIn('if: $CI_COMMIT_REF_PROTECTED == "true"', projection)
        self.assertIn("WIB_CI_RUNNER_TAG: ci-linux-arm64-container-protected", projection)
        self.assertIn("WIB_CI_RUNNER_TAG: ci-linux-arm64-container\n", projection)
        self.assertIn("    - $WIB_CI_RUNNER_TAG", projection)
        self.assertNotIn("/opt/homebrew", projection)
        self.assertIn("gitleaks version", projection)
        self.assertIn("gitleaks git --no-banner --redact=100 --exit-code 1 .", projection)

    def test_github_actions_is_an_independent_pinned_ci_plane(self):
        root = Path(__file__).resolve().parents[2]
        workflow = root / ".github" / "workflows" / "verify.yml"
        self.assertTrue(workflow.is_file())
        projection = workflow.read_text(encoding="utf-8")
        self.assertIn("pull_request:", projection)
        self.assertIn("workflow_dispatch:", projection)
        self.assertIn("permissions:", projection)
        self.assertIn("contents: read", projection)
        actions = re.findall(r"(?m)^\s+uses: (\S+)$", projection)
        self.assertEqual(len(actions), 5)
        pinned = re.compile(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}")
        self.assertTrue(all(pinned.fullmatch(action) for action in actions))
        tools = _locked_tools(root)
        self.assertIn(f"version: {tools['uv']}\n", projection)
        gitleaks = tools["github:gitleaks/gitleaks"]
        self.assertIn(f"GITLEAKS_VERSION: {gitleaks}\n", projection)
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
