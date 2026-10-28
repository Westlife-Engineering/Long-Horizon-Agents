# Application：已有成效的机制与瓶颈

准备日期：2026-10-28（Asia/Shanghai）。本轮由用户明确启动，目标是解释 S001 §6 五类已有应用的成效，比较 model、harness 与环境条件；不寻找新应用、新方向，不设计或执行实验。

## 共同范围与判据

主 Agent 完整核读 S001 §6（PDF pp.55–67，第7节之前），查看 Fig.14（p.57），按需回读 §4–5。五类是可重叠的观察—行动接口，不是难度阶梯；§6.5 本轮只讨论跨应用数字任务，不外推具身和所有专业服务。

C 先交付判据，A/B 与主 Agent 按同一版本分析；材料收齐后 C 一次审查，主 Agent 修订收束，不增加辩论轮次。允许结果为耦合或尚不能区分。正文预算约5–8篇，本轮初选6篇（SWE-agent、Agentless、UI-TARS、WebThinker、VideoSeek、Toolathlon）；如关键对照需要，可回读已有 Magentic-One，共不超过7篇。论文身份/可读性不足时替换并登记，不凑数量。

## 人员与文件所有权

用户指定所有 subagents 使用 gpt-6-astra，reasoning high；本轮显式覆盖通常同主模型约定。A：软件与GUI，独占 S071–S073 来源文件和过程/A-软件与GUI.md。B：信息获取与多模态，独占 S074–S075 来源文件和过程/B-检索与多模态.md。C：先判据、后一次证据审查。主 Agent：S076 Toolathlon、共享主题/索引/日志/综述页与最终验收。任何文件同一时刻只有一位写者；不建立新聊天，不另派论文任务。

## 状态与保存

原件：[[raw/surveys/Towards Long-Horizon Agents.pdf|S001]]，SHA-256 `C62DA7E66A4C3F7251ED8B450F51DF6500B2F850C7C70853779614E3D780E738`。新来源锁定版本与阅读范围分别见唯一论文页。完整结构化分析、C审查与修订在本目录；正式综合归 [[wiki/applications/Overview|Application]] 相关页面。临时提取/渲染在 .tmp/，验收后清理。

启动时已有 AGENTS、索引、日志、Optimization 多页及 S001 等未提交改动，另有 .claudian/、插件data.json、conversation-to-note/、debug.log；这些不是本轮产物，保留。Git由主Agent统一处理。本轮增量与已有未提交的索引、日志、综述变更交织；本轮保留为工作区修改，不混入提交、不push。

## 交付与停止条件

交付约2000–3000中文字的成功机制对照、3–4条共同原因、逐类瓶颈及主动验证/内化结论；附原文页码与实验定位。完成一次证据审查和结构检查后结束。内容、结构与应用实测分开报告；未授权桌面操作，Obsidian内显示未测。

## 完成与验收

- 实际6篇：[[wiki/papers/harness/tools/SWE-agent|S071]]、[[wiki/papers/harness/workflows/Agentless|S072]]、[[wiki/papers/optimization/finetuning/UI-TARS|S073]]、[[wiki/papers/optimization/reinforcement-learning/WebThinker|S074]]、[[wiki/papers/harness/tools/VideoSeek|S075]]、[[wiki/papers/harness/tools/Toolathlon|S076]]；没有启用第7篇补读。
- 正式成果：[[wiki/applications/success-mechanisms|已有应用为何有效]]；形成过程：[[组会/2026-10-28-Application/讨论记录|讨论与修订记录]]，包含A/B/主Agent分析和C先判据后一次审查的入口。正文约2100汉字，连同英文术语与数据约为所要求的2000–3000中文篇幅；引文索引另列。
- C对六篇关键原页作独立回核，主Agent落实六项修订；不以共识增加证据强度。未审所有附录/代码，未复现实验。WebThinker原文冲突及UI-TARS计分未确认项留在唯一页，不声称已经解决。
- `python scripts/check_vault.py`通过：126个Markdown、76个学术来源页（75论文+1综述）、98份Raw，0错误/警告；旧92份Raw逐字节哈希不变，新6份Raw哈希逐项匹配。索引与综述页差异已按任务启动快照复核，已有日志字节前缀保留。此为结构/来源完整性检查，不代替学术验证。
- 表格wikilink、来源页码与文档结构已检查；没有新增图解资产或操作桌面，Obsidian内显示未测。后出现的其他组会PPT目录不是本轮产物，未修改。
- 清理本批次可再生临时文件33个，约21.52 MiB；另清理最初系统临时目录中的综述提取/渲染。仅清理本任务目录，保留六篇原件、唯一页及结构化讨论。
- 本轮已收束，不启动后续研究、实验或推送。
