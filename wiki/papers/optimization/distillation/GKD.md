---
type: paper
primary_direction: optimization/distillation
source_id: S056
created: 2026-10-25
updated: 2026-10-25
reading_status: targeted-fulltext-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/distillation/GKD.pdf]]"
---

# On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes

## 来源身份与读取范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S056 |
| 作者 | Rishabh Agarwal、Nino Vieillard、Yongchao Zhou、Piotr Stanczyk、Sabela Ramos、Matthieu Geist、Olivier Bachem（以下载PDF署名为准） |
| 版本 | arXiv:2306.13649v3；ICLR 2024 conference paper |
| 原始页面 | [arXiv版本页](https://arxiv.org/abs/2306.13649v3)；[版本PDF](https://arxiv.org/pdf/2306.13649v3)；访问2026-10-25 |
| DOI | 10.48550/arXiv.2306.13649（arXiv标识） |
| 原件 | [[raw/papers/optimization/distillation/GKD.pdf\|本地PDF · 18页]] |
| SHA-256 | `A81C71FA0CD15506642092790D854347F030C29EE1D6AA643B55AA51348E6869` |
| S001引用 | 引文3；§5.6，PDF pp.52；书目p.76 |
| 读取日期与范围 | 2026-10-25；正文pp.1–10；附录A.1–A.7（pp.14–18）的自蒸馏、模型初始化、预算与任务配置；看图核对p.4 Algorithm 1/损失及p.7 Figures 5–6。参考文献未逐项核验，未复现实验。 |

## 核心理解：纠正学生实际生成前缀上的预测

**原文陈述。** GKD处理的是自回归序列蒸馏的训练—推理分布偏移：固定专家输出只覆盖专家会到达的token前缀，部署时学生一次早期错误会改变后续前缀。GKD让学生生成输出，再让教师在同一前缀上给下一token概率；它不是先由教师生成一条正确答案再要求学生照抄。[[raw/papers/optimization/distillation/GKD.pdf#page=3|§3–3.1 · pp.3–4]]

| 要分开的选择 | GKD怎样做 | 不能混同的含义 |
| --- | --- | --- |
| 谁产生训练前缀 | 固定数据与当前学生生成，以学生比例λ混合 | λ=1才是纯学生生成；λ不是KL权重 |
| 谁给监督 | 教师在该前缀给全token分布 | 不要求学生原输出正确，但依赖可用教师概率 |
| 怎样更新 | 对前缀处散度求梯度，不反传采样分布 | 不能直接等同完整序列奖励的policy gradient |
| 散度选择 | forward KL、reverse KL、generalized JSD | 任务、温度和多样性目标共同影响选择 |

表格依据 [[raw/papers/optimization/distillation/GKD.pdf#page=4|§3.1、Algorithm 1 · p.4]] 与 [[raw/papers/optimization/distillation/GKD.pdf#page=5|Choice of Divergence · p.5]]。这里的“状态”首先是文本前缀，不是已经执行工具后产生的外部环境状态。

令P为教师、Q为学生，forward KL是$D_{KL}(P\|Q)$，reverse KL是$D_{KL}(Q\|P)$。GKD按序列长度平均各位置散度，再混合固定样本与学生样本。学生采样停止梯度是方法核心；若结合RL，Eq.5额外加入序列奖励，α控制蒸馏与奖励权衡。二者可共用rollout，但不是“有教师监督便不需要奖励”。[[raw/papers/optimization/distillation/GKD.pdf#page=3|§2–3、Eqs.1–2 · p.3]] [[raw/papers/optimization/distillation/GKD.pdf#page=4|§3.1、Eq.4 · p.4]] [[raw/papers/optimization/distillation/GKD.pdf#page=5|§3.2、Eq.5 · p.5]]

## 实验说明了什么

学生为77M/250M/800M T5，教师约3B T5-XL，主要任务先做任务SFT再蒸馏；不是从随机或无任务适应的小模型开始。XSum用ROUGE，WMT14英德翻译用BLEU，GSM8K用4-shot CoT及外部计算器核对最终答案。指令蒸馏使用FLAN2021，评估未纳入蒸馏数据的MMLU/BBH。各任务生成长度及训练步数见附录，不把语言生成结果升级成长时工具交互证据。[[raw/papers/optimization/distillation/GKD.pdf#page=5|§4 · pp.5–9]] [[raw/papers/optimization/distillation/GKD.pdf#page=14|A.2–A.6 · pp.14–18]]

学生生成比例与散度消融支持：在这些模型/任务上，on-policy与mixed通常优于仅固定序列；最佳散度并不统一。WMT Figure 6中JSD(0.1)较好；XSum的质量—多样性折中随评估温度改变；指令蒸馏reverse KL更好。因而不能从“reverse KL倾向mode seeking”推导所有任务都该使用它。[[raw/papers/optimization/distillation/GKD.pdf#page=6|§4.1、Figure 4 · pp.6–7]] [[raw/papers/optimization/distillation/GKD.pdf#page=7|Figure 6 · p.7]] [[raw/papers/optimization/distillation/GKD.pdf#page=9|§4.4、Figure 10 · p.9]]

GKD与RLAIF结合的XSum实验把NLI分类器蕴含分数作奖励；Figure 5显示α改变ROUGE与事实一致性代理的折中。这不是人类事实审计，也不表明全部教师错误均能自动修复。学生在线采样有成本：A.2报告GSM8K相对固定输出训练约1.8–2.2倍开销（随师生比例）。[[raw/papers/optimization/distillation/GKD.pdf#page=7|§4.1、Figure 5 · p.7]] [[raw/papers/optimization/distillation/GKD.pdf#page=14|A.2 · p.14]]

## 与本库的关系与边界

**本库综合。** 本文提供OPD的机制基线：分别登记采样分布、教师目标与散度。附录自蒸馏同规模教师先经GSM8K微调，学生未做该任务微调；不能因“self”就称完全没有外来信息。[[raw/papers/optimization/distillation/GKD.pdf#page=14|A.1 · p.14]]

原文将ImitKD、f-distill及MiniLLM作为邻近工作；本次未核读这些原论文，其新颖性与优劣比较只记为作者比较。[[raw/papers/optimization/distillation/GKD.pdf#page=10|§5 · p.10]] 与本批DAgger的区别是：GKD首先修正token前缀分布，DAgger另外改变真实环境中由谁执行整轮动作。候选问题为0；先保留从文本到交互的证据距离。

## 主题联系与维护状态

已整合到 [[wiki/optimization/distillation|Optimization · OPD]]；当前已完成摄入，内容与结构已验收。原件存在与哈希已核对；Obsidian渲染、公式及跳转未测（本轮已停用Computer Use）。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/distillation|optimization/distillation]]。
