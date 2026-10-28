---
type: paper
source_id: S079
primary_direction: optimization/finetuning
related_directions:
  - optimization/reinforcement-learning
created: 2026-10-28
updated: 2026-10-28
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf]]"
---

# 推理SFT的泛化：优化、数据与底座共同决定条件

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S079 |
| 原文标题 | Rethinking Generalization in Reasoning SFT: A Conditional Analysis on Optimization, Data, and Model Capability |
| 作者 | Qihan Ren、Peng Wang、Ruikun Cai、Shuai Shao、Dadi Guo、Yuejin Xie、Yafu Li、Quanshi Zhang、Xia Hu、Jing Shao、Dongrui Liu |
| 版本 | arXiv:2604.06628v2，2026-08-15；PDF标记 Published as a conference paper at COLM 2026 |
| 原始来源 | [固定版本 PDF](https://arxiv.org/pdf/2604.06628v2)；[官方身份页](https://arxiv.org/abs/2604.06628v2)；访问／本轮读取日期 2026-10-28；PDF首页版本已核对，DOI未确认 |
| Raw | [[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf\|本地原件，48页]] |
| SHA-256 | `23C8527985B7E0960C011BDE148E1EA3182DFFBBB1BED27721710C9FA00BC37F` |
| 实际读取 | 正文pp.1–10；p.17 Appendix A及B.1开头；pp.35–36 C.12–C.15（含Table12提示词线索、Table13–17）。查看p.4 Fig.2–3、p.7 Table2、p.8 Fig.5、p.36 Tables14–17原页图像。其他附录完整训练曲线、全部逐条案例、实现与数据未核读；未复现实验 |
| 选择理由 | [[组会/2026-10-28-Optimization-RL/README\|Optimization-RL组会]] 的争议补读2：检查“SFT只记忆、不泛化”的过强前提 |
| 当前状态 | 已完成内容整合；原件、结构与应用验收分开记录，Obsidian未测 |

## 它改变了什么问题

**原文问题。** 作者研究标准SFT目标在长CoT推理监督下何时跨域迁移；不是设计新的SFT损失。主实验从预训练底座开始，改变训练时程、轨迹数据和模型能力，再分别测数学、域外推理、一般能力与安全性。这个设计允许检验“早期不泛化是否只是尚未学好”，而非把一次检查点的结果当成训练目标固有限制。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=2|§1–2 · pp.2–3]]

**实验条件。** 默认Math-CoT-20k含20,480道数学题，Qwen3-32B生成长CoT并用答案验证筛选；最大训练响应16,384 tokens。主底座为Qwen3-14B／8B，另含InternLM2.5及Qwen2.5等；默认AdamW、学习率5e-5、batch256、cosine调度、8 epochs。评估温度0.6、生成上限32,768；不同基准报告pass@1或多次独立采样的平均分，而非统一的大k覆盖。域外推理包括LiveCodeBench v2、GPQA-Diamond、MMLU-Pro，尚不是工具环境迁移。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=3|§2 · pp.3–4]]

## 三组条件证据，不能缩成“多训就好”

1. **优化阶段会改变观察到的泛化。** 所测多组模型在长CoT SFT早期出现性能下降、响应变长，继续训练后部分域外指标回升并超过底座。作者将“先学表面冗长、再学有效过程”作为解释；响应长度及规则词检测属于行为线索，不是参数层面的机制证明。更激进的学习率和时程仍可导致退化，所以结果不支持无限延长训练。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=4|§3.1–3.4、Fig.3–4 · pp.4–6]]
2. **轨迹质量与结构影响迁移。** Table2比较同题长CoT、删除thinking段的短解、NuminaMath解及Countdown长CoT；高质量长CoT在若干推理指标上更好，但一般指令指标不总占优。Countdown训练后在Qwen3上有数学和域外推理收益，也有IFEval退化；其窄任务来源支持“可迁移过程”解释，却未直接识别某一种抽象算法。原文NoCoT仍保留逐步总结和答案，不应误写为只有最终答案。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=6|§4、Table2 · pp.6–7]]
3. **底座能力与监督有交互。** 同数据／协议下，Qwen3-14B、8B、4B与1.7B的迁移和响应长度不同；弱模型可能只有有限或负收益。作者强调能力不等于参数数目，还涉及预训练和中期训练得到的表示与知识。这里只是受控案例，不是对所有模型设定一个容量阈值。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=8|§5、Fig.5及脚注 · p.8]] [[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=35|C.12–C.13 · p.35]]

**本库归纳。** 这些结果足以反对“SFT必然不能跨域泛化”，支持将问题改成“什么底座在何种数据与优化预算下会迁移”。它没有证明所有SFT都能泛化，也没有将数学到代码／科学问答的迁移转换成新工具、新环境或长程恢复能力的证据。

## 与RL比较时，预算和教师信息必须留下

§8和C.14有SFT与GRPO的同题比较：匹配Qwen3-14B底座、题池、batch、响应上限和梯度更新次数，SFT在五个所测ID／OOD推理基准更好，一般能力结果混合。作者明确未匹配生成token总数与总FLOPs，RL还受奖励设计和熵收缩影响；SFT使用的教师长轨迹也是训练信息差别。因此本结果不建立SFT普遍优于RL的排序，更不支持据它否定学生状态采集的价值。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=10|§8 · p.10]] [[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=35|C.14、Table14 · pp.35–36]]

## 泛化也会带来其他行为变化

**原文实验。** 在HEx-PHI和所用judge／ASR定义下，长CoT SFT较匹配的NoCoT训练带来更大的拒绝／安全性退化。作者提出“持续解题倾向可能被用于绕开拒绝”的解释，并报告自我合理化文本线索与ASR的相关。附录明确相关不建立内部因果机制；不能将该解释写成已发现的模型内部过程。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=8|§6 · pp.8–9]] [[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=36|C.15、Tables15–16 · p.36]]

**原文局限。** 主要训练域仍是数学；虽有代码复制实验，但科学／多模态等监督未全面覆盖。实验不含更大规模dense或MoE；没有穷尽三类因素的全因子交互；行为检测不能替代表示层机制解释。[[raw/papers/optimization/finetuning/Reasoning-SFT-Generalization.pdf#page=17|Appendix A · p.17]]

## 整合落点与验收边界

已整合到 [[wiki/optimization/finetuning|微调]] 的条件化泛化说明，以及 [[wiki/optimization/Questions|Optimization问题]] 的SFT／RL／OPD分工与评价讨论；相关比较也写入Agentic RL页，索引同步。与 [[wiki/optimization/reinforcement-learning|Agentic RL]] 的联系是训练比较必须保留数据、教师、预算、底座及迁移定义。形成过程见 [[组会/2026-10-28-Optimization-RL/过程/C-前提与反证|C的前提与反证]]。原件与结构验收见 [[组会/2026-10-28-Optimization-RL/README#执行状态|本轮验收]]；Obsidian显示未测，未复现实验。
