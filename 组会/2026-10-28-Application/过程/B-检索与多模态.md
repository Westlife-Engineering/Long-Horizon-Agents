# B：信息获取与多模态理解

2026-10-28；范围固定为 S001 §6.2／§6.4 中 WebThinker [337]、VideoSeek [365]，不找新方向、不设计实验。独立核读版本：WebThinker 2504.21776v2、VideoSeek 2603.20185v1；身份、哈希与读取范围见唯一页 [[wiki/papers/optimization/reinforcement-learning/WebThinker|S074]]、[[wiki/papers/harness/tools/VideoSeek|S075]]。本记录保存解释形成过程，不构成新学术证据。

## 初始问题与共同判据

初始假设是：长程应用的进展可能主要来自不断取得并保留任务相关证据，未必等于模型本体已经获得更强理解。按任务成效→环境→机制→model/harness贡献→证据→边界核查，特别寻找同模型改流程、同帧比较、工具消融和训练对照。

## WebThinker：没有正确性 oracle，仍能逐步填知识缺口

它用 QwQ-32B 调度深度网页探索，Explorer 搜索、点击、摘要；报告模式保留文档记忆，由助手模型写节和编辑。网页只能提供内容，不能直接告诉系统最终答案正确。`check` 返回的是提纲，不是事实核验结果；停止依靠模型 EOS 或上限。环境支持读取重试、再搜索和编辑报告，论文没有测试登录权限、外部发布或真实回滚。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=4|§3／Fig.3 · pp.4–5]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=17|附录 A · pp.17–18]]

相同 QwQ-32B 下，WebWalkerQA 从标准 RAG 31.2 到 Base 41.9，再到 RL 46.5，支持 harness 与训练均有作用；但各流程可访问链接、实际调用数与计算不完全匹配，不能把优势单独归为“自主”。训练偏好先正确、再少调用、再短思考；没有调用量统计足以证明训练已减少外部流程。跨 R1 骨干还用了冷启动 SFT，不是零训练迁移。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=6|Table1 · p.6]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|§4.6／Table3 · p.9]]

报告证据更弱：30个 Glaive 问题由模型打分，Base→RL 均分8.0→8.1，去自动分节写作降至6.6。最值得修订的是“报告高分等于可靠研究”的直觉：评审提示明确不考虑引用。能确认的是输出组织有帮助，不能确认来源追溯或每项事实已核验。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=19|附录 B.2 · p.19]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=24|附录 C.3.2 · p.24]]

## VideoSeek：选对观察和处理观察都有贡献

视频可任意回访，允许 overview／skim／focus 三种粒度的低风险观察。模型依据完整轨迹判断不足、选区间和提问，工具返回模型描述，最多20轮后要求作答。无本文新训练；字幕是额外输入，不能隐入“模型理解更好”的解释。[[raw/papers/harness/tools/VideoSeek.pdf#page=4|§3–4.1 · pp.4–5]]

最强对照是 LVBench 无字幕的同帧实验：GPT-5均匀384帧60.1%，使用 VideoSeek 所选约92.4帧63.9%，完整 VideoSeek68.4%。先说明取对证据比多看更重要，再说明只把同样帧一次交给模型仍未达到整套流程。但后半差额混合多轮推理、感知转文本与调用预算，不能精确命名为理解能力增量。换思考模型为o4-mini后看更多帧、走更多轮，准确率反降；模型选择同样重要。[[raw/papers/harness/tools/VideoSeek.pdf#page=7|Tables3–4 · p.7]] [[raw/papers/harness/tools/VideoSeek.pdf#page=12|附录 A.3／Table5 · p.12]]

主动验证分三步：选要检查的时间与问题、执行观察、判断返回内容是否足够并改计划。p.17案例第一次只读出“新年祝词”，模型发现仍不能分选项，再看后读出完整文字。它说明可行性，不证明普遍正确；p.8案例也存在从姿态推断衣服破损的间接证据。突然且无法预测的稀有事件是作者承认的边界。少帧不等于更快：无字幕token83K→49K，但测得时延66.1→135.9秒。[[raw/papers/harness/tools/VideoSeek.pdf#page=17|Fig.10 · p.17]] [[raw/papers/harness/tools/VideoSeek.pdf#page=8|Fig.3／§5 · p.8]] [[raw/papers/harness/tools/VideoSeek.pdf#page=12|附录 A.1 · p.12]]

## 经核读后的修订

**本库综合：**两类应用有效的共同条件是环境仍有可取得的证据，harness把它变成可选择、可回访、可积累的观察，model把当前不足转成下一行动并解释反馈。现有证据不支持“全靠更多检索”或“全靠更大模型”，也不足以把残余错误统一判为理解不足。检索／采样遗漏、摘要损失、证据解释、停止判断与权限限制应分别判断；没有证据时保留不足，不把工程工作量写成已证明的能力瓶颈。

交付：两篇原件与唯一页已写；未改共享主题、索引、日志，交协调者串行整合。关键原图表已目视核对；无 Obsidian 实测、代码审计或实验复现。临时区由协调者验收后清理。
