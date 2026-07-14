import unittest
from pathlib import Path


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
        workspace = (root / ".ethos" / "workspace.toml").read_text(encoding="utf-8")
        self.assertIn('accepted_branch = "main"', workspace)
        self.assertIn('candidate_branch = "work/controlled-web-ingestion-topology"', workspace)

    def test_runtime_remains_independent_of_ethos_product_imports(self):
        root = Path(__file__).resolve().parents[2]
        runtime = "\n".join(path.read_text(encoding="utf-8") for path in (root / "src" / "web_ingestion").rglob("*.py"))
        self.assertNotIn("import ethos", runtime)
        self.assertNotIn("from ethos", runtime)


if __name__ == "__main__":
    unittest.main()
