---
type: paper
source_id: S028
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/AgentPRM-Xi.pdf]]"
---

# AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress

## 评估行动的前景与进展，而不是给每一步贴对错标签

**身份边界：**这里是 Xi 等人的 *Step-Wise Promise and Progress*（2511.08325），不是 Choudhury 的同名 AgentPRM（2502.10325，未纳入本文直接证据）。S001 的会议条目与本次预印本作者/版本不完全一致，主张只对应归档 v1。

**原文机制：**AgentPRM 学习行动后取得终局回报的预期值（promise），同时约束相邻行动价值变化（progress）。例如暂时离开目标页面去登录，可能是之后发帖的必要步骤，不能只按页面距离判错。这里的“离目标近”是策略条件下的预期回报，不是几何距离或正确性证明。[[raw/papers/AgentPRM-Xi.pdf#page=5|§3.1–3.2 · pp.5–6]]

$$Q^\pi(s_t,a_t)=\mathbb E_{\tau\sim\pi(\cdot\mid s_t,a_t)}[r(u,\tau)],\qquad
\mathcal L=\mathcal L_Q+\beta\mathcal L_A.$$

$\mathcal L_Q$ 拟合价值标签，$\mathcal L_A$ 拟合相邻预测值之差与目标值之差。这个表达依赖论文的**确定性状态转移、非终局稀疏奖励**条件，不能直接搬到随机转移或中间密集奖励环境。[[raw/papers/AgentPRM-Xi.pdf#page=5|Eq.2–4 · p.5]] [[raw/papers/AgentPRM-Xi.pdf#page=6|Eq.5–10 · p.6]]

| 阶段 | 获得什么反馈 | 实际改变对象 |
| --- | --- | --- |
| 奖励模型训练 | 采样轨迹的环境终局回报；当前模型预测与 TD/GAE 构造中间目标 | 奖励模型参数，联合拟合 promise/progress |
| 推理 Best-of-N | 对完整候选轨迹评分，使用末步分数选一条 | 候选选择；不是给策略新增真值反馈 |
| 推理 beam search | 每步展开行动并由 PRM 保留高分候选 | 搜索路径与计算分配 |
| PPO 实验 | **末步 PRM 预测作为整条轨迹 reward** | 策略参数；不能描述成逐步密集奖励实验 |

证据：[[raw/papers/AgentPRM-Xi.pdf#page=4|§2 · p.4]] [[raw/papers/AgentPRM-Xi.pdf#page=7|§3.3 · pp.7–8]] [[raw/papers/AgentPRM-Xi.pdf#page=22|Appendix B/C · pp.22–23]]。终局目标直接取环境奖励，中间标签仍包含 bootstrap 估计误差；“自动标注”不等于获得无误的过程真值。

## 实验范围与成本口径

AgentGym 中 WebShop 最长6次交互，BabyAI/TextCraft 最长20次，评测分别100/90/97条 query。WebShop 与 TextCraft 报 success rate，BabyAI 报 reward；三任务平均图不能无条件解释成统一成功率。主要 backbone 含 Qwen2.5-0.5B/3B，另有7B、Llama3.1-8B分析；策略先用300条轨迹初始化，奖励模型每 query 取16条 TD 轨迹。[[raw/papers/AgentPRM-Xi.pdf#page=9|§4.1 · pp.9–10]]

Table 1 的 Qwen2.5-3B、WebShop、8×8 beam 条件下，AgentPRM 76.0、PVM 54.5；该差异属于固定环境与搜索协议下的模型比较。相反0.5B BabyAI 的2×2条件 AgentPRM 82.9低于PVM 84.6，故正文的 consistently 不能解读为每一格都领先。SFT/RFT用 greedy，搜索使用额外候选预算，不能将二者差异全部归因于训练目标。[[raw/papers/AgentPRM-Xi.pdf#page=8|Table 1 · p.8]] [[raw/papers/AgentPRM-Xi.pdf#page=10|§4.1.4–4.2 · p.10]]

作者的“8倍计算效率”来自候选数量与匹配性能的 BoN 曲线，不是整条系统的墙钟加速保证。Table 3 的 MC/TD 对照以**生成训练标签所采样的 tokens**计费，MC还需从每一步额外 rollout；这又与推理时效率不同。[[raw/papers/AgentPRM-Xi.pdf#page=2|Fig.1 · p.2]] [[raw/papers/AgentPRM-Xi.pdf#page=12|§5.4、Table 3 · p.12]]

**局限与待核查：**奖励模型高分不保证终局成功，Fig.7成功/失败行动的分布比较不是误报率校准；离线采样训练、部署策略变化与搜索对极端高分的偏好仍需单独评估。beam 分支依赖可执行候选/恢复状态的环境接口，本文未证明在有不可逆副作用的生产环境适用。论文伪代码对状态拼接、环境交互和索引有简化，本库未以此推断代码错误。[[raw/papers/AgentPRM-Xi.pdf#page=12|§5.5、Fig.7 · p.12]] [[raw/papers/AgentPRM-Xi.pdf#page=23|Algorithm 2 · p.23]]

## 已有比较与下一条证据

与已读 [[wiki/papers/SWE-Gym|SWE-Gym]] 的共同点是学习验证器用于选择；差别在于本文显式约束步骤间价值差，并提供搜索和PPO示例。本文对其他PRM的定位属于作者相关工作归纳，未读取原作的条目不能作为本库直接结论。[[raw/papers/AgentPRM-Xi.pdf#page=21|Appendix A、Table 4 · p.21]]

**本库推断：**应将“过程训练目标”“推理选择粒度”“RL奖励实际发放粒度”分开登记；三者在这篇论文中并不相同。若后续研究奖励训练接口，先核对可观察性、终局标签、策略分布与总环境交互预算，而不是把步骤评分天然视为可靠信用分配。当前不据此新建研究缺口。

## 来源身份与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S028 |
| 作者 | Zhiheng Xi、Chenyang Liao、Guanyu Li、Yajie Yang、Wenxiang Chen、Zhihao Zhang、Binghai Wang、Senjie Jin、Yuhao Zhou、Jian Guan、Wei Wu、Tao Ji、Tao Gui、Qi Zhang、Xuanjing Huang |
| 版本 | arXiv v1，提交日期2025-11-11；PDF 首页标2025-11-12，按该预印本锁定 |
| 标识符 | arXiv:2511.08325v1；DOI:10.48550/arXiv.2511.08325 |
| 原始入口 | [发布页](https://arxiv.org/abs/2511.08325)；[本次 PDF](https://arxiv.org/pdf/2511.08325v1) |
| 原件 | [[raw/papers/AgentPRM-Xi.pdf\|AgentPRM-Xi.pdf · 23 页]] |
| SHA-256 | `EFB13B8BBF1630CC4C2DA65EB594FD1FA249AB20D34472396F2418D962646745` |
| 获取与阅读日期 | 2026-10-25；下载原字节以不覆盖方式归档，身份按该 PDF 首页核对 |
| S001 追索 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=35\|§4.6.2；Table 4 · PDF pp.35,36 · 引文 702]]；参考文献 PDF pp.132 |

核读正文 PDF pp.1–13，Appendix A–D pp.21–23；查看 p.3 Fig.2、p.6 Eq.5–10、p.8 Table 1/Eq.13–14、p.22 Algorithm 1与PPO配置图像。参考文献未逐篇追读；未检查实现代码或复算曲线。PDF 与印刷页码相同。

**主题整合：**已整合至 [[wiki/harness/Overview#验证|Harness · 验证]]，内容与结构已验收。同时整合至 [[wiki/optimization/Overview#过程评分怎样进入策略更新|Optimization · 过程评分与策略更新]]。尚未复现实验；按本轮要求不进行ComputerUse，Obsidian公式、表格、折叠、来源跳转及宽窄窗口均未实测。
