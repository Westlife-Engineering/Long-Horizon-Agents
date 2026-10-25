---
type: paper
source_id: S040
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/TOUCAN.pdf]]"
---

# TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World MCP Environments

## 来源与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S040 |
| 作者 | Zhangchen Xu、Adriana Meza Soria、Shawn Tan、Anurag Roy、Ashish Sunil Agrawal、Radha Poovendran、Rameswar Panda |
| 版本 | arXiv:2510.01179v1，2025-10-01 |
| 原始入口 | [TOUCAN](https://arxiv.org/abs/2510.01179)；访问日期 2026-10-25 |
| 原件 | [[raw/papers/TOUCAN.pdf\|本地 PDF，共 35 页]] |
| SHA-256 | `78B90827799A8DB9B71AF8A47781F65B822B14AAAC9B9EF7ABB5F16DD5F4ED55` |
| 实际阅读 | 2026-10-25；正文 pp.1–9；附录 A pp.15–17、C p.20、D.4–D.5 pp.31–35；看 p.3 Fig.1–2、p.8 Table3/Fig.7–8、p.20 Fig.13/Table5–6。未逐项核读服务器列表、全部生成提示及引用文献。 |
| S001 定位 | 引文 737，§5.2.3，PDF p.43；书目 p.135 |

以下为原论文直接证据与明确标注的本库分析；未复现实验。页码均为本地 PDF 自首页起算。

## 核心理解：真实工具返回与合成任务、合成用户共同组成轨迹

TOUCAN 以 MCP server 的工具描述生成任务，让教师 Agent 真正调用远端工具，再用规则和模型筛选轨迹；目标是提供多工具、多步和多轮的 SFT 数据。任务及用户追问是合成的，工具返回来自实际执行，最终“任务完成”通常由 LLM 根据对话判分。这三种来源不能混写成真实用户任务、完整环境状态和客观成功验证均已具备。[[raw/papers/TOUCAN.pdf#page=3|§3.1、Fig.2 · pp.3–5]]

| 流程对象 | 生成/过滤办法 | 留下的边界 |
| --- | --- | --- |
| 工具环境 | 从约 2,800 server 中保留可远端 HTTP 调用、无需第三方凭据且试运行可用者，最终 495 个 | 特殊配置、账户/API key 场景被排除；真实 MCP 不等于完整生产使用分布 |
| 任务 | 五种模型根据工具 spec 生成单 server、多 server、精选 server 场景；实验最大目标工具数 N=3 | 任务设计从指定工具倒推，工具多不等于长依赖链 |
| 轨迹 | GPT-OSS-120B、Kimi-K2、Qwen3-32B 配 Qwen-agent/OpenAI-agent，记录调用、返回和回答 | 真实返回可检查调用，但不会自动证明最终写入副作用或长期状态正确 |
| 质量 | 规则过滤连接/工具错误、无调用及本地路径；检验目标工具覆盖和顺序，GPT-OSS 判完整与简洁 | target tool 由生成器预设，存在替代方案；完整性是判断而非统一执行 oracle |
| 扩展 | 无关工具、persona/约束变化、多轮拆题和追问；无关任务例外保留零工具调用 | 多轮来自自模拟，不是收集真实用户交互；过滤失败可能弱化恢复案例 |

直接依据：[[raw/papers/TOUCAN.pdf#page=4|§3.1 Stage1–3 · p.4]]、[[raw/papers/TOUCAN.pdf#page=5|Stage4–5、§3.2 · p.5]]；副作用验证与恢复偏差为**本库推断**。附录 A 的 schema 保存 messages、目标工具、质量标签与元数据，但本次原文未见统一的外部最终状态审计；“可验证性”在 D.4 中实际是模型评估答案多容易核查，不等于已执行该核查。[[raw/papers/TOUCAN.pdf#page=15|Appendix A · pp.15–17]]、[[raw/papers/TOUCAN.pdf#page=32|Appendix D.4 · p.32]]

## 1.5M 数据集与训练用 119.3K 不可混用

发布规模为 1,527,259 条轨迹，其中多轮对话 567,262；论文 SFT 只从高质量部分抽取并重平衡 **119.3K**：原始 28.3K、irrelevance 40K、diversify 15.8K、multi-turn 35.2K。筛选要求任务质量/真实性=5，回答完整/简洁≥4，目标工具覆盖=1。强质量选择和大量拒绝工具例对实际训练分布都有影响。[[raw/papers/TOUCAN.pdf#page=2|Table1 · p.2]]、[[raw/papers/TOUCAN.pdf#page=7|§4.1 · p.7]]

模型为 Qwen2.5-Instruct 7B/14B/32B，SFT 2 epochs、有效 batch64、最大序列 32768、8 或 64 张 H100，Hermes 调用模板。τ/τ²-Bench 用 GPT-4o 模拟用户，MCP-Universe 按基准搭建本地执行环境；并非同一类“真实世界”测试。[[raw/papers/TOUCAN.pdf#page=7|§4.1 · pp.7–8]]、[[raw/papers/TOUCAN.pdf#page=20|Appendix C.2、Table5 · p.20]]

## 实验证明了哪些收益，哪些没有

BFCL V3 上 32B overall 从 61.73% 到 70.45%，多轮从 26.38% 到 46.50%，但基准同时含 AST 调用匹配与多轮指标，不能把其总分直接称完整任务成功率。7B non-live AST 和 relevance 反而下降，14B relevance 也下降。τ²-Bench telecom 中 7B 从 16.70% 降到 10.50%，32B 从 21.11% 到 20.20%；因此数据有效不代表各任务全面收益。[[raw/papers/TOUCAN.pdf#page=7|Table2 · p.7]]、[[raw/papers/TOUCAN.pdf#page=8|Table3 · p.8]]

MCP-Universe 图中特意区分完整 task success 和 partial evaluation score，不能挑浅色高柱当成功率。作者说明其中大多数需特殊配置的 server 不在合成集合中，这提供一定跨工具环境证据，但不是严格证明所有 server、任务无重叠。[[raw/papers/TOUCAN.pdf#page=8|§4.2、Fig.7–8 · pp.8–9]]

逐步加入扩展时，14B 的单轮数据先让 τ-Bench Airline/Retail 低于原模型，最后加入 multi-turn 才明显提高；BFCL 中 diversify 从 64.74% 变为 64.56%。所以不能照抄作者“所有组件提升”的笼统说法，也不能把这种逐步增加数据量的消融当作等预算的单因素证明。[[raw/papers/TOUCAN.pdf#page=9|§4.3、Fig.9 · p.9]]、[[raw/papers/TOUCAN.pdf#page=20|Appendix C.3、Table6 · p.20]]

## 判断器可靠性与下一步证据

任务 judge 的人工对照只有随机 50 个样本，Kimi-K2 Pearson r=0.264，最高 GPT-4.1=0.385；作者因成本选 Kimi-K2。此结果支持记录评判器的有限一致性，不能把“高质量”标签升级成可靠真值。论文没有借此证明所有最终轨迹都被人核验。[[raw/papers/TOUCAN.pdf#page=20|Appendix C.1、Fig.13 · p.20]]

本库的待核查问题是：在固定轨迹与预算下，目标工具覆盖、judge 完整性和外部状态检查何时分歧；现有结果只支持进一步审计动机，未完成查新，不宣布研究缺口。与 ToolACE/APIGen 的比较仍为作者转述，本次未独立核读它们。

## 主题联系与验收状态

已整合至 [[wiki/optimization/Overview#数据与环境合成|数据与环境合成]]；监督训练接口亦见 [[wiki/optimization/Overview#微调|微调]]。主题、索引、互链与摄入日志已同步；主 Agent 已完成内容与结构验收，Raw 哈希匹配。Obsidian 应用未测，未复现实验。
