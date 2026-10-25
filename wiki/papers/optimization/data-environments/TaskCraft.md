---
type: paper
primary_direction: optimization/data-environments
related_directions:
  - optimization/finetuning
source_id: S037
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/data-environments/TaskCraft.pdf]]"
---

# TaskCraft: Automated Generation of Agentic Tasks

## 来源与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S037 |
| 作者 | Dingfeng Shi、Jingyi Cao、Qianben Chen 等 17 人；完整名单见原始发布页和 PDF p.12 Contributions |
| 版本 | arXiv:2506.10055v2，2025-06-17；PDF 封面标 Date June 18, 2025，保留两种日期口径 |
| 原始入口 | [TaskCraft](https://arxiv.org/abs/2506.10055)；访问日期 2026-10-25 |
| 原件 | [[raw/papers/optimization/data-environments/TaskCraft.pdf\|本地 PDF，共 23 页]] |
| SHA-256 | `E73A88DA040CB86AF752757381CD34C87B6717CDF2B3C24B47B2D1D3D2FB2C85` |
| 实际阅读 | 2026-10-25；正文 pp.1–11、作者页 p.12；附录 A–E pp.16–23；实际查看 p.4–5 方法图/公式、p.9 Table 2–3。参考文献未逐条核读。 |
| S001 定位 | 引文 540，§5.2.1，PDF p.41；书目 p.119 |

以下为原论文直接证据与明确标注的本库分析；未复现实验。页码均为本地 PDF 自首页起算。

## 核心理解：生成依赖链，不等于完整链都被执行验证

TaskCraft 解决的是训练任务与轨迹缺少、人工标注难扩张的问题。它先从网页、PDF、图片的真实工具返回里抽取答案与关系，再反向构造问题；长程压力来自前一子问题的答案决定后一工具输入，以及多个子任务需要汇合。作者的“atomic”省略了定位文件与搜索导航，假设给定详细输入索引后能有限步获取内容，因此一个标注 hop 不是一次实际工具调用。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=3|§2 · p.3]]

| 生成对象 | 怎样改变任务 | 验证到底覆盖什么 |
| --- | --- | --- |
| 原子任务 | 从工具输入索引、真实内容、答案及关系生成问题 | 让带工具 Agent 与裸 LLM 分别回答，再由 judge 比较答案；附录的保留条件是 AgentScore > LLMScore 且 AgentAnswer 非零，不是数学证明所有裸模型都无法解答 |
| 深度扩展 | 用一个新问题替换旧工具索引，让新问题的答案给出旧索引；递归形成依赖链 | 新增片段和替换关系由 LLM 检查 strict superset、唯一性及泄漏；完整长任务不重新由 Agent 执行验证 |
| 宽度扩展 | 合并两个问题和答案，形成可分解子任务 | 合并/改写不自动引入新的顺序依赖，不能与深度 hop 混为同一难度 |
| 轨迹 | 简单任务直接执行记录；复杂任务在扩展和验证时拼接中间计划 | 构造轨迹能提供监督，但不等于某个执行 Agent 从最终问题端到端成功 |

证据：[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=4|§3.1–3.2、Eq.1–3 · pp.4–5]]、[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=6|§3.3 · p.6]]、[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=19|Appendix C.1 · p.19]]。深度约束排除同义改写与直接泄漏，作者在附录给出失败例；这些仍是模型判断的验证流程。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=17|Appendix B · pp.17–19]]

## 实验支持的范围

论文对 1,000 个合成任务用 Smolagents 与增强工具版 Smolagents+ 评测，答案由 0/1/2 分制比较；工具增强同时改变检索与处理能力，模态间难度结果不能单独归因 hop 深度。生成提示优化是筛选 few-shot 示例，优化目标含通过率与可扩展深度；这是生成器改进。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=7|§4.2–4.3 · pp.7–9、Fig.6–7、Table 1–2]]

训练验证采用 **3,202 条多跳任务轨迹**，对 Qwen2.5-3B Base/Instruct 做 SFT，屏蔽搜索返回 token 的训练损失；并在 Search-R1 设定下进一步 RL。评测为 HotpotQA、MuSiQue、Bamboogle 的 Exact Match。Base workflow + SFT 的三项平均从 0.034 到 0.174，Instruct 从 0.113 到 0.173；Search-R1 后加此初始化的收益对 Base 更明显，Instruct 平均仅从 0.230 到 0.236。它支持该配方下的搜索问答训练价值，不支持任意多工具长任务同幅度改善。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=9|§4.4、Table 3 · pp.9–10]]

预算与检索条件：RL 沿用 NQ+HotpotQA 训练集、2018 Wikipedia、E5 检索、每次 3 段，PPO 500 步、动作预算 4。SFT 数据不能与论文全部生成数据量混用；摘要/结论称约 36k，p.2 贡献列表另写 about 32k，本文保留其内部口径差异，不据此给出唯一精确规模。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=22|Appendix D · pp.22–23]]、[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=2|§1 · p.2]]

## 对当前知识的影响与待检验边界

**本库推断：**任务构造时的可分解路径、筛选模型认为有工具必要性、最终任务可在真实环境复现，是三个不同证据层级。增量验证节约成本，却可能保留组合后的歧义、检索捷径或累积错误；本文没有证明所有长合成任务均须走标注链。筛选也倾向“特定 Agent 能解、特定裸 LLM 较差”的任务分布，并非中立的难度采样。

与 Self-Instruct 等的差异目前只采用作者 §5 的比较，未独立核读那些原论文。最有价值的后续核查是：固定工具、任务内容与预算，对扩展链独立重执行，分别统计依赖必要性、答案正确性与整体可达性；这属于验证需求，未完成查新，不宣称创新缺口。

## 主题联系与验收状态

已整合至 [[wiki/optimization/data-environments|数据与环境合成]]；监督轨迹接口亦见 [[wiki/optimization/finetuning|微调]]。主题、索引、互链与摄入日志已同步；主 Agent 已完成内容与结构验收，Raw 哈希匹配。Obsidian 应用未测，未复现实验。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/data-environments|optimization/data-environments]] · [[wiki/optimization/finetuning|optimization/finetuning]]。
