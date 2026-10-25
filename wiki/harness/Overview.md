---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/HiAgent.pdf]]"
  - "[[raw/papers/MemGPT.pdf]]"
  - "[[raw/papers/A-MEM.pdf]]"
  - "[[raw/papers/ExpeL.pdf]]"
  - "[[raw/papers/ReSum.pdf]]"
  - "[[raw/papers/Lost-in-the-Middle.pdf]]"
---

# Harness：外部运行机制

Harness 是围绕模型组织执行的机制：安排何时调用模型、带入什么状态、执行哪些工具、如何协调与检查。[[wiki/papers/Towards Long-Horizon Agents|S001]] 将它作为长程能力的外化路径，与 [[wiki/optimization/Overview|模型优化]] 共同分析。这里归纳分类与接口责任，尚不评价某个具体方法的优劣。[[raw/papers/Towards Long-Horizon Agents.pdf#page=20|S001 · §4 · p.20]]

## 页内导航

[[wiki/harness/Overview#循环与工作流|循环与工作流]] · [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] · [[wiki/harness/Overview#工具、MCP 与技能|工具、MCP 与技能]] · [[wiki/harness/Overview#编排|编排]] · [[wiki/harness/Overview#Hooks 与中间件|Hooks 与中间件]] · [[wiki/harness/Overview#验证|验证]]

## 循环与工作流

决定模型调用、行动、观察与状态更新如何接续。综述区分沿单条轨迹推进的线性流程、显式维护子目标的计划—执行流程，以及比较候选路径的分支流程。分类回答的是如何控制执行，不直接保证哪种结构效果更好。[[raw/papers/Towards Long-Horizon Agents.pdf#page=20|S001 · §4.1 · p.20]]

细分导航：Linear Workflows（§4.1.1）；Plan-Execute Workflows（§4.1.2）；Branching Workflows（§4.1.3）。后续阅读关注：失败时由谁重规划，状态如何传给下一步？

## 上下文与记忆

当前上下文是这次调用实际可见的状态，持久记忆是能够跨越当前窗口、任务或会话存续的信息。综述用“丢弃、压缩、选择”描述工作上下文的维护，用“写入、维护、检索”描述持久记忆操作。二者区别在存续范围与运行时角色，而不只在文件是否落盘。[[raw/papers/Towards Long-Horizon Agents.pdf#page=23|S001 · §4.2 · Fig.8 · p.23]]

细分导航：Working Context（§4.2.1）；Persistent Memory（§4.2.2）。与 [[wiki/foundations/Formalization#H1–H3 与 C1–C3|C2/C3]] 相关。第一轮 S007–S011 已完成摄入与主题整合，下面是原论文支持的机制比较；内容与结构已验收，Obsidian 应用未测。

### 先区分保存的对象，再问怎样取回

“有记忆”不足以说明后续行为怎样改变。下面沿两个问题比较：**保存的是执行细节、组织后的信息还是经验规则；这些内容怎样重新进入当前决策。** 这是本库依据原文组织的比较轴，不是论文间的性能排名。

| 保存对象与更新边界 | 重新进入决策的方式 | 可回查的原文 |
| --- | --- | --- |
| 当前子目标保留完整行动—观察；完成的子目标改为摘要 | 摘要维持可见进度，需要细节时取回旧轨迹；压缩不等于删除原轨迹 | [[wiki/papers/HiAgent\|HiAgent]]；[[raw/papers/HiAgent.pdf#page=3\|S007 §3 · PDF pp.3–4 / 印刷 pp.32781–32782]] |
| 超出窗口的消息留在 Recall，其他内容可写入 Archival；主上下文单独维护 | 模型经函数读写，队列管理器自动淘汰；heartbeat 可把多步检索连起来 | [[wiki/papers/MemGPT\|MemGPT]]；[[raw/papers/MemGPT.pdf#page=2\|S008 §2 · pp.2–4]] |
| 交互成为带关键词、标签、描述和链接的 notes；新 note 可更新旧 note 组织 | 生成的元信息参与向量检索，关联内容再交给回答模型 | [[wiki/papers/A-MEM\|A-MEM]]；[[raw/papers/A-MEM.pdf#page=3\|S009 Figure 2、§3 · pp.3–5]] |
| 训练任务成败轨迹提炼成可修改的经验规则，成功轨迹另存 | 规则直接加入提示，相似成功轨迹作为示例；无参数更新仍有经验收集阶段 | [[wiki/papers/ExpeL\|ExpeL]]；[[raw/papers/ExpeL.pdf#page=3\|S010 §4、Figure 1 · pp.3–6]] |
| 接近窗口上限时，把搜索历史压成相关证据摘要 | 以“原问题＋摘要”重置上下文并继续搜索；本文用系统阈值触发 | [[wiki/papers/ReSum\|ReSum]]；[[raw/papers/ReSum.pdf#page=3\|S011 §3.1 · p.3]]、[[raw/papers/ReSum.pdf#page=13\|Algorithm 1 · p.13]] |

这组对照澄清了两种容易混淆的扩展：HiAgent / ReSum 主要让**同一任务继续执行**；ExpeL 主要让**不同任务之间复用经验**。MemGPT / A-MEM 提供可跨当前窗口存续的信息与取回机制，其主实验则偏向对话、文档或合成检索。存续范围、操作方式与实际评测任务需要分别登记，不能用“长期记忆”一个词替代三者。[[raw/papers/HiAgent.pdf#page=4|S007 §4.1 · PDF p.4 / 印刷 p.32782]] [[raw/papers/ExpeL.pdf#page=7|S010 §5 · pp.7–9]] [[raw/papers/MemGPT.pdf#page=5|S008 §3 · pp.5–8]] [[raw/papers/A-MEM.pdf#page=5|S009 §4.1 · pp.5–7]]

**补充诊断证据（S036 已完成摄入，应用未测）：**[[wiki/papers/Lost-in-the-Middle|Lost in the Middle]] 的开放域 QA 实验中，增加文档后检索召回仍增长，reader 准确率却较早饱和；把 query 同时放在数据前后，明显改善合成 KV 检索，却没有同样消除语义 QA 的位置趋势。因此本库需分别问“是否取回”“如何编排”和“是否被模型使用”；这不是对上述五种记忆方法的直接反证，也不证明重排能够普遍修复 Agent。对应 [[wiki/optimization/Overview#架构基础|架构基础]] 的有效上下文边界。[[raw/papers/Lost-in-the-Middle.pdf#page=8|S036 §4.2、Fig.9 · p.8]] [[raw/papers/Lost-in-the-Middle.pdf#page=9|§5、Fig.11 · pp.9–10]]

### 机制可比较，分数必须留在原条件中

这些来源并不构成同一评测上的五个竞品。HiAgent 使用 GPT-4、五个行动环境、最多 30 步；MemGPT 的召回对照中，普通模型只见历史摘要而系统可搜索完整历史；A-MEM 的主证据是长对话 QA，检索 k 还按模型与题型调整。ExpeL 有训练任务重试和更强模型归纳经验的成本；ReSum 的主要推理比较为固定工具预算下的网页搜索，但默认摘要器本身经过训练。每项提升必须保留这些条件。[[raw/papers/HiAgent.pdf#page=4|S007 §4 · PDF pp.4–5 / 印刷 pp.32782–32783]] [[raw/papers/MemGPT.pdf#page=5|S008 §3.1.1 · p.5]] [[raw/papers/A-MEM.pdf#page=18|S009 Table 8 · p.18]] [[raw/papers/ExpeL.pdf#page=15|S010 Table 4 · p.15]] [[raw/papers/ReSum.pdf#page=4|S011 §3.2、§4.1 · pp.4–5]]

**本库推断：**工作记忆应同时检查“压缩后保留什么”和“丢失后怎样恢复”，持久经验则应检查“生成的解释如何影响以后检索或行动”。HiAgent 的轨迹取回与 MemGPT 的外部历史让恢复通道具体可见；A-MEM 元信息、ExpeL 规则和 ReSum 摘要均包含模型加工后的理解，不能与原始观察自动视为同等可靠。

**待检验问题，尚非已成立研究缺口：**如何区分写入错误、压缩遗漏、检索提前停止和经验规则不适用？如何在匹配探索预算后判断“更好的状态表示”与“更多继续执行机会”的贡献？ReSum 的训练比较正提示这个归因问题：普通 GRPO 训练限 40 次工具调用，ReSum-GRPO 为 60，不能把收益全部归给训练算法的一项变化。详见 [[wiki/optimization/Overview#Agentic Reinforcement Learning|运行状态与策略训练的接口]]。[[raw/papers/ReSum.pdf#page=15|S011 附录 D.2 · p.15]]

## 工具、MCP 与技能

这一组件规定 Agent 怎样访问外部能力、发现可用工具，以及复用程序性经验。综述将工具接口/协议、主动工具发现、技能库分开组织；工具接口与“如何完成一段工作”的可复用技能承担不同角色。[[raw/papers/Towards Long-Horizon Agents.pdf#page=26|S001 · §4.3 · p.26]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=2|§4.3.1–4.3.3 目录 · p.2]]

细分导航：Tool Interfaces and Protocols；Active Tool Discovery；Skill Libraries。这里只保留主题入口，尚未核读具体协议文档或技能方法论文。

## 编排

编排把工作分配到多个执行循环：拆分任务和角色，决定协调拓扑，调整路由/协调策略，再通过协议交换消息与产物。这是工作组织问题；不能由“用了多个 Agent”直接推出能力提升。[[raw/papers/Towards Long-Horizon Agents.pdf#page=29|S001 · §4.4 · Fig.9 · p.29]]

细分导航：Decomposition and Roles；Coordination Topologies；Orchestration Optimization；Agent Protocols。后续需要核查角色分工、通信、重复劳动与验证对端到端表现的影响。

## Hooks 与中间件

Hooks 在运行流程的特定位置介入，让动作继续、阻止动作或交接控制。综述按规则来源与适应性分成预定义规则、用户定义策略、运行时自适应信号三类。Hooks 可以使用规则或模型判断，因此不应一概当成形式化安全保证。[[raw/papers/Towards Long-Horizon Agents.pdf#page=31|S001 · §4.5 · Fig.10 · p.31]]

细分导航：Pre-defined Rule-based Hooks；Custom User-defined Hooks；Runtime-adaptive Hooks。与 [[wiki/frontier/Overview|可信性前沿]] 相连。

## 验证

验证检查状态、行动、输出或副作用是否满足要求。综述按三条轴组织：**检查什么**（正确性、安全性、指令遵循、验证器一致性）、**何时检查**（步骤中、运行结束）、**怎样产生判断**（自动标签/隐式奖励、验证器引导搜索、验证计算分配）。拦截机制与判断机制可以协作，但不是同一个角色。[[raw/papers/Towards Long-Horizon Agents.pdf#page=34|S001 · §4.6–4.6.1 · p.34]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=36|§4.6.2–4.6.3 · pp.36–37]]

细分导航：Assessment Targets；Verification Levels；Verifier Strategies。与 [[wiki/optimization/Overview#Agentic Reinforcement Learning|训练中的信用分配]]、[[wiki/applications/Overview|评测的成功判据]] 相关；运行时检查有效，不自动证明它可作为可靠训练奖励。

## 后续如何增长

当前六类都是有内容的导航段落，不对应六个空文件夹。新论文进入后，将它实际提供的机制、证据与限制写入相关段落，并链接唯一论文页；当内容需要独立比较时，再拆成如 `Context and Memory.md` 或 `Verification.md` 的页面。



## 第一轮选读队列

2026-10-25 按用户授权从 S001 引用选读。下表仅登记选择理由与来源 ID 预留，**候选并不代表已读**；论文页在正文核读后建立。相同 ID 在多个方向出现只计一个来源。状态以验收和本轮交付为准。


### 选读：循环与工作流

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S002 · [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=21\|S001 §§4.1.1 · p.21 · 引文761]] | 以观察—行动交替作为线性控制基线，后续用它区分响应式循环、显式计划与搜索的改变对象。 | 候选未读 |
| S003 · [ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models](https://arxiv.org/abs/2305.18323) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=21\|S001 §§4.1.2 · p.21 · 引文720]] | 选择推理与工具观察解耦的计划—执行路线，核查它在提前规划、依赖关系和工具失败上的适用前提。 | 候选未读 |
| S004 · [Toward Generalist Autonomous Research via Hypothesis-Tree Refinement](https://arxiv.org/abs/2606.11926) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=21\|S001 §§4.1.2 · p.21,22 · 引文262]] | 选择持久假设树与协调者—执行者循环，理解长期研究如何保存证据、分支和经验；不把其自主实验设置直接等同于本库文献找 idea。 | 候选未读 |
| S005 · [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://papers.nips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=22\|S001 §§4.1.3 · p.22 · 引文760]] | 作为分支搜索的基础机制，核查生成、评分、回溯与提交的控制责任，并保留静态推理任务到交互任务的外推边界。 | 候选未读 |
| S006 · [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://proceedings.mlr.press/v235/zhou24r.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=22\|S001 §§4.1.3；另见 §4.6.3 · p.22,37 · 引文875]] | 与 ToT 对照，追问树搜索怎样结合环境反馈、价值估计与反思，以及评估分支的成本和可回退性。 | 候选未读 |

### 选读：上下文与记忆

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S007 · [HiAgent: Hierarchical Working Memory Management for Solving Long-Horizon Agent Tasks with Large Language Model](https://aclanthology.org/2025.acl-long.1575/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=24\|S001 §§4.2.1；Table 3 · p.24,25 · 引文224]] | 以子目标为单位管理工作记忆，与全文摘要和长期存储区分，核查压缩何时发生及任务进度是否被保留。 | 完成摄入；应用未测 |
| S008 · [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=25\|S001 §§4.2.2；Table 3 · p.25,26 · 引文464]] | 选择分层存储与上下文换页路线，追问谁决定读写、触发中断以及上下文外状态如何重新进入决策。 | 完成摄入；应用未测 |
| S009 · [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=25\|S001 §§4.2.2；Table 3 · p.25,26 · 引文731]] | 选择动态组织、连接和演化的记忆笔记，比较检索相关性、维护操作与任务执行状态之间的关系。 | 完成摄入；应用未测 |
| S010 · [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=25\|S001 §§4.2.2；Table 3 · p.25,26 · 引文853]] | 选择从训练任务轨迹提炼经验但不更新参数的路线，区分事实记忆、经验规律及跨任务复用的证据。 | 完成摄入；应用未测 |
| S011 · [ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization](https://arxiv.org/abs/2509.13313) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=24\|S001 §§4.2.1；Table 3 · p.24,25 · 引文693]] | 选择周期性轨迹摘要，比较摘要接口与训练适配；核查训练免费 ReSum 和 ReSum-GRPO 的实验贡献能否分开。 | 完成摄入；应用未测 |

### 选读：工具、MCP 与技能

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S012 · [Toolformer: Language Models Can Teach Themselves to Use Tools](https://papers.nips.cc/paper_files/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.1 · p.27 · 引文523]] | 提供工具调用能力如何被训练的基础参照，区分调用接口、调用选择和参数学习，避免把所有工具提升归因于外部 harness。 | 候选未读 |
| S013 · [AnyTool: Self-Reflective, Hierarchical Agents for Large-Scale API Calls](https://proceedings.mlr.press/v235/du24h.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.2 · p.27 · 引文140]] | 选择分层工具检索与失败后重新检索，对照固定工具列表；兼顾论文对工具评测协议的质疑。 | 候选未读 |
| S014 · [Executable Code Actions Elicit Better LLM Agents](https://proceedings.mlr.press/v235/wang24h.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.2 · p.27,28 · 引文656]] | 选择可执行代码作为行动空间，比较一次程序组合多个工具与逐个函数调用；分别核查行动表示和配套微调的收益。 | 候选未读 |
| S015 · [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=28\|S001 §§4.3.3；另见 §4.2.2 · p.28,25,26 · 引文630]] | 选择可执行技能库的获取、验证与复用，连接工具表面、持久经验与长程探索，并核查其 Minecraft 环境边界。 | 候选未读 |
| S016 · [MCPMark: A Benchmark for Stress-Testing Realistic and Comprehensive MCP Use](https://arxiv.org/abs/2509.24002) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.1 · p.27 · 引文700]] | 用包含状态改变与程序验收的多步 MCP 任务检查接口能力，防止仅凭单次工具调用成绩判断长期执行能力。 | 候选未读 |

### 选读：编排

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S017 · [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=29\|S001 §§4.4.1；§4.4.4 · p.29,30 · 引文219]] | 作为固定角色和标准流程的代表，与动态生成、中央协调和优化图比较，核查结构收益与角色提示收益如何分离。 | 候选未读 |
| S018 · [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=30\|S001 §§4.4.2 · p.30 · 引文157]] | 选择中央协调者维护进展、重规划和恢复的通用任务系统，比较模块化执行与固定流水线。 | 候选未读 |
| S019 · [GPTSwarm: Language Agents as Optimizable Graphs](https://proceedings.mlr.press/v235/zhuge24a.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=30\|S001 §§4.4.3 · p.30 · 引文897]] | 选择可优化的节点与连边表示，追问编排优化改变信息流还是基础模型，以及优化成本和泛化条件。 | 候选未读 |
| S020 · [TDAG: A Multi-Agent Framework based on Dynamic Task Decomposition and Agent Generation](https://arxiv.org/abs/2402.10178) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=29\|S001 §§4.4.1 · p.29 · 引文660]] | 选择动态任务拆解和临时 Agent 生成，对照固定角色组，核查粒度、上下文交接和级联失败。 | 候选未读 |
| S021 · [Why Do Multi-Agent LLM Systems Fail?](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=29\|S001 §§4.4；§4.4.1 · p.29,30 · 引文48]] | 加入失败分析作为反证视角，核查角色不清、协调错位和验证缺失的证据，避免只收集系统成功故事。 | 候选未读 |

### 选读：Hooks 与中间件

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S022 · [IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems](https://www.ndss-symposium.org/ndss-paper/isolategpt-an-execution-isolation-architecture-for-llm-based-agentic-systems/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=32\|S001 §§4.5.1 · p.32 · 引文698]] | 选择执行隔离的架构路线，核查跨组件消息/工具交互的信任边界，与内容分类型 guardrail 区分。 | 候选未读 |
| S023 · [AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents](https://arxiv.org/abs/2503.18666) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=32\|S001 §§4.5.2 · p.32 · 引文633]] | 选择用户定义 DSL、触发器和谓词约束，区分形式化执行机制的保证与规则本身是否充分。 | 候选未读 |
| S024 · [ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning](https://proceedings.mlr.press/v267/chen25ae.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=33\|S001 §§4.5.2 · p.33 · 引文80]] | 选择政策文档到可验证规则的路线；专门核查编译、规则检索、shielding plan 与执行时判断的分工及保证边界。 | 候选未读 |
| S025 · [InfrastructureSentinel: Policy Enforced Guardrails for Secure MCP-driven Infrastructure Agents](https://ojs.aaai.org/index.php/AAAI/article/view/41468) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=33\|S001 §§4.5.2 · p.33 · 引文285]] | 选择运行时 guardian LLM 解释自然语言政策的路线，与符号执行和静态编译比较灵活性、控制点与误判。 | 候选未读 |
| S026 · [AGrail: A Lifelong Agent Guardrail with Effective and Adaptive Safety Detection](https://aclanthology.org/2025.acl-long.399/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=34\|S001 §§4.5.3 · p.34 · 引文408]] | 选择可生成、优化并跨任务复用安全检查的自适应路线，核查更新对象、反馈可靠性和记忆污染边界。 | 候选未读 |

### 选读：验证

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S027 · [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing](https://arxiv.org/abs/2305.11738) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=35\|S001 §§4.6.2；Table 4 · p.35,36 · 引文182]] | 选择借助外部工具反馈的验证—纠正循环，与纯自评区分；核查反馈来源何时提供新增信息。 | 候选未读 |
| S028 · [AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress](https://arxiv.org/abs/2511.08325) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=35\|S001 §§4.6.2；Table 4 · p.35,36 · 引文702]] | 选择按动作离目标距离和增量进展评分的过程奖励模型，核查验证、搜索引导与训练反馈的界限。 | 候选未读 |
| S029 · [Agent-as-a-Judge: Evaluate Agents with Agents](https://proceedings.mlr.press/v267/zhuge25a.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=35\|S001 §§4.6.2；Table 4 · p.35,36 · 引文898]] | 选择能执行工具和多步判断的评估者，追问评估是否真正检查工作产物与过程证据，以及人与模型一致性的适用条件。 | 候选未读 |
| S030 · [Can LLMs Correct Themselves? A Benchmark of Self-Correction in LLMs](https://papers.nips.cc/paper_files/paper/2025/hash/ec07904adc847a45f53dceb44078f8f0-Abstract-Datasets_and_Benchmarks_Track.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=36\|S001 §§4.6.2 · p.36 · 引文605]] | 加入自我纠错的条件性与成本分析，核查何种模型/任务有收益，防止把反思次数或重复检查本身当作可靠性证明。 | 候选未读 |
| S031 · [On the Multi-turn Instruction Following for Conversational Web Agents](https://aclanthology.org/2024.acl-long.477/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=35\|S001 §§4.6.1 · p.35 · 引文118]] | 补充跨多轮用户指令与环境交互的遵循问题，核查此前约束、当前指令和任务状态怎样共同评测，连接记忆与验证。 | 候选未读 |

返回 [[wiki/index|索引]]。
