---
type: paper
source_id: S062
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/rStar-Math.pdf]]"
---

# rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking

## 来源与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S062 |
| 作者 | Xinyu Guan、Li Lyna Zhang、Yifei Liu、Ning Shang、Youran Sun、Yi Zhu、Fan Yang、Mao Yang |
| 版本 | ICML 2025正式版，PMLR 267:20640–20661 |
| 原始入口 | [rStar-Math](https://proceedings.mlr.press/v267/guan25f.html)；访问2026-10-25 |
| 原件 | [[raw/papers/rStar-Math.pdf\|本地PDF，共22页]] |
| SHA-256 | `CC5BA4F6002B4B4D121D3818EFD33B888F1ED132A6D5C4CA290F63A40B0CAE03` |
| 实际阅读 | 2026-10-25；正文pp.1–9；附录A.2 pp.13–15训练、奖励模型和推理设置；A.1 pp.12–13选读；看pp.3–5方法图/公式和p.7 Table 3/Figure 3。A.3–A.4案例/提示未完整逐项核读。 |
| S001定位 | 引文191，§5.7.1，PDF p.54；书目 pp.90 |

正文PDF页码与印刷页码一致。未逐项核读参考文献，未审查代码或复现实验。

## 策略与评分器一起演化，题库仍有外部答案

rStar-Math将代码增强MCTS轨迹、策略SFT和过程偏好模型PPM连成四轮，更新的模型生成下一轮数据。针对的是静态数学多步推理与搜索；没有直接验证开放环境的长期行动、记忆或恢复。[[raw/papers/rStar-Math.pdf#page=3|§3、Figure 1 · pp.3–5]]

> [!important] “from scratch”不表示没有大模型帮助
> §3.3明确使用747k带答案题，来自NuminaMath/MetaMath，并用GPT-4围绕MATH train及AMC-AIME training split合成题，以十次解答的一致性过滤。Round 1用 **DeepSeek-Coder-V2-Instruct 236B** 跑MCTS，选轨迹启动小模型。摘要“without distillation from superior models”应与这些具体依赖并列，不能改写成无大模型、无标签自举。[[raw/papers/rStar-Math.pdf#page=1|摘要 · p.1]] [[raw/papers/rStar-Math.pdf#page=5|§3.3、Table 2 · p.5]]

## 更新对象与验证边界

| 环节 | 实际操作 | 不能替代的条件 |
| --- | --- | --- |
| 生成一步 | 推理写作Python注释，代码与前缀拼接执行 | 运行成功不证明数学语义正确 |
| 训练搜索 | 前两轮终局标签回传；后两轮PPM初始化中间值，再终局回传 | 训练终局仍匹配ground truth |
| 策略SFT | 正确解中选高质量轨迹 | 每轮从初始base重新训练 |
| PPM训练 | 高/低Q值且最终对/错的分支组成偏好对 | 有限搜索Q值不是步骤因果正确性真值 |
| 测试搜索 | PPM评分并选一个最终答案 | 不使用测试标签作训练式终局回传 |

机制依据[[raw/papers/rStar-Math.pdf#page=4|§3.1 · Eq.1–3、Figure 2 · p.4]]、[[raw/papers/rStar-Math.pdf#page=5|§3.2 · Eq.4 · p.5]]、[[raw/papers/rStar-Math.pdf#page=13|附录A.2 · pp.13–15]]；第三列为本库解释。

PPM一般比较共享前缀的候选步骤，最终答案步骤放宽该要求；用Q值选偏好对，再用pairwise ranking loss，而非把噪声Q值直接当精确回归标签。PPM训练还筛选能同时产生正确/错误路径的题；合成题按答案正确比例再过滤。因此反馈质量、任务覆盖和搜索预算共同变化。[[raw/papers/rStar-Math.pdf#page=5|§3.2 · p.5]] [[raw/papers/rStar-Math.pdf#page=13|A.2 · pp.13–14]]

## 不把搜索结果都归给策略训练

完整四轮仅在Qwen2.5-Math-7B进行；其余1.5B–7B模型用第四轮数据微调，并非各自独立演化。启动轮8次rollout，通常16次；第四轮难题追加64/128次及不同随机树，故轮次收益同时伴随覆盖和算力改变。[[raw/papers/rStar-Math.pdf#page=5|§3.3–4.1 · pp.5–6]]

Table 3的Pass@1指**搜索后选一个答案**：AIME/AMC默认16条轨迹，其余8条，另报64条版本。Qwen2.5-Math-7B的MATH 90.0%是64条版本；附录Table 9第四轮单轨迹策略为78.4%。闭源对照还混用默认思考预算和技术报告成绩，不能推出等成本优劣。[[raw/papers/rStar-Math.pdf#page=6|§4.1 · p.6]] [[raw/papers/rStar-Math.pdf#page=7|Table 3、Figure 3 · p.7]] [[raw/papers/rStar-Math.pdf#page=14|Table 9 · p.14]]

Table 5控制训练配方比较轨迹来源；Table 6的ORM配Best-of-N，而PQM/PPM配MCTS，因此不是只替换评分器。附录Table 10固定首轮策略，比较不同轮PPM，更直接支持评分器改善。[[raw/papers/rStar-Math.pdf#page=8|§4.3、Tables 5–6 · pp.8–9]] [[raw/papers/rStar-Math.pdf#page=14|Table 10 · p.14]]

## 局限与主题意义

作者抽查剩余未解20题，其中19题被认为错标，随后停止第四轮；有限抽查不能证明全部剩余题无效。训练集精确去污染协议本次未确认；使用训练分割不排除预训练记忆或合成题重叠。[[raw/papers/rStar-Math.pdf#page=6|§3.3 · p.6]]

**本库综合：**与[[wiki/papers/STaR|STaR]]一样保留外部终局标签，但增添执行检查与学习评分器。关键问题是搜索质量怎样影响下一轮数据，而不是自演化是否“摆脱监督”。验证可靠性与预算归因仍是材料/比较缺口；未进行额外查新，不认定新颖研究缺口。

## 主题联系与验收

已整合至 [[wiki/optimization/Overview#自我演化|Optimization · 自我演化]]，论文与主题互链、队列及索引已同步；内容与结构经主Agent验收通过，Raw哈希匹配，已完成摄入。Obsidian渲染、操作与来源跳转未测。

返回 [[wiki/index|索引]]。
