import importlib.util
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_documentation", ROOT / "tools" / "ci" / "check_documentation.py"
)
assert SPEC and SPEC.loader
CHECK_DOCUMENTATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_DOCUMENTATION)
PRETTIER_IGNORE = ROOT / ".config" / "checks" / "prettier" / "prettierignore"
# ETHOS itself keeps archived OpenSpec Changes immutable.
ETHOS_IMMUTABLE_ROOTS = frozenset({"openspec/changes/archive/"})


def immutable_record_roots():
    """Return the roots the Prettier ignore file keeps at their captured bytes."""
    roots, collecting = [], False
    for line in PRETTIER_IGNORE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            collecting = line.startswith("# Immutable records")
        elif collecting and line:
            root = (PRETTIER_IGNORE.parent / line).resolve().relative_to(ROOT)
            roots.append(f"{root.as_posix()}/")
    return roots


def unvendored(paths):
    """Return the paths whose Git attributes do not set linguist-vendored."""
    fields = subprocess.run(
        ["git", "check-attr", "-z", "--stdin", "linguist-vendored"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        input=b"".join(path.encode() + b"\0" for path in paths),
    ).stdout.split(b"\0")
    return [
        fields[index].decode()
        for index in range(0, len(fields) - 1, 3)
        if fields[index + 2] != b"set"
    ]


class DocumentationFormatTests(unittest.TestCase):
    def test_immutable_records_are_received_by_git_attributes(self):
        roots = [root for root in immutable_record_roots() if root not in ETHOS_IMMUTABLE_ROOTS]
        self.assertTrue(roots)
        listed = subprocess.run(
            ["git", "ls-files", "-z", "--", *roots], cwd=ROOT, check=True, capture_output=True
        ).stdout.decode()
        records = [path for path in listed.split("\0") if path]
        self.assertTrue(records)
        self.assertEqual(unvendored(records), [])

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
