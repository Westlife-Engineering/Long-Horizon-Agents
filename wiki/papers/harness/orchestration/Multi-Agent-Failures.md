---
type: paper
primary_direction: harness/orchestration
related_directions:
  - harness/verification
source_id: S021
created: 2026-10-25
updated: 2026-10-25
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf]]"
---

# Why Do Multi-Agent LLM Systems Fail?

> [!info] 状态
> 原文核读、主题整合与主 Agent 内容/结构验收已完成；未复现实验，Obsidian 应用未测。

## 来源身份与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S021 |
| 作者 | Mert Cemri、Melissa Z. Pan、Shuyi Yang、Lakshya A Agrawal、Bhavya Chopra、Rishabh Tiwari、Kurt Keutzer、Aditya Parameswaran、Dan Klein、Kannan Ramchandran、Matei Zaharia、Joseph E. Gonzalez、Ion Stoica |
| 锁定版本 | NeurIPS 2025 Datasets and Benchmarks 正式会议 PDF，54页；DOI 10.52202/085713-4082 |
| 原始发布页 | [Multi-Agent-Failures](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html) |
| 下载原件 | [原始 PDF](https://papers.nips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf)；访问 2026-10-25 |
| Raw | [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf\|Multi-Agent-Failures.pdf，54 页]] |
| SHA-256 | `6AFF168D6E201217D3F79611F6AD024590A599A03B97AC2AEB0B0B128BAC374C` |
| 阅读日期与范围 | 2026-10-25；正文 §§1–6（pp.1–10）；Appendix A–B（pp.24–27）、E（p.29）、H（pp.33–35）、I–K（pp.35–37）；实际查看 p.2 Fig.1、p.6 Fig.3/Table2、p.34 Table5、p.35 Fig.10–11。未逐项核读参考文献、Checklist、附录 C/D/F/G 全部内容及 L–N完整提示/轨迹示例；未重标注数据或复现干预。 |
| S001 引用路线 | 引文 48，§4.4；§4.4.1，PDF pp.29,30；书目 pp.79 |

本页页码均按所存 PDF 第一页计数；除 GPTSwarm 的会议卷页码外，引用采用 PDF 内页码。下载后验证标题与哈希，以不覆盖方式归档。作者/版本按实际原件登记，不沿用综述的不同署名。

## 这是一套失败观察与分析工具

**原文陈述：**本篇构建 MAST 分类与 MAST-Data 轨迹数据，用来分析多 Agent 系统为什么失败，不提出一个通用任务求解器。论文收集1642条轨迹、七个开放系统，覆盖编程、数学和通用任务；在150条初始轨迹上以 grounded theory 构建分类，再发展自动标注。它的直接价值是把“协作失败”拆成可定位的行为模式。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=2|§1 · pp.2–3]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=5|§3 · pp.5–6]]

## 如何区分三类问题

| 类别 | 观察对象 | 对读编排论文的用途 |
| --- | --- | --- |
| System Design Issues | 违反任务/角色规范、重复、丢历史、不知终止条件 | 核对职责、状态保存和停止规则是否真正执行 |
| Inter-Agent Misalignment | 对话重置、不澄清、偏题、隐去信息、忽略其他 Agent 输入、推理行动不符 | 区分“有通信通道”和“传了接收者需要的信息” |
| Task Verification | 过早终止、未检查/检查不全、错误检查 | 区分代码能运行、子任务完成和最终目标满足 |

这是本库按14种 failure modes 归纳的用途表；原始定义见 [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=24|Appendix A · pp.24–25]]，分类图见 [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=2|Fig.1 · p.2]]。类别是观察与解释框架，不代表互斥因果机制；同一表面信息缺失可能来自没传、没用或上下文丢失。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=7|§4 · pp.7–8]]

Fig.3 的例子中，执行者读到登录需要电话号码，却只把失败归给 credentials，没有把接口要求传回 supervisor。**本库推断：**增加共享状态或统一格式还不够，必须知道哪个事实影响接收者的决策；但作者关于 theory of mind 与目标训练的讨论是解释/研究观点，并非该图已证明唯一机制。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=6|Fig.3 · p.6]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=8|§4 FC2 · p.8]]

## 标签可信到什么程度

分类定义经三名专家多轮标注和讨论修订，最后平均 κ=0.88；o1 few-shot 标注与人类的一致性为 κ=0.77、F1=0.80。新系统/任务验证报告 κ=0.79。它们说明在此标注条件下能较一致地使用分类，不能等同于真实根因被完全识别。标注集规模较小，且分类与提示经过迭代校准。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=5|§§3.2–3.4、Table2 · pp.5–6]]

不同系统运行不同任务/模型；作者在 Fig.4 和 Fig.5 明确不允许把跨系统失败条数/比率作为性能排名。成功轨迹也可能出现 failure-mode 标签，故标签次数不是终局失败次数。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=8|Fig.4 · p.8]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=26|Fig.5 · p.26]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=36|Appendix J.1、Table7 · p.36]]

## 干预提供的较强证据与限制

AG2 的200条 GSM-Plus 题、两种 LLM、六次重复显示：提示改进与拓扑改变的效果依赖模型，GPT-4 下新拓扑的提升不显著。ChatDev 的 ProgramDev-v0 为32项任务，提示改进使25.0到34.4，循环拓扑使25.0到40.6，即9.4与15.6**个百分点**；不是全1642条轨迹上的统一提升。ChatDev 拓扑干预同时改变验证/终止规则，并带最大迭代截止，不能只归因于“多一条边”。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=33|Appendix H.1–H.2、Table5 · pp.33–34]]

> [!warning] 原文内部张力，暂不合并解释
> H.3 声称两种干预都减少各类失败，但 Fig.10 的 AG2 prompt-intervention 柱在若干类别高于 Original；图中拓扑干预明显较低。图注/正文不足以确认标签计数、调用量和任务完成率怎样对应。本库保留差异，不用“失败标签普遍减少”作为结论，也不据此否定 Table5 的任务准确率。[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=34|Appendix H.3 · p.34]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=35|Fig.10–11 · p.35]]

## 本库如何使用这一证据

对 MetaGPT 和 Magentic-One，本篇是独立的系统分析来源，但其运行版本、任务与模型不同于原方法论文，不能把差异当作同条件复现矛盾。对编排，MAST 支持把职责、信息交接与验证分开检查；对研究探索，它提醒“共识”和“形式完整的交付”都不自动增加证据强度。

**待检验问题：**一次错误交接如何区分发送端遗漏、接收端忽略和状态截断？当前已有分类覆盖这些现象，不能再把命名问题当作创新；更强的因果归因需要受控干预和足够轨迹，这属于下一步证据需求。

## 主题联系与验收状态

已整合到 [[wiki/harness/orchestration|Harness · 编排]]；涉及反馈检查时联系 [[wiki/harness/verification|验证]]。共享主题与索引已同步，已通过主 Agent 内容/结构验收并完成摄入。关键页码和 Raw 哈希已检查，Obsidian 应用渲染与来源跳转未测。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/orchestration|harness/orchestration]] · [[wiki/harness/verification|harness/verification]]。
