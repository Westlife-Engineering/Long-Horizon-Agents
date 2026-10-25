---
type: topic
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
---

# Application：应用与评测

[[wiki/surveys/Towards Long-Horizon Agents|S001]] 按 Agent 与环境的**观察—行动接口**组织应用，而不是按任务难度排序。接口决定能看到什么、能改变什么、能获得什么反馈。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=55|S001 · §6 · pp.55–56]]

## 五类应用入口

下表概括综述 p.56 的五类定义；具体方法和基准论文尚未独立核读。

| 应用 | 接口与反馈 | 后续阅读时要核查的问题 |
| --- | --- | --- |
| Software Engineering | 代码仓库、执行环境，测试/编译/运行结果 | 测试通过是否覆盖了真实需求？状态如何跨编辑和修复保留？ |
| Information Seeking | 网页、搜索与知识来源，通常缺少直接执行判定器 | 证据来自哪里，何时停止检索，结论如何核验？ |
| Computer Use | 截图、可访问性树、界面操作，状态部分可见 | 观察是否反映真实状态，错误动作怎样恢复？ |
| Multimodal Agents | 跨时间的视觉、音频和文本流 | 跨模态信息怎样保留与对齐？ |
| General-purpose Agents | 一个流程组合多个接口、工具、权限和服务 | 接口切换后约束、状态与权限是否保持一致？ |

分类来源：[[raw/surveys/Towards Long-Horizon Agents.pdf#page=56|S001 · §6 · p.56]]；最后一列是本库据此提出的核查问题。软件工程中“测试不必然充分覆盖真实需求”的限制也见同页 §6.1。

## 怎样阅读评测结论

综述要求同时关注任务跨度和结果归因：分数受模型、harness 与训练方案共同影响；评测环境还可能被用于训练。Table 7 同时列有系统和基准，且部分多模态理解资源衡量的是基础感知能力，并非严格意义上的长程 Agent 任务。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=64|S001 · §6.6 · pp.64–65]]

**本库后续比较记录项**（维护约定，不是声称所有论文已经提供）：任务依赖与 [[wiki/foundations/Formalization#H1–H3 与 C1–C3|H1–H3]] 范围、模型与版本、harness 配置、可用工具、训练/测试关系、成功判据、执行预算、恢复能力和失败案例。缺项标“未报告/未读取”，不能凭总分完成归因。

综述还根据外部评测数据讨论时间跨度增长，但指出测试集覆盖、上界估计和协议差异限制解释；增长趋势本身无法区分模型与 harness 各自贡献。本库暂不收录其模型排行或倍增数字，也未独立读取相关外部评测来源。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=12|S001 · §2.3 · Fig.4 · p.12]]

## 当前不做的推断

当前只有综述提供的分类与评测入口，不能据此判定哪类应用最适合本库研究，也不能将表中系统条目都当成已核验论文。确定问题后再选取实际基准原文，通过 [[workflows/ingest|Ingest]] 进入知识库。

相关机制见 [[wiki/harness/Overview|Harness]] 与 [[wiki/optimization/Overview|Optimization]]；评测真实性和迁移问题见 [[wiki/frontier/Overview|Frontier]]。

返回 [[wiki/index|索引]]。
