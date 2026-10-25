---
type: paper
primary_direction: optimization/distillation
source_id: S058
created: 2026-10-25
updated: 2026-10-25
reading_status: targeted-fulltext-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/distillation/MAD-OPD.pdf]]"
---

# MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate

## 来源身份与读取范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S058 |
| 作者 | Jianze Wang、Ying Liu、Jinlong Chen、Xuchun Hu、Qilong Zhang、Yu Cao、Jun Wang、Hua Yang、Yong Xie、Qianglong Chen |
| 版本 | arXiv:2605.01347v1；预印本，正式发表状态未确认 |
| 原始页面 | [arXiv版本页](https://arxiv.org/abs/2605.01347v1)；[版本PDF](https://arxiv.org/pdf/2605.01347v1)；访问2026-10-25 |
| DOI | 10.48550/arXiv.2605.01347（arXiv标识） |
| 原件 | [[raw/papers/optimization/distillation/MAD-OPD.pdf\|本地PDF · 28页]] |
| SHA-256 | `659E8625E1D6FFD33B36E490CD7E0CB2E828EF0DF231BE0788E460BEA08B4971` |
| S001引用 | 引文635；§5.6.1，PDF pp.53；书目p.126 |
| 读取日期与范围 | 2026-10-25；正文pp.1–10；附录A、B.1–B.12、C.1–C.7、D.1–D.6（pp.12–24），E案例入口p.24。看图核对p.6流程/权重/目标、p.13训练与选模型、p.17消融、pp.22–23理论推导。E余下案例pp.25–28未逐项核读；没有核查代码或复现实验。 |

## 核心理解：把讨论内容变成教师侧的特权上下文

**原文陈述。** 学生先在当前状态生成动作；两位教师先独立回答，再读彼此答案修订，完整讨论只供教师看。每位教师在学生已经采样的动作前缀上输出token分布，学生不看讨论。更新目标是**各教师散度的加权和**，不是直接模仿一段多数票答案，也不是先平均教师概率再统一求散度。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=5|§4.1 · p.5]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=6|§4.2–4.3、Figure 2、Eq.8 · p.6]]

| 组成 | 实际信号 | 限制 |
| --- | --- | --- |
| 学生状态/动作 | 当前历史下学生生成action | token on-policy不自动保证环境历史也是在线采样 |
| 教师信息 | K=2、R=2的讨论历史 | 教师共享讨论，不代表判断独立 |
| 权重 | 自报0–100置信度除100，再做温度1的softmax | 不是外部正确性校准；高置信仍可能错 |
| agentic目标 | 对称JSD，β=0.5 | 不用稀疏终局奖励的policy gradient |
| code目标 | reverse KL：KL(学生‖教师) | 本文任务选择，非所有代码分布的定理 |

依据 [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=6|§4.2–4.4、Eqs.6–10 · pp.6–7]] 与 [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=13|B.3–B.5 · p.13]]。教师logits固定、梯度只流入学生，采样路径停止梯度；因此作者“dense token-level RL”是surrogate解释，不能与完整回报梯度等同。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=20|D.1、Eq.11 · p.20]]

## OPAD的循环描述与实验数据边界

§4.4与Algorithm 1把OPAD写成“学生动作→环境观察→下一轮”并逐步蒸馏：每个action内部取token均值，再对各环境步求和。**但B.3将ToolACE轨迹拆成约16K独立step样本，给定先前对话/工具历史，在该步生成动作。** 仅凭当前PDF，尚未充分说明训练时所有后续历史均由学生实际动作重新推进环境得到，不能把独立step训练直接写成完整长程在线环境rollout。需代码核查的这一区别不否定其step级监督实验。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=7|§4.4、Eqs.9–10 · p.7]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=12|Algorithm 1 · p.12]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=13|B.3 · p.13]]

## 实验证据与可比较范围

六组Qwen3/Qwen3.5师生配置；agentic与code分别训练checkpoint，ToolACE约16K与OpenThoughts3 30K，均non-thinking、1 epoch。agentic评BFCL-v4、τ²-Bench、VitaBench；code评LCB-v6、MBPP+。单教师OPD用同组较强教师，另有无讨论等权MT-OPD和7:3教师序列混合MT-SeqKD。Table 1支持本配方在六组overall平均上的改善；“每组最佳平均”不等于每个任务都最佳。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=7|§5.1–5.3、Table 1 · pp.7–9]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=13|B.3–B.6 · pp.13–14]]

14B+8B→4B的散度消融中，JSD的agentic均值25.69，reverse KL为22.16；code均值则reverse KL 48.12，JSD 44.71。这是同一配方内的任务依赖观察。讨论与权重消融有帮助，但不证明模型共识本身增加独立事实证据。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=16|C.1、Table 3 · p.16]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=17|C.2、Table 4 · p.17]]

必须保留三个评测条件：

- BFCL与LCB用于反复选择checkpoint，不是完全未参与选择的测试集；τ²、Vita、MBPP+才按B.6未用于选择。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=13|B.6 · p.13]]
- τ²与Vita排除未正常执行episode，包含API错误及malformed tool call导致崩溃，要求正常执行比例≥90%；因此分数不是所有发起任务的端到端成功率。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=15|B.9–B.10 · p.15]]
- code pass@1用16个解码seed平均，agentic只一次run。BoN@16依测试通过数选择，是有测试反馈的候选选择口径，不是额外训练seed或无验证器的自主选择能力。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=13|B.6 · p.13]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=17|C.4 · pp.17–18]]

训练还需要可访问全词表概率、师生同词表和多教师讨论开销；8×H20的4B运行约agentic16小时/code32小时是作者配置记录，不是本库复现或对其他硬件保证。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=9|Limitations · pp.9–10]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=12|B.2 · p.12]]

## 理论主张的适用前提：本库数学核查

**作者主张。** §3.2–3.3把JSD的逐位置logit梯度有界，与reverse KL的模态集中解释，组合为任务自适应选择规则。D.4明确有界对象是堆叠的各位置logits，参数梯度仍通过共享θ累加；不能将其升级成任意长轨迹参数更新稳定性保证。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=4|§3.2–3.3 · pp.4–5]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=22|D.4 · pp.22–23]]

**本库数学核查：现有假设不支持单模态全局最优或普遍收敛。** D.3将可行对象写成softmax参数化分布，p为不相交支持的混合；Eq.27化为KL(μ‖α)，却将集中最大模态的正成本−logαmax称为最优。取两token词表、两个单点模态，权重0.6/0.4，则$q=p=(0.6,0.4)=\operatorname{softmax}(\log0.6,\log0.4)$可行且KL为0；集中一个模态的成本−log0.6反而大于0。q=p处梯度也为0，因此现有假设同样不支持从任意初始化都收敛到单模态。已核读定义和证明没有额外的单峰、确定性或单一支持分量约束；这是针对原文陈述的解析核查，不是实验结果或作者承认的更正。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=3|§3.1–3.3 · pp.3–5]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=22|D.3、Eqs.26–28 · p.22]]

支持不相交只禁止在所有合法支持的并集之外放质量，不能禁止同时覆盖多个合法模态。若另限定q只能支撑于一个模态且能精确表示它，才可在各分支的−logα值中选最大权重模态；实际网络容量、参数耦合或梯度估计导致mode seeking，需要另外明确条件。D.5从forward-KL/JSD匹配多模态直接推断代码必然拼接不一致，也缺少位置间条件被破坏的机制：若q精确匹配完整教师的各前缀条件分布，采样复现的是教师序列分布。故不将“代码必须用reverse KL”作为普遍保证。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=22|D.3 · p.22]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=23|D.5 · p.23]]

这项核查与两类证据分开：D.4针对固定教师、堆叠位置logits的特定界可以保留，reverse KL也存在无统一有限界的分布构造；它们不保证共享参数训练的全局稳定。Table 4仍是特定配方下JSD-agentic、reverse-KL-code更好的经验观察，上述反例不否定该表或整篇方法。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=17|C.2、Table 4 · p.17]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=22|D.4 · pp.22–23]]

**本库综合。** 本文新增的可靠理解是“同一学生采样位置可获得讨论条件化的不同教师目标”，以及散度选择需要任务实证；现有假设下的通用最优定理不获数学支持，完整在线环境状态覆盖仍待实现核查。其他多教师工作未逐篇核读，新颖性比较仍为作者说法。候选问题暂不升级，先完成上述证据核查。

## 主题联系与维护状态

已整合到 [[wiki/optimization/distillation|Optimization · OPD]]；当前已完成摄入，内容与结构已验收。原件存在与哈希已核对；Obsidian渲染、公式、Mermaid及跳转未测（本轮已停用Computer Use）。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/distillation|optimization/distillation]]。
