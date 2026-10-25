---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/finetuning/AgentTuning.pdf]]"
  - "[[raw/papers/optimization/finetuning/ATLAS.pdf]]"
  - "[[raw/papers/optimization/finetuning/Agent-Distillation.pdf]]"
  - "[[raw/papers/optimization/finetuning/Agent-R.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf]]"
  - "[[raw/papers/optimization/finetuning/Toolformer.pdf]]"
  - "[[raw/papers/harness/tools/CodeAct.pdf]]"
  - "[[raw/papers/optimization/data-environments/TaskCraft.pdf]]"
  - "[[raw/papers/optimization/data-environments/SWE-Gym.pdf]]"
  - "[[raw/papers/optimization/data-environments/TOUCAN.pdf]]"
  - "[[raw/papers/optimization/data-environments/WebDreamer.pdf]]"
---

# 微调


监督微调（SFT）用整理过的轨迹教授交互方式，例如分解目标、调用工具、解释观察、恢复和终止。综述的三个入口是示范选择与混合、课程学习、蒸馏；其覆盖范围受到监督轨迹分布的限制。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=45|S001 · §5.4 · p.45]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=47|§5.4 小结 · p.47]]

细分导航：Instruction Selection and Mixing；Curriculum Learning；Distillation。第一轮 S047–S050 已完成摄入与本节整合，内容与结构验收通过；S041复用已完成来源，不重复计数。Obsidian应用未测。

### 状态由谁产生，哪些输出受到监督

**本库比较轴：**“用了SFT”只说明更新目标，不能单独说明数据是固定教师生成，还是当前策略重新采集。再问模型学习全部输出、部分关键步骤，还是错误后的修订后缀，才看清这些训练方法的差别。以下比较机制和成立条件，不跨任务排列分数。

| 状态与数据来源 | 参数更新实际学习什么 | 必须保留的边界 |
| --- | --- | --- |
| AgentTuning：教师在六类任务中交互，筛选后固定为AgentInstruct，与通用对话混合 | 模型输出的监督最大似然；通用对话帮助维持能力 | 主要覆盖教师访问状态；Mind2Web是teacher-forced单步；混合不保证每项通用指标无损。[[wiki/papers/optimization/finetuning/AgentTuning\|S047]]；[[raw/papers/optimization/finetuning/AgentTuning.pdf#page=4\|§2.1–2.2 · PDF pp.4–5 / 印刷 pp.3056–3057]] |
| ATLAS：既有专家轨迹，由GPT-4o按计划/观察/动作/纠错语义选步骤 | 完整轨迹仍输入，仅选中的thought/action计loss | 至多30%指步骤监督覆盖，不是总输入或总成本；选择不直接产生学生失败状态。[[wiki/papers/optimization/finetuning/ATLAS\|S048]]；[[raw/papers/optimization/finetuning/ATLAS.pdf#page=4\|§3.2–3.3 · PDF p.4 / 印刷 p.25337]] |
| Agent Distillation：教师在检索/代码环境生成并按答案筛选轨迹，FTP改变教师首个thought前缀 | 学生监督学习thought/action，环境观察不计loss | 固定教师状态；SAG是额外测试时采样与执行筛选，不能归入训练收益。[[wiki/papers/optimization/finetuning/Agent-Distillation\|S049]]；[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=4\|§4、Eq.4–5、Fig.3 · pp.4–5]] |
| Agent-R：每轮当前actor用MCTS采集好坏分支，再判错并构造修复轨迹 | 好轨迹＋修复信号/后续的SFT，混入通用对话；下轮重新采集 | 当前策略采样不自动等于RL或逐步OPD；树搜索、筛选与拼接都改变训练分布。[[wiki/papers/optimization/finetuning/Agent-R\|S050]]；[[raw/papers/optimization/finetuning/Agent-R.pdf#page=6\|§3.1–3.2 · pp.6–7]] |
| AgentGym-RL：当前策略在环境内在线rollout，逐阶段增大交互上限 | 根据环境reward做RL参数更新 | 主路线无需额外任务SFT；它是本方向的跨范式课程对照。[[wiki/papers/optimization/reinforcement-learning/AgentGym-RL\|S041，复用]]；[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=9\|§3.3 · p.9]] |

### 减少模仿，改善泛化，还是降低成本

AgentTuning的混合训练优于只用agent数据，但13B在held-out上的general-only分数还略高于混合；通用任务也有退步。因此它支持在训练中检查通用能力保留，不能证明每种规模都从agent示范获得独立泛化收益。ATLAS把干预移到监督位置；它相对完整轨迹的held-in收益更明显，held-out上关键30%与随机30%平均仅38.36对38.04，缺少该差值置信区间。两者共同提醒：**数据选择机制、同骨干消融和逐任务结果比“泛化更强”的总称更有信息。** [[raw/papers/optimization/finetuning/AgentTuning.pdf#page=6|S047 Tables3–4 · PDF pp.6–7 / 印刷 pp.3058–3059]] [[raw/papers/optimization/finetuning/ATLAS.pdf#page=7|S048 Table3 · PDF p.7 / 印刷 p.25340]]

同样不能由“小数据”或“小模型”直接推出总成本优势。ATLAS保留完整输入并需强模型选择；Agent Distillation的SAG默认每步采8个动作再执行筛选。后者最多5步、固定Wikipedia 2018与数学代码任务，模型变小的结果包含外部工具和额外推理预算。训练token、选择/教师成本、环境执行次数和测试时延应分别记录。[[raw/papers/optimization/finetuning/ATLAS.pdf#page=4|S048 §3.2 · PDF p.4 / 印刷 p.25337]] [[raw/papers/optimization/finetuning/ATLAS.pdf#page=14|Appendix B.1 · PDF p.14 / 印刷 p.25347]] [[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=6|S049 §5 · p.6]]

### 学到修订行为以后，环境是否能继续

Agent-R的恢复测试让模型从基础Llama失败轨迹的随机截断处继续，最多50轮，检查特定失败状态上的后续结果。[[raw/papers/optimization/finetuning/Agent-R.pdf#page=11|S050 §4.4、Table3 · p.11]] **公开实现核查已缩小材料缺口：**MCTS采树有reset与动作前缀重放；离线训练构造直接拼接坏前缀、修订信号和好分支文本，不在构造函数内执行后缀核验；恢复函数则真实执行传入前缀后在线续做。三者不能互相替代为状态一致性证明。构造数据的loss字段已见，最终训练mask及恢复实验入口尚未完整核验；底层环境服务语义仍未知。固定commit `82fcc1c`的原始快照、行定位和剩余范围见 [[wiki/papers/optimization/finetuning/Agent-R#公开实现核查：三个阶段怎样处理环境状态|唯一论文页]]。因此现有证据既不保证任意不可逆任务恢复，也不支持因训练拼接疑点否定已报告的恢复评测。

这与 [[wiki/harness/workflows#分支能否撤回，评价能否被信任|运行时分支与状态恢复]] 形成接口：SFT提供行动倾向，harness决定哪些动作实际执行、失败后的状态怎样保留/恢复。ATLAS的关键步语义判断、Agent-R的actor判错、SAG的可执行/一致输出也各有误差，不能当作同一种可靠过程标签。当前未形成已查新的研究缺口。

### 与已有工具和数据路线的联系

**工具调用的训练接口（S012 / S014 已完成摄入，应用未测）：**[[wiki/papers/optimization/finetuning/Toolformer|Toolformer]] 用执行结果对后续 token 预测的帮助筛选调用，再微调模型，学到的对象包括调用时机、工具及参数；这个损失代理没有直接优化长程任务成功或调用成本，也没有链式工具训练。[[wiki/papers/harness/tools/CodeAct|CodeAct]] 则需分开动作表示和模型适应：CodeActInstruct 收集并筛选多轮成功及纠错轨迹，与通用对话混合后训练 CodeActAgent。其通用数据消融和不同基础模型表现说明，不能把收益全部归于“代码”或“纠错”一个因素。两者的运行时执行接口见 [[wiki/harness/tools|工具方向]]；AnyTool / Voyager 的候选池或技能库更新不应计作参数微调。[[raw/papers/optimization/finetuning/Toolformer.pdf#page=3|S012 §2 · pp.3–4]] [[raw/papers/optimization/finetuning/Toolformer.pdf#page=9|§6 · p.9]] [[raw/papers/harness/tools/CodeAct.pdf#page=6|S014 §3、Tables 4–5 · pp.6–8]] [[raw/papers/harness/tools/CodeAct.pdf#page=14|Table A.8 · p.14]]


**监督对象与课程范式（S037–S041，已完成摄入，应用未测）：**TaskCraft 用构造的多跳问答轨迹训练策略；SWE-Gym 用实际执行后测试成功的轨迹训练策略，并另外以成功/失败标签训练 verifier；TOUCAN 对真实工具轨迹进行模型质量筛选后做 SFT；WebDreamer 则训练“截图与动作→变化描述”的世界模型组件。它们学的对象不同，不能把共同出现的 fine-tuning 视为同一种 Agent 能力证据。[[raw/papers/optimization/data-environments/TaskCraft.pdf#page=9|S037 §4.4 · p.9]] [[raw/papers/optimization/data-environments/SWE-Gym.pdf#page=5|S038 §4–5 · pp.5–7]] [[raw/papers/optimization/data-environments/TOUCAN.pdf#page=7|S040 §4.1 · p.7]] [[raw/papers/optimization/data-environments/WebDreamer.pdf#page=5|S039 §3.3 · pp.5–6]]

S001 在课程学习小节引用 [[wiki/papers/optimization/reinforcement-learning/AgentGym-RL|AgentGym-RL]]；核读原文后须限定：ScalingInter 是**在线 RL 的交互上限课程**，主路线不要求额外任务 SFT，不能充当 SFT 课程有效的直接证据。框架支持 SFT 与方法实际使用 SFT 是不同事实；课程思想的跨范式联系见下节。[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=6|S041 §3.2.2 · p.6]] [[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=9|§3.3 · p.9]]

## 论文入口与交叉方向

- [[wiki/papers/optimization/finetuning/Toolformer|S012 · Toolformer]]：主归属。
- [[wiki/papers/harness/tools/CodeAct|S014 · CodeAct]]：交叉关联；主归属为`harness/tools`。
- [[wiki/papers/optimization/data-environments/TaskCraft|S037 · TaskCraft]]：交叉关联；主归属为`optimization/data-environments`。
- [[wiki/papers/optimization/data-environments/SWE-Gym|S038 · SWE-Gym]]：交叉关联；主归属为`optimization/data-environments`。
- [[wiki/papers/optimization/data-environments/WebDreamer|S039 · WebDreamer]]：交叉关联；主归属为`optimization/data-environments`。
- [[wiki/papers/optimization/data-environments/TOUCAN|S040 · TOUCAN]]：交叉关联；主归属为`optimization/data-environments`。
- [[wiki/papers/optimization/reinforcement-learning/AgentGym-RL|S041 · AgentGym-RL]]：交叉关联；主归属为`optimization/reinforcement-learning`。
- [[wiki/papers/optimization/finetuning/AgentTuning|S047 · AgentTuning]]：主归属。
- [[wiki/papers/optimization/finetuning/ATLAS|S048 · ATLAS]]：主归属。
- [[wiki/papers/optimization/finetuning/Agent-Distillation|S049 · Agent-Distillation]]：主归属。
- [[wiki/papers/optimization/finetuning/Agent-R|S050 · Agent-R]]：主归属。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
