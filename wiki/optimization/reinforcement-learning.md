---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/Search-R1.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/ToolRL.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf]]"
  - "[[raw/code/S053-GiGPO/20bd331bdbc9026a5668e11362178e10ab7400c8/agent_system/environments/env_manager.py]]"
  - "[[raw/code/S053-GiGPO/20bd331bdbc9026a5668e11362178e10ab7400c8/gigpo/core_gigpo.py]]"
  - "[[raw/code/S053-GiGPO/20bd331bdbc9026a5668e11362178e10ab7400c8/verl/workers/actor/dp_actor.py]]"
  - "[[raw/papers/optimization/reinforcement-learning/C3.pdf]]"
  - "[[raw/papers/harness/verification/AgentPRM-Xi.pdf]]"
  - "[[raw/papers/harness/memory/ReSum.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf]]"
---

# Agentic Reinforcement Learning


Agentic RL 用自身交互反馈优化策略，目标从单次回答扩展为多轮轨迹。综述拆成四个问题：怎样分配成功/失败的信用、怎样稳定更新策略、采哪些轨迹，以及怎样组织层级、多 Agent 或记忆交互。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=47|S001 · §5.5 · Fig.12 · pp.47–48]]

| 子方向 | 主题入口 | 原文定位 |
| --- | --- | --- |
| Credit Assignment | 终局、过程与显式评价准则（rubric）信用；判断哪些决策造成结果 | §5.5.1，p.48 |
| Policy Optimization | 裁剪式更新、按轮次优化、维持探索；将信用转成参数更新 | §5.5.2，p.50 |
| Sampling Strategy | 轨迹采样、树采样、预算控制；决定获取哪些交互经验 | Fig.12，p.47；§5.5.3 起于 p.50 |
| Interaction Patterns | 层级、多 Agent、记忆学习；决定训练交互的结构 | Fig.12，p.47；§5.5.4 起于 p.51 |

表格入口依据 [[raw/surveys/Towards Long-Horizon Agents.pdf#page=47|Fig.12]]、[[raw/surveys/Towards Long-Horizon Agents.pdf#page=48|§5.5.1]] 与 [[raw/surveys/Towards Long-Horizon Agents.pdf#page=50|§5.5.2–5.5.3]]；不是这些子方向有效性的比较。过程奖励与 [[wiki/harness/verification|运行时验证]] 相关，但需要分别检查判断偏差与优化后的行为。

### 先确认训练中是谁产生状态，谁提供反馈

第一轮S051–S055已完成原文核读、主题整合与内容/结构验收，已计入完成摄入；应用未测。**本库比较轴：**同样使用PPO/GRPO，可能学习当前策略的完整交互，也可能学习固定历史上的单步回复，或学习记忆模块；奖励稠密程度必须与这些条件一起看。

| 决策与训练状态 | 反馈来源和信用单位 | 必须保留的条件 |
| --- | --- | --- |
| 当前策略生成搜索词，检索结果追加进历史，再搜索或回答 | Search-R1用最终答案EM；PPO用critic/GAE，GRPO比较同题完整rollout | 检索token是观察，进入上下文但排除策略梯度和GRPO KL；主要为固定Wiki/E5、4动作。[[wiki/papers/optimization/reinforcement-learning/Search-R1\|S051]]；[[raw/papers/optimization/reinforcement-learning/Search-R1.pdf#page=4\|§3.1–3.4 · pp.4–6]]、[[raw/papers/optimization/reinforcement-learning/Search-R1.pdf#page=16\|Appendix B.2 · p.16]] |
| 给定历史下生成下一步工具调用 | ToolRL按标准调用的工具名、参数名和值给部分匹配分，再合成回复级reward | **训练多步数据拆成带历史单步实例**，需要每步标准调用；不是完整在线轨迹探索。[[wiki/papers/optimization/reinforcement-learning/ToolRL\|S052]]；[[raw/papers/optimization/reinforcement-learning/ToolRL.pdf#page=4\|§2.3 · p.4]]、[[raw/papers/optimization/reinforcement-learning/ToolRL.pdf#page=5\|§3.1 · p.5]] |
| 同任务、同初态采完整轨迹，再寻找重复环境状态 | GiGPO同时比较整条总回报和同状态后动作的折扣回报 | 不增rollout，依赖重复覆盖与状态匹配；局部优势不是额外过程标签。[[wiki/papers/optimization/reinforcement-learning/GiGPO\|S053]]；[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf#page=5\|§4.2–4.3 · pp.5–6]] |
| 从多条初始链随机挑中间节点，共享前缀并扩展后缀 | Tree-GRPO比较叶轨迹在本树和同题全部树中的奖励，利用共享节点形成局部更新贡献 | 同时改变采样相关性、独立探索与优势；只测试搜索工具。[[wiki/papers/optimization/reinforcement-learning/Tree-GRPO\|S054]]；[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=4\|§3.1–3.2 · pp.4–5]]、[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=6\|§4.1 · p.6]] |
| 新信息与旧记忆决定编辑操作；问题与检索集合决定回答 | Memory-R1以最终QA EM训练Manager或Answer，另一组件固定 | 分阶段训练；预构造记忆与回答器影响信号；**LongMemEval为oracle版**。[[wiki/papers/optimization/reinforcement-learning/Memory-R1\|S055]]；[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=4\|§3 · PDF pp.4–5 / 印刷12808–12809]]、[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=14\|Appendix B · PDF p.14 / 印刷12818]] |

Search-R1和ToolRL说明“有反馈”仍需分清反馈来自哪里：前者最终答案可验证，不直接评价每次查询；后者借助标准调用分解部分正确，但没有证据证明所有等效路径都得到相同奖励。ToolRL的BFCL总体提高与Multi Turn仍低可以并存，不能把调用匹配提升等同于长程可靠完成。更长输出也不是更强能力的统一代理：其长度奖励对多数所测小模型降低BFCL。[[raw/papers/optimization/reinforcement-learning/Search-R1.pdf#page=6|S051 §3.4 · p.6]] [[raw/papers/optimization/reinforcement-learning/ToolRL.pdf#page=4|S052 §2.3 · p.4]] [[raw/papers/optimization/reinforcement-learning/ToolRL.pdf#page=6|Table1 · p.6]] [[raw/papers/optimization/reinforcement-learning/ToolRL.pdf#page=9|Fig.4 · p.9]]

### 局部比较组从哪里来，决定了什么可被区分

GiGPO和Tree-GRPO都从后续结果构造较细信号，却不取得新的逐步正确性oracle。GiGPO在已有rollout中事后聚合相同环境状态；折扣回报让同一成功轨迹中较早绕路与较晚有效动作可被区分，再与episode优势相加。Tree-GRPO主动从共享前缀采新后缀，先为叶轨迹计算树内/跨树优势；共享节点上的梯度贡献把分支结果联系起来。后者的理论是特定二元假设下与step-DPO具有相同梯度结构、权重不同，不能升级为完整算法恒等。[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf#page=5|S053 Eq.5–9 · pp.5–6]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=5|S054 Eq.6–12 · pp.5–6]]

两者有不同前提。GiGPO论文在ALFWorld/WebShop使用最近两步历史与当前观察，QA保留全历史并采用相似度分组；因此相同观察不必代表完整policy上下文相同。Tree-GRPO使用根到节点的完整历史接续搜索；这不证明外部有副作用环境可恢复到同一状态。跨环境分支条件见 [[wiki/harness/workflows#分支能否撤回，评价能否被信任|Harness分支接口]]。[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf#page=18|S053 Appendix E.2 · pp.18–19]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=4|S054 §3.1 · p.4]]

**S053公开实现补充：**锁定commit `20bd331`后可确认，分组anchor与加入历史、步数等信息的policy输入分别保存；同轨迹重复访问可同组，step均值包括自身，可选只减均值或再除std，合成优势后才进入actor的clip。它支持“分组条件不等于完整策略上下文”的窄判断；若将排序解释成同一决策条件下的动作差异，还需核对组内相关信息，不能反推历史不同就令算法不成立，或已造成有偏/性能损害。当前公开commit未证明等于论文实验版本；具体代码行、实际组样本缺口和进一步实现边界见 [[wiki/papers/optimization/reinforcement-learning/GiGPO#公开实现核查：分组观察与策略输入分别保存|S053唯一页]]。[[raw/code/S053-GiGPO/20bd331bdbc9026a5668e11362178e10ab7400c8/agent_system/environments/env_manager.py|环境管理器 L138–208、390–505]]；[[raw/code/S053-GiGPO/20bd331bdbc9026a5668e11362178e10ab7400c8/gigpo/core_gigpo.py|分组与优势 L153–171、243–384]]；[[raw/code/S053-GiGPO/20bd331bdbc9026a5668e11362178e10ab7400c8/verl/workers/actor/dp_actor.py|actor L365–424]]。

**分开检查采样收益与优势收益。**Tree-GRPO的3B多跳QA消融在名义约4条完整轨迹预算下，链GRPO平均31.8，树仅跨树优势33.8，树内加跨树36.8；小组仅树内优势会collapse。它支持两部分共同作用，不能把总增益全归于精细信用。GiGPO删除episode或step信号均损害所测表现，也不表示任意状态分组都正确。两篇预算口径、匹配误差与具体训练设置留在唯一论文页，不能跨任务排名。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=10|S054 Table4 · p.10]] [[raw/papers/optimization/reinforcement-learning/GiGPO.pdf#page=9|S053 §5.4、Fig.4 · p.9]]

**同一前缀的反事实何时能成为参照？**综述外补读[[wiki/papers/optimization/reinforcement-learning/C3|S068 C3]]把条件写得更明确：恢复记录前缀后注入替代消息，所得后续消息/奖励分布须等于恢复完整真实状态后的分布。因果相关变量必须能记录并恢复，或按给定前缀的正确条件分布重采样；未恢复的外部副作用、记忆或路由属于隐藏状态，不受保证。满足条件后，冻结本轮行为策略，采独立替代消息并分别继续到终局，再减去其他替代的平均回报，才得到作者所定义的消息级优势估计；非自适应接续次数也是无偏前提。[[raw/papers/optimization/reinforcement-learning/C3.pdf#page=4|S068 §2.3–2.4、Eq.2 · pp.4–5]] [[raw/papers/optimization/reinforcement-learning/C3.pdf#page=16|A.2 · p.16]]

这与GiGPO事后聚合同观察、Tree-GRPO共享前缀采样是不同的比较条件。C3还用不共享rollout的独立接续作参照，检验信用排序；但其2–10决策点诊断主要是冻结数学工作流的**开头决策点**，同每点预算下10点链可靠性仍约0.01。无偏不等于有限预算下排序可靠，也不验证GiGPO组内历史差异已造成损害。训练另有2/3角色数学任务，共享前缀与优势同时变化，MAPPO基线还有长度归一化差异，不能将总收益只归于信用估计。[[raw/papers/optimization/reinforcement-learning/C3.pdf#page=7|Table1 · p.7]] [[raw/papers/optimization/reinforcement-learning/C3.pdf#page=26|B.5 · p.26]] [[raw/papers/optimization/reinforcement-learning/C3.pdf#page=28|B.7 · pp.28–29]] [[raw/papers/optimization/reinforcement-learning/C3.pdf#page=23|B.2–B.4 · pp.23–25]]

### 过程评分怎样进入策略更新

[[wiki/papers/harness/verification/AgentPRM-Xi|S028 AgentPRM-Xi，已完成摄入]] 以环境终局回报与TD/GAE目标训练步骤价值，并约束相邻价值差；这是奖励模型的过程训练。其Qwen2.5-3B在BabyAI/TextCraft上的PPO实验却以**末步PRM预测作为整条轨迹奖励**，不能描述为逐步密集奖励实验。推理阶段另有BoN与beam选择，比较见 [[wiki/harness/verification#选择误差与纠错净收益要分别测量|Harness · 验证]]。过程评分如何产生、何时用于选择、何时发放训练奖励须分别登记；确定性转移/稀疏奖励假设、bootstrap标签与策略分布条件也不会因接入PPO而消失。[[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=6|§3.2–3.3 · pp.6–8]] [[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=11|§5.2 · p.11]] [[raw/papers/harness/verification/AgentPRM-Xi.pdf#page=22|Appendix C · p.22]]

### 记忆写入和使用也能成为训练接口

Memory-R1把运行时可变记忆接到参数学习：Manager输出编辑操作与内容，Answer从60个检索候选中选择证据并回答；训练Manager时Answer冻结，训练Answer时Manager固定。反馈是最终QA EM，而非每条记忆都获正确性标签。冻结另一方减少训练漂移，但本库推断仍须保留回答器依赖：保存了正确事实，也可能因回答器不会使用而得零；对当前QA有效，也未证明对未知未来问题有效。[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=4|S055 §3 · PDF pp.4–5 / 印刷12808–12809]] [[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=18|Appendix E · PDF p.18 / 印刷12822]]

“152训练QA”不包含基础模型、GPT-4o-mini构造记忆、检索和RL反复采样成本。正文和伪代码对临时记忆的24/50turn及重置过程存在待核查差异；跨集LongMemEval是oracle版本，不能写成完整大记忆库端到端检索迁移。与 [[wiki/harness/memory|Harness记忆机制]] 的联系，是明确哪些信息能进入未来决策；与下述ReSum的联系，是运行状态接口与策略适应训练共同决定效果。[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=14|S055 Appendix B.2 · PDF p.14 / 印刷12818]] [[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=20|Algorithm5 · PDF p.20 / 印刷12824]]

### 摘要接续怎样进入策略训练

[[wiki/papers/harness/memory/ReSum|ReSum]] 给出一项已核读的跨模块实例：[[wiki/harness/memory|Harness]] 在摘要后把输入重置为“原问题＋摘要”；ReSum-GRPO 则以这些摘要点分段，把最终答案的二值奖励归一化为轨迹级 advantage，广播到该轨迹各段，工具观察不计策略损失。因此运行时状态接口直接决定训练看到的状态和 rollout 结构；广播终局信号不等于识别了每段独立因果贡献。[[raw/papers/harness/memory/ReSum.pdf#page=4|S011 §3.3、Figure 3 · pp.4–5]]

**归因边界：**training-free ReSum 只指现成策略不再训练，默认摘要器 ReSumTool-30B 自身已蒸馏训练。普通 GRPO 与 ReSum-GRPO 虽共享部分超参数，训练工具调用上限却为 40 对 60，且接续改变了可采到的长轨迹；Table 2 的效果不能全部归于 advantage broadcasting。后续比较需同时登记反馈、状态表示、探索机会与预算，而不能仅按算法名排列。[[raw/papers/harness/memory/ReSum.pdf#page=4|S011 §3.2 · p.4]] [[raw/papers/harness/memory/ReSum.pdf#page=15|S011 附录 D.2 · p.15]] [[raw/papers/harness/memory/ReSum.pdf#page=7|S011 Table 2 · p.7]]

### 交互上限怎样改变在线训练

[[wiki/papers/optimization/reinforcement-learning/AgentGym-RL|AgentGym-RL]] 的 ScalingInter 先限制每条在线轨迹的最大轮数，再随训练阶段提高上限。它改变可访问的路径和由当前策略采到的状态，区别于只对固定示范排序，也区别于测试时多试几次。Deep Search 的固定5轮/10轮与渐增轮数曲线支持该设定下的稳定性折中；未匹配全部环境调用/token 的结果，不能把收益只归于课程顺序。[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=9|S041 §3.3 · p.9]] [[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=12|§4.2、Fig.7 · p.12]]

这与 ReSum 的比较共同提出一个归因要求：**状态接口、探索机会与更新算法须分别记录。** AgentGym-RL 的主实验在数字环境中按环境训练，作者承认 in-domain 与物理任务边界；其测试 Pass@K 说明候选覆盖，不证明系统能选对一个结果。具体环境筛选见 [[wiki/optimization/data-environments#筛选不只改变质量，也改变能学到的状态|数据分布]]，不能用“无需 SFT”消除基础模型预训练与环境配置成本。[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=16|S041 §5.1 · pp.16–17]] [[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=21|§7 · p.21]]

## 论文入口与交叉方向

- [[wiki/papers/harness/memory/ReSum|S011 · ReSum]]：交叉关联；主归属为`harness/memory`。
- [[wiki/papers/optimization/reinforcement-learning/AgentGym-RL|S041 · AgentGym-RL]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/Search-R1|S051 · Search-R1]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/ToolRL|S052 · ToolRL]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/GiGPO|S053 · GiGPO]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/Tree-GRPO|S054 · Tree-GRPO]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/Memory-R1|S055 · Memory-R1]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/C3|S068 · C3]]：主归属。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
