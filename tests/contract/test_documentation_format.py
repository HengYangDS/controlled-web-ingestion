import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_documentation", ROOT / "tools" / "ci" / "check_documentation.py"
)
assert SPEC and SPEC.loader
CHECK_DOCUMENTATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_DOCUMENTATION)


class DocumentationFormatTests(unittest.TestCase):
    def test_tracked_text_layout_passes_repository_policy(self):
        failures = [
            failure
            for path in CHECK_DOCUMENTATION.tracked_text_paths()
            for failure in CHECK_DOCUMENTATION.text_layout_failures(path)
        ]
        self.assertEqual(failures, [])

    def test_blank_line_policy_rejects_decorative_and_excessive_gaps(self):
        scratch = ROOT / "build" / "runtime" / "work" / "format-policy-fixture.txt"
        scratch.parent.mkdir(parents=True, exist_ok=True)
        self.addCleanup(scratch.unlink, missing_ok=True)
        scratch.write_text("first\n\n\n\nsecond\n", encoding="utf-8")
        failures = CHECK_DOCUMENTATION.text_layout_failures(scratch)
        self.assertIn(
            "three or more consecutive blank lines: build/runtime/work/format-policy-fixture.txt:2",
            failures,
        )

    def test_non_python_text_policy_rejects_double_blank_lines(self):
        scratch = ROOT / "build" / "runtime" / "work" / "format-policy-fixture.md"
        scratch.parent.mkdir(parents=True, exist_ok=True)
        self.addCleanup(scratch.unlink, missing_ok=True)
        scratch.write_text("first\n\n\nsecond\n", encoding="utf-8")
        failures = CHECK_DOCUMENTATION.text_layout_failures(scratch)
        self.assertIn(
            "multiple consecutive blank lines outside Python: "
            "build/runtime/work/format-policy-fixture.md:2",
            failures,
        )

    def test_python_policy_permits_pep8_module_spacing(self):
        scratch = ROOT / "build" / "runtime" / "work" / "format-policy-fixture.py"
        scratch.parent.mkdir(parents=True, exist_ok=True)
        self.addCleanup(scratch.unlink, missing_ok=True)
        scratch.write_text(
            "def first():\n    return 1\n\n\ndef second():\n    return 2\n",
            encoding="utf-8",
        )
        self.assertEqual(CHECK_DOCUMENTATION.text_layout_failures(scratch), [])

    def test_python_policy_rejects_single_blank_line_between_module_definitions(self):
        scratch = ROOT / "build" / "runtime" / "work" / "format-policy-fixture.py"
        scratch.parent.mkdir(parents=True, exist_ok=True)
        self.addCleanup(scratch.unlink, missing_ok=True)
        scratch.write_text(
            "def first():\n    return 1\n\ndef second():\n    return 2\n",
            encoding="utf-8",
        )
        failures = CHECK_DOCUMENTATION.text_layout_failures(scratch)
        self.assertIn(
            "Python module-level definitions require two blank lines: "
            "build/runtime/work/format-policy-fixture.py:4",
            failures,
        )

    def test_python_policy_permits_a_standalone_main_guard_between_definitions(self):
        scratch = ROOT / "build" / "runtime" / "work" / "format-policy-fixture.py"
        scratch.parent.mkdir(parents=True, exist_ok=True)
        self.addCleanup(scratch.unlink, missing_ok=True)
        scratch.write_text(
            "class First:\n    pass\n\n\n"
            'if __name__ == "__main__":\n    unittest.main()\n\n'
            "class Second:\n    pass\n",
            encoding="utf-8",
        )
        self.assertEqual(CHECK_DOCUMENTATION.text_layout_failures(scratch), [])

    def test_json_policy_rejects_decorative_blank_lines(self):
        scratch = ROOT / "build" / "runtime" / "work" / "format-policy-fixture.json"
        scratch.parent.mkdir(parents=True, exist_ok=True)
        self.addCleanup(scratch.unlink, missing_ok=True)
        scratch.write_text('{\n\n  "key": "value"\n}\n', encoding="utf-8")
        failures = CHECK_DOCUMENTATION.text_layout_failures(scratch)
        self.assertIn(
            "decorative blank line in machine-readable file: "
            "build/runtime/work/format-policy-fixture.json:2",
            failures,
        )


if __name__ == "__main__":
    unittest.main()
