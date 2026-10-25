---
type: topic
created: 2026-10-19
updated: 2026-10-19
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
---

# Optimization：能力内化与训练

[[wiki/papers/Towards Long-Horizon Agents|S001]] 按架构基础及六个能力发展环节组织这一主线，共七个入口。它讨论如何把长程行为逐步内化到策略及可训练模块；这是一种组织框架，不意味着每篇方法都必须依次完成七个环节。[[raw/papers/Towards Long-Horizon Agents.pdf#page=37|S001 · §5 · p.37]]

## 页内导航

[[wiki/optimization/Overview#架构基础|架构基础]] · [[wiki/optimization/Overview#数据与环境合成|数据与环境合成]] · [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]] · [[wiki/optimization/Overview#微调|微调]] · [[wiki/optimization/Overview#Agentic Reinforcement Learning|Agentic RL]] · [[wiki/optimization/Overview#On-Policy Distillation|On-Policy Distillation]] · [[wiki/optimization/Overview#自我演化|自我演化]]

## 架构基础

先问长轨迹能否被表示、训练和高效处理。综述按显式上下文、压缩状态、混合架构组织历史表示方式，并将高吞吐机制作为另一条轴：解码或缓存更省，不等于旧证据一定能被准确取回。[[raw/papers/Towards Long-Horizon Agents.pdf#page=37|S001 · §5.1 · p.37]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=40|§5.1.3–5.1.4 · p.40]]

细分导航：Explicit-Context Architectures；Compressed-State Architectures；Hybrid Architectures；High-Throughput Mechanisms。后续原论文需要分别核查信息保留能力与计算收益。

## 数据与环境合成

综述把可训练经验拆成三个耦合对象：任务规定目标和能力压力，环境承载动作与可核查反馈，轨迹记录决策、观察、错误和恢复。记录一串文字动作，不自动等于保留了环境状态变化与验证证据。[[raw/papers/Towards Long-Horizon Agents.pdf#page=40|S001 · §5.2 · p.40]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=43|§5.2.3 · p.43]]

细分导航：Task Synthesis；Environment Synthesis；Trajectory Synthesis。与 [[wiki/applications/Overview|应用接口和评测]]、[[wiki/frontier/Overview|环境真实性问题]] 相连。

## 预训练与中期训练

综述将这一环节作为后续交互学习的能力基础，讨论推理先验、长上下文状态、多模态感知，以及数据混合和训练策略。它区别于直接模仿一条完成任务的交互轨迹。[[raw/papers/Towards Long-Horizon Agents.pdf#page=43|S001 · §5.3 · p.43]]

细分导航：Reasoning Priors；Long-Context State；Multimodal Perception；Data Mixture and Training Strategies。当前尚无独立训练论文的直接证据。

## 微调

监督微调（SFT）用整理过的轨迹教授交互方式，例如分解目标、调用工具、解释观察、恢复和终止。综述的三个入口是示范选择与混合、课程学习、蒸馏；其覆盖范围受到监督轨迹分布的限制。[[raw/papers/Towards Long-Horizon Agents.pdf#page=45|S001 · §5.4 · p.45]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=47|§5.4 小结 · p.47]]

细分导航：Instruction Selection and Mixing；Curriculum Learning；Distillation。不要把某篇工作中“小数据有效”的结果推广成普遍规律；后续须核对基础模型、数据选择与训练管线。

## Agentic Reinforcement Learning

Agentic RL 用自身交互反馈优化策略，目标从单次回答扩展为多轮轨迹。综述拆成四个问题：怎样分配成功/失败的信用、怎样稳定更新策略、采哪些轨迹，以及怎样组织层级、多 Agent 或记忆交互。[[raw/papers/Towards Long-Horizon Agents.pdf#page=47|S001 · §5.5 · Fig.12 · pp.47–48]]

| 子方向 | 主题入口 | 原文定位 |
| --- | --- | --- |
| Credit Assignment | 终局、过程与显式评价准则（rubric）信用；判断哪些决策造成结果 | §5.5.1，p.48 |
| Policy Optimization | 裁剪式更新、按轮次优化、维持探索；将信用转成参数更新 | §5.5.2，p.50 |
| Sampling Strategy | 轨迹采样、树采样、预算控制；决定获取哪些交互经验 | Fig.12，p.47；§5.5.3 起于 p.50 |
| Interaction Patterns | 层级、多 Agent、记忆学习；决定训练交互的结构 | Fig.12，p.47；§5.5.4 起于 p.51 |

表格入口依据 [[raw/papers/Towards Long-Horizon Agents.pdf#page=47|Fig.12]]、[[raw/papers/Towards Long-Horizon Agents.pdf#page=48|§5.5.1]] 与 [[raw/papers/Towards Long-Horizon Agents.pdf#page=50|§5.5.2–5.5.3]]；不是这些子方向有效性的比较。过程奖励与 [[wiki/harness/Overview#验证|运行时验证]] 相关，但需要分别检查判断偏差与优化后的行为。

## On-Policy Distillation

同策略蒸馏（OPD）在学生当前策略实际访问的状态上提供监督，区别于只学习固定专家轨迹。综述再分为教师指导和自我改进式监督；核心阅读问题是“谁产生状态，谁提供纠正信号”。这是一种机制描述，尚不支持 OPD 普遍优于 RL 的结论。[[raw/papers/Towards Long-Horizon Agents.pdf#page=52|S001 · §5.6 · pp.52–53]]

细分导航：Teacher-guided OPD；Self-improving OPD。

## 自我演化

本章讨论的训练式自我演化把生成经验、筛选反馈和策略更新接成循环，并可能更新任务或环境分布。作者区分离线生成—筛选—训练、在线交互更新、Agent—环境共同演化。[[raw/papers/Towards Long-Horizon Agents.pdf#page=54|S001 · §5.7 · Fig.13 · pp.54–55]]

细分导航：Offline Self-evolution；Online Self-evolution；Agent–Environment Co-evolution。这里的范围较窄：外部记忆或技能库的增长，只有被蒸馏、微调、RL 或可训练模块吸收时，才属于该章所说的训练式内化。更广义的外部自我演化见 [[wiki/frontier/Overview|Frontier]]。[[raw/papers/Towards Long-Horizon Agents.pdf#page=55|S001 · §5.7 小结 · p.55]]

## 后续整合原则

当前保留方法入口及其边界，不按每个算法建页。新论文先回答它改了哪个对象、用什么反馈、在哪些条件下有效，再把证据放进相应段落并链接唯一论文页。与 [[wiki/harness/Overview|Harness]] 的关系应通过具体机制和证据说明，不凭分类决定结论。

返回 [[wiki/index|索引]]。
