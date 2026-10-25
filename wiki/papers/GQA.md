---
type: paper
source_id: S035
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/GQA.pdf]]"
reading_status: 正文与附录已读
ingest_status: complete
---

# GQA：共享 KV 头，降低解码读取成本

> [!abstract] 核心理解
> GQA 保留多个 query 头，但让一组 query 共用 key/value 头，在 MHA 与 MQA 之间选择资源与质量的折中。它减少每个时间位置存储的 KV 头数量，**没有把时间历史压成固定大小状态，也没有删除某些历史位置**。论文主要验证 T5 encoder–decoder 的生成任务与推理效率，不是长期 Agent 的任务成功率。[[raw/papers/GQA.pdf#page=2|S035 · §2.2、Fig.2 · PDF p.2 / 印刷 p.4896]] [[raw/papers/GQA.pdf#page=3|§3.1–3.2、Table 1 · PDF p.3 / 印刷 p.4897]]

## 身份与读取边界

| 项目 | 记录 |
| --- | --- |
| 标题 | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints |
| 作者 | Joshua Ainslie、James Lee-Thorp、Michiel de Jong、Yury Zemlyanskiy、Federico Lebrón、Sumit Sanghai |
| 版本与标识 | EMNLP 2023 会议正式 PDF；DOI `10.18653/v1/2023.emnlp-main.298`；PDF 7 页，对应印刷 pp.4895–4901 |
| 原始来源 | [ACL Anthology](https://aclanthology.org/2023.emnlp-main.298/)；[本次 PDF](https://aclanthology.org/2023.emnlp-main.298.pdf)，访问 2026-10-25 |
| 原件 | [[raw/papers/GQA.pdf\|GQA.pdf]] |
| SHA-256 | `C52DE1D3339174FBF93B588AA4CC9BF36092C865F2358ECE3999DE152F57455C` |
| 读取日期与范围 | 2026-10-25；PDF pp.1–7，正文、局限、附录 A 与参考文献文本；未逐篇读取被引原论文，未复现实验 |
| 图表核验 | 渲染并查看 PDF p.2 Fig.2、p.3 Table 1 与 Fig.3；表/图时间单位标注不一致，见下文 |
| 综述来源 | [[wiki/papers/Towards Long-Horizon Agents\|S001]] ref.[5]，§5.1.4 PDF p.40；参考文献 p.76 |
| 整合状态 | 已整合至 [[wiki/optimization/Overview#架构基础\|Optimization 架构基础]]；内容与结构已验收，应用未测 |

## 为什么 query 多、KV 少可以节省成本

自回归解码的每一步都需要访问过去位置的 key/value。MHA 为各注意力头保存各自 KV；当历史变长，加载缓存的带宽成为开销。GQA 把 query 头分组，每组共用一套 KV，使缓存中每个历史位置的头数从 $H$ 下降到 $G$，但 query 头数维持 $H$。[[raw/papers/GQA.pdf#page=1|S035 · §1 · PDF p.1 / 印刷 p.4895]] [[raw/papers/GQA.pdf#page=2|§2.2、Fig.2 · PDF p.2 / 印刷 p.4896]]

| 形式 | Query 头 | KV 头 | 时间位置 |
| --- | --- | --- | --- |
| MHA | H | H | 保留 |
| GQA | H | G（1 < G < H） | 保留 |
| MQA | H | 1 | 保留 |

这是头维度的共享。按相同序列长度与每头维度比较，KV 缓存随 KV 头数量减少；缓存仍随序列长度增长。不能从这个机制推导无限上下文或无损保存全部任务语义。[[raw/papers/GQA.pdf#page=2|S035 · §2.2、Fig.2 · PDF p.2 / 印刷 p.4896]]

## 如何把已有 MHA 模型转换过来

作者先将每组 MHA key/value 投影做 mean pooling，初始化共享 KV 投影，再使用原预训练配方继续训练，让模型适应改变后的结构。论文将这一步称作 uptraining；不是只改推理配置便能取得全部质量结果。实验采用原预训练步骤的 5%，并用更多/更少训练量作消融。[[raw/papers/GQA.pdf#page=1|S035 · §2.1 · PDF pp.1–2 / 印刷 pp.4895–4896]] [[raw/papers/GQA.pdf#page=4|§3.3、Fig.4–6 · PDF p.4 / 印刷 p.4898]]

组数提供资源选择：更少 KV 组通常降低缓存与读取成本，但表示共享程度更强；本文在测试范围内选择 GQA-8 作为有利折中。这个数依赖模型与部署设置，不能推广为所有模型的最佳组数。[[raw/papers/GQA.pdf#page=4|S035 · §3.3、Fig.6 · PDF p.4 / 印刷 p.4898]]

## 实验条件及支持范围

主体实验基于 T5.1.1 Large/XXL，改动 **decoder self-attention 与 cross-attention**，encoder self-attention 仍为 MHA。任务包括 CNN/Daily Mail、arXiv、PubMed、MediaSum、MultiNews 摘要，WMT 翻译与 TriviaQA。输入最长设置为 2048 token，采用 greedy decoding；它不是百万 token 长上下文测试。[[raw/papers/GQA.pdf#page=2|S035 · §3.1 · PDF pp.2–3 / 印刷 pp.4896–4897]]

Table 1 中 T5-XXL 的 MHA、GQA-8、MQA 平均质量分数分别为 47.2、47.1、46.6。这里平均了 ROUGE-1、BLEU、F1 等不同任务的指标；适合描述作者的整体质量比较，不等于可解释为百分比的统一“任务成功率”。结合时间测试，作者认为 GQA 在其设置下接近 MHA 质量、接近 MQA 速度。[[raw/papers/GQA.pdf#page=3|S035 · §3.2、Table 1 · PDF p.3 / 印刷 p.4897]]

计时在 8 个 TPUv4 芯片上测量，对各模型选择最大可用批量（每 TPU 上限 32）与优化的分片。因此它反映这种硬件与配置下的部署表现，不是所有模型在完全相同 batch 下的单请求延迟。Table 1 时间列标为秒，而 Fig.3 横轴标为毫秒，存在单位标注不一致；本页不据此抄录绝对耗时或计算绝对速度承诺。[[raw/papers/GQA.pdf#page=3|S035 · §3.1–3.2、Table 1、Fig.3 · PDF p.3 / 印刷 p.4897]]

## 限制及与长期 Agent 的关系

作者明确指出只测试 encoder–decoder，没有完成 XXL 从头训练的对照；对 decoder-only 的收益是预期。长文本摘要的 ROUGE 也不是完整质量评估。附录 A 还报告 MQA 的部分训练不稳定，GQA 在作者实验中更稳定，但原因未系统研究。[[raw/papers/GQA.pdf#page=5|S035 · Limitations · PDF p.5 / 印刷 p.4899]] [[raw/papers/GQA.pdf#page=7|Appendix A · PDF p.7 / 印刷 p.4901]]

**本库推断：**较低的 KV 成本可能使固定资源下的长上下文执行更可行，但不自动提升对远处信息的检索与使用，也不提供跨上下文迁移、规划或错误恢复机制。要讨论 Agent 收益，应把模型解码成本与检索质量、工具等待和完整任务指标分开测量。当前本文只能直接支撑前者的部分设置。

**最近工作与查新状态：**MQA、T5 等相关比较来自本文；本批没有逐篇核读其原论文，不把作者背景描述当作独立复核。暂不提出新颖性主张或强制生成研究 idea。

## 主题联系

相关入口为 [[wiki/optimization/Overview#架构基础|Optimization：Architecture Design / computational efficiency]]。已整合 KV 头共享和时间状态压缩的区别，以及效率与长程信息使用效果应分别举证；内容与结构已验收。Obsidian 应用渲染、公式及跳转未测。
