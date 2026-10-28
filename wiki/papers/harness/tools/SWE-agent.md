---
type: paper
primary_direction: harness/tools
related_directions:
  - harness/verification
source_id: S071
created: 2026-10-28
updated: 2026-10-28
reading_status: selected-body-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/SWE-agent.pdf]]"
---

# SWE-agent：把仓库操作改成模型能有效使用的接口

关键贡献是固定基础模型后改造 agent–computer interface（ACI）：搜索结果怎样显示、编辑如何提交、错误如何退回，以及哪些历史保留。它并未训练一个新的代码模型。[[raw/papers/harness/tools/SWE-agent.pdf#page=3|§2–3 · pp.3–4]]

## 身份与实际读取

- 来源 S071；标题 *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*；作者 John Yang、Carlos E. Jimenez、Alexander Wettig、Kilian Lieret、Shunyu Yao、Karthik Narasimhan、Ofir Press。
- 版本 arXiv:2405.15793v3，2024-11-11；[身份页](https://arxiv.org/abs/2405.15793v3)；[原始PDF](https://arxiv.org/pdf/2405.15793v3)，访问日 2026-10-28。原下载名 `2405.15793v3.pdf` 原样归档为 [[raw/papers/harness/tools/SWE-agent.pdf|SWE-agent.pdf]]，118页，PDF页码与正文页脚一致。
- SHA-256：`d171e0693060b910ceb2cddd0fd4bc7cae302005d42d0d8059bfdbe056c3adba`。
- 2026-10-28 实读 PDF pp.3–9：ACI、设置、结果/消融与行为分析、讨论；看原页 p.6 Tables 1–3、p.8 Figs.7–8。附录及全量轨迹未读，未复现。S001 的进入点为 [[raw/surveys/Towards Long-Horizon Agents.pdf#page=57|§6.1.1 · p.57 · [747]]]。

## 环境怎样使反馈有用

输入为 issue 与仓库，Agent 在 Linux shell 中查找、编辑、运行程序；搜索按文件/目录摘要返回，过多匹配要求缩窄查询；文件窗给行号与遗漏范围。编辑是一次范围替换并立刻展示更新，lint 发现选定错误时丢弃修改、保留原状态并要求重试。旧观察只保留最近五条的完整内容，以免旧代码与冗余输出持续干扰。[[raw/papers/harness/tools/SWE-agent.pdf#page=3|§3 · pp.3–4]]

**本库机制解释：**仓库与程序输出提供可定位、可复查的状态；拒绝坏编辑使局部尝试更易恢复。模型仍负责定位故障、提出语义正确的修复、选择复现与测试并解释结果；harness 负责把选择落实为可执行动作及及时反馈。lint 只拒绝一类错误，不能证明需求满足；获得 shell 权限也不等于生产部署权限。

## 成效及可归因范围

SWE-bench 为12个 Python 仓库的2294题，Lite为300题；主指标为提交补丁后通过评测测试的比例。模型为 GPT-4 Turbo `gpt-4-1106-preview` 和 Claude 3 Opus `claude-3-opus-20240229`；每题API预算4美元，超出自动提交已有编辑。GPT-4 Turbo 在全量集为12.47%，Lite为18.00%；同模型 Shell-only 在Lite为11.00%。这是限定基准下的代码修复成效，不能外推到完整产品交付。[[raw/papers/harness/tools/SWE-agent.pdf#page=5|§4–5 · pp.5–6 · Table1]]

| 同 GPT-4 Turbo、同 Lite 的接口条件 | Resolved |
| --- | --- |
| 完整 ACI | 18.0% |
| 去掉专用 edit | 10.3% |
| edit 保留但不做 lint | 15.0% |
| 摘要搜索换成逐条翻阅 | 12.0% |
| 最近5条完整观察改为全历史 | 15.0% |

原文消融：[[raw/papers/harness/tools/SWE-agent.pdf#page=6|§5.1 · Table3 · pp.6–7]]。这些对照支持接口与运行状态管理确实影响同模型表现，但不能将几个百分点相加为各模块的独立贡献，也未匹配所有条件的实际token消耗。它们比跨系统总分更接近harness归因。

## 剩余失败不是单一层的问题

作者把248条未解决轨迹用GPT-4o分类；人工验证一致率87%。约52%归为错误或过度特定的实现，23.4%为编辑后未恢复。**原文解释线索，不是模型/harness因果分解。**正确接口仍不足以补齐诊断与实现能力；反过来，同模型接口消融说明不能只靠模型能力解释成功。[[raw/papers/harness/tools/SWE-agent.pdf#page=8|§5.2 · Fig.8 · p.8]]

与 [[wiki/papers/harness/workflows/Agentless|S072 Agentless]] 的机制差别在于是否让模型逐步选择下一动作；不能拿不同模型、补丁采样数和测试筛选预算下的总分直接判断谁更优。可执行测试仍只是需求代理，综述明确保留隐藏需求、安全与回归限制。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=56|S001 · §6.1 · p.56]]

## 整合状态

已整合至 [[wiki/applications/success-mechanisms|应用成功机制与瓶颈]]；本轮过程见 [[组会/2026-10-28-Application/过程/A-软件与GUI|软件与GUI核读]]。未修改共享主题/索引/日志；本地原件及引用检查完成，Obsidian未实测。
