---
type: paper
primary_direction: optimization/reinforcement-learning
related_directions:
  - optimization/finetuning
source_id: S077
created: 2026-10-28
updated: 2026-10-28
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf]]"
---

# DeepSeek-R1：可验证推理中的 RL 与多阶段后训练

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S077 |
| 原文标题 | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning |
| 作者 | DeepSeek-AI；完整贡献名单见原文 pp.11–12，本页不展开约 200 位作者 |
| 版本 | arXiv:2501.12948v2，2026-01-04；v1 为 2025-01-22。arXiv 登记期刊版为 Nature 645, 633–638 (2025)，期刊 DOI `10.1038/s41586-025-09422-z`；本页核读的是 arXiv v2 PDF，未另读期刊排版版 |
| 原始来源 | [身份与版本页](https://arxiv.org/abs/2501.12948v2)；[固定版本 PDF](https://arxiv.org/pdf/2501.12948v2)；访问 2026-10-28 |
| Raw | [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf\|本地原件，共 86 页]] |
| SHA-256 | `b191b0a365a64b4ab2791d117069ed17a2933d03554a662ced58b37df52018f4` |
| 主归属理由 | 本轮用于核对推理模型后训练中的 RL，及其与 Agentic RL 的联系和边界；跨方向关联 SFT 配方 |
| 实际阅读 | 2026-10-28：正文 pp.1–11（§1–6，p.11 仅至作者表之前）；附录 B.3.1–B.3.2 pp.19–21、B.3.3 pp.26–27、B.4–B.6 pp.34–37、C–D.1 pp.37–41、E.1 的 Table12及相邻解释 p.56、E.2–E.5 pp.57–60、F–G pp.60–64（p.64 至 G.2 结束）。额外定位了 pp.25、27、34 的示例边界，不把未读的长示例算已核读 |
| 原页视觉核对 | p.3 Eqs.1–3／超参数，p.4 Fig.1，p.6 Fig.2，p.9 Table3，p.36 Fig.6，p.40 D.1，p.61 Tables15–16，p.62 Table17，p.63 G.1–G.2；第二轮另逐页复核 p.3、p.6、p.40、pp.61–63，未扩展本页正文阅读范围；其余上述范围以 PDF 文本核读 |
| 未读与未做 | 未完整核读作者表、A 背景／B.1 基础设施、长案例、D.3 安全附录、H–I及全部参考文献；未核代码、未复现实验 |
| S001 入口 | 综述引文112；§5.5.1 在 PDF p.48 将可验证终局奖励联系到后续交互式 RL。本页按 v2 解释，不假定它与综述引用版本完全一致 |

PDF 页码从首页起算，本版本与页脚页码一致。v2 的发布日期不等于这些实验是 2026 年前沿结果；本页保留原文的模型、数据集与历史比较对象。

## 它回答的是哪种问题

**原文陈述。** 作者检验：能否从已有 DeepSeek-V3-Base 出发，不先提供人工推理轨迹做 SFT，只用可验证结果和格式奖励，经 RL 得到更好的推理行为。R1-Zero 是该探索；正式 R1 另加入冷启动 SFT、第二次 SFT 与偏好 RL，处理可读性、语言混合和通用任务。这里的“纯 RL”修饰后训练方案，不表示随机初始化、没有预训练知识、没有问题数据或没有验证器。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=2|§1–2 · p.2]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=6|§3、Fig.2 · p.6]]

**本库定位。** 本文主要把长计算放在一次生成的推理链中。其软件工程结果采用 Agentless 框架，作者也明确说工具使用和大规模软件工程 RL 尚有限。因此它可作为“推理模型后训练 RL”的直接证据，不能把长 CoT 自动当成长程环境交互；“模型生成代码，执行器在训练后评分”与“模型在 rollout 内根据执行结果继续行动”也应分开。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=10|§6 · pp.10–11]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=40|D.1 · p.40]]

## 配方：RL 与 SFT 怎样分工

R1-Zero 对同一问题采样一组输出，用组内奖励的相对高低构造优势，采用 GRPO 更新，含参考策略的 KL 约束。推理任务采用答案匹配／测试等准确性奖励，加格式奖励；不使用神经网络过程奖励。训练从每题16条、最大32,768 token开始，在第8.2k步把最大长度提高到65,536，总计10,400步。**Fig.1 的后段增长同时伴随长度上限调整，不能全部解释为不变条件下自发增加思考。** [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=3|§2.1–2.3、Eqs.1–4、Fig.1 · pp.3–4]]

正式 R1 的 Fig.2 显示的是包含数据回流的多阶段配方，不能压成“把 R1-Zero 接着训成 R1”。

| 环节 | 做什么 | 边界 |
| --- | --- | --- |
| 冷启动 SFT | 从 R1-Zero 采样并筛选，结合 V3 与人工修订构造较可读的长 CoT；在 V3-Base 上形成 Dev1 | 有人类风格与语言偏好；不再是 R1-Zero 的无 SFT 配方 |
| 推理 RL | Dev1 经可验证奖励及语言一致性奖励得到 Dev2 | 可读性目标与任务得分可能有取舍 |
| 拒绝采样与第二次 SFT | 从 Dev2 获得约60万推理样本，加约20万非推理数据，再对 V3-Base 做 SFT 得到 Dev3 | 不是在 Dev2 参数上简单连续叠加 SFT；数据、目标和初始化都需保留 |
| 综合 RL | Dev3 继续使用推理规则奖励和一般任务偏好奖励，形成 R1 | 第二段共1,700步，偏好数据和偏好奖励仅在最后400步引入 |

依据 [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=6|§3、Fig.2 · pp.6–8]]、[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=20|B.3.2 · pp.20–21]]、[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=26|B.3.3 · pp.26–27]]。Table5 中约80万 SFT 样本大多是单轮交互，作者明确保留多轮能力限制。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=27|B.3.3、Table5 · p.27]]

**蒸馏也需分清。** R1-Distill 系列在固定约80万样本上对较小基座做 SFT，本文未为这些蒸馏模型增加 RL。它属于离线轨迹蒸馏，不是按当前学生 rollout 查询教师的 OPD。后一句是按本库术语作的分类。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=35|B.4.3 · p.35]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=60|F · pp.60–61]]；OPD 定义见 [[raw/surveys/Towards Long-Horizon Agents.pdf#page=52|S001 §5.6 · p.52]]。

## 结果支持什么

- **在本文配方下，RL 能明显提高可验证推理任务表现。** Fig.1 的 R1-Zero AIME 2024 pass@1 从15.6%到77.9%，cons@16另为86.7%；这两种统计不可混用。评价时温度0.6、top-p 0.95，AIME每题64次采样估计平均pass@1，最大输出32,768 token；cons指标使用多样本投票。它支持该基座、数据与预算下的提升，不证明所有基座或所有任务都能复现。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=4|§2.3、Fig.1 · pp.4–5]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=40|D.1 · pp.40–41]]
- **阶段收益并非同向增长。** Table3 中冷启动后指令遵循改善，同时部分推理得分下降；推理 RL 与后续通用数据／偏好 RL 的改善侧重点不同。该表是完整配方阶段的观察，多个因素共同变化，不能据此给 SFT 或 RL 分配普遍、独立的因果贡献。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=8|§4、Table3 · pp.8–9]]
- **小模型能通过离线蒸馏获得强推理表现。** Table16 在 Qwen2.5-32B 上比较从强教师生成数据蒸馏与本论文10K步以上的纯RL配方，前者在报告的五个任务指标上更好。它不是预算严格匹配的所有 SFT／RL 路线裁决，也没有测试 OPD。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=61|F.1、Table16 · pp.61–62]]
- **行为线索与能力结论分开。** C.2 统计若干反思词与“wait”的频率；这描述输出模式变化，不能单凭词频证明形成了新的推理算法或突破基座可达能力。B.3.2 又明确说明正式 R1 的拟人化风格部分来自工程设计。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=38|C.2、Fig.9 · pp.38–39]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=20|B.3.2 · pp.20–21]]

## 对长期 Agent 的限制

**反馈与时间成本。** 作者观察到偏好奖励继续上升而 Codeforces 表现下降的 reward hacking；可靠验证器难构建的开放任务仍是限制。软件工程评估耗时也阻碍本文进行大规模相关 RL。这说明训练效率和反馈质量是实际限制，不能据此把“长任务困难”全归给 GRPO。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=11|§6 · p.11]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=35|B.5、Fig.6 · pp.35–36]]

**基座与泛化。** G.1 报告早期7B dense／16B MoE试验提升不足；F.1另报告Qwen2-Math-7B-Zero在所测AIME上高于Qwen2-Math-7B-Instruct和GPT-4o。**Table17的对照不是同一7B基座训练前后**，不能据此单独识别RL的全部因果贡献。这些是不同基座和配方下的经验，不能推广成“小模型不能RL”或仅由参数量决定上限。D.1承认n-gram去污染不能排除改写污染；E.2提供训练后发布数学竞赛的补充结果，但仍不等于跨环境Agent泛化。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=62|F.1、Table17、G.1 · pp.62–63]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=40|D.1 · p.40]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=57|E.2 · p.57]]

**本库综合。** 本文支持把“训练到更好的回答分布”“改善推理计算的使用”“在工具反馈中完成任务”分开讨论。SFT、RL和蒸馏可位于同一配方；长CoT及推理榜单提升还不足以证明状态恢复、外部动作选择和长期任务完成均已提高。后者需结合 [[wiki/optimization/reinforcement-learning|Agentic RL]] 的交互证据另核，不能由论文的历史发布地位替代。

## 整合状态

已整合到 [[wiki/optimization/reinforcement-learning|Agentic RL]] 的推理RL／交互RL比较、[[wiki/optimization/finetuning|微调]] 的阶段分工，以及 [[wiki/optimization/Questions|Optimization问题]] 的宏观讨论；唯一来源页与索引同步。问题首稿与本轮维护状态见 [[组会/2026-10-28-Optimization-RL/过程/B-训练范式与动向|组会B首稿]]。原件和固定版本哈希已核对；原页视觉核对范围如上，Obsidian显示未测。
