# Long-Horizon Agents 知识库

这里积累关于长程 Agent 的定义、机制、证据和研究问题。当前处于**建立地图与文献驱动的 idea 探索阶段，未选定具体研究问题**。

## 当前证据边界

- 已登记 **86篇学术来源**：S001综述及S002–S086八十五篇独立论文；第一轮64篇核心选读、5篇定向补读，Application另核读6篇，Optimization-RL讨论新增3篇，用户指定Terminal-Bench与RRSI，本次Terminal-Bench比较新增5篇前作。S002–S086已完成摄入，各篇实际读取与应用未测范围见唯一页。核心65个方向名额中O2/O4复用S041，同篇不重复计数。
- S001整体为地图式阅读，Foundation（§2，PDF pp.7–15）已补充问题驱动精读；§6 Application已完整核读并补充6篇代表论文机制比较；§5已回核整体结构，以7篇定向原文形成3个RL问题和6个宏观讨论问题；其余论文实际正文、附录及实现读取范围见唯一页，均不表示全文所有附录/实现已审或复现实验。未读综述引用和搜索线索不是直接证据。
- 第一轮核心阅读、补读、两轮Brainstorm与跨模块综合已完成；保留4张材料问题卡，**未确认新颖研究缺口，未选定最终课题**。内容与结构已验收，Obsidian新页应用验收未完成。
- 五篇综述外补读为TRACE、BRIDGE、SpecRover、C3、R-Quest，理由与预算见[[maintenance/research/R001#第一轮查新补读|Harness]]和[[maintenance/research/R001#Optimization：第一轮查新补读|Optimization]]；Agent-R/GiGPO同源代码补充不增加论文数。方法论资料[[raw/articles/llm-wiki|LLM Wiki]]不计学术来源数。

## 从哪里开始

[[wiki/overview|领域总览]]：用系统耦合、任务层级与证据边界理解整张地图。

**第一轮研究成果从[[wiki/frontier/Overview#第一轮结果与亲读入口|四个问题与亲读路线]]进入**；模块细节分别见[[wiki/harness/Questions#第一轮Brainstorm结案|Harness讨论结案]]、[[wiki/optimization/Questions#第一轮Brainstorm结案|Optimization讨论结案]]。下面的Foundation仍是基础定义的默认图解入口。

本次准备与学长讨论RL，可从 [[wiki/optimization/Overview|第5章整体结构]] → [[wiki/optimization/Questions#2026-10-28：从整体理解转向RL提问|三个具体问题与六个宏观问题]] → [[组会/2026-10-28-Optimization-RL/讨论记录|完整组会讨论]] 阅读。

评估 Terminal-Bench 的实际进步，从 [[wiki/applications/terminal-bench-comparison|五篇前作与八项主张的反证审视]] 进入：区分新增技术任务覆盖、设计取舍、质量控制与尚未证明的总体优越。

## Foundation：从图解笔记开始

**[[wiki/foundations/Formalization|定义、运行循环与理解辨析]]** 是默认阅读入口。流程图放在运行机制旁，反馈与成功的辨析接在循环之后，纠错恢复与时间代理接在任务分层之后；详细推导和依据按需展开。

已有具体困惑时，可以用 [[wiki/foundations/Formalization#从这套基础定义还能多理解什么|问题导航]] 直接进入。其他主题在后续阅读和更新时按内容需要逐步改善展示。

## 六个初始视角

六个视角沿用 S001 的组织方式（[[raw/surveys/Towards Long-Horizon Agents.pdf#page=6|§1 · p.6]]），是导航起点，不是永久分类。

| 视角 | 页面 | 这里回答什么 |
| --- | --- | --- |
| Foundation | [[wiki/foundations/Formalization\|定义、运行循环与理解辨析]] | 从状态—观察—上下文理解 Agent 循环，串起任务依赖、H1–H3、记忆与自我演化，并区分定义、推断和评测代理。 |
| Evolution | [[wiki/foundations/Evolution\|从 Prompt 到 Runtime]] | 控制对象怎样从单次提示扩展到完整执行轨迹？ |
| Harness | [[wiki/harness/Overview\|外部运行机制]] | 六类运行机制、原文条件比较，以及记忆使用/修复验证的收窄问题。 |
| Optimization | [[wiki/optimization/Overview\|能力内化与训练]] | 训练条件、能力形成与经验循环；三个RL问题、六个宏观讨论及历史下钻问题。 |
| Application | [[wiki/applications/Overview\|应用与评测]] | 五类接口的应用地图；六篇代表论文解释成功机制、归因与耦合瓶颈。 |
| Frontier | [[wiki/frontier/Overview\|前沿与待检验问题]] | 第一轮研究结果、跨模块联系、查新范围与亲读路线；另保留作者展望。 |

Harness 与 Optimization 的Overview保留地图；13个方向综合与两份问题页已独立列出。论文目录按主归属分层，交叉方向仍共享唯一来源。

## 学术来源目录

正文与唯一页按主归属镜像分类；一篇只保存一份，交叉方向通过链接表达。下列分类是本库导航判断，不改变原论文类型或综述的初始选文队列。

### 综述

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S001 | [[wiki/surveys/Towards Long-Horizon Agents\|Towards Long-Horizon Agents]] | survey | — | 地图来源与阅读记录；Foundation、Optimization与Application的定向回读及证据落点 |

### harness/workflows · 循环与工作流

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S002 | [[wiki/papers/harness/workflows/ReAct\|ReAct]] | harness/workflows | — | 完成摄入，应用未测；思考与环境观察的区别、交互历史和提示敏感性 |
| S003 | [[wiki/papers/harness/workflows/ReWOO\|ReWOO]] | harness/workflows | — | 完成摄入，应用未测；预定计划结构、证据变量与未知环境的适用边界 |
| S004 | [[wiki/papers/harness/workflows/Arbor\|Arbor]] | harness/workflows | — | 完成摄入，应用未测；假设树、实验事实与解释、版本隔离及评测准入边界 |
| S005 | [[wiki/papers/harness/workflows/Tree-of-Thoughts\|Tree-of-Thoughts]] | harness/workflows | — | 完成摄入，应用未测；部分解搜索、模型误剪和最终输出选择 |
| S006 | [[wiki/papers/harness/workflows/LATS\|LATS]] | harness/workflows | — | 完成摄入，应用未测；环境反馈、MCTS与反思，以及可回退性和oracle条件 |
| S072 | [[wiki/papers/harness/workflows/Agentless\|Agentless]] | harness/workflows | harness/verification | 固定定位—修复—验证；补丁选择消融及生成测试的语义边界；未复现、应用未测。 |

### harness/memory · 上下文与记忆

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S007 | [[wiki/papers/harness/memory/HiAgent\|HiAgent]] | harness/memory | — | 完成摄入，应用未测；子目标工作记忆、摘要与轨迹取回 |
| S008 | [[wiki/papers/harness/memory/MemGPT\|MemGPT]] | harness/memory | — | 完成摄入，应用未测；分层存储、函数读写与控制流接续 |
| S009 | [[wiki/papers/harness/memory/A-MEM\|A-MEM]] | harness/memory | — | 完成摄入，应用未测；notes 关联/演化与长对话问答证据 |
| S010 | [[wiki/papers/harness/memory/ExpeL\|ExpeL]] | harness/memory | — | 完成摄入，应用未测；跨任务经验规则与成功轨迹检索 |
| S011 | [[wiki/papers/harness/memory/ReSum\|ReSum]] | harness/memory | optimization/reinforcement-learning | 完成摄入，应用未测；摘要接续与策略适应训练的接口和归因边界 |
| S066 | [[wiki/papers/harness/memory/TRACE\|TRACE]] | harness/memory | — | 综述外补读，完成摄入；返回时记忆准入、隐式失效与准入/使用错误分离；应用未测 |

### harness/tools · 工具、MCP 与技能

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S013 | [[wiki/papers/harness/tools/AnyTool\|AnyTool]] | harness/tools | — | 完成摄入，应用未测；分层工具发现、失败驱动候选池更新与评价口径 |
| S014 | [[wiki/papers/harness/tools/CodeAct\|CodeAct]] | harness/tools | optimization/finetuning | 完成摄入，应用未测；可组合代码动作、执行反馈与配套微调的区分 |
| S015 | [[wiki/papers/harness/tools/Voyager\|Voyager]] | harness/tools | harness/memory | 完成摄入，应用未测；程序性技能获取与跨任务复用，以及环境和成功判定条件 |
| S016 | [[wiki/papers/harness/tools/MCPMark\|MCPMark]] | harness/tools | harness/verification | 完成摄入，应用未测；有状态 MCP 任务、程序验收与重复运行可靠性 |
| S071 | [[wiki/papers/harness/tools/SWE-agent\|SWE-agent]] | harness/tools | harness/verification | 同模型接口消融；搜索、编辑与上下文组织的贡献；未复现、应用未测。 |
| S075 | [[wiki/papers/harness/tools/VideoSeek\|VideoSeek]] | harness/tools | harness/workflows, harness/memory | 长视频主动观察与同帧对照；证据选择、感知与推理的边界；未复现、应用未测。 |
| S076 | [[wiki/papers/harness/tools/Toolathlon\|Toolathlon]] | harness/tools | harness/verification | 跨应用状态、对象覆盖与终态验证；单例成功和重复可靠性区别；未复现、应用未测。 |
| S080 | [[wiki/papers/harness/tools/Terminal-Bench\|Terminal-Bench]] | harness/tools | harness/verification | 困难终端任务、现实验收与人工对齐；已结合五篇前作重审覆盖和优越性主张；未复现、应用未测。 |
| S082 | [[wiki/papers/harness/tools/SWE-bench\|SWE-bench]] | harness/tools | harness/verification | 完成摄入；真实issue与修复／回归测试，结果通过与专业质量的距离；固定v2，未复现、应用未测。 |
| S083 | [[wiki/papers/harness/tools/SWE-Lancer\|SWE-Lancer]] | harness/tools | harness/verification | 完成摄入；历史付费任务、E2E验收与经济价值代理；ICML会议版，未复现、应用未测。 |
| S084 | [[wiki/papers/harness/tools/AppWorld\|AppWorld]] | harness/tools | harness/verification | 完成摄入；可控模拟应用、状态差分与场景变体一致性；固定v1，未复现、应用未测。 |
| S085 | [[wiki/papers/harness/tools/OSWorld\|OSWorld]] | harness/tools | harness/verification | 完成摄入；真实OS与GUI／CLI任务，人类基线和副作用验收边界；NeurIPS会议版，未复现、应用未测。 |
| S086 | [[wiki/papers/harness/tools/tau-bench\|τ-bench]] | harness/tools | harness/verification | 完成摄入；动态用户、政策、状态评分与重复成功，区分过程合规；ICLR会议版，未复现、应用未测。 |

### harness/orchestration · 编排

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S017 | [[wiki/papers/harness/orchestration/MetaGPT\|MetaGPT]] | harness/orchestration | harness/verification | 完成摄入，应用未测；固定角色、结构化产物与订阅依赖，保留反馈/角色消融边界 |
| S018 | [[wiki/papers/harness/orchestration/Magentic-One\|Magentic-One]] | harness/orchestration | harness/verification | 完成摄入，应用未测；双账本与停滞重规划，区分固定团队与动态调度 |
| S019 | [[wiki/papers/harness/orchestration/GPTSwarm\|GPTSwarm]] | harness/orchestration | harness/verification | 完成摄入，应用未测；可学习通信图与节点提示，分开优化和框架展示证据 |
| S020 | [[wiki/papers/harness/orchestration/TDAG\|TDAG]] | harness/orchestration | harness/verification | 完成摄入，应用未测；按结果调整子任务、定制执行者与文本技能可靠性 |
| S021 | [[wiki/papers/harness/orchestration/Multi-Agent-Failures\|Multi-Agent-Failures]] | harness/orchestration | harness/verification | 完成摄入，应用未测；失败模式分类、标注与干预，区分过程缺陷和因果归因 |
| S067 | [[wiki/papers/harness/orchestration/BRIDGE\|BRIDGE]] | harness/orchestration | — | 综述外补读，完成摄入；依赖图、成对故障校准与选择性交接修复，保留局部回滚和完整成本边界；应用未测 |

### harness/hooks · Hooks 与中间件

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S022 | [[wiki/papers/harness/hooks/IsolateGPT\|IsolateGPT]] | harness/hooks | harness/verification | 完成摄入，应用未测；跨应用执行/记忆隔离、权限交接与人工警告边界 |
| S023 | [[wiki/papers/harness/hooks/AgentSpec\|AgentSpec]] | harness/hooks | harness/verification | 完成摄入，应用未测；事件–谓词–处置 DSL、规则充分性与正常任务误拒 |
| S024 | [[wiki/papers/harness/hooks/ShieldAgent\|ShieldAgent]] | harness/hooks | harness/verification | 完成摄入，应用未测；政策规则电路与在线模型判断，修订全静态分类理解 |
| S025 | [[wiki/papers/harness/hooks/InfrastructureSentinel\|InfrastructureSentinel]] | harness/hooks | harness/verification | 完成摄入，应用未测；输入/计划/执行/审计四处治理与初步实验报告边界 |
| S026 | [[wiki/papers/harness/hooks/AGrail\|AGrail]] | harness/hooks | harness/verification | 完成摄入，应用未测；可演化检查清单、跨任务记忆与条件评测口径 |

### harness/verification · 验证

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S027 | [[wiki/papers/harness/verification/CRITIC\|CRITIC]] | harness/verification | — | 已完成摄入；应用未测；工具反馈、critique、修订与停止，保留oracle和误改边界 |
| S028 | [[wiki/papers/harness/verification/AgentPRM-Xi\|AgentPRM-Xi]] | harness/verification | — | 已完成摄入；应用未测；promise/progress评分、搜索选择与末步PPO奖励粒度 |
| S029 | [[wiki/papers/harness/verification/Agent-as-a-Judge\|Agent-as-a-Judge]] | harness/verification | — | 已完成摄入；应用未测；按需求读取产物、人工一致性与尚未实测在线修复 |
| S030 | [[wiki/papers/harness/verification/CorrectBench\|CorrectBench]] | harness/verification | — | 已完成摄入；应用未测；纠错/误改双向指标、净收益和额外预算口径 |
| S031 | [[wiki/papers/harness/verification/Self-MAP\|Self-MAP]] | harness/verification | harness/memory | 已完成摄入；应用未测；跨轮指令、静态HTML快照和记忆rationale，TSR为Turn |
| S070 | [[wiki/papers/harness/verification/SpecRover\|SpecRover]] | harness/verification | — | 综述外补读，完成摄入；联合核对意图、补丁与测试，区分回归失败、旧测试失效和选择后正确性；应用未测 |

### optimization/architecture · 架构基础

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S032 | [[wiki/papers/optimization/architecture/Longformer\|Longformer]] | optimization/architecture | — | 完成摄入，应用未测；显式 token 的局部/全局稀疏访问 |
| S033 | [[wiki/papers/optimization/architecture/Mamba\|Mamba]] | optimization/architecture | — | 完成摄入，应用未测；输入相关的有限递归状态与长度/吞吐证据边界 |
| S034 | [[wiki/papers/optimization/architecture/Kimi-Linear\|Kimi-Linear]] | optimization/architecture | — | 完成摄入，应用未测；KDA/MLA 混合与训练版本、缓存和吞吐条件 |
| S035 | [[wiki/papers/optimization/architecture/GQA\|GQA]] | optimization/architecture | — | 完成摄入，应用未测；KV 头共享、解码成本与时间历史压缩的区别 |
| S036 | [[wiki/papers/optimization/architecture/Lost-in-the-Middle\|Lost-in-the-Middle]] | optimization/architecture | harness/memory | 完成摄入，应用未测；位置稳健性、检索召回与上下文使用的区别 |

### optimization/data-environments · 数据与环境合成

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S037 | [[wiki/papers/optimization/data-environments/TaskCraft\|TaskCraft]] | optimization/data-environments | optimization/finetuning | 完成摄入，应用未测；依赖结构生成、增量语言核查与端到端执行的区别 |
| S038 | [[wiki/papers/optimization/data-environments/SWE-Gym\|SWE-Gym]] | optimization/data-environments | harness/verification, optimization/finetuning | 完成摄入，应用未测；可执行仓库、测试标签、成功轨迹筛选与 verifier 重排 |
| S039 | [[wiki/papers/optimization/data-environments/WebDreamer\|WebDreamer]] | optimization/data-environments | optimization/finetuning | 完成摄入，应用未测；真实交互监督的状态预测、执行前模拟与评分边界 |
| S040 | [[wiki/papers/optimization/data-environments/TOUCAN\|TOUCAN]] | optimization/data-environments | optimization/finetuning | 完成摄入，应用未测；MCP 真实返回、合成用户/任务与质量筛选分布 |

### optimization/pretraining · 预训练与中期训练

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S042 | [[wiki/papers/optimization/pretraining/DeepSeek-V3\|DeepSeek-V3]] | optimization/pretraining | optimization/architecture | 完成摄入，应用未测；组合配方、MLA、MTP与扩窗，以及后训练工程结果的归因层次 |
| S043 | [[wiki/papers/optimization/pretraining/YaRN\|YaRN]] | optimization/pretraining | — | 完成摄入，应用未测；频率分段与温度扩窗，PPL/passkey证据和版本边界 |
| S044 | [[wiki/papers/optimization/pretraining/ProLong\|ProLong]] | optimization/pretraining | — | 完成摄入，应用未测；SFT后长任务评测、长短数据混合与训练长度条件 |
| S045 | [[wiki/papers/optimization/pretraining/Qwen2-VL\|Qwen2-VL]] | optimization/pretraining | — | 完成摄入，应用未测；动态视觉token、M-RoPE与Qwen-Agent多轮系统证据 |
| S046 | [[wiki/papers/optimization/pretraining/DoReMi\|DoReMi]] | optimization/pretraining | — | 完成摄入，应用未测；小模型excess loss优化域采样，跨尺度迁移和预算口径 |

### optimization/finetuning · 微调

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S012 | [[wiki/papers/optimization/finetuning/Toolformer\|Toolformer]] | optimization/finetuning | harness/tools | 完成摄入，应用未测；调用选择的数据筛选、参数学习与单次调用证据边界 |
| S047 | [[wiki/papers/optimization/finetuning/AgentTuning\|AgentTuning]] | optimization/finetuning | — | 完成摄入，应用未测；固定教师轨迹与通用对话混合、能力保留与分布边界 |
| S048 | [[wiki/papers/optimization/finetuning/ATLAS\|ATLAS]] | optimization/finetuning | — | 完成摄入，应用未测；完整历史上的关键步骤监督、语义选择与成本条件 |
| S049 | [[wiki/papers/optimization/finetuning/Agent-Distillation\|Agent-Distillation]] | optimization/finetuning | harness/tools | 完成摄入，应用未测；教师前缀、离线工具蒸馏与测试时动作筛选 |
| S050 | [[wiki/papers/optimization/finetuning/Agent-R\|Agent-R]] | optimization/finetuning | optimization/self-evolution | 完成摄入，应用未测；迭代SFT及采树重放、训练拼接、在线恢复三阶段的代码证据与边界 |
| S073 | [[wiki/papers/optimization/finetuning/UI-TARS\|UI-TARS]] | optimization/finetuning | optimization/data-environments | GUI训练与恢复；固定步数SFT/DPO对照及评价协议限制；未复现、应用未测。 |
| S079 | [[wiki/papers/optimization/finetuning/Reasoning-SFT-Generalization\|Reasoning-SFT-Generalization]] | optimization/finetuning | optimization/reinforcement-learning | 完成摄入，应用未测；SFT泛化的优化／数据／底座条件，保留教师信息与总预算边界。 |

### optimization/reinforcement-learning · Agentic Reinforcement Learning

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S041 | [[wiki/papers/optimization/reinforcement-learning/AgentGym-RL\|AgentGym-RL]] | optimization/reinforcement-learning | optimization/data-environments, optimization/finetuning | 完成摄入，应用未测；在线 RL 的交互课程、环境重置与训练状态分布 |
| S051 | [[wiki/papers/optimization/reinforcement-learning/Search-R1\|Search-R1]] | optimization/reinforcement-learning | — | 完成摄入，应用未测；在线搜索状态、终局EM与检索token损失屏蔽 |
| S052 | [[wiki/papers/optimization/reinforcement-learning/ToolRL\|ToolRL]] | optimization/reinforcement-learning | — | 完成摄入，应用未测；标准调用的细粒度奖励与带历史单步训练边界 |
| S053 | [[wiki/papers/optimization/reinforcement-learning/GiGPO\|GiGPO]] | optimization/reinforcement-learning | — | 完成摄入，应用未测；两级优势及分组anchor、策略输入、自包含均值的官方代码证据与版本边界 |
| S054 | [[wiki/papers/optimization/reinforcement-learning/Tree-GRPO\|Tree-GRPO]] | optimization/reinforcement-learning | — | 完成摄入，应用未测；共享前缀采样、树内/跨树优势和预算归因 |
| S055 | [[wiki/papers/optimization/reinforcement-learning/Memory-R1\|Memory-R1]] | optimization/reinforcement-learning | harness/memory | 完成摄入，应用未测；分阶段记忆操作/使用学习、回答器依赖与oracle测试边界 |
| S068 | [[wiki/papers/optimization/reinforcement-learning/C3\|C3]] | optimization/reinforcement-learning | — | 综述外补读，完成摄入；trace状态恢复、执行反事实信用和预算可靠性；应用未测 |
| S074 | [[wiki/papers/optimization/reinforcement-learning/WebThinker\|WebThinker]] | optimization/reinforcement-learning | harness/tools, harness/orchestration | 深度浏览、报告状态与在线DPO；区分流程收益和引用可靠性；未复现、应用未测。 |
| S077 | [[wiki/papers/optimization/reinforcement-learning/DeepSeek-R1\|DeepSeek-R1]] | optimization/reinforcement-learning | optimization/finetuning | 完成摄入，应用未测；推理RL与多阶段SFT／蒸馏配方，区分交互条件和能力归因。 |
| S078 | [[wiki/papers/optimization/reinforcement-learning/RL-Reasoning-Capacity\|RL-Reasoning-Capacity]] | optimization/reinforcement-learning | optimization/finetuning | 完成摄入，应用未测；有限采样覆盖与成功概率，避免把经验边界写成普遍不可能性。 |

### optimization/distillation · On-Policy Distillation

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S056 | [[wiki/papers/optimization/distillation/GKD\|GKD]] | optimization/distillation | — | 完成摄入，应用未测；学生前缀上的教师概率监督、散度与文本任务边界 |
| S057 | [[wiki/papers/optimization/distillation/DAgger-LLM\|DAgger-LLM]] | optimization/distillation | — | 完成摄入，应用未测；混合环境执行与教师动作标签、教师执行概率和评测分母 |
| S058 | [[wiki/papers/optimization/distillation/MAD-OPD\|MAD-OPD]] | optimization/distillation | — | 完成摄入，应用未测；讨论条件化教师分布、任务消融与理论适用前提核查 |
| S059 | [[wiki/papers/optimization/distillation/Pi-Play\|Pi-Play]] | optimization/distillation | optimization/self-evolution | 完成摄入，应用未测；QCP特权蒸馏、GRPO及出题课程共同更新 |
| S060 | [[wiki/papers/optimization/distillation/Self-Distillation-Zero\|Self-Distillation-Zero]] | optimization/distillation | — | 完成摄入，应用未测；SRT修订者到首次生成的蒸馏、阶段贡献与预算口径 |

### optimization/self-evolution · 自我演化

| ID | 唯一来源页 | 主归属 | 交叉方向 | 摘要与状态 |
| --- | --- | --- | --- | --- |
| S061 | [[wiki/papers/optimization/self-evolution/STaR\|STaR]] | optimization/self-evolution | — | 完成摄入，应用未测；固定答案锚点与推理自举、每轮重初始化和dev/test边界 |
| S062 | [[wiki/papers/optimization/self-evolution/rStar-Math\|rStar-Math]] | optimization/self-evolution | — | 完成摄入，应用未测；策略/PPM与搜索共同更新、启动模型及标签来源 |
| S063 | [[wiki/papers/optimization/self-evolution/R-Zero\|R-Zero]] | optimization/self-evolution | — | 完成摄入，应用未测；可学习任务分布、多数票伪标签与迭代失稳 |
| S064 | [[wiki/papers/optimization/self-evolution/Agent0\|Agent0]] | optimization/self-evolution | — | 完成摄入，应用未测；代码反馈、课程奖励、ADPO与有限轮次边界 |
| S065 | [[wiki/papers/optimization/self-evolution/Environment-Tuning\|Environment-Tuning]] | optimization/self-evolution | — | 完成摄入，应用未测；人工课程、教学反馈、奖励真值和撤除条件 |
| S069 | [[wiki/papers/optimization/self-evolution/R-Quest\|R-Quest]] | optimization/self-evolution | — | 综述外补读，完成摄入；坏题/重复诊断、外部初始化与回放锚点；应用未测 |
| S081 | [[wiki/papers/optimization/self-evolution/RRSI\|RRSI]] | optimization/self-evolution | harness/workflows, harness/verification | 完成摄入；固定权重的harness搜索、提案／准入正则与跨套件迁移；未复现、应用未测。 |

## 主题综合目录

| 页面 | 内容 |
| --- | --- |
| [[wiki/applications/success-mechanisms\|已有应用为何有效]] | 六篇原文的机制对照、条件性瓶颈及主动验证与内化边界；与Application组会记录互链。 |
| [[wiki/applications/terminal-bench-comparison\|Terminal-Bench的反证导向比较]] | 五篇前作、八项主张：真实执行不是独占，技术任务覆盖有增量，质量与经济外推需另证。 |
| [[wiki/harness/workflows\|循环与工作流]] | 三类工作流的定义与组合；反馈时点、分支恢复，以及任务内调整与跨轮harness修改的区别。 |
| [[wiki/harness/memory\|上下文与记忆]] | 工作上下文与持久记忆的循环、操作与内容分类；原论文的保存、准入、取回和使用边界。 |
| [[wiki/harness/tools\|工具、MCP 与技能]] | Tool、函数调用、MCP、工具发现与 skill 的定义和关系图解；原论文中的组合、复用与任务验收。 |
| [[wiki/harness/orchestration\|编排]] | 控制结构外化、四类设计问题与可选优化路线；分工、交接及选择性修复的原论文比较。 |
| [[wiki/harness/hooks\|Hooks 与中间件]] | 判断与执行控制的协作图、政策准备与运行期对照；三类方案及执行权与误拒边界。 |
| [[wiki/harness/verification\|验证]] | 证据、评价与用途的关系；终态验收、轨迹诊断与纠错净收益，以及任务验证与系统修改准入的区别。 |
| [[wiki/harness/connections\|Harness 跨模块联系与阶段性理解]] | 基于综述第 4 章的组会图解成果：共享记录何时成为依据、封装动作由何处约束、主动验收如何区分介入前后结果；未查新或实验。 |
| [[wiki/optimization/architecture\|架构基础]] | 显式、压缩与混合的分层图解；MLA 的压缩对象，以及生成、缓存和算子效率的区别。 |
| [[wiki/optimization/data-environments\|数据与环境合成]] | 任务—环境—轨迹的关系图解；课程、环境类型与轨迹加工维度，以及执行、标签和筛选分布的边界。 |
| [[wiki/optimization/pretraining\|预训练与中期训练]] | 训练阶段、三类基础能力与数据策略的层次图解；原论文机制和代理指标的边界。 |
| [[wiki/optimization/finetuning\|微调]] | SFT的行为塑造与冷启动；数据／课程／蒸馏配合、条件化泛化及与RL／OPD的分工。 |
| [[wiki/optimization/reinforcement-learning\|Agentic Reinforcement Learning]] | RL训练闭环与四个设计维度；推理RL／Agentic RL交互条件、能力测量及原论文归因边界。 |
| [[wiki/optimization/distillation\|On-Policy Distillation]] | 学生轨迹上的监督回路、两类监督路线与训练阶段关系；原论文的状态覆盖和教师权限。 |
| [[wiki/optimization/self-evolution\|自我演化]] | 经验回写的外层循环；训练式演化与固定权重harness搜索的区别，真值锚点与迁移约束。 |
| [[wiki/harness/Questions\|harness问题与关闭依据]] | 两轮讨论后保留的材料问题、反对证据与关闭理由。 |
| [[wiki/optimization/Questions\|Optimization问题与讨论]] | 本次3个RL问题＋6个宏观问题；另保留第一轮材料问题、反证与关闭依据。 |

## 维护入口

- [[maintenance/research/R001|R001研究维护记录]]：范围、选读理由、讨论协议与Git版本。
- [[maintenance/research/2026-10-29-terminal-bench-review|Terminal-Bench比较维护记录]]：五篇原文分工、主张范围、证据复核与本轮验收。
- [[maintenance/migrations/2026-10-25-directory-migration|目录迁移记录]]：旧新路径、附件精简、哈希与验收。

- [[wiki/log|操作日志]]：按时间记录来源摄入、查询沉淀、规则调整与健康检查。
- [[AGENTS|长期规则]]：三层边界、证据层级、论文唯一性和结构演化条件。
- [[workflows/ingest|Ingest]] · [[workflows/query|Query]] · [[workflows/lint|Lint]] · [[workflows/presentation|阅读表达]]：可逐步执行、随实践迭代的维护清单。
- [[workflows/autoresearch|Auto Research]]：按方向选文、每篇由同模型 subagent 摄入、共享写入、预算与停止条件；包含 Harness / Optimization 的启动和分工方案。
- [[workflows/brainstorm|Brainstorm]]：共同证据上的独立分析、互评、查新反证与候选问题状态。

**本轮状态（2026-10-25）：**R001文献研究完成，应用验收未完成；Harness 6类、Optimization 7类各5个核心名额，去重64篇，另补读5篇。论文由同模型subagent分批读取、整合和收尾，最多3个子任务并行；主Agent调度、交付验收、跨模块综合与本地Git检查点。六份独立首稿后交换，六个角色完成最后第二轮，未另开第三轮。范围及各批提交见[[maintenance/research/R001#范围与检查点|第一轮自主研究]]；未实验、未训练、未推送远程，本轮停止。

新论文来了先整合已有页面；新问题形成独立内容时再拆页。自主研究在选定范围内引导后续阅读，不代替用户确定最终研究方向。[[wiki/frontier/Overview#本库的待检验问题|现有问题]] 仍是探索记录，是否追踪取决于后续选文与证据。
