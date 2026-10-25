---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/data-environments/TaskCraft.pdf]]"
  - "[[raw/papers/optimization/data-environments/SWE-Gym.pdf]]"
  - "[[raw/papers/optimization/data-environments/WebDreamer.pdf]]"
  - "[[raw/papers/optimization/data-environments/TOUCAN.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf]]"
---

# 数据与环境合成


综述把可训练经验拆成三个耦合对象：任务规定目标和能力压力，环境承载动作与可核查反馈，轨迹记录决策、观察、错误和恢复。记录一串文字动作，不自动等于保留了环境状态变化与验证证据。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=40|S001 · §5.2 · p.40]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=43|§5.2.3 · p.43]]

细分导航：Task Synthesis；Environment Synthesis；Trajectory Synthesis。第一轮 S037–S041 已完成摄入与本节整合，内容与结构验收通过；Obsidian 应用未测。与 [[wiki/applications/Overview|应用接口和评测]]、[[wiki/frontier/Overview|环境真实性问题]] 相连。

### 生成了什么，真实执行到了哪里

**本库比较轴：**先确认被生成的是问题、可执行环境、状态预测还是训练轨迹，再核对标签来源。“真实工具”“可验证任务”和“高质量轨迹”分别描述不同环节，不能相互替代。下表比较机制，不把不同模型与基准的分数排列成优劣。

| 生成或构建对象 | 执行与标签的来源 | 关键限定及原文 |
| --- | --- | --- |
| 任务的依赖结构 | TaskCraft 从真实工具内容抽答案，再以深度扩展替换输入索引、以宽度扩展合并子题；原子任务执行，长链主要做增量语言核查 | 设计好的路径不等于最终问题被端到端成功执行；一个 hop 也不等于一次调用。[[wiki/papers/optimization/data-environments/TaskCraft\|S037 TaskCraft]]；[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=3\|§2–3 · pp.3–6]] |
| 可执行训练环境 | SWE-Gym 将真实 issue、仓库快照、依赖和测试配套；实际运行轨迹的测试成败用于筛选策略数据及训练 verifier | 环境半手工配置；测试标签受测试覆盖限制，学习 verifier 的预测另有误差。[[wiki/papers/optimization/data-environments/SWE-Gym\|S038 SWE-Gym]]；[[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=4\|§3.1 · p.4]]、[[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=7\|§5.1.1 · p.7]] |
| 动作后的状态变化描述 | WebDreamer 先真实网页随机交互，教师根据前后截图描述变化；Dreamer-7B 学习预测这种描述，测试时用模拟辅助选动作 | 不是完整可执行网页模拟器；主实验模拟 H=1，评分器与环境真实成功反馈不同。[[wiki/papers/optimization/data-environments/WebDreamer\|S039 WebDreamer]]；[[raw/papers/optimization/data-environments/WebDreamer.pdf#page=4\|§3.2–3.3 · pp.4–6]]、[[raw/papers/optimization/data-environments/WebDreamer.pdf#page=8\|§5.1 · p.8]] |
| 合成任务与工具交互轨迹 | TOUCAN 从 MCP spec 倒推任务，教师真正调用工具，规则检查调用，模型判断完整与简洁；多轮用户由自模拟产生 | 真实返回不自动验证最终副作用；“可验证性”是质量评分维度，不是统一执行 oracle。[[wiki/papers/optimization/data-environments/TOUCAN\|S040 TOUCAN]]；[[raw/papers/optimization/data-environments/TOUCAN.pdf#page=4\|§3.1–3.2 · pp.4–5]]、[[raw/papers/optimization/data-environments/TOUCAN.pdf#page=32\|Appendix D.4 · p.32]] |
| 当前策略的在线经验 | AgentGym-RL 在独立环境实例中执行当前策略，收集观察和结局反馈，再做 RL；ScalingInter 分阶段提高交互上限 | 真正调用基准环境不等于实机实验；策略、horizon 和重置条件共同决定训练状态分布。[[wiki/papers/optimization/reinforcement-learning/AgentGym-RL\|S041 AgentGym-RL]]；[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=5\|§3.1、Fig.3 · p.5]]、[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=9\|§3.3 · p.9]] |

### 筛选不只改变质量，也改变能学到的状态

TaskCraft 保留特定 Agent 比裸 LLM 答得更好的原子任务；SWE-Gym 训练策略主要使用成功轨迹，并在 MoatlessTools 实验限制每题成功样本数，避免易题占满数据；TOUCAN 排除需凭据/特殊配置的服务器和错误调用轨迹，再按模型标签筛选。这些选择都定义了分布，而非仅从一个不变总体中“去掉噪声”。后一句是本库分析；它提醒后续检查困难状态、替代工具方案和失败恢复经验是否被保留，不表示已测出每种偏差的影响。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=19|S037 Appendix C.1 · p.19]] [[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=6|S038 §4.3 · p.6]] [[raw/papers/optimization/data-environments/TOUCAN.pdf#page=4|S040 §3.1 · pp.4–5]]

在线 RL 也不是无选择的经验收集。AgentGym-RL 的 WebArena 实验为并行 rollout 排除插入/更新/删除的 Content & Config 任务，使用 372 训练和 50 测试 query；它不支持把结果推广到完整不可逆写入任务。与之对应，WebDreamer 的在线网页规划避免通过真实回退搜索候选，但模拟可能产生不存在的动作；两者解决不同约束，不能合并成“真实环境问题已经解决”。[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=32|S041 Appendix B.1 · p.32]] [[raw/papers/optimization/data-environments/WebDreamer.pdf#page=6|S039 §4.1 · p.6]] [[raw/papers/optimization/data-environments/WebDreamer.pdf#page=8|§5.1 · p.8]]

### 从数据量到学习效果，还要保留哪层证据

公开数据规模、实际训练子集和执行预算分别登记：TaskCraft 的 SFT 实验用 3,202 条轨迹；SWE-Gym 的 OpenHands policy 用 491 条成功轨迹；TOUCAN 发布约 1.5M，实验只筛选/重平衡 119.3K。三者都提供具体训练价值的证据，却不构成“更多数据必然更好”的统一实验。SWE-Gym 的一次 OpenHands 自采样再训练还使 Lite 下降，而受限 MoatlessTools 工作流仅小幅改善，说明产生经验的策略与使用经验的方式同样重要。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=9|S037 §4.4 · p.9]] [[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=5|S038 §4.2–4.3 · pp.5–6]] [[raw/papers/optimization/data-environments/TOUCAN.pdf#page=7|S040 §4.1 · p.7]]

标签需要独立看待：TOUCAN 的任务 judge 与人工对照只有 50 样本、Kimi-K2 Pearson r=0.264；WebDreamer 的 intrinsic evaluation 则通过世界模型加评分器判断正确/偏离动作的排序，平分也算正确。前者不是全数据人工验收，后者不是逐项验证页面转移保真度。原文中的数值口径差异和实验细节留在唯一论文页。[[raw/papers/optimization/data-environments/TOUCAN.pdf#page=20|S040 Appendix C.1、Fig.13 · p.20]] [[raw/papers/optimization/data-environments/WebDreamer.pdf#page=19|S039 Appendix D.1–D.3 · pp.19–20]]

**待检验问题，尚未完成查新：**固定任务、工具版本和总预算后，生成路径是否必要、真实执行是否可达、标签是否准确、筛选后哪些状态缺失，分别能解释多少训练收益？当前五篇将这些问题拆开，尚不能据此宣布研究空白。运行时选择与验证见 [[wiki/harness/workflows#分支能否撤回，评价能否被信任|分支执行]]、[[wiki/harness/verification|验证]]；参数学习接口见 [[wiki/optimization/finetuning|微调]] 和 [[wiki/optimization/reinforcement-learning#交互上限怎样改变在线训练|在线交互课程]]。

## 论文入口与交叉方向

- [[wiki/papers/optimization/data-environments/TaskCraft|S037 · TaskCraft]]：主归属。
- [[wiki/papers/optimization/data-environments/SWE-Gym|S038 · SWE-Gym]]：主归属。
- [[wiki/papers/optimization/data-environments/WebDreamer|S039 · WebDreamer]]：主归属。
- [[wiki/papers/optimization/data-environments/TOUCAN|S040 · TOUCAN]]：主归属。
- [[wiki/papers/optimization/reinforcement-learning/AgentGym-RL|S041 · AgentGym-RL]]：交叉关联；主归属为`optimization/reinforcement-learning`。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
