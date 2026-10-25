---
type: paper
primary_direction: optimization/self-evolution
source_id: S065
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf]]"
---

# Don't Just Fine-tune the Agent, Tune the Environment

## 来源与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S065 |
| 作者 | Siyuan Lu、Zechuan Wang、Hongxuan Zhang、Qintong Wu、Leilei Gan、Chenyi Zhuang、Jinjie Gu、Tao Lin |
| 版本 | arXiv:2510.10197v2，2026-01-30；归档按v2锁定；DOI 10.48550/arXiv.2510.10197 |
| 原始入口 | [Environment-Tuning](https://arxiv.org/abs/2510.10197v2)；访问2026-10-25 |
| 原件 | [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf\|本地PDF，共44页]] |
| SHA-256 | `E410EB1F51CA7221B09034D0AE5CF0AD68B0D64C3982AA81B91EC098426C4F02` |
| 实际阅读 | 2026-10-25；正文pp.1–10；附录A–E pp.14–22的POMDP、提示生成/审查、奖励、评测及稳定性；看pp.4–6 Figure 2/3及奖励公式、p.8 Table 2、p.20 Figure 5/公式。pp.23–44完整提示和长案例未逐页核读。 |
| S001定位 | 引文401，§5.7.3，PDF p.55；书目 pp.108 |

正文PDF页码与印刷页码一致。未逐项核读参考文献，未审查代码或复现实验。

## 调整训练环境的教学条件，不是自主生成世界

本文关注BFCL少数据多轮工具任务上的RL冷启动与不稳定。实际改变**人工规定的课程阶段、错误反馈信息和奖励函数**，同时训练agent参数；反馈经半自动LLM流程增强。可作为训练环境可调的实例，不能因为S001将其列入co-evolution，就改写成无监督任务/世界生成器自主演化。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=3|§3.1–3.2 · pp.3–5]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=14|附录B · p.14]]

| 阶段 | 训练内容 | 环境反馈 | 优化信号 |
| --- | --- | --- | --- |
| 1 | 输出与工具schema语法 | 标准 | 格式/工具正确性，要求尝试工具 |
| 2 | BFCL Base多轮任务 | 增强提示 | 每个用户turn的进展 |
| 3 | 加缺参数、缺函数、长上下文 | 增强提示 | 进展奖励 |
| 4 | 全训练题，对齐测试 | 撤掉增强提示 | 仍为进展奖励 |

表据[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=4|§3.2、Figure 3 · pp.4–5]]。切阶段依据验证准确率平台与梯度范数稳定，课程结构不是另一环境策略学出的。第四阶段撤除教学提示，因此不能用训练富提示条件等同实际测试。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=5|Remark 3.1 · p.5]]

## 没有专家演示，仍有专家信息和真值

增强反馈把含混报错改成依赖/工具约束提示。Generator读取错误轨迹并参考人工样例；Constitutional Judge检验是否泄露具体调用、参数、完整序列以及提示是否可操作，拒绝后最多重试3次。每领域需3–5个人工增强反馈示例，Judge提示明确提供ground-truth calls。具体生成器/裁判模型版本在已核读实现段未确认。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=6|§3.3 · p.6]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=14|附录B.1–B.3 · pp.14–18]]

“没有预收集专家轨迹”不能写成无监督：任务、工具规则、目标状态、期望返回值、提示示例和裁判参考调用都提供信息。模型Judge通过不等于形式化排除泄漏。这里改变教学反馈，未证明环境转移规则也由agent自主共同改写。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=17|B.2–B.3 · pp.17–18]]

进展奖励为 $R_P=\frac1T\sum_t r_t^{state}r_t^{exec}$；每个**用户turn结束**同时通过目标状态与执行结果检查才记1。一个turn可能含多步工具调用，不是逐token/逐次调用独立标注。附录D.2再将轨迹奖励按同题组内归一化为GRPO式advantage，配非对称clip和KL。因此逐turn较密评估不等于每步因果信用分配。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=6|§3.4 · pp.6–7]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=14|附录A · p.14]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=18|附录C · pp.18–19]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=20|D.2、Eq.4–5 · p.20]]

## 实验收益与适用条件

BFCL V3共800题，四分割各取100形成400训练题，正文称其余400为held-in test。模型包括Qwen2.5-7B-Instruct、Llama-3.1-8B-Instruct及工具SFT版本。Table 1支持完整方案改善多轮成功；课程、反馈、奖励与训练进展同时变化，不能只归因“调环境”。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=7|§4.1、Table 1 · pp.7–8]]

OOD涵盖BFCL V4搜索/记忆、τ2-bench和ACEBench Agent。Table 2有许多相对base的提高，**并非每项都优于直接RL**：ToolACE起点BFCL V4 avg为ToolRL 18.91%对Environment Tuning 16.79%；watt起点ACEBench avg为9.15%对7.50%。不能从非匹配的SFT基线推出“SFT必过拟合、RL必泛化”。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=8|Table 2 · p.8]]

Table 3/Figure 4给阶段、增强反馈、进展奖励消融，附录E给单阶段RL崩塌及KL系数比较；支持这些所测设置的稳定性改进，未提供全部因素等总预算的全面分离。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=9|§4.3、Table 3、Figure 4 · pp.9–10]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=20|附录E · pp.20–22]]

> [!warning] 验证与测试隔离尚不清楚
> §4.1/附录D.1称训练外400题全为held-in test；E.1 Figure 5又从剩余BFCL选100题作validation，且validation决定阶段切换。已核读文字未明确这100题是否从最终测试排除。应保留协议核查项，不能称完全独立测试，也不能未查代码就断言训练泄漏。[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=7|§4.1 · p.7]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=19|D.1 · p.19]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=20|E.1、Figure 5 · p.20]]

**本库综合：**该文具体化了训练时可见信息：教学阶段给依赖提示，再撤去测迁移。它不同于[[wiki/papers/optimization/reinforcement-learning/AgentGym-RL|AgentGym-RL]]改变交互上限，也不同于[[wiki/papers/optimization/self-evolution/Agent0|Agent0]]更新出题者参数。后续比较应分开可访问路径、可见信息、反馈真值、参数更新。提示撤除后的有效迁移是候选比较问题，validation/test隔离是本文材料缺口；当前未做新颖性查新或实验。

## 主题联系与验收

已整合至 [[wiki/optimization/self-evolution|Optimization · 自我演化]]，论文与主题互链、队列及索引已同步；内容与结构经主Agent验收通过，Raw哈希匹配，已完成摄入。Obsidian渲染、操作与来源跳转未测。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/self-evolution|optimization/self-evolution]]。
