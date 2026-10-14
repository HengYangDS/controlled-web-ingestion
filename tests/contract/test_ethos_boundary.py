import tomllib
import unittest
from pathlib import Path


class EthosAdopterBoundaryTests(unittest.TestCase):
    def test_adopter_binding_uses_canonical_identity_and_native_proof_gates(self):
        root = Path(__file__).resolve().parents[2]
        profile_path = root / ".ethos" / "profile.toml"
        profile = profile_path.read_text(encoding="utf-8")
        profile_data = tomllib.loads(profile)
        self.assertIn('profile_id = "controlled-web-ingestion"', profile)
        self.assertFalse(
            {
                "schema_version",
                "profile_version",
                "ethos_contract_version",
                "repository",
                "roots",
            }
            & set(profile_data)
        )
        self.assertEqual(
            profile_data["proof"]["code_correctness_gates"],
            [gate["id"] for gate in profile_data["proof"]["gates"]],
        )
        gates = {gate["id"]: gate for gate in profile_data["proof"]["gates"]}
        self.assertEqual(
            {
                axis: gates[gate_id].get("providers")
                for axis, gate_id in profile_data["proof"]["code_correctness_map"].items()
            },
            {
                "behavior": ["ethos.adapters.gates.code_quality:behavior_report"],
                "static-analysis": ["ethos.adapters.gates.code_quality:static_report"],
            },
        )
        workspace = tomllib.loads((root / ".ethos" / "workspace.toml").read_text(encoding="utf-8"))[
            "branch_roles"
        ]
        self.assertEqual(workspace["release_branch"], "main")
        self.assertEqual(workspace["accepted_branch"], "accepted/controlled-web-ingestion")
        self.assertEqual(workspace["candidate_branch"], "candidate/controlled-web-ingestion")
        self.assertEqual(workspace["proposal_branch_prefix"], "submit/")
        self.assertNotIn("submit_branch_prefix", workspace)
        self.assertNotEqual(workspace["release_branch"], workspace["accepted_branch"])
        self.assertFalse(workspace["candidate_branch"].startswith(workspace["work_branch_prefix"]))

    def test_openspec_material_paths_cover_governance_closeout_artifacts(self):
        root = Path(__file__).resolve().parents[2]
        profile = tomllib.loads((root / ".ethos" / "profile.toml").read_text(encoding="utf-8"))
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
        specs = root / "openspec" / "specs"
        self.assertTrue((specs / "governance-closeout" / "spec.md").is_file())
        self.assertEqual(
            sorted(path.name for path in specs.glob("*/*") if path.name != "spec.md"),
            [],
        )
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
