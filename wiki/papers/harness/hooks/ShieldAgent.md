---
type: paper
primary_direction: harness/hooks
related_directions:
  - harness/verification
source_id: S024
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/hooks/ShieldAgent.pdf]]"
---

# ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning


## 阅读结论与证据身份

**原文陈述：**ShieldAgent 将政策文件转为动作相关的逻辑规则电路，再对当前动作、观察和历史进行检查。**它运行时仍生成 shielding plan、调用工具、给谓词赋值并生成验证代码**，不应读成“离线编译后只有静态规则运行”。逻辑验证只覆盖所编码规则与当前赋值；自然语言政策抽取、事实判定仍会出错。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=3|§3、Fig.1 · pp.3–6]]

## 两阶段分别在改变什么

| 阶段 | 输入、状态与操作 | 可靠性依赖 |
| --- | --- | --- |
| 政策建模 | GPT-4o 从法规、平台政策和用户约束抽取结构化政策与 LTL 规则；反复细化、去重，按动作聚类 | 抽取完整性、可观测谓词、原文与逻辑一致性；作者允许专家复查 |
| 权重学习 | 真实或模拟安全标签训练规则软权重 | 标签与样本分布；权重并非每条约束都不可违背 |
| 在线检查 | 抽取动作谓词、检索电路/历史工作流，生成计划，搜索、二元检查、内容检测与形式验证 | 检索、事实赋值、工具和生成代码的正确性 |
| 最终决策 | 比较执行/不执行动作两种赋值下的概率差与阈值，输出许可、违规规则和解释 | 模型内评分与阈值，不是现实系统总体安全概率 |

表中机制见 [[raw/papers/harness/hooks/ShieldAgent.pdf#page=4|§3.2 · pp.4–5]]、[[raw/papers/harness/hooks/ShieldAgent.pdf#page=6|§3.3 · p.6]]。Action rules 约束动作，physical rules 表达状态关系；状态谓词有时误判，后者作为逻辑知识辅助纠错。它没有提供 IsolateGPT 式进程/权限隔离，保护边界由宿主接入 guardrail 决策的位置决定。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=11|Appendix A.2 · p.11]]

规则电路按 Markov Logic Network 定义 $P_\theta(\mu)\propto\exp(\sum_r\theta_r\mathbf1[\mu\models r])$。Eq.5 的允许条件是 $P_\theta(\mu_{p_a=1})-P_\theta(\mu_{p_a=0})\ge\epsilon$，其他状态谓词保持不变。这是**编码模型里的相对评分条件**；不可将其写成对未知未来状态的现实概率保证。规则权重由 Eq.6 hinge loss 学习，谓词赋值前还有 LLM/工具步骤。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=5|§3.2.4、Eqs.4–6、Algorithm 1 · p.5]]

短期交互缓存服务当前动作序列，验证后丢弃；长期记忆保存成功检查工作流，用作类似规则的少样例计划参考。Search 与 Binary-Check 用基于 InternVL2-2B 微调的专门模型，工具还包括内容检测和形式验证器。**因此系统同时改变规则、检查模型和工作流复用，主结果不能单独归因于一种 hook。**[[raw/papers/harness/hooks/ShieldAgent.pdf#page=6|§3.3 · p.6]]

## 证据范围：检测、误拒和在线效用

ShieldAgent-Bench 以 AWM web agent、六种网页环境、AgentPoison 与 AdvWeb 两类扰动构造安全/不安全轨迹；基线拿到同一政策，分别为直接 GPT-4o 判定、逐规则检查、GuardAgent。Table 2 的 agent-based / environment-based ACC 为 90.4/91.7，FPR 为 5.6/4.0，规则召回 ARR 为 87.5/92.7。**规则召回不是攻击拦截率，仍有误拒和漏检。**它比逐规则遍历省调用，但比直接提示的 1 次调用更贵；运行时平均约 31–34 秒/样本，未包括所有离线建模成本。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=7|§4–5、Table 2 · pp.7–8]]

作者还重建 ST-Web、VWA-Adv、AgentHarm 的政策与轨迹，而非直接照搬原始任务成功指标。在线测试为 AWM 加逐步 post-verification 与反馈，Table 4 报的是**条件于任务成功的政策遵从率**，不是完整任务联合成功率，也未证明所有副作用都在发生前被拦截。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=7|§5.1 · p.7]] [[raw/papers/harness/hooks/ShieldAgent.pdf#page=8|§5.2、Tables 3–4 · p.8]]

> [!warning] 归档版本存在报告不一致
> p.2 写 2K，p.6/Table 1 写 3,110，§4 写“3,110 unsafe trajectories”，而 p.15 Table 9 合计是 1,555 safe + 1,555 unsafe = 3,110。p.17 图注又描述每样例一条安全、两条攻击轨迹。摘要/正文的平均提升说法也不同。本库引用具体表格条件，不替作者合并成单一数据构成或总体提升结论。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=2|p.2]] [[raw/papers/harness/hooks/ShieldAgent.pdf#page=6|§4、Table 1 · p.6]] [[raw/papers/harness/hooks/ShieldAgent.pdf#page=15|Table 9 · p.15]] [[raw/papers/harness/hooks/ShieldAgent.pdf#page=17|Fig.7 · p.17]]

案例 pp.24–28 确认运行时多轮赋值和生成 Prover9/Mace4 检查代码，但示意中的变量命名/值以及概率差数字也有不一致，不能把案例截图当作可直接运行且已经验证的程序。核心比较结论是机制责任划分，不是接受“形式验证”字样后的普遍安全宣称。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=24|Appendix G、Figs.15–19 · pp.24–28]]

## 对综述分类的修订

综述转述身份：S001 §4.5.2 把它置于 Static LLM-compiled Hooks，并将该类描述为编译后执行时无需进一步 LLM 介入。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=33|S001 §4.5.2、引文80 · p.33]] **本库核读后的限定：**存在离线政策结构化，但推理期仍有 LLM 计划、事实判定、代码生成、软规则推断。可以沿“规则何时产生”和“决策何时依赖模型”两轴描述，不能从分类名推断全流程静态。此直接证据来自归档 arXiv v2，尚未与 PMLR 逐项对齐，不推定两版本内容一致或将差异归因于版本变化。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=3|S024 §3、Fig.1 · pp.3–6]] 长程风险类别包括重复登录造成锁定，尚非任意长度/未知策略下的长期安全证明。[[raw/papers/harness/hooks/ShieldAgent.pdf#page=14|Appendix E.1 · p.14]]

## 来源身份与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S024 |
| 作者 | Zhaorun Chen、Mintong Kang、Bo Li |
| 版本 | arXiv:2503.22738v2，2025-11-27，32 页；PMLR 267 / ICML 2025 身份已核对，但正式 PDF 获取失败，未与 PMLR 逐项对齐 |
| 原始获取 | [原始 PDF](https://arxiv.org/pdf/2503.22738v2)；访问日期 2026-10-25 |
| 原件 | [[raw/papers/harness/hooks/ShieldAgent.pdf\|ShieldAgent，32 页]] |
| SHA-256 | `9217E40A58E778D19AF322BDC60C8ACFCC14FC0B9470867933BEA699B7707C34` |
| 综述入口 | S001 引文 [80]，§4.5.2，PDF p.33；书目 p.82 |
| 实际阅读 | 2026-10-25；主文 §§1–6 pp.1–8；Appendix A–F pp.11–16（机制/训练算法/统计）；案例 pp.17–18、24–28。实际看 Fig.1、Eqs.4–6/Algorithm 1、Tables 2–4/9 的 pp.3、5、7、8、15。未逐项核读 pp.19–23 全部政策示例和 pp.29–32 完整提示；未审查程序实现。 |
| 未做 | 未复现实验、未执行论文代码、未逐项追读相关工作；Obsidian 应用未测 |

本页页码均从归档 PDF 第一页计。论文结果是作者报告，不代表本库完成复现。已完成摄入并整合到 Harness 与索引；内容与结构验收通过，Obsidian 应用未测。

## 主题联系与后续核查

已整合到 [[wiki/harness/hooks|Hooks 与中间件]]，同时连接 [[wiki/harness/verification|验证]] 对判断来源和拦截位置的区分。跨论文分析由本库提出，不是新的实验结果；候选问题尚未查新，不据此宣布研究空白。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/hooks|harness/hooks]] · [[wiki/harness/verification|harness/verification]]。
