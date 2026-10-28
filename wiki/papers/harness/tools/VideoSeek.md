---
type: paper
source_id: S075
primary_direction: harness/tools
related_directions:
  - harness/workflows
  - harness/memory
created: 2026-10-28
updated: 2026-10-28
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/VideoSeek.pdf]]"
---

# VideoSeek：先判断缺什么，再选择视频片段

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S075 |
| 原文标题 | VideoSeek: Long-Horizon Video Agent with Tool-Guided Seeking |
| 作者 | Jingyang Lin、Jialian Wu、Jiang Liu、Ximeng Sun、Ze Wang、Xiaodong Yu、Jiebo Luo、Zicheng Liu、Emad Barsoum |
| 版本 | arXiv:2603.20185v1，2026-03-20；arXiv 身份页标记 Accepted at CVPR 2026 |
| 原始来源 | [版本页](https://arxiv.org/abs/2603.20185v1)、[锁定 PDF](https://arxiv.org/pdf/2603.20185v1)；访问 2026-10-28；身份页与 PDF 首页已核对 |
| Raw | [[raw/papers/harness/tools/VideoSeek.pdf\|本地原件，共 18 页]] |
| SHA-256 | `FEFE579556637365A8A8214B850FB234F424BFAD7A3A145B2E5C502E93EE414F`；下载副本与归档后一致 |
| 实际阅读 | 2026-10-28；正文 pp.1–8、附录 A pp.12–18；看原页 p.6 Table1、p.7 Tables2–4、p.8 Fig.3、p.12 Table5／成本表／预算曲线、p.17 Fig.10。参考文献未逐条核读；未审代码、未复现实验 |
| S001 入口 | [365]，§6.4.1，PDF p.61；按下载 v1 解释 |
| 分类理由 | 主要改变视频观察工具和运行循环，无本文新模型训练；主归属 harness/tools |

以下为原论文直接核读，分析另标“本库推断”；页码为 PDF 页码，与印刷页码一致。

## 环境如何决定这套流程能奏效

任务是长视频问答及复杂视频推理。输入视频可按时间任意回访，模型不必连续观看；可选字幕会直接放入初始问题。默认 GPT-5 负责思考，也解释工具获得的画面。它只通过抽样画面的模型描述逐步获得观察，完整思考—动作—观察历史进入下一轮，没有预建完整视频数据库或专门压缩记忆。[[raw/papers/harness/tools/VideoSeek.pdf#page=3|§3 · pp.3–5]] [[raw/papers/harness/tools/VideoSeek.pdf#page=13|附录 A.4／Fig.4／Fig.6 · p.13]]

**本库推断：**环境允许低风险重复观察，失败时可以换区间、改问题再看；但观察文本本身是模型解释，不是可信正确性反馈。视频预先存在、可随机访问，不同于只能前进的直播或已发生即不可恢复的物理交互。实验不涉及外部写权限，不能据此推断部署到驾驶、机器人就可靠。

三种工具提供不同观察粒度：`overview` 全片均匀取 16α 帧建立粗略线索；`skim` 对较长候选区间取 4α 帧；`focus` 对不超过 4α 秒的小片段按 1 FPS 检查细节。LVBench 取 α=4，其他基准 α=2；最多 20 轮，达到上限后会追加直接作答指令。每轮由模型判断证据是否充分，决定继续看还是答，不是外部 oracle 验证通过才停。[[raw/papers/harness/tools/VideoSeek.pdf#page=4|§3.2–3.3／Algorithm1 · pp.4–5]]

## 成效与归因：先取对信息，再组织理解

评估包括 LVBench（103 段约一小时视频、1,549 道选择题）、Video-MME long（900 题）、LongVideoBench long（564 题）、Video-Holmes（1,837 题）。主要成效指标是答案准确率及平均所看帧数；默认基线是同 GPT-5 对 384 帧均匀采样后回答。没有本文新训练。[[raw/papers/harness/tools/VideoSeek.pdf#page=5|§4.1 · p.5]]

| 对照 | 结果 | 能说明什么 |
| --- | --- | --- |
| LVBench，无字幕，同 GPT-5 基座 | 固定384帧：60.1%；VideoSeek：68.4%，平均92.3帧 | 完整 harness 用更少视觉输入获得更高准确率；不是相同总计算预算 |
| LVBench，同一批选中帧 | GPT-5* 使用 VideoSeek 所选帧：63.9%；完整流程68.4%；表中两者均约92.4帧 | 选帧解释部分增益；余下差距支持中间交互有用，但不能单独归因为纯推理能力 |
| 固定工具框架，换思考模型 | GPT-5：68.4%／4.42轮；o4-mini：58.5%／5.08轮；GPT-4.1：53.0%／2.99轮 | 多看多轮不能弥补所有模型差异；作者“过早自信”解释尚非独立心理量测 |
| 分别去 overview／skim／focus | 68.4→55.1／62.4／63.7 | 全局定位与局部检查均有作用；工具移除也改变信息和调用机会 |

证据：[[raw/papers/harness/tools/VideoSeek.pdf#page=6|Table1 · p.6]] [[raw/papers/harness/tools/VideoSeek.pdf#page=7|Tables3–4 · p.7]] [[raw/papers/harness/tools/VideoSeek.pdf#page=12|附录 A.3／Table5 · p.12]]。正文92.3与同帧实验92.4的细小差异保留原表口径，未自行抹平。

**本库推断：**同帧对照比单纯“比大模型高分”更能说明没有看见关键信息与看后处理之间的区别；但完整流程还有工具提示、视觉转文本、多次模型调用和逐步思考，附录没有在相同 token／调用数下拆开这些贡献。本文也没有同工具同预算的固定粗到细流程对照，因此能说“动态流程有效”，不能说已证明动态性本身必胜固定流程。

字幕条件需单列：LVBench 加字幕后 VideoSeek 达76.7%、27.2帧；GPT-5加字幕基线66.5%、384帧。字幕提供了额外文本观察，作者将其解释为暴露视频逻辑流；**本库推断：**这与“提供更多易检索的答案线索”没有被消融分离，不能把差额全部命名为理解时间因果结构。[[raw/papers/harness/tools/VideoSeek.pdf#page=6|Table1 · p.6]] [[raw/papers/harness/tools/VideoSeek.pdf#page=7|§4.3 · p.7]]

少帧也不等于更快。附录 A.1 报告无字幕时 token 从83K降到49K，耗时从66.1秒增至135.9秒；带字幕从97K降到57K，耗时71.3→89.7秒。作者指出 API 调度、网络及后台硬件影响时间比较。因此此处保留“节约视觉输入／报告 token”，不概括为全部计算成本或延迟都下降。α 由各基准精度—效率曲线选定，本次未确认独立验证集选择，不能当作未调参的统一预算结果。[[raw/papers/harness/tools/VideoSeek.pdf#page=12|附录 A.1–A.2 · p.12]]

## 主动验证要分成选择、执行、理解并修订

1. **选择检查什么：**模型先把不足转成时间区间与具体查询，而非无条件增加所有帧。p.17 案例先找到建筑，再检查文字是否是新年祝词，最后区分两个相近选项。
2. **执行检查：**工具对指定区间重新采样，仍由 GPT-5 读画面；没有确定性 OCR／事件判定 oracle。
3. **理解并修订：**第一次 focus 只返回“新年祝词”，模型指出仍不足以区分选项，重新聚焦获得完整文字，之后停止。这个案例显示可行的证据不足判断；不提供总体校准率或失败率。

案例：[[raw/papers/harness/tools/VideoSeek.pdf#page=17|附录 A.5／Fig.10 · p.17]]；工具提示：[[raw/papers/harness/tools/VideoSeek.pdf#page=13|Fig.6 · p.13]]。另一个 p.8 案例在 focus 无相关结果后转回 skim，体现流程不是固定只能由粗到细；但最终“裙子破损”仍根据姿态等间接线索推断，不能把模型写出的高置信度当真实验证。[[raw/papers/harness/tools/VideoSeek.pdf#page=8|Fig.3 · p.8]]

## 能力瓶颈与适用边界

当前证据支持 **model 与 harness 耦合**：工具决定能看什么、如何定位，思考模型决定下一次观察与停止；完整历史保留此前线索。原文没有独立记忆消融、训练内化实验或可靠性 oracle，因此不能声称专用记忆机制或新训练造成增益。作者明确指出罕见、突发且局部的异常事件可能不适合逻辑引导跳看；本库据此理解为可预测线索分布的环境前提，而非“工程再多做几个工具”必然可补足。[[raw/papers/harness/tools/VideoSeek.pdf#page=2|方法定位 · p.2]] [[raw/papers/harness/tools/VideoSeek.pdf#page=8|§5 · p.8]]

应用整合入口：[[wiki/applications/Overview|Application]]；形成记录：[[组会/2026-10-28-Application/过程/B-检索与多模态|B：检索与多模态]]。已整合至 [[wiki/applications/success-mechanisms|应用成功机制与瓶颈]]；主Agent已完成内容与结构检查，Obsidian内显示未测。
