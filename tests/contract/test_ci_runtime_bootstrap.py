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
        projection = (root / ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertIn("tools/ci/scripts/with-python-runtime.sh", projection)
        self.assertNotIn("uv run --locked --python python python tools/ci", projection)


if __name__ == "__main__":
    unittest.main()
