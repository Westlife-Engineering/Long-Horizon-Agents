---
type: survey
source_id: S001
created: 2026-10-19
updated: 2026-10-28
reading_status: map-read
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
---

# Towards Long-Horizon Agents: A Survey

## 这张笔记的用途

这是一张**综述来源说明页**：记录当前知识地图依据哪份综述建立、我们读到了哪里，以及综述中的框架被整合进了哪些主题。综述在本库的作用是帮助探索领域；当前已启动 Harness / Optimization 多方向选读，尚未确定最终研究问题，具体队列和状态见 [[maintenance/research/R001#范围与检查点|第一轮研究]]。

- 想浏览领域地图，从 [[wiki/overview|总览]] 或 [[wiki/index|索引]] 进入六个主题。
- 想核对“这个分类或定义从哪里来”，在本页查原始 PDF、章节定位与阅读范围。
- 以后读入新论文，知识综合持续更新在主题页；本页继续说明 S001 这份综述本身，不承担全库的阅读计划或讨论汇总。

## 来源身份与读取范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S001 |
| 标题 | Towards Long-Horizon Agents: A Survey |
| 副标题 | Foundation, Evolution, Harness, Optimization, Application, and Frontier |
| 作者 | Guanting Dong 等，完整作者列表见原文 p.1 |
| 原件 | [[raw/surveys/Towards Long-Horizon Agents.pdf\|本地 PDF，共 149 页]] |
| 原文件名 | `Dong 等 - Towards Long-Horizon Agents A Survey.pdf` |
| 版本依据 | 用户提供的本地版本，以 SHA-256 区分；该综述本身的 DOI、arXiv 版本号、正式发表日期未确认，不用 PDF 创建时间代替 |
| SHA-256 | `C62DA7E66A4C3F7251ED8B450F51DF6500B2F850C7C70853779614E3D780E738` |
| 读取日期 | 2026-10-19；2026-10-24 补读 Foundation；2026-10-25 为选文核读 §4–5 与参考文献；2026-10-26 回读 §4.1–4.2；2026-10-27 回读 §4.3–4.6；2026-10-28 为组会跨模块讨论核读 §4，回读 §5.1–5.7，完整核读 §6 |
| 阅读状态 | 整体为地图式阅读（map-read）；§2 已做问题驱动精读，不是全文逐项精读 |

身份以 [[raw/surveys/Towards Long-Horizon Agents.pdf#page=1|原文首页]] 为准。本次核读摘要、目录、引言、核心定义与层级、演进主线，选读 §4–5 的组件/训练阶段入口和与笔记有关的正文，阅读 §6 应用定义与评测总述、§7 前沿及 §8 结论。重点核对 Fig.1、Fig.2、Fig.3、Eq.1 与 Table 8 的页面图像。

2026-10-24 针对阅读疑问补读 PDF pp.7–15 的 §2（p.8 为全篇分类图，p.15 含 §2 结尾及 §3 衔接），核对 p.9 的循环公式及 Fig.3/4/5 页面图像。重点整合状态—观察—上下文、固定基础策略与反馈适应、C2/C3 记忆用途、self-evolution 的四类改变对象，以及时间跨度代理的证据边界，写入 [[wiki/foundations/Formalization|基础理解页]]。§2.3 仅核读综述的指标说明和解释，未独立读取 METR 数据源或复算拟合；对话中的额外概率推导不计作本文已验证结论。

2026-10-25 两个同模型选文任务直接核读 §4（PDF pp.20–37）、§5（pp.37–55）的相关正文和所选参考文献条目，用于建立首轮候选及核对原始发布页身份。该范围属于选文定位阅读，不是全部方法和图表的逐项精读；所引独立论文的核读与摄入状态分别登记在唯一论文页及索引。

2026-10-26 围绕三类工作流的讨论回读 §4.1（PDF pp.20–23），核对 Fig.7 页面图像；将定义、特点、优缺点及并列／补强／组合关系整合到 [[wiki/harness/workflows|循环与工作流]]。关系图与 Plan–Execute 的局限分析标为本库归纳／推断，不视为综述统一对照实验的结论。

同日参考用户提供的“综述记忆部分总结”对话，回读 §4.2（PDF pp.23–26）、Table 3，核对 Fig.8 页面图像；在 [[wiki/harness/memory|上下文与记忆]] 前部整合两类状态、工作区三种操作、持久记忆内容与管理操作及信息循环。示意图、操作风险与 C2/C3 作用联系标明本库重绘／综合，学术依据仍追溯本综述。

2026-10-27 参考用户提供的“解释函数调用”对话，回读 §4.3（PDF pp.26–29），在 [[wiki/harness/tools|工具、MCP 与技能]] 前部补充概念表、关系辨析、技能库维护及完整任务评测说明；关系归纳与教学例子显式标记，基准结果保留综述转述身份，未新增独立论文读取或协议规范核验。

同日参考用户提供的“综述编排优化解释”对话，回读 §4.4（PDF pp.29–31）正文，在 [[wiki/harness/orchestration|编排]] 前部补充控制结构外化、四类设计问题及可选优化路线；方案来源与运行时固定／动态、协议与组织形式的区别标为本库辨析。未新增独立论文读取，未核验协议规范或逐项检查 Fig.9 图像。

同日参考用户提供的“综述 Hooks 和 Middleware”对话及其后续审核，回读 §4.5–4.6（PDF pp.31–37），核对 Fig.10 与 Table 4 页面图像；在 [[wiki/harness/hooks|Hooks 与中间件]]、[[wiki/harness/verification|验证]] 前部整合判断与执行控制的协作、政策准备与运行期对照、证据—评价—用途，以及 PRM 与免训练的范围辨析。两张 Excalidraw 图及贯穿例子为本库教学重组，方案不表示固定执行顺序；未新增独立论文读取。

2026-10-28 为 [[组会/2026-10-28-Harness/README|Harness 组会讨论]] 核读第 4 章正文：从 PDF p.20 章节标题至 p.37 第 5 章之前，并查看 Fig.7–10 与 Table 4。三个同模型子任务分别核对相关原页，两轮提案与互评后，主 Agent 将共享记忆的接受范围、工具封装的约束位置及主动验收的结果归属提炼到 [[wiki/harness/connections|跨模块联系与阶段性理解]]。它们是本库归纳、假设与教学情境，未追读原论文、未联网查新或实验；各角色实际页段与修订见组会记录。

同日参考用户提供的“解释 MLA 优势”对话，回读 §5.1（PDF pp.37–40），查看 Fig.11 页面图像；在 [[wiki/optimization/architecture|架构基础]] 重排显式上下文、压缩状态、混合与高吞吐的分层解释，补充 MLA 压缩对象和代表性例子。关系图、状态更新图与分类辨析为本库教学重组；MLA 和 MTP 的细节另回读库内 S042 DeepSeek-V3，未新增来源或实验。

同日参考用户提供的“综述5.2层次解析”对话，回读 §5.2（PDF pp.40–43），查看 p.42 页面图像；在 [[wiki/optimization/data-environments|数据与环境合成]] 以关系图和简表说明三个合成对象的配合、课程的独立调节维度、环境的分类依据与轨迹的四项改进。图示、概念辨析和修复任务例子标为本库归纳／教学情境；保留已有原论文比较，未新增来源或实验。

同日参考用户提供的“解析综述5.3”对话，回读 §5 总述（PDF p.37）、§5.3 及 §5.4 开头（pp.43–45），查看 p.44 页面图像；在 [[wiki/optimization/pretraining|预训练与中期训练]] 区分训练阶段、三类基础能力和横跨能力的数据策略，解释任务工作状态与长度边界。关系图、概念辨析和论文核对例子为本库教学整理；LongWriter、OPUS 仅保留综述转述身份，未新增来源或实验。

同日参考用户提供的“解析综述54内容”对话，回读 §5.4（PDF pp.45–47）、§5 总览（p.37）及 §5.6 导言（p.52），查看 Fig.11（p.39）。在 [[wiki/optimization/finetuning|微调]] 以关系图、简表说明行为塑造与冷启动、选择／课程／蒸馏的配合、蒸馏来源与过程结构的区别，以及学生状态覆盖的局限；图示与分类辨析为本库归纳。监督位置另回核库内 S048、S049 原文 p.4；未新增学术来源或实验。

同日参考用户提供的“解析综述5.5”完整对话，回读 §5 总述（PDF p.37）、§5.5（pp.47–52）及 §5.6 导言（p.52），查看 Fig.12 与 Table 6。在 [[wiki/optimization/reinforcement-learning|Agentic Reinforcement Learning]] 用闭环图和简表说明阶段定位、四个设计维度及其可组合关系，区分评价标准、反馈粒度与更新单位。图示、分类辨析和修复例子为本库教学重组；保留原论文比较，未新增来源或实验。

同日参考用户提供的“综述57层次解析”完整对话，回读 §5.7（PDF pp.53–55）、§5 总述与 Table 5（pp.37–38）、§5.2.1（p.41）及 §5.6.1–5.6.2（p.53），查看 Fig.11、Fig.13。在 [[wiki/optimization/self-evolution|自我演化]] 用闭环图与简表解释外层训练循环、离线／在线的组织方式和共同演化的更新对象；图示、维度辨析与代码修复例子为本库教学归纳。保留已有原论文比较，未新增来源或实验。

同日参考用户提供的“解析综述5.6内容”对话，回读 §5 总览（PDF p.37）、§5.6 及 §5.7 入口（pp.52–54），查看 pp.52–53 页面图像。在 [[wiki/optimization/distillation|On-Policy Distillation]] 用监督回路与简表解释学生状态分布、教师指导／自我改进及其与 SFT、RL、自我演化的关系；区分监督调度与信号构造、特权信息与环境反馈。图示与关系辨析为本库归纳；另回核库内 GKD、DAgger-LLM、π-Play、SD-Zero 的相关机制页，保留文本前缀与环境状态的区别，未新增来源或实验。

2026-10-28 为 [[组会/2026-10-28-Application/README|Application组会]] 完整核读 §6（PDF pp.55–67，第7节之前，含§6.6及Table7），查看Fig.14（p.57），回看§4与§5总述（pp.20、37）。以六篇原论文进行定向核查，形成 [[wiki/applications/success-mechanisms|已有应用的成功机制与瓶颈]]；本轮完整读取的是综述第6节，不表示逐项核验其全部引文。原始结果与推断分开，未复现实验，也不以本轮案例外推通用Agent所有子类。

2026-10-28 为 [[组会/2026-10-28-Optimization-RL/README|Optimization-RL组会]] 再核读完整§5（PDF pp.37–55，截至§6标题前），查看Table5 p.38、Fig.11 p.39、Fig.12 p.47、Table6 p.49、Fig.13 p.54。将七节以“训练条件—能力形成与适配—经验改进循环”组织到 [[wiki/optimization/Overview|Optimization总览]]；该关系是本库教学归纳，原节号与证据身份保留。另定向核读7篇原论文（4篇库内回读、3篇新增）支持 [[wiki/optimization/Questions#2026-10-28：从整体理解转向RL提问|三个RL问题与六个宏观问题]]；不表示逐项核验本综述全部引文，原论文版本／范围见各唯一页，未复现实验。

**尚未完成：**§4–6 所引全部方法的细节、全篇所有图表和全部参考文献的逐项核验。本次提取文本只用于定位，未作为新的原始来源。本文引用使用 PDF 页码；已使用的正文位置与印刷页码一致。

## 本文研究什么

综述希望统一讨论“长程 Agent 是什么，以及能力来自哪里”：相关工作涉及记忆、工具、训练和运行控制，但术语及能力归因容易混在一起。作者选择“外部 harness 与内部模型优化共同演进”作为组织主线，提供六个视角的领域地图。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=5|§1 · pp.5–6]]

## 核心理解与证据落点

| 本文的定义、归纳或观点 | 原文位置 | 已整合到 |
| --- | --- | --- |
| 长程任务关注多步依赖与持续反馈；Agent 是模型策略与 harness 的耦合系统 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=9\|§2.1 · Eq.1 · pp.7,9]] | [[wiki/foundations/Formalization\|Foundation]]、[[wiki/overview\|总览]] |
| H1–H3 / C1–C3 描述上下文内、跨上下文、跨任务的任务与能力范围 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=10\|§2.2 · Fig.3 · pp.10–11]] | [[wiki/foundations/Formalization\|Foundation]] |
| 环境观察、上下文组装、动作选择和状态转移组成闭环；部分可观测、终止与延迟效用有不同含义 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=9\|§2.1 · Agent–Environment Loop · p.9]] | [[wiki/foundations/Formalization#Agent 每一步究竟怎样循环\|运行循环]] |
| Long-horizon 与运行时长、自主程度、自我演化回答不同问题；持久改变可发生于参数、记忆、工具或拓扑 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=14\|§2.4 · Fig.5 · pp.13–15]] | [[wiki/foundations/Formalization#与相邻概念的区别\|概念辨析]] |
| 控制单位从提示、上下文扩展到整条运行轨迹，阶段相互嵌套 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=15\|§3 · Table 1 · pp.15–16]] | [[wiki/foundations/Evolution\|Evolution]] |
| Harness 分为循环/工作流、上下文/记忆、工具/MCP/技能、编排、hooks/中间件、验证 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=20\|§4 · p.20]] | [[wiki/harness/Overview\|Harness]] |
| Optimization 按架构基础及六个能力发展环节组织 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=37\|§5 · p.37]] | [[wiki/optimization/Overview\|Optimization]] |
| 架构按历史表示与运行效率区分；MLA 保留逐 token 访问，Hybrid 组合显式访问与压缩状态 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=38\|§5.1 · pp.38–40]] | [[wiki/optimization/architecture\|架构基础]] |
| 任务、环境与轨迹是三个耦合对象；课程正交调节难度，环境按转移与反馈机制分类，轨迹沿四个方向加工 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=40\|§5.2 · pp.40–43]] | [[wiki/optimization/data-environments\|数据与环境合成]] |
| 预训练／中期训练形成推理、长上下文状态与感知基础；数据选择、配比与结构横跨这些能力 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=43\|§5.3 · pp.43–45]] | [[wiki/optimization/pretraining\|预训练与中期训练]] |
| SFT 通过轨迹模仿塑造行为；选择、课程与蒸馏共同设计监督分布，覆盖仍受示范限制 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=45\|§5.4 · pp.45–47]] | [[wiki/optimization/finetuning\|微调]] |
| Agentic RL 从信用、更新、采样和交互结构四个维度组织长程策略学习 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=47\|§5.5、Fig.12、Table 6 · pp.47–52]] | [[wiki/optimization/reinforcement-learning\|Agentic Reinforcement Learning]] |
| 自我演化将自身经验回写训练；离线、在线与 Agent–环境共同演化可衔接，持续进步仍受验证和优化约束 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=54\|§5.7、Fig.13 · pp.53–55]] | [[wiki/optimization/self-evolution\|自我演化]] |
| 五类应用按环境接口划分；评测需要考虑跨度与模型/harness/训练的共同影响 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=56\|§6 · p.56]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=64\|§6.6 · pp.64–65]] | [[wiki/applications/Overview\|Application]] |
| 作者的开放方向分为 evolution、effectiveness、efficiency、trustworthiness 四条轴 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=68\|§7 · Table 8 · pp.67–68]] | [[wiki/frontier/Overview\|Frontier]] |

主题页承载持续综合，本页保留本论文的身份、解释与证据边界；后续精读仍更新这一个页面。

## 如何理解它的贡献与限制

这篇综述提供的是定义、分类、历史解释、资源梳理与研究立场。不能把整篇综述理解为一次统一对照实验，或者把“外化与内化共同演进”当成已经对所有任务验证的性能定律。作者在 §1 列明其贡献类型。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=6|§1 · Contributions and Roadmap · pp.6–7]]

§2.3 另有基于外部时间跨度评测数据的描述性拟合；原文指出上界估计、协议和覆盖差异带来的不确定性，也明确说趋势不能解释模型与 harness 的贡献来源。本库未独立核读该外部数据源，也未复算拟合，暂不引用增长数字作为已验证结论。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=12|§2.3 · Fig.4 · p.12]]

§7 是作者提出的研究立场，尤其不应把对未来的预期当成实证结果。当前还保留 [[wiki/frontier/Overview#需保留的原文表述张力|T001：终身学习必要条件的适用范围]]，避免在综合时掩盖原文差异。

返回 [[wiki/index|索引]]。
