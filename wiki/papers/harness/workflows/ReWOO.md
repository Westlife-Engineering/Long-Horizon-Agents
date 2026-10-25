---
type: paper
primary_direction: harness/workflows
source_id: S003
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/harness/workflows/ReWOO.pdf]]"
reading_status: 正文与关键附录已核读
ingest_status: complete
---

# ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

ReWOO 先让 Planner 一次生成带有证据变量的计划，再由 Worker 调用工具填入变量，最后由 Solver 结合计划和证据回答。它减少了每次工具返回后重复发送整段示范与历史的开销。**后续工具可以依赖前一步得到的值，但计划的结构先于观察生成。** 这两个性质可以同时成立，也构成其效率与适应性之间的主要取舍。[[raw/papers/harness/workflows/ReWOO.pdf#page=3|S003 · §2.1 · pp.3–4]]

> [!info] 阅读与摄入状态
> 原文已核读；已整合共享主题与索引并通过主 Agent 内容/结构验收，完成摄入；Obsidian 应用未测。以下结果均是作者报告，本库没有复现实验。论文中“提升百分比”的概述与表格不能混为“百分点”。

## 身份与读取范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S003 |
| 作者 | Binfeng Xu, Zhiyuan Peng, Bowen Lei, Subhabrata Mukherjee, Yuchen Liu, Dongkuan Xu |
| 版本 | arXiv:2305.18323v1，2023-05-23；原件注明 Preprint / Under review |
| 原始来源 | [固定版本 PDF](https://arxiv.org/pdf/2305.18323v1)，访问 2026-10-25 |
| 本地原件 | [[raw/papers/harness/workflows/ReWOO.pdf\|ReWOO.pdf]]，25 页 |
| SHA-256 | `1847BB42B9EFB3A2860CA48EDC962EE9C9B7D3E0359887EA596E1B23084DE9FF` |
| 实际读取 | 2026-10-25；正文 PDF pp.1–9，Appendix A–B（PDF pp.12–14，印刷 pp.13–15）及 C.1 起始例；实际查看 PDF p.2 Fig.1、p.4 Eqs.1–2、p.7 Table2、p.8 Table3/Figs.5–6 的渲染原页 |
| 未系统核读 | 文献表未逐项追索，PDF pp.14–25 的全部轨迹示例未逐项核读；未运行代码、训练或工具接口 |
| 综述入口 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=21\|S001 · §4.1.2 · p.21]]，参考文献 [720] |

## 具体问题：为一次新观察重复提交多少旧文本

作者关注无状态 API 下的工具调用：每得到一次观察，下一次模型请求往往重新包含说明、示范和先前轨迹。观察越长、步骤越多，重复输入越多。ReWOO 针对这个执行形态重组请求，而不是声称自然语言模型不再需要外部知识。[[raw/papers/harness/workflows/ReWOO.pdf#page=1|S003 · §1 · pp.1–3]]

**本库分析：**这里的长程压力主要是一个任务内部的依赖链和重复上下文成本；论文的主要实证是知识问答与数学/科学推理，没有把持续运行数小时、跨窗口恢复或跨任务经验积累作为验证对象。[[raw/papers/harness/workflows/ReWOO.pdf#page=5|S003 · §3.1 · pp.5–6]]

## 机制：计划决定结构，证据变量传递实际值

```mermaid
flowchart LR
    Q[问题与工具说明] --> P[Planner 生成计划及证据占位符]
    P --> W[Worker 按依赖调用工具]
    W -->|实际结果填入 E1、E2 等变量| E[计划与证据配对]
    P --> E
    E --> S[Solver 综合回答]
```

本库依据 Fig.1 与 §2.1 重绘。该基本流程没有画出“观察返回 Planner 重新规划”的边，因为正文方法没有把它作为默认闭环。[[raw/papers/harness/workflows/ReWOO.pdf#page=2|S003 · Fig.1 · p.2]] [[raw/papers/harness/workflows/ReWOO.pdf#page=3|S003 · §2.1 · pp.3–4]]

例如先搜索某饮品，把结果存为 `#E1`；下一步从 `#E1` 提取原料为 `#E2`；再搜索 `#E2` 的生产者。Planner 不必事先知道原料的名字，也能事先写出这些步骤。这依赖于它正确预测“前面工具会提供后面需要的信息”；变量能传递结果，不能保证结果包含预期字段。[[raw/papers/harness/workflows/ReWOO.pdf#page=2|S003 · Fig.1 · p.2]] [[raw/papers/harness/workflows/ReWOO.pdf#page=13|S003 · Appendix A.2 · PDF p.13 / 印刷 p.14]]

Solver 被提示谨慎使用计划与证据，可以依靠自身知识处理简单任务或补偿部分失败。论文中的 Worker 也可以是 LLM 工具，所以“三个模块”不等于固定三次模型调用；作者在实验 token 统计中包含了 LLM 工具的消耗。[[raw/papers/harness/workflows/ReWOO.pdf#page=4|S003 · §2.1–2.2 · p.4]] [[raw/papers/harness/workflows/ReWOO.pdf#page=6|S003 · §3.1 · p.6]]

## 为什么节省，以及证据支持到哪里

§2.2 的公式把重复的输入拆成问题、系统说明、示范和累计轨迹。逐步重传历史会让早期轨迹被多次计数；ReWOO 则主要分别输入 Planner 和 Solver。这个结论依赖文中的请求与计费假设，不能直接当作采用缓存、裁剪历史等其他 harness 的当代成本预测。后一句是本库的适用条件分析，不是本论文测量。[[raw/papers/harness/workflows/ReWOO.pdf#page=4|S003 · §2.2 · Eqs.1–2 · p.4]]

| 设置 | 原文结果与可支持判断 | 证据 |
| --- | --- | --- |
| HotpotQA，1000 题；gpt-3.5-turbo，两工具、六条示范，工具和示范问题与本文 ReAct 对照对齐 | 每题总 token 约 9795 → 1986；GPT-4 评分 Accuracy 40.8 → 42.4，但 EM 32.2 → 30.4。支持明显减少该设置的 token，准确率趋势依赖指标 | [[raw/papers/harness/workflows/ReWOO.pdf#page=6\|§3.1–3.2 · pp.6–7、Table2]] |
| 六个公开 NLP 基准及自建 SOTUQA | 在本文 ReAct 对照的语义 Accuracy 上表现较好，但直接回答或 CoT 在部分任务更好；不能概括为工具规划普遍胜过无工具方法 | [[raw/papers/harness/workflows/ReWOO.pdf#page=7\|Table2 · p.7]] |
| 所有工具统一返回 `No evidence found` | ReWOO 比本文 ReAct 对照保留更多准确率；这是完全缺失证据的特定故障注入，不是工具错误、部分失败、动作副作用等所有异常的恢复测试 | [[raw/papers/harness/workflows/ReWOO.pdf#page=7\|§3.2.1 · pp.7–8、Table3]] |
| 在 HotpotQA 逐步添加额外工具 | 增加无关工具可能损害结果；失败案例涉及工具误用。支持工具选择空间也有成本，不支持“工具越少一定越好” | [[raw/papers/harness/workflows/ReWOO.pdf#page=7\|§3.2.1 · pp.7–8、Fig.5]] |

**数字边界：**Table 2 的 HotpotQA Accuracy 差为 1.6 个百分点，相对 40.8 约为 3.9%；因此摘要的“4% accuracy improvement”不能转写成增加 4 个百分点。正文另用“absolute”描述平均提升，未在本页沿用其概述值；本库优先记录可从表中核对的任务、指标和原值。[[raw/papers/harness/workflows/ReWOO.pdf#page=1|S003 · Abstract · p.1]] [[raw/papers/harness/workflows/ReWOO.pdf#page=6|S003 · §3.2.1 · pp.6–7、Table2]]

论文另将 GPT-3.5 生成并经答案筛选的计划用于微调一个 7B Planner，展示模块化对训练的便利。**替换的是 Planner，并非证明整个系统只需要一个 7B 模型。** 这属于额外训练干预，应与冻结模型上的 prompt 效率结果分开。[[raw/papers/harness/workflows/ReWOO.pdf#page=4|S003 · §2.3 · pp.4–5]] [[raw/papers/harness/workflows/ReWOO.pdf#page=8|S003 · §3.3、Fig.6 · p.8]]

## 最有用的反例：未知环境里，先写全计划可能更困难

作者自己用 ALFWorld 的找花瓶任务说明局限：如果起初不知道物体在哪里，Planner 需要预先枚举可能的搜索位置，失去按观察逐步收缩搜索范围的优势。这是作者的机制反例，不是本文跑出的 ALFWorld 性能对照。[[raw/papers/harness/workflows/ReWOO.pdf#page=8|S003 · §4 · pp.8–9]]

Appendix A.2 的失败分析进一步区分：ReAct 可能在失败工具之间循环；ReWOO 可能产生看似合理但预期错误的计划，例如假设搜索结果必有某人的年龄；即使计划和证据都对，Solver 也可能给出错误结论。这解释了两种结构的不同故障路径，不能简单排列为谁更可靠。[[raw/papers/harness/workflows/ReWOO.pdf#page=12|S003 · Appendix A.2 · PDF pp.12–13 / 印刷 pp.13–14]]

作者将两个不同基础模型的结果差异解释为对话 RLHF 可能损害推理；本库只保留其“换模型后结果变化”的观察，不接受为 RLHF 的独立因果证据，因为不是隔离 RLHF 的受控消融。[[raw/papers/harness/workflows/ReWOO.pdf#page=8|S003 · §3.2.1 · p.8、Table3]]

## 与已有知识的关系

与已读的 [[wiki/papers/harness/workflows/ReAct|ReAct]] 比较，变化在于**何时让观察参与下一步结构决策**：ReAct 每步可根据观察选下一动作，ReWOO 先固定计划的依赖结构，再向结构中填实际值。两者原论文所用模型和测试设置不同，不能把 S002 与 S003 的成绩直接拼成排行榜；S003 自身的 ReAct 对照也调整了工具说明与接口设置。[[raw/papers/harness/workflows/ReAct.pdf#page=3|S002 · §2 · pp.3–4]] [[raw/papers/harness/workflows/ReWOO.pdf#page=6|S003 · §3.1 · p.6]]

已整合到 [[wiki/harness/workflows|Harness · 循环与工作流]]。**待检验问题：**哪些任务的不确定性只影响变量值，哪些会改变下一步应执行的操作结构？目前这只是帮助划分任务与机制的比较问题，不是已经查新的研究缺口。主题与论文页已互链，内容与结构已验收；Obsidian 应用未测。

已核对本地原件、关键图表和引用页码；Obsidian 的图、表、来源跳转与窄分栏未实测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/workflows|harness/workflows]]。
