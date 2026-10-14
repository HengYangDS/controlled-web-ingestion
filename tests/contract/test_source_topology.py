import unittest
from pathlib import Path


class SourceTopologyTests(unittest.TestCase):
    def test_runtime_and_tool_owners_have_no_flat_compatibility_surface(self):
        root = Path(__file__).resolve().parents[2]
        self.assertFalse(any(root.glob("*.py")))
        self.assertFalse((root / "scripts").exists())
        self.assertFalse((root / "ops").exists())
        runtime_sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (root / "src" / "web_ingestion").rglob("*.py")
        )
        self.assertNotIn("tools.benchmark", runtime_sources)
        self.assertNotIn("run_framework_comparison", runtime_sources)

    def test_ci_is_a_thin_projection_over_owner_scripts(self):
        root = Path(__file__).resolve().parents[2]
        for path in (
            root / "tools" / "ci" / "run_tests.py",
            root / "tools" / "ci" / "check_documentation.py",
            root / "tools" / "ci" / "check_source_topology.py",
        ):
            with self.subTest(path=path):
                self.assertTrue(path.is_file())
        projection = (root / ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertIn("tools/ci/run_tests.py", projection)
        self.assertIn("tools/ci/validate_schemas.py", projection)
        self.assertIn("tools/ci/check_documentation.py", projection)
        self.assertIn("tools/ci/check_source_topology.py", projection)
        self.assertIn("gitleaks git --no-banner --redact=100 --exit-code 1 .", projection)
        self.assertNotIn("unittest discover", projection)
        self.assertNotIn("bash -n", projection)

    def test_both_hosted_ci_planes_are_repository_owned(self):
        root = Path(__file__).resolve().parents[2]
        gitlab = root / ".gitlab-ci.yml"
        github = root / ".github" / "workflows" / "verify.yml"
        self.assertTrue(gitlab.is_file())
        self.assertTrue(github.is_file())
        for command in (
            "tools/ci/run_tests.py",
            "tools/ci/validate_schemas.py",
            "tools/ci/check_documentation.py",
            "tools/ci/check_source_topology.py",
            "gitleaks git --no-banner --redact=100 --exit-code 1 .",
        ):
            with self.subTest(command=command):
                self.assertIn(command, gitlab.read_text(encoding="utf-8"))
                self.assertIn(command, github.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
