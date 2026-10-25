---
type: paper
primary_direction: harness/tools
related_directions:
  - harness/verification
source_id: S016
created: 2026-10-25
updated: 2026-10-25
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/MCPMark.pdf]]"
---

# MCPMark：接口可用以后，任务是否真正完成

MCPMark 是评测，不是新的工具调用训练方法。它让模型在有明确初始状态的环境中完成涉及增删改查的多步任务，再用程序检查环境结果。因此，**工具成功返回、模型说完成、验收通过**是三个不同事件；MCP 的标准接口本身不保证后两者。[[raw/papers/harness/tools/MCPMark.pdf#page=1|Fig.1 · p.1]] [[raw/papers/harness/tools/MCPMark.pdf#page=5|§2.3 · p.5]]

## 来源与读取范围

| 项目 | 记录 |
| --- | --- |
| ID / 标题 | S016 / MCPMark: A Benchmark for Stress-Testing Realistic and Comprehensive MCP Use |
| 作者 | Zijian Wu, Xiangyan Liu, Xinyuan Zhang, Lingjun Chen, Fanqing Meng, Lingxiao Du, Yiran Zhao, Fanshi Zhang, Yaoqi Ye, Jiawei Wang, Zirui Wang, Jinjie Ni, Yufan Yang, Arvin Xu, Michael Qizhe Shieh |
| 锁定版本 | arXiv:2509.24002v1，2025-09-28，Technical Report，42 页 |
| 原始 URL / 访问 | [版本页](https://arxiv.org/abs/2509.24002v1)；[PDF](https://arxiv.org/pdf/2509.24002v1)；2026-10-25 |
| 原件 / SHA-256 | [[raw/papers/harness/tools/MCPMark.pdf\|MCPMark.pdf]]；`69E57B01A7F39DAFF489DEE5807C5F5AB2F16440C66DDFCDA4AA11DE7B92AC13` |
| 归档 | 带版本 URL 下载原字节归档；本页 PDF 页码与页脚页码一致 |
| 实际阅读 | 2026-10-25；正文 §§1–6（pp.1–10）；附录 A–B（pp.15–17）；C 定位任务矩阵；D 选读 Filesystem/PostgreSQL 表（pp.19、23）；E 核读 GitHub 与 PostgreSQL 案例原图（pp.27–29、36–38）；F 成本/调用口径 p.39；G 定位 p.40；H 选读 p.42。其他案例、全部逐任务矩阵、全部服务表与代码仓库未逐项核读 |
| 图表检查 | 已看 Fig.1、Tables 2–3、Figs.4–5、Figs.10–12、Figs.19–21 原页；未复算统计或运行验证脚本 |
| S001 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=27\|§4.3.1 · p.27 · 引文700]]；书目 p.132；不与 MCP-Universe 混同 |

## 一个评测样本包含状态和验收合同

127 个任务来自 38 个初始状态，覆盖 Filesystem 30、Notion 28、Playwright 25、GitHub 23、PostgreSQL 21 个任务。任务由专家和生成/执行 agent 共同探索、加难、编写 verifier，再做人工交叉检查；作者还修改环境结果来检验 checker 能否识别成败。它比只看最终回答更接近有副作用的工作流，但“现实性”仍受这五类人工构造任务的覆盖限制。[[raw/papers/harness/tools/MCPMark.pdf#page=4|§2.1–2.2 · Fig.3 · pp.4–5]]

```mermaid
flowchart LR
  I[初始环境快照与任务要求] -->|初始化| A[模型与 MCP 工具循环]
  A -->|无进一步工具调用的最终回答| F[最终环境状态]
  F -->|逐项检查任务约束| V[程序验收结果]
  V -->|恢复相同起点| R[重置环境]
  R -->|另一独立运行| A
```

本库根据 §2.3 绘制。验收对象是状态是否满足要求，不是模型的完成宣称；重置使四次运行可比较，不表示真实任务的破坏性副作用总能撤销。MCPMark-Agent 是 LiteLLM 与 MCP Python SDK 上的基础工具循环，支持一般 function-calling 路径及部分模型原生路径。[[raw/papers/harness/tools/MCPMark.pdf#page=5|§2.3 · p.5]] [[raw/papers/harness/tools/MCPMark.pdf#page=6|§3.1 · p.6]]

例如 GitHub 案例不只检查“创建了 PR”，还检查 ESLint 配置、工作流文件、CI 曾失败再成功以及错误是否修复。任务依赖横跨多个外部状态，单次调用合法不能替代这些联合约束。[[raw/papers/harness/tools/MCPMark.pdf#page=27|附录 E · Figs.10–12 · pp.27–29]]

## 三个成功指标回答不同问题

| 指标 | 原文含义 | 不应误读为 |
| --- | --- | --- |
| pass@1 | 单次运行成功率，主表通常报告四次独立运行的均值及标准差 | 四次全成功的可靠率 |
| pass@4 | 四次中至少一次成功的任务覆盖 | 同一有副作用任务可无成本重试四次 |
| pass^4 | 四次都成功才算该任务成功 | 从平均 pass@1 直接取四次方的解析估计 |

定义来自 [[raw/papers/harness/tools/MCPMark.pdf#page=6|§3.1–3.2 · p.6]]。最后一列是本库的解释边界；本文是实际重复运行统计，任务难度并不相同。

每次运行限 100 turns 和 3600 秒，大部分使用各模型默认推理设置。锁定报告中的 GPT-5-medium 为 52.56% pass@1、68.50% pass@4、33.86% pass^4，展示“偶尔能做”和“重复稳定完成”的距离；这是该版本、框架与任务下的历史结果，不能当作当前模型排行榜或所有 MCP 系统的上限。Table 2 中 Claude Opus 4.1 的 pass@4 / pass^4 未给值，不能假设所有模型都具有完整四次结果。[[raw/papers/harness/tools/MCPMark.pdf#page=6|§3.1–3.2 · pp.6–7]]

## 低成功率说明什么，尚不能说明什么

**原文结果：**显式失败包括上下文溢出、轮数耗尽、放弃、过早停止和调用格式错误；隐式失败是运行正常结束但不满足验收要求。隐式失败在所示模型中占很大比例。因此“API 没报错”不能视为成功。[[raw/papers/harness/tools/MCPMark.pdf#page=8|§4.2 · Fig.5 · pp.8–9]]

**作者解释，尚非因果核验：**远程服务表现较差可能来自训练覆盖不足，更多推理可能帮助泛化；成功轨迹较短可能体现更好的决策。论文未拿到并控制各模型训练数据，也未随机干预工具调用次数，故不能把这些相关性升级成“数据不足已被证实是原因”或“减少调用必然提高成功率”。Table 3 中更高 reasoning effort 也不是单调改善。[[raw/papers/harness/tools/MCPMark.pdf#page=6|§3.2 · pp.6–8]]

**本库推断：**统一基础 harness 有助于比较，但仍测量模型、接口转换、工具服务器和环境的组合。附录 B 包含 `@playwright/mcp@latest` 等调用方式，而未在该页给出全部服务器固定版本；后续复现应锁版本、初始状态与 verifier。程序验收的正确性与覆盖仍依赖任务规范和测试，本文没有形式化证明其完全性。[[raw/papers/harness/tools/MCPMark.pdf#page=17|附录 B · p.17]] [[raw/papers/harness/tools/MCPMark.pdf#page=15|附录 A · pp.15–16]]

**原文待核查细节：**p.38 的 PostgreSQL 失败案例标题/图注标 grok-4，截图内部却标 gpt-oss-120b；下方勾选表示表结构和索引已有、所需数据缺失，图注又概括 rows/indexes missing。本页仅将其作为“部分状态满足不等于全部验收通过”的示例，不把该轨迹归因给某个模型。[[raw/papers/harness/tools/MCPMark.pdf#page=38|附录 E · Fig.21 · p.38]]

## 对工具方向的更新

与 [[wiki/papers/harness/tools/AnyTool|AnyTool]] 的差异首先是测量对象：AnyTool 的主要判据是 GPT-4 对解答的判断，MCPMark 在初始化和重置框架中检查任务状态。两者不是同任务竞品，也不能跨表比较分数。与 [[wiki/papers/harness/tools/Voyager|Voyager]] 的联系是运行时 critic 和任务验收的区分：技能是否该入库、当前任务是否成功，都需要保留“谁检查、检查什么”的说明。

**待检验问题：**在固定模型、服务器版本、初始状态和调用预算后，工具发现、代码组合、技能检索或运行时验证分别能减少哪类未满足约束？这是适合用本评测提出的归因问题；尚未做相关工作查新或实验，不记作已确认研究缺口。作者明确指出扩展难度、任务构造成本、模糊用户意图及更多服务器都是未来方向，属于作者展望。[[raw/papers/harness/tools/MCPMark.pdf#page=10|§6 · p.10]]

## 整合与验收状态

已整合至 [[wiki/harness/tools|工具、MCP 与技能]] 与 [[wiki/harness/verification|验证]]，内容与结构验收通过；[[wiki/applications/Overview|应用评测]] 仅为相关入口，本批未写入该页。未运行 benchmark、未独立审查 verifier 源码；Obsidian 渲染与跳转尚未实测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/tools|harness/tools]] · [[wiki/harness/verification|harness/verification]]。
