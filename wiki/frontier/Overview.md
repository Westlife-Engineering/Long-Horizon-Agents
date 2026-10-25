---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
---

# Frontier：前沿与待检验问题

当前尚未选定细分研究方向。本页分别保存 [[wiki/papers/Towards Long-Horizon Agents|S001]] 作者的展望、本库的疑问和证据缺口；这些内容不是已经成立的研究成果。

## 作者提出的四条前沿轴

S001 将 §7 明确写作作者的立场与展望，分为四条轴、九个方向。下表是其 Table 8 的简要归纳。[[raw/papers/Towards Long-Horizon Agents.pdf#page=67|S001 · §7 · p.67]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=68|Table 8 · p.68]]

| 前沿轴 | 方向 | 作者指出的开放挑战与展望 |
| --- | --- | --- |
| Evolution | Self-evolving Harness and Agents | 改进目标与范围仍多由人设定；需要控制长期漂移与过拟合 |
| Evolution | Harness Generalization and Transferability | 模型与特定运行机制绑定；研究跨 harness 训练、可移植经验与协议 |
| Evolution | Continual and Lifelong Learning | 外部经验有噪声，参数更新可能遗忘；研究经过验证的经验积累与内化 |
| Effectiveness | Real-world Environment Interaction | 真实交互慢、贵且部分不可逆；模拟与合成环境需检查真实性 |
| Effectiveness | From Digital to Embodied Agents | 慢规划与快控制时间尺度冲突；研究分层控制和多尺度反馈 |
| Efficiency | Cost- and Budget-aware Agency | 感知成本、判断不可行、运行中调整路线并执行预算上限 |
| Efficiency | Multimodal and Omni Harnesses | 跨模态证据保留、预算分配和验证仍缺统一组织方式 |
| Trustworthiness | Reflection and Error Robustness | 反馈延迟且有噪声；需要及时发现失败、转换路径与外部校验 |
| Trustworthiness | Safety and Governance | 外部输入和经验复用会带入风险；自我修改需要保持约束并独立验证 |

作者对环境建设、harness 作用和未来演进的强判断，应继续作为待检验立场保存；不能因为它们出现在综述结论中就视为已证明。

## 本库的待检验问题

以下三个问题是**本库据综述提出的阅读问题**，不是用户已经选择的研究方向，也不构成“尚无人研究”的新颖性判断。

| 问题 | 提问依据与关联主题 | 下一步需要什么证据 |
| --- | --- | --- |
| 相同模型在不同 harness 下的差异，有多少来自状态、动作接口或验证器？ | [[raw/papers/Towards Long-Horizon Agents.pdf#page=69\|S001 · §7.1.2 · p.69]]；[[wiki/harness/Overview\|Harness]]、[[wiki/applications/Overview\|评测]] | 阅读控制模型与任务条件、改变 harness 组件的原论文，核对预算与接口差异 |
| 跨上下文恢复后，怎样确认关键约束与任务进度没有被摘要损坏？ | [[raw/papers/Towards Long-Horizon Agents.pdf#page=23\|S001 · §4.2 · p.23]]；[[wiki/foundations/Formalization\|H2/C2]] | 具有可检查状态与恢复测试的原论文；区分事实召回、约束保留和任务成功 |
| 什么证据足以说明经验应从外部记忆进入模型参数？ | [[raw/papers/Towards Long-Horizon Agents.pdf#page=70\|S001 · §7.1.3 · p.70]]；[[wiki/optimization/Overview#自我演化\|自我演化]] | 比较外部复用与参数更新的任务迁移、遗忘和成本，而非只看当前任务成绩 |

这些问题由初始化时的阅读提出，尚未被用户选为最终研究问题。2026-10-25已完成Harness与Optimization共64篇独立论文的首轮摄入，原有问题将结合这些证据接受独立讨论与修订；它们目前仍是宽泛阅读问题，不自动升级为新颖研究缺口。

## 需保留的原文表述张力

**T001：终身学习是否是所有长程 Agent 的必要条件？**

- §2.4.3 明确允许 H1/H2 Agent 使用固定策略与临时状态完成任务，不要求自我演化。[[raw/papers/Towards Long-Horizon Agents.pdf#page=14|S001 · p.14]]
- §7.1.3 在讨论跨任务、持续改进的展望时，将终身学习称为长程能力的必要条件。[[raw/papers/Towards Long-Horizon Agents.pdf#page=70|S001 · p.70]]

**本库推断：**后一句可能针对作者期望的 H3/长期部署目标，前一句则覆盖 H1/H2 定义；但原文没有在这句“必要条件”中明确限定范围。因此暂记为适用范围待澄清，不将“所有长程 Agent 都必须终身学习”写入 [[wiki/foundations/Formalization|基础定义]]。状态：开放，等待更精确的定义讨论或后续证据。

## 当前证据缺口

Harness六方向与Optimization七方向已各有约5篇独立原文摄入，机制与条件比较见对应主题；综述的其他引用仍未逐项核验。当前没有复现实验，跨论文的任务、模型、预算与验证权限也不相同。本轮接下来通过共同证据上的独立Brainstorm、定向查新与反证，判断哪些问题已经被覆盖、哪些仍需补充材料。来源数和实际阅读范围见 [[wiki/index|索引]]。
