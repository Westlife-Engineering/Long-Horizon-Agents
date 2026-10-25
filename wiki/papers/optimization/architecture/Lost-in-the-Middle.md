---
type: paper
primary_direction: optimization/architecture
related_directions:
  - harness/memory
source_id: S036
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf]]"
reading_status: 正文与实验附录已读
ingest_status: complete
---

# Lost in the Middle：容得下上下文，仍可能用不好中间的信息

> [!abstract] 核心理解
> 这是一项诊断研究。作者保持答案内容不变，移动证据的位置或增加干扰，观察模型是否仍能找到并使用它。在所测试的 2023 年模型与任务中，位置常显著影响结果；更长的标称窗口并不自动带来更稳健的信息使用。但 U 形曲线有任务和模型例外，不能当成所有模型、所有长度下的普遍定律。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=3|S036 · §2 · pp.3–5]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=6|§3 · pp.6–7]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=16|Appendix E · p.16]]

## 身份与读取边界

| 项目 | 记录 |
| --- | --- |
| 标题 | Lost in the Middle: How Language Models Use Long Contexts |
| 作者 | Nelson F. Liu、Kevin Lin、John Hewitt、Ashwin Paranjape、Michele Bevilacqua、Fabio Petroni、Percy Liang |
| 锁定版本 | arXiv:2307.03172v3，2023-11-20；PDF 18 页。S001 引用 TACL 2024 版本；本地读的是 arXiv v3，未与期刊 PDF 逐字节/逐项对齐 |
| 原始来源 | [arXiv 版本页](https://arxiv.org/abs/2307.03172v3)；[本次 PDF](https://arxiv.org/pdf/2307.03172v3)，访问 2026-10-25 |
| 原件 | [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf\|Lost-in-the-Middle.pdf]] |
| SHA-256 | `653B29619EAE2AE4B361D7BDCDC06DB4BEDCB1B0EABE31814036BECA8C1AF0B1` |
| 读取日期与范围 | 2026-10-25；正文 pp.1–11、实验附录 pp.14–18；参考文献未逐篇核读；未运行模型或复现 |
| 图表核验 | 实际渲染查看 p.5 Fig.5/Table 1，p.7 Fig.7，p.8 Figs.8–9，p.18 Tables 5–7 |
| 综述来源 | [[wiki/surveys/Towards Long-Horizon Agents\|S001]] ref.[378]，§5.1.1 / §5.1.3 PDF pp.38、40；参考文献 p.106 |
| 整合状态 | 已整合至 [[wiki/optimization/architecture\|Optimization 架构基础]] 与 [[wiki/harness/memory\|Harness 上下文与记忆]]；内容与结构已验收，应用未测 |

## 实验怎样隔离“证据位置”

论文没有提出一个新的长上下文架构，而是设计两类可控输入。固定内容后重新排序，比单独测最大窗口长度更能观察模型是否真正使用不同位置的信息。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=3|S036 · §2.1 · pp.3–4、Figs.2–4]]

| 测试 | 固定什么 | 改变什么 | 评测什么 |
| --- | --- | --- | --- |
| 多文档 QA | 问题和含答案的文档；使用 NaturalQuestions-Open 中 2655 个长答案为段落的查询 | 含答案文档在 10/20/30 份文档中的位置；其余为检索到但不含标注答案的干扰 | 生成内容是否含任何一个标注正确答案 |
| 合成 KV 检索 | 要找的 key/value，均为随机 UUID | 对应 pair 的位置；75/140/300 对 KV，分别 500 样例 | 输出是否包含对应 value |

定位：[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=3|S036 · §2.1 · p.3]]、[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=6|§3.1–3.2 · p.6、Fig.6]]。前者理想设计恰有一份含答案文档，但数据歧义可能让其他文档也有合理答案；作者对无歧义子集作了复核，结果趋势相似。它不能被描述为已经彻底排除所有语义歧义。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=14|Appendix A · p.14]]

```mermaid
flowchart LR
    Q[相同问题与证据内容] --> P[移动证据位置]
    Q --> D[增加干扰文档]
    P --> M[固定模型与提示配方运行]
    D --> M
    M --> R[比较回答准确率]
```

本库示意图表示评测控制，不是模型内部的因果机制证明。本文使用 greedy decoding 和既定提示；改变位置后准确率变化是行为观察，并未唯一定位到某个注意力头或训练机制。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=4|S036 · §2.2 · pp.4–5]]

## 主要发现及例外

**位置会改变结果。** 例如 20 文档设置中，GPT-3.5-Turbo-0613 的正确率从证据位于第 1 份时的 75.8%，下降到第 10 份的 53.8%，到第 20 份又为 63.2%。这分别是相差 22.0 和 9.4 个百分点，不应模糊写成“下降 22%”。这组具体结果只描述当时模型、数据与 prompt；不能直接套在今天的模型上。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=18|S036 · Appendix G.2、Table 6 · p.18]]

**可接受长度与有效使用分开。** 在相同输入同时装得下普通与扩展窗口版本时，部分版本的曲线几乎重合。这否定的是“扩大窗口必然改善共同范围内信息使用”的自动推论，不是否定扩展窗口对原来装不下的输入有价值。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=5|S036 · §2.3、Fig.5 · pp.5–6]]

**U 形不是普适现象。** Claude-1.3 系列在 UUID KV 检索上近乎完美，却在多文档 QA 上仍有位置效应；Llama-2 7B 主要呈近因偏好，13B/70B 才出现明显首尾偏好。LongChat 某些失败还涉及输出代码而非直接返回 value。不能把所有错误统一称为“记忆丢失”。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=6|S036 · §3.2、Fig.7 · pp.6–7]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=16|Appendix E、Fig.16 · p.16]]

## 哪些解释得到测试，哪些仍是猜测

1. **把 query 同时放在数据前后。** 作者称为 query-aware contextualization；它使测试中的合成 KV 任务接近完美，但没有同样消除多文档 QA 的位置趋势。因此“先告诉模型要找什么”对该简单检索任务有证据，对语义 QA 不是已验证通用修复。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=8|S036 · §4.2、Fig.9 · p.8]]
2. **Encoder–decoder 与训练长度。** Flan-UL2 在训练期长度范围内相对稳健，超出该范围后出现中间退化；作者关于双向 encoder 更好估计文档重要性的解释是机制假说。模型间还存在训练与规模差异，不能把结果解释成单独改变架构的充分因果证明。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=7|S036 · §4.1、Fig.8 · pp.7–8]]
3. **是否由 instruction tuning 引起。** MPT base 和 instruct 都出现位置趋势，后训练可改变绝对分数和差距，但不是唯一来源。该结果没有证明所有训练方法都无法解决位置问题。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=8|S036 · §4.3、Fig.10 · pp.8–9]]
4. **是否只是检索排序先验或困难负例。** 随机干扰、打乱干扰顺序并在 prompt 说明随机排列后，位置趋势仍存在，削弱了这些因素作为唯一解释的说法。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=14|S036 · Appendices B–C、Figs.13–14 · pp.14–15]]

## Harness 与 Optimization 为什么需要共同看这篇

§5 将模型放入 Contriever→文档拼接→回答的开放域 QA 流程。与控制实验不同，此时 top-k 中可能没有答案或多份文档都有答案。随着检索文档数增加，retriever recall 继续增长，而 reader accuracy 较早趋于饱和。这说明“把更多相关材料送入上下文”与“模型用好了它们”需要两类证据。作者提出 reranking/截断作为可能方向，但本文没有据此验证一个普遍最优的上下文编排方法。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=9|S036 · §5、Fig.11 · pp.9–10]]

**本库推断：**对于 [[wiki/papers/optimization/architecture/Longformer|Longformer]]、[[wiki/papers/optimization/architecture/Mamba|Mamba]] 与 [[wiki/papers/optimization/architecture/Kimi-Linear|Kimi Linear]]，结构允许信息流动或压缩状态可持续更新，只能回答机制与成本的一部分；信息能否恢复仍应使用合适任务检验。本文没有实测后两者，也没有提供它们的排名或直接反例。对于 [[wiki/papers/optimization/architecture/GQA|GQA]]，降低 KV 带宽不能替代这个信息使用检查。

**待检验阅读问题：**将类似的位置控制用于 Agent 的约束、工具结果与旧错误，会观察到怎样的行为？真正 Agent 历史有时序依赖，任意重排可能改变任务含义；需要先构造语义保持的变换，不能照搬文档洗牌后声称在测同一任务。该问题尚未查新，不能把位置效应本身重新命名为新发现。

## 局限与主题联系

模型和 API 版本锁在论文测试时期（GPT 使用 0613 系列）；两项主要任务都以答案字符串包含作为指标，并非完整推理质量、人类评价或多轮行动成功。模型的 tokenization 不同，图中的约 4K/8K/16K 是粗略标签，精确输入计数见 Appendix F，不能假定所有模型都运行相同 token 数或全部长度。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=4|S036 · §2.2 · pp.4–5]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=6|§3.1 · p.6]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=17|Appendix F、Tables 2–4 · p.17]]

相关入口：[[wiki/optimization/architecture|Optimization：架构基础的有效上下文边界]]、[[wiki/harness/memory|Harness：上下文编排与证据选择]]。前者需要区分可运行长度、检索行为与下游任务，后者需要区分检索召回与 reader 使用。共享整合完成、内容与结构已验收；Obsidian 渲染与跳转未测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/architecture|optimization/architecture]] · [[wiki/harness/memory|harness/memory]]。
