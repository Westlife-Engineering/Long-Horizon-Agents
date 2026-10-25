# Long-Horizon Agents 知识库

这里积累关于长程 Agent 的定义、机制、证据和研究问题。当前处于**建立地图与文献驱动的 idea 探索阶段，未选定具体研究问题**。

## 当前证据边界

- 已纳入 **1 篇学术来源**：S001，Dong 等的综述；整体为地图式阅读，Foundation（§2，PDF pp.7–15）已补充问题驱动精读，尚非全篇技术细节的精读。
- **独立方法/实验论文已读数为 0**。综述中的引用不是本库已验证的证据；已制定从综述引用出发的自主选读协议，具体论文队列尚未生成。
- 方法论原始资料为 [[raw/articles/llm-wiki|LLM Wiki]]，不计入学术来源数。具体工作规则见 [[AGENTS|Schema]]。

## 从哪里开始

[[wiki/overview|领域总览]]：用系统耦合、任务层级与证据边界理解整张地图，再选择问题深入。

## Foundation：从图解笔记开始

**[[wiki/foundations/Formalization|定义、运行循环与理解辨析]]** 是默认阅读入口。流程图放在运行机制旁，反馈与成功的辨析接在循环之后，纠错恢复与时间代理接在任务分层之后；详细推导和依据按需展开。

已有具体困惑时，可以用 [[wiki/foundations/Formalization#从这套基础定义还能多理解什么|问题导航]] 直接进入。其他主题在后续阅读和更新时按内容需要逐步改善展示。

## 六个初始视角

六个视角沿用 S001 的组织方式（[[raw/papers/Towards Long-Horizon Agents.pdf#page=6|§1 · p.6]]），是导航起点，不是永久分类。

| 视角 | 页面 | 这里回答什么 |
| --- | --- | --- |
| Foundation | [[wiki/foundations/Formalization\|定义、运行循环与理解辨析]] | 从状态—观察—上下文理解 Agent 循环，串起任务依赖、H1–H3、记忆与自我演化，并区分定义、推断和评测代理。 |
| Evolution | [[wiki/foundations/Evolution\|从 Prompt 到 Runtime]] | 控制对象怎样从单次提示扩展到完整执行轨迹？ |
| Harness | [[wiki/harness/Overview\|外部运行机制]] | 循环、状态、工具、编排、拦截和验证分别负责什么？ |
| Optimization | [[wiki/optimization/Overview\|能力内化与训练]] | 架构、数据、训练和经验更新怎样组织成能力发展路线？ |
| Application | [[wiki/applications/Overview\|应用与评测]] | 不同环境接口提供什么反馈，评测如何归因？ |
| Frontier | [[wiki/frontier/Overview\|前沿与待检验问题]] | 作者提出哪些开放方向？本库还有哪些证据与概念缺口？ |

Harness 与 Optimization 的子方向都保留在各自 Overview 的页内导航中；当前没有空白细分页面。

## 学术来源目录

| 来源 | 唯一来源页 | 状态与用途 |
| --- | --- | --- |
| S001 | [[wiki/papers/Towards Long-Horizon Agents\|Towards Long-Horizon Agents: A Survey]] | 地图来源与阅读记录；已补充 Foundation 问题驱动精读及证据落点 |

## 维护入口

- [[wiki/log|操作日志]]：按时间记录来源摄入、查询沉淀、规则调整与健康检查。
- [[AGENTS|长期规则]]：三层边界、证据层级、论文唯一性和结构演化条件。
- [[workflows/ingest|Ingest]] · [[workflows/query|Query]] · [[workflows/lint|Lint]] · [[workflows/presentation|阅读表达]]：可逐步执行、随实践迭代的维护清单。
- [[workflows/autoresearch|Auto Research]]：按方向选文、每篇由同模型 subagent 摄入、共享写入、预算与停止条件；包含 Harness / Optimization 的启动和分工方案。
- [[workflows/brainstorm|Brainstorm]]：共同证据上的独立分析、互评、查新反证与候选问题状态。

**本轮状态（2026-10-25）：**按用户决定，先完成规则与启动方案，下一轮开始读论文。Harness / Optimization 可以按现有一级子方向分批探索，每方向约 5 篇；尚未启动论文摄入或后台自动运行。

新论文来了先整合已有页面；新问题形成独立内容时再拆页。自主研究在选定范围内引导后续阅读，不代替用户确定最终研究方向。[[wiki/frontier/Overview#本库的待检验问题|现有问题]] 仍是探索记录，是否追踪取决于后续选文与证据。
