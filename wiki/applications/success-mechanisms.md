---
type: topic
created: 2026-10-28
updated: 2026-10-28
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/harness/tools/SWE-agent.pdf]]"
  - "[[raw/papers/harness/workflows/Agentless.pdf]]"
  - "[[raw/papers/optimization/finetuning/UI-TARS.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf]]"
  - "[[raw/papers/harness/tools/VideoSeek.pdf]]"
  - "[[raw/papers/harness/tools/Toolathlon.pdf]]"
---

# 已有应用为何有效：成功机制与瓶颈

准备 PPT 时可直接使用文末的 [[wiki/applications/success-mechanisms#PPT 提炼：五类应用为什么有效、卡在哪里|五段机制提炼]]；前文保留实验依据与归因边界。

本轮六篇原始文献支持的判断是：已有成效通常来自**模型判断、可操作的接口、环境中的信息与反馈相互配合**；支持“组件有用”的证据多于支持“某一侧是主要瓶颈”的证据。以下“论文事实”指各原论文报告结果，未复现；共同原因与瓶颈归纳均为跨案例推断。

综述§6、Fig.14按接口分类，五类彼此重叠；图中反馈强弱不是难度排名。§6.6还提醒总分混合模型、harness及训练贡献。我们完整核读了pp.55–67；通用Agent仅选§6.5.1跨应用数字任务，多模态仅选§6.4.1视频理解，不外推全部子领域。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=55|S001 · §6/Fig.14 · pp.55–57]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=64|§6.6 · pp.64–67]]。

| 应用／任务 | 已有成效：限定配置内的论文事实 | 环境、状态与 model/harness 分工 |
| --- | --- | --- |
| 软件工程：修复仓库issue | SWE-agent同GPT-4 Turbo、每题4美元上限，在SWE-bench Lite为18.0%，shell-only为11.0%；移除专用编辑降至10.3%。 | 仓库、终端、编译测试提供可执行但不完整的反馈；保留代码、补丁和诊断。模型定位与修复；harness把搜索、编辑、lint变成易用动作。[[raw/papers/harness/tools/SWE-agent.pdf#page=6\|S071 · p.6 Tables1/3]]。 |
| 信息获取：复杂网页问答 | WebThinker同QwQ-32B基础下，WebWalkerQA固定Query Planning RAG为32.5%，交互Base为41.9%，训练后46.5%。 | 网页和链接提供证据，运行时无答案oracle；保留子问题、网页线索与报告草稿。模型决定查什么及如何综合；harness负责浏览、内容提取和草稿读写。工具与计算量并未完全匹配。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=6\|S074 · pp.6–9 Tables1/3]]。 |
| 计算机操作：桌面多步任务 | UI-TARS作者协议下，72B、OSWorld截图、15步上限，SFT18.8%，DPO22.7%。 | 截图只暴露部分状态；保留最近截图及动作历史。模型负责定位、动作与恢复判断；harness执行鼠标键盘并回传观察。不可行轨迹计分细则未确认。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=25\|S073 · pp.25–26 Table9]]。 |
| 多模态：长视频问答 | VideoSeek在LVBench无字幕、最多20轮为68.4%；同GPT-5固定384帧60.1%，改用它选出的约92帧为63.9%。 | 原视频允许按时段重复读取；保留时间定位与已见证据。模型选择概览、扫读、细看及停止；harness执行采样、调用GPT-5感知并组织历史。[[raw/papers/harness/tools/VideoSeek.pdf#page=12\|S075 · p.12 Table5]]。 |
| 通用：简历→Notion→邮件 | Toolathlon刊载Claude-4-Sonnet一条45次调用的成功轨迹；全套108任务统一100轮上限，Claude-4.5-Sonnet配置pass@1为38.6%，三次皆成功仅20.4%。 | 原件、岗位库、权限及预配的相关MCP服务器构成条件；模型匹配实体、解释错误、决定下一步；harness连接工具并保留可回查历史。单例不代表稳定成功。[[raw/papers/harness/tools/Toolathlon.pdf#page=7\|S076 · p.7 Table3、pp.31–36]]。 |

**跨应用的共同成功原因。**以下三条为本库推断，各有原论文支点；不是综述的统一因果结论。

**第一，把领域操作和相关信息组织成模型能有效使用的形式。**SWE-agent的收益来自紧凑编辑、搜索结果和上下文设计；VideoSeek通过问题驱动的帧选择，比固定读取更多帧更有效。这既包含领域接口知识，也包含观测分配，并非只有“模型更强”。但VideoSeek少用帧不等于运行更快，其无字幕配置运行时间反而更长；接口改进也不证明harness已解决语义判断。[[raw/papers/harness/tools/SWE-agent.pdf#page=6|S071 · Table3 · p.6]]；[[raw/papers/harness/tools/VideoSeek.pdf#page=12|S075 · App.A.1/A.3 · p.12]]。

**第二，把大任务分成可处理步骤，并用外部产物维持约束。**WebThinker把搜索与报告草稿交错，移除自动草拟后报告模型评审分由8.1降至6.6；Toolathlon成功轨迹先查询岗位结构，再把简历映射为记录和邮件。这支持“中间结构有用”的解释，但后一案例没有消融。软件工程的Agentless尤其提醒：固定定位—修复—测试选择流程也能取得成效，自由规划不是必要前提。不能将所有收益都归于动态验证。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|S074 · Table3 · p.9]]；[[raw/papers/harness/tools/Toolathlon.pdf#page=31|S076 · App.E.2 · pp.31–36]]；[[raw/papers/harness/workflows/Agentless.pdf#page=6|S072 · §3 · pp.6–9]]。

**第三，反馈可推动局部进展，整任务完成仍需核对完整目标与副作用。**Agentless固定候选下加入回归与复现测试，解决数由多数票77/300增至96/300；Toolathlon成功轨迹也能根据API错误修正格式。但前者生成的复现测试并不总能识别真实修复，后者另一个案例选对checkpoint却漏上传依赖图片。局部通过可以支持下一步，不能独自证明整任务完成。[[raw/papers/harness/workflows/Agentless.pdf#page=11|S072 · §§5.1.3、5.2.3 · pp.11–14]]；[[raw/papers/harness/tools/Toolathlon.pdf#page=18|S076 · App.E.2 · pp.18、27–30]]。

这些共同机制还依赖领域知识和任务本身可分解：代码修复需要理解程序语义，网页报告需要判断论据关系，跨应用操作需要识别对象与格式。外部状态降低了记忆负担，却不会自动保证状态正确；工具扩大了行动范围，也没有自动提供可靠的任务规格。这是跨案例机制推断，不是已有统一消融。

**model 与 harness 的瓶颈比较。**当前瓶颈需要与上述成功依赖分开判断。能力瓶颈指完成任务仍缺什么，不能按搭建组件的工程工作量判断，更不能把不同benchmark分数排成领域难度。

- **软件工程：有明确harness干预收益，剩余瓶颈仍耦合。**专用编辑消融能识别接口作用；测试的语义错误和真实需求覆盖不足，则涉及模型诊断、验证设计与环境规格。不能从18.0→10.3便推出harness比model更难。[[raw/papers/harness/tools/SWE-agent.pdf#page=6|S071 · Tables1/3 · p.6]]；[[raw/papers/harness/workflows/Agentless.pdf#page=11|S072 · §5.1.3 · pp.11–12]]。
- **信息获取：获取与使用证据耦合，且任务类型不同。**WebThinker去掉深层浏览会降分，训练同框架策略也会提升问答；但报告生成训练前后仅8.0→8.1，主要收益更符合流程与产物组织。报告裁判明确不检查引用，不能将高评分当成可追溯性已验证。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|S074 · Table3 · p.9]]；[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=24|App.C.3.2 · p.24]]。
- **GUI：模型侧存在干预证据，整体不足不能单归模型。**UI-TARS在所报接口与协议下，改变训练配置能改善得分；但视觉定位、状态历史、步数预算与恢复共同决定结果。与代码测试不同，界面改变通常只证明动作发生，是否达到目标还要解释状态或检查产物。它也没有穷尽harness替换，无法证明harness改善无效。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=25|S073 · §5.4–5.5 · pp.25–27]]。
- **多模态理解：证据获取与推理能力共同限制。**VideoSeek的同帧对照支持“看到了什么”解释一部分收益；同框架更换思考模型也改变准确率，但轮数随之变化。剩余68.4−63.9个百分点不能全部归于纯推理，仍包含多轮交互、感知输出组织及预算差异。[[raw/papers/harness/tools/VideoSeek.pdf#page=7|S075 · Tables3/5 · pp.7、12]]。
- **跨应用：已有资源未被充分利用的策略失败可见，但宜判耦合。**Toolathlon记录了漏处理对象、提前结束和产物依赖遗漏。模型会错用已有信息，外部覆盖清单与结束条件也可能影响表现；缺少相应替换消融，尚不能确定主导侧，更不能外推机器人或专业服务。[[raw/papers/harness/tools/Toolathlon.pdf#page=15|S076 · App.C.2/E.2 · pp.15–18]]。

**主动验证与能力内化。**本轮较直接的证据是**任务相关的观察选择与测试筛选有用**。VideoSeek同帧实验支持它选出的证据集合有效；尚未隔离在线自适应的必要性，也没有匹配选择成本与多轮计算。可回访、线索可定位的环境使这种机制合理；突发、难预测事件则是作者承认的边界。WebThinker相对固定检索更好，但同时改变浏览工具、信息范围及调用量，动态策略的独立收益尚不能区分。Agentless则证明，一部分收益可由固定流程中的测试筛选解释；本轮未建立普遍优于传统领域方法的结论。[[raw/papers/harness/tools/VideoSeek.pdf#page=12|S075 · App.A.3 · p.12]]；[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=6|S074 · Tables1/3 · pp.6、9]]；[[raw/papers/harness/workflows/Agentless.pdf#page=14|S072 · Table4 · p.14]]。

职责应拆成三步：模型或固定规则**选择**下一项检查；工具、解释器或感知模型**执行**检查；模型或确定规则**解释结果并修订、停止**。代码测试依据可执行规格，视频与网页返回的是需判断的证据，Toolathlon终态评分脚本属于评测者。三者的可信来源不同。[[raw/papers/harness/workflows/Agentless.pdf#page=8|S072 · §3.3 · pp.8–9]]；[[raw/papers/harness/tools/VideoSeek.pdf#page=4|S075 · §3.2–3.3 · pp.4–5]]；[[raw/papers/harness/tools/Toolathlon.pdf#page=5|S076 · §2.4 · p.5]]。

能力内化方面，WebThinker用正确性优先并兼顾工具/推理效率的轨迹偏好训练策略，UI-TARS用交互反思与偏好数据改进动作选择；它们支持行为可训练。WebThinker适配其他骨干仍经过SFT/RL，UI-TARS跨域思考收益也不一致，均不能证明能力脱离原harness迁移。**训练改善了如何使用流程；是否减少外部流程负担，本轮证据尚不能判断。**


训练依据：[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=5|S074 · §3.5、§4.6 · pp.5–7、9]]；[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=21|S073 · §4.5–5.5 · pp.21–27]]。

## 原论文与读取范围

本轮仅6篇，不构成领域全覆盖。以下唯一页保存版本、SHA-256、读取范围和完整限定；原论文链接用于在线核对。

- [[wiki/papers/harness/tools/SWE-agent|S071 SWE-agent]] · [2405.15793v3](https://arxiv.org/abs/2405.15793v3)。
- [[wiki/papers/harness/workflows/Agentless|S072 Agentless]] · [2407.01489v2](https://arxiv.org/abs/2407.01489v2)。
- [[wiki/papers/optimization/finetuning/UI-TARS|S073 UI-TARS]] · [2501.12326v1](https://arxiv.org/abs/2501.12326v1)。
- [[wiki/papers/optimization/reinforcement-learning/WebThinker|S074 WebThinker]] · [2504.21776v2](https://arxiv.org/abs/2504.21776v2)。
- [[wiki/papers/harness/tools/VideoSeek|S075 VideoSeek]] · [2603.20185v1](https://arxiv.org/abs/2603.20185v1)。
- [[wiki/papers/harness/tools/Toolathlon|S076 Toolathlon]] · [2510.25726v2](https://arxiv.org/abs/2510.25726v2)。

## PPT 提炼：五类应用为什么有效、卡在哪里

以下是基于本轮案例的**本库提炼**，用于讲清机制差异；“卡点”指证据暴露的具体困难，不表示已经测出整类应用的首要瓶颈。多模态限长视频理解，通用 Agent 限跨应用数字任务。

**软件工程：容易把尝试变成反馈，难在把“过检查”变成“真修好”。** 代码可以搜索、修改和运行，模型的修复想法能迅速接受测试；SWE-agent把这些操作做得顺手，Agentless甚至用固定流程也能获得收益。当前卡点是：能否找准原因，以及测试是否真的代表需求。生成测试本身会错，过了现有检查也可能只是修掉表面症状。因此，这类应用的优势是可执行、可反复检查；进一步可靠的关键在诊断与验收，不能只增加操作自由度或测试次数。[[raw/papers/harness/tools/SWE-agent.pdf#page=6|S071 · §5.1、Table3 · pp.6–7]]；[[raw/papers/harness/workflows/Agentless.pdf#page=11|S072 · §5.1.3 · pp.11–12]]。

**信息获取：有效的是逐步补齐知识缺口，难的是判断证据何时足够。** WebThinker把大问题拆成可继续搜索的线索，沿网页深入，再把材料组织进草稿；收益既来自找到更多相关内容，也来自保留和组织已有内容。它缺少软件测试那样的直接判定：有材料不等于支持结论，报告完整不等于引用可信。当前卡在“下一步还缺什么、已有证据能否支撑回答、何时停止”。浏览和训练都有收益，但本轮没有拆清漏检与误解各占多少；报告评分也未验证引用，不能把写得好当成查得准。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=4|S074 · §3 · pp.4–5]]；[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|Table3 · p.9]]；[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=24|App.C.3.2 · p.24]]。

**计算机操作：把屏幕和键鼠变成通用接口，难在持续判断“现在到底是什么状态”。** GUI Agent通过截图找目标、执行动作、再看结果，能够把多步操作接起来。困难在于每一步都要把画面、对象和动作对准：点到了不等于生效，画面变化也未必由刚才的动作引起；判断错了，后续操作就可能沿着错误状态继续。UI-TARS的训练对照表明，交互策略本身可以改善，不能只把困难归为接口工程；但尚未分清剩余错误有多少来自看错、决策错或状态不可见。这里应重点看感知—行动—再确认能否持续可靠。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=15|S073 · §4.1–4.3 · pp.15–17]]；[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=25|§5.4、Table9 · pp.25–26]]。

**多模态理解：先把有限观察用在关键位置，再谈能否理解。** 长视频里，大量内容与问题无关。VideoSeek先找线索，再回看局部，选出的少量帧比固定读取更多帧更有效，说明“没看到关键信息”本身就是重要障碍。卡点有两层：关键片段能否被发现，以及画面转成描述、进入推理后是否失真。突发、难预测的事件尤其可能被跳看漏掉。已有对照能确认选证据有价值，却不能把余下收益全算成推理增强，也没有证明动态观察在同预算下必胜固定流程。[[raw/papers/harness/tools/VideoSeek.pdf#page=12|S075 · App.A.3、Table5 · p.12]]；[[raw/papers/harness/tools/VideoSeek.pdf#page=8|§5 · p.8]]。

**通用 Agent：把现成能力串成一件事，难在保证整件事没有漏项。** Toolathlon的成功案例把读简历、查岗位、填表和发信连起来，关键是跨工具保持同一个人、同一条规则和同一个目标。跨接口后多了一层完整交付要求：选对模型却漏上传图片、处理完一年就提前结束，局部都可能做对，整体仍失败。本轮最明确暴露的是对象覆盖、产物依赖和结束判断，而非工具数量不足。检查清单与状态记录可能帮助，但尚无消融证明加上它们就能解决；现有证据支持盯住完整交付，不能直接指定由 model 或 harness 单独负责。[[raw/papers/harness/tools/Toolathlon.pdf#page=16|S076 · App.C.2/E.2 · pp.16–18]]；[[raw/papers/harness/tools/Toolathlon.pdf#page=31|成功轨迹 · pp.31–36]]。

形成过程与单轮审查：[[组会/2026-10-28-Application/README|Application组会]]。返回 [[wiki/applications/Overview|应用地图]] · [[wiki/index|索引]]。内容核读不等于复现；Obsidian内显示未测。
