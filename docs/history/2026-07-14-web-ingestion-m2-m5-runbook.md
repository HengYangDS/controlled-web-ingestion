# Web-Ingestion M2–M5 运行手册（2026-07-14）

## 决策与边界

Firecrawl 已准入，但仅作为按需、临时、loopback-only 的服务路线。唯一用户入口为：

```bash
web_ingest.py
```

它不是常驻服务，也没有 MCP、默认 Agent 工具、Hermes、Open WebUI 或既有 RAG 的注册/写入权。静态请求使用安全 HTTP transport 与 Trafilatura；browser 与 crawl 仅可由 CLI 间接启动 Firecrawl 的 disposable runner。Crawl4AI、Crawlee、Scrapy+Trafilatura 的 M1 准入结论不随本手册改变。

## 受控入口

在 `.` 执行：

```bash
uv run --locked python web_ingest.py ingest \
  --url https://example.com/ \
  --purpose '明确、可审计的采集用途' \
  --mode static \
  --max-pages 1 \
  --timeout-seconds 45 \
  --stage-root /absolute/path/to/stage
```

必填字段缺失、模式/预算/超时越界、嵌入凭据、私网目标、重定向到私网、robots 禁止或 MIME 不在允许集合内时，入口 fail closed。browser/crawl 在 Firecrawl 启动前先进行同一 preflight；服务返回的最终 source URL 也要重新做公网准入。

模式与上限：

| mode | 路线 | 最大页数 | 运行面 |
| --- | --- | ---: | --- |
| `static` | 安全 transport + Trafilatura | 1 | 进程内 |
| `browser` | Firecrawl scrape | 1 | 临时 loopback service |
| `crawl` | Firecrawl crawl，单并发 | 10 | 临时 loopback service |

路由 SSOT：`ops/web-ingestion-routing.json`。

## Staging、promotion 与 RAG bridge

成功采集只写入 staging receipt。receipt 包含用途、路由、请求/最终 URL、redirect chain、策略/robots 决定、digest、质量和预算；不含正文、HTML、Markdown 或 raw response。相同 content digest 的第二条 receipt 标记为 `duplicate`，不得 promotion。

```bash
uv run --locked python web_ingest.py promote \
  --stage-root /absolute/path/to/stage \
  --receipt /absolute/path/to/stage/staging/RECEIPT.json \
  --confirm

uv run --locked python web_ingest.py prepare-rag \
  --bridge-root /absolute/path/to/bridge \
  --receipt /absolute/path/to/stage/promoted/RECEIPT.json \
  --confirm
```

第一条命令只把满足策略的 receipt 移入本地 promotion ledger。第二条命令只写 `sink: null` 的 bridge manifest；没有 CLI 真实 delivery 命令，也不配置网络/本地 RAG sink。未来若需 delivery，必须单独审查 adapter、授权目的、内存载荷 digest 校验与目标 RAG 边界。

## Firecrawl 供应链、运行与回滚

每次 browser/crawl 启动前，runner 会执行：

```bash
python3 scripts/verify-firecrawl-provenance.py
```

它将 `ops/firecrawl-provenance.json` 中审查过的官方 GHCR reference、`linux/arm64` 和本地 image ID 逐项比对；不一致即停止。runner 只使用 `web-ingestion-firecrawl-bench` Compose 项目与 benchmark 专属 loopback 端口，不复用 `nomad_redis`、既有 Postgres、容器、卷、网络或 listener。退出、错误和信号都会触发 teardown。

镜像、tag、digest、Compose 拓扑、端口暴露或接入面有任何变更时，停止使用该路线；恢复至上一份审查清单或清理临时运行面后，重新运行 M1 与本手册的 M2–M5 验收。不得以 Docker daemon 修改、registry mirror、Docker Hub 替代镜像或常驻化绕过这一流程。

## 复验

受控验收只允许如下 manifest 中的三条公开、无凭据 workload：

```bash
scripts/web-ingestion-m2-m5-validate.sh
```

allowlist：`ops/web-ingestion-authorized-workloads.json`。

该脚本验证：provenance、static、重复、promotion、sinkless bridge、browser、十页 crawl、私网 runner 子请求失败恢复，以及容器/卷/网络/端口/项目 `.venv` 为零。结果只写脱敏摘要：

```text
evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-validation.json
```

完整 Python 兼容性复验：

```bash
WORK=$(mktemp -d -t web-ingestion-matrix.XXXXXX)
for version in 3.12 3.13 3.14; do
  UV_NO_MANAGED_PYTHON=1 \
  UV_PROJECT_ENVIRONMENT="$WORK/venv-$version" \
  uv run --locked --python "/opt/homebrew/opt/python@$version/bin/python$version" \
    python -m unittest discover -s tests -v
done
rm -rf "$WORK"
```

本次实测为 Python 3.12.13、3.13.14、3.14.6，各 52/52 通过。

## 当前限制

- 不是生产容量、持续抓取、任意网站授权或隐私数据采集结论。
- crawl 仅限 10 页、单并发；新的递归路线仍需独立验证 crawl-delay 与站点策略。
- Firecrawl 不可信任为 egress policy 的唯一执行点；本地 preflight 与结果 URL revalidation 是保留约束。
- RAG bridge 是接口与审计边界，不是默认同步机制。
