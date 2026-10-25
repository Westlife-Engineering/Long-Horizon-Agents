---
type: paper
primary_direction: harness/memory
source_id: S010
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/harness/memory/ExpeL.pdf]]"
reading_status: 方法与主要实验核读，附录选读
ingest_status: complete
---

# ExpeL：把多次任务经验转为规则和示例

ExpeL 的学习发生在模型参数之外：先通过训练任务中的成功、失败与重试收集轨迹，再把经验归纳成自然语言 insights；遇到新任务时，给策略模型同时提供规则和相似成功轨迹。**不更新模型权重，不等于没有训练任务、反馈或经验收集成本。**[[raw/papers/harness/memory/ExpeL.pdf#page=3|S010 · §4、Figure 1 · pp.3–6]]

## 身份与阅读范围

| 项目 | 登记 |
| --- | --- |
| 标题 | ExpeL: LLM Agents Are Experiential Learners |
| 作者 | Andrew Zhao、Daniel Huang、Quentin Xu、Matthieu Lin、Yong-Jin Liu、Gao Huang |
| 版本 | arXiv:2308.10144v3，2024-12-20；原始页面标注 AAAI 2024；38 页 |
| 原始来源 | [arXiv](https://arxiv.org/abs/2308.10144)；[v3 PDF](https://arxiv.org/pdf/2308.10144v3)，访问 2026-10-25 |
| Raw | [[raw/papers/harness/memory/ExpeL.pdf\|ExpeL.pdf]] |
| SHA-256 | `01E533D81FB4A5F91797C073A9B1929ACBAA64DA45A592B26563CA7D135024F3` |
| 实际阅读 | 2026-10-25；p.1 摘要，pp.2–10 正文，pp.14–15 任务与超参数；实际查看 p.3 Figure 1、p.8 Figure 5、p.10 Table 3；完整提示和轨迹案例附录未逐项核读，未复现 |
| 综述入口 | S001 §4.2.2 / Table 3，pp.25–26；参考文献 [853]（p.144） |

## 经验怎样影响下一次执行

```mermaid
flowchart LR
    A[训练任务与成功失败反馈] --> B[ReAct执行 失败后Reflexion重试]
    B --> C[保存成功与失败轨迹]
    C --> D[同任务成败对比 跨任务成功归纳]
    D --> E[更新自然语言规则及计数]
    C --> F[按新任务相似度取成功轨迹]
    E --> G[新任务提示：规则加示例]
    F --> G
    G --> H[策略执行一次测试任务]
```

本库机制示意，依据 §4、Figure 1。经验收集阶段允许失败后重试，归纳阶段分别使用同任务的成败对和多个任务的成功集合。规则更新允许 ADD、EDIT、UPVOTE、DOWNVOTE：新规则计数为 2，支持或修改使计数增加，反对减少，降到零移除。计数表示归纳流程的保留机制，**不是独立实验证据数或真实性概率**。[[raw/papers/harness/memory/ExpeL.pdf#page=4|§4.1–4.2 · pp.4–5]]

执行新任务时，使用任务相似度检索成功轨迹作为 few-shot 示例；规则列表直接加入提示。本文实现没有为规则列表本身设计无限增长下的检索机制，作者将这一点列为终身学习时的后续需求。[[raw/papers/harness/memory/ExpeL.pdf#page=5|§4.3 · pp.5–6]] [[raw/papers/harness/memory/ExpeL.pdf#page=10|§6 Limitations · p.10]]

经验提炼使用 GPT-4-0613，策略评估使用 GPT-3.5-turbo-0613；Faiss/kNN 与 all-mpnet-base-v2 用于示例检索。因此增益也利用了更强模型在离线归纳阶段的能力。作者在迁移实验使用的“finetune insights”是根据目标任务示例重写文字规则，不是参数微调。[[raw/papers/harness/memory/ExpeL.pdf#page=8|§5.4 · pp.8–9]] [[raw/papers/harness/memory/ExpeL.pdf#page=15|附录 D.5、E / Table 4 · p.15]]

## 任务、反馈与主要证据

主实验为 HotpotQA、ALFWorld、WebShop，使用任务成功率；迁移从 HotpotQA 到 FEVER。正文以确定性环境建模，附录还将 WebShop 的价格随机性固定，并把每页商品数由 3 改为 10。经验生成可重试、能辨认成功失败，是成败比较的前提；这与开放世界中没有可靠终局反馈的情况不同。[[raw/papers/harness/memory/ExpeL.pdf#page=2|§3 · p.2]] [[raw/papers/harness/memory/ExpeL.pdf#page=14|附录 D.1–D.3 · p.14]]

评估跨任务泛化时通常一次尝试，不能与收集经验时的重试次数混为一谈。Figure 5 中完整 ExpeL 在三任务优于对应 ReAct，且同时使用规则与示例优于各自单用；但 rules-only 与 retrieve-only 的相对表现依任务而异。例如 HotpotQA 更受益于规则，ALFWorld 更受益于示例。论文另有把 Reflexion 重试加回评估的补充实验，须单列其额外尝试预算。[[raw/papers/harness/memory/ExpeL.pdf#page=7|§5.1–5.2 · pp.7–8]] [[raw/papers/harness/memory/ExpeL.pdf#page=9|§5.5、Table 2 · p.9]]

附录 Table 4 给出 HotpotQA / WebShop / ALFWorld 最大行动步数分别 7 / 15 / 20，最多检索示例分别 6 / 2 / 2，经验阶段最多反思重试 3 次。这里更直接支持跨任务经验复用，而非超长单次上下文不断接续。[[raw/papers/harness/memory/ExpeL.pdf#page=15|附录 E、Table 4 · p.15]]

Table 3 表明把反思文本也加到经验提炼输入中反而降低 HotpotQA 表现；作者推测原因是反思可能出现幻觉。这一原因未被独立证明，但结果足以反对“更多自我反思必然更好”。换较弱的 insight 模型也会减益；因此经验质量和归纳模型均属重要条件。[[raw/papers/harness/memory/ExpeL.pdf#page=9|§5.6 · pp.9–10、Table 3]]

## 对当前探索的意义

**本库推断：**应区分保存过去发生了什么（轨迹）与保存今后建议怎样做（规则）；后者是经过模型解释的经验，不应与原始观察具有同样的证据身份。ExpeL 的规则计数、成功失败配对和任务相似检索提供了具体可比较机制，但不能证明经验归纳不会过度推广。

**待检验问题：**一条规则在新任务中不适用时，应依据任务条件限制其使用，还是依据后续失败撤销？本文展示跨任务与跨任务类型迁移，但本次所读证据未系统区分规则冲突与适用范围错误。这是候选阅读问题，未做充分查新，不认定为新颖缺口。

作者局限包括文本观察、闭源模型以及规则将来超出上下文时的扩展问题。[[raw/papers/harness/memory/ExpeL.pdf#page=10|§6 · p.10]]

## 主题联系与整合状态

已整合 [[wiki/harness/memory|Harness：上下文与记忆]]：跨任务持久经验与自然语言策略规则，与 [[wiki/papers/harness/memory/HiAgent|HiAgent]] 的单次任务工作记忆分开。与 [[wiki/optimization/Overview|Optimization]] 的概念联系是本文没有梯度更新，但存在训练任务划分与离线经验阶段；本批未在 Optimization 单独加入 ExpeL 综合。主题与索引已同步，内容与结构验收通过；Obsidian 未测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/memory|harness/memory]]。
