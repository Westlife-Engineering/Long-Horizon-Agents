---
type: paper
primary_direction: harness/hooks
related_directions:
  - harness/verification
source_id: S023
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/hooks/AgentSpec.pdf]]"
---

# AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents


## 阅读结论与证据身份

**原文陈述：**AgentSpec 提供可读的 DSL，将“什么事件触发、哪些条件成立、采取何种干预”从 Agent 提示中外置到运行流程。规则由人工写，或由 LLM 生成 Python 谓词。规则确定地被执行，并不等于规则涵盖了所有风险。[[raw/papers/harness/hooks/AgentSpec.pdf#page=3|§§2.3–3 · pp.3–5]] [[raw/papers/harness/hooks/AgentSpec.pdf#page=6|§4 · p.6]]

## 从规则到实际控制点

规则是三元组 $r=(\eta_r,\mathcal P_r,\mathcal E_r)$：触发事件出现，且所有谓词都为真，才按顺序执行 enforcement。**这里谓词为真表示触发规则，不表示动作安全。**事件包括 state_change、before_action、agent_finish。LangChain 实现拦截 `iter_next_step`，在 AgentAction、AgentStep、AgentFinish 处介入。[[raw/papers/harness/hooks/AgentSpec.pdf#page=5|§3.3 Definitions 3.1–3.3、§4 · pp.5–6]]

| 干预 | 实际依赖 | 保证边界 |
| --- | --- | --- |
| stop | 程序终止 | 只阻止被当前规则识别的路径 |
| user_inspection | 人判断同意/拒绝 | 仍依赖人工理解具体副作用 |
| invoke_action | 预定义纠正动作 | 纠正动作本身及环境语义需要可信 |
| llm_self_examine | 模型重新审视并产生动作 | 判定与恢复仍可能出错，非纯符号证明 |

该表依据 [[raw/papers/harness/hooks/AgentSpec.pdf#page=4|§3.2–3.3 · pp.4–5]]。例如“倒液体”前检查目标是否属于可浇湿对象，必要时停止；代码检查可检查危险命令、URL 白名单与 I/O，不能把浅层代码匹配称作完整数据流分析。状态和工具参数通过接入点供谓词检查，本文没有提出与 IsolateGPT 相同的跨应用进程隔离。[[raw/papers/harness/hooks/AgentSpec.pdf#page=7|§5.2、Fig.5–7 · pp.7–8]]

## 手写规则与自动规则必须分开看

作者在 RedCode-Exec、SafeAgentBench、FixDrive 上分别评估代码、具身和 Apollo 自动驾驶规则。代码集 25 类、每类 30 个风险提示；Table 3 区分模型实际拟调用解释器 `#inv`、规则触发 `#vio` 和人工允许 `#pass`，不能把所有提示都算成 guardrail 挡住的执行。部分所谓风险代码经作者检查认为无害后获准执行。[[raw/papers/harness/hooks/AgentSpec.pdf#page=6|§5.1–5.2 · pp.6–7、Table 3]]

手写具身规则下，所测十类危险指令的完成率均为零，但安全任务完成率从 58.62% 降至 54.26%；安全与正常任务效用要同时测。FixDrive 只覆盖八个给定违规场景，Table 5 的 100% 不能外推为开放道路安全。[[raw/papers/harness/hooks/AgentSpec.pdf#page=8|§5.2、Tables 4–5 · p.8]]

o1 自动规则使用代码 75/750、具身 25/250 的样例，其余用于测试；AV 零样例，生成规则只在 5/8 场景防止违规。错误包括只识别示例中敏感路径、遗漏物体状态、将“不要造成危险的倒液体”误写成禁止所有 pour。**规则生成会同时造成漏过和误拒。**[[raw/papers/harness/hooks/AgentSpec.pdf#page=9|§5.3、Table 6 · p.9]]

> [!warning] 指标措辞不能静默统一
> Table 6 将具身 95.56% 标为 Enforced，§5.3 又称 precision，并称借助安全对照计算 recall=70.96%；没有足够混淆矩阵细节让本库重新核算标准 precision/recall。本页保留作者的指标身份，不把 95.56% 当成已核算的通用检测率。[[raw/papers/harness/hooks/AgentSpec.pdf#page=9|§5.3 · p.9]]

解析与谓词计算在所测设置为毫秒级，人工审批等待和 LLM 自检成本则另受用户/模型延迟影响。实验模型和运行预算的部分细节正文未明确，本库未靠引用框架名称补全。[[raw/papers/harness/hooks/AgentSpec.pdf#page=10|§5.5 · p.10]]

## 长程边界与比较用途

作者承认当前是离散检查点的确定性 enforcement，不预测数步之后才出现的不安全状态；概率前瞻属于未来工作。**本库推断：**“能接收轨迹”与“已经验证长期后果”是不同能力，形式语义没有消除谓词不完备和感知错误。与本批 IsolateGPT 比较，前者控制检查点，后者控制组件之间的信息边界；没有统一任务/预算比较可用于性能排序。[[raw/papers/harness/hooks/AgentSpec.pdf#page=11|§6.3 · p.11]]

## 来源身份与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S023 |
| 作者 | Haoyu Wang、Christopher M. Poskitt、Jun Sun |
| 版本 | arXiv:2503.18666v3，2025-07-31；官方页面注明 ICSE 2026。归档预印本首页 ACM DOI 仍为占位，不把占位写作正式 DOI |
| 原始获取 | [原始 PDF](https://arxiv.org/pdf/2503.18666v3)；访问日期 2026-10-25 |
| 原件 | [[raw/papers/harness/hooks/AgentSpec.pdf\|AgentSpec，12 页]] |
| SHA-256 | `A8EF39247392EB49E275768C19ACA11A111C997E432225DCBCF74DFBF31ABAE7` |
| 综述入口 | S001 引文 [633]，§4.5.2，PDF p.32；书目 p.126 |
| 实际阅读 | 2026-10-25；主文 pp.1–11（§§1–8，含语义、实现、实验与限制）；p.12 参考文献未逐项追读。实际看 pp.5–6 的语义/流程图与 pp.8–9 的 Tables 4–6。 |
| 未做 | 未复现实验、未执行论文代码、未逐项追读相关工作；Obsidian 应用未测 |

本页页码均从归档 PDF 第一页计。论文结果是作者报告，不代表本库完成复现。已完成摄入并整合到 Harness 与索引；内容与结构验收通过，Obsidian 应用未测。

## 主题联系与后续核查

已整合到 [[wiki/harness/hooks|Hooks 与中间件]]，同时连接 [[wiki/harness/verification|验证]] 对判断来源和拦截位置的区分。跨论文分析由本库提出，不是新的实验结果；候选问题尚未查新，不据此宣布研究空白。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/hooks|harness/hooks]] · [[wiki/harness/verification|harness/verification]]。
