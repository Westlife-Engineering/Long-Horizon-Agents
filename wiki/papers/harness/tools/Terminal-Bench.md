---
type: paper
source_id: S080
primary_direction: harness/tools
related_directions:
  - harness/verification
created: 2026-10-28
updated: 2026-10-29
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/Terminal-Bench.pdf]]"
---

# Terminal-Bench：让 Agent 在真实终端里完成可验收的任务

**这是一篇评测基准论文。** 它把来自实际工作的问题做成可启动的计算机环境，让 Agent 自己探索、操作和修复，最后检查环境是否达到要求。本文的主要贡献是任务集与评测过程，另提供通用运行框架 Harbor 和用于模型比较的简单 Agent Terminus 2；不是新的训练算法，也不是综述。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|S080 · §§1–2.1 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§§3.1–3.4 · p.6]]

阅读时最值得抓住的区别是：**命令执行成功、Agent 宣称完成、最终测试通过，以及测试确实覆盖需求，是四件事。** Terminal-Bench 把最后两件事分别交给任务验收与基准质量审查；前者仍不能自动保证后者。以下解释依据本次锁定的 v1，不代表当前在线榜单。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=10|§5 · pp.10–11]]

## 来源身份与读取范围

- **标题／作者：** Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces；Mike A. Merrill、Alexander G. Shaw（共同第一作者）、Nicholas Carlini 等，完整作者见 PDF p.1。
- **固定版本：** [arXiv:2601.11868v1](https://arxiv.org/abs/2601.11868v1)，2026-01-17；[原始 PDF URL](https://arxiv.org/pdf/2601.11868v1)，DOI `10.48550/arXiv.2601.11868`。2026-10-28 核对官方版本页的标题、作者、日期与 DOI；仅作身份核对，不保留网页快照。
- **原件：** [[raw/papers/harness/tools/Terminal-Bench.pdf|84 页 PDF]]；SHA-256 `4430E04A507B2442BB7B24A88899B750948FA0A6B3BBC33A8D541D6D4DEBCC1E`。从用户指定的 `C:\Users\ZENGZX\Desktop\人大高瓴paper\Agent & RSI\Terminal-Bench - Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces.pdf` 复制，保留外部原件；全 Raw 哈希排重无重复，复制前后哈希相同。
- **实际阅读：** 2026-10-28 读取正文 §§1–7（PDF pp.1–11），附录 A 的实验统计说明（p.21）、B 质量控制（p.21、pp.25–28）、C 轨迹错误定义与例子（pp.29–35）、F Terminus 2（p.51）、G 调用/token 分析（pp.51–53）、Table 2（p.81）。2026-10-29 按 benchmark 阅读工作流回核正文、人工一致性与统计说明，补读 H 的任务描述（p.54）、ABC Table 3（p.82），浏览适配列表（p.84），并全文检索指标及区间计算线索。PDF 页码与印刷页码一致。
- **原页图表检查：** pp.3–5 的 Figs.1–4／Table 1、pp.9–10 的 Figs.8–9、p.51 Fig.34、pp.52–53 Figs.35–36、p.81 Table 2；本次补查 pp.7–9 的 Figs.5–8 与 p.54 任务表。附录逐任务结果矩阵、完整命令分类及每模型分布、全部任务清单、适配器实现和官方代码未逐项核读；未运行基准或复现实验。
- **归属理由：** 主归属 `harness/tools`，与本库 MCPMark、Toolathlon 的工具环境评测并列；任务验收与错误诊断交叉关联 `harness/verification`。目录归属是本库导航判断，不把评测误写为工具调用方法。

## 为什么值得测，新增价值在哪里

**作者的目标：**终端是软件工程、系统管理、科学计算等专业工作的共同接口；能生成命令还不足以说明能独立完成工作。作者希望测试需要领域知识、相互依赖的操作和自主排错的完整任务，补足既有评测在任务广度、现实环境与前沿难度方面的不足。前半部分是明确的测量动机；“既有基准不足”仍需按具体比较对象判断。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|§1 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|§6 · p.11]]

**本库判断：**这项测量有助于开发者选择、调试能交付技术工作产物的 Agent，也可为研究者提供失败轨迹。它直接测到的是“模型＋harness 在选定困难任务、环境与预算下的完成表现”；若要把分数解释为独立的规划能力、一般职业胜任力或经济收益，还缺少对应的控制或外部验证。其增量在于把多领域终端任务、执行环境和题目质量审查结合起来，不能仅凭“模型仍做不完”证明价值。依据：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|§§1–2 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§3.1 · p.6]]。

作者在 Related Work 中作了以下定位比较。**这是本文的分类与主张**，没有一组统一横向实验证明 Terminal-Bench 全面优于它们。2026-10-29 已进一步核读其中五篇原论文，独立比较见表后的综合入口；其余被引工作仍未在本轮核读。

| 本文比较的范围 | 举出的工作 | 作者强调的区别 |
| --- | --- | --- |
| 软件工程 | SWE-Bench、SWE-Bench Multimodal、SWE-Lancer、HumanEval、DevEval | 扩展到软件工程以外的终端技术工作 |
| 工具使用 | τ-Bench、Berkeley Function Calling Leaderboard | 将工具操作放入完整、可执行的终端任务 |
| 计算机使用 | WebArena、Visual Web Arena、AppWorld、OS World | 以真实 shell 为接口，强调专家贡献的困难任务 |
| 科学研究 | ReplicationBench、MLGym-Bench、Auto-Bench | 任务范围不限定于科学研究 |
| 终端专项 | shell 脚本优化、环境配置、自然语言转 Bash 的相关工作 | 从专项操作扩展到一般的 Agent 计算机操作 |

定位：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|§6 · p.11]]。不能把作者的“真实 shell”论述扩写成其他基准都不真实；与本库已读评测的协议比较另见下文。

**读过前作后的修订判断：**[[wiki/applications/terminal-bench-comparison|五篇前作与八项主张的反证审视]] 已核读 [[wiki/papers/harness/tools/SWE-bench|S082 SWE-bench]]、[[wiki/papers/harness/tools/SWE-Lancer|S083 SWE-Lancer]]、[[wiki/papers/harness/tools/AppWorld|S084 AppWorld]]、[[wiki/papers/harness/tools/OSWorld|S085 OSWorld]]、[[wiki/papers/harness/tools/tau-bench|S086 τ-bench]]。OSWorld 真实 OS 中可以打开终端，SWE-Lancer 也提供真实容器和终端命令；“其他基准是合成环境”作为普遍比较须收窄。仍有支持的增量是多种专业终端任务与审查流程的组合；更好的现实代表性、verifier 准确性或经济收益预测尚未由横向证据建立。[[raw/papers/harness/tools/OSWorld.pdf#page=3|S085 · §§2.2–3.1 · pp.3–5]] [[raw/papers/harness/tools/OSWorld.pdf#page=36|App.D.5.1 · p.36]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|S083 · §3.1 · p.5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|S080 · §2.4、Fig.4 · p.5]]

## 它要测什么，任务怎样走完

论文关注的不是把一句自然语言翻译成一条 Bash，而是完成依赖多个步骤的技术工作，例如迁移旧程序、配置系统、训练模型或恢复数据。一个任务把**初始环境、目标描述、最终检查和可行解**放在一起，再设置时间上限。评测检查容器最终状态，不按 Agent 的命令序列或终端输出字符串直接评分，因此允许不同实现路线。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|§§1–2.1 · p.2]]

| 任务组成 | 在评测中做什么 | 容易混淆的边界 |
| --- | --- | --- |
| 指令与 Docker 环境 | 提供目标、软件、文件和可操作状态 | 真实 shell 不意味着覆盖所有真实工作，也不意味着环境不会漂移 |
| Agent 的交互执行 | 观察环境，运行命令或工具，修改文件和状态 | 基准不强制所有参评 Agent 只能使用 Bash |
| 测试 | Agent 执行后将测试复制入环境，检查最终结果 | 隐藏验收测试不是每步向 Agent 提供的成功 oracle |
| 人工参考解与时限 | 参考解用于证明至少有一条可行路线；时限约束执行 | 参考解不交给被测 Agent，也不是要求它逐步模仿的唯一轨迹 |

依据：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|§2.2、Fig.2 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3 · p.4]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§3.1 · p.6]]。表中边界为本库据这些设置作的解释。

Fig.2 的 COBOL 迁移例子很直观：输入是旧程序、相关数据与“用 Python 产生相同结果”的要求；Agent 要读取源码和数据、理解行为、编写实现并自行检查；最终评测看所需文件和程序行为。图里即使文件存在，一旦数据缺失或账户余额不符，任务仍不通过。它说明“产物出现了”比“功能等价”弱得多。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|Fig.2 · p.3]]

另一类任务是用 R 实现 adaptive rejection sampler：除生成样本，还要求验证输入、检查对数凹性，并与已知分布作统计比较。它说明不同专业任务的正确性要求并不相同；本次仅核读任务描述，未检查测试源码中的统计阈值及误判率，不能据描述认定评分器已充分验证分布正确性。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=54|App.H · p.54]]

**与专业工作对齐到哪里？** 本库认为，终态验收保留了“交付结果达到要求”的工作逻辑，且容许不同解法，不必让模型模仿人类的操作序列。但任务说明与测试彼此一致，只能证明内部规范对齐；它们是否涵盖实际雇主会要求的性能、可维护性或其他质量，仍须逐题检查。本次未见将同一批产物交给独立领域专家按现实验收标准复核的系统性实验，因而将现实对齐判断为**有设计支持，外部验证有限**。原文依据：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|§2.1 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3 · p.4]]。

**本库分析：**这里的“长”主要体现在连续环境操作和跨步骤依赖；Terminus 2 还能通过摘要接续上下文。因此它能给 H1／部分 H2 压力提供任务场景，但论文没有按本库 H1–H3 标注逐任务需求，也没有直接测跨任务经验积累的 H3。不能把人类预计耗时、模型 token 数和任务依赖长度当成同一个量。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|§2.4 · p.5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=51|App.F · p.51]]；定义入口见 [[wiki/foundations/Formalization|任务层级与时间代理]]。

## 难任务先要成为可信的测量工具

Terminal-Bench 2.0 从 93 位贡献者提交的 229 个任务中，依据作者难度评估和人工质量审查选取 89 个。它是**刻意构造并筛选的困难任务集**，不能据此估计日常终端工作的平均完成率；正文的人工耗时也是任务作者估计，未报告统一招募人类受试者的计时实验。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|§2.2 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|§2.4、Table 1 · p.5]]

§4.3 又用 Terminus 2 搭配所选模型的通过表现定义经验难度，与作者预测的人类难度比较。Fig.7 中，作者预估为 hard 的题大部分对模型也难，但预估为 medium 的题仍有相当部分落入模型 hard。**这比较的是人的预估与特定系统的经验难度，不是人类与模型在同等条件下的实测胜任力，也不是评分器与专家验收的一致性。** 更换模型集合或 harness，经验难度可能改变；本库不将其当作任务固有的难度尺度。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=8|§4.3、Fig.7 · pp.8–9]]

质量审查围绕三个不同问题展开：

| 标准 | 要排除的问题 | 实际检查方式 |
| --- | --- | --- |
| Specificity：说明与测试一致 | 测试要求指令没说的细节，或指令要求的功能没有被测 | 贡献者清单、LLM 检查与人工复核要求双向对应 |
| Solvability：确实可解 | 环境或测试有错，使任何 Agent 都无法完成 | 人工参考脚本必须通过；无操作的 dummy Agent 应失败 |
| Integrity：通过不能靠作弊 | 读到参考答案、未来 Git 状态，或利用测试只检查“正确答案存在” | 隔离测试／参考解；多模型运行审查；对抗 Agent 找捷径后由人工确认 |

依据：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3、Fig.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=21|App.B.1 · p.21]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=25|App.B.2–B.4 · pp.25–27]]。

**原文的验证标准不是完备性证明。** 作者将“测试通过当且仅当终态可接受”作为审查目标，同时承认仍可能有漏测、歧义、非确定性和作弊通道；附录也承认没有客观测试覆盖指标及基准缺陷对分数影响的量化分析。这让我们可以相信它经过较多检查，不能据此声称所有任务的 verifier 都完全正确。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=10|§5 · pp.10–11]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=27|App.B.5 · pp.27–28]]

### 与人类评价的一致性，验证了哪一层

**有人工对照，但不能将它概括成“整个基准与专家验收一致”。** 最终任务成败由程序测试判定，轨迹与命令的失败分析另用 LLM judge；两类评价的验证证据不同。

| 评价对象 | 论文报告的人工证据 | 本库判读 |
| --- | --- | --- |
| 最终任务成败 | 人工审题、参考解、运行轨迹复核和对抗审计 | 支持题目质量控制；已读范围未见代表性终态的独立专家验收与 verifier 误放行／误拒绝统计 |
| 轨迹失败原因 | 两位标注者；20 条校准轨迹报告 Cohen's κ 为 93%；judge 对 120 条人工标注轨迹报告 agreement 90%、precision 92%、recall 90% | 支持该样本及 rubric 下的辅助诊断；κ 不是简单准确率，不能迁移为最终验收正确率 |
| 单条命令是否失败 | 三位标注者对 66 对输入输出形成多数标签，judge agreement 为 92.4% | 验证命令级失败识别，不表示整个任务失败 |
| 命令失败分类 | 对一位作者的 50 条标注，judge agreement 为 82.0% | 范围较小的分类校准，不能外推为各模型、类别均有相同可靠性 |

定位：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=9|§§4.4–4.5 · pp.9–10]]。数字为固定版本原文报告，未复算；文中所称标注者不能自动称为各领域专家，校准与最终验证样本的完整划分本次未取得。

ABC 清单的 judge 准确性／人工一致性项在 Table 3 标为 N/A，测试质量另按人工审查等项目评估。因此，本库不把“没有最终验收的人工一致性数字”直接判为无效，而是保留测试覆盖与外部验收尚未充分量化的限制。该清单是论文报告的自我评估，ABC 作者参与过开发；清单分数不增加独立证据，也不能取代具体实验描述。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=27|App.B.5 · pp.27–28]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=82|Table 3 · p.82]]

## Harbor、Terminus 2 和模型成绩分别是什么

Harbor 负责描述任务、启动隔离环境和运行评测；Terminus 2 是被评测的 Agent scaffold 之一。后者让模型产生按键，在 Docker 内的 tmux shell 执行，再把终端面板内容送回模型；上下文接近上限时调用模型做摘要。**“只有一个终端工具”不等于没有 harness**：状态接口、输出捕获和摘要接续已经是运行设计。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§§3.1–3.4 · p.6]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=51|App.F、Fig.34 · p.51]]

实验涵盖六种 Agent，对支持的模型—Agent 组合至少重复运行五次；正文报告 32,155 次单任务尝试。可配置 reasoning effort 使用提供方默认值，闭源模型走第一方 API、开放权重模型走 Together.AI；容器在 Daytona 上运行。每任务有时间上限，但本次核读正文和附录未取得逐任务时限、完整版本配置及等成本约束，不能把所有组合描述成完全相同预算。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|§2.1 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§3 · p.6]]

**结果应读成组合能力的历史快照。** Fig.1 对每个模型选择成绩最好的 scaffold；最高组合 GPT-5.2＋Codex CLI 的平均 resolution rate 约为 63%。这说明该测试集在论文测量时仍有未完成任务，不说明当前模型上限，也不直接等同于部署可靠率。核对模型与 scaffold 的变化看 Table 2，而不是只看 Fig.1 的横条长度。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|Fig.1 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=81|Table 2 · p.81]]

**分数与不确定性：**论文报告任务解决率及 95% 置信区间，A.3 说明逐任务结果对对应任务—Agent—模型的尝试取平均。“重复运行至少五次”不意味着报告的是“五次中至少成功一次”；不能自行将其改称 pass@5。本次在正文、A.1–A.3 和 Table 2 中未定位到总分加权、区间估计方法及基础设施失败处理的完整计算说明，全文关键词检索也未补足；因此不复算差异显著性，不把 32,155 次尝试当作同样数量的独立任务。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§3 · p.6]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=21|App.A.1–A.3 · p.21]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=81|Table 2 · p.81]]

**成本也是结果的一部分：**Fig.5 给出成绩与美元成本的 Pareto 前沿；在所画组合中，更贵并不总带来更高解决率。它支持按资源取舍系统的读法，不能视为等成本受控比较。本次未核对计价时间、环境及评分成本是否全部计入，加之附录 token 统计分母存在差异，暂不引用精确美元数作为复现预算。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=7|§4.1、Fig.5 · p.7]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=81|Table 2 · p.81]]

作者据选定组合的差异提出“模型选择通常比 scaffold 更重要”；**本库保留其为作者解释**：兼容组合不是完整因子实验，成本、工具与上下文处理也未全部控制，无法推出“harness 普遍不重要”。同样，附录 G 的跨模型平均轮数／输出 token 相关性，不是对同一系统增加预算的干预实验，不能用来否定 test-time scaling。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=7|§§4–4.1 · p.7]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=52|App.G · pp.52–53]]

## 错误分析在诊断什么

轨迹级分析在统一 Terminus 2 下，对每个任务、每个模型抽取两次失败尝试，使用 rubric 与 LLM judge 识别错误，人工校准范围见上节。它把错误分为执行、一致性、验证三类；**不是把总失败率拆成互斥原因的因果占比**，一个轨迹可能同时违反多条 rubric。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=9|§4.4、Fig.8 · p.9]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=29|App.C.1–C.3 · pp.29–35]]

| 观察层次 | 例子 | 可以据此说什么 |
| --- | --- | --- |
| 执行 | 不遵守任务规范、无实质策略变化地重复、没有适时停止 | 某类可观察行为出现在失败轨迹中；未证明加某模块就能修好 |
| 一致性 | 忘记已知状态、行动与声称不符、偏离目标 | 过程约束没有持续保持；尚不能只归因于上下文窗口大小 |
| 验证 | 过早宣告结束、没有相关检查、检查未覆盖关键性质 | 自检与真正满足要求之间有缺口；不是说所有终态 verifier 都失效 |
| 单条命令 | 程序未安装／不在 PATH、文件不存在、运行时错误 | 命令返回了错误；不等于整个任务必然失败，也未区分全部有意探测和不可恢复错误 |

依据：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=9|§§4.4–4.5 · pp.9–10]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=29|App.C · pp.29–34]]；后半列是本库的诊断边界。

附录的 MTEB 例子尤其适合解释弱验证：网页获取失败后，Agent 猜一个模型名、写入指定文件，再通过读取文件确认“写入了”。检查确实执行了，但只证明文件内容存在，没证明它是指定日期的正确榜首。该案例仍是论文刊载的失败片段，不是本库复现。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=34|App.C.3 · p.34]]

**实际发现：**Fig.8 展示的两个闭源模型在失败样本中以执行类问题较突出，Qwen Coder 480B 的错误分布更广；命令级抽取的 3,800 个失败中，“命令不存在”是最多的子类。这些结果把“没完成”具体化为可进一步检查的行为与环境问题，但抽样只覆盖失败，不能据此估计所有运行中的发生率；作者建议改进指令遵从或自我监控，仍需干预实验判断是否有效。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=9|§§4.4–4.5、Figs.8–9 · pp.9–10]]

## 与本库已有评测放在一起看

三篇都关心环境中的任务结果，不能把“终态验收”当成 Terminal-Bench 独有贡献。真正值得对齐的是接口、任务覆盖、运行约束与重复成功指标；下面比较协议，不跨基准排列模型分数。

| 来源 | 环境与主要测量对象 | 运行与重复口径 |
| --- | --- | --- |
| [[wiki/papers/harness/tools/Terminal-Bench\|S080 Terminal-Bench]] | 困难终端工作；多类技术任务，检查容器终态 | 每任务时限；多种 scaffold，兼容组合至少五次；报告 resolution rate 与置信区间 |
| [[wiki/papers/harness/tools/MCPMark\|S016 MCPMark]] | 127 个任务、五类 MCP 服务，检查有状态工具工作流 | 基础 MCPMark-Agent；100 turns／3600 秒，四次运行；区分 pass@1、pass@4 与 pass^4 |
| [[wiki/papers/harness/tools/Toolathlon\|S076 Toolathlon]] | 108 个任务、32 个应用；每任务暴露必要服务器，保留服务器内部工具选择 | 统一基础框架，100 轮、三次运行；区分 pass@1、pass@3 与 pass^3 |

比较证据沿用 2026-10-28 的原文核查，本次未重新读取 MCPMark／Toolathlon：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|S080 · §§2.1、3 · pp.2、6]]；[[raw/papers/harness/tools/MCPMark.pdf#page=4|S016 · §§2–3.1 · pp.4–6]]；[[raw/papers/harness/tools/Toolathlon.pdf#page=4|S076 · §§2.2–2.4 · pp.4–5]] [[raw/papers/harness/tools/Toolathlon.pdf#page=7|S076 · §4.1 · p.7]]。

## 局限与本版本待核查点

- **公开与联网：**允许安装依赖和查询网页，带来外部状态漂移及读取公开参考解的可能；作者称未在已观察轨迹中发现后者，不能推成不会发生。canary 字符串有助于去污染，但无法防止故意训练；本版本没有私有测试集。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=10|§5 · pp.10–11]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=28|App.B.5 · p.28]]
- **环境一致性：**容器与依赖约束改善复现，仍受硬件、资源限制、联网 API 和运行时影响。附录 B.2 对 apt 与 Python 依赖采取不同固定策略，不宜概括成“所有依赖完全锁定”。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=10|§5 · p.10]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=25|App.B.2 · p.25]]
- **更新与时间外推：**作者在 §4.2 计划持续评测新模型、发布更难任务，并预测 2.0 可能趋于饱和。这是论文当时的计划与展望，不是本次核实的后续进展；Fig.6 使用各模型的最佳 harness，也不能把时间趋势全部归因于模型本身。今后比较须锁定数据集和协议版本，不能直接串接不同版本的分数。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=7|§4.2、Fig.6 · pp.7–8]]
- **任务数与统计范围不完全对齐：**正文称 89 个任务，Table 1 的两行计数各合计 74，Table 2 图注又将 token 统计称为“全部 74 个任务”。本次未取得原始实验配置解释差异；不擅自把所有表的分母改成 89，也不据 token 列复算全套成本。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|§2.2 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|Table 1 · p.5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=81|Table 2 · p.81]]
- **报告内部版本痕迹：**§3 开头的模型数量与后续名单／结果表未完全对齐；附录 G 图例与正文的相关系数、显著性值及部分结果描述也不一致。本页不采用这些精确相关值作为定量结论；若后续需要成本比较或复现，应先核对实验配置与原始统计。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§3 · p.6]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=52|App.G、Figs.35–36 · pp.52–53]]

## 怎样使用这个评测

以下是依据前文证据的**本库使用判断**，不是论文验证过的部署建议：

- **研究困难终端任务的完成与失败：**可沿“指令→环境→产物→测试→轨迹”检查问题，先区分 Agent 失误、规范缺口和验收缺陷，再提出需要实验验证的改进。
- **比较候选系统：**可在固定任务版本和明确预算下比较模型／harness 组合，同时检查任务类别与成本；进一步声称某组件更好，需要控制其他条件。一次运行通过不等于跨尝试可靠。
- **估计实际业务价值：**先检查本领域工作是否被覆盖，补充代表性任务及业务验收；本论文的困难题总分不足以直接回答可替代多少现实工作。

这篇论文带来的持久认识是：把真实问题放进可执行环境后，仍须回答“失败来自系统，还是题目与测试”，所以任务设计与测量工具的验证必须一起读。它没有据此确认新的研究缺口，也不改变模型／harness 的一般优先级。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|§2.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|§7 · p.11]]

## 已整合主题与验收

已整合至 [[wiki/applications/Overview|应用与评测]]、[[wiki/harness/verification|验证]] 及 [[wiki/applications/terminal-bench-comparison|反证导向的跨基准比较]]；保留前轮测量价值、现实对齐、人工一致性与 MCPMark／Toolathlon 比较。本轮主协调者回读 pp.2–11、21、25–28、51、81–82，视觉核对 pp.3–5、81–82；五篇前作的决定性原页复核见 [[maintenance/research/2026-10-29-terminal-bench-review|维护记录]]。未复现实验，Obsidian 内显示与来源跳转未实测。
