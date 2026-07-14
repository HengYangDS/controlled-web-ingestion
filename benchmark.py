#!/usr/bin/env python3
"""Run one body-redacted web-ingestion benchmark case at a time.

The command deliberately keeps fetched page bodies in process memory only.  The
result JSON is an evidence record, not a content cache.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import resource
import sys
import time
import urllib.robotparser
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urldefrag, urljoin, urlparse


ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT / ".runtime"
REQUIRED_FIELDS = {
    "candidate",
    "case",
    "requested_url",
    "final_url",
    "started_at",
    "ended_at",
    "status",
    "content_sha256",
    "title",
    "source_url",
    "discovered_count",
    "error",
    "resources",
    "artifacts",
}
FORBIDDEN_FIELDS = {"body", "content", "html", "markdown", "raw_response"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TITLE_RE = re.compile(r"<title[^>]*>\s*(.*?)\s*</title>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
USER_AGENT = "AgenticWebIngestionBenchmark/0.1 (+local, contact: disabled)"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return deterministic contract violations without retaining fetched content."""
    errors: list[str] = []
    for field in sorted(REQUIRED_FIELDS - record.keys()):
        errors.append(f"missing required field {field}")
    for field in sorted(FORBIDDEN_FIELDS & record.keys()):
        errors.append(f"forbidden field {field}")
    digest = record.get("content_sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append("content_sha256 must be a lowercase 64-character SHA-256 digest")
    return errors


def normalized_record(
    *,
    candidate: str,
    case: str,
    requested_url: str,
    final_url: str,
    content: str | None,
    title: str | None,
    discovered_count: int,
    started_at: str,
    ended_at: str,
    resources: dict[str, Any],
    status: str = "success",
    error: str | None = None,
    artifacts: list[str] | None = None,
) -> dict[str, Any]:
    """Create a complete record while hashing, rather than persisting, content."""
    return {
        "candidate": candidate,
        "case": case,
        "requested_url": requested_url,
        "final_url": final_url,
        "started_at": started_at,
        "ended_at": ended_at,
        "status": status,
        "content_sha256": hashlib.sha256((content or "").encode("utf-8")).hexdigest(),
        "title": title,
        "source_url": final_url,
        "discovered_count": discovered_count,
        "error": error,
        "resources": resources,
        "artifacts": artifacts or [],
    }


def text_title(text: str | None) -> str | None:
    if not text:
        return None
    for line in text.splitlines():
        value = line.strip().lstrip("#").strip()
        if value:
            return value[:300]
    return None


def html_title(html: str) -> str | None:
    match = TITLE_RE.search(html)
    if not match:
        return None
    value = TAG_RE.sub(" ", match.group(1))
    return " ".join(value.split())[:300] or None


def resource_sample(started: float) -> dict[str, int]:
    # macOS reports ru_maxrss in bytes; normalize to KiB without recording content.
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {
        "elapsed_ms": round((time.perf_counter() - started) * 1000),
        "max_rss_kb": round(max_rss / 1024),
    }


async def run_with_timeout(operation: Any, *, timeout_seconds: float) -> Any:
    """Await a framework operation with a benchmark-level wall-clock bound."""
    return await asyncio.wait_for(operation, timeout=timeout_seconds)


def safe_error(exc: BaseException) -> str:
    value = f"{type(exc).__name__}: {exc}"
    return value.replace("\n", " ")[:500]


def load_case(name: str) -> dict[str, Any]:
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    if name not in cases:
        raise ValueError(f"unknown case {name!r}; expected one of {sorted(cases)}")
    return cases[name]


def robots_allowed(url: str) -> bool | None:
    """Return False only for an explicit robots denial; unavailable robots is recorded as unknown."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except OSError:
        return None
    return parser.can_fetch(USER_AGENT, url)


def bounded_same_origin_links(
    *,
    base_url: str,
    hrefs: list[str],
    already_requested: set[str],
    remaining: int,
) -> list[str]:
    """Return at most ``remaining`` new same-origin canonical links.

    The bound is applied before yielding requests to the crawler.  A framework
    close-after-N setting alone is insufficient because it can still leave a
    large request queue and an indeterminate shutdown time.
    """
    base_origin = urlparse(base_url).netloc
    selected: list[str] = []
    known = set(already_requested)
    for href in hrefs:
        absolute = urldefrag(urljoin(base_url, href))[0]
        if urlparse(absolute).netloc != base_origin or absolute in known:
            continue
        known.add(absolute)
        selected.append(absolute)
        if len(selected) >= max(0, remaining):
            break
    return selected


def extract_crawl4ai_markdown(result: Any) -> str:
    markdown = getattr(result, "markdown", None)
    for name in ("fit_markdown", "raw_markdown", "markdown_with_citations"):
        value = getattr(markdown, name, None)
        if isinstance(value, str) and value.strip():
            return value
    return str(markdown or "")


def crawlee_concurrency_settings() -> Any:
    """Create the public Crawlee 1.x one-request-at-a-time configuration."""
    from crawlee._types import ConcurrencySettings

    return ConcurrencySettings(min_concurrency=1, max_concurrency=1, desired_concurrency=1)


async def run_crawl4ai(case: dict[str, Any]) -> tuple[str | None, str | None, str, int]:
    from crawl4ai import AsyncWebCrawler, BFSDeepCrawlStrategy, BrowserConfig, CacheMode, CrawlerRunConfig

    url = case["url"]
    config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        channel="chrome",
        chrome_channel="chrome",
        text_mode=True,
        verbose=False,
    )
    run_config = CrawlerRunConfig(
        word_count_threshold=1,
        cache_mode=CacheMode.BYPASS,
        check_robots_txt=True,
        page_timeout=30_000,
        semaphore_count=1,
        verbose=False,
    )
    if case["name"] == "crawl":
        run_config.deep_crawl_strategy = BFSDeepCrawlStrategy(
            max_depth=1,
            max_pages=case["max_pages"],
            include_external=False,
        )
    base_directory = str(RUNTIME_DIR / "crawl4ai")
    async with AsyncWebCrawler(config=config, base_directory=base_directory) as crawler:
        response = await crawler.arun(url=url, config=run_config)
    results = response if isinstance(response, list) else [response]
    successful = [item for item in results if getattr(item, "success", False)]
    if not successful:
        message = getattr(results[0], "error_message", "Crawl4AI returned no successful result")
        raise RuntimeError(str(message))
    first = successful[0]
    metadata = getattr(first, "metadata", {}) or {}
    title = metadata.get("title") or text_title(extract_crawl4ai_markdown(first))
    final_url = getattr(first, "url", url) or url
    return extract_crawl4ai_markdown(first), title, final_url, len(successful)


async def run_crawlee(case: dict[str, Any]) -> tuple[str | None, str | None, str, int]:
    os.environ["CRAWLEE_STORAGE_DIR"] = str(RUNTIME_DIR / "crawlee-storage")
    url = case["url"]
    gathered: list[tuple[str, str | None, str]] = []

    if case["name"] == "javascript":
        from crawlee.crawlers import PlaywrightCrawler

        crawler = PlaywrightCrawler(
            headless=True,
            browser_type="chrome",
            max_requests_per_crawl=1,
            concurrency_settings=crawlee_concurrency_settings(),
            respect_robots_txt_file=True,
            configure_logging=False,
            request_handler_timeout=timedelta(seconds=30),
        )

        @crawler.router.default_handler
        async def capture_browser(context: Any) -> None:
            title_node = await context.page.query_selector("title")
            title = await title_node.inner_text() if title_node else None
            text = await context.page.locator("body").inner_text()
            gathered.append((context.request.loaded_url or context.request.url, title, text))

    else:
        from crawlee.crawlers import BeautifulSoupCrawler

        crawler = BeautifulSoupCrawler(
            max_requests_per_crawl=case["max_pages"] if case["name"] == "crawl" else 1,
            max_crawl_depth=1 if case["name"] == "crawl" else 0,
            concurrency_settings=crawlee_concurrency_settings(),
            respect_robots_txt_file=True,
            configure_logging=False,
            request_handler_timeout=timedelta(seconds=30),
        )

        @crawler.router.default_handler
        async def capture_http(context: Any) -> None:
            title_node = context.soup.find("title")
            title = title_node.get_text(" ", strip=True) if title_node else None
            text = context.soup.get_text(" ", strip=True)
            gathered.append((context.request.loaded_url or context.request.url, title, text))
            if case["name"] == "crawl":
                await context.enqueue_links()

    await run_with_timeout(crawler.run([url]), timeout_seconds=45)
    if not gathered:
        raise RuntimeError("Crawlee produced no page record")
    final_url, title, content = gathered[0]
    return content, title or text_title(content), final_url, len(gathered)


def run_scrapy_trafilatura(case: dict[str, Any]) -> tuple[str | None, str | None, str, int]:
    import scrapy
    import trafilatura
    from scrapy.crawler import CrawlerProcess

    url = case["url"]
    results: list[tuple[str, str | None, str]] = []

    class BenchmarkSpider(scrapy.Spider):
        name = "web_ingestion_benchmark"
        start_urls = [url]
        custom_settings = {
            "LOG_ENABLED": False,
            "ROBOTSTXT_OBEY": True,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
            "CONCURRENT_REQUESTS": 1,
            "DOWNLOAD_DELAY": 1.0,
            "CLOSESPIDER_PAGECOUNT": case["max_pages"] if case["name"] == "crawl" else 1,
            "CLOSESPIDER_TIMEOUT": 45,
            "DEPTH_LIMIT": 1 if case["name"] == "crawl" else 0,
            "USER_AGENT": USER_AGENT,
            "TELNETCONSOLE_ENABLED": False,
        }

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.requested_urls: set[str] = {url}

        def parse(self, response: Any) -> Any:
            text = trafilatura.extract(
                response.text,
                url=response.url,
                output_format="txt",
                include_comments=False,
                include_tables=False,
            ) or " ".join(response.css("body *::text").getall())
            title = response.css("title::text").get(default=None)
            results.append((response.url, title, text))
            if case["name"] == "crawl":
                remaining = max(0, case["max_pages"] - len(self.requested_urls))
                for next_url in bounded_same_origin_links(
                    base_url=response.url,
                    hrefs=response.css("a::attr(href)").getall(),
                    already_requested=self.requested_urls,
                    remaining=remaining,
                ):
                    self.requested_urls.add(next_url)
                    yield response.follow(next_url, callback=self.parse)

    process = CrawlerProcess(settings={"LOG_ENABLED": False})
    process.crawl(BenchmarkSpider)
    process.start(stop_after_crawl=True)
    if not results:
        raise RuntimeError("Scrapy yielded no page after robots and response handling")
    final_url, title, content = results[0]
    return content, title or text_title(content), final_url, len(results)


def run_jina_reader(case: dict[str, Any]) -> tuple[str | None, str | None, str, int, str | None]:
    if case["name"] == "crawl":
        return None, None, case["url"], 0, "recursive crawl is outside this reader baseline"
    target = f"https://r.jina.ai/{case['url']}"
    request = urllib.request.Request(target, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        content = response.read().decode("utf-8", errors="replace")
    return content, text_title(content), case["url"], 1, None


def run_firecrawl(case: dict[str, Any]) -> tuple[str | None, str | None, str, int]:
    """Run only through an explicitly configured loopback Firecrawl endpoint."""
    endpoint = os.environ.get("FIRECRAWL_ENDPOINT")
    if not endpoint:
        raise RuntimeError("FIRECRAWL_ENDPOINT must explicitly name the isolated loopback API")
    from admission import TargetPolicy, validate_target
    from firecrawl_client import FirecrawlClient

    target = validate_target(case["url"], policy=TargetPolicy())
    if not target.allowed:
        raise RuntimeError(f"Firecrawl target rejected by admission policy: {target.reason}")
    client = FirecrawlClient(endpoint)
    if case["name"] == "crawl":
        result = client.crawl(target.canonical_url, max_pages=case["max_pages"])
    else:
        result = client.scrape(target.canonical_url)
    return result.content, result.title, result.final_url, result.discovered_count


def execute(candidate: str, case: dict[str, Any]) -> tuple[str | None, str | None, str, int, str | None, str]:
    if candidate == "crawl4ai":
        content, title, final_url, count = asyncio.run(run_crawl4ai(case))
        return content, title, final_url, count, None, "success"
    if candidate == "crawlee":
        content, title, final_url, count = asyncio.run(run_crawlee(case))
        return content, title, final_url, count, None, "success"
    if candidate == "scrapy-trafilatura":
        content, title, final_url, count = run_scrapy_trafilatura(case)
        return content, title, final_url, count, None, "success"
    if candidate == "jina-reader":
        content, title, final_url, count, unsupported = run_jina_reader(case)
        return content, title, final_url, count, unsupported, "unsupported" if unsupported else "success"
    if candidate == "firecrawl":
        content, title, final_url, count = run_firecrawl(case)
        return content, title, final_url, count, None, "success"
    raise ValueError(f"unknown candidate {candidate!r}")


def write_record(path: Path, record: dict[str, Any]) -> None:
    errors = validate_record(record)
    if errors:
        raise ValueError(f"refusing invalid benchmark record: {errors}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, choices=["crawl4ai", "crawlee", "scrapy-trafilatura", "jina-reader", "firecrawl"])
    parser.add_argument("--case", required=True, choices=["static", "javascript", "crawl"])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    case = {"name": args.case, **load_case(args.case)}
    started_at = utc_now()
    timer = time.perf_counter()
    try:
        if args.case == "crawl":
            allowed = robots_allowed(case["url"])
            if allowed is False:
                record = normalized_record(
                    candidate=args.candidate,
                    case=args.case,
                    requested_url=case["url"],
                    final_url=case["url"],
                    content=None,
                    title=None,
                    discovered_count=0,
                    started_at=started_at,
                    ended_at=utc_now(),
                    resources=resource_sample(timer),
                    status="skipped",
                    error="robots.txt explicitly disallows this benchmark user agent",
                )
            else:
                content, title, final_url, count, error, status = execute(args.candidate, case)
                record = normalized_record(
                    candidate=args.candidate,
                    case=args.case,
                    requested_url=case["url"],
                    final_url=final_url,
                    content=content,
                    title=title,
                    discovered_count=count,
                    started_at=started_at,
                    ended_at=utc_now(),
                    resources=resource_sample(timer),
                    status=status,
                    error=error,
                )
        else:
            content, title, final_url, count, error, status = execute(args.candidate, case)
            record = normalized_record(
                candidate=args.candidate,
                case=args.case,
                requested_url=case["url"],
                final_url=final_url,
                content=content,
                title=title,
                discovered_count=count,
                started_at=started_at,
                ended_at=utc_now(),
                resources=resource_sample(timer),
                status=status,
                error=error,
            )
    except Exception as exc:  # Every framework failure is evidence, not a benchmark abort.
        record = normalized_record(
            candidate=args.candidate,
            case=args.case,
            requested_url=case["url"],
            final_url=case["url"],
            content=None,
            title=None,
            discovered_count=0,
            started_at=started_at,
            ended_at=utc_now(),
            resources=resource_sample(timer),
            status="error",
            error=safe_error(exc),
        )
    write_record(args.output, record)
    print(json.dumps({key: record[key] for key in ("candidate", "case", "status", "discovered_count", "error")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
