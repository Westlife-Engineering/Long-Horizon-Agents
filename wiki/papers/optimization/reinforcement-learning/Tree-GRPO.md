---
type: paper
primary_direction: optimization/reinforcement-learning
source_id: S054
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf]]"
---

# Tree-GRPO：共享前缀如何改变采样与学习信号

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S054 |
| 原文标题 | Tree Search for LLM Agent Reinforcement Learning |
| 作者 | Yuxiang Ji、Ziyu Ma、Yong Wang、Guanhua Chen、Xiangxiang Chu、Liaoni Wu |
| 版本 | arXiv:2509.21240v3，2026-03-18；PDF标记ICLR 2026 |
| 原始来源 | [锁定 PDF](https://arxiv.org/pdf/2509.21240v3)；访问 2026-10-25；发布页与 PDF 首页身份已核对 |
| Raw | [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf\|本地原件，共 27 页]] |
| SHA-256 | `56B9E6F0F227F3A36868A68CE27E0939BEEA98749B76BE0976CE28E7BB362843` |
| 实际阅读 | 2026-10-25；正文pp.1–10；附录A–D pp.16–23（数据、预算、优势消融、理论假设与算法）；实际看p.4 Fig.3/Eq.4、p.5 Fig.4/Eq.6–8、p.10 Table4、p.8 Table3、p.20 Table7。附录E pp.24–27案例未完整核读；理论读假设与推导边界，未独立形式验证证明 |
| S001 入口 | 引文250，§5.5.2/5.5.3，综述pp.50–51；书目p.96；本页按实际下载版本解释，不能假定与综述所引版本完全相同 |

以下主张来自原论文直接核读，另标本库推断；未复现实验、未核读实现代码。PDF 页码从首页起算。

## 一次改变两个对象：采样树和相对优势

Tree-GRPO先并行采多条完整轨迹，再从已有轨迹的非终止节点随机选位置、复用前缀并继续生成。节点是一整个thought–action–observation步骤，树中保存观察是为了接续上下文；可训练策略动作仍是模型生成的thought/action，环境观察不是模型采样出的动作。所有实验只使用搜索工具，不能据“web-agent”名称认为已测试浏览器任意写入和回滚。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=3|§2.1、Eq.1–2 · p.3]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=4|§3.1、Fig.3 · p.4]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=6|§4.1 · p.6]]

```mermaid
flowchart LR
 A[M条独立初始链] --> B[每树随机抽N个非终止节点]
 B --> C[复用根到节点的完整历史]
 C --> D[生成新的后续与最终答案]
 D --> E[叶子答案得到终局奖励]
 E --> F[树内及跨树相对优势]
 F --> G[共享前缀下的策略更新]
 D -->|按L轮扩展| B
```

本库示意。它是训练时online rollout组织，不是测试时必须跑MCTS；扩展点随机选择，不依赖额外训练的PRM。每题得到$G=M(LN+1)$条叶轨迹；更多共享前缀减少重复生成，但减少独立初始链也收窄探索。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=4|§3.1 · p.4]]

## 为什么终局反馈会形成局部偏好

每条叶轨迹先相对本树所有叶子的奖励均值/std得到$A_{intra}$，再相对同题全部树叶子得到$A_{inter}$，两者相加。**Eq.6–8实际仍先为叶轨迹计算优势；步骤信号来自不同后缀共享前缀时，更新贡献沿共同节点累积。**不能误写为每个节点都获独立人工过程标签，或每对同胞都由一个oracle判对错。树内叶子太少时均值不稳定，跨树比较提供较稳基线。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=5|§3.2、Eqs.6–8、Fig.4 · p.5]]

作者将其解释为隐式step-level preference learning。理论结论在二元胜/负、相应概率归一化与简化优势等假设下，说明与step-DPO的梯度有相同“胜负log概率梯度差”结构，但权重不同；不是完整clipped、KL、有限采样Tree-GRPO与一般DPO算法恒等，也不直接覆盖F1连续奖励的全部设定。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=5|§3.3 · pp.5–6]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=19|Appendix C · pp.19–22]]

正式目标写token级importance ratio；附录B.3明确在token级分叉对照中排除observation作为分叉点，但没有独立完整列出主实现的observation loss-mask代码。本次未读代码，故只确认策略/环境角色，不把分叉mask与训练loss mask混为同一已核验实现。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=5|Eq.8 · p.5]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=18|Appendix B.3、Eq.14–15 · p.18]]

## 训练分布与预算

| 场景 | 训练数据/反馈 | 主要训练与工具限制 |
| --- | --- | --- |
| 单跳QA | NQ 79,168；EM | 180steps，batch512，response4096，最多3次search；本地Wiki/E5 top3 |
| 多跳QA | HotpotQA 90,447；EM | 同上；与单跳是分开训练集，不能当成统一混合训练 |
| Web QA | ASearcher抽2,000＋WebDancer200；F1 | 34steps/2epochs，batch128，response8000，最多5次search；Bing top10 |

共同学习率1e-6，KL0.001，默认链group4、树(M=2,N=2,L=1)。格式不合法扣0.2，因此“只有outcome reward”仍含格式惩罚，没有新增逐步语义标签。测试涵盖11个QA集，GAIA只用103个纯文本问题；Web QA报F1，不能与其他工作的judge成功率直接排名。GPU数/总GPU时在本次核读材料未确认。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=16|Appendix A · pp.16–17]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=17|Appendix B.1、Table5、Eq.13 · p.17]]

训练状态是原问题加根到分叉点的完整历史。前缀复用使多条样本相关，也把预算集中到既有路径附近；不能把更多叶子当成同数量独立初态探索。搜索任务可接续历史不等于任意有副作用环境可恢复到分叉状态。这个迁移前提是本库推断，与 [[wiki/harness/Overview|Harness]] 的分支可撤回性相连。

## 哪些证据分开支持采样与优势

Table4在Qwen2.5-3B多跳QA、名义约4条完整轨迹预算下：链GRPO平均31.8，树只用跨树优势33.8，树内加跨树36.8；只用树内则collapse。这支持收益同时涉及采样组织和优势构造，不能全部归给“更细信用”。增加树内分支到N=6后，单独树内不再collapse；所以稳定性依赖组规模。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=10|Table4 · p.10]]

预算对照用“若干完整轨迹的预期token/tool成本”衡量；不是严格实测等GPU小时。默认有更多叶轨迹，训练反向计算和相关样本数也改变。单跳任务深度常约2，收益较小；Web QA的BrowseComp F1仍低，作者承认训练数据难度/质量限制。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=8|Table3、§4.3 · pp.8–9]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=7|§4.2 · p.7]]

> [!note]- 预算表达需复核，不按印刷式直接估价
> §3.1定义每棵树每轮扩N个点，并给叶数M(LN+1)，但Eq.4写预期成本MB+LNB/2。按其每树扩展措辞，扩展项是否应包含M需要核对实现；Table3的M=2,N=2,L=1列为约4预算，而直接代入印刷Eq.4为3B。Table7还把相同默认配置列于“约2”分组，与Table3口径不同。本页保留此张力，不据此定性整体算法错误，也不把近似预算当成本承诺。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=4|§3.1、Eq.4 · p.4]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=8|Table3 · p.8]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=20|Table7 · p.20]]

与 [[wiki/papers/optimization/reinforcement-learning/GiGPO|GiGPO]] 比较：GiGPO不增加rollout、在自然重复状态后事后分组；Tree-GRPO主动从共享历史扩展分支。前者依赖状态匹配，后者依赖前缀可接续及预算分配；二者均未提供逐步真实因果标签。下一条值得核查的证据是实测token、调用、训练时长均匹配时的增益分解，尚未做完整查新。

## 主题联系与状态

已整合 [[wiki/optimization/reinforcement-learning|Optimization：Agentic RL]] 的状态分布、反馈与信用比较。与 [[wiki/harness/Overview|Harness]] 的状态和反馈接口保持交叉联系。本篇内容与结构验收通过，已完成摄入；主题、队列、索引及摄入日志已同步。按用户要求本轮不做Obsidian应用检查，应用未测；未复现实验。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/reinforcement-learning|optimization/reinforcement-learning]]。
