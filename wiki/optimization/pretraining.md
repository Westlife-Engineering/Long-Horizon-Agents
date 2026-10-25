---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/pretraining/DeepSeek-V3.pdf]]"
  - "[[raw/papers/optimization/pretraining/YaRN.pdf]]"
  - "[[raw/papers/optimization/pretraining/ProLong.pdf]]"
  - "[[raw/papers/optimization/pretraining/Qwen2-VL.pdf]]"
  - "[[raw/papers/optimization/pretraining/DoReMi.pdf]]"
---

# 预训练与中期训练


综述将这一环节作为后续交互学习的能力基础，讨论推理先验、长上下文状态、多模态感知，以及数据混合和训练策略。它区别于直接模仿一条完成任务的交互轨迹，但同一模型报告可以同时包含预训练、后训练与 Agent 评测，不能仅凭章节归类裁定证据类型。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=43|S001 · §5.3 · pp.43–45]]

细分导航：Reasoning Priors；Long-Context State；Multimodal Perception；Data Mixture and Training Strategies。本轮 S042–S046 已完成摄入与本节整合，内容与结构验收通过；Obsidian 应用未测。

### 改变哪个环节，就先检查哪种证据

下表是本库依据原文建立的机制比较，不是性能排名。架构决定历史怎样表示，训练进一步决定模型学会利用什么；两者与 [[wiki/optimization/architecture|历史表示和访问]] 相接，但不能互相替代证据。

| 改变对象 | 训练或运行机制 | 直接证据及归因边界 |
| --- | --- | --- |
| token 预测目标与整体基础模型配方 | DeepSeek-V3 的 MTP 在隐藏态上串接额外预测模块，增加未来 token 的监督；同时有 MoE/MLA、数据变化和后训练 | MTP 消融是较小 MoE 的受控对照，推理时丢弃模块；不是环境动作规划。最终聊天模型成绩含 SFT/RL，不能全归预训练。[[wiki/papers/optimization/pretraining/DeepSeek-V3\|S042]]；[[raw/papers/optimization/pretraining/DeepSeek-V3.pdf#page=10\|§2.2 · pp.10–11]]、[[raw/papers/optimization/pretraining/DeepSeek-V3.pdf#page=26\|§4.5.1、Table4 · p.26]] |
| 位置频率与注意力分布 | YaRN 分段插值 RoPE 频率，保留高频近邻区分，再调整 attention temperature，配合长文本适配训练 | Llama 系列的 PPL、passkey 与短任务结果；128K版本从64K checkpoint续训，并非只改一个配置。[[wiki/papers/optimization/pretraining/YaRN\|S043]]；[[raw/papers/optimization/pretraining/YaRN.pdf#page=5\|§3.2–4.1 · pp.5–7]] |
| 继续训练的数据组成、长度与后续 SFT | ProLong 在固定训练/评测流程中比较长短混合、文本来源、训练长度及指令数据 | 只有 PPL 或简单找针不能指导全部下游任务；最终配方与消融初始化不同。[[wiki/papers/optimization/pretraining/ProLong\|S044]]；[[raw/papers/optimization/pretraining/ProLong.pdf#page=3\|§3–5 · PDF pp.3–6 / 印刷 pp.7378–7381]] |
| 视觉信息编码及多模态训练 | Qwen2-VL 用动态视觉 token 和时间/高/宽 M-RoPE；三阶段训练后连接 Qwen-Agent | 有视觉消融，也有多轮任务结果；两类实验的模型规模、组件和指标不同，未分离单一训练机制对 Agent 的贡献。[[wiki/papers/optimization/pretraining/Qwen2-VL\|S045]]；[[raw/papers/optimization/pretraining/Qwen2-VL.pdf#page=5\|§2.1–2.2 · pp.5–7]]、[[raw/papers/optimization/pretraining/Qwen2-VL.pdf#page=13\|§3.2.7 · p.13]] |
| 数据域采样比例 | DoReMi 用小模型的相对损失优化域权重，取时间平均，再按比例重采样训练大模型 | 传递的是数据比例；1024长度的一般LM实验，未直接测长上下文和Agent。[[wiki/papers/optimization/pretraining/DoReMi\|S046]]；[[raw/papers/optimization/pretraining/DoReMi.pdf#page=3\|§2–3.1 · pp.3–5]] |

### 可接受长度、可用证据与任务成功分别测试

YaRN 用64K训练数据得到可在128K进行语言建模和passkey检索的模型，但passkey是在无意义干扰中找一个数字；它的作者也指出困惑度不能完整预测检索表现。DeepSeek-V3 使用YaRN做两阶段扩窗，NIAH图则来自SFT后的模型。这些结果支持所测输入使用能力，不能单独证明长轨迹的状态更新、恢复与终止。[[raw/papers/optimization/pretraining/YaRN.pdf#page=7|S043 §4.1–4.3 · pp.7–8]] [[raw/papers/optimization/pretraining/YaRN.pdf#page=19|Appendix B.5 · p.19]] [[raw/papers/optimization/pretraining/DeepSeek-V3.pdf#page=23|S042 §4.3、Fig.8 · p.23]]

ProLong把评测进一步拆成多类长任务与短能力保持：在Llama-3-8B、5B-token消融中，增加长数据可降低PPL，却可能使SFT后的长任务表现下降；同一checkpoint在SFT前后也可能给出不同的配方排序。因此“长文本训练有效”必须说明在哪个训练阶段、用何种任务和指标判断。它最终仅用短UltraChat SFT取得强长上下文表现，并不证明短交互轨迹足以训练长程Agent。[[raw/papers/optimization/pretraining/ProLong.pdf#page=2|S044 §2.1–3.2、Fig.1–2 · PDF pp.2–4 / 印刷 pp.7377–7379]] [[raw/papers/optimization/pretraining/ProLong.pdf#page=6|§5 · PDF p.6 / 印刷 p.7381]] [[raw/papers/optimization/pretraining/ProLong.pdf#page=16|Appendix B、Fig.4 · PDF pp.16–17 / 印刷 pp.7391–7392]]

**需要保留正面的交互证据。**Qwen2-VL在Qwen-Agent下保留32K观察—动作历史，报告ALFRED、卡牌及导航任务；ALFRED用高层动作和SAM，属于模拟环境中的组合系统。AITZ的TM/EM是动作匹配，ALFRED的SR/GC分别对应整任务与子目标。它说明感知模型可以参与多轮执行，也显示导航仍落后专用模型；M-RoPE的小模型感知消融不能解释成72B长程成功的归因。[[raw/papers/optimization/pretraining/Qwen2-VL.pdf#page=10|S045 Table5 · p.10]] [[raw/papers/optimization/pretraining/Qwen2-VL.pdf#page=12|§3.2.7 · pp.12–13]] [[raw/papers/optimization/pretraining/Qwen2-VL.pdf#page=15|§3.3.2、Table8 · p.15]]

DeepSeek-V3也有SWE-Bench Verified工程结果，但使用Agentless框架、最终后训练模型；这些条件和MTP小规模消融属于不同证据层。把输入容量、感知/检索质量、特定harness任务成功按层检查，可与 [[wiki/harness/memory|运行时历史选择]]、[[wiki/optimization/finetuning|交互行为的监督学习]] 共同解释。[[raw/papers/optimization/pretraining/DeepSeek-V3.pdf#page=30|S042 §5.3.1、Table6 · pp.30–31]]

### 数据配方的代理目标与使用目标是否一致

DoReMi用“代理比参考还差多少”的excess loss选择域比例，避免只追最难或最容易的数据；ProLong直接用多类下游任务指导配方。前者不需要已知下游目标，后者更贴近指定使用需求，但依赖开发集覆盖。现有实验的数据、模型、长度及预算不同，不能据此排名。代理模型增大也未让DoReMi收益单调提高，说明转移到更大模型的配方需要实证检查。[[raw/papers/optimization/pretraining/DoReMi.pdf#page=3|S046 §2 · pp.3–4]] [[raw/papers/optimization/pretraining/DoReMi.pdf#page=8|§4、Fig.6 · p.8]] [[raw/papers/optimization/pretraining/ProLong.pdf#page=2|S044 §2 · PDF pp.2–3 / 印刷 pp.7377–7378]]

成本同样需要分开：DoReMi的2.6×描述主模型达到目标质量的训练步数，域权重搜索另有成本；ProLong的同token长度对照并非同FLOPs；DeepSeek-V3正式训练成本不含前期研究/消融。不能把其中任一数字直接当Agent训练或部署预算保证。[[raw/papers/optimization/pretraining/DoReMi.pdf#page=5|S046 §3.1–3.2 · pp.5–6]] [[raw/papers/optimization/pretraining/ProLong.pdf#page=5|S044 §4、脚注4 · PDF p.5 / 印刷 p.7380]] [[raw/papers/optimization/pretraining/DeepSeek-V3.pdf#page=5|S042 Table1及说明 · p.5]]

**待检验问题，尚未查新：**固定模型、harness、动作权限和预算后，困惑度/检索/视觉定位改善中，哪些能预测多轮状态跟踪与恢复成功？若将任务族或恢复阶段作为数据域，小模型的相对损失是否仍是可迁移的配方选择信号？当前材料让验证条件更具体，尚不能把这些证据缺口认定为研究空白。YaRN本地v3与S001所引会议版的关系、公式不一致等版本细节保留在唯一论文页。

## 论文入口与交叉方向

- [[wiki/papers/optimization/pretraining/DeepSeek-V3|S042 · DeepSeek-V3]]：主归属。
- [[wiki/papers/optimization/pretraining/YaRN|S043 · YaRN]]：主归属。
- [[wiki/papers/optimization/pretraining/ProLong|S044 · ProLong]]：主归属。
- [[wiki/papers/optimization/pretraining/Qwen2-VL|S045 · Qwen2-VL]]：主归属。
- [[wiki/papers/optimization/pretraining/DoReMi|S046 · DoReMi]]：主归属。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
