import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("ci_projection", ROOT / "tools" / "ci" / "project.py")
project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project)


class CiProjectionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for relative in project.PROJECTIONS.values():
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
        patches = (
            mock.patch.object(project, "ROOT", self.root),
            mock.patch.object(project, "cue_executable", return_value="cue"),
            mock.patch.object(
                project, "render", side_effect=lambda _cue, name: f"{name}\n".encode()
            ),
        )
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_write_renders_every_projection_from_the_model(self):
        self.assertEqual(project.main(["--write"]), 0)
        for name, relative in project.PROJECTIONS.items():
            self.assertEqual((self.root / relative).read_bytes(), f"{name}\n".encode())
        self.assertEqual(project.main(["--check"]), 0)

    def test_check_names_each_projection_that_differs_from_the_model(self):
        project.main(["--write"])
        (self.root / ".gitlab-ci.yml").write_text("edited by hand\n", encoding="utf-8")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(project.main(["--check"]), 1)
        self.assertIn(".gitlab-ci.yml differs from .config/ci/pipeline.cue", stderr.getvalue())
        self.assertNotIn("verify.yml", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
