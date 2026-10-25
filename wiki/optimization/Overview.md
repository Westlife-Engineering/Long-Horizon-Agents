---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/ReSum.pdf]]"
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

### 摘要接续怎样进入策略训练

[[wiki/papers/ReSum|ReSum]] 给出一项已核读的跨模块实例：[[wiki/harness/Overview#上下文与记忆|Harness]] 在摘要后把输入重置为“原问题＋摘要”；ReSum-GRPO 则以这些摘要点分段，把最终答案的二值奖励归一化为轨迹级 advantage，广播到该轨迹各段，工具观察不计策略损失。因此运行时状态接口直接决定训练看到的状态和 rollout 结构；广播终局信号不等于识别了每段独立因果贡献。[[raw/papers/ReSum.pdf#page=4|S011 §3.3、Figure 3 · pp.4–5]]

**归因边界：**training-free ReSum 只指现成策略不再训练，默认摘要器 ReSumTool-30B 自身已蒸馏训练。普通 GRPO 与 ReSum-GRPO 虽共享部分超参数，训练工具调用上限却为 40 对 60，且接续改变了可采到的长轨迹；Table 2 的效果不能全部归于 advantage broadcasting。后续比较需同时登记反馈、状态表示、探索机会与预算，而不能仅按算法名排列。[[raw/papers/ReSum.pdf#page=4|S011 §3.2 · p.4]] [[raw/papers/ReSum.pdf#page=15|S011 附录 D.2 · p.15]] [[raw/papers/ReSum.pdf#page=7|S011 Table 2 · p.7]]

## On-Policy Distillation

同策略蒸馏（OPD）在学生当前策略实际访问的状态上提供监督，区别于只学习固定专家轨迹。综述再分为教师指导和自我改进式监督；核心阅读问题是“谁产生状态，谁提供纠正信号”。这是一种机制描述，尚不支持 OPD 普遍优于 RL 的结论。[[raw/papers/Towards Long-Horizon Agents.pdf#page=52|S001 · §5.6 · pp.52–53]]

细分导航：Teacher-guided OPD；Self-improving OPD。

## 自我演化

本章讨论的训练式自我演化把生成经验、筛选反馈和策略更新接成循环，并可能更新任务或环境分布。作者区分离线生成—筛选—训练、在线交互更新、Agent—环境共同演化。[[raw/papers/Towards Long-Horizon Agents.pdf#page=54|S001 · §5.7 · Fig.13 · pp.54–55]]

细分导航：Offline Self-evolution；Online Self-evolution；Agent–Environment Co-evolution。这里的范围较窄：外部记忆或技能库的增长，只有被蒸馏、微调、RL 或可训练模块吸收时，才属于该章所说的训练式内化。更广义的外部自我演化见 [[wiki/frontier/Overview|Frontier]]。[[raw/papers/Towards Long-Horizon Agents.pdf#page=55|S001 · §5.7 小结 · p.55]]

## 后续整合原则

当前保留方法入口及其边界，不按每个算法建页。新论文先回答它改了哪个对象、用什么反馈、在哪些条件下有效，再把证据放进相应段落并链接唯一论文页。与 [[wiki/harness/Overview|Harness]] 的关系应通过具体机制和证据说明，不凭分类决定结论。



## 第一轮选读队列

2026-10-25 按用户授权从 S001 引用选读。下表仅登记选择理由与来源 ID 预留，**候选并不代表已读**；论文页在正文核读后建立。相同 ID 在多个方向出现只计一个来源。状态以验收和本轮交付为准。


### 选读：架构基础

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S032 · [Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=38\|S001 §5.1.1 · p.38 · 引文32]] | 显式上下文与局部/全局稀疏注意力代表；核查可访问历史与计算成本如何折中。 | 候选未读 |
| S033 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=39\|S001 §5.1.2 · p.39 · 引文186]] | 压缩状态路线，与显式保留token对照；核查选择性状态更新和精确回忆的适用边界。 | 候选未读 |
| S034 · [Kimi Linear: An Expressive, Efficient Attention Architecture](https://arxiv.org/abs/2510.26692) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=40\|S001 §5.1.3 · p.40 · 引文842]] | 线性状态与全局MLA的混合路线；区分架构表示能力、训练配方和吞吐收益。 | 候选未读 |
| S035 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://aclanthology.org/2023.emnlp-main.298/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=40\|S001 §5.1.4 · p.40 · 引文5]] | 服务效率轴代表；避免把KV成本降低直接写成长期状态保持能力提升。 | 候选未读 |
| S036 · [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=38\|S001 §5.1.1; 5.1.3 · p.38,40 · 引文378]] | 分析论文用于检查长窗口与真正使用远处证据的差异，作为架构叙述的证据边界。 | 候选未读 |

### 选读：数据与环境合成

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S037 · [TaskCraft: Automated Generation of Agentic Tasks](https://arxiv.org/abs/2506.10055) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=41\|S001 §5.2.1 · p.41 · 引文540]] | 任务依赖链与可验证任务生成；核查增加依赖深度是否区别于单纯增加交互步数。 | 候选未读 |
| S038 · [Training Software Engineering Agents and Verifiers with SWE-Gym](https://proceedings.mlr.press/v267/pan25g.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=41\|S001 §5.2.1; 5.2.2 · p.41,42 · 引文467]] | 真实仓库、可执行环境与测试的符号环境路线；检查环境可复现性与验证器训练的关系。 | 候选未读 |
| S039 · [Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for Web Agents](https://arxiv.org/abs/2411.06559) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=42\|S001 §5.2.2 · p.42 · 引文188]] | WebDreamer作为神经环境/世界模型对照；核查想象的状态转移、训练模拟器与真实执行之间的界限。 | 候选未读 |
| S040 · [TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World MCP Environments](https://arxiv.org/abs/2510.01179) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=43\|S001 §5.2.3 · p.43 · 引文737]] | 真实工具执行轨迹代表；检查多工具轨迹是否保留副作用、观察与质量验证。 | 候选未读 |
| S041 · [AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2509.08755) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=43\|S001 §5.2.3 · p.43 · 引文701]] | 策略对齐rollout与horizon调度；与固定教师轨迹比较状态分布差异。 | 候选未读 |

### 选读：预训练与中期训练

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S042 · [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437v2) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=44\|S001 §5.3.1 · p.44 · 引文110]] | 基础模型训练配方代表；区分预训练先验、架构和后训练贡献，不用整体分数归因单一机制。 | 候选未读 |
| S043 · [YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=44\|S001 §5.3.2 · p.44 · 引文477]] | 位置扩展路线；与数据配方分开理解可用窗口如何获得，原论文版本需在下载时锁定。 | 候选未读 |
| S044 · [How to Train Long-Context Language Models (Effectively)](https://aclanthology.org/2025.acl-long.366/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=44\|S001 §5.3.2 · p.44 · 引文171]] | ProLong关注训练数据组成、训练长度与指令训练，补足仅从位置编码解释长上下文的不足。 | 候选未读 |
| S045 · [Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution](https://arxiv.org/abs/2409.12191) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=44\|S001 §5.3.3 · p.44 · 引文644]] | 多模态感知与位置表示路线；核查感知能力证据何时可以或不可以外推为长期交互能力。 | 候选未读 |
| S046 · [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](https://papers.nips.cc/paper_files/paper/2023/hash/dcba6be91359358c2355cd920da3fcbd-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=44\|S001 §5.3.4 · p.44,45 · 引文715]] | 数据混合优化与代理模型路线；核查一般预训练数据选择对agent结论的证据距离。 | 候选未读 |

### 选读：微调

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S047 · [AgentTuning: Enabling Generalized Agent Abilities for LLMs](https://aclanthology.org/2024.findings-acl.181/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=45\|S001 §5.4.1 · p.45 · 引文794]] | 交互轨迹与通用指令混合代表；核查agent能力和通用能力保留如何同时评估。 | 候选未读 |
| S048 · [ATLAS: Agent Tuning via Learning Critical Steps](https://aclanthology.org/2025.findings-acl.1299/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=45\|S001 §5.4.1 · p.45 · 引文81]] | 只学习关键决策步骤，与全轨迹模仿形成机制对照；检查关键步骤如何识别及跨环境条件。 | 候选未读 |
| S041 · [AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2509.08755) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=46\|S001 §5.4.2 · p.46 · 引文701]] | 复用数据方向同一篇，核查综述放在SFT章节的horizon curriculum论据；原发布摘要明确其为无需SFT的RL框架，不能据章节归类为SFT方法。 | 候选未读 |
| S049 · [Distilling LLM Agent into Small Models with Retrieval and Code Tools](https://papers.nips.cc/paper_files/paper/2025/hash/99263f9bf46874e2b8b7f104b5063864-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=46\|S001 §5.4.3 · p.46,47 · 引文269]] | 强教师到小模型的轨迹蒸馏；核查检索、代码行动与推理结构各自转移什么。 | 候选未读 |
| S050 · [Agent-R: Training Language Model Agents to Reflect via Iterative Self-Training](https://arxiv.org/abs/2501.11425) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=47\|S001 §5.4.3 · p.47 · 引文789]] | 失败定位和纠正轨迹的自训练；比较离线修复监督、运行时反思与在线策略更新的区别。 | 候选未读 |

### 选读：Agentic Reinforcement Learning

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S051 · [Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning](https://arxiv.org/abs/2503.09516) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=48\|S001 §5.5.1; 5.5.3 · p.48,51 · 引文261]] | 终局奖励与搜索rollout基线；核查搜索、停止与最终正确性之间如何分配学习信号。 | 候选未读 |
| S052 · [ToolRL: Reward is All Tool Learning Needs](https://papers.nips.cc/paper_files/paper/2025/hash/97c5b2707228e7e3fb67e4ecc2e0e607-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=48\|S001 §5.5.1 · p.48,49 · 引文487]] | 工具选择/参数等奖励分解，与稀疏终局信号对照；检查细粒度奖励对真正任务成功的关系。 | 候选未读 |
| S053 · [Group-in-Group Policy Optimization for LLM Agent Training](https://arxiv.org/abs/2505.10978) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=50\|S001 §5.5.2 · p.50 · 引文156]] | episode与step分层优势/比较组；核查局部状态对齐如何改变信用分配。 | 候选未读 |
| S054 · [Tree Search for LLM Agent Reinforcement Learning](https://arxiv.org/abs/2509.21240) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=50\|S001 §5.5.2; 5.5.3 · p.50,51 · 引文250]] | Tree-GRPO树采样与同胞分支比较；检查收益来自采样、信用还是额外预算。 | 候选未读 |
| S055 · [Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning](https://aclanthology.org/2026.acl-long.583/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=52\|S001 §5.5.4 · p.52 · 引文743]] | 将记忆管理作为学习对象；连接Harness记忆方向并检查管理器/回答器的归因。 | 候选未读 |

### 选读：On-Policy Distillation

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S056 · [On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes](https://arxiv.org/abs/2306.13649) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=52\|S001 §5.6 · p.52 · 引文3]] | GKD基础机制：学生生成分布上的教师反馈；核查其任务证据与多轮agent外推边界。 | 候选未读 |
| S057 · [Revisiting DAgger in the Era of LLM-Agents](https://arxiv.org/abs/2605.12913) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=52\|S001 §5.6.1 · p.52,53 · 引文309]] | turn-level教师/学生插值与逐步监督；直接考察多轮状态分布偏移。 | 候选未读 |
| S058 · [MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate](https://arxiv.org/abs/2605.01347) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=53\|S001 §5.6.1 · p.53 · 引文635]] | 多教师讨论形成监督，与单教师OPD比较；重点检查教师错误与成本条件。 | 候选未读 |
| S059 · [π-Play: Multi-Agent Self-Play via Privileged Self-Distillation without External Data](https://arxiv.org/abs/2604.14054) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=53\|S001 §5.6.2 · p.53 · 引文838]] | 训练期特权信息路线；同时核查任务生成/共同演化与综述OPD固定任务边界是否重叠。 | 候选未读 |
| S060 · [Self-Distillation Zero: Self-Revision Turns Binary Rewards into Dense Supervision](https://arxiv.org/abs/2604.12002) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=53\|S001 §5.6.2 · p.53 · 引文216]] | 环境二元反馈转稠密自监督；区分反馈可得与反馈如何改变token级目标。 | 候选未读 |

### 选读：自我演化

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S061 · [STaR: Bootstrapping Reasoning With Reasoning](https://papers.nips.cc/paper_files/paper/2022/hash/639a9a172c044fbb64175b5fad42e9a5-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=54\|S001 §5.7.1 · p.54 · 引文793]] | 离线生成—筛选—训练的基础路线；用于理解自举机制，不自动当成长程交互证据。 | 候选未读 |
| S062 · [rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking](https://proceedings.mlr.press/v267/guan25f.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=54\|S001 §5.7.1 · p.54 · 引文191]] | 搜索与过程偏好模型共同迭代；核查筛选可靠性及policy/verifier共同更新。 | 候选未读 |
| S063 · [R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://arxiv.org/abs/2508.05004) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=55\|S001 §5.7.2 · p.55 · 引文233]] | challenger—solver自举任务分布；与固定任务上的自训练做边界对照。 | 候选未读 |
| S064 · [Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning](https://arxiv.org/abs/2511.16043) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=55\|S001 §5.7.2 · p.55 · 引文704]] | 课程Agent与工具执行者共同演化，比较纯推理任务生成和带工具交互。 | 候选未读 |
| S065 · [Don't Just Fine-tune the Agent, Tune the Environment](https://arxiv.org/abs/2510.10197) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=55\|S001 §5.7.3 · p.55 · 引文401]] | 把环境/任务难度作为更新对象；核查与只更新策略或收集更多轨迹的区别。 | 候选未读 |

返回 [[wiki/index|索引]]。
