# Web-Ingestion 准入闭环：M1 复验与 M2–M5 落地（2026-07-14）

## 结论

Firecrawl 由 `hold` 调整为 **`admit-as-service`**，但“service”仅指**按需、显式调用、一次性、loopback-only 的隔离运行面**；M2–M5 现已将这一判断固化为唯一受策略约束 CLI、启动前 provenance 校验、授权公开工作负载、显式 promotion 与默认无 sink 的 RAG bridge。它仍不授权常驻 daemon，更不授权 MCP、默认 Agent 工具、Hermes Dashboard、Open WebUI Pipe 或直接写入 RAG。

其余候选结论不变：Crawl4AI 为 `admit-as-library`；Crawlee 为 `admit-as-library-with-condition`（真实递归采集前必须实施每域 crawl-delay）；Scrapy+Trafilatura 为 `admit-as-static-library`；Jina Reader 保持 `hold`。

## 本次解决的阻断

此前不是 Firecrawl 功能失败，而是本机到 GHCR blob CDN 的连续大对象传输被截断。恢复路径只使用官方 GHCR：先将 tag 解析并绑定到审查过的 arm64 manifest digest，再对官方短期签名 URL 发起分段读取，每个 blob 按 manifest SHA-256 校验后才构造本地 `docker load` archive。未修改 Docker daemon，未添加 mirror，未使用 Docker Hub 替代镜像。

运行集固定为：

- `ghcr.io/firecrawl/firecrawl:2.10.19`，官方 arm64 manifest `sha256:e6860ab406e738b632cc41b02a54085575909a1da1fbe4b3577b8339257fee70`；
- `ghcr.io/firecrawl/playwright-service:latest`，官方 arm64 manifest `sha256:3f21958ad289a7c7ed7d1f2598847a37582d723559e4efb7069d1754ac009852`；
- `ghcr.io/firecrawl/nuq-postgres:latest`，官方 arm64 manifest `sha256:ee30cebf9afb6648f5406ac3e7505e21be30fd2f11c2067bd98a53e7542ecbac`。

## 本次验收

| 门槛 | 结果 |
| --- | --- |
| 静态页 | 成功，781 ms |
| JS 页 | 成功，2,609 ms |
| 十页 crawl | 成功，37,060 ms、10 页；请求 `maxConcurrency=1`、`maxDiscoveryDepth=1`、禁用 sitemap |
| 服务侧 loopback 目标 | `127.0.0.1` scrape 返回 HTTP 400，拒绝 |
| 监听 | 仅 `127.0.0.1:13002`（API）、`127.0.0.1:16379`（Redis）、`127.0.0.1:15672/25672`（RabbitMQ）、本地 EPMD |
| 资源样本 | API `1.276 GiB / 4 GiB`；Postgres `132.9 MiB / 1 GiB`；Playwright `183.2 MiB / 2 GiB` |
| 清理 | 容器、卷、网络、基准端口、项目虚拟环境均为 0 |

结果均为 body-redacted 证据；只保存元数据、URL、摘要哈希、资源和脱敏错误。

## 操作契约

1. 用户入口仅为 `web_ingest.py`；`scripts/firecrawl-isolated-benchmark.sh` 仅由 CLI 内部调用，用于 browser/crawl 的一次性运行面。
2. 每次采集都必须显式提供 URL、用途、模式、页数预算、超时和 staging 根目录；在服务启动前通过公网目标、每跳重定向、robots 与 MIME 预检。Firecrawl 返回的最终 source URL 也会再次做公网准入。
3. receipt 仅持久化策略、质量、digest 与审计元数据；不持久化正文、HTML、Markdown 或 raw response。重复 digest 可 stage，但不得 promotion。
4. promotion 必须独立 `--confirm`；`prepare-rag --confirm` 只生成 `sink: null` 的脱敏 bridge manifest。它不构成真实 RAG 交付。
5. 不复用 `nomad_redis`、既有 Postgres、既有 Compose 项目或监听；支持服务均临时创建，脚本退出即清理。
6. 任何镜像 digest、镜像 tag、服务配置、暴露面或接入面变化，均须重新进行功能、安全、资源、监听和清理验收；不得把本次结论外推为生产容量、站点授权或默认 Agent 能力。

## M2–M5 验收

2026-07-14 的受控验证只读取三项已授权、无凭据的公开工作负载：`https://example.com/`、`https://quotes.toscrape.com/js/`、`https://quotes.toscrape.com/`。static 成功并产生重复项；首次 receipt 显式 promotion 后生成 sinkless bridge manifest；browser 成功；crawl 成功且 `discovered_count=10`；直接向隔离 runner 传入 `http://127.0.0.1/` 的内部请求非零退出，随后资源为零。镜像 provenance 在每次 Firecrawl 启动前通过。Python 3.12.13、3.13.14、3.14.6 的全量锁定测试矩阵各为 52/52 通过。

## 证据

- 本次可发布版本不包含原始逐运行目录 `results/m1/`；它属于本机留存的历史 receipt。可移植的运行摘要见下项证据。
- M1 runtime 摘要：`evidence/benchmarks/2026-07-14-web-ingestion-firecrawl-m1-runtime.json`。
- 全候选比较 v2：`evidence/benchmarks/2026-07-14-web-ingestion-framework-benchmark-v2.json`。
- M2–M5 脱敏验证：`evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-validation.json`。
- Housekeeping 与复盘：`docs/benchmarks/2026-07-14-web-ingestion-m2-m5-closeout-retrospective.md`，对应 receipt 为 `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-housekeeping.json`。
- 运行手册：`docs/benchmarks/2026-07-14-web-ingestion-m2-m5-runbook.md`。
- Python 3.12.13、3.13.14、3.14.6：各 52/52 通过，日志位于 `evidence/benchmarks/python-py312-tests.txt`、`python-py313-tests.txt`、`python-py314-tests.txt`。
