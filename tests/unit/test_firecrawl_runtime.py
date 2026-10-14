import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from web_ingestion import runtime

REVIEWED = {"api": "ghcr.io/firecrawl/firecrawl@sha256:" + "a" * 64}
CLEAN = {"containers": 0, "volumes": 0, "networks": 0, "published_listener": 0}


def completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


def compose_lifecycle(*, up=None, resources=None):
    """Patch Docker at the bounded-command seam and record every Compose command."""
    commands = []

    def run(command, **_options):
        commands.append(command)
        return (up or completed()) if "up" in command else completed()

    stack = ExitStack()
    stack.enter_context(patch.object(runtime, "verify_reviewed_images", return_value=REVIEWED))
    stack.enter_context(
        patch.object(runtime, "project_resources", side_effect=resources or [CLEAN, CLEAN])
    )
    stack.enter_context(patch.object(runtime, "bounded", side_effect=run))
    return stack, commands


class RuntimeLifecycleTests(unittest.TestCase):
    def test_runtime_waits_for_health_then_removes_the_project(self):
        stack, commands = compose_lifecycle()
        with stack, runtime.firecrawl_runtime() as endpoint:
            self.assertEqual(endpoint, "http://127.0.0.1:13002")

        up, down = commands
        prefix = ["docker", "compose", "--project-name", runtime.PROJECT, "--file"]
        self.assertEqual((up[:5], down[:5]), (prefix, prefix))
        self.assertEqual(up[6:9], ["up", "--detach", "--wait"])
        self.assertEqual(down[6:], ["down", "--volumes", "--remove-orphans", "--timeout", "30"])

    def test_failure_inside_the_run_still_removes_the_project(self):
        stack, commands = compose_lifecycle()
        with stack, self.assertRaisesRegex(ValueError, "staged request failed"):
            with runtime.firecrawl_runtime():
                raise ValueError("staged request failed")
        self.assertIn("down", commands[-1])

    def test_failed_startup_is_reported_after_teardown(self):
        stack, commands = compose_lifecycle(up=completed(1, stderr="dependency failed"))
        with stack, self.assertRaisesRegex(runtime.RuntimeFailure, "dependency failed"):
            with runtime.firecrawl_runtime():
                self.fail("the body must not run when startup fails")
        self.assertIn("down", commands[-1])

    def test_remaining_resources_fail_the_run(self):
        stack, _ = compose_lifecycle(resources=[CLEAN, {**CLEAN, "volumes": 1}])
        with stack, self.assertRaisesRegex(runtime.RuntimeFailure, "teardown_incomplete"):
            with runtime.firecrawl_runtime():
                pass

    def test_a_dirty_project_is_never_started(self):
        stack, commands = compose_lifecycle(resources=[{**CLEAN, "containers": 2}])
        with stack, self.assertRaisesRegex(runtime.RuntimeFailure, "not_clean"):
            with runtime.firecrawl_runtime():
                self.fail("a dirty project must not start")
        self.assertEqual(commands, [])

    def test_each_run_receives_fresh_store_credentials(self):
        environments = []

        def run(_command, *, environment=None, **_options):
            environments.append(environment)
            return completed()

        with (
            patch.object(runtime, "verify_reviewed_images", return_value=REVIEWED),
            patch.object(runtime, "project_resources", side_effect=[CLEAN, CLEAN]),
            patch.object(runtime, "bounded", side_effect=run),
            runtime.firecrawl_runtime(),
        ):
            pass
        started, removed = environments
        self.assertEqual(started["POSTGRES_PASSWORD"], removed["POSTGRES_PASSWORD"])
        self.assertEqual(len(started["POSTGRES_PASSWORD"]), 48)
        self.assertNotEqual(started["POSTGRES_PASSWORD"], started["BULL_AUTH_KEY"])


class ImageVerificationTests(unittest.TestCase):
    def test_drifted_local_image_refuses_startup(self):
        provenance = json.loads(runtime.PROVENANCE_FILE.read_text(encoding="utf-8"))
        record = {
            "Id": "sha256:" + "f" * 64,
            "Os": "linux",
            "Architecture": "arm64",
            "RepoDigests": [runtime.pinned_reference(provenance["images"]["api"])],
        }
        with patch.object(runtime, "bounded", return_value=completed(1, json.dumps([record]))):
            with self.assertRaisesRegex(runtime.RuntimeFailure, "image_id does not match"):
                runtime.verify_reviewed_images()

    def test_unreachable_engine_is_reported_as_such(self):
        with patch.object(runtime, "bounded", return_value=completed(1, "", "Cannot connect")):
            with self.assertRaisesRegex(runtime.RuntimeFailure, "Cannot connect"):
                runtime.verify_reviewed_images()

    def test_compose_names_exactly_the_reviewed_digests(self):
        provenance = json.loads(runtime.PROVENANCE_FILE.read_text(encoding="utf-8"))
        images = [
            line.split("image:", 1)[1].strip()
            for line in runtime.COMPOSE_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("image:")
        ]
        expected = [runtime.pinned_reference(entry) for entry in provenance["images"].values()]
        self.assertEqual(sorted(images), sorted(expected))


class ProjectResourceTests(unittest.TestCase):
    def test_resources_are_counted_by_compose_label(self):
        listings = {"ps": "a\nb\n", "volume": "", "network": "n\n"}

        def run(command, **_options):
            self.assertIn(f"label=com.docker.compose.project={runtime.PROJECT}", command)
            return completed(stdout=listings[command[1]])

        with patch.object(runtime, "bounded", side_effect=run):
            counts = runtime.project_resources()
        self.assertEqual((counts["containers"], counts["volumes"], counts["networks"]), (2, 0, 1))
        self.assertIn(counts["published_listener"], (0, 1))

    def test_published_ports_accept_both_compose_output_forms(self):
        publishers = [
            {"URL": "127.0.0.1", "PublishedPort": 13002},
            {"URL": "", "PublishedPort": 0},
        ]
        service = {"Publishers": publishers}
        for stdout in (json.dumps([service]), json.dumps(service) + "\n" + json.dumps({})):
            with patch.object(runtime, "bounded", return_value=completed(stdout=stdout)):
                self.assertEqual(runtime.published_ports(), ["127.0.0.1:13002"])


@unittest.skipUnless(os.name == "posix", "process groups are POSIX")
class BoundedCommandTests(unittest.TestCase):
    def test_deadline_ends_the_whole_process_group(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "grandchild.pid"
            child = (
                "import os, time; "
                f"open({str(marker)!r}, 'w').write(str(os.getpid())); time.sleep(60)"
            )
            parent = (
                "import subprocess, sys, time; "
                f"subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(60)"
            )
            with self.assertRaises(subprocess.TimeoutExpired):
                runtime.bounded([sys.executable, "-c", parent], timeout=3)
            grandchild = int(marker.read_text(encoding="utf-8"))
        for _ in range(50):
            try:
                os.kill(grandchild, 0)
            except ProcessLookupError:
                return
            time.sleep(0.1)
        self.fail("the grandchild survived the group deadline")

    def test_completed_command_returns_its_output(self):
        result = runtime.bounded([sys.executable, "-c", "print('ready')"], timeout=10)
        self.assertEqual((result.returncode, result.stdout.strip()), (0, "ready"))


if __name__ == "__main__":
    unittest.main()
