# Web-Ingestion M2–M5 Closeout、Housekeeping 与复盘（2026-07-14）

## 1. 闭环结论

本轮完成了从候选框架评测到受控 Web-Ingestion 路线的最小闭环。结论不是“部署 Firecrawl”，而是将其限定为一个可验证、可撤销、按需启用的服务路线：

- 用户入口唯一：`web_ingest.py`；
- `static` 走安全 HTTP transport + Trafilatura；
- `browser` 与 `crawl` 只经 CLI 间接启动一次性的 loopback Firecrawl runner；
- 每次请求必须携带 URL、用途、模式、预算、超时和 staging 根目录；
- 采集前执行公网目标、逐跳重定向、robots、MIME 预检；Firecrawl 返回的最终 URL 再次做公网准入；
- 采集结果仅落 body-redacted receipt；重复 digest 不得 promotion；
- promotion 与 RAG bridge 均需独立确认，bridge 默认 `sink: null`；
- 未引入 MCP、默认 Agent 工具、Hermes、Open WebUI 或既有 RAG 写入。

这是一项**受控能力准入**，不是常驻服务、生产容量、任意站点授权或自动知识库同步的批准。

## 2. 交付物与证据

| 层次 | 交付物 | 状态 |
| --- | --- | --- |
| 设计 SSOT | `docs/superpowers/specs/2026-07-14-web-ingestion-m2-m5-design.md` | 完成 |
| 实施计划 | `docs/superpowers/plans/2026-07-14-web-ingestion-m2-m5-implementation.md` | 全部 checkbox 完成 |
| 唯一入口 | `experiments/web-ingestion-benchmark/web_ingest.py` | 完成 |
| 策略控制器 | `experiments/web-ingestion-benchmark/web_ingestion.py` | 完成 |
| RAG bridge | `experiments/web-ingestion-benchmark/rag_bridge.py` | 完成，默认无 sink |
| 供应链 gate | `scripts/verify-firecrawl-provenance.py` | 完成 |
| 授权 workload | `ops/web-ingestion-authorized-workloads.json` | 三条公开、无凭据 URL |
| 端到端验证 | `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-validation.json` | 通过 |
| 跨版本矩阵 | `evidence/benchmarks/python-py312-tests.txt` 等 | 3.12/3.13/3.14 各 52/52 |
| Housekeeping receipt | `evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-housekeeping.json` | 通过 |

## 3. 验收事实

1. `static` 公开页面成功，第二次相同内容被标为 `duplicate`，且不能 promotion。
2. 显式 promotion 后，`prepare-rag` 只输出 `sink: null` 的 bridge manifest。
3. browser 路径成功；crawl 路径成功且 `discovered_count=10`，符合页数上限和单并发约束。
4. 每次 Firecrawl 运行前，官方 GHCR arm64 镜像 reference、架构与本地 image ID 的 provenance 检查通过。
5. 直接向隔离 runner 注入 `http://127.0.0.1/` 的内部请求非零退出；cleanup 后资源归零。
6. Python 3.12.13、3.13.14、3.14.6 的 locked matrix 各 52/52 通过。
7. Housekeeping 复核时，Compose 容器、卷、网络均为 0；`13002`、`16379`、`15672`、`25672`、`43691` 均无监听；项目无 `.venv` 与 bytecode cache。

## 4. Housekeeping

本次执行的是**最小、证据优先**的 housekeeping：

- 清除本轮验证生成的项目内 `__pycache__`；复核后为 0。
- 清除一个已退出测试遗留的 0-byte `/tmp/web-ingestion-final-matrix.*` 当前轮临时目录；该目录不含测试环境、证据或运行资源。
- 未删除 `results/` 下 29 个历史基准结果、M1 运行日志、镜像检查、资源样本或旧测试日志；它们属于可追溯证据，而非可安全推断的垃圾。
- `results/m1/current-run.pid` 指向已退出的历史 PID `74974`；该文件保留为运行 receipt，不被误作活跃任务或删除对象。
- 未安装、更新、迁移任何软件；未改 Docker daemon；未启动或停止任何外部常驻服务。

Housekeeping 的可复核 receipt 为：

```text
evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-housekeeping.json
```

## 5. 复盘：有效做法

### 5.1 先将“要不要引入”变成可证伪的准入问题

最初的问题不是缺一个爬虫，而是缺少一个可审计的 web-ingestion 能力边界。将候选比较、供应链、运行时隔离、数据面和后续接入拆开后，Firecrawl 的“强能力”不再自动等于“可接入”。准入由明确约束决定，而不是由框架热度决定。

### 5.2 把控制点放在服务之前与服务之后

仅依赖 Firecrawl 自己的 SSRF 或 crawl 限制不够。CLI 在服务启动前做 target/redirect/robots/MIME 准入；服务返回 final URL 后再次验证。这使服务即使退化或被错误配置，也不能单独决定外部目标是否进入 receipt。

### 5.3 以 receipt 替代正文持久化

将正文限制在内存中，将 digest、质量、路由、预算和策略决定写入 receipt，使质量判断、去重、promotion 和审计可以独立进行。这既降低数据留存面，也避免“先采集、后补治理”的不可逆路径。

### 5.4 把 RAG bridge 设计成边界，而非自动化捷径

`sink: null` 不是功能缺失，而是治理完成前的 fail-closed 默认。它允许后续独立评估知识库权限、保留、删除、追溯和目标系统 adapter，而不把 Firecrawl 的接入决定偷换成“自动进入 RAG”。

### 5.5 用实际工作负载证明运行边界

静态、JS、十页 crawl、重复、promotion、bridge 和私网失败恢复共同验证了端到端路径。单元测试不能代替真实 Firecrawl runtime；真实运行也不能代替跨版本测试。两者都必须保留。

## 6. 复盘：问题、原因与改进

| 问题/风险 | 根因 | 已采取措施 | 后续规则 |
| --- | --- | --- | --- |
| 早期直接否决 Firecrawl 过于武断 | 将“本机供应链阻断”误判为“框架不适合” | 改为多候选基准、GHCR recovery 与隔离运行验证 | 将环境阻断、产品能力和准入结论分开陈述 |
| Firecrawl 的能力面大于当前可治理面 | 服务 API 和 browser/crawl 能力天然容易被外推 | 固定唯一 CLI、disposable runner、loopback、allowlist | 不允许直连 API、常驻化或默认工具注册 |
| 仅有预检不能覆盖服务回传值 | 服务最终 URL 是另一个不可信输入边界 | 新增 final URL revalidation 测试与实现 | 所有外部组件回传的 target identity 都必须重验 |
| 页数预算可能被服务结果绕开 | 预算只在请求参数层声明 | 新增 route-specific page budget 与 `discovered_count` guard | 将预算同时绑定到请求、响应和 receipt |
| closeout 易误删“看似临时”的证据 | PID、日志、旧矩阵结果的语义不等于垃圾 | 仅删除一个已确认 0-byte 的当前轮 `/tmp` 目录，并记录 retained evidence hash | 只删当前轮可归因 scratch；历史证据默认保留 |
| shell 环境可出现 PATH 异常 | 长运行环境或 wrapper 暂时污染命令解析 | 对 closeout 使用明确二进制路径并重新验证 | 验收脚本应尽量固定关键命令路径，避免环境依赖掩盖结果 |

## 7. 后续触发器与停止规则

仅在以下变化发生时重开工作：

1. 新站点、新用途或新数据等级：先增加单独 allowlist 与采集契约；不复用当前三条公开 workload 的授权。
2. 镜像、tag、digest、Compose、端口、服务拓扑变更：停止该路线，重跑 M1 与 M2–M5 验收。
3. 需要真实 RAG delivery：先完成独立 sink adapter 与权限、保留、删除、审计、回滚评审；不得绕过 `sink: null`。
4. 需要递归 crawl 扩容：先验证站点 robots/crawl-delay、预算、恢复与成本；不得把当前 10 页单并发结论外推。
5. 需要 MCP、Hermes、Open WebUI 或默认 Agent 工具：作为新的控制面项目立项，不可由当前准入自然推导。

停止规则同样明确：没有上述触发器时，不运行常驻服务、不做无目的重测、不删除历史证据，也不继续扩展框架表面积。

## 8. 当前权威状态

- 准入决定：`docs/benchmarks/2026-07-14-web-ingestion-firecrawl-m1-closeout.md`
- 操作手册：`docs/benchmarks/2026-07-14-web-ingestion-m2-m5-runbook.md`
- 端到端证据：`evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-validation.json`
- Housekeeping receipt：`evidence/benchmarks/2026-07-14-web-ingestion-m2-m5-housekeeping.json`

上述四份文件共同构成当前 Web-Ingestion 能力的 closeout SSOT。任何后续变更必须以它们为基线，并产生新的、可独立验证的证据。
