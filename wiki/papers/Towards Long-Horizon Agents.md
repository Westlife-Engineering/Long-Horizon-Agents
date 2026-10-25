---
type: paper
source_id: S001
created: 2026-10-19
updated: 2026-10-25
reading_status: map-read
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
---

# Towards Long-Horizon Agents: A Survey

## 这张笔记的用途

这是一张**综述来源说明页**：记录当前知识地图依据哪份综述建立、我们读到了哪里，以及综述中的框架被整合进了哪些主题。综述在本库的作用是帮助探索领域；当前已启动 Harness / Optimization 多方向选读，尚未确定最终研究问题，具体队列和状态见 [[wiki/overview#第一轮自主研究|第一轮研究]]。

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
| 原件 | [[raw/papers/Towards Long-Horizon Agents.pdf\|本地 PDF，共 149 页]] |
| 原文件名 | `Dong 等 - Towards Long-Horizon Agents A Survey.pdf` |
| 版本依据 | 用户提供的本地版本，以 SHA-256 区分；该综述本身的 DOI、arXiv 版本号、正式发表日期未确认，不用 PDF 创建时间代替 |
| SHA-256 | `C62DA7E66A4C3F7251ED8B450F51DF6500B2F850C7C70853779614E3D780E738` |
| 读取日期 | 2026-10-19；2026-10-24 补读 Foundation；2026-10-25 为选文核读 §4–5 与参考文献 |
| 阅读状态 | 整体为地图式阅读（map-read）；§2 已做问题驱动精读，不是全文逐项精读 |

身份以 [[raw/papers/Towards Long-Horizon Agents.pdf#page=1|原文首页]] 为准。本次核读摘要、目录、引言、核心定义与层级、演进主线，选读 §4–5 的组件/训练阶段入口和与笔记有关的正文，阅读 §6 应用定义与评测总述、§7 前沿及 §8 结论。重点核对 Fig.1、Fig.2、Fig.3、Eq.1 与 Table 8 的页面图像。

2026-10-24 针对阅读疑问补读 PDF pp.7–15 的 §2（p.8 为全篇分类图，p.15 含 §2 结尾及 §3 衔接），核对 p.9 的循环公式及 Fig.3/4/5 页面图像。重点整合状态—观察—上下文、固定基础策略与反馈适应、C2/C3 记忆用途、self-evolution 的四类改变对象，以及时间跨度代理的证据边界，写入 [[wiki/foundations/Formalization|基础理解页]]。§2.3 仅核读综述的指标说明和解释，未独立读取 METR 数据源或复算拟合；对话中的额外概率推导不计作本文已验证结论。

2026-10-25 两个同模型选文任务直接核读 §4（PDF pp.20–37）、§5（pp.37–55）的相关正文和所选参考文献条目，用于建立首轮候选及核对原始发布页身份。该范围属于选文定位阅读，不是全部方法和图表的逐项精读；所引独立论文的核读与摄入状态分别登记在唯一论文页及索引。

**尚未完成：**§4–6 全部方法细节、所有图表、全部参考文献的逐项核验。本次提取文本只用于定位，未作为新的原始来源。本文引用使用 PDF 页码；已使用的正文位置与印刷页码一致。

## 本文研究什么

综述希望统一讨论“长程 Agent 是什么，以及能力来自哪里”：相关工作涉及记忆、工具、训练和运行控制，但术语及能力归因容易混在一起。作者选择“外部 harness 与内部模型优化共同演进”作为组织主线，提供六个视角的领域地图。[[raw/papers/Towards Long-Horizon Agents.pdf#page=5|§1 · pp.5–6]]

## 核心理解与证据落点

| 本文的定义、归纳或观点 | 原文位置 | 已整合到 |
| --- | --- | --- |
| 长程任务关注多步依赖与持续反馈；Agent 是模型策略与 harness 的耦合系统 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=9\|§2.1 · Eq.1 · pp.7,9]] | [[wiki/foundations/Formalization\|Foundation]]、[[wiki/overview\|总览]] |
| H1–H3 / C1–C3 描述上下文内、跨上下文、跨任务的任务与能力范围 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=10\|§2.2 · Fig.3 · pp.10–11]] | [[wiki/foundations/Formalization\|Foundation]] |
| 环境观察、上下文组装、动作选择和状态转移组成闭环；部分可观测、终止与延迟效用有不同含义 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=9\|§2.1 · Agent–Environment Loop · p.9]] | [[wiki/foundations/Formalization#Agent 每一步究竟怎样循环\|运行循环]] |
| Long-horizon 与运行时长、自主程度、自我演化回答不同问题；持久改变可发生于参数、记忆、工具或拓扑 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=14\|§2.4 · Fig.5 · pp.13–15]] | [[wiki/foundations/Formalization#与相邻概念的区别\|概念辨析]] |
| 控制单位从提示、上下文扩展到整条运行轨迹，阶段相互嵌套 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=15\|§3 · Table 1 · pp.15–16]] | [[wiki/foundations/Evolution\|Evolution]] |
| Harness 分为循环/工作流、上下文/记忆、工具/MCP/技能、编排、hooks/中间件、验证 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=20\|§4 · p.20]] | [[wiki/harness/Overview\|Harness]] |
| Optimization 按架构基础及六个能力发展环节组织 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=37\|§5 · p.37]] | [[wiki/optimization/Overview\|Optimization]] |
| 五类应用按环境接口划分；评测需要考虑跨度与模型/harness/训练的共同影响 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=56\|§6 · p.56]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=64\|§6.6 · pp.64–65]] | [[wiki/applications/Overview\|Application]] |
| 作者的开放方向分为 evolution、effectiveness、efficiency、trustworthiness 四条轴 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=68\|§7 · Table 8 · pp.67–68]] | [[wiki/frontier/Overview\|Frontier]] |

主题页承载持续综合，本页保留本论文的身份、解释与证据边界；后续精读仍更新这一个页面。

## 如何理解它的贡献与限制

这篇综述提供的是定义、分类、历史解释、资源梳理与研究立场。不能把整篇综述理解为一次统一对照实验，或者把“外化与内化共同演进”当成已经对所有任务验证的性能定律。作者在 §1 列明其贡献类型。[[raw/papers/Towards Long-Horizon Agents.pdf#page=6|§1 · Contributions and Roadmap · pp.6–7]]

§2.3 另有基于外部时间跨度评测数据的描述性拟合；原文指出上界估计、协议和覆盖差异带来的不确定性，也明确说趋势不能解释模型与 harness 的贡献来源。本库未独立核读该外部数据源，也未复算拟合，暂不引用增长数字作为已验证结论。[[raw/papers/Towards Long-Horizon Agents.pdf#page=12|§2.3 · Fig.4 · p.12]]

§7 是作者提出的研究立场，尤其不应把对未来的预期当成实证结果。当前还保留 [[wiki/frontier/Overview#需保留的原文表述张力|T001：终身学习必要条件的适用范围]]，避免在综合时掩盖原文差异。

返回 [[wiki/index|索引]]。
