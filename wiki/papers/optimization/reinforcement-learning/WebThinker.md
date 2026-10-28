---
type: paper
source_id: S074
primary_direction: optimization/reinforcement-learning
related_directions:
  - harness/tools
  - harness/orchestration
created: 2026-10-28
updated: 2026-10-28
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf]]"
---

# WebThinker：把找资料、推理与报告状态接到一起

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S074 |
| 原文标题 | WebThinker: Empowering Large Reasoning Models with Deep Research Capability |
| 作者 | Xiaoxi Li、Jiajie Jin、Guanting Dong、Hongjin Qian、Yongkang Wu、Ji-Rong Wen、Yutao Zhu、Zhicheng Dou |
| 版本 | arXiv:2504.21776v2，2025-10-13；PDF 标记 NeurIPS 2025 |
| 原始来源 | [版本页](https://arxiv.org/abs/2504.21776v2)、[锁定 PDF](https://arxiv.org/pdf/2504.21776v2)；访问 2026-10-28；身份页与 PDF 首页已核对 |
| Raw | [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf\|本地原件，共 41 页]] |
| SHA-256 | `FC359ACC58AE4074834AB2973DEF7AB799476E252F58D8BE642637442CFCAF03`；下载副本与归档后一致 |
| 实际阅读 | 2026-10-28；正文 pp.1–9；附录 A/B pp.17–19、C.3.2 及 C.4/D/E/F 的相关段落 pp.24–26；看原页 p.4 Fig.3、p.6 Table1、p.9 Table3。附录其余提示词与完整案例表未逐条核读，未审代码、未复现实验 |
| S001 入口 | [337]，§6.2.4，PDF p.59；本页以实际下载的 v2 为准 |
| 分类理由 | 既有深度浏览 harness，也训练研究工具使用策略；主归属保留 Agentic RL，应用分析重点为两者的对照 |

以下是原论文直接核读；解释性判断另标“本库推断”。页码为 PDF 页码，与正文印刷页码一致。

## 任务、环境与有效机制

它处理两类任务：一类需要边查外部知识边推理以得到短答案；另一类需要搜集材料后形成多节研究报告。主模型遇到知识缺口时调用 Deep Web Explorer；后者自行搜索、沿链接获取页面并返回与当前意图相关的摘要。报告模式把已访问页面保存在 document memory，助手模型检索相关页面来写节、修改报告；主模型负责何时搜、何时写、何时检查结构。这种分工把“新证据到来后更新哪一部分”变成可以执行的操作。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=4|§3.2–3.4／Fig.3 · pp.4–5]]

环境是 Bing Web Search API（US-EN，top-10）加 Crawl4AI 抓取的**文本网页**；不是完整浏览器 GUI，也不处理图片或视频。主问答过程初次获取 top-10 文档内容，Explorer 内部搜索返回标题、URL、片段，点击后再抓取并按意图压缩。主模型因此只能看到经搜索、抓取和摘要选择后的局部证据；“没理解已有信息”与“关键信息没被抓到或保留下来”不能仅由最终答错区分。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=7|§4.3 · p.7]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=17|附录 A · pp.17–18]]

**本库推断：**可观测性受网页访问与摘要接口共同限制；读取和追加搜索大体可重试，报告可以编辑，但论文没有测真实发布后的回滚、登录权限或外部写操作。反馈是网页内容和模型整理结果，没有运行时的答案 oracle。`check` 工具仅把标题／子标题形成的提纲返回给主模型，并非事实核验器；写作与编辑结果不全文回注主推理。结束依靠 EOS 或 token 上限，不是外部证明所有论点均正确。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=17|附录 A.1–A.2 · pp.17–18]]

## 哪些对照支持 model／harness 贡献

主实验骨干为 QwQ-32B，助手为同参数规模的 Qwen2.5-Instruct；生成上限 81,920 tokens。以下问答为 Pass@1，由 Qwen2.5-72B-Instruct 判断正确性；GAIA 只测 103 道纯文本验证题，WebWalkerQA 680 道测试题，GPQA diamond 198 题，HLE 随机 500 道纯文本题。不能当作全量 GAIA 或全部 HLE 排行。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=6|§4.1–4.3 · pp.6–7]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=18|附录 B · pp.18–19]]

| 对照 | 原文结果 | 支持与限制 |
| --- | --- | --- |
| QwQ-32B 固定骨干的流程比较 | WebWalkerQA：直接回答 4.3，标准 RAG 31.2，Iterative RAG 31.5，Search-o1 34.1，WebThinker-Base 41.9 | 不训练也有增益，支持外部探索／组织机制有用；各流程可用操作、调用量和实际计算不同，不能单独归因“自主” |
| Base → online DPO | GAIA 44.7→48.5；WebWalkerQA 41.9→46.5；HLE 13.0→15.8 | 固定框架的训练增益；未隔离每种偏好规则的贡献 |
| 去掉点击／整个 Explorer | 四项问答均值 45.4→42.6／38.3 | 支持深入页面和 Explorer 配置有作用；去模块同时改变信息可达性与计算，非纯推理能力消融 |
| 报告去自动分节写作／去检查编辑 | 报告四维均分 8.1→6.6／7.7；去检查编辑时 coherence 7.9→6.9 | 支持报告状态及迭代组织；不是引用真实性或实际研究完成度的验证 |

证据：[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=6|Table1 · p.6]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=7|Table2 · p.7]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|Table3 · p.9]]。Table3 的 RL 问答均值为 45.4，§4.7 文字另写 44.9，本页采用表格且保留该不一致；不使用摘要图中与 Table2 不一致的 Search-o1 HLE 数字。

报告评估仅 30 道 Glaive 问题，四维评分由 DeepSeek-R1-671B 和 GPT-4o 平均；训练与测试均从 Glaive 来源采样。Base→RL 的平均分只有 8.0→8.1，factuality 均为 7.7。尤其评审提示明确要求**不考虑文章引用**；因此不能从这个分数推出来源追溯已经解决，也不能把嵌入 t-SNE 分散程度当证据覆盖的独立测量。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=8|§4.5／Fig.4 · p.8]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=19|附录 B.2 · p.19]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=24|附录 C.3.2 · p.24]]

## 训练内化了什么，没有证明什么

在线 DPO 对同题自采样轨迹构造偏好：首先选正确答案／更好报告，其次在都正确时选更少工具调用，调用相同再按长度阈值选更短推理。更新后重新采样、再构造偏好，两轮训练、最大训练序列 32,768。目标是改善**带工具的决策策略**，不是把网页事实全部背入参数。模型仍需调用 Explorer、保留文档、使用写作助手。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=5|§3.5 · pp.5–7]]

**本库推断：**规则确实偏好少调用，但本次核读的实验没有给出训练后实际调用量下降的统计，不能据此断言训练已经减少外部流程。跨 DeepSeek-R1 7B／14B／32B 的适配还使用了 7.8k QwQ 轨迹冷启动 SFT 和 RL，因此是“框架加再训练可适配”的证据，不是零训练换骨干的迁移。训练数据含 WebWalkerQA Silver、SuperGPQA 等多个来源；与同源测试的关系不能简化为完全跨分布泛化。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|§4.6 · p.9]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=19|附录 B · p.19]]

## 对应用理解的改变与边界

原有问题“没有可执行正确性检查时如何进展”可拆为：搜索揭露新内容、摘要与文档记忆保留可用证据、主模型判断知识缺口、报告工具维护输出结构。这些环节能提高指定任务分数；它们未把开放网页变成可信 oracle。当前证据把瓶颈定位在**模型判断与证据接口的耦合**，还不足以把剩余错误主要归入“理解差”或“检索差”。权限、恶意网页、抓取失败、引用审计和完整成本匹配在本次核读范围内没有相应受控结果。作者也明确列出多模态、工具范围与 GUI 访问限制。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|§5 · p.9]]

应用整合入口：[[wiki/applications/Overview|Application]]；形成记录：[[组会/2026-10-28-Application/过程/B-检索与多模态|B：检索与多模态]]。已整合至 [[wiki/applications/success-mechanisms|应用成功机制与瓶颈]]；主Agent已完成内容与结构检查，Obsidian内显示未测。
