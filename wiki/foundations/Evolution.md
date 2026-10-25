---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
---

# Evolution：从 Prompt 到 Runtime

[[wiki/surveys/Towards Long-Horizon Agents|S001]] 用“可控制的对象扩大了什么”来组织历史。作者强调三个阶段是嵌套累积关系；阶段年份描述其主导时期，不是相关方法首次发表的时间，也不是后一个阶段淘汰前一个阶段。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=15|S001 · §3 · Table 1 · p.15]]

| 作者的阶段划分 | 控制单位 | 当前可带走的理解 |
| --- | --- | --- |
| Prompt Engineering（2020–2023） | 单次请求的语言表达 | 用提示组织推理、分解和规划；控制主要进入提示文本 |
| Context Engineering（2023–2025） | 单次调用可见的信息 | 选择证据、工具、历史与记忆；关注模型看到了什么 |
| Runtime Harnesses（2025–该版本所述时期） | 整条执行轨迹 | 管理行动、观察、验证、恢复和状态持续性 |

来源：[[raw/surveys/Towards Long-Horizon Agents.pdf#page=15|S001 · §3 · Table 1 · p.15]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=16|Fig.6 · p.16]]。这些时间段是原文的叙事框架，不作为本库对当前发展阶段的独立核验。

## 为什么需要扩大控制范围

综述的解释是：提示不能提供从未输入的外部信息，因此要组织上下文；而只组织单次调用的输入，不能充分管理行动之后的环境变化、错误累积与副作用，因此控制进一步进入运行时。这里保留作者的概念主线，不把所有实际系统强行分成互斥阶段。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=17|S001 · §3.1–3.2 · pp.17–18]]

## 外化与内化并行

作者将“先用外部机制组织行为，再将执行经验用于训练”的往复过程作为主线。运行结构产生轨迹与反馈，训练又可能改变模型对外部结构的依赖。它不是“harness 最终必然消失”的预测。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=19|S001 · §3.3 · pp.19–20]]

**本库的使用方式：**阅读新方法时记录它改变了哪个控制单位，以及改进来自提示、状态组织、运行逻辑还是策略训练。这是一种分析提问方式，不能代替原论文中的对照实验。

## 交叉阅读

- [[wiki/foundations/Formalization|Foundation]] 提供任务依赖和能力层级。
- [[wiki/harness/Overview|Harness]] 展开运行时控制的六个组成部分。
- [[wiki/optimization/Overview|Optimization]] 展开能力内化的七个入口。
- [[wiki/frontier/Overview|Frontier]] 追问这些能力能否跨运行系统和任务迁移。

返回 [[wiki/index|索引]]。
