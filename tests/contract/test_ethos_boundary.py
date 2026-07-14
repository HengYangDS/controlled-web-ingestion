import unittest
from pathlib import Path
import tomllib


class EthosAdopterBoundaryTests(unittest.TestCase):
    def test_adopter_binding_uses_canonical_identity_and_native_proof_gates(self):
        root = Path(__file__).resolve().parents[2]
        profile = (root / ".ethos" / "profile.toml").read_text(encoding="utf-8")
        project = (root / ".ethos" / "project.toml").read_text(encoding="utf-8")
        self.assertIn('profile_id = "controlled-web-ingestion"', profile)
        self.assertIn('root_subject = "controlled-web-ingestion"', profile)
        self.assertIn('name = "controlled-web-ingestion"', project)
        self.assertIn('code_correctness_gates = ["controlled-web-ingestion-tests", "controlled-web-ingestion-static"]', profile)
        self.assertIn('behavior = "controlled-web-ingestion-tests"', profile)
        self.assertIn('static-analysis = "controlled-web-ingestion-static"', profile)
        workspace = tomllib.loads(
            (root / ".ethos" / "workspace.toml").read_text(encoding="utf-8")
        )["branch_roles"]
        self.assertEqual(workspace["release_branch"], "main")
        self.assertEqual(workspace["accepted_branch"], "accepted/controlled-web-ingestion")
        self.assertEqual(workspace["candidate_branch"], "candidate/controlled-web-ingestion")
        self.assertNotEqual(workspace["release_branch"], workspace["accepted_branch"])
        self.assertFalse(workspace["candidate_branch"].startswith(workspace["work_branch_prefix"]))

    def test_runtime_remains_independent_of_ethos_product_imports(self):
        root = Path(__file__).resolve().parents[2]
        runtime = "\n".join(path.read_text(encoding="utf-8") for path in (root / "src" / "web_ingestion").rglob("*.py"))
        self.assertNotIn("import ethos", runtime)
        self.assertNotIn("from ethos", runtime)


if __name__ == "__main__":
    unittest.main()
