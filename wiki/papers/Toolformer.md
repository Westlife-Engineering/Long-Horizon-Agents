---
type: paper
source_id: S012
created: 2026-10-25
updated: 2026-10-25
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/Toolformer.pdf]]"
  - "[[raw/papers/Toolformer-supplement.pdf]]"
---

# Toolformer：把工具调用学进语言模型

Toolformer 解决的是**怎样用少量接口示例生成训练数据，让模型学会何时调用工具**。它提供了工具使用的自监督训练机制，但本文主实验每个输入最多调用一次 API，不能作为多步工具链已经可靠的证据。[[raw/papers/Toolformer.pdf#page=3|§2 · pp.3–4]] [[raw/papers/Toolformer.pdf#page=6|§4.2 · p.6]]

## 来源与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID / 标题 | S012 / Toolformer: Language Models Can Teach Themselves to Use Tools |
| 作者 | Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom |
| 版本 | NeurIPS 2023 正式版；主文 13 页、独立补充材料 10 页。正式版含 Eric Hambro，不能直接套用 arXiv v1 的作者列表 |
| 原始发布与访问 | [NeurIPS 发布页](https://papers.nips.cc/paper_files/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html)；2026-10-25 |
| 主文 / SHA-256 | [[raw/papers/Toolformer.pdf\|主文]]；`391845B5F4F7F5E7C04A34E5280F031C17A5FBF868F53E1C5AF3E25B0179FB1C` |
| 补充材料 / SHA-256 | [[raw/papers/Toolformer-supplement.pdf\|独立补充 PDF]]；`A54B40A9E52CFE260FDAB898F5F59AFC8A571C59EE5F479152AF4ECED46D0502` |
| 原始文件关系 | 发布页 Paper / Supplemental 分别原样归档为以上两个文件；同一论文、同一来源 ID |
| 读取 | 2026-10-25；主文 §§1–7（pp.1–10），补充 A–G（pp.1–9）；参考文献未逐项核验。已看主文 Fig.2、筛选公式、Tables 3–5 和补充 Tables 7–8 原页图像 |
| 页码 | 两个 PDF 各自从第一页计数，页脚印刷页码与各自 PDF 页码一致；补充材料不接续主文页码 |
| S001 选文定位 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=27\|§4.3.1 · p.27 · 引文523]]；书目 p.118 |

## 训练时筛什么，运行时执行什么

核心不是让人工为每个任务演示整条工具轨迹，而是在普通语料中提出候选调用，再检查工具结果能否帮助预测原文后续 token。保留的调用插入原文本，成为语言建模微调数据。[[raw/papers/Toolformer.pdf#page=2|§2 · Fig.2 · pp.2–4]]

```mermaid
flowchart LR
  T[普通文本与少量接口示例] -->|采样位置和参数| C[候选 API 调用]
  C -->|执行| R[工具结果]
  R -->|比较后续 token 损失| F[保留有预测收益的调用]
  F -->|插回文本并微调| M[更新后的模型参数]
  M -->|运行时生成调用标记| E[暂停解码并执行 API]
  E -->|插入返回文本| D[继续生成]
```

本图为本库按原文重绘的机制示意，左侧是离线训练数据构造，右侧是推理时接口执行；箭头不表示任务成功保证。

筛选比较 $L_i^+=L_i(e(c_i,r_i))$ 与 $L_i^-=\min\{L_i(\epsilon),L_i(e(c_i,\epsilon))\}$，仅保留 $L_i^- - L_i^+\ge\tau_f$ 的调用。也就是说，有结果的调用必须优于“完全不调用”和“只给调用输入、不给结果”中较好的一个，避免仅靠问题文字降低损失。这里衡量的是**后续文本可预测性**，不是任务完成、安全性或工具成本。[[raw/papers/Toolformer.pdf#page=3|§2 · 筛选公式 · p.3]] [[raw/papers/Toolformer.pdf#page=9|§6 · p.9]]

输入输出须能序列化为文本，工具用法须有少量示例；使用 QA、Wikipedia 搜索、计算器、翻译和日历。构造数据还依赖工具特定启发式筛选，故“自监督”不等于没有人工设计。补充材料说明 QA 数据生成用 Atlas-large，推理用 Atlas-xxl，模型表现包含外部工具能力。[[raw/papers/Toolformer.pdf#page=4|§3 · pp.4–5]] [[raw/papers/Toolformer-supplement.pdf#page=1|补充 A.1 · p.1]]

## 实验实际支持到哪里

主实验以 GPT-J 和 CCNet 子集训练，比较原模型、仅继续训练 CCNet、Toolformer 禁用工具和启用工具。补充 B 给出每 API 最多 25k 样本、1024 序列长度、最多 2000 步、8 张 A100 40GB 的训练条件。下游采用 prompted zero-shot；推理将 API 起始符进入 top-10 即触发，并限制每输入最多一次 API 调用。这是运行控制条件，不能只把结果解释为模型自然贪心解码下的调用选择。[[raw/papers/Toolformer.pdf#page=5|§4.1–4.2 · pp.5–6]] [[raw/papers/Toolformer-supplement.pdf#page=3|补充 B · p.3]]

| 证据 | 支持与边界 |
| --- | --- |
| LAMA 与算术 | 同 GPT-J 的启用/禁用工具比较支持外部工具有贡献；LAMA 禁用 Wikipedia Search，QA 任务禁用 QA 工具，且成功判据比严格 exact match 宽松。[[raw/papers/Toolformer.pdf#page=6\|Table 3、§4.2 · p.6]] |
| QA 与多语言 QA | QA 仍落后于该文 GPT-3 基线；多语言并非一致优于原 GPT-J，CCNet 继续训练会损害部分语言表现。[[raw/papers/Toolformer.pdf#page=7\|Tables 4–5 · p.7]] |
| 语言建模 | 只在禁用调用时测 WikiText / CCNet perplexity，不能扩大成所有通用能力均无损。[[raw/papers/Toolformer.pdf#page=8\|§4.3 · p.8]] |
| 更强基础模型 | LLaMA 实验中强 QA 工具有益，而 WikiSearch 相对同一微调模型禁用工具时反而下降；工具效用依赖模型原有能力和返回内容质量。[[raw/papers/Toolformer-supplement.pdf#page=9\|补充 G · Tables 7–8 · pp.7–9]] |

## 对长程工具使用的意义与限制

**原文陈述：**独立生成各工具调用，使训练数据没有链式工具依赖；本文不能学习把一个工具输出交给下一个工具，也未实现交互式搜索修订。作者另列调用敏感于措辞、稀疏有效样本和未计工具成本等限制。[[raw/papers/Toolformer.pdf#page=9|§6 · p.9]]

**本库推断：**它将“接口存在”推进到“参数学到何时使用接口”，但短程 token 损失代理不自动解决跨步骤依赖。将其放入 Harness 分类时应同时标出训练侧变化，而不是归为纯运行时提示方法。适合在 [[wiki/harness/Overview#工具、MCP 与技能|工具、MCP 与技能]] 和 [[wiki/optimization/Overview|模型优化]] 中讨论工具表面、数据构造与策略能力的接口。

作者把 TALM 视为接近工作，差异是其任务特定微调设置；这是作者比较，本次未独立核读 TALM，不据此确认新颖性或跨工作优劣。[[raw/papers/Toolformer.pdf#page=9|§5 · p.9]]

**待检验问题：**短程预测收益筛选在有状态、多工具依赖任务上是否保留了有长期作用但即时信息收益较低的调用？当前是机制外推问题，尚未完成查新，不记作已成立研究缺口。

## 整合与验收状态

已整合至 [[wiki/harness/Overview#工具、MCP 与技能|Harness 工具方向]] 与 [[wiki/optimization/Overview#微调|微调的工具接口]]，内容与结构验收通过。未复现实验，Obsidian 图表、公式及来源跳转尚未实测。
