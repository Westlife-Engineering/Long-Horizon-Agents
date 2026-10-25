---
type: paper
primary_direction: optimization/distillation
source_id: S060
created: 2026-10-25
updated: 2026-10-25
reading_status: targeted-fulltext-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf]]"
---

# Self-Distillation Zero: Self-Revision Turns Binary Rewards into Dense Supervision

## 来源身份与读取范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S060 |
| 作者 | Yinghui He、Simran Kaur、Adithya Bhaskar、Yongjin Yang、Jiarui Liu、Narutatsu Ri、Liam Fowl、Abhishek Panigrahi、Danqi Chen、Sanjeev Arora |
| 版本 | arXiv:2604.12002v2；预印本，正式发表状态未确认 |
| 原始页面 | [arXiv版本页](https://arxiv.org/abs/2604.12002v2)；[版本PDF](https://arxiv.org/pdf/2604.12002v2)；访问2026-10-25 |
| DOI | 10.48550/arXiv.2604.12002（arXiv标识） |
| 原件 | [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf\|本地PDF · 31页]] |
| SHA-256 | `D6C91BA9FE38C9011318C5698D67010F7A6FC9F4C70B0F9FB13662D3AC7EA777` |
| S001引用 | 引文216；§5.6.2，PDF pp.53；书目p.93 |
| 读取日期与范围 | 2026-10-25；正文pp.1–10；附录A–F（pp.16–29）与G（pp.30–31）选读设计/限制，参考文献不作独立来源。看图核对p.2 Figure 2、p.4 Eqs.1–4、p.5 Table 1、p.19采样账、p.23实现表。未运行代码、未复现实验；G的全部数值未独立重算。 |

## 核心理解：先学会依据对错修订，再蒸馏回首次生成

**原文陈述。** SD-Zero在可验证数学/代码任务上，用同一模型架构分别当generator与reviser。它仍需要题目和最终答案/二元验证器；“Zero”是不需要外部强教师与gold解题过程，不是没有训练数据或真实反馈。教师侧特权信息是**完整学生初答＋该答对错**。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=3|§2–2.1 · pp.3–4]]

| 阶段 | 数据与更新 | 信息流的关键区别 |
| --- | --- | --- |
| SRT | 初答→验证→正确则改写、错误则重做→只留修订后正确的轨迹 | 训练revision与generation两项交叉熵 |
| Self-distillation | 学生生成新初答，冻结SRT修订者看完整初答和结果，再评分相同token前缀 | reverse KL(学生‖修订者)，不需要另采修订答案 |
| 迭代扩展实验 | 一轮蒸馏后将教师同步为新学生，继续训练 | 是§3.4额外实验，主设置Phase 2教师固定 |

依据 [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=2|Figure 2 · p.2]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=4|§2.1–2.2、Eqs.1–4 · p.4]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=7|§3.4 · pp.7–8]]。

SRT的generation目标不是只学修好答案：Eq.2的目标串为`初答＋结果提示＋修订答案`，可能包含原错误过程；revision目标只在该上下文后预测修订部分。两个目标一同训练解释了SRT会生成长的显式自修订。随后蒸馏在学生原答案每个位置比较两种条件分布：学生看题目和当前前缀；冻结教师还看到完整初答与结果提示，梯度仅进学生。主阶段不额外加入GRPO奖励项；二元反馈用于构造教师上下文。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=4|Eqs.1–4 · p.4]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=17|Algorithm 1 · p.17]]

## 实验证据：主要增益来自哪里

主实验分别训练OpenR1-Math与Codeforces域，Qwen3-4B-Instruct及Olmo-3-7B-Instruct，八项数学/代码测试用avg@8；这不是8次任一成功的pass@8。Table 1中Qwen平均49.8→SRT57.6→SD-Zero60.3，Olmo41.1→50.3→51.5：大部分提升来自SRT，第二阶段提供增益和长度压缩，不能把全收益归于OPD。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=5|§3.1、Table 1 · p.5]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=6|§3.2–3.3 · p.6]]

AIME24分析中SRT首次回答平均8458 token，SD-Zero3518，准确率66.7与68.3；修订评估另提供真值对错反馈，与无反馈首次生成不同。原文“1K AIME24 questions”的采样/去重口径本次未确认，不将其写成1K独立AIME原题。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=25|D.3、Table 9 · p.25]]

双损失消融和跳过SRT的实验支持先训练修订能力的重要性；只做Phase 2平均51.4，而完整方法60.3。但这仅说明该模型/预算的配方，不能断言所有模型必须先SRT。thinking模式的负结果来自**SDFT**附加实验，不是直接测试SD-Zero对所有thinking模型失效。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=27|E.2、Tables 11–13 · pp.27–28]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=29|F、Table 14 · p.29]]

## 采样预算与实现表存在需保留的差异

附录C.1–C.2给出SRT从10K初始题各采一次初答、再各采3次修订，共40K generation，筛出6K轨迹；Phase 2另用9K题各采一次，总49K。基线按15K题×4为60K。作者另用平均长度估算采样token约225M对222M，并估算前向loss token接近；这不等于实测总FLOPs、显存或墙钟严格相同。10K出发题与9K additional题对“相同15K问题集”的映射没有完全交代，需代码/数据核查，不直接认定全部独立题预算相同。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=19|C.1–C.2、Table 3 · pp.19–20]]

C.3还有正文/预算口径差异：Table 4写3 epochs，预算表按1；Table 5 GRPO写8 rollouts，而主比较C.2及D.4明确4；Table 6 SDFT写1 generation，预算按4；§3.1训练温度0.7、16K上限，而Table 6蒸馏温度1.0、8192。将主结果解释依照相邻正文及专门预算说明，但**复现配置待核查**。Table 6还注明top-K=64且不把外部概率全置零，故理论全词表KL与具体近似实现也需区分。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=5|§3.1 · p.5]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=21|C.3、Tables 4–6 · pp.21–23]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=25|D.4 · p.25]]

## 稠密信号不等于真实因果信用

作者以200 responses的token KL集中度及示例提出“自定位”解释。须区分完整token分布KL（非负）与已采样token的log概率比（可正可负）；后者才是图中可能为负的Token KL Reward。它反映修订教师对token的偏好，不是验证器直接指出真实错误步骤，也不是因果责任证明。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=7|Figure 4 · p.7]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=8|§4.1 · p.8]]

**本库综合。** 本文把“可得的二元结果”与“如何构造稠密教师目标”分开，是OPD监督来源的重要实例。实验对象主要为一次文本解题/代码生成，附录G也属于推理与后训练；未证明外部环境状态被不可逆改变时可恢复，不能直接作为长期交互Agent的完成证据。作者明确保留无可验证奖励域和thinking模型迁移限制。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=9|§5 Limitations · pp.9–10]]

其他自蒸馏方法的新颖性比较来自本文，未独立核读对方论文；与本批π-Play的直接可核对差异是固定题目/冻结修订者对比出题课程/EMA教师、纯蒸馏对比RL混合。当前候选问题为材料核查而非研究缺口。

## 主题联系与维护状态

已整合到 [[wiki/optimization/distillation|Optimization · OPD]]；当前已完成摄入，内容与结构已验收。原件存在与哈希已核对；Obsidian渲染、公式、Mermaid及跳转未测（本轮已停用Computer Use）。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/distillation|optimization/distillation]]。
