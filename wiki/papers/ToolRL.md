---
type: paper
source_id: S052
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/ToolRL.pdf]]"
---

# ToolRL：细粒度工具奖励依赖什么监督

## 身份与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S052 |
| 原文标题 | ToolRL: Reward is All Tool Learning Needs |
| 作者 | Cheng Qian、Emre Can Acikgoz、Qi He、Hongru Wang、Xiusi Chen、Dilek Hakkani-Tür、Gokhan Tur、Heng Ji |
| 版本 | NeurIPS 2025 官方会议 PDF；DOI 10.52202/085713-3524 |
| 原始来源 | [锁定 PDF](https://papers.nips.cc/paper_files/paper/2025/file/97c5b2707228e7e3fb67e4ecc2e0e607-Paper-Conference.pdf)；访问 2026-10-25；发布页与 PDF 首页身份已核对 |
| Raw | [[raw/papers/ToolRL.pdf\|本地原件，共 31 页]] |
| SHA-256 | `419096B066D6F28493033E6F388C5BE378D72A079778EF8BFA712627F73A4639` |
| 实际阅读 | 2026-10-25；正文 pp.1–10；附录 C–E pp.24–26、H–J pp.28–31及p.23背景；实际看 p.3 Fig.1、p.4奖励公式、p.26 Tables9–10。NeurIPS checklist pp.16–22、附录完整结果逐单元格未核验；参考文献未逐条读 |
| S001 入口 | 引文487，§5.5.1，综述 pp.48–49；书目 p.115；本页按实际下载版本解释，不能假定与综述所引版本完全相同 |

以下主张来自原论文直接核读，另标本库推断；未复现实验、未核读实现代码。PDF 页码从首页起算。

## 核心判断：奖励更细，不等于没有监督

ToolRL 对预测工具调用与数据中的标准调用做匹配，奖励工具名、参数名和参数值的部分正确。它减少了“整个调用完全正确才得分”的稀疏性，但依赖每个训练步骤有 ground-truth tool calls。标题不是无监督学习主张，作者在附录 J.1也明确奖励本身是一种监督。[[raw/papers/ToolRL.pdf#page=3|§2.1 · p.3]] [[raw/papers/ToolRL.pdf#page=4|§2.3 · p.4]] [[raw/papers/ToolRL.pdf#page=30|Appendix J.1 · p.30]]

> [!important] 区分任务形式与实际训练分布
> §2用思考—工具—观察的多轮轨迹定义TIR，运行时也可执行工具并接回观察。但 §3.1 明确把多步训练轨迹拆成**单步实例**，先前对话作为prompt输入。RL采样的是给定历史下的候选回复，不能据此认定模型在训练中持续沿自己造成的偏离状态完成整条长任务。[[raw/papers/ToolRL.pdf#page=3|§2.1–2.2 · p.3]] [[raw/papers/ToolRL.pdf#page=5|§3.1 · p.5]]

## 奖励怎样形成更新信号

| 部分 | 实际评分 | 能说明什么 |
| --- | --- | --- |
| 格式 | 必需标签与顺序正确记1，否则0 | 结构符合训练协议，不保证任务完成 |
| 工具名 | 预测与标准工具名集合的Jaccard重合 | 工具选择部分匹配 |
| 参数名 | 配对调用的参数key集合重合 | schema部分匹配 |
| 参数值 | 标准key上的值逐项exact match | 对给定标签的一致性，未证明所有等效调用都获奖 |

总匹配分经最大可能分数归一化至[-3,3]，再加格式分；预测和标准调用之间选择最大总匹配。每个候选回复获得一个合成奖励，GRPO将同一query的4个候选奖励中心化并标准化，再做clipped policy update。**细粒度指评分分解，不是给每个思考token独立正确性标签，也不是学到了无偏因果信用。**主设置去掉reference KL。[[raw/papers/ToolRL.pdf#page=4|§2.3–2.4 · p.4]] [[raw/papers/ToolRL.pdf#page=24|Appendix C · p.24]]

工具返回在历史中是条件输入，策略输出是思考、调用及回复；正文未单列多轮observation的loss mask实现，本次未查代码，不能从统一轨迹记号推定工具返回参与action loss。[[raw/papers/ToolRL.pdf#page=3|§2.2 · p.3]]

## 训练与实验支持到哪里

数据为ToolACE 2K、Hammer masked 1K、xLAM 1K；Hammer随机化工具/参数名，要求依据描述。模型为Qwen2.5-Instruct 1.5B/3B/7B及Llama3.2-3B-Instruct；“cold start”指不先额外SFT，已有指令模型不是随机初始化。GRPO batch512、每query4回复、15 epochs、温度1、学习率1e-6、prompt2048/response1024。[[raw/papers/ToolRL.pdf#page=5|§3.1–3.2 · p.5]] [[raw/papers/ToolRL.pdf#page=26|Table9 · p.26]]

BFCL V3、API-Bank和Bamboogle分别检查调用正确性、多轮API及最终QA。Table1中7B GRPO的BFCL总体58.38%，但Multi Turn仅18.12%；提高平均调用表现不等于长任务可靠。Llama3B GRPO总体44.10低于SFT4K的44.16，不能概括所有模型都胜过SFT。[[raw/papers/ToolRL.pdf#page=6|Tables1–2 · p.6]]

奖励消融支持对分解方式的关注：原始部分匹配奖励优于更严格的组合匹配；加长度奖励对多数所测小模型降低BFCL，故更长思考不是该设置的质量代理。动态平滑缩放对3B/Llama有益，但1.5B的45.71仍低于原始46.20，不写成所有模型稳定改善。[[raw/papers/ToolRL.pdf#page=9|Figs4–5 · p.9]] [[raw/papers/ToolRL.pdf#page=10|Fig.6 · p.10]]

## 归因限制与待核查

- PPO与GRPO在正文称相同超参数，但附录Table9–10的prompt/response上限分别为2048/1024与1024/512，GPU memory utilization也不同。算法优劣不能仅由这些表归因；设备总数与总GPU时在本次核读范围未确认。[[raw/papers/ToolRL.pdf#page=26|Tables9–10 · p.26]]
- Table5与Search-R1的Bamboogle比较未证明同检索环境；Search-R1使用固定Wikipedia/E5，本篇写web search，故保留为作者跨设置对照，不作为奖励设计净效应。[[raw/papers/ToolRL.pdf#page=7|Table5、Free-form Inference · p.7]] [[raw/papers/Search-R1.pdf#page=7|S051 §4.3 · p.7]]
- p.8 Table7的scale=1 BFCL40.62，与p.9 Fig.5 Equal Max的51.76不一致；附录H还把format范围描述为[-1,1]，不同于§2.3的{0,1}。动态缩放配方若用于实现需查代码，不能将文字平滑为已确认配置。[[raw/papers/ToolRL.pdf#page=8|Table7 · p.8]] [[raw/papers/ToolRL.pdf#page=9|Fig.5 · p.9]] [[raw/papers/ToolRL.pdf#page=28|Appendix H · pp.28–29]]

**本库推断/待检验：**当存在多条等效工具路径，或模型已经偏离给定历史时，标准调用匹配是否仍代表任务进展？本篇的结果使问题具体化，尚未证明这是新研究缺口。与 [[wiki/papers/Search-R1|Search-R1]] 的关系是“有步骤标签的局部调用学习”对“在线检索后的终局QA反馈”，不能把稠密与稀疏奖励当作脱离状态分布的单一开关。

## 主题联系与状态

已整合 [[wiki/optimization/Overview#Agentic Reinforcement Learning|Optimization：Agentic RL]] 的状态分布、反馈与信用比较。与 [[wiki/harness/Overview|Harness]] 的状态和反馈接口保持交叉联系。本篇内容与结构验收通过，已完成摄入；主题、队列、索引及摄入日志已同步。按用户要求本轮不做Obsidian应用检查，应用未测；未复现实验。
