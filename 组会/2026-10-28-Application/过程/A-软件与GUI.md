# A｜软件工程与GUI：成效如何产生，瓶颈如何判断

2026-10-28；范围为S001 §6.1、§6.3与S071–S073三篇原论文。这里只解释已有应用，不提出新方向或实验。下文机制归纳是本库分析；数字是各论文规定条件下的报告结果。原件版本、哈希、实际读取范围见各唯一来源页。

## 软件工程：可执行反馈有价值，但检查本身也会错

**具体成效。**[[wiki/papers/harness/tools/SWE-agent|SWE-agent]]用GPT-4 Turbo，在SWE-bench Lite 300题、每题API上限4美元下解决18%；同模型Shell-only为11%。输入为issue与代码仓库，输出是通过评测测试的补丁，不能直接外推到完整产品开发。[[raw/papers/harness/tools/SWE-agent.pdf#page=5|S071 · §4–5 · pp.5–6 · Table1]]

**为什么有效。**环境提供可搜索的文件、可执行程序及可观察错误；harness把它变成紧凑的定位—编辑—执行循环：摘要搜索降低无效翻页，带行号文件窗稳定编辑目标，单次范围替换立即显示新状态，lint拒绝坏编辑，旧观察压缩减少过时代码干扰。模型承担故障解释、修复实现和测试选择。固定GPT-4 Turbo的消融中，去掉专用edit降至10.3%，去lint为15%，改逐条搜索为12%，全历史为15%。这支持harness贡献，但不允许把贡献相加，也不是匹配全部token消耗后的比较。[[raw/papers/harness/tools/SWE-agent.pdf#page=3|S071 · §3 · pp.3–4]] [[raw/papers/harness/tools/SWE-agent.pdf#page=6|Table3 · pp.6–7]]

**自主程度不是成效解释。**[[wiki/papers/harness/workflows/Agentless|Agentless]]固定定位—修复—验证流程，以树/骨架逐层缩窄代码，四组位置各生成10补丁，再执行回归及生成复现测试筛选。GPT-4o、300题、40补丁与40测试候选的整套配置解决96题；模型/预算不同，不能把32%与SWE-agent的18%当作自主性的因果比较。更有力的是同候选选择消融：多数票77题，加回归81题，再加复现96题。[[raw/papers/harness/workflows/Agentless.pdf#page=9|S072 · §4–5 · pp.9–10]] [[raw/papers/harness/workflows/Agentless.pdf#page=14|§5.2.3 · Table4]]

**为什么两层都不够。**模型有代码能力却会受操作接口限制；接口改善也未消除语义错误。SWE-agent未解决轨迹约52%被标为错误/过度特定实现，23.4%为编辑恢复失败，但这是自动分型线索，不是因果分摊。Agentless更直接暴露验证边界：213个测试在原代码报“复现”，只有94个在开发者正确补丁后报“解决”。主动验证必须拆成选择/生成检查、执行检查、解释结果并修订/停止；第二步可自动执行，不能替第一和第三步担保。[[raw/papers/harness/tools/SWE-agent.pdf#page=8|S071 · §5.2 · Fig.8]] [[raw/papers/harness/workflows/Agentless.pdf#page=11|S072 · §5.1.3 · pp.11–12]]

## GUI：模型侧有干预证据，反馈解释仍依赖运行环境

**成效及机制。**[[wiki/papers/optimization/finetuning/UI-TARS|UI-TARS]]把GUI截图感知、坐标grounding、动作序列与纠错训练进Qwen2-VL。它不仅标注“这一步应怎样做”，还标注“坏动作已经发生后怎样恢复”，以SFT与DPO学习；运行时保留最近5张截图和完整思考/动作历史，由外部执行器落实键鼠动作。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=15|S073 · §4.1 · p.15]] [[raw/papers/optimization/finetuning/UI-TARS.pdf#page=21|§4.5–4.6 · pp.21–22]]

OSWorld截图输入、15步下，72B-SFT为18.8%，72B-DPO为22.7%；同DPO增到50步为24.6%。这支持训练改变策略的实际作用，不能归为纯harness收益，也不能只从整套配置胜过其他系统推导模型优越。CallUser或未Finish轨迹被称为不可行，具体计分/分母处理未确认。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=25|S073 · §5.4 · pp.25–26 · Table9]]

**环境优势与限制。**屏幕和键鼠提供跨软件的公共接口，动作后可重新观察；但截图是局部可见状态，变化可能来自动画/后台刷新，成功动作不必然意味着目标完成。训练加入相邻截图变化解释；恢复示例只证明特定情形可补偿。登录/认证有CallUser，权限并非模型推理能补齐。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=16|S073 · §4.2–4.3 · pp.16–17]]

**剩余判断。**同模型切换thought，域内单次采样略差、域外AndroidWorld更好，说明推理帮助受任务和预算制约。软件的测试返回显式结果，但检查语义仍可能错；GUI反馈经常还要先推断“状态变了什么”。现有证据支持GUI模型侧有改善空间，却不足以量化剩余失败属于感知、规划、状态暴露或执行控制。最稳妥结论是耦合瓶颈，不能由界面复杂直接判定harness不足。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=26|S073 · §5.5 · pp.26–27 · Fig.8]]

## 交付边界

三篇均为已读待整合；共享主题、索引与日志由主Agent完成。未审运行代码、未复现实验、未实测Obsidian。已看关键原页图表；没有把个别成功案例当普遍有效性，也没有将生成测试、截图或作者失败解释升级为可靠判定器。正式入口为 [[wiki/applications/Overview|应用与评测]]。
