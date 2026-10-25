---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/ReSum.pdf]]"
  - "[[raw/papers/Longformer.pdf]]"
  - "[[raw/papers/Mamba.pdf]]"
  - "[[raw/papers/Kimi-Linear.pdf]]"
  - "[[raw/papers/GQA.pdf]]"
  - "[[raw/papers/Lost-in-the-Middle.pdf]]"
  - "[[raw/papers/Toolformer.pdf]]"
  - "[[raw/papers/Toolformer-supplement.pdf]]"
  - "[[raw/papers/CodeAct.pdf]]"
  - "[[raw/papers/TaskCraft.pdf]]"
  - "[[raw/papers/SWE-Gym.pdf]]"
  - "[[raw/papers/WebDreamer.pdf]]"
  - "[[raw/papers/TOUCAN.pdf]]"
  - "[[raw/papers/AgentGym-RL.pdf]]"
---

# Optimization：能力内化与训练

[[wiki/papers/Towards Long-Horizon Agents|S001]] 按架构基础及六个能力发展环节组织这一主线，共七个入口。它讨论如何把长程行为逐步内化到策略及可训练模块；这是一种组织框架，不意味着每篇方法都必须依次完成七个环节。[[raw/papers/Towards Long-Horizon Agents.pdf#page=37|S001 · §5 · p.37]]

## 页内导航

[[wiki/optimization/Overview#架构基础|架构基础]] · [[wiki/optimization/Overview#数据与环境合成|数据与环境合成]] · [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]] · [[wiki/optimization/Overview#微调|微调]] · [[wiki/optimization/Overview#Agentic Reinforcement Learning|Agentic RL]] · [[wiki/optimization/Overview#On-Policy Distillation|On-Policy Distillation]] · [[wiki/optimization/Overview#自我演化|自我演化]]

## 架构基础

先问长轨迹能否被表示、训练和高效处理。综述按显式上下文、压缩状态、混合架构组织历史表示方式，并将高吞吐机制作为另一条轴：解码或缓存更省，不等于旧证据一定能被准确取回。[[raw/papers/Towards Long-Horizon Agents.pdf#page=37|S001 · §5.1 · p.37]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=40|§5.1.3–5.1.4 · p.40]]

细分导航：Explicit-Context Architectures；Compressed-State Architectures；Hybrid Architectures；High-Throughput Mechanisms。本轮 S032–S036 已完成原文摄入与主题整合，内容与结构已验收；Obsidian 应用未测。

### 历史留在哪里，下一步怎样使用

这四种机制不能只按“支持多少 token”排列。先看历史的表示，再看模型是否仍能直接访问某个位置；最后单独核对效率。下表是本库依据已读原文构建的比较轴，不是同一基准上的性能排名。

| 机制 | 历史如何保留与访问 | 成立条件与直接证据 |
| --- | --- | --- |
| **显式 token + 稀疏连接** | Longformer 保留 token 表示，多数位置在局部窗口内交换信息，少量任务指定全局位置连通全序列 | 固定窗口和受控全局位置数支撑线性长度成本；全局位置由任务给定，不是已经学会自主识别所有重要状态。[[wiki/papers/Longformer\|S032 Longformer]]；[[raw/papers/Longformer.pdf#page=3\|§3.1、Fig.2 · pp.3–4]] |
| **有限递归状态** | Mamba 不逐 token 留存可寻址历史，让输入相关的 Δ、B、C 决定旧状态延续、写入和读出 | 内容选择与状态大小共同决定保留什么；scan 的实现解决 GPU 计算成本，不能证明任意细节都可恢复。[[wiki/papers/Mamba\|S033 Mamba]]；[[raw/papers/Mamba.pdf#page=5\|§3.1–3.3、Algorithm 2 · pp.5–7]] |
| **压缩层 + 全局层** | Kimi Linear 每三层 KDA 插入一层全局 MLA；KDA 用通道遗忘与 delta 修正更新矩阵状态，全局层保留历史访问 | 固定状态仅适用于 KDA；全模型仍保留增长的 KV 和全注意力项。3:1 是所测配置的折中。[[wiki/papers/Kimi-Linear\|S034 Kimi Linear]]；[[raw/papers/Kimi-Linear.pdf#page=4\|§3、Eq.1 · p.4]]、[[raw/papers/Kimi-Linear.pdf#page=6\|§4、Fig.3 · p.6]]、[[raw/papers/Kimi-Linear.pdf#page=8\|§5.2、Table 1 · p.8]] |
| **KV 头共享** | GQA 让多组 query 共享更少的 KV 头，每个时间位置仍保留；它改变头维度存储与读取成本 | 不是时间历史压缩或检索算法；原文对照基于经 uptraining 的 T5 encoder–decoder。[[wiki/papers/GQA\|S035 GQA]]；[[raw/papers/GQA.pdf#page=2\|§2.2、Fig.2 · PDF p.2 / 印刷 p.4896]]、[[raw/papers/GQA.pdf#page=3\|§3、Table 1 · PDF p.3 / 印刷 p.4897]] |

### 容量、检索、任务质量和效率分别举证

**可运行很长，不代表所有任务都利用了那么长的历史。** Mamba 的百万长度结果包含小词表合成关联任务，以及 DNA / 音频序列；这些不能直接替代百万自然语言 token 的任意检索。Kimi Linear 主长上下文对照是 1.4T 训练后的 128k 测试，而 1M RULER 属于另一个 5.7T checkpoint；不能把两组结果拼成同一个受控实验。[[raw/papers/Mamba.pdf#page=10|S033 §4.1 · pp.10–11]] [[raw/papers/Mamba.pdf#page=13|§4.3–4.4 · pp.13–14]] [[raw/papers/Kimi-Linear.pdf#page=12|S034 §5.5、Table 5 · p.12]] [[raw/papers/Kimi-Linear.pdf#page=28|Appendix D · p.28]]

**显式访问也需要行为检查。** [[wiki/papers/Lost-in-the-Middle|S036 Lost in the Middle]] 固定问题和证据、改变证据位置，在所测旧模型的多文档 QA 中观察到位置差异；但 Claude 的合成 KV 检索近乎完美，Llama-2 7B 主要呈近因偏好。因此它支持“检查位置和干扰”的评测要求，不建立所有模型都遵守的 U 形定律，也没有直接评测 Mamba 或 Kimi Linear。[[raw/papers/Lost-in-the-Middle.pdf#page=5|S036 §2.3、Fig.5 · p.5]] [[raw/papers/Lost-in-the-Middle.pdf#page=7|§3.2、Fig.7 · p.7]] [[raw/papers/Lost-in-the-Middle.pdf#page=16|Appendix E、Fig.16 · p.16]]

**吞吐结果保留部署条件。** Mamba 的生成比较在 A100、2048-token prompt、128-token 输出下改变 batch；Kimi Linear 的 batch=1 图与扩大 batch 后约 6.3× 的论述不能混用；GQA 则按各模型优化批量与分片。它们说明资源配置下的计算行为，不是完整 Agent 运行耗时或成功率。模型质量、任务成功与工具等待需另行测量。[[raw/papers/Mamba.pdf#page=36|S033 Appendix E.5 · p.36]] [[raw/papers/Kimi-Linear.pdf#page=13|S034 Fig.7 · p.13]] [[raw/papers/Kimi-Linear.pdf#page=16|§6.3 · p.16]] [[raw/papers/GQA.pdf#page=3|S035 §3.1–3.2 · PDF p.3 / 印刷 p.4897]]

**待检验阅读问题，尚未查新：**当未来目标尚未出现时，压缩状态需要保留哪些关联，全局访问又能恢复哪些细节？将位置/干扰检查迁移到 Agent 轨迹时，必须保持任务语义和时序依赖，不能任意洗牌后仍当成同一任务。现有证据让问题具体化，尚未证明它是未被研究的缺口；与 [[wiki/harness/Overview#上下文与记忆|运行时状态选择]] 共同讨论。

## 数据与环境合成

综述把可训练经验拆成三个耦合对象：任务规定目标和能力压力，环境承载动作与可核查反馈，轨迹记录决策、观察、错误和恢复。记录一串文字动作，不自动等于保留了环境状态变化与验证证据。[[raw/papers/Towards Long-Horizon Agents.pdf#page=40|S001 · §5.2 · p.40]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=43|§5.2.3 · p.43]]

细分导航：Task Synthesis；Environment Synthesis；Trajectory Synthesis。第一轮 S037–S041 已完成摄入与本节整合，内容与结构验收通过；Obsidian 应用未测。与 [[wiki/applications/Overview|应用接口和评测]]、[[wiki/frontier/Overview|环境真实性问题]] 相连。

### 生成了什么，真实执行到了哪里

**本库比较轴：**先确认被生成的是问题、可执行环境、状态预测还是训练轨迹，再核对标签来源。“真实工具”“可验证任务”和“高质量轨迹”分别描述不同环节，不能相互替代。下表比较机制，不把不同模型与基准的分数排列成优劣。

| 生成或构建对象 | 执行与标签的来源 | 关键限定及原文 |
| --- | --- | --- |
| 任务的依赖结构 | TaskCraft 从真实工具内容抽答案，再以深度扩展替换输入索引、以宽度扩展合并子题；原子任务执行，长链主要做增量语言核查 | 设计好的路径不等于最终问题被端到端成功执行；一个 hop 也不等于一次调用。[[wiki/papers/TaskCraft\|S037 TaskCraft]]；[[raw/papers/TaskCraft.pdf#page=3\|§2–3 · pp.3–6]] |
| 可执行训练环境 | SWE-Gym 将真实 issue、仓库快照、依赖和测试配套；实际运行轨迹的测试成败用于筛选策略数据及训练 verifier | 环境半手工配置；测试标签受测试覆盖限制，学习 verifier 的预测另有误差。[[wiki/papers/SWE-Gym\|S038 SWE-Gym]]；[[raw/papers/SWE-Gym.pdf#page=4\|§3.1 · p.4]]、[[raw/papers/SWE-Gym.pdf#page=7\|§5.1.1 · p.7]] |
| 动作后的状态变化描述 | WebDreamer 先真实网页随机交互，教师根据前后截图描述变化；Dreamer-7B 学习预测这种描述，测试时用模拟辅助选动作 | 不是完整可执行网页模拟器；主实验模拟 H=1，评分器与环境真实成功反馈不同。[[wiki/papers/WebDreamer\|S039 WebDreamer]]；[[raw/papers/WebDreamer.pdf#page=4\|§3.2–3.3 · pp.4–6]]、[[raw/papers/WebDreamer.pdf#page=8\|§5.1 · p.8]] |
| 合成任务与工具交互轨迹 | TOUCAN 从 MCP spec 倒推任务，教师真正调用工具，规则检查调用，模型判断完整与简洁；多轮用户由自模拟产生 | 真实返回不自动验证最终副作用；“可验证性”是质量评分维度，不是统一执行 oracle。[[wiki/papers/TOUCAN\|S040 TOUCAN]]；[[raw/papers/TOUCAN.pdf#page=4\|§3.1–3.2 · pp.4–5]]、[[raw/papers/TOUCAN.pdf#page=32\|Appendix D.4 · p.32]] |
| 当前策略的在线经验 | AgentGym-RL 在独立环境实例中执行当前策略，收集观察和结局反馈，再做 RL；ScalingInter 分阶段提高交互上限 | 真正调用基准环境不等于实机实验；策略、horizon 和重置条件共同决定训练状态分布。[[wiki/papers/AgentGym-RL\|S041 AgentGym-RL]]；[[raw/papers/AgentGym-RL.pdf#page=5\|§3.1、Fig.3 · p.5]]、[[raw/papers/AgentGym-RL.pdf#page=9\|§3.3 · p.9]] |

### 筛选不只改变质量，也改变能学到的状态

TaskCraft 保留特定 Agent 比裸 LLM 答得更好的原子任务；SWE-Gym 训练策略主要使用成功轨迹，并在 MoatlessTools 实验限制每题成功样本数，避免易题占满数据；TOUCAN 排除需凭据/特殊配置的服务器和错误调用轨迹，再按模型标签筛选。这些选择都定义了分布，而非仅从一个不变总体中“去掉噪声”。后一句是本库分析；它提醒后续检查困难状态、替代工具方案和失败恢复经验是否被保留，不表示已测出每种偏差的影响。[[raw/papers/TaskCraft.pdf#page=19|S037 Appendix C.1 · p.19]] [[raw/papers/SWE-Gym.pdf#page=6|S038 §4.3 · p.6]] [[raw/papers/TOUCAN.pdf#page=4|S040 §3.1 · pp.4–5]]

在线 RL 也不是无选择的经验收集。AgentGym-RL 的 WebArena 实验为并行 rollout 排除插入/更新/删除的 Content & Config 任务，使用 372 训练和 50 测试 query；它不支持把结果推广到完整不可逆写入任务。与之对应，WebDreamer 的在线网页规划避免通过真实回退搜索候选，但模拟可能产生不存在的动作；两者解决不同约束，不能合并成“真实环境问题已经解决”。[[raw/papers/AgentGym-RL.pdf#page=32|S041 Appendix B.1 · p.32]] [[raw/papers/WebDreamer.pdf#page=6|S039 §4.1 · p.6]] [[raw/papers/WebDreamer.pdf#page=8|§5.1 · p.8]]

### 从数据量到学习效果，还要保留哪层证据

公开数据规模、实际训练子集和执行预算分别登记：TaskCraft 的 SFT 实验用 3,202 条轨迹；SWE-Gym 的 OpenHands policy 用 491 条成功轨迹；TOUCAN 发布约 1.5M，实验只筛选/重平衡 119.3K。三者都提供具体训练价值的证据，却不构成“更多数据必然更好”的统一实验。SWE-Gym 的一次 OpenHands 自采样再训练还使 Lite 下降，而受限 MoatlessTools 工作流仅小幅改善，说明产生经验的策略与使用经验的方式同样重要。[[raw/papers/TaskCraft.pdf#page=9|S037 §4.4 · p.9]] [[raw/papers/SWE-Gym.pdf#page=5|S038 §4.2–4.3 · pp.5–6]] [[raw/papers/TOUCAN.pdf#page=7|S040 §4.1 · p.7]]

标签需要独立看待：TOUCAN 的任务 judge 与人工对照只有 50 样本、Kimi-K2 Pearson r=0.264；WebDreamer 的 intrinsic evaluation 则通过世界模型加评分器判断正确/偏离动作的排序，平分也算正确。前者不是全数据人工验收，后者不是逐项验证页面转移保真度。原文中的数值口径差异和实验细节留在唯一论文页。[[raw/papers/TOUCAN.pdf#page=20|S040 Appendix C.1、Fig.13 · p.20]] [[raw/papers/WebDreamer.pdf#page=19|S039 Appendix D.1–D.3 · pp.19–20]]

**待检验问题，尚未完成查新：**固定任务、工具版本和总预算后，生成路径是否必要、真实执行是否可达、标签是否准确、筛选后哪些状态缺失，分别能解释多少训练收益？当前五篇将这些问题拆开，尚不能据此宣布研究空白。运行时选择与验证见 [[wiki/harness/Overview#分支能否撤回，评价能否被信任|分支执行]]、[[wiki/harness/Overview#验证|验证]]；参数学习接口见 [[wiki/optimization/Overview#微调|微调]] 和 [[wiki/optimization/Overview#交互上限怎样改变在线训练|在线交互课程]]。

## 预训练与中期训练

综述将这一环节作为后续交互学习的能力基础，讨论推理先验、长上下文状态、多模态感知，以及数据混合和训练策略。它区别于直接模仿一条完成任务的交互轨迹。[[raw/papers/Towards Long-Horizon Agents.pdf#page=43|S001 · §5.3 · p.43]]

细分导航：Reasoning Priors；Long-Context State；Multimodal Perception；Data Mixture and Training Strategies。当前尚无独立训练论文的直接证据。

## 微调

监督微调（SFT）用整理过的轨迹教授交互方式，例如分解目标、调用工具、解释观察、恢复和终止。综述的三个入口是示范选择与混合、课程学习、蒸馏；其覆盖范围受到监督轨迹分布的限制。[[raw/papers/Towards Long-Horizon Agents.pdf#page=45|S001 · §5.4 · p.45]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=47|§5.4 小结 · p.47]]

细分导航：Instruction Selection and Mixing；Curriculum Learning；Distillation。不要把某篇工作中“小数据有效”的结果推广成普遍规律；后续须核对基础模型、数据选择与训练管线。

**工具调用的训练接口（S012 / S014 已完成摄入，应用未测）：**[[wiki/papers/Toolformer|Toolformer]] 用执行结果对后续 token 预测的帮助筛选调用，再微调模型，学到的对象包括调用时机、工具及参数；这个损失代理没有直接优化长程任务成功或调用成本，也没有链式工具训练。[[wiki/papers/CodeAct|CodeAct]] 则需分开动作表示和模型适应：CodeActInstruct 收集并筛选多轮成功及纠错轨迹，与通用对话混合后训练 CodeActAgent。其通用数据消融和不同基础模型表现说明，不能把收益全部归于“代码”或“纠错”一个因素。两者的运行时执行接口见 [[wiki/harness/Overview#工具、MCP 与技能|工具方向]]；AnyTool / Voyager 的候选池或技能库更新不应计作参数微调。[[raw/papers/Toolformer.pdf#page=3|S012 §2 · pp.3–4]] [[raw/papers/Toolformer.pdf#page=9|§6 · p.9]] [[raw/papers/CodeAct.pdf#page=6|S014 §3、Tables 4–5 · pp.6–8]] [[raw/papers/CodeAct.pdf#page=14|Table A.8 · p.14]]


**监督对象与课程范式（S037–S041，已完成摄入，应用未测）：**TaskCraft 用构造的多跳问答轨迹训练策略；SWE-Gym 用实际执行后测试成功的轨迹训练策略，并另外以成功/失败标签训练 verifier；TOUCAN 对真实工具轨迹进行模型质量筛选后做 SFT；WebDreamer 则训练“截图与动作→变化描述”的世界模型组件。它们学的对象不同，不能把共同出现的 fine-tuning 视为同一种 Agent 能力证据。[[raw/papers/TaskCraft.pdf#page=9|S037 §4.4 · p.9]] [[raw/papers/SWE-Gym.pdf#page=5|S038 §4–5 · pp.5–7]] [[raw/papers/TOUCAN.pdf#page=7|S040 §4.1 · p.7]] [[raw/papers/WebDreamer.pdf#page=5|S039 §3.3 · pp.5–6]]

S001 在课程学习小节引用 [[wiki/papers/AgentGym-RL|AgentGym-RL]]；核读原文后须限定：ScalingInter 是**在线 RL 的交互上限课程**，主路线不要求额外任务 SFT，不能充当 SFT 课程有效的直接证据。框架支持 SFT 与方法实际使用 SFT 是不同事实；课程思想的跨范式联系见下节。[[raw/papers/AgentGym-RL.pdf#page=6|S041 §3.2.2 · p.6]] [[raw/papers/AgentGym-RL.pdf#page=9|§3.3 · p.9]]

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

### 交互上限怎样改变在线训练

[[wiki/papers/AgentGym-RL|AgentGym-RL]] 的 ScalingInter 先限制每条在线轨迹的最大轮数，再随训练阶段提高上限。它改变可访问的路径和由当前策略采到的状态，区别于只对固定示范排序，也区别于测试时多试几次。Deep Search 的固定5轮/10轮与渐增轮数曲线支持该设定下的稳定性折中；未匹配全部环境调用/token 的结果，不能把收益只归于课程顺序。[[raw/papers/AgentGym-RL.pdf#page=9|S041 §3.3 · p.9]] [[raw/papers/AgentGym-RL.pdf#page=12|§4.2、Fig.7 · p.12]]

这与 ReSum 的比较共同提出一个归因要求：**状态接口、探索机会与更新算法须分别记录。** AgentGym-RL 的主实验在数字环境中按环境训练，作者承认 in-domain 与物理任务边界；其测试 Pass@K 说明候选覆盖，不证明系统能选对一个结果。具体环境筛选见 [[wiki/optimization/Overview#筛选不只改变质量，也改变能学到的状态|数据分布]]，不能用“无需 SFT”消除基础模型预训练与环境配置成本。[[raw/papers/AgentGym-RL.pdf#page=16|S041 §5.1 · pp.16–17]] [[raw/papers/AgentGym-RL.pdf#page=21|§7 · p.21]]

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
| S032 · [Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=38\|S001 §5.1.1 · p.38 · 引文32]] | 显式上下文与局部/全局稀疏注意力代表；核查可访问历史与计算成本如何折中。 | 完成摄入；应用未测 |
| S033 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=39\|S001 §5.1.2 · p.39 · 引文186]] | 压缩状态路线，与显式保留token对照；核查选择性状态更新和精确回忆的适用边界。 | 完成摄入；应用未测 |
| S034 · [Kimi Linear: An Expressive, Efficient Attention Architecture](https://arxiv.org/abs/2510.26692) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=40\|S001 §5.1.3 · p.40 · 引文842]] | 线性状态与全局MLA的混合路线；区分架构表示能力、训练配方和吞吐收益。 | 完成摄入；应用未测 |
| S035 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://aclanthology.org/2023.emnlp-main.298/) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=40\|S001 §5.1.4 · p.40 · 引文5]] | 服务效率轴代表；避免把KV成本降低直接写成长期状态保持能力提升。 | 完成摄入；应用未测 |
| S036 · [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=38\|S001 §5.1.1; 5.1.3 · p.38,40 · 引文378]] | 分析论文用于检查长窗口与真正使用远处证据的差异，作为架构叙述的证据边界。 | 完成摄入；应用未测 |

### 选读：数据与环境合成

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S037 · [TaskCraft: Automated Generation of Agentic Tasks](https://arxiv.org/abs/2506.10055) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=41\|S001 §5.2.1 · p.41 · 引文540]] | 任务依赖链与可验证任务生成；核查增加依赖深度是否区别于单纯增加交互步数。 | [[wiki/papers/TaskCraft\|完成摄入，应用未测]] |
| S038 · [Training Software Engineering Agents and Verifiers with SWE-Gym](https://proceedings.mlr.press/v267/pan25g.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=41\|S001 §5.2.1; 5.2.2 · p.41,42 · 引文467]] | 真实仓库、可执行环境与测试的符号环境路线；检查环境可复现性与验证器训练的关系。 | [[wiki/papers/SWE-Gym\|完成摄入，应用未测]] |
| S039 · [Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for Web Agents](https://arxiv.org/abs/2411.06559) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=42\|S001 §5.2.2 · p.42 · 引文188]] | WebDreamer作为神经环境/世界模型对照；核查想象的状态转移、训练模拟器与真实执行之间的界限。 | [[wiki/papers/WebDreamer\|完成摄入，应用未测]] |
| S040 · [TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World MCP Environments](https://arxiv.org/abs/2510.01179) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=43\|S001 §5.2.3 · p.43 · 引文737]] | 真实工具执行轨迹代表；检查多工具轨迹是否保留副作用、观察与质量验证。 | [[wiki/papers/TOUCAN\|完成摄入，应用未测]] |
| S041 · [AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2509.08755) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=43\|S001 §5.2.3 · p.43 · 引文701]] | 策略对齐rollout与horizon调度；与固定教师轨迹比较状态分布差异。 | [[wiki/papers/AgentGym-RL\|完成摄入，应用未测]] |

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
| S041 · [AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2509.08755) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=46\|S001 §5.4.2 · p.46 · 引文701]] | 复用数据方向同一篇，核查综述放在SFT章节的horizon curriculum论据；原发布摘要明确其为无需SFT的RL框架，不能据章节归类为SFT方法。 | [[wiki/papers/AgentGym-RL\|完成摄入，应用未测]] |
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
