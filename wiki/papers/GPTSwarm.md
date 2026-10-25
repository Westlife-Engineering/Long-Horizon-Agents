---
type: paper
source_id: S019
created: 2026-10-25
updated: 2026-10-25
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/GPTSwarm.pdf]]"
---

# GPTSwarm: Language Agents as Optimizable Graphs

> [!info] 状态
> 原文核读、主题整合与主 Agent 内容/结构验收已完成；未复现实验，Obsidian 应用未测。

## 来源身份与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S019 |
| 作者 | Mingchen Zhuge、Wenyi Wang、Louis Kirsch、Francesco Faccio、Dmitrii Khizbullin、Jürgen Schmidhuber |
| 锁定版本 | ICML 2024 / PMLR 235:62743–62767 官方会议 PDF，25 页；PDF 内页码 1–25 |
| 原始发布页 | [GPTSwarm](https://proceedings.mlr.press/v235/zhuge24a.html) |
| 下载原件 | [原始 PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/zhuge24a/zhuge24a.pdf)；访问 2026-10-25 |
| Raw | [[raw/papers/GPTSwarm.pdf\|GPTSwarm.pdf，25 页]] |
| SHA-256 | `63AAB69835F124FD1BEE714A21433A696C4D8D36DA9F7883E0B5B01B836FD6ED` |
| 阅读日期与范围 | 2026-10-25；正文 §§1–5（pp.1–9）；附录 D、E.1（pp.17–18）、E.2–E.3（pp.20–22）、F资源表（p.25）及 G局限（p.22）；实际查看 p.4 Eq.2/算法2–3、p.6 Fig.3–4、p.8 Table2。未逐项核读 pp.10–16 全部书目/工程图、p.19 示例及 pp.23–24 全部 GAIA prompts。 |
| S001 引用路线 | 引文 897，§4.4.3，PDF pp.30；书目 pp.148 |

本页页码均按所存 PDF 第一页计数；除 GPTSwarm 的会议卷页码外，引用采用 PDF 内页码。下载后验证标题与哈希，以不覆盖方式归档。作者/版本按实际原件登记，不沿用综述的不同署名。

## 把通信结构也变成优化对象

**原文陈述：**GPTSwarm 将 LLM 调用、工具或函数操作当节点，输入/输出传递当有向边；一个 Agent 是子图，团队是组合图。论文形式化与实验限于 DAG，按拓扑顺序执行，节点接收题目及前驱输出。这里优化的不只是角色提示，也包括哪些节点可互通。[[raw/papers/GPTSwarm.pdf#page=2|§§2.1–2.2 · pp.2–3]]

| 改变对象 | 更新方式 | 不应混淆的概念 |
| --- | --- | --- |
| Agent 间候选边的分布参数 | 采样不成环的组合图，用任务 utility 与 REINFORCE 更新边概率 | 参数是图分布，不是基础 LLM 权重 |
| 节点 prompt | 保留节点输入输出历史，由改进器选择/修改提示；HumanEval 实现选择演示样本 | 提示优化与推理时重新分配子任务不同 |
| 给定图上的本次执行 | 按依赖执行节点并传递输出，输出节点聚合 | 不是任意循环的状态机或自动增加无限 Agent |

来源：[[raw/papers/GPTSwarm.pdf#page=3|§2.3、Eq.1 · pp.3–4]] [[raw/papers/GPTSwarm.pdf#page=4|§2.4、Eq.2、Algorithms2–3 · p.4]]。

边优化目标是最大化图采样后的期望 utility；因此必须存在能为试验图提供反馈的任务评估器。**本库推断：**这把编排设计转为有反馈成本的搜索/学习问题，仍要核对反馈权限、优化题目与测试题目是否分开。它不直接证明某次真实任务卡住后会安全地重规划。

## 四类实验不可混成一个结论

| 实验 | 实际优化与证据边界 |
| --- | --- |
| MMLU 对抗者 | GPT-4-Turbo，dev 上 200 次迭代、每次四个图样本，验证前10%共153题评估；学习抑制被提示故意答错的节点。恢复接近单 IO 基线，不是任意未知恶意 Agent 的安全保证。[[raw/papers/GPTSwarm.pdf#page=5\|§3.1 · p.5]] [[raw/papers/GPTSwarm.pdf#page=18\|Appendix E.1 · p.18]] |
| Mini Crosswords | 同一20题子集用于优化与评估；utility 是图返回候选中的 best-state word accuracy，需参考正确词，不等于自行选择最终答案的整题成功率。边数接近的随机分布对照提示收益不只来自密度，但不等于全面匹配 token/调用成本。[[raw/papers/GPTSwarm.pdf#page=5\|§3.2 · pp.5–6]] |
| HumanEval | ReAct 式代码节点用题干给定测试反馈；每四个新问题更新演示、最多四例，在最近十个输入比较候选提示。在线积累与整集重复评估应保留，不能直接当独立留出集上的静态模型成绩。[[raw/papers/GPTSwarm.pdf#page=7\|§3.3 · p.7]] [[raw/papers/GPTSwarm.pdf#page=20\|Appendix E.3 · pp.20–22]] |
| GAIA | 七个同类 ToT Agent＋self-consistency 展示模块框架，作者明确没有边或节点优化。不能用 GAIA 提升证明 REINFORCE 编排有效。工具和调用规模随配置变化。[[raw/papers/GPTSwarm.pdf#page=7\|§3.4、Tables1–2 · pp.7–8]] |

Mini Crosswords 的优化从 GPT-3.5-Turbo 图分布迁移到 GPT-4-Turbo 的实验值得注意，但仅选一个图分布、相同题目池，不能扩大为跨任务普遍迁移。附录 D.2 进一步在该20题上做节点优化，仍属此条件。[[raw/papers/GPTSwarm.pdf#page=6|§3.2 · p.6]] [[raw/papers/GPTSwarm.pdf#page=17|Appendix D.2 · p.17]]

## 成本、失败与本库比较位置

Table11 分开优化与评估成本，节点/边优化需要额外运行；图更稠密也可能增加传播与调用。附录 G 明确当前重心是 Agent 间连接，Agent 内部拓扑变化和百级规模通信仍待研究；这些是作者限制/展望。[[raw/papers/GPTSwarm.pdf#page=22|Appendices F–G · pp.22,25]]

本篇将 [[wiki/harness/Overview#编排|编排]] 与 [[wiki/optimization/Overview|优化]] 连在“可学习外部结构”这一接口上，但不得归为基础模型训练。与 MetaGPT、Magentic-One 的直接机制比较已有本批原文支持；DyLAN、DSPy 等对比只记录作者实验/转述，本次未独立核读其原论文。下一条证据应是固定工具/反馈权限、计入优化费用的独立任务迁移；这是材料需求，尚不宣布研究空白。

## 主题联系与验收状态

已整合到 [[wiki/harness/Overview#编排|Harness · 编排]]；涉及反馈检查时联系 [[wiki/harness/Overview#验证|验证]]。共享主题与索引已同步，已通过主 Agent 内容/结构验收并完成摄入。关键页码和 Raw 哈希已检查，Obsidian 应用渲染与来源跳转未测。

返回 [[wiki/index|索引]]。
