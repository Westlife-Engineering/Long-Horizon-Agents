# Long-Horizon Agents 知识库

这里积累关于长程 Agent 的定义、机制、证据和研究问题。当前处于**建立地图与文献驱动的 idea 探索阶段，未选定具体研究问题**。

## 当前证据边界

- 已纳入 **55 篇学术来源**：S001 综述及 S002–S055 五十四篇独立论文。S001 整体为地图式阅读，Foundation（§2，PDF pp.7–15）已补充问题驱动精读；独立论文的实际正文/附录阅读范围见各论文页，均不表示复现实验。
- **独立论文（含方法、系统、评测与分析）完成摄入数为 54**。综述中的引用不是本库已验证的证据；第一轮已选定 65 个方向名额、64 篇不同候选，正在分批核读，候选与待验收论文不计完成摄入。
- 方法论原始资料为 [[raw/articles/llm-wiki|LLM Wiki]]，不计入学术来源数。具体工作规则见 [[AGENTS|Schema]]。

## 从哪里开始

[[wiki/overview|领域总览]]：用系统耦合、任务层级与证据边界理解整张地图，再选择问题深入。

## Foundation：从图解笔记开始

**[[wiki/foundations/Formalization|定义、运行循环与理解辨析]]** 是默认阅读入口。流程图放在运行机制旁，反馈与成功的辨析接在循环之后，纠错恢复与时间代理接在任务分层之后；详细推导和依据按需展开。

已有具体困惑时，可以用 [[wiki/foundations/Formalization#从这套基础定义还能多理解什么|问题导航]] 直接进入。其他主题在后续阅读和更新时按内容需要逐步改善展示。

## 六个初始视角

六个视角沿用 S001 的组织方式（[[raw/papers/Towards Long-Horizon Agents.pdf#page=6|§1 · p.6]]），是导航起点，不是永久分类。

| 视角 | 页面 | 这里回答什么 |
| --- | --- | --- |
| Foundation | [[wiki/foundations/Formalization\|定义、运行循环与理解辨析]] | 从状态—观察—上下文理解 Agent 循环，串起任务依赖、H1–H3、记忆与自我演化，并区分定义、推断和评测代理。 |
| Evolution | [[wiki/foundations/Evolution\|从 Prompt 到 Runtime]] | 控制对象怎样从单次提示扩展到完整执行轨迹？ |
| Harness | [[wiki/harness/Overview\|外部运行机制]] | 循环、状态、工具、编排、拦截和验证分别负责什么？ |
| Optimization | [[wiki/optimization/Overview\|能力内化与训练]] | 架构、数据、训练和经验更新怎样组织成能力发展路线？ |
| Application | [[wiki/applications/Overview\|应用与评测]] | 不同环境接口提供什么反馈，评测如何归因？ |
| Frontier | [[wiki/frontier/Overview\|前沿与待检验问题]] | 作者提出哪些开放方向？本库还有哪些证据与概念缺口？ |

Harness 与 Optimization 的子方向都保留在各自 Overview 的页内导航中；当前没有空白细分页面。

## 学术来源目录

| 来源 | 唯一来源页 | 状态与用途 |
| --- | --- | --- |
| S001 | [[wiki/papers/Towards Long-Horizon Agents\|Towards Long-Horizon Agents: A Survey]] | 地图来源与阅读记录；已补充 Foundation 问题驱动精读及证据落点 |
| S002 | [[wiki/papers/ReAct\|ReAct]] | 完成摄入，应用未测；思考与环境观察的区别、交互历史和提示敏感性 |
| S003 | [[wiki/papers/ReWOO\|ReWOO]] | 完成摄入，应用未测；预定计划结构、证据变量与未知环境的适用边界 |
| S004 | [[wiki/papers/Arbor\|Arbor]] | 完成摄入，应用未测；假设树、实验事实与解释、版本隔离及评测准入边界 |
| S005 | [[wiki/papers/Tree-of-Thoughts\|Tree of Thoughts]] | 完成摄入，应用未测；部分解搜索、模型误剪和最终输出选择 |
| S006 | [[wiki/papers/LATS\|LATS]] | 完成摄入，应用未测；环境反馈、MCTS与反思，以及可回退性和oracle条件 |
| S007 | [[wiki/papers/HiAgent\|HiAgent]] | 完成摄入，应用未测；子目标工作记忆、摘要与轨迹取回 |
| S008 | [[wiki/papers/MemGPT\|MemGPT]] | 完成摄入，应用未测；分层存储、函数读写与控制流接续 |
| S009 | [[wiki/papers/A-MEM\|A-MEM]] | 完成摄入，应用未测；notes 关联/演化与长对话问答证据 |
| S010 | [[wiki/papers/ExpeL\|ExpeL]] | 完成摄入，应用未测；跨任务经验规则与成功轨迹检索 |
| S011 | [[wiki/papers/ReSum\|ReSum]] | 完成摄入，应用未测；摘要接续与策略适应训练的接口和归因边界 |
| S012 | [[wiki/papers/Toolformer\|Toolformer]] | 完成摄入，应用未测；调用选择的数据筛选、参数学习与单次调用证据边界 |
| S013 | [[wiki/papers/AnyTool\|AnyTool]] | 完成摄入，应用未测；分层工具发现、失败驱动候选池更新与评价口径 |
| S014 | [[wiki/papers/CodeAct\|CodeAct]] | 完成摄入，应用未测；可组合代码动作、执行反馈与配套微调的区分 |
| S015 | [[wiki/papers/Voyager\|Voyager]] | 完成摄入，应用未测；程序性技能获取与跨任务复用，以及环境和成功判定条件 |
| S016 | [[wiki/papers/MCPMark\|MCPMark]] | 完成摄入，应用未测；有状态 MCP 任务、程序验收与重复运行可靠性 |
| S017 | [[wiki/papers/MetaGPT\|MetaGPT]] | 完成摄入，应用未测；固定角色、结构化产物与订阅依赖，保留反馈/角色消融边界 |
| S018 | [[wiki/papers/Magentic-One\|Magentic-One]] | 完成摄入，应用未测；双账本与停滞重规划，区分固定团队与动态调度 |
| S019 | [[wiki/papers/GPTSwarm\|GPTSwarm]] | 完成摄入，应用未测；可学习通信图与节点提示，分开优化和框架展示证据 |
| S020 | [[wiki/papers/TDAG\|TDAG]] | 完成摄入，应用未测；按结果调整子任务、定制执行者与文本技能可靠性 |
| S021 | [[wiki/papers/Multi-Agent-Failures\|Multi-Agent-Failures]] | 完成摄入，应用未测；失败模式分类、标注与干预，区分过程缺陷和因果归因 |
| S022 | [[wiki/papers/IsolateGPT\|IsolateGPT]] | 完成摄入，应用未测；跨应用执行/记忆隔离、权限交接与人工警告边界 |
| S023 | [[wiki/papers/AgentSpec\|AgentSpec]] | 完成摄入，应用未测；事件–谓词–处置 DSL、规则充分性与正常任务误拒 |
| S024 | [[wiki/papers/ShieldAgent\|ShieldAgent]] | 完成摄入，应用未测；政策规则电路与在线模型判断，修订全静态分类理解 |
| S025 | [[wiki/papers/InfrastructureSentinel\|InfrastructureSentinel]] | 完成摄入，应用未测；输入/计划/执行/审计四处治理与初步实验报告边界 |
| S026 | [[wiki/papers/AGrail\|AGrail]] | 完成摄入，应用未测；可演化检查清单、跨任务记忆与条件评测口径 |
| S027 | [[wiki/papers/CRITIC\|CRITIC]] | 已完成摄入；应用未测；工具反馈、critique、修订与停止，保留oracle和误改边界 |
| S028 | [[wiki/papers/AgentPRM-Xi\|AgentPRM-Xi]] | 已完成摄入；应用未测；promise/progress评分、搜索选择与末步PPO奖励粒度 |
| S029 | [[wiki/papers/Agent-as-a-Judge\|Agent-as-a-Judge]] | 已完成摄入；应用未测；按需求读取产物、人工一致性与尚未实测在线修复 |
| S030 | [[wiki/papers/CorrectBench\|CorrectBench]] | 已完成摄入；应用未测；纠错/误改双向指标、净收益和额外预算口径 |
| S031 | [[wiki/papers/Self-MAP\|Self-MAP]] | 已完成摄入；应用未测；跨轮指令、静态HTML快照和记忆rationale，TSR为Turn |
| S032 | [[wiki/papers/Longformer\|Longformer]] | 完成摄入，应用未测；显式 token 的局部/全局稀疏访问 |
| S033 | [[wiki/papers/Mamba\|Mamba]] | 完成摄入，应用未测；输入相关的有限递归状态与长度/吞吐证据边界 |
| S034 | [[wiki/papers/Kimi-Linear\|Kimi Linear]] | 完成摄入，应用未测；KDA/MLA 混合与训练版本、缓存和吞吐条件 |
| S035 | [[wiki/papers/GQA\|GQA]] | 完成摄入，应用未测；KV 头共享、解码成本与时间历史压缩的区别 |
| S036 | [[wiki/papers/Lost-in-the-Middle\|Lost in the Middle]] | 完成摄入，应用未测；位置稳健性、检索召回与上下文使用的区别 |
| S037 | [[wiki/papers/TaskCraft\|TaskCraft]] | 完成摄入，应用未测；依赖结构生成、增量语言核查与端到端执行的区别 |
| S038 | [[wiki/papers/SWE-Gym\|SWE-Gym]] | 完成摄入，应用未测；可执行仓库、测试标签、成功轨迹筛选与 verifier 重排 |
| S039 | [[wiki/papers/WebDreamer\|WebDreamer]] | 完成摄入，应用未测；真实交互监督的状态预测、执行前模拟与评分边界 |
| S040 | [[wiki/papers/TOUCAN\|TOUCAN]] | 完成摄入，应用未测；MCP 真实返回、合成用户/任务与质量筛选分布 |
| S041 | [[wiki/papers/AgentGym-RL\|AgentGym-RL]] | 完成摄入，应用未测；在线 RL 的交互课程、环境重置与训练状态分布 |

| S042 | [[wiki/papers/DeepSeek-V3\|DeepSeek-V3]] | 完成摄入，应用未测；组合配方、MTP与扩窗，以及后训练工程结果的归因层次 |
| S043 | [[wiki/papers/YaRN\|YaRN]] | 完成摄入，应用未测；频率分段与温度扩窗，PPL/passkey证据和版本边界 |
| S044 | [[wiki/papers/ProLong\|ProLong]] | 完成摄入，应用未测；SFT后长任务评测、长短数据混合与训练长度条件 |
| S045 | [[wiki/papers/Qwen2-VL\|Qwen2-VL]] | 完成摄入，应用未测；动态视觉token、M-RoPE与Qwen-Agent多轮系统证据 |
| S046 | [[wiki/papers/DoReMi\|DoReMi]] | 完成摄入，应用未测；小模型excess loss优化域采样，跨尺度迁移和预算口径 |


| S047 | [[wiki/papers/AgentTuning\|AgentTuning]] | 完成摄入，应用未测；固定教师轨迹与通用对话混合、能力保留与分布边界 |
| S048 | [[wiki/papers/ATLAS\|ATLAS]] | 完成摄入，应用未测；完整历史上的关键步骤监督、语义选择与成本条件 |
| S049 | [[wiki/papers/Agent-Distillation\|Agent Distillation]] | 完成摄入，应用未测；教师前缀、离线工具蒸馏与测试时动作筛选 |
| S050 | [[wiki/papers/Agent-R\|Agent-R]] | 完成摄入，应用未测；当前actor再采样、修复SFT与环境状态一致性待核查 |

| S051 | [[wiki/papers/Search-R1\|Search-R1]] | 完成摄入，应用未测；在线搜索状态、终局EM与检索token损失屏蔽 |
| S052 | [[wiki/papers/ToolRL\|ToolRL]] | 完成摄入，应用未测；标准调用的细粒度奖励与带历史单步训练边界 |
| S053 | [[wiki/papers/GiGPO\|GiGPO]] | 完成摄入，应用未测；重复环境状态分组、折扣回报与两级优势 |
| S054 | [[wiki/papers/Tree-GRPO\|Tree-GRPO]] | 完成摄入，应用未测；共享前缀采样、树内/跨树优势和预算归因 |
| S055 | [[wiki/papers/Memory-R1\|Memory-R1]] | 完成摄入，应用未测；分阶段记忆操作/使用学习、回答器依赖与oracle测试边界 |

## 维护入口

- [[wiki/log|操作日志]]：按时间记录来源摄入、查询沉淀、规则调整与健康检查。
- [[AGENTS|长期规则]]：三层边界、证据层级、论文唯一性和结构演化条件。
- [[workflows/ingest|Ingest]] · [[workflows/query|Query]] · [[workflows/lint|Lint]] · [[workflows/presentation|阅读表达]]：可逐步执行、随实践迭代的维护清单。
- [[workflows/autoresearch|Auto Research]]：按方向选文、每篇由同模型 subagent 摄入、共享写入、预算与停止条件；包含 Harness / Optimization 的启动和分工方案。
- [[workflows/brainstorm|Brainstorm]]：共同证据上的独立分析、互评、查新反证与候选问题状态。

**本轮状态（2026-10-25）：**第一轮 Auto Research 已启动，覆盖 Harness 6 类与 Optimization 7 类一级子方向；选文初筛完成，原文核读、主题整合与验收正分批推进，本轮尚未结束。每方向核心选读约 5 篇，先全局去重，再由同模型 subagent 分批摄入；最多同时 3 个子任务，主 Agent 验收与提交 Git。进度和边界见 [[wiki/overview#第一轮自主研究|第一轮自主研究]]；候选不计已读。

新论文来了先整合已有页面；新问题形成独立内容时再拆页。自主研究在选定范围内引导后续阅读，不代替用户确定最终研究方向。[[wiki/frontier/Overview#本库的待检验问题|现有问题]] 仍是探索记录，是否追踪取决于后续选文与证据。
