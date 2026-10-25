---
type: paper
source_id: S030
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/CorrectBench.pdf]]"
---

# Can LLMs Correct Themselves? A Benchmark of Self-Correction in LLMs

## 自我纠错要同时计算改对多少、改错多少和花了多少

**原文定位：**CorrectBench把纠错分成intrinsic（模型内部反馈）、external（工具/检索等外部反馈）和fine-tuned（训练专用纠错能力），比较常识/知识问答、数学、代码任务。它是评测与分析工作；静态答案修订的结果不能直接证明长程环境行动可以恢复。[[raw/papers/CorrectBench.pdf#page=3|§2、Fig.2 · pp.3–4]] [[raw/papers/CorrectBench.pdf#page=26|Appendix D · p.26]]

本文有用的细化是同时记录两种方向的转换：

| 初始答案 | 纠错后 | 对应指标 |
| --- | --- | --- |
| 错 | 对 | Correction Rate：初始错误样本中成功改对的比例 |
| 对 | 错 | Misjudgment Rate：初始正确样本中被误改的比例 |

作者在Claude 3.5-Sonnet、GPQA/AQUA/HotpotQA子集上比较CoVe与RARR的这两个指标；不是所有11种方法、全部模型都完成相同诊断。[[raw/papers/CorrectBench.pdf#page=8|§4.6、Table 3 · p.8]]

**本库推导：**若同一批样本初始准确率为$p$，每样本最终判断标准一致，且CR/MR按上述条件分母统计，则

$$p_{\rm after}=p+(1-p)\,CR-p\,MR.$$

所以高初始准确率时，小量误改就可能抵消纠错收益。此式是二分类转移的算术关系，**不是论文报告的新实验或因果结论**。它提示测试停止条件时必须同时保留原本正确样本，不能只筛选错误题后宣称部署收益。

## 方法收益与额外资源不能混成一种效果

CorrectBench比较单一方法及串接S1/S2；Table 1有正向也有负向格，Reflexion-v1在多个任务下降，CRITIC在所列GSM8K条件下降，故不能将论文总体措辞理解成所有方法总能自我纠正。fine-tuned组的基座、训练数据和目标不同，不能将表间差异简单归因于“纠错类型”。[[raw/papers/CorrectBench.pdf#page=5|Table 1、§3–4.1 · p.5]] [[raw/papers/CorrectBench.pdf#page=7|§4.4–4.5、Table 2 · p.7]]

任务指标包括答案accuracy、数学solve rate和代码pass@k，模糊答案还会采用人工或GPT-4o判断。**评判器是实验条件的一部分**，pass@k也不是选出一个答案后的成功率。论文并未在本次核读部分充分统一所有模型/方法的预算、k和判断分支，保留为复现前待核查。[[raw/papers/CorrectBench.pdf#page=5|§3 Evaluation Metrics · p.5]]

Table 4按MATH的150个样本列tokens、API calls、搜索tokens与accuracy；其Efficiency Rank定义为accuracy/(tokens×calls)，是作者选定的比率，不能当墙钟或货币成本。Fig.7测到的响应时间还依赖服务与模型条件。动态controller、按错误类型选策略和早停在§6/Appendix D属于后续方向，并非本文已验证的通用控制器。[[raw/papers/CorrectBench.pdf#page=8|§4.7、Fig.7 · pp.8–9]] [[raw/papers/CorrectBench.pdf#page=10|§6 · p.10]]

## 使用结果前必须保留的内部不一致

> [!warning] 本库仅采用可定位的条件性结论
> 本论文有多处图表、正文或范围不一致；这不等于所有观察都无效，但不足以支持精确的跨任务总体提升或因果归因。

- **样本身份/分母：**p.2称CorrectBench-base共3825对；p.24 Table 7列2018，正文说每数据集抽100后剔除；p.9成本表又是MATH150例。可能包含不同子集，但本文未把所有口径清晰对应。本库不统一成单一已核验样本量。[[raw/papers/CorrectBench.pdf#page=2|§1 · p.2]] [[raw/papers/CorrectBench.pdf#page=24|Appendix B.1、Table 7 · p.24]] [[raw/papers/CorrectBench.pdf#page=9|Table 4 · p.9]]
- **叙述与表格：**p.5正文CoVe/GPQA的+23.24与Table 1的+18.85不同；GSM8K的+5.28在表中对应Self-Refine，CoVe为+5.77。后续引用以明确表格为准，不取正文叙述数字。[[raw/papers/CorrectBench.pdf#page=5|Table 1、§4.1 · p.5]]
- **模型分类与机制归因：**p.6将LLaMA/Qwen置于closed-source叙述、GPT/Claude置于open-source叙述，与p.9 Table 5相反。DeepSeek-V3高初始表现导致纠错收益小，可以作为作者解释；“内置纠错机制导致”并未由本研究隔离验证，不采作已证实机制。[[raw/papers/CorrectBench.pdf#page=6|§4.2 · p.6]] [[raw/papers/CorrectBench.pdf#page=9|§4.8、Table 5 · p.9]]
- **预算与统计：**p.34的CoVe示例包含基线、核验问题、逐问题作答、最终回答多个步骤；p.9 Table 4仅列1.0 API Calls，具体计数范围需要实现核验。Appendix B.3声称报告bootstrap区间，但该段未列数值区间。不能据此自行补全显著性或预算相等的论证。[[raw/papers/CorrectBench.pdf#page=34|Appendix G.4 · pp.34–35]] [[raw/papers/CorrectBench.pdf#page=24|Appendix B.3 · p.24]]

## 对本库比较的作用

与已读 [[wiki/papers/CRITIC|CRITIC]] 一致，净收益必须同时考虑纠正与误改。两篇的模型代际、数据、工具与提示不同，表面上“是否能自纠”不同不是直接矛盾。尚未读取的CoVe/RARR等原论文仅作为本文评测对象，不升级为本库直接机制证据。

**本库推断：**目前最稳固的知识增量是评测口径：记录初始基线、错误/正确子集转换、工具信息权限、额外预算和最终成功。对长程Agent的迁移需要环境状态与副作用证据；本篇不能填补这一证据缺口，也不能单独证明某类模型已到纠错上限。

## 来源身份与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S030 |
| 作者 | Guiyao Tie、Zenghui Yuan、Zeli Zhao、Chaoran Hu、Tianhe Gu、Ruihang Zhang、Sizhe Zhang、Junran Wu、Xiaoyue Tu、Ming Jin、Qingsong Wen、Lixing Chen、Pan Zhou、Lichao Sun |
| 版本 | NeurIPS 2025 Datasets and Benchmarks Track 会议PDF，47页 |
| 标识符 | 会议条目 DOI:10.52202/085713-5386 |
| 原始入口 | [发布页](https://papers.nips.cc/paper_files/paper/2025/hash/ec07904adc847a45f53dceb44078f8f0-Abstract-Datasets_and_Benchmarks_Track.html)；[本次 PDF](https://papers.nips.cc/paper_files/paper/2025/file/ec07904adc847a45f53dceb44078f8f0-Paper-Datasets_and_Benchmarks_Track.pdf) |
| 原件 | [[raw/papers/CorrectBench.pdf\|CorrectBench.pdf · 47 页]] |
| SHA-256 | `50FF5D2A551F26D87133D1FA6FD35980814DD9300537BDEFC2FA65E7E2AE6B4A` |
| 获取与阅读日期 | 2026-10-25；下载原字节以不覆盖方式归档，身份按该 PDF 首页核对 |
| S001 追索 | [[raw/papers/Towards Long-Horizon Agents.pdf#page=36\|§4.6.2 · PDF pp.36 · 引文 605]]；参考文献 PDF pp.124 |

核读正文 PDF pp.1–10，Appendix A–D pp.23–26；抽查提示/案例G.4–G.5 pp.34–36及CRITIC案例p.45。查看p.5 Table 1、p.8 Table 3/Fig.7、p.9 Table 4/5、p.24 Table 7/8图像。未逐项核读其余提示、全部模型分项表、checklist或实现代码；结论只限这些实际读到的范围。PDF与印刷页码相同。

**主题整合：**已整合至 [[wiki/harness/Overview#验证|Harness · 验证]]，内容与结构已验收。尚未复现实验；按本轮要求不进行ComputerUse，Obsidian公式、表格、折叠、来源跳转及宽窄窗口均未实测。
