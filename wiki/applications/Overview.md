---
type: topic
created: 2026-10-19
updated: 2026-10-29
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/harness/tools/Terminal-Bench.pdf]]"
  - "[[raw/papers/harness/tools/SWE-bench.pdf]]"
  - "[[raw/papers/harness/tools/SWE-Lancer.pdf]]"
  - "[[raw/papers/harness/tools/AppWorld.pdf]]"
  - "[[raw/papers/harness/tools/OSWorld.pdf]]"
  - "[[raw/papers/harness/tools/tau-bench.pdf]]"
---

# Application：应用与评测

[[wiki/surveys/Towards Long-Horizon Agents|S001]] 按 Agent 与环境的**观察—行动接口**组织应用，而不是按任务难度排序。接口决定能看到什么、能改变什么、能获得什么反馈。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=55|S001 · §6 · pp.55–56]]

## 五类应用入口

下表概括综述 p.56 的五类定义。已围绕第6节定向核读6篇原论文；成功机制、组件对照和条件性瓶颈判断见 [[wiki/applications/success-mechanisms|已有应用为何有效]]，不将少量案例外推到整类。

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

### Terminal-Bench 补充的测量边界

[[wiki/papers/harness/tools/Terminal-Bench|S080 Terminal-Bench]] 把困难终端任务做成容器、指令、隐藏测试与人工参考解，检查最终环境是否满足目标；任务覆盖不局限于软件修复。其质量审查要求指令与测试双向一致、参考解可通过、作弊捷径被排除，但这是经人工和工具审查的目标，不是所有 verifier 均完备的证明。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|S080 · §§2.1–2.3 · pp.2–5]]

**本库据此补充：**读评测需要分别核查“题目与验收是否可信”和“Agent 在这个验收下完成得怎样”。Terminal-Bench 的主图为每个模型选择最好 scaffold，测得的是组合表现；人类耗时为作者估计，跨模型平均轮数也不是长程能力的单一量尺。与 MCPMark、Toolathlon 的接口和重复指标比较见 [[wiki/papers/harness/tools/Terminal-Bench#与本库已有评测放在一起看|三篇评测对照]]，不跨任务集比较总分。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|Fig.1 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|§2.4 · p.5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=52|App.G · pp.52–53]]

**测量价值与外推要分开。** 本库判断，这类困难任务集适合比较和诊断选定条件下的系统；要估计真实工作表现，还需核对任务代表性及专业验收要求。专家参与出题、作者估计人类难度、自动诊断与人工标签一致，分别支持不同判断；详见 [[wiki/papers/harness/tools/Terminal-Bench#与人类评价的一致性，验证了哪一层|S080 的分层证据]]，不能将诊断器的一致率当作任务验收正确率。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|§§2.2–2.4 · pp.3–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=9|§§4.4–4.5 · pp.9–10]]

### 回到前作检验“更真实、更可靠”

**新增比较入口：[[wiki/applications/terminal-bench-comparison|读过前作后，Terminal-Bench 还进步在哪里？]]** 2026-10-29 已核读 [[wiki/papers/harness/tools/SWE-bench|SWE-bench]]、[[wiki/papers/harness/tools/SWE-Lancer|SWE-Lancer]]、[[wiki/papers/harness/tools/AppWorld|AppWorld]]、[[wiki/papers/harness/tools/OSWorld|OSWorld]]、[[wiki/papers/harness/tools/tau-bench|τ-bench]]。本库据此将“真实”拆为任务来源、执行环境、验收标准与样本代表性：OSWorld／SWE-Lancer 已有真实执行，AppWorld 的合成环境支持严格状态检查，不能将真实 shell 直接排成质量更高。Terminal-Bench 的多种专业终端任务与审查流程仍有增量，但经济价值和可靠部署外推需另证。[[raw/papers/harness/tools/OSWorld.pdf#page=3|S085 · §§2–3 · pp.3–6]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|S083 · §3.1 · p.5]] [[raw/papers/harness/tools/AppWorld.pdf#page=6|S084 · §3.2 · p.6]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

## 当前不做的推断

此前 Application 六篇阅读对SWE-agent／Agentless、WebThinker、UI-TARS、VideoSeek、Toolathlon做机制核查，其他综述条目仍须按各自实际读取状态判断，不因被提及就升级证据。不能依据分数排列领域难度，也不能从某组件提升推出该侧是主要瓶颈。[[wiki/applications/success-mechanisms|机制综合]]逐项区分论文事实、跨案例推断与尚不能判断；完整过程见 [[组会/2026-10-28-Application/README|Application组会记录]]。

相关机制见 [[wiki/harness/Overview|Harness]] 与 [[wiki/optimization/Overview|Optimization]]；评测真实性和迁移问题见 [[wiki/frontier/Overview|Frontier]]。

返回 [[wiki/index|索引]]。
