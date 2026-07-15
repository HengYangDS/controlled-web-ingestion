import unittest
from pathlib import Path
import tomllib


class EthosAdopterBoundaryTests(unittest.TestCase):
    def test_adopter_binding_uses_canonical_identity_and_native_proof_gates(self):
        root = Path(__file__).resolve().parents[2]
        profile_path = root / ".ethos" / "profile.toml"
        profile = profile_path.read_text(encoding="utf-8")
        profile_data = tomllib.loads(profile)
        project = (root / ".ethos" / "project.toml").read_text(encoding="utf-8")
        self.assertIn('profile_id = "controlled-web-ingestion"', profile)
        self.assertIn('root_subject = "controlled-web-ingestion"', profile)
        self.assertIn('name = "controlled-web-ingestion"', project)
        self.assertEqual(
            profile_data["proof"]["code_correctness_gates"],
            ["controlled-web-ingestion-tests", "controlled-web-ingestion-static"],
        )
        self.assertIn('behavior = "controlled-web-ingestion-tests"', profile)
        self.assertIn('static-analysis = "controlled-web-ingestion-static"', profile)
        workspace = tomllib.loads(
            (root / ".ethos" / "workspace.toml").read_text(encoding="utf-8")
        )["branch_roles"]
        self.assertEqual(workspace["release_branch"], "main")
        self.assertEqual(
            workspace["accepted_branch"], "accepted/controlled-web-ingestion"
        )
        self.assertEqual(
            workspace["candidate_branch"], "candidate/controlled-web-ingestion"
        )
        self.assertNotEqual(workspace["release_branch"], workspace["accepted_branch"])
        self.assertFalse(
            workspace["candidate_branch"].startswith(workspace["work_branch_prefix"])
        )

    def test_openspec_material_paths_cover_governance_closeout_artifacts(self):
        root = Path(__file__).resolve().parents[2]
        profile = tomllib.loads(
            (root / ".ethos" / "profile.toml").read_text(encoding="utf-8")
        )
        material_paths = set(profile["openspec"]["material_paths"])
        self.assertTrue(
            {
                "evidence/verification/**",
                "evidence/claims/**",
                "docs/evidence/**",
                "docs/history/**",
                "docs/reference/**",
                "docs/plans/**",
                "openspec/**",
            }
            <= material_paths
        )

    def test_governance_closeout_capability_is_canonical_and_archive_only(self):
        root = Path(__file__).resolve().parents[2]
        canonical = root / "openspec" / "specs" / "governance-closeout"
        self.assertTrue((canonical / "spec.md").is_file())
        self.assertTrue((canonical / "capability.toml").is_file())
        self.assertFalse(
            (root / "openspec" / "changes" / "2026-07-15-governance-closeout").exists()
        )

    def test_runtime_remains_independent_of_ethos_product_imports(self):
        root = Path(__file__).resolve().parents[2]
        runtime = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (root / "src" / "web_ingestion").rglob("*.py")
        )
        self.assertNotIn("import ethos", runtime)
        self.assertNotIn("from ethos", runtime)


if __name__ == "__main__":
    unittest.main()
