---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/distillation/GKD.pdf]]"
  - "[[raw/papers/optimization/distillation/DAgger-LLM.pdf]]"
  - "[[raw/papers/optimization/distillation/MAD-OPD.pdf]]"
  - "[[raw/papers/optimization/distillation/Pi-Play.pdf]]"
  - "[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf]]"
---

# On-Policy Distillation


综述把OPD描述为在学生自己访问的状态上提供教师监督，并分为教师指导与自我改进式监督。核读后需要再问：**“状态”是学生生成的token前缀，还是由学生动作推进的外部环境历史？教师看到了什么额外信息？** 这决定了分布偏移被修正到哪一层，不能只按OPD名称推断已解决长程交互。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=52|S001 · §5.6 · pp.52–53]] [[raw/papers/optimization/distillation/GKD.pdf#page=4|S056 §3.1 · p.4]] [[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=4|S057 §3.2 · p.4]]

细分导航：Teacher-guided OPD；Self-improving OPD。本轮S056–S060已完成摄入，内容与结构已验收；应用未测。

### 状态由谁产生，教师能看到什么

下表比较信息流与更新对象，不排列不同任务的分数。固定教师指本次学生更新时教师参数不随梯度改变；教师输入仍可逐样本变化。

| 方法 | 采样状态与教师信息权限 | 输出监督与更新对象 |
| --- | --- | --- |
| [[wiki/papers/optimization/distillation/GKD\|S056 GKD]] | 学生生成token前缀，可与固定序列按λ混合；教师看到相同前缀 | 教师token概率，散度可选；固定教师、更新学生，采样停止梯度。RL是另加的可选项。[[raw/papers/optimization/distillation/GKD.pdf#page=4\|§3.1–3.2 · pp.4–5]] |
| [[wiki/papers/optimization/distillation/DAgger-LLM\|S057 DAgger-LLM]] | 教师/学生按轮混合执行，真实环境返回观察；每个访问状态都查询教师动作 | 教师动作文本交叉熵，动作内部前缀也是教师标签；不要求教师logits。固定教师、按批更新学生。[[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=4\|§3.2、Eqs.8–13 · pp.4–5]] |
| [[wiki/papers/optimization/distillation/MAD-OPD\|S058 MAD-OPD]] | 学生采样动作；讨论历史只对教师可见；训练环境历史覆盖需另核查 | 置信度加权各教师散度之和；教师固定，学生更新；agentic用JSD、code用reverse KL是本文配方。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=6\|§4.2–4.4 · pp.6–7]] |
| [[wiki/papers/optimization/distillation/Pi-Play\|S059 π-Play]] | 学生搜索rollout；教师额外看出题构造路径QCP，examiner还更新题目分布 | 学生GRPO＋KL(学生‖教师)，教师EMA软更新；examiner用难度反馈另更新。[[raw/papers/optimization/distillation/Pi-Play.pdf#page=4\|§2.2–2.5 · pp.4–5]] |
| [[wiki/papers/optimization/distillation/Self-Distillation-Zero\|S060 SD-Zero]] | 学生生成文本解答；教师额外看完整初答及二元验证结果 | 先双损失SRT训练修订者，再用冻结修订者做reverse KL；额外同步教师属于后续迭代实验。[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=4\|§2.1–2.2 · p.4]]、[[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=7\|§3.4 · pp.7–8]] |

DAgger提供本批直接的多轮软件环境证据，但实际教师执行概率最低仍为0.6，不是训练末期纯学生环境分布。MAD-OPD的算法写有在线环境循环，附录训练数据却是ToolACE独立step样本；仅从PDF不能确认整个训练历史都由学生执行后刷新。GKD、SD-Zero主要是文本生成/数学代码推理，不能把自回归长度当成真实环境恢复验证。[[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=17|S057 F.1–F.2 · pp.17–18]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=12|S058 Algorithm 1、B.3 · pp.12–13]] [[raw/papers/optimization/distillation/GKD.pdf#page=5|S056 §4 · pp.5–9]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=5|S060 §3.1 · p.5]]

### 稠密监督来自额外条件，不等于因果信用

教师监督可以是固定专家概率、教师动作文本、讨论条件化概率、出题路径条件化概率或结果条件化修订者。稠密表示每个位置都有优化信号；它仍可能继承教师错误、置信度偏差或合成任务错误。SD-Zero的完整分布KL与样本token的log概率比也不同，后者可正可负；信号集中在少数位置不等于验证器证明了这些位置的因果责任。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=6|S058 §4.2–4.3 · p.6]] [[raw/papers/optimization/distillation/Pi-Play.pdf#page=4|S059 §2.2–2.3 · p.4]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=8|S060 §4.1 · p.8]]

**本库数学核查，限定S058的普遍理论主张。** MAD-OPD D.3在不相交支持混合与无约束softmax下宣称reverse KL单模态全局最优；但取$p=q=(0.6,0.4)$，KL=0且梯度为0，集中解成本反而为−log0.6>0。故这些假设不足以保证单模态最优或普遍收敛，需额外可行族/优化条件。其固定教师、独立位置logit界与Table 4经验消融分别保留，不升级为参数训练稳定或代码连贯性的普遍定理，完整说明见 [[wiki/papers/optimization/distillation/MAD-OPD#理论主张的适用前提：本库数学核查|唯一论文页]]。[[raw/papers/optimization/distillation/MAD-OPD.pdf#page=22|S058 D.3–D.5 · pp.22–23]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=17|Table 4 · p.17]]

### 比较收益之前，先核对分母和成本

本批不支持“OPD普遍优于RL”。DAgger的GRPO基线使用不同任务子集，SWE Verified只评466/500；MAD-OPD用BFCL/LCB选checkpoint，部分交互评测排除执行失败；SD-Zero的大部分增益来自SRT，且采样预算与实现表仍有配置口径差异。π-Play同时使用GRPO和蒸馏，最多5轮训练交互；它的“2–3倍演化效率”不能直接当墙钟加速。具体条件已在各论文页归位。[[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=6|S057 §4.1 · p.6]] [[raw/papers/optimization/distillation/MAD-OPD.pdf#page=13|S058 B.6、B.9–B.10 · pp.13–15]] [[raw/papers/optimization/distillation/Self-Distillation-Zero.pdf#page=19|S060 C.1–C.3 · pp.19–23]] [[raw/papers/optimization/distillation/Pi-Play.pdf#page=13|S059 B–C.2、Table 11 · pp.13–15]]

## 论文入口与交叉方向

- [[wiki/papers/optimization/distillation/GKD|S056 · GKD]]：主归属。
- [[wiki/papers/optimization/distillation/DAgger-LLM|S057 · DAgger-LLM]]：主归属。
- [[wiki/papers/optimization/distillation/MAD-OPD|S058 · MAD-OPD]]：主归属。
- [[wiki/papers/optimization/distillation/Pi-Play|S059 · Pi-Play]]：主归属。
- [[wiki/papers/optimization/distillation/Self-Distillation-Zero|S060 · Self-Distillation-Zero]]：主归属。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
