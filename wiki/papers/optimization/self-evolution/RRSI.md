---
type: paper
primary_direction: optimization/self-evolution
related_directions:
  - harness/workflows
  - harness/verification
source_id: S081
created: 2026-10-28
updated: 2026-10-28
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/self-evolution/RRSI.pdf]]"
  - "[[raw/papers/optimization/self-evolution/STaR.pdf]]"
  - "[[raw/papers/optimization/self-evolution/Agent0.pdf]]"
---

# RRSI：约束 Harness 的递归修改，让改进能够迁移

## 来源与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID／类型 | S081；方法论文，附跨任务迁移、组级消融与案例分析；不是综述，也不是模型权重训练方法。 |
| 完整题名 | RRSI: Regularized Recursive Self-Improvement of Agent Harnesses |
| 作者 | Peng Xia、Rujun Han、Zifeng Wang、Yanfei Chen、Yufan Zhuang、Yoonho Lee、Chengsong Huang、Han Yu、Zhongying CuiZhu、Yifei Ming、Huaxiu Yao、Burak Gokturk、Tomas Pfister、Chen-Yu Lee |
| 版本与日期 | arXiv:2609.24972v3；arXiv 版本日期 2026-10-04，用户 PDF 首页另标 2026-10-06，分别保留；出版会议未确认。 |
| 身份入口 | [arXiv v3](https://arxiv.org/abs/2609.24972v3)、[DOI](https://doi.org/10.48550/arXiv.2609.24972)；2026-10-28 核对 arXiv 身份页。论文给出[官方代码](https://github.com/google-research/rrsi)及[项目站](https://regularized-rsi.com)，本次未审代码或站内轨迹。 |
| 原始文件与复制 | 用户文件 `C:\Users\ZENGZX\Desktop\人大高瓴paper\Agent & RSI\RRSI - Regularized Recursive Self-Improvement of Agent Harnesses.pdf` 原样复制为 [[raw/papers/optimization/self-evolution/RRSI.pdf\|RRSI.pdf，27页]]；源文件保留。 |
| SHA-256 | `26F8B5417F8A60C9284BB4A36D3981C41B8E071134AEA0BF3402FE9584C8CD76`；复制前后相同。 |
| 实际阅读 | 2026-10-28；正文 pp.1–11、附录 A–F pp.17–27；参考文献 pp.11–15 仅定位相关工作，p.16 为附录目录。直接查看 Fig.2–3、Tables 1–3、5–6、8–9、Algorithms 1–2 及方法公式原页。比较另回读 STaR pp.3–4、Agent0 pp.3–6、8。 |
| 归属理由 | 主问题是跨轮经验怎样转成持久的系统改动，故放 `optimization/self-evolution`；更新对象是外部 harness，交叉关联 [[wiki/harness/workflows\|工作流]] 与 [[wiki/harness/verification\|验证]]，不据目录归属声称进行了参数训练。 |

PDF 页码与印刷页码一致。论文结果以下均指该用户提供版本；没有逐项核验参考文献、执行实验或检查发布代码。身份网页只作元数据核对，不另存快照。

## 先读懂这篇论文

**问题是什么？** 让 Agent 反复看失败记录、改提示或工具流程，确实可能使练习任务得分上升；但它也可能只是越来越熟悉这套题和评分方式。RRSI 要解决的是：模型权重不动时，怎样让反复修改 harness 得到的收益，转移到没参与修改选择的任务集。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=2|§1–2 · pp.2–3]]

**方法是什么？** 限制每次能同时改多少件事，保留成功与失败的修改历史，停滞时探索未尝试的组件；候选还须通过泄漏检查、成绩底线与成本条件，并让长期无收益的结构成为后续删除目标。它约束的是搜索与保留规则，仍允许修改提示、控制流、工具、记忆等各种组件。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=4|§3、Fig.2 · pp.4–6]]

**证据说明什么？** 三个领域分别演化一个 harness，再原样评测未参与搜索的套件。本文报告的六个 held-out 划分均改善；工作场景消融显示，去掉提案侧或选择侧约束，都可能让练习分更高、迁移分更低。这个证据支持整套约束在所测条件的价值，不能分别证明每项约束的独立贡献。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=8|§4.2–4.3、Fig.3、Tables 1–2 · pp.8–9]]

**能带走什么？** “本轮分数涨了”不足以决定哪些经验应该永久留在系统里。应把修改对象、反馈复用、迁移评价与运行成本同时记录；本文没有证明无限迭代仍稳定，也没有研究权重与 harness 同时更新。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=11|§6、Limitations · p.11]]

## 为什么反复改进也会过拟合

论文把 Agent 写作 $A=(\pi,H)$：$\pi$ 是冻结的底座策略，$H$ 是提示、控制流、工具接口、记忆和上下文管理。外层循环在固定的 $D_{\mathrm{evolve}}$ 上运行当前版本，将轨迹变成反馈，提出几个修改，再在同一任务集上评测和选择。后续提案已经利用先前测过的成绩，因此这不是多次互不相关的测试，而是**对有限反馈的适应性复用**。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=3|§2、Eq.1–3 · p.3]]

作者归纳三种风险：把题目或评分习惯写进系统；把随机高分当作改进；不断增加上下文、反思或工具结构，用更多计算换取练习分。**本库分析：**本文的“长”主要体现在跨轮保留修改及多步工具任务；它不直接用 H1–H3 分层，不能仅凭递归名称就视为跨会话自主学习已经解决。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=2|§1 · p.2]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=7|§4.1 · p.7]]

## 一轮 RRSI 怎样运行

| 环节 | 输入、动作与产物 | 它约束什么 |
| --- | --- | --- |
| 提案预算 | 当前 harness、失败反馈及历史 → 每个候选只捆绑有限个可区分的修改；预算按余弦日程逐步缩小。 | 控制每轮对有限反馈的拟合能力，也让后期修改更容易解释。 |
| 历史与探索 | 记录组件、假设、diff、分数／成本变化和是否入选；停滞时给未测组件预留候选名额。 | 拒绝过的方案仍留下证据，避免只反复改同一类提示。 |
| 评测前 critic | 检查实际 diff，筛除任务名称、答案、特定实体／数值等基准特化逻辑和惰性结构。 | 避免泄漏候选先拿到高分，再影响后续搜索；通用提示或工具说明仍可改。 |
| 评测与准入 | 在 evolve 集测成绩与 policy-token 成本；先过历史最佳成绩底线，再按增益所在区间检查成本／新颖度条件。 | 限制噪声获胜者和缺乏收益依据的成本增长。 |
| 保留与剪枝反馈 | 在合格候选中选最高分；没有则保留当前版本。近期没有正收益的组件进入后续删除提案清单。 | 永久状态需要持续证据支持；删除也是候选修改，须继续接受评测与准入。 |

以上对应 [[raw/papers/optimization/self-evolution/RRSI.pdf#page=5|§3.2–3.3 · pp.5–6]] 与 [[raw/papers/optimization/self-evolution/RRSI.pdf#page=20|附录 D、Algorithms 1–2 · pp.20–22]]。它没有把全部规则写成一个可互相补偿的总奖励：很省 token 也不能补偿跌破成绩底线。

这里的“信用分配”是**修改证据账本**，不是动作级 RL 优势，也不是已识别的组件因果贡献。同一候选捆绑多个修改时，每条修改记录共享该候选的 $\Delta S$、$\Delta C$；逐步减少修改数只是减轻混杂。剪枝按窗口内组件关联修改的最大测得增益判定，窗口内没有记录也可能成为目标；不能把“未见正收益”翻译为“证明该组件无用”。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=20|附录 D.2、Eq.9–14 · pp.20–21]]

### 用一个实际案例走完选择

编码首轮两个候选都增加完成前验证和长任务处理指导。R0-A 的测得增益超过噪声门槛，被接受；R0-B 虽然涨分，但涨幅落在噪声带内且增加计算，被成本规则拒绝。另一个候选 R8-B 在完成前重读原任务要求，虽然省计算，却因跌破底线被拒绝。输入是旧 harness 与失败反馈，中间产物是具体 diff 及评价记录，输出是保留一个新版本或继续沿用旧版本；**“听起来合理的规则”不会自动进入永久系统**。这些是作者报告的轨迹案例，未用发布日志独立复算。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=25|附录 F、Table 8 · pp.25–26]]

### 核心数学：限制修改量，再分区间判断准入

每轮 $t$ 的修改数量上限为 $b_t$；$T$ 是演化轮数，$b_{\min}$、$b_{\max}$ 是日程参数：

$$
b_t=\left\lceil b_{\min}+(b_{\max}-b_{\min})\frac{1+\cos(\pi t/T)}{2}\right\rceil.
$$

这是对每个候选中活跃修改数量的约束，不是模型参数的 $L_0$ 优化。候选池每轮都可变化。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=5|§3.2、Eq.4 · p.5]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=20|附录 D.2、Eq.9 · p.20]]

以 $\hat S(H)$ 表示测得成绩、$\hat C(H)$ 表示 policy-token 成本，$S^\star$ 表示已接受路径上维护的历史最佳成绩，$\delta$ 来自重复评测初始 harness 的经验波动。新候选首先必须满足：

$$
\hat S(H')\geq S^\star-\delta,\qquad
\Delta S=\hat S(H')-\hat S(H_t),\quad
\Delta C=\frac{\hat C(H')-\hat C(H_t)}{\hat C(H_t)}.
$$

若 $\Delta S>\delta$，要求 $\Delta C\leq\beta_0+\beta_1\Delta S$：更大收益可以换取更多 token。若 $\Delta S\leq\delta$，改用 $w_s\Delta S-w_c\Delta C+w_n\nu_t(H')>0$：小幅分差还要结合成本下降或结构新颖度判断。$\nu_t$ 只奖励此前没有进入获胜修改的工具、skill、memory、subagent 组件类型；编码设置令 $w_s=0$，另外两个领域使用正值。**这里允许底线内有条件的小回退，并不保证逐轮成绩严格上升；经验噪声带也不是自适应搜索的统计保证。** [[raw/papers/optimization/self-evolution/RRSI.pdf#page=6|§3.3、Eq.5–7 · p.6]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=22|附录 D.3、Eq.15–17 · p.22]]

作者把更新数量、结构删除、资源增长控制分别类比为 $L_0$、Lasso/$L_1$、Ridge/$L_2$。三者是功能类比，尤其成本规则没有平方范数、剪枝没有连续 $L_1$ 损失；不能把它写成求解了传统正则化目标或给出了泛化定理。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=4|§3.1 · p.4]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=19|附录 D · p.19]]

## 实验支持什么，不能怎样解读

### 任务与预算先分清

| 演化实例 | 搜索用任务 | 完成搜索后不改 harness 的评测 | 关键条件 |
| --- | --- | --- | --- |
| 编码 | Terminal-Bench 2.1，89题 | SWE-bench Verified，跨套件 OOD | 20轮，每任务每评测2次；初始 harness 为 Terminus-2。 |
| 办公／专业工作 | Harvey LAB，固定120题 evolve | 同源40题 ID held-out；JobBench、GDPval、APEX-Agents 三个 OOD 套件 | 20轮，每任务每评测2次；ReAct、MCP工具入口、动态工具集合与 ReSum 式上下文管理。 |
| 工程设计 | EngDesign 可运行的61题，无 ID held-out | Frontier-Eng OOD | 40轮，每任务每评测4次；冻结模拟器评分。 |

主实验 policy、proposer、analyst、critic 均为论文所记的 Claude Opus 4.8，policy 权重冻结。每轮候选预算 $m=2$；基线共享初始 harness、policy、evolve 集与候选预算，**相同候选数不等于相同总 token、调用数或搜索成本**。超参数声称不参考 held-out/OOD，完整协议见 [[raw/papers/optimization/self-evolution/RRSI.pdf#page=7|§4.1 · p.7]]、[[raw/papers/optimization/self-evolution/RRSI.pdf#page=17|附录 B · pp.17–19]]、[[raw/papers/optimization/self-evolution/RRSI.pdf#page=23|附录 E.1、Table 5 · p.23]]。

### 哪些结果最有解释力

- **练习分不是迁移分。** Table 1 中 RRSI 的 Harvey LAB evolve 增益比所列演化基线小，三个办公 OOD 套件平均分却最高；ID held-out 与最强该项基线持平。看 Fig.3 时注意这是八个基准、九个划分，包含三个 evolve、一个 ID held-out 和五个 OOD；不是每个领域都留了独立同分布测试。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=8|Fig.3、Table 1 · p.8]]
- **两组约束都影响迁移，但单个部件贡献尚未分离。** Table 2 去掉任一组约束后，办公 OOD 平均下降；完全不正则化更偏向 evolve 分。消融单位是 proposal／acceptance 整组，没有逐一隔离 critic、剪枝、噪声底线、退火或新颖度，更没有单独证明“成本控制导致泛化”。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=9|§4.3、Table 2 · p.9]]
- **省的是相对演化基线的运行 token。** Table 2 的每 trial policy tokens 为未正则化 3.80m、RRSI 2.42m、初始 harness 1.56m；Fig.4 成本测于办公 evolve 集。RRSI 仍比初始版本贵，不能称无额外推理成本；这些数也不包含完整外层搜索账单。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=9|Table 2 · p.9]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=10|Fig.4 · p.10]]
- **换模型有两种实验。** Table 3 是分别用两种冻结 policy 重新演化，再测试跨套件迁移；Table 4 才是把 Gemini 3.5 Flash 搜得的同一 harness 直接交给未参与搜索的 Gemini 3.1 Flash Lite，但只在 Terminal-Bench 上测试。后一项支持有限的跨模型复用，没有同时证明“新模型＋新套件”的联合迁移。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=9|Tables 3–4 · pp.9–10]]
- **报告了评价不确定性和搜索重跑。** 附录对任务做配对 bootstrap，并给每个主实例的两次独立搜索结果；二者分别回答有限测试样本和提案随机性问题。两次搜索及有限轮数仍不足以说明长期稳定。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=24|附录 E.2、Tables 6–7 · pp.24–25]]

工程结果说明所见迁移不全依赖 LLM judge，但不能据此排除所有评测特化。Frontier-Eng 排除了与 evolve 集重合的 EngDesign 域，采用47题固定分母，环境无法构建的题不给分，38题可贡献分数；Medal Score 与办公 rubric／胜率不是同一指标。Harvey LAB 按 criterion 聚合、长 rubric 权重更高；APEX 用全480题分母，缺失 rollout 算失败。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=17|附录 B.3–B.8 · pp.17–19]]

## 与库内自我演化工作的比较

下表是**本库基于各文原页的机制比较**，不是 RRSI 对它们的直接实验，也不排列性能优劣。

| 维度 | [[wiki/papers/optimization/self-evolution/STaR\|STaR]] | [[wiki/papers/optimization/self-evolution/Agent0\|Agent0]] | RRSI |
| --- | --- | --- | --- |
| 持久更新对象 | 重生成推理数据，从初始权重重新微调模型 | 交替训练课程生成者和执行者 | 固定 policy，保留修改后的 harness |
| 主要反馈锚点 | 固定题目的已知正确答案；失败题可获得答案提示 | 工具返回值进入上下文，最终奖励仍基于多数票伪标签 | evolve 集的测试／rubric／模拟器评分，另以 token 成本与 diff 检查约束选择 |
| 主要学习／搜索风险 | 答案正确不保证理由可靠，数据筛选与训练过拟合 | 众数不等于真值，课程和策略共同变化 | 反复复用有限评分，特化修改与资源膨胀进入永久状态 |
| 已核对的证据范围 | 推理自举的参数学习流程 | 工具推理及三轮共同演化 | 有限轮 harness 搜索、跨套件及有限跨模型迁移 |

比较依据：[[raw/papers/optimization/self-evolution/STaR.pdf#page=3|S061 · §3、Algorithm 1 · pp.3–4]]；[[raw/papers/optimization/self-evolution/Agent0.pdf#page=3|S064 · §3 · pp.3–6]]、[[raw/papers/optimization/self-evolution/Agent0.pdf#page=8|Fig.4 · p.8]]；[[raw/papers/optimization/self-evolution/RRSI.pdf#page=3|S081 · §2–3 · pp.3–6]]。它们共同有“反馈影响下一轮”的外层循环，**留下的东西不同：参数、题目分布或外部程序**。RRSI 补充了 [[wiki/optimization/self-evolution|自我演化]] 中固定权重的外部演化一轴，没有反驳 S001 §5.7 作为训练管线闭环的定位。

RRSI 更接近的 Meta-Harness、AHE、TTHE、HarnessX，本次未读其原文。可以确认的是 **RRSI 本文如何实现和报告这些基线比较**（§4、附录 C/F）；不能据此宣布那些方法一般都不会泛化，或把作者对其机制的描述当作本库独立核验。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=19|附录 C · p.19]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=27|Table 9 · p.27]]

## 限制与尚未确认的报告细节

作者明确限于冻结模型、有限 evolve 集与有限搜索预算；不同架构、工具生态和更长运行仍待验证。**本库归纳：**保留全部修改历史不使测量独立，噪声阈值不提供泛化证明，critic 也没有单独的误判／漏判评估。Table 9 对“可复用机制”的解释是作者案例分析，本次未审查真实 diff 或执行轨迹。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=11|Limitations · p.11]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=25|附录 F · pp.25–27]]

以下不一致保留为复核项，不据此否定整体方法：

1. **摘要数字与具体图表口径不同。** 摘要称 OOD 最多提升4.3点，而 Fig.3／Table 6 给 JobBench +4.7；摘要称少30% policy tokens，Table 2 的3.80m→2.42m按所列数计算约少36.3%。本页引用具体设置和图表，不把摘要数字当统一汇总。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=1|摘要 · p.1]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=8|Fig.3、Table 2 · pp.8–9]]
2. **准入权重与校准时点未完全交代。** D.3 说 $w_s,w_c,w_n$ 见 Table 5，但该表未列这三个权重；E.1 一面称运行前固定且不扫参，一面描述依据 opening rounds 校准成本阈值，具体先导／正式轮次关系未确认。正文给出了规则，尚不足以还原所有实现参数。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=22|附录 D.3–E.1 · pp.22–23]]
3. **GDPval 评价计数存在歧义。** B.5 同时写185个任务、每对两个展示顺序及每位 judge 发出204次比较，未解释这些数量的关系；本次不擅自改成另一分母。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=18|附录 B.5 · p.18]]

下一条最有价值的证据是核对发布实现的准入权重、校准时点与逐候选成本账本；这是实现核查需求，尚未执行，也不是已确认的研究缺口。

## 能借走的思路与思路重建

可迁用的是：将任务内运行与跨任务修改分开，明确谁能改什么、改动如何被测量、哪些证据允许它永久保留；在搜索阶段记录失败修改，在评价阶段保留未参与选择的任务；同时区分最终 harness 的运行成本和寻找它的成本。是否有效仍依赖可靠反馈、可重复评测与足够的迁移测试，不能直接把某组阈值搬到任意工具环境。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=3|§2–3 · pp.3–6]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=24|附录 E.2 · p.24]]

**下面是本库思路重建，不是作者日记。** 已有自动修改流程让“多试几个版本”成为可能，却会不断从同一批题获得选择信号；若版本越来越长、题内分越来越高，迁移仍不增长，就要怀疑留下的是评分习惯而非通用工作能力。【推断】因此值得尝试的方向，是先让每次变化更可追溯，再要求保留下来的变化同时解释收益与代价，并在冻结最终版本后，用未参与选择的任务检验收益是否迁移。这个方向由本文问题设定与实验所支持，不等于任何特定正则规则必然有效。[[raw/papers/optimization/self-evolution/RRSI.pdf#page=2|§1–3 · pp.2–6]] [[raw/papers/optimization/self-evolution/RRSI.pdf#page=9|Table 2 · p.9]]

## 主题联系与验收

已整合至 [[wiki/optimization/self-evolution|自我演化]]、[[wiki/harness/workflows|工作流]]、[[wiki/harness/verification|验证]]；论文、主题与索引已同步，主 Agent 已独立核查关键原页并通过内容与结构验收，原件复制前后 SHA-256 一致，完成摄入。未复现实验；Obsidian 内显示、公式及表格渲染、来源跳转未测。

返回 [[wiki/index|索引]]。
