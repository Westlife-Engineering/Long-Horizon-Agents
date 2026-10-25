---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/self-evolution/STaR.pdf]]"
  - "[[raw/papers/optimization/self-evolution/rStar-Math.pdf]]"
  - "[[raw/papers/optimization/self-evolution/R-Zero.pdf]]"
  - "[[raw/papers/optimization/self-evolution/Agent0.pdf]]"
  - "[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf]]"
  - "[[raw/papers/optimization/self-evolution/R-Quest.pdf]]"
  - "[[raw/papers/optimization/finetuning/Agent-R.pdf]]"
  - "[[raw/papers/optimization/distillation/Pi-Play.pdf]]"
  - "[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf]]"
  - "[[raw/supplements/S061-STaR/STaR-supplement.pdf]]"
---

# 自我演化


本章讨论的训练式自我演化把生成经验、筛选反馈和策略更新接成循环，并可能更新任务或环境分布。作者区分离线生成—筛选—训练、在线交互更新、Agent—环境共同演化。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=54|S001 · §5.7 · Fig.13 · pp.54–55]]

细分导航：Offline Self-evolution；Online Self-evolution；Agent–Environment Co-evolution。这里的范围较窄：外部记忆或技能库的增长，只有被蒸馏、微调、RL 或可训练模块吸收时，才属于该章所说的训练式内化。更广义的外部自我演化见 [[wiki/frontier/Overview|Frontier]]。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=55|S001 · §5.7 小结 · p.55]]

### 循环中究竟更新了什么

“自己生成训练材料”与“自己确定正确性”是两条轴。下面比较实际更新对象及外部信息来源；S061–S065已完成摄入，内容与结构验收通过；Obsidian应用未测。

| 方法 | 循环改变什么 | 正确性或质量锚点 |
| --- | --- | --- |
| [[wiki/papers/optimization/self-evolution/STaR\|S061 STaR]] | 固定题目上重生成推理过程，再从初始base权重SFT | 已知正确答案筛选；失败题生成时额外提示答案；少量人工推理示例。[[raw/papers/optimization/self-evolution/STaR.pdf#page=4\|§3.2、Algorithm 1 · p.4]] |
| [[wiki/papers/optimization/self-evolution/rStar-Math\|S062 rStar-Math]] | 固定题库上更新MCTS数据、策略和PPM；难题追加搜索预算 | 带答案题库、代码执行、终局标签；GPT-4参与合成题，236B模型启动首轮。[[raw/papers/optimization/self-evolution/rStar-Math.pdf#page=5\|§3.2–3.3 · pp.5–6]] |
| [[wiki/papers/optimization/self-evolution/R-Zero\|S063 R-Zero]] | 交替更新Challenger和Solver，任务分布随能力变化 | Solver多数票生成伪标签；一致率用于难度和过滤；无独立训练真值。[[raw/papers/optimization/self-evolution/R-Zero.pdf#page=3\|§2.2–2.4 · pp.3–4]] |
| [[wiki/papers/optimization/self-evolution/Agent0\|S064 Agent0]] | 更新课程Agent及工具executor；ADPO依一致率调整更新 | 代码返回值提供外部计算反馈，最终训练标签仍是多数票；出题还奖励工具调用。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=4\|§3.2–3.3 · pp.4–6]] |
| [[wiki/papers/optimization/self-evolution/Environment-Tuning\|S065 Environment-Tuning]] | 人工四阶段切换数据、反馈和奖励，同时更新agent；半自动改写错误提示 | 任务目标状态/期望返回值；人工提示样例；反馈Judge可见参考调用。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=5\|§3.2–3.4 · pp.5–6]]、[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=17\|附录B–C · pp.17–19]] |
| [[wiki/papers/optimization/self-evolution/R-Quest\|S069 R-Quest，完成摄入]] | 用有效性和批内任务新颖度反馈更新Questioner，再用筛选后的众数伪标签训练Solver | 外部模型与人工复核初始化；每轮10%标注数据回放；循环内Solver判有效、冻结base判新颖。后续不新增强模型调用，不等于没有外部监督。[[raw/papers/optimization/self-evolution/R-Quest.pdf#page=14\|A.1–A.2 · pp.14–16]]、[[raw/papers/optimization/self-evolution/R-Quest.pdf#page=19\|C.2 · p.19]] |

**本库综合：**零新增训练题不等于零知识，自己生成轨迹不等于没有外部监督。STaR保留真实答案；rStar-Math摘要的“without distillation from superior models”必须和其大模型启动、合成题依赖一起理解。R-Zero撤去题库标签以后，匹配伪标签只证明自一致，不能当作真值正确；Agent0的Python反馈改善计算条件，但没有自动把众数变成独立oracle。[[raw/papers/optimization/self-evolution/STaR.pdf#page=3|§3.1 · pp.3–4]] [[raw/papers/optimization/self-evolution/rStar-Math.pdf#page=5|§3.3 · p.5]] [[raw/papers/optimization/self-evolution/R-Zero.pdf#page=4|§2.3–2.4 · p.4]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=5|§3.3.1 · p.5]]

[[wiki/papers/optimization/finetuning/Agent-R|S050 Agent-R，已完成摄入，应用未测]]提供已核读的迭代SFT实例：更新actor后重新采集MCTS轨迹，同时提高筛选门槛，再监督学习修复后续。它说明更新目标与经验刷新频率应分开登记；策略、采样数据、门槛和训练量同时变化，不能把结果只归因于“自我反思”。具体恢复条件和实现材料缺口见 [[wiki/optimization/finetuning#学到修订行为以后，环境是否能继续|微调的恢复边界]]。[[raw/papers/optimization/finetuning/Agent-R.pdf#page=7|§3.2–4.2 · pp.7–9]]

### OPD与自我演化可以处在同一个循环

**修订S001分类边界。** S001 §5.6用“固定任务/环境、只加密监督”区别OPD与自我演化；这可描述某些单轮训练设置，不能作为互斥论文分类。[[wiki/papers/optimization/distillation/Pi-Play|S059 π-Play]]在内层学生rollout上做特权蒸馏，外层examiner又随学生能力更新题目课程，教师以EMA跟随学生，且学生保留GRPO终局奖励。因此应分别记录任务分布、学生策略和教师目标的更新频率。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=52|S001 §5.6 · p.52]] [[raw/papers/optimization/distillation/Pi-Play.pdf#page=4|S059 §2.2–2.5 · pp.4–5]]

QCP来自检索支持的出题过程，仅教师可见；“无需外部训练数据”仍依赖预训练模型、Wikipedia和搜索接口，不等于没有外部知识。SD-Zero则展示固定题集上把改进学生同步成下一轮修订教师的另一种循环，尚未因此证明长期任务分布扩展。两者都提供更新对象的具体实例，不能由有限轮次结果宣布持续自我演化已解决。[[raw/papers/optimization/distillation/Pi-Play.pdf#page=6|S059 §3.1–3.3 · pp.6–7]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=7|S060 §3.4 · pp.7–8]]

### 真实执行、训练辅助和循环轮数分别核对

STaR的长推理与rStar-Math的数学树搜索，不直接证明开放环境中的持续行动。rStar-Math还区分单轨迹策略与PPM选择后的搜索结果；同叫Pass@1也可能已经用了多条候选路径，训练轮次又伴随搜索预算扩大。Agent0确实把Python返回值接回上下文，但主要证据是数学/一般推理评测及三轮共演化，不能直接外推为跨会话工具任务或永久自改进。[[raw/papers/optimization/self-evolution/rStar-Math.pdf#page=6|S062 §4.1 · pp.6–7]] [[raw/papers/optimization/self-evolution/rStar-Math.pdf#page=14|Tables 9–10 · p.14]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=5|S064 §3.3.1 · p.5]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=8|Figure 4 · p.8]]

Environment-Tuning提供真实有状态API训练的另一轴：先让报错透露工具约束/前置依赖，末阶段再撤掉提示，对齐标准环境。它与AgentGym-RL改变可访问交互深度不同，也不是学习一个自主出题的环境策略。其进展奖励按**用户turn**检查目标状态与返回值，再聚合为轨迹奖励；比终局全对/全错更密，不等于工具步骤的独立因果信用。训练额外信息、原有奖励真值及撤除后的迁移必须一起登记。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=5|S065 §3.2–3.4 · pp.5–6]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=18|附录C/D.2 · pp.18–20]] [[raw/papers/optimization/reinforcement-learning/AgentGym-RL.pdf#page=9|S041 §3.3 · p.9]]

### 持续进步是待检验属性，不是循环名称

R-Zero原文已经观察到多轮后性能回落；以外部模型作诊断参考时，伪标签质量也随迭代下降，但作者没有证明噪声是唯一原因。STaR的多数票标签消融明显弱于真实答案版本，而Agent0仅报告三轮收益；这些证据共同要求把**任务多样性、伪标签可靠性、外部成绩和计算预算**分开监测。不能用一致率提高、题目变难或工具次数变多替代真实能力改善。[[raw/papers/optimization/self-evolution/R-Zero.pdf#page=7|S063 §4.2–4.4、Figure 3 · pp.7–9]] [[raw/papers/optimization/self-evolution/R-Zero.pdf#page=17|附录E · pp.17–18]] [[raw/supplements/S061-STaR/STaR-supplement.pdf#page=15|S061 H.1 · PDF p.15 / 印刷p.28]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=8|S064 Figure 4、Table 5 · pp.8–9]]

定向补读[[wiki/papers/optimization/self-evolution/R-Quest|S069 R-Quest]]进一步把诊断推进到**题目是否有效、是否反复训练同一练习模式**：它比较保留无效题与替换为修复题的匹配训练，分析BLEU把同类题拆散，并给出有效性/新颖度门控消融。因而坏题和任务重复已有直接研究证据，不能只因原R-Zero未充分分离原因便视为未研究。K从8增至16虽进一步降低题型集中度，数学表现反而下降，说明最低重复率不等于最好课程。[[raw/papers/optimization/self-evolution/R-Quest.pdf#page=3|§2.2、Fig.3–4 · pp.3–4]] [[raw/papers/optimization/self-evolution/R-Quest.pdf#page=7|Table3、§4.3 · pp.7–9]]

其结论仍依赖具体信息来源与预算。validity标签把“无法可靠判断”也映射为INVALID，外部模型诊断不是全体题目的人工真值；初始化与10%标注回放持续提供锚点。每轮同候选题数之外，另有9次有效性回复、过关后10次求解和K次比较，未构成完整同计算量对照。五轮表格按领域分别选最佳checkpoint，十轮改善只在Qwen3-4B数学课程中验证；初始化、回放与门控的完整等预算归因仍未解决。[[raw/papers/optimization/self-evolution/R-Quest.pdf#page=14|A.2 · p.14]] [[raw/papers/optimization/self-evolution/R-Quest.pdf#page=19|C.2–D · pp.19–20]] [[raw/papers/optimization/self-evolution/R-Quest.pdf#page=5|§4.1–4.2、Fig.5 · pp.5–7]]

**当前证据边界：**“自生成即无监督”“代码执行通过即过程正确”“有限轮收益即持续演化”仍是需避免的概念误解。现有材料已经提供失稳诊断与干预，尚未在匹配完整预算、独立真值和长程环境条件下形成充分比较；具体问题状态在共同补充证据的第二轮审查后统一整理。Environment-Tuning的validation/test隔离、Agent0的筛选阈值及各文表文差异保留在唯一论文页，不用不一致数字作结论。

## 论文入口与交叉方向

- [[wiki/papers/optimization/finetuning/Agent-R|S050 · Agent-R]]：交叉关联；主归属为`optimization/finetuning`。
- [[wiki/papers/optimization/distillation/Pi-Play|S059 · Pi-Play]]：交叉关联；主归属为`optimization/distillation`。
- [[wiki/papers/optimization/self-evolution/STaR|S061 · STaR]]：主归属。
- [[wiki/papers/optimization/self-evolution/rStar-Math|S062 · rStar-Math]]：主归属。
- [[wiki/papers/optimization/self-evolution/R-Zero|S063 · R-Zero]]：主归属。
- [[wiki/papers/optimization/self-evolution/Agent0|S064 · Agent0]]：主归属。
- [[wiki/papers/optimization/self-evolution/Environment-Tuning|S065 · Environment-Tuning]]：主归属。
- [[wiki/papers/optimization/self-evolution/R-Quest|S069 · R-Quest]]：主归属。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
