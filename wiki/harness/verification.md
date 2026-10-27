---
type: topic
created: 2026-10-25
updated: 2026-10-27
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/harness/verification/CRITIC.pdf]]"
  - "[[raw/papers/harness/verification/AgentPRM-Xi.pdf]]"
  - "[[raw/papers/harness/verification/Agent-as-a-Judge.pdf]]"
  - "[[raw/papers/harness/tools/MCPMark.pdf]]"
  - "[[raw/papers/harness/verification/Self-MAP.pdf]]"
  - "[[raw/papers/harness/orchestration/MetaGPT.pdf]]"
  - "[[raw/papers/harness/orchestration/Magentic-One.pdf]]"
  - "[[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf]]"
  - "[[raw/papers/harness/memory/TRACE.pdf]]"
  - "[[raw/papers/harness/orchestration/BRIDGE.pdf]]"
  - "[[raw/papers/optimization/data-environments/SWE-Gym.pdf]]"
  - "[[raw/papers/harness/verification/CorrectBench.pdf]]"
  - "[[raw/papers/harness/verification/SpecRover.pdf]]"
---

# 验证

Agent 声称“任务完成了”，系统还需要证据判断动作是否合规、过程是否偏离、最终产物是否满足要求。Verification 承担这个评价职责；评价如何落实为执行约束，见 [[wiki/harness/hooks#与 Verification 的关系|Hooks 与 Verification 的协作图]]。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=34|S001 · §4.6 · p.34]]

## 验证怎样工作：证据、评价与用途

下面是**本库的机制阅读框架**，用于拆开一次验证中的不同责任；不是综述新增的分类，也不要求它们由三个模块顺序执行。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=34|S001 · §4.6 · p.34]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=36|§4.6.2–4.6.3 · pp.36–37]]

| 环节 | 要问的问题 | 为什么不能省略 |
| --- | --- | --- |
| **取得证据** | 依据是原文、工具返回、环境状态，还是模型采样？ | 工具返回提供信息，不自动证明模型正确理解了信息。 |
| **形成评价** | 用程序检查、模型判断，还是学习到的评分器？ | 判断或高分可能出错；先明确它评价的是哪项要求。 |
| **使用评价** | 交给 Hook 拦截，供搜索选择，触发修订，还是验收产物？ | 有反馈不等于已接入纠错；有局部检查不等于完成整项任务。 |

沿用知识库例子：检查笔记是否夸大结论，需要读取原文作为证据、比较表述与证据的适用范围，再把结论用于修订或验收。只确认文件位于可写目录，回答的是权限问题，不能替代这次内容验证。

### PRM 在评价环节中的位置

**PRM（Process Reward Model）为中间步骤产生质量估计；ORM（Outcome Reward Model）侧重最终结果。** PRM 可以是实际训练出的模型，“模型”与“函数”是实现与数学描述的关系：

$$
\underbrace{\hat r_t}_{\text{步骤质量估计}}
= f_\phi\!\left(\underbrace{\text{上下文},\text{候选步骤}}_{\text{评价输入}}\right)
$$

其中 $\phi$ 是模型参数；公式为本库教学抽象。**分数本身不执行动作**，由搜索或控制机制使用它来选择候选、引导修正等。步骤级验证也可调用工具、生成检查推理，不必都训练专用 PRM；高分仍不等于真实正确或任务完成。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=36|S001 · §4.6.2 · p.36]]

## 三个维度：目标、粒度与策略

| 维度 | 它改变或选择什么 |
| --- | --- |
| **Assessment Targets：检查什么** | Correctness 检查内容正确性；Safety 检查动作风险；Faithfulness 检查指令遵循与目标保持。综述还列出 Multi-agent Cross-verification，强调多个评估者交叉检查。 |
| **Verification Levels：在哪个粒度介入** | Step-level 检查中间推理或决策；End-of-run 检查最终产物或环境状态。二者可以单用或组合，不能仅凭时点判断采用了什么评估机制。 |
| **Verifier Strategies：怎样改进验证** | 自动标签／隐式奖励改变**评价信号的获取**；验证器引导搜索改变**评分参与探索和选择的方式**；计算分配改变**生成、搜索、判断之间的预算投入**。 |

来源：[[raw/surveys/Towards Long-Horizon Agents.pdf#page=34|S001 · §4.6.1 · pp.34–35]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=36|§4.6.2–4.6.3 · pp.36–37]]。**本库辨析：**交叉验证偏重评估者的组织方式，可用于正确性等目标；多评估者达成一致也不自动等于事实正确。以上维度用于描述和组合方案，不是三阶段流程。

> [!example] 把维度组合起来：检查论文总结是否夸大结论
> **目标**选正确性与指令忠实性；**粒度**选关键结论形成后，再在提交前整体检查；有多条候选解释时，**策略**可选择用验证评分引导后续搜索。
>
> 具体可读取原文后用模型评价，再据此选解释、要求修订或接受产物。“怎样实现判断”和“怎样使用评价”是本库补充的机制描述，不是综述另外两类方案；这只是教学配置，不要求每个任务都采用。

## Table 4：方法索引与训练范围

Table 4 按上述维度分组列举代表方法；读一行时，先看它被用来说明哪个方面，再看机制和训练前提。**Train-free 表示能用冻结模型开展该方法，不等于无模型或零开销。** [[raw/surveys/Towards Long-Horizon Agents.pdf#page=35|S001 · Table 4 · p.35]]

表中 Implicit PRM 标为非免训练，机制栏却写“无需额外训练”；正文补充其依赖已做结果训练的模型。因此“无需再训练过程模型”不能读成“整条路线无需训练”。这里仅核对综述表格与正文，不展开对应论文。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=35|S001 · Table 4 · p.35]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=36|§4.6.3 · p.36]]

后文分别核对局部检查、最终成功与纠错净收益；评价被用于 [[wiki/optimization/reinforcement-learning|训练奖励]] 时，还须确认标签是否可靠，不能仅因运行时有用就充当 [[wiki/applications/Overview|任务成功判据]]。

## 原论文中的判断与效果

本轮 S027–S031 已完成摄入；应用未测。下面按反馈来源、判断对象和判断之后的动作组织原论文证据，不把“验证”视为单一算法。

### 判断依赖什么证据，之后改变什么

| 反馈来源与判断对象 | 怎样形成判断 | 判断后的作用与边界 |
| --- | --- | --- |
| 搜索结果、解释器返回、毒性评分；检查当前答案/程序/文本 | CRITIC把工具返回加入模型critique | 重写答案并按规则停止；工具事实、模型解释与修订可分别出错。[[wiki/papers/harness/verification/CRITIC\|S027]]；[[raw/papers/harness/verification/CRITIC.pdf#page=4\|§3、Algorithm 1 · pp.4–5]] |
| 采样轨迹的环境终局回报；预测行动的promise/progress | AgentPRM用TD/GAE与相邻价值差训练评分模型 | BoN选完整轨迹或beam保留步骤；高分是预测，非无误的完成证明。[[wiki/papers/harness/verification/AgentPRM-Xi\|S028]]；[[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=5\|§3 · pp.5–8]] |
| 开发工作区、可选执行轨迹；检查每项需求 | Agent-as-a-Judge定位、读取产物，再由模型判定 | 输出需求评估；本文未实测把反馈接回执行者在线修复。[[wiki/papers/harness/verification/Agent-as-a-Judge\|S029]]；[[raw/papers/harness/verification/Agent-as-a-Judge.pdf#page=6\|§4.1 · pp.6–7]]、[[raw/papers/harness/verification/Agent-as-a-Judge.pdf#page=9\|§6 · p.9]] |

**工具方向的直接证据（S016，已完成摄入，应用未测）：**MCPMark 把运行正常结束却未满足任务约束记为隐式失败；这说明缺少异常不能替代结果检查。其程序验收经过环境结果扰动和人工交叉检查，但本库未审查全部 verifier 源码，论文也未证明验证器完备。应把运行时模型 critic、工具异常与最终环境验收分别记录，具体机制与重复运行口径见 [[wiki/harness/tools#协议接通与任务完成之间还差什么证据|工具方向比较]]。[[raw/papers/harness/tools/MCPMark.pdf#page=8|S016 §4.2、Fig.5 · pp.8–9]] [[raw/papers/harness/tools/MCPMark.pdf#page=15|Appendix A · pp.15–16]]

**Hooks 与验证的接口（S022–S026 已完成摄入，应用未测）：**权限警告、程序谓词、模型判断、形式模型内推断和事后审计具有不同证据含义；先确认判断如何产生、动作是否已经执行，再报告允许、阻止、误拒与漏过。具体条件见 [[wiki/harness/hooks#拦住了什么，正常任务还能做多少|Hooks 证据比较]]，不能用一次检查通过替代全任务完成或长期安全。

**本库综合：**先登记可访问的外部信息及标签，再判断模型从中推断了什么，最后记录系统选择、修改或拦截了什么。运行时取证、学习价值预测、程序验收可以互补，但各自的误差不会因模块更多而自动消失。判断可以在结束后评估要求，也可以在步骤间选候选；时间位置不能替代机制身份。

### 检查对象决定成功指标

Agent-as-a-Judge 的DevAI将需求组织成依赖图，独立需求达标、考虑前置条件的达标率、整任务成功分别计分；与人工共识的Alignment Rate又是**评估者**的指标。负例较多时一致率可能偏高，作者因此另用PR曲线。取证准确不等于被评估Agent已完成任务，人工共识也不是绝对真值。[[raw/papers/harness/verification/Agent-as-a-Judge.pdf#page=3|S029 §2.2 · p.3]] [[raw/papers/harness/verification/Agent-as-a-Judge.pdf#page=5|Table 2、§3 · pp.5–6]] [[raw/papers/harness/verification/Agent-as-a-Judge.pdf#page=8|§4.2、Fig.6 · p.8]]

跨轮指令进一步改变评价单位。[[wiki/papers/harness/verification/Self-MAP|S031 MT-Mind2Web/Self-MAP]] 的SSR要求元素与操作同时正确，TSR要求**一轮用户指令内**所有步骤正确；TSR不是整个对话的完成率。它主要贡献离线多轮指令任务和记忆增强规划，不能因被S001归入验证选读就写成独立verifier。静态HTML快照没有实证错误行动改变状态后的恢复；记忆机制见 [[wiki/harness/memory|上下文与记忆]]。[[raw/papers/harness/verification/Self-MAP.pdf#page=6|§5.1 · PDF p.6 / 印刷8800]] [[raw/papers/harness/verification/Self-MAP.pdf#page=9|Limitation · PDF p.9 / 印刷8803]]

**编排中的验证责任（S017–S021 已完成摄入，应用未测）：**MetaGPT 的执行测试反馈、Magentic-One 的“任务完成”自判，以及 MAST 对最终目标检查不足的观察，分别涉及测试、控制和诊断。验证动作存在不代表覆盖用户要求；MAST 也发现成功轨迹可含验证缺陷。具体角色与状态交接见 [[wiki/harness/orchestration#失败发生在设计、交接，还是验收|编排诊断]]，不能把模型共识或无运行异常直接当作完成证据。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=6|S017 §3.3 · p.6]] [[raw/papers/harness/orchestration/Magentic-One.pdf#page=7|S018 §4.1 · p.7]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=8|S021 §4 FC3 · p.8]] [[raw/papers/harness/orchestration/Multi-Agent-Failures.pdf#page=36|Appendix J.1 · p.36]]

### 选择误差与纠错净收益要分别测量

记忆与交接中的检查也有不同终点：[[wiki/harness/memory#来源真实、当前准入与后续使用是三个条件|TRACE的来源绑定与准入]]控制可见证据；[[wiki/harness/orchestration#从故障分类到选择性交接修复|BRIDGE的局部后置条件]]控制修复消息提交。两篇都给出前一阶段通过、后一阶段仍失败的实例，因此需保留准入/局部检查与最终使用/任务验收两套观察，不能把前者代作后者的标签。[[raw/papers/harness/memory/TRACE.pdf#page=24|S066 C.8 · p.24]] [[raw/papers/harness/orchestration/BRIDGE.pdf#page=18|S067 Appendix E、Table13 · p.18]]

**可执行标签与学习验证器（S038，已完成摄入，应用未测）：**[[wiki/papers/optimization/data-environments/SWE-Gym|SWE-Gym]] 用真实仓库测试产生轨迹成败标签，再训练 outcome verifier 在候选轨迹间预测和选择。OpenHands 的32B策略/32B验证器在 SWE-Bench Verified 上，16条候选的 Pass@16=42.8%，选出一条的 Best@16=32.0%；前者是覆盖上界，后者才包含选择误差。测试标签仍受测试覆盖约束，verifier又增加预测误差。与 MCPMark 的程序检查区别在于判断如何产生；数据来源、筛选与预算见 [[wiki/optimization/data-environments|Optimization]]。[[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=4|S038 §3.1 · p.4]] [[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=7|§5.1.1、Fig.3 · p.7]]

AgentPRM增加步骤间价值差约束，但**奖励模型训练粒度、搜索选择粒度与RL奖励粒度不同**。其BoN按末步分数选轨迹，beam按步骤保留分支；PPO实验仍以末步PRM预测作整轨迹奖励，详见 [[wiki/optimization/reinforcement-learning#过程评分怎样进入策略更新|策略更新接口]]。WebShop/TextCraft报成功率而BabyAI报reward，候选数、搜索展开和训练标签采样成本也要分别记账；本文的计算效率不能直接当墙钟加速。[[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=4|S028 §2 · p.4]] [[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=9|§4.1 · pp.9–10]] [[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=22|Appendix C · p.22]]

纠错则要比较同一答案修改前后的双向变化。CRITIC的非oracle分析既发现错误修复，也发现正确答案被误改；星号CRITIC只修正已知错误初答，不能当作部署时拥有的检测能力。[[wiki/papers/harness/verification/CorrectBench|S030 CorrectBench]] 用Correction Rate（初始错误中改对的比例）和Misjudgment Rate（初始正确中误改的比例）把这两侧明确分开。[[raw/papers/harness/verification/CRITIC.pdf#page=5|S027 §4 · p.5]] [[raw/papers/harness/verification/CRITIC.pdf#page=26|Appendix D.2.2、Table 7 · p.26]] [[raw/papers/harness/verification/CorrectBench.pdf#page=8|S030 §4.6、Table 3 · p.8]]

**本库推导：**在同一批样本、相同正确性判据下，若初始准确率为$p$，则$p_{after}=p+(1-p)CR-pMR$。因此只在错误样本上测改对率，不能说明部署后的净收益；停止或追加检查还需算入误改与额外成本。该式是条件分母的算术关系，不是新实验。CorrectBench的样本/表述口径差异保留在唯一页，本库不从中提取统一提升量，也不把作者建议的动态controller写成已验证方法。[[raw/papers/harness/verification/CorrectBench.pdf#page=8|§4.6–4.7 · pp.8–9]] [[raw/papers/harness/verification/CorrectBench.pdf#page=10|§6 · p.10]]

**后续证据需求，尚非已成立研究缺口：**固定反馈权限、原本正确样本比例、可回退性和总预算后，判断新增取证改善的是漏检、选择还是修订；随后再测副作用与完整任务。当前已有工作已覆盖工具增强critique、学习评分与按需求取证，不能仅靠增加反思轮数、评分节点或Agent人数提出创新主张。

### 修复时，测试也可能需要重新核对

[[wiki/papers/harness/verification/SpecRover|S070 SpecRover，完成摄入]]将上述验证问题放进实际仓库修复循环：从issue与代码推断函数应有行为，生成补丁和复现测试；reviewer结合修改前后的执行结果，**分别判断补丁与测试**；既有回归测试失败后可以重试，多次尝试后还可按issue意图选择候选。因此“修复时保留旧功能、回归失败再修订”已有直接机制覆盖。[[raw/papers/harness/verification/SpecRover.pdf#page=3|S070 §III.A–D、Fig.2 · pp.3–5]]

| 看到的失败或通过 | 还必须区分什么 |
| --- | --- |
| 生成的复现测试失败 | 可能是补丁未修好，也可能是测试写错；SymPy案例中，测试错误地比较对象与字符串，reviewer认可补丁而否定测试。[[raw/papers/harness/verification/SpecRover.pdf#page=9\|S070 Fig.8 · pp.9–10]] |
| 既有回归测试失败 | 可能破坏旧功能，也可能新需求合法改变函数签名，使旧测试过时；selection依据最新issue判断，但仍可能误判。[[raw/papers/harness/verification/SpecRover.pdf#page=5\|S070 §III.D · p.5]] |
| 最终验收测试通过 | 仍受测试覆盖限制；作者在Lite的93个测试通过补丁中，仅将56个判断为与开发者补丁语义等价。[[raw/papers/harness/verification/SpecRover.pdf#page=7\|S070 §V.A · p.7]] |

运行时回归集来自原buggy程序，开发者修复后新增的acceptance tests仅用于评测，二者不能混为同一种反馈权限。reviewer的Table II又只统计119个生成过复现测试的任务，50% precision不是全300任务的成功率；其correct标签与人工语义参照/acceptance tests的确切衔接，现有文字不足以完全确认。选择后分母、覆盖率与标签不确定性详见[[wiki/papers/harness/verification/SpecRover#实验支持系统效果，尚不能隔离各组件贡献|唯一论文页]]。[[raw/papers/harness/verification/SpecRover.pdf#page=6|S070 §IV · p.6]] [[raw/papers/harness/verification/SpecRover.pdf#page=8|§V.B、Table II、Fig.6 · p.8]]

**本库推断与剩余材料缺口：**保持旧通过项不是无条件目标，先要确认需求与测试的语义是否仍有效。SpecRover没有在本次核读正文中报告同一任务每轮修订的稳定需求满足向量、非目标项1→0转移，或按改动影响范围重验证的固定预算对照；这不等于领域无人研究。初次补丁漏修一处、最终任务失败、测试覆盖不足，也都不能单独证明修订破坏了原本正确的功能。后续若核查该窄问题，需要稳定判据下的产物前后对与独立验证。[[raw/papers/harness/verification/SpecRover.pdf#page=2|S070 §II、Fig.1 · pp.2–3]] [[raw/papers/harness/verification/SpecRover.pdf#page=7|§V · pp.7–10]]

## 论文入口与交叉方向

- [[wiki/papers/harness/tools/MCPMark|S016 · MCPMark]]：交叉关联；主归属为`harness/tools`。
- [[wiki/papers/harness/orchestration/MetaGPT|S017 · MetaGPT]]：交叉关联；主归属为`harness/orchestration`。
- [[wiki/papers/harness/orchestration/Magentic-One|S018 · Magentic-One]]：交叉关联；主归属为`harness/orchestration`。
- [[wiki/papers/harness/orchestration/GPTSwarm|S019 · GPTSwarm]]：交叉关联；主归属为`harness/orchestration`。
- [[wiki/papers/harness/orchestration/TDAG|S020 · TDAG]]：交叉关联；主归属为`harness/orchestration`。
- [[wiki/papers/harness/orchestration/Multi-Agent-Failures|S021 · Multi-Agent-Failures]]：交叉关联；主归属为`harness/orchestration`。
- [[wiki/papers/harness/hooks/IsolateGPT|S022 · IsolateGPT]]：交叉关联；主归属为`harness/hooks`。
- [[wiki/papers/harness/hooks/AgentSpec|S023 · AgentSpec]]：交叉关联；主归属为`harness/hooks`。
- [[wiki/papers/harness/hooks/ShieldAgent|S024 · ShieldAgent]]：交叉关联；主归属为`harness/hooks`。
- [[wiki/papers/harness/hooks/InfrastructureSentinel|S025 · InfrastructureSentinel]]：交叉关联；主归属为`harness/hooks`。
- [[wiki/papers/harness/hooks/AGrail|S026 · AGrail]]：交叉关联；主归属为`harness/hooks`。
- [[wiki/papers/harness/verification/CRITIC|S027 · CRITIC]]：主归属。
- [[wiki/papers/harness/verification/AgentPRM-Xi|S028 · AgentPRM-Xi]]：主归属。
- [[wiki/papers/harness/verification/Agent-as-a-Judge|S029 · Agent-as-a-Judge]]：主归属。
- [[wiki/papers/harness/verification/CorrectBench|S030 · CorrectBench]]：主归属。
- [[wiki/papers/harness/verification/Self-MAP|S031 · Self-MAP]]：主归属。
- [[wiki/papers/optimization/data-environments/SWE-Gym|S038 · SWE-Gym]]：交叉关联；主归属为`optimization/data-environments`。
- [[wiki/papers/harness/verification/SpecRover|S070 · SpecRover]]：主归属。

[[wiki/harness/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
