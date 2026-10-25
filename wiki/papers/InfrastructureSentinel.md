---
type: paper
source_id: S025
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/InfrastructureSentinel.pdf]]"
---

# InfrastructureSentinel: Policy Enforced Guardrails for Secure MCP-driven Infrastructure Agents


## 阅读结论与证据身份

**原文陈述：**该系统用独立 Guardian LLM 解释自然语言政策，在 MCP 驱动的基础设施 Agent 流程中设置四处检查。它强调运行时用户身份、时段和系统健康状态会改变允许的动作，因此同一工具调用不能只靠输入文本判断。**本文主要提供架构和初步应用证据；不是形式化安全证明。**[[raw/papers/InfrastructureSentinel.pdf#page=4|§4 · PDF pp.4–5 / 印刷 pp.40298–40299]]

## 四个位置分别阻止什么

| 控制点 | 看的状态 | 允许/阻止及边界 |
| --- | --- | --- |
| 输入过滤 | 用户输入、已认证角色、会话、时间、历史、系统健康 | 高置信恶意输入阻断；LLM 置信分并非校准概率 |
| 工具选择验证 | 拟执行工具序列和参数、权限、目标环境 | 拒绝禁用工具、危险组合或越权计划 |
| 执行前门控 | 最新健康度、依赖、锁与维护状态 | 单个 MCP 调用前 Go/No-Go；此前批准不代表现在仍可执行 |
| 执行后审计 | 工具返回、状态变化、前面各层决策 | 留痕与反馈，可能调整政策解释；本身无法撤销既有副作用 |

前三行来自 [[raw/papers/InfrastructureSentinel.pdf#page=4|§4.1–4.4 · PDF p.4 / 印刷 p.40298]]；最后一行机制来自 [[raw/papers/InfrastructureSentinel.pdf#page=5|§4.5 · PDF p.5 / 印刷 p.40299]]，“不能撤销”是本库对时点的限定。政策由领域专家用自然语言描述，例如角色、批量操作上限和审批窗口；本文不是先把所有政策编译成程序谓词再运行。

Fig.2 给出事后发现重启过多节点引起服务错误，之后增加单次重启比例限制的例子。它说明作者设想的反馈回路，不能单凭图认定已做长期自适应学习验证；§7 仍把增强 Layer 4、形式验证与自动政策发现列为未来方向。[[raw/papers/InfrastructureSentinel.pdf#page=6|Fig.2、§7 · PDF p.6 / 印刷 p.40300]]

## 实际实验强度与缺失项

§5 称在自建模拟 MCP 环境和内部 HPE HPC 原型环境测试，命令由专家与 LLM 生成，基线为无 guardrail 和 LLM-as-filter。Table 1 对直接注入、间接注入、工具投毒、命令注入和上下文政策违规分别报告 ADR **大于** 90/85/88/76/50%，并称整体 FPR<10%。这些是作者报告的下界式数字，不能改写为精确成功率，更不能填成“几乎全部防住”。[[raw/papers/InfrastructureSentinel.pdf#page=5|§5、Table 1 · PDF p.5 / 印刷 p.40299]]

**本次核读未在正文找到：**各类样本量、具体 Guardian 与任务模型版本、重复次数/方差、阈值选择、各层独立消融、攻击强度及完整可复现数据划分。§5.1 甚至以“例如 Llama 3 70B 或 GPT-4”的将来时描述基线。不能据此补全实际配置或推断某层贡献。§6 的低延迟论述提出缓存和异步审计等办法，没有给出可比较的完整延迟/成本表。[[raw/papers/InfrastructureSentinel.pdf#page=5|§5.1 · PDF p.5]] [[raw/papers/InfrastructureSentinel.pdf#page=6|§6.1 · PDF p.6]]

## 对当前地图的贡献

**本库推断：**有价值的比较点是“计划检查之后，还要在真正执行前重新检查最新状态”，以及“审计与事前阻断职责不同”。四层使用相关的模型与上下文，层数本身不增加独立证据，也不保证错误不会共同传播。此文没有提供跨应用地址空间/权限能力隔离或策略解释正确性的普遍保证。可信身份、实时状态来源和不可绕过的 MCP 调用入口都是落地前提，需另查实现而非从图推定。

## 来源身份与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S025 |
| 作者 | Tarun Kumar、Aalap Tripathy、Gayathri Saranathan、Martin Foltin、Suparna Bhattacharya、Scott Hinchley、Donald M Bahls、David Brookshire、Larry Kaplan、Robert W. Wisniewski |
| 版本 | AAAI 2026，40(47):40295–40301，IAAI Emerging Applications 技术轨道；DOI 10.1609/aaai.v40i47.41468 |
| 原始获取 | [原始 PDF](https://ojs.aaai.org/index.php/AAAI/article/view/41468/45429)；访问日期 2026-10-25 |
| 原件 | [[raw/papers/InfrastructureSentinel.pdf\|InfrastructureSentinel，7 页]] |
| SHA-256 | `D7BF031B23650643D3772069BD1D3058A1E7C8E4FC38BAF7E590AA34923A62DD` |
| 综述入口 | S001 引文 [285]，§4.5.2，PDF p.33；书目 p.99 |
| 实际阅读 | 2026-10-25；主文 §§1–7 pp.1–6，参考文献 p.7 仅浏览；实际看 Fig.1/2 与 Table 1（pp.3、5、6）。PDF p.1 对应印刷 p.40295，后续顺延；无附录。 |
| 未做 | 未复现实验、未执行论文代码、未逐项追读相关工作；Obsidian 应用未测 |

本页页码均从归档 PDF 第一页计。论文结果是作者报告，不代表本库完成复现。已完成摄入并整合到 Harness 与索引；内容与结构验收通过，Obsidian 应用未测。

## 主题联系与后续核查

已整合到 [[wiki/harness/Overview#Hooks 与中间件|Hooks 与中间件]]，同时连接 [[wiki/harness/Overview#验证|验证]] 对判断来源和拦截位置的区分。跨论文分析由本库提出，不是新的实验结果；候选问题尚未查新，不据此宣布研究空白。

返回 [[wiki/index|索引]]。
