"""Run the reviewed Firecrawl topology on demand under native Compose and always remove it."""

from __future__ import annotations

import json
import os
import secrets
import signal
import socket
import subprocess
import threading
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .adapters.firecrawl import FirecrawlClient
from .contracts import IngestionOutcome, IngestionRequest
from .controller import IngestionController
from .supply_chain.provenance import pinned_reference, verify_image_records

ROOT = Path(__file__).resolve().parents[2]
COMPOSE_FILE = ROOT / "system" / "projections" / "firecrawl-isolated-compose.yaml"
PROVENANCE_FILE = ROOT / "system" / "supply-chain" / "firecrawl-provenance.json"
PROJECT = "web-ingestion-firecrawl-bench"
HOST, PORT = "127.0.0.1", 13002
ENDPOINT = f"http://{HOST}:{PORT}"
STARTUP_TIMEOUT_SECONDS = 180
TEARDOWN_TIMEOUT_SECONDS = 120


class RuntimeFailure(RuntimeError):
    """The disposable topology could not be verified, started or completely removed."""


def _stop_group(process: subprocess.Popen[str]) -> None:
    """End one owned Docker client together with the plugin processes it started."""
    if os.name != "posix":
        process.kill()
        process.wait()
        return
    for stop_signal, grace_seconds in ((signal.SIGTERM, 10), (signal.SIGKILL, 10)):
        try:
            os.killpg(process.pid, stop_signal)
        except ProcessLookupError:
            break
        try:
            process.wait(timeout=grace_seconds)
            return
        except subprocess.TimeoutExpired:
            continue
    process.wait()


def bounded(
    command: list[str], *, timeout: float, environment: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    """Run one command in its own process group and end that group at the caller's deadline."""
    process = subprocess.Popen(
        command,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=os.name == "posix",
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except BaseException:
        _stop_group(process)
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                stream.close()
        raise
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def verify_reviewed_images() -> dict[str, str]:
    """Fail closed unless every local topology image is the reviewed object."""
    provenance = json.loads(PROVENANCE_FILE.read_text(encoding="utf-8"))
    references = {name: pinned_reference(entry) for name, entry in provenance["images"].items()}
    inspected = bounded(["docker", "image", "inspect", *references.values()], timeout=60)
    try:
        records = json.loads(inspected.stdout or "[]")
    except json.JSONDecodeError as error:
        raise RuntimeFailure("docker_image_inspect_unreadable") from error
    if inspected.returncode and not records:
        raise RuntimeFailure(f"docker_image_inspect_failed: {inspected.stderr.strip()[-300:]}")
    errors = verify_image_records(provenance, records)
    if errors:
        raise RuntimeFailure("firecrawl_provenance_rejected: " + "; ".join(errors))
    return references


def project_resources() -> dict[str, int]:
    """Count Compose-labelled containers, volumes and networks plus the published listener."""
    label = f"label=com.docker.compose.project={PROJECT}"
    counts: dict[str, int] = {}
    for kind, command in (
        ("containers", ["docker", "ps", "--all", "--quiet", "--filter", label]),
        ("volumes", ["docker", "volume", "ls", "--quiet", "--filter", label]),
        ("networks", ["docker", "network", "ls", "--quiet", "--filter", label]),
    ):
        listed = bounded(command, timeout=60)
        if listed.returncode:
            raise RuntimeFailure(f"docker_{kind}_unavailable: {listed.stderr.strip()[-300:]}")
        counts[kind] = len(listed.stdout.split())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(1.0)
        counts["published_listener"] = int(probe.connect_ex((HOST, PORT)) == 0)
    return counts


def published_ports() -> list[str]:
    """Return every host address and port that the running project publishes."""
    listed = bounded(
        ["docker", "compose", "--project-name", PROJECT, "ps", "--format", "json"], timeout=60
    )
    if listed.returncode:
        raise RuntimeFailure(f"docker_compose_ps_failed: {listed.stderr.strip()[-300:]}")
    text = listed.stdout.strip()
    try:
        parsed = json.loads(text or "[]")
        services = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        services = [json.loads(line) for line in text.splitlines() if line.strip()]
    return sorted(
        f"{publisher['URL']}:{publisher['PublishedPort']}"
        for service in services
        for publisher in service.get("Publishers") or []
        if publisher.get("PublishedPort")
    )


@contextmanager
def _terminate_as_exit() -> Generator[None, None, None]:
    """Turn SIGTERM into SystemExit so teardown runs; only the main thread owns signals."""
    if threading.current_thread() is not threading.main_thread():
        yield
        return

    def _exit(signum: int, _frame: Any) -> None:
        raise SystemExit(128 + signum)

    previous = signal.signal(signal.SIGTERM, _exit)
    try:
        yield
    finally:
        signal.signal(signal.SIGTERM, previous)


@contextmanager
def firecrawl_runtime(
    *, startup_timeout_seconds: int = STARTUP_TIMEOUT_SECONDS
) -> Generator[str, None, None]:
    """Yield the loopback endpoint of one fresh topology, then remove it and prove it is gone."""
    verify_reviewed_images()
    if any(project_resources().values()):
        raise RuntimeFailure("firecrawl_project_not_clean_before_start")
    environment = {
        **os.environ,
        "POSTGRES_USER": "firecrawl_bench",
        "POSTGRES_PASSWORD": secrets.token_hex(24),
        "BULL_AUTH_KEY": secrets.token_hex(24),
    }
    compose = ["docker", "compose", "--project-name", PROJECT, "--file", str(COMPOSE_FILE)]
    wait = ["--wait", "--wait-timeout", str(startup_timeout_seconds)]
    with _terminate_as_exit():
        try:
            started = bounded(
                [*compose, "up", "--detach", *wait],
                timeout=startup_timeout_seconds + 60,
                environment=environment,
            )
            if started.returncode:
                raise RuntimeFailure(f"firecrawl_startup_failed: {started.stderr.strip()[-600:]}")
            yield ENDPOINT
        finally:
            removed = bounded(
                [*compose, "down", "--volumes", "--remove-orphans", "--timeout", "30"],
                timeout=TEARDOWN_TIMEOUT_SECONDS,
                environment=environment,
            )
            remaining = project_resources()
            if removed.returncode or any(remaining.values()):
                raise RuntimeFailure(f"firecrawl_teardown_incomplete: {remaining}")


def stage_with_firecrawl(request: IngestionRequest, stage_root: Path) -> IngestionOutcome:
    """Stage one admitted browser or crawl request through a disposable Firecrawl topology."""
    with firecrawl_runtime() as endpoint:
        client = FirecrawlClient(endpoint, timeout_seconds=request.timeout_seconds)

        def browser_handler(admitted: IngestionRequest) -> tuple[str, str | None, str, int]:
            result = (
                client.crawl(admitted.url, max_pages=admitted.max_pages)
                if admitted.mode == "crawl"
                else client.scrape(admitted.url)
            )
            return result.content, result.title, result.final_url, result.discovered_count

        return IngestionController(browser_handler=browser_handler).ingest(
            request, stage_root=stage_root
        )
