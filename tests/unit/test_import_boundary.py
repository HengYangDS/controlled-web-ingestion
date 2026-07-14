import importlib
import unittest
from pathlib import Path


class RuntimePackageBoundaryTests(unittest.TestCase):
    def test_runtime_is_owned_by_the_src_package_not_repository_root(self):
        root = Path(__file__).resolve().parents[2]
        for module in (
            "web_ingestion",
            "web_ingestion.contracts",
            "web_ingestion.policy",
            "web_ingestion.transport",
            "web_ingestion.staging",
            "web_ingestion.controller",
            "web_ingestion.bridge",
            "web_ingestion.adapters.static",
            "web_ingestion.adapters.firecrawl",
        ):
            with self.subTest(module=module):
                self.assertIsNotNone(importlib.import_module(module))
        self.assertFalse((root / "web_ingestion.py").exists())
        self.assertFalse((root / "admission.py").exists())
        self.assertFalse((root / "web_ingest.py").exists())


if __name__ == "__main__":
    unittest.main()
