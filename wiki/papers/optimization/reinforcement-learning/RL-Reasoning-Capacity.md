---
type: paper
source_id: S078
primary_direction: optimization/reinforcement-learning
related_directions:
  - optimization/finetuning
created: 2026-10-28
updated: 2026-10-28
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf]]"
---

# RLVR 的成功概率与可解覆盖：怎样理解底座能力边界

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S078 |
| 原文标题 | Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model? |
| 作者 | Yang Yue（乐洋）、Zhiqi Chen、Rui Lu、Andrew Zhao、Zhaokai Wang、Yang Yue（乐阳）、Shiji Song、Gao Huang；同名作者依 PDF 首页脚注区分 |
| 版本 | arXiv:2504.13837v5，2025-11-24；正文首页另标 November 25, 2025，两日期保留原标记，不混作同一出版日期 |
| 原始来源 | [固定版本 PDF](https://arxiv.org/pdf/2504.13837v5)；[官方身份页](https://arxiv.org/abs/2504.13837v5)；访问／本轮读取日期 2026-10-28；PDF 首页版本已核对，DOI 未确认 |
| Raw | [[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf\|本地原件，31页]] |
| SHA-256 | `76139EA0BA0E9155569C7AA7B8153502F6A5B23FED717AF0CA9934EC9D764F9A` |
| 实际读取 | pp.1–10；p.11 §5 讨论；pp.12–13 展望与局限；p.19 A.1–A.2；pp.23–25 C.4–C.8。查看 p.4 Fig.2、p.8 Table2／Fig.6、p.19 Eq.2、p.23 Tables3–4 原页图像。其余附录、逐条CoT案例和源码未完整核读；没有复现实验 |
| 选择理由 | [[组会/2026-10-28-Optimization-RL/README\|Optimization-RL组会]] 的争议补读1：约束“RL永远不能拓展能力”这一过强解释，不用于全领域查新 |
| 当前状态 | 已完成内容整合；原件、结构与应用验收分开记录，Obsidian未测 |

## 它测的是采样覆盖，不是实际选中正确答案

**原文陈述。** 对每个问题采样多次，只要至少一次通过验证就算覆盖；数据集平均值表示给定采样预算下的潜在可解比例。作者明确将其与 best-of-N、majority voting 的实际选择用途区分：能生成正确候选，并不等于系统能识别它。文中用每题的 n 次采样估计各 k≤n 的 pass@k；n通常为128、256或1024，具体随基准变化。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=5|§2.2 · p.5]] [[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=19|A.2、Eq.2 · p.19]]

**本库解释。** 单次成功概率、有限预算可解覆盖、候选选择后的成功率是不同对象。底座在较大 k 上胜出，并不能否定 RL 在实际有限调用预算下的收益；反过来，pass@1 提升也不自动证明模型覆盖了此前不会的问题。有限采样未出现某个解，不是其概率严格为零的证明。

## 支持哪些经验判断

**原文实验。** 数学部分比较 Qwen2.5 7B／14B／32B 与 LLaMA3.1-8B 的预训练起点及对应 RLVR 模型；代码和视觉部分有指令／蒸馏模型起点，不能把所有对照的“base”都理解为纯预训练模型。数学主要采用零样本一致提示；常规评估 temperature 0.6、top-p 0.95、生成上限16,384 tokens，DeepCoder比较另用32K。覆盖任务包括数学基准、代码生成和视觉数学，不是多轮工具环境。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=4|§2.1–3、Table1 · pp.4–7]]

在主要 pass@k 曲线中，RL模型在小k更优，底座在较大k追上或超过；这支持“所测训练改善采样效率，却未普遍扩大有限预算覆盖”。作者对数学答案猜中的风险做了部分CoT人工检查，但未逐条证明全部答案的推理正确。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=4|Fig.2 · p.4]] [[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=6|§3.1–3.3 · pp.6–7]]

**原文分析与解释边界。** Table2 中，MATH500 在k=128时有1%问题只被RL模型解出；C.7报告增大底座采样至1024后也能解出这些题。因此这是增加采样后的覆盖证据，不是相同预算下严格包含。对两道AIME题的PPL分析以及附录10题的训练过程分析，支持被检验轨迹与底座先验较接近；不能凭少量轨迹和平均token似然穷尽所有推理机制。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=8|§4.1、Table2、Fig.6 · pp.8–9]] [[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=23|C.4、C.7 · pp.23–24]]

## 为什么不能把它写成普遍不可能性结论

论文部分正文用“底座上界”作较强概括，但附录数值本身要求更精确的限定。Table3 的 MATH500 pass@256 为底座96.2、RLOO97.4；Omni-MATH-Test 为底座69.1、Reinforce++69.7。这些差异没有在本次核读中得到独立显著性判断，但足以说明不能将作者叙述抄成“所有RL训练在所有同预算覆盖指标上必不超过底座”的严格规则。Table4亦显示不同训练阶段不同，不能只取训练末期退化概括整个过程。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=23|C.5、Tables3–4 · p.23]]

**原文局限。** 作者没有取得所有最强模型及私有训练流程，承认新技术可能缓解所见限制。增加rollout的消融同时受训练步数与资源限制；更大规模训练是否改变结论仍留待研究。多轮 Agentic RL、课程、过程信号、高层探索是作者提出的未来方向，本论文没有完成这些路线的验证。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=10|§4.4 · p.10]] [[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=24|C.6 · p.24]] [[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=12|§5、§7 · pp.12–13]]

**本库归纳。** 这篇论文使问题从“RL是否创造能力”变成“在什么底座、反馈、探索和预算下，改善了成功概率、覆盖还是迁移”。它既不支持宣布RL普遍无能力增量，也不证明多轮交互已经解决了能力边界。与SFT的比较还须注意教师提供了额外轨迹信息：§4.2的蒸馏曲线支持该设置的覆盖扩大，不是同信息／同计算成本下的训练算法排名。[[raw/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity.pdf#page=9|§4.2、Fig.7 · p.9]]

## 整合落点与验收边界

已整合到 [[wiki/optimization/reinforcement-learning|Agentic RL]] 的能力测量边界和 [[wiki/optimization/Questions|Optimization问题]] 的宏观讨论；相关概念也写入微调页，索引同步。与 [[wiki/optimization/finetuning|微调]] 的联系是“更好采样、教师迁移和泛化不宜混作同一能力指标”。本轮审查记录见 [[组会/2026-10-28-Optimization-RL/过程/C-前提与反证|C的前提与反证]]。原件与结构验收见 [[组会/2026-10-28-Optimization-RL/README#执行状态|本轮验收]]；Obsidian显示未测，未复现实验。
