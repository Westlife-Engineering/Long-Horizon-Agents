---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/ReAct.pdf]]"
  - "[[raw/papers/ReWOO.pdf]]"
  - "[[raw/papers/Arbor.pdf]]"
  - "[[raw/papers/Tree-of-Thoughts.pdf]]"
  - "[[raw/papers/LATS.pdf]]"
  - "[[raw/papers/HiAgent.pdf]]"
  - "[[raw/papers/MemGPT.pdf]]"
  - "[[raw/papers/A-MEM.pdf]]"
  - "[[raw/papers/ExpeL.pdf]]"
  - "[[raw/papers/ReSum.pdf]]"
  - "[[raw/papers/Lost-in-the-Middle.pdf]]"
  - "[[raw/papers/Toolformer.pdf]]"
  - "[[raw/papers/Toolformer-supplement.pdf]]"
  - "[[raw/papers/AnyTool.pdf]]"
  - "[[raw/papers/CodeAct.pdf]]"
  - "[[raw/papers/Voyager.pdf]]"
  - "[[raw/papers/MCPMark.pdf]]"
  - "[[raw/papers/SWE-Gym.pdf]]"
  - "[[raw/papers/WebDreamer.pdf]]"
  - "[[raw/papers/MetaGPT.pdf]]"
  - "[[raw/papers/Magentic-One.pdf]]"
  - "[[raw/papers/GPTSwarm.pdf]]"
  - "[[raw/papers/TDAG.pdf]]"
  - "[[raw/papers/Multi-Agent-Failures.pdf]]"
---

# Harness：外部运行机制

Harness 是围绕模型组织执行的机制：安排何时调用模型、带入什么状态、执行哪些工具、如何协调与检查。[[wiki/papers/Towards Long-Horizon Agents|S001]] 将它作为长程能力的外化路径，与 [[wiki/optimization/Overview|模型优化]] 共同分析。这里归纳分类与接口责任，尚不评价某个具体方法的优劣。[[raw/papers/Towards Long-Horizon Agents.pdf#page=20|S001 · §4 · p.20]]

## 页内导航

[[wiki/harness/Overview#循环与工作流|循环与工作流]] · [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] · [[wiki/harness/Overview#工具、MCP 与技能|工具、MCP 与技能]] · [[wiki/harness/Overview#编排|编排]] · [[wiki/harness/Overview#Hooks 与中间件|Hooks 与中间件]] · [[wiki/harness/Overview#验证|验证]]

## 循环与工作流

决定模型调用、行动、观察与状态更新如何接续。综述区分沿单条轨迹推进的线性流程、显式维护子目标的计划—执行流程，以及比较候选路径的分支流程。分类回答的是如何控制执行，不直接保证哪种结构效果更好。[[raw/papers/Towards Long-Horizon Agents.pdf#page=20|S001 · §4.1 · p.20]]

细分导航：Linear Workflows（§4.1.1）；Plan-Execute Workflows（§4.1.2）；Branching Workflows（§4.1.3）。第一轮 S002–S006 已完成摄入与本节整合，内容与结构已验收；Obsidian 应用未测。

### 状态保留什么，反馈何时改变后续决策

**本库比较轴：**工作流的区别不只在有没有计划或树，而在保存的状态、观察进入决策的时点，以及允许重试什么。下面比较机制，不把不同模型、任务、反馈权限和调用预算的分数排成优劣。

| 维持的状态 | 反馈怎样进入下一步 | 重选或恢复的边界 | 原文与唯一论文页 |
| --- | --- | --- | --- |
| 线性的 thought–action–observation 历史 | 外部动作返回观察后，可重新解释状态、调整后续动作；thought 本身只写回上下文 | 可以动态调整单条轨迹，没有自动保存所有替代分支或保证从错误中恢复 | [[wiki/papers/ReAct\|ReAct]]；[[raw/papers/ReAct.pdf#page=3\|S002 · §2 · pp.3–4]] |
| 预生成的计划结构与 `#E` 证据变量 | 工具结果填入变量，后续工具使用实际值，Solver 最后综合；基本流程不让观察重新设计整份计划 | 信息不足且需探索时，预期的证据可能不存在，计划结构也可能需要改变 | [[wiki/papers/ReWOO\|ReWOO]]；[[raw/papers/ReWOO.pdf#page=3\|S003 · §2.1 · pp.3–4]]、[[raw/papers/ReWOO.pdf#page=8\|§4 · pp.8–9]] |
| 假设、实验事实、解释与实现版本组成的研究树 | 每批 Executor 返回实验结果后，Coordinator 归纳认识、细化或剪枝，并选择候选材料 | Executor 固定假设、隔离实现；树边表示假设细化，当前最佳代码另有版本引用 | [[wiki/papers/Arbor\|Arbor]]；[[raw/papers/Arbor.pdf#page=6\|S004 · §4.2–4.3 · pp.6–8]] |
| 同一道题的多个部分解与搜索候选集合 | 模型为候选评分或投票，BFS/DFS 程序决定保留、继续、剪枝和回溯 | 文本部分解可复制回退；模型评价可能剪掉正确分支 | [[wiki/papers/Tree-of-Thoughts\|ToT]]；[[raw/papers/Tree-of-Thoughts.pdf#page=3\|S005 · §3 · pp.3–4]]、[[raw/papers/Tree-of-Thoughts.pdf#page=8\|§4.3 · p.8]] |
| 记录行动和观察的搜索树，以及失败轨迹与反思 | 先取得观察再评价状态；终局奖励作 MCTS 数值回传，失败反思以文本影响下一次尝试 | 需要可回退或重试的环境；观察、奖励、自评和反思的可靠性各不相同 | [[wiki/papers/LATS\|LATS]]；[[raw/papers/LATS.pdf#page=4\|S006 · §4 · pp.4–6]]、[[raw/papers/LATS.pdf#page=14\|Appendix B · p.14]] |

由此可以更具体地问“失败后怎样改”：ReAct 可改变下一动作；ReWOO 让已有结构接收实际变量值，但作者的未知位置例子说明结构本身未必可提前确定；Arbor 则在实验结束后修订下一批假设。**本库推断：**先判断新信息只是补齐参数，还是会改变应执行的操作，才有依据选择反馈时点。这个问题尚是比较框架，不是已查新的研究缺口。[[raw/papers/ReAct.pdf#page=3|S002 · §2 · pp.3–4]] [[raw/papers/ReWOO.pdf#page=8|S003 · §4 · pp.8–9]] [[raw/papers/Arbor.pdf#page=7|S004 · §4.3 · pp.7–8]]

### 分支能否撤回，评价能否被信任

ToT 回退的是保存在搜索程序中的部分解；LATS 将这种选择扩展到行动与观察，却明确要求环境可恢复。**本库推断：**重新放入旧历史不等于撤销外部副作用，真实交互若不能重置，就需要另行说明分支怎样评估与提交。ToT 的 24 点和填字实验不能独自支持现实长程任务的恢复能力；LATS 的受控环境也不能替代不可逆任务证据。[[raw/papers/Tree-of-Thoughts.pdf#page=4|S005 · §3–4 · pp.4–5]] [[raw/papers/LATS.pdf#page=14|S006 · Appendix B · p.14]]

**执行前模拟提供另一种分支方式（S039，已完成摄入，应用未测）：**[[wiki/papers/WebDreamer|WebDreamer]] 用世界模型预测候选动作后的页面变化、由 LLM 评分，只执行选中动作，再用真实新观察重新规划。它不需要为每个候选实际回退网站，但也不保证模拟正确或操作安全；主实验模拟 H=1，更深模拟反而受到不可用动作幻觉影响。Dreamer-7B 的训练对象是变化描述，score 仍由 GPT-4o 提供，详见 [[wiki/optimization/Overview#生成了什么，真实执行到了哪里|数据与环境]]。[[raw/papers/WebDreamer.pdf#page=4|S039 §3.2 · pp.4–5]] [[raw/papers/WebDreamer.pdf#page=8|§5.1 · p.8]]

评价信号同样要分开：ToT 的模型启发式会误剪罕见但正确的填字状态；LATS 的 HotpotQA 在提交答案后有 oracle 告知对错，编程则先用内部合成测试搜索、最后用真正测试集测量。相同的“反思”或“成功”标签，因此不意味着取得了同等质量的依据。对应 [[wiki/harness/Overview#验证|验证]] 中“何时检查、怎样产生判断”的区分。[[raw/papers/Tree-of-Thoughts.pdf#page=8|S005 · §4.3 · p.8]] [[raw/papers/LATS.pdf#page=6|S006 · §5.1–5.2 · pp.6–7]]

Arbor 还引入另一种风险边界：事实结果和归纳后的 insight 应分别保留，否则单次实现失败可能被提升成整个方向的负面约束。这是本库对其状态表示的分析，不是已测量的因果错误率。其 `E_test` 在合并准入与最终验证中的使用关系也仍需核查：循环算法包含准入测试，任务说明又强调保留最终验证；现有文字不足以确认完整的独立评估安排，不能据此断言实际运行发生泄漏。[[raw/papers/Arbor.pdf#page=6|S004 · §4.2 · p.6]] [[raw/papers/Arbor.pdf#page=7|Algorithm1 · p.7]] [[raw/papers/Arbor.pdf#page=23|Appendix A · p.23]] [[raw/papers/Arbor.pdf#page=34|Appendix C.4 · p.34]]

与 [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] 相连时，也须保留状态的存续范围：ToT / LATS 的搜索状态主要服务当前任务，Arbor 将同一研究任务的假设树落盘用于压缩后恢复；这不同于已经验证跨任务经验迁移。Arbor 的实验目标是给定材料与评测器下的优化，对本库文献探索的分工和证据组织只能提供机制类比，不能证明系统会自动提出新颖 idea。[[raw/papers/LATS.pdf#page=3|S006 · Table1注释、§4 · pp.3–6]] [[raw/papers/Arbor.pdf#page=23|S004 · Appendix A–B · pp.23–27]]

**后续比较条件：**固定反馈权限、可回退性和总资源口径后，再区分候选覆盖、状态评价、反思与输出选择各自的贡献。ReAct 的平均/最佳提示表现、ReWOO 的 Accuracy/EM、ToT 的系统输出/oracle 最佳状态、LATS 的属性平均分/严格成功率已在各论文页分开；当前不据这些异质分数决定研究方向。

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

细分导航：Tool Interfaces and Protocols；Active Tool Discovery；Skill Libraries。第一轮 S012–S016 已完成摄入与本节整合，内容与结构验收通过，Obsidian 应用未测；尚未独立核读 MCP 协议规范，不能用基准论文替代协议文档。

### 发现、表示、复用和验收改变的是不同对象

**本库比较轴：**工具存在以后，还需要决定何时调用、找出合适接口、组合依赖动作、复用过去程序，并确认外部任务完成。下面五项工作改变不同环节，不能按各自成功率排成同一榜单。

| 要解决的问题 | 实际改变的对象 | 运行与训练边界、原文 |
| --- | --- | --- |
| 何时调用已有工具，怎样填写参数？ | Toolformer 采样并执行候选调用，以后续 token 预测损失改善筛选数据，再微调模型；推理时暂停生成并插入工具结果 | 有参数训练；不是主动发现新工具。[[wiki/papers/Toolformer\|Toolformer]]；[[raw/papers/Toolformer.pdf#page=3\|S012 §2 · pp.3–4]] |
| 大工具库中漏检后怎样继续找？ | AnyTool 维护分类层级中的搜索历史、完成标记与全局 API 候选池，失败理由驱动逐层重启发现 | 运行时多 Agent / solver / 反思，无新增参数训练。[[wiki/papers/AnyTool\|AnyTool]]；[[raw/papers/AnyTool.pdf#page=5\|S013 §4 · pp.5–6]] |
| 一次动作能表达多少依赖操作？ | CodeAct 用 Python 变量、循环与分支组合工具，解释器结果或异常返回下一轮 | 动作表示可直接用于现成模型；CodeActAgent 的 SFT 是另一项变化。[[wiki/papers/CodeAct\|CodeAct]]；[[raw/papers/CodeAct.pdf#page=3\|S014 §2.1 · pp.3–4]] |
| 已做成的程序怎样用于以后任务？ | Voyager 把成功判定后的 JavaScript 程序及描述存入技能库，以描述检索程序，再生成、组合和修复代码 | 更新程序库与任务进度，GPT-4 参数不更新。[[wiki/papers/Voyager\|Voyager]]；[[raw/papers/Voyager.pdf#page=4\|S015 §2.2–2.3 · pp.4–6]] |
| 工具调用结束后，任务约束满足了吗？ | MCPMark 初始化环境、运行工具循环、程序检查最终状态，再重置进行重复测量 | 是评测与验收框架，不是训练方法。[[wiki/papers/MCPMark\|MCPMark]]；[[raw/papers/MCPMark.pdf#page=5\|S016 §2.3–3.1 · pp.5–6]] |

这也解释了工具与技能的区别：工具接口提供当前可调用能力；Voyager 的技能则是过去任务产生的可执行程序经验。它的检索描述帮助找程序，但检索正确与新状态中执行成功仍是两件事。与 [[wiki/harness/Overview#上下文与记忆|持久记忆]] 对接时，要记录保存的是事实、经验规则还是程序，以及它如何进入动作；不能仅凭“有技能库”推断环境前提仍成立。[[raw/papers/Voyager.pdf#page=4|S015 §2.2 · pp.4–5]] [[raw/papers/Voyager.pdf#page=42|B.4.4、Table A.4 · p.42]]

### 依赖怎样执行，失败以后改哪里

Toolformer 的训练调用独立生成，原文明确不能学习把一个工具输出交给下一个工具；评测每条输入最多一次调用。因此它支持“调用选择可被学到”，尚不支持长程多工具依赖已解决。AnyTool 则把失败反馈用于改变**可选工具集合**；CodeAct 把局部依赖写进**可执行动作**，再用结果修订后续代码。三者作用不同，也有不同资源开销。[[raw/papers/Toolformer.pdf#page=6|S012 §4 · p.6]] [[raw/papers/Toolformer.pdf#page=9|§6 · p.9]] [[raw/papers/AnyTool.pdf#page=6|S013 §4.3 · p.6]] [[raw/papers/CodeAct.pdf#page=3|S014 §2.1 · pp.3–4]]

比较执行效率时，必须先统一“一步”的单位：CodeAct 的 M³ToolEval 对照让 JSON / Text 每轮只调用一个工具，而代码一轮可调用多个，故轮数下降不能直接解释为底层调用减少。AnyTool 的反思消融没有匹配总调用成本；其全系统 token 预算还包括发现和反思，不能只拿 solver 的 API 次数代表总资源。[[raw/papers/CodeAct.pdf#page=17|S014 Appendix F.3–F.5 · p.17]] [[raw/papers/AnyTool.pdf#page=7|S013 §5.3 · pp.7–8]] [[raw/papers/AnyTool.pdf#page=12|Appendix A.1 · p.12]]

Voyager 更进一步跨任务保留程序：新世界测试清空物品，却保留技能库，因而是已有经验迁移；它依赖 Minecraft 结构化状态、Mineflayer 高层接口和复活保留物品等设置。主要探索最多 160 次 prompting iterations、三次运行中钻石级仅一次达到，不能把一次探索突破写成稳定或无限持续能力。[[raw/papers/Voyager.pdf#page=7|S015 §3.3、Tables 1–2 · pp.7–8]] [[raw/papers/Voyager.pdf#page=38|Appendix B.1 · p.38]]

### 协议接通与任务完成之间还差什么证据

AnyTool 使用 GPT-4 判断解答；Voyager 用 GPT-4 critic 决定任务成功和技能入库；MCPMark 则针对任务写程序检查环境状态。它们都称“成功”，但判断对象和误差来源不同。AnyTool 对旧 ToolBench 的检查还说明：若把候选 API 无法解决也计入 pass，检索失败可能使分数变好；统计分母本身也是证据的一部分。[[raw/papers/AnyTool.pdf#page=4|S013 §3.2 · p.4]] [[raw/papers/AnyTool.pdf#page=6|§5.1 · p.6]] [[raw/papers/Voyager.pdf#page=5|S015 §2.3 · pp.5–6]] [[raw/papers/MCPMark.pdf#page=5|S016 §2.3 · p.5]]

MCPMark 的 127 个任务、38 个初始状态覆盖五类服务；GitHub 案例检查配置、工作流、PR 与 CI 先失败后成功等联合约束，展示了“调用返回正常”和“任务完成”的距离。每次限 100 turns / 3600 秒；pass@1、四次至少成功一次的 pass@4、四次全成功的 pass^4 分别测量单次表现、重试覆盖和重复稳定性。统一 MCP 接口没有取消这些区别；程序 verifier 本身的规范覆盖也需核查。详见 [[wiki/harness/Overview#验证|验证]]。[[raw/papers/MCPMark.pdf#page=4|S016 §2.1–3.1 · pp.4–6]] [[raw/papers/MCPMark.pdf#page=27|Appendix E · pp.27–29]]

**待检验问题，尚未完成查新：**固定模型、初始状态、工具版本和总资源后，工具发现、代码组合与技能复用各减少了哪类未满足约束？一次被判成功的程序在何种条件下需要重新验证？现有五篇使问题更具体，尚不能据此宣布新的研究缺口；训练数据与参数的接口另见 [[wiki/optimization/Overview#微调|微调]]。

## 编排

编排把工作分配到多个执行循环：拆分任务和角色，决定协调拓扑，调整路由/协调策略，再通过协议交换消息与产物。这是工作组织问题；不能由“用了多个 Agent”直接推出能力提升。[[raw/papers/Towards Long-Horizon Agents.pdf#page=29|S001 · §4.4 · Fig.9 · p.29]]

细分导航：Decomposition and Roles；Coordination Topologies；Orchestration Optimization；Agent Protocols。第一轮 S017–S021 已完成摄入与本节整合，内容与结构验收通过；Obsidian 应用未测。这里比较运行机制和证据边界，不把不同任务的分数排成优劣。

### 谁负责分工，交接时保留什么

**本库比较轴：**团队成员是否固定、执行顺序是否固定、信息怎样流动，是三个不同问题。固定成员可以动态调度；生成新执行者也不意味着新的模型参数；通信图被学习也不等于每次行动都在重新规划。

| 分工与控制责任 | 共享或传递的状态 | 反馈后改变什么 | 直接证据 |
| --- | --- | --- | --- |
| MetaGPT：预定义专业角色按 SOP 协作 | PRD、架构/接口、任务列表、代码等进入共享 message pool，按角色订阅，依赖满足后行动 | 工程师依据执行测试和历史修复代码；主流程仍由既定 SOP 组织 | [[wiki/papers/MetaGPT\|S017 MetaGPT]]；[[raw/papers/MetaGPT.pdf#page=4\|§3、Fig.2 · pp.4–6]] |
| Magentic-One：Orchestrator 选择固定工具团队中的执行者 | Task Ledger 区分事实、待查/待推导信息、猜测和计划；Progress Ledger 保存完成/进展判断及下一指令 | 每步调整执行者与指令；停滞超过阈值后更新计划并重置 Agent 上下文 | [[wiki/papers/Magentic-One\|S018 Magentic-One]]；[[raw/papers/Magentic-One.pdf#page=5\|§4.1、Fig.2 · pp.5–7]] |
| TDAG：MainAgent 拆任务，Generator 定制当前执行者 | 子任务与前序结果进入执行；定制工具文档和检索到的文本技能提供上下文 | 前序结果更新后续子任务；成功判定后的经验总结更新技能库 | [[wiki/papers/TDAG\|S020 TDAG]]；[[raw/papers/TDAG.pdf#page=5\|§4、Algorithm1 · pp.5–7]] |
| GPTSwarm：Agent 是操作子图，团队是组合 DAG | 节点沿边接收前驱输出；节点历史可用于提示改进 | 用任务 utility 学习 Agent 间边分布，或优化节点提示；固定图执行按拓扑依赖进行 | [[wiki/papers/GPTSwarm\|S019 GPTSwarm]]；[[raw/papers/GPTSwarm.pdf#page=2\|§2、Algorithms1–3 · pp.2–4]] |

这组比较修正了“固定与动态”过粗的分类：Magentic-One 团队固定但路由与计划可变，TDAG 同时定制执行者上下文，GPTSwarm 则把通信边分布作为学习对象。上述主要改变发生在外部控制、提示与状态，不能仅因使用 REINFORCE 就归为基础 LLM 权重训练。[[raw/papers/Magentic-One.pdf#page=19|S018 §6.2 · p.19]] [[raw/papers/TDAG.pdf#page=6|S020 §4.2 · p.6]] [[raw/papers/GPTSwarm.pdf#page=4|S019 §§2.3–2.4 · p.4]]

与 [[wiki/harness/Overview#上下文与记忆|记忆]] 相接时，还要检查状态的有效期：Magentic-One 明确丢弃任务间经验；TDAG 保留文本技能，但作者承认环境不能保证技能正确。本库尚未确认 TDAG 测试遍历时技能库的初始化、重置与顺序，不能据“有库”直接推定独立任务上的迁移收益。**本库推断：**清除 Agent 上下文与撤销外部动作也不同，重规划后的状态一致性须另有证据。[[raw/papers/Magentic-One.pdf#page=6|S018 §4.1 · p.6]] [[raw/papers/Magentic-One.pdf#page=19|§6.2 · p.19]] [[raw/papers/TDAG.pdf#page=6|S020 §4.2 · pp.6–7]] [[raw/papers/TDAG.pdf#page=12|Appendix B · p.12]]

### 整体系统有效，是否知道哪项编排起了作用

四篇方法论文支持的作用范围不同，需要保留消融究竟移除了什么。

- **角色增加不等于纯数量效应。**MetaGPT 的角色消融仅对两项任务平均，增加角色时文档、调用与成本也改变。Magentic-One 删除专项 Agent 时同时减少工具能力；把完整协调者换成 GroupChat 又一次移除账本、规划、进展追踪、循环检测和明确指令。因此可以说这些组合在相应实验中有帮助，不能把收益单独归给 Agent 数量或某一本账本。[[raw/papers/MetaGPT.pdf#page=9|S017 §4.4、Table3 · p.9]] [[raw/papers/Magentic-One.pdf#page=12|S018 §5.3、Fig.3 · pp.12–14]]
- **框架展示不等于优化组件的证据。**GPTSwarm 的 GAIA 实验明确没有节点或边优化；TDAG 的 WebShop/TextCraft 实验明确不启用 Agent Generation。这些结果分别支持所测框架配置或动态拆解，不能挪用为拓扑学习、动态定制执行者的泛化证明。[[raw/papers/GPTSwarm.pdf#page=7|S019 §3.4 · pp.7–8]] [[raw/papers/TDAG.pdf#page=9|S020 §5.5 · p.9]]
- **成绩需要对应反馈与终局选择。**GPTSwarm 的填字优化/评估使用同20题，utility 是候选中的 best-state word accuracy；TDAG 的旅行主成绩是分层细粒度评分，非整任务成功率。额外优化、候选搜索和测试反馈的费用与权限必须保留，不能只比较最终一个分数。[[raw/papers/GPTSwarm.pdf#page=5|S019 §3.2 · pp.5–6]] [[raw/papers/GPTSwarm.pdf#page=25|Table11 · p.25]] [[raw/papers/TDAG.pdf#page=4|S020 §3.3 · pp.4–5]]

### 失败发生在设计、交接，还是验收

[[wiki/papers/Multi-Agent-Failures|S021 MAST]] 提供分析反面证据的分类工具：系统设计问题覆盖职责、历史和终止规则；Agent 间错位覆盖信息未传、未用、未澄清和偏离目标；任务验证覆盖过早终止、检查缺失和错误检查。其14类模式来自轨迹归纳，不是14种已隔离的因果机制；标注一致性也不等于根因已被完全识别。[[raw/papers/Multi-Agent-Failures.pdf#page=5|§3、Table2 · pp.5–6]] [[raw/papers/Multi-Agent-Failures.pdf#page=24|Appendix A · pp.24–25]]

**本库推断：**比较交接机制时，可沿“执行者是否掌握关键信息—是否传给协调者—协调者是否采用—最终结果是否被核查”追踪同一事实。MAST 的电话号码登录例子说明，有接口文档和消息通道仍可能漏传决定性约束。这支持细分检查责任，但作者关于 social reasoning 和目标训练的解释仍是观点，不能据单例确立唯一根因。[[raw/papers/Multi-Agent-Failures.pdf#page=6|S021 Fig.3 · p.6]] [[raw/papers/Multi-Agent-Failures.pdf#page=8|§4 FC2 · p.8]]

MAST 的干预案例进一步说明效果有条件：AG2 在不同模型上对拓扑改变的响应不同；ChatDev 的32项 ProgramDev-v0 测试改变验证/终止流程后，任务准确率得到改善，但不是全1642条数据上的统一提升。不同系统在不同任务的失败率不能互排；成功轨迹也会带有失败模式标签，因此标签减少与终局成功要分别检查。原文个别图文计数张力保留在唯一论文页，不据此否定任务结果。[[raw/papers/Multi-Agent-Failures.pdf#page=26|S021 Fig.5 · p.26]] [[raw/papers/Multi-Agent-Failures.pdf#page=33|Appendix H、Table5 · pp.33–35]] [[raw/papers/Multi-Agent-Failures.pdf#page=36|Appendix J.1 · p.36]]

**后续证据需求，尚非已成立研究缺口：**在匹配工具能力、反馈权限和总调用预算后，如何通过受控交接干预区分发送端遗漏、接收端忽略与状态截断？MAST 已为这些现象提供分类，不能只重新命名就称为创新；当前应先确定可操作的比较条件。

## Hooks 与中间件

Hooks 在运行流程的特定位置介入，让动作继续、阻止动作或交接控制。综述按规则来源与适应性分成预定义规则、用户定义策略、运行时自适应信号三类。Hooks 可以使用规则或模型判断，因此不应一概当成形式化安全保证。[[raw/papers/Towards Long-Horizon Agents.pdf#page=31|S001 · §4.5 · Fig.10 · p.31]]

细分导航：Pre-defined Rule-based Hooks；Custom User-defined Hooks；Runtime-adaptive Hooks。与 [[wiki/frontier/Overview|可信性前沿]] 相连。

## 验证

验证检查状态、行动、输出或副作用是否满足要求。综述按三条轴组织：**检查什么**（正确性、安全性、指令遵循、验证器一致性）、**何时检查**（步骤中、运行结束）、**怎样产生判断**（自动标签/隐式奖励、验证器引导搜索、验证计算分配）。拦截机制与判断机制可以协作，但不是同一个角色。[[raw/papers/Towards Long-Horizon Agents.pdf#page=34|S001 · §4.6–4.6.1 · p.34]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=36|§4.6.2–4.6.3 · pp.36–37]]

细分导航：Assessment Targets；Verification Levels；Verifier Strategies。与 [[wiki/optimization/Overview#Agentic Reinforcement Learning|训练中的信用分配]]、[[wiki/applications/Overview|评测的成功判据]] 相关；运行时检查有效，不自动证明它可作为可靠训练奖励。

**工具方向的直接证据（S016，已完成摄入，应用未测）：**MCPMark 把运行正常结束却未满足任务约束记为隐式失败；这说明缺少异常不能替代结果检查。其程序验收经过环境结果扰动和人工交叉检查，但本库未审查全部 verifier 源码，论文也未证明验证器完备。应把运行时模型 critic、工具异常与最终环境验收分别记录，具体机制与重复运行口径见 [[wiki/harness/Overview#协议接通与任务完成之间还差什么证据|工具方向比较]]。[[raw/papers/MCPMark.pdf#page=8|S016 §4.2、Fig.5 · pp.8–9]] [[raw/papers/MCPMark.pdf#page=15|Appendix A · pp.15–16]]

**可执行标签与学习验证器（S038，已完成摄入，应用未测）：**[[wiki/papers/SWE-Gym|SWE-Gym]] 用真实仓库测试产生轨迹成败标签，再训练 outcome verifier 在候选轨迹间预测和选择。OpenHands 的32B策略/32B验证器在 SWE-Bench Verified 上，16条候选的 Pass@16=42.8%，选出一条的 Best@16=32.0%；前者是覆盖上界，后者才包含选择误差。测试标签仍受测试覆盖约束，verifier又增加预测误差。与 MCPMark 的程序检查区别在于判断如何产生；数据来源、筛选与预算见 [[wiki/optimization/Overview#数据与环境合成|Optimization]]。[[raw/papers/SWE-Gym.pdf#page=4|S038 §3.1 · p.4]] [[raw/papers/SWE-Gym.pdf#page=7|§5.1.1、Fig.3 · p.7]]

**编排中的验证责任（S017–S021 已完成摄入，应用未测）：**MetaGPT 的执行测试反馈、Magentic-One 的“任务完成”自判，以及 MAST 对最终目标检查不足的观察，分别涉及测试、控制和诊断。验证动作存在不代表覆盖用户要求；MAST 也发现成功轨迹可含验证缺陷。具体角色与状态交接见 [[wiki/harness/Overview#失败发生在设计、交接，还是验收|编排诊断]]，不能把模型共识或无运行异常直接当作完成证据。[[raw/papers/MetaGPT.pdf#page=6|S017 §3.3 · p.6]] [[raw/papers/Magentic-One.pdf#page=7|S018 §4.1 · p.7]] [[raw/papers/Multi-Agent-Failures.pdf#page=8|S021 §4 FC3 · p.8]] [[raw/papers/Multi-Agent-Failures.pdf#page=36|Appendix J.1 · p.36]]

## 后续如何增长

当前六类都是有内容的导航段落，不对应六个空文件夹。新论文进入后，将它实际提供的机制、证据与限制写入相关段落，并链接唯一论文页；当内容需要独立比较时，再拆成如 `Context and Memory.md` 或 `Verification.md` 的页面。



## 第一轮选读队列

2026-10-25 按用户授权从 S001 引用选读。下表仅登记选择理由与来源 ID 预留，**候选并不代表已读**；论文页在正文核读后建立。相同 ID 在多个方向出现只计一个来源。状态以验收和本轮交付为准。


### 选读：循环与工作流

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S002 · [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=21\|S001 §§4.1.1 · p.21 · 引文761]] | 以观察—行动交替作为线性控制基线，后续用它区分响应式循环、显式计划与搜索的改变对象。 | 完成摄入；应用未测 |
| S003 · [ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models](https://arxiv.org/abs/2305.18323) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=21\|S001 §§4.1.2 · p.21 · 引文720]] | 选择推理与工具观察解耦的计划—执行路线，核查它在提前规划、依赖关系和工具失败上的适用前提。 | 完成摄入；应用未测 |
| S004 · [Toward Generalist Autonomous Research via Hypothesis-Tree Refinement](https://arxiv.org/abs/2606.11926) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=21\|S001 §§4.1.2 · p.21,22 · 引文262]] | 选择持久假设树与协调者—执行者循环，理解长期研究如何保存证据、分支和经验；不把其自主实验设置直接等同于本库文献找 idea。 | 完成摄入；应用未测 |
| S005 · [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://papers.nips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=22\|S001 §§4.1.3 · p.22 · 引文760]] | 作为分支搜索的基础机制，核查生成、评分、回溯与提交的控制责任，并保留静态推理任务到交互任务的外推边界。 | 完成摄入；应用未测 |
| S006 · [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](https://proceedings.mlr.press/v235/zhou24r.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=22\|S001 §§4.1.3；另见 §4.6.3 · p.22,37 · 引文875]] | 与 ToT 对照，追问树搜索怎样结合环境反馈、价值估计与反思，以及评估分支的成本和可回退性。 | 完成摄入；应用未测 |

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
| S012 · [Toolformer: Language Models Can Teach Themselves to Use Tools](https://papers.nips.cc/paper_files/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.1 · p.27 · 引文523]] | 提供工具调用能力如何被训练的基础参照，区分调用接口、调用选择和参数学习，避免把所有工具提升归因于外部 harness。 | [[wiki/papers/Toolformer\|完成摄入，应用未测]] |
| S013 · [AnyTool: Self-Reflective, Hierarchical Agents for Large-Scale API Calls](https://proceedings.mlr.press/v235/du24h.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.2 · p.27 · 引文140]] | 选择分层工具检索与失败后重新检索，对照固定工具列表；兼顾论文对工具评测协议的质疑。 | [[wiki/papers/AnyTool\|完成摄入，应用未测]] |
| S014 · [Executable Code Actions Elicit Better LLM Agents](https://proceedings.mlr.press/v235/wang24h.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.2 · p.27,28 · 引文656]] | 选择可执行代码作为行动空间，比较一次程序组合多个工具与逐个函数调用；分别核查行动表示和配套微调的收益。 | [[wiki/papers/CodeAct\|完成摄入，应用未测]] |
| S015 · [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=28\|S001 §§4.3.3；另见 §4.2.2 · p.28,25,26 · 引文630]] | 选择可执行技能库的获取、验证与复用，连接工具表面、持久经验与长程探索，并核查其 Minecraft 环境边界。 | [[wiki/papers/Voyager\|完成摄入，应用未测]] |
| S016 · [MCPMark: A Benchmark for Stress-Testing Realistic and Comprehensive MCP Use](https://arxiv.org/abs/2509.24002) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|S001 §§4.3.1 · p.27 · 引文700]] | 用包含状态改变与程序验收的多步 MCP 任务检查接口能力，防止仅凭单次工具调用成绩判断长期执行能力。 | [[wiki/papers/MCPMark\|完成摄入，应用未测]] |

### 选读：编排

| 来源 ID / 原始发布页 | 综述定位 | 选择理由 | 状态 |
| --- | --- | --- | --- |
| S017 · [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=29\|S001 §§4.4.1；§4.4.4 · p.29,30 · 引文219]] | 作为固定角色和标准流程的代表，与动态生成、中央协调和优化图比较，核查结构收益与角色提示收益如何分离。 | [[wiki/papers/MetaGPT\|完成摄入，应用未测]] |
| S018 · [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=30\|S001 §§4.4.2 · p.30 · 引文157]] | 选择中央协调者维护进展、重规划和恢复的通用任务系统，比较模块化执行与固定流水线。 | [[wiki/papers/Magentic-One\|完成摄入，应用未测]] |
| S019 · [GPTSwarm: Language Agents as Optimizable Graphs](https://proceedings.mlr.press/v235/zhuge24a.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=30\|S001 §§4.4.3 · p.30 · 引文897]] | 选择可优化的节点与连边表示，追问编排优化改变信息流还是基础模型，以及优化成本和泛化条件。 | [[wiki/papers/GPTSwarm\|完成摄入，应用未测]] |
| S020 · [TDAG: A Multi-Agent Framework based on Dynamic Task Decomposition and Agent Generation](https://arxiv.org/abs/2402.10178) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=29\|S001 §§4.4.1 · p.29 · 引文660]] | 选择动态任务拆解和临时 Agent 生成，对照固定角色组，核查粒度、上下文交接和级联失败。 | [[wiki/papers/TDAG\|完成摄入，应用未测]] |
| S021 · [Why Do Multi-Agent LLM Systems Fail?](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html) | [[raw/papers/Towards Long-Horizon Agents.pdf#page=29\|S001 §§4.4；§4.4.1 · p.29,30 · 引文48]] | 加入失败分析作为反证视角，核查角色不清、协调错位和验证缺失的证据，避免只收集系统成功故事。 | [[wiki/papers/Multi-Agent-Failures\|完成摄入，应用未测]] |

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
