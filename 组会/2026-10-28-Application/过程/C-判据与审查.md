# C：统一判据与证据审查

## 首轮统一判据

先按“任务与成效→环境→机制→model/harness贡献→证据→边界”逐项记录，不给五类应用预排名。成效必须绑定具体任务、输入和环境、比较基线、指标及预算；仅展示可运行或个别成功的，写可行性而非稳定提升。环境另记可观测性、反馈可信度、可恢复性与工具权限。瓶颈指当前失败所必需却不足的能力，工程工作量指已有能力的接入、编排、成本和可靠性负担，两者可并存；归属允许model、harness、耦合、环境或证据不足。归因优先核对同模型换harness、同harness换模型、模块消融、训练对照，并用成功/失败轨迹检查机制；同步排查预算、权限、输入信息及训练数据混杂。系统总分只证明整套配置的表现，作者解释仅提供机制线索，单次案例只能支持局部可行性，均不能单独分配贡献比例。主动验证拆为选择何时与何种检查、实际执行、解释结果并修订或停止，逐步确定责任与可见证据。综述转述不升级为原论文实证；缺失条件明确记未确认。

C模型：gpt-6-astra，reasoning high。初稿先发主Agent，再同版交A/B；未预看各类排名。

## 唯一全量审查｜2026-10-28

审查对象为同批次综合初稿、A/B 与主 Agent 的案例交付。采用 academic-researcher 技能检查结果与归因边界；独立回读六篇原文的决定性对照：SWE-agent PDF pp.5–6；Agentless p.14；UI-TARS pp.25–27；WebThinker pp.6、9、24；VideoSeek pp.5、7、12；Toolathlon pp.7、16、18。未审代码、未复现实验，不扩展文献。本节是一次合并审查，后续由主 Agent 一次收敛，不追加讨论轮次。

**总判断：主体比较部分支持，完成以下收窄后可交付。**初稿没有将五类排成高低，也没有把系统总分分摊为 model/harness 比例；单例与总体统计、运行时工具返回与评测 oracle、训练改善与脱离 harness 迁移已大体分清。主要问题是个别总结句超过对照识别范围，以及短稿省略了会改变解释的输入与预算。

### 必须修改的六处

1. **主动验证的普遍适用条件尚未被识别。**“最强的正面证据在下一条有价值观察不能预先确定……”把本库机制解释写成了受验证的适用条件；“同帧实验直接支持主动选择观察”也容易被读成已证明在线自适应本身必要。建议整段开头改为：“本轮较直接的证据是：任务相关观察选择与测试筛选能改善指定配置的结果。VideoSeek 所选帧交给同 GPT-5 后优于均匀384帧，支持该证据集合更有用；它没有比较同工具、同总预算的固定选帧策略，选帧过程的调用成本也未匹配，尚不能单独证明动态性本身的收益。”后接 WebThinker 混杂与 Agentless 固定流程反例即可。根据 [[raw/papers/harness/tools/VideoSeek.pdf#page=12|S075 · 附录A.3 · Table5 · p.12]]、[[raw/papers/harness/workflows/Agentless.pdf#page=14|S072 · §5.2.3 · Table4 · p.14]]。

2. **关键输入、预算和权限应在综合稿就近保留。**软件行补“300题、每题API上限4美元；实际消耗未匹配”；视频行补“无字幕，最多20轮，默认思考与感知均调用GPT-5”，不能让68.4与有字幕配置混淆；通用行补“各模型100轮上限，预配任务相关MCP服务器及通用工具”，并写明单例为Claude-4-Sonnet、总体最高为Claude-4.5-Sonnet。WebThinker可在脚注或正文补“主模型QwQ-32B、另有助手模型，生成上限81,920 tokens，工具/实际计算未匹配”，避免同骨干被理解成同一模型调用资源。根据 [[raw/papers/harness/tools/SWE-agent.pdf#page=5|S071 · §4 · p.5]]、[[raw/papers/harness/tools/VideoSeek.pdf#page=5|S075 · §4.1 · p.5]]、[[raw/papers/harness/tools/Toolathlon.pdf#page=7|S076 · §4.1 · p.7]]；WebThinker配置沿唯一页的§4.3与附录A定位。工程接入工作多，并不单凭工作量证明当前能力主要受harness限制。

3. **视频工具中的感知本身也是模型计算。**表格“harness执行采样、感知并组织历史”建议改为“harness采样、调用感知模型并组织历史；GPT-5解释画面、选择后续观察与作答”。该修改避免将工具内部的模型能力算成纯harness贡献；主模型替换实验只替换思考模型，不能理解为整个系统所有模型同时替换。根据 [[raw/papers/harness/tools/VideoSeek.pdf#page=5|S075 · §4.1 Base Models · p.5]]、[[raw/papers/harness/tools/VideoSeek.pdf#page=7|Table3 · p.7]]。

4. **GUI训练对照不要升级成接口不充分的证明。**将“训练对照说明仅有执行接口并不足够”改为“在作者所报执行接口与评价协议下，更换训练配置提高了得分，说明模型策略侧的干预有用”。表中未穷尽其他harness，也没有建立某一接口能否充分完成任务的定理。保留“不可行轨迹计分细则未确认”即可，无须升级为确定排除失败。根据 [[raw/papers/optimization/finetuning/UI-TARS.pdf#page=26|S073 · §5.4 · Table9 · p.26]]。

5. **局部进展不要求先覆盖完整目标。**“反馈只有被正确解释并覆盖完整目标，才转化为进展”过强；建议改为“反馈经解释可以推动局部进展；判定整任务完成，还需检查完整目标与副作用”。后面的测试筛选、遗漏图片正好支持此区别。根据 [[raw/papers/harness/workflows/Agentless.pdf#page=14|S072 · §5.2.3 · p.14]]、[[raw/papers/harness/tools/Toolathlon.pdf#page=18|S076 · 附录E.2 · p.18]]。

6. **证据身份与相邻定位需随正式稿保留。**开头“论文事实指原实验”改为“数值与案例均为已核读原论文的报告结果，本轮未复现；跨案例原因与瓶颈判断为本库归纳”。正式稿的“见p.X TableY”转换为邻近Raw链接，不仅依赖文末来源表。报告评分8.1→6.6需明确为30个Glaive问题上的模型评审均分，且不审引用；不要以一个评分消融推出报告事实准确性或现实研究完成度。根据 [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|S074 · Table3 · p.9]]、[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=24|附录C.3.2 · p.24]]。

### 已核查、应保留的边界

- **UI-TARS协议：部分支持训练配置差异，不支持确定的分母指控。**同72B、同OSWorld截图输入、同15步上限，18.8→22.7是作者报告的3.9个百分点增幅；24.6另属50步。p.26确实称CallUser与未Finish轨迹为infeasible，但所读正文未明确计失败、排除或其他计分操作，不能据一句话断言已排除分母。若两配置产生不同数量的此类轨迹且处理影响样本总体，可能影响可比性；这是条件风险，尚无发生证据。负样本改善动作区分属于作者机制解释，不等于单独识别规划、感知或恢复增益。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=25|S073 · §5.4 · pp.25–26]]
- **WebThinker：有流程与训练干预，不存在引用审计结论。**固定QwQ骨干的Query Planning RAG32.5、Base41.9、RL46.5与Table1一致；不能与其他模型RAG行混用。报告Base8.0、RL8.1和去自动草拟6.6与Table3一致，但评审明确不考虑引用。Table3均值45.4与正文44.9的不一致已避开，不需以猜测修正原文。[[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=6|S074 · Table1 · p.6]] [[raw/papers/optimization/reinforcement-learning/WebThinker.pdf#page=9|Table3／§4.7 · p.9]]
- **VideoSeek：收益不能等同速度或纯推理。**Table5同帧差额不能全部归于推理能力；多轮调用、视觉转文本、提示和预算同时存在。无字幕测得耗时更长应写作“作者此次测量更长”，保留网络、后端等条件，不能推广为方法必然更慢。[[raw/papers/harness/tools/VideoSeek.pdf#page=12|S075 · 附录A.1／A.3 · p.12]]
- **Toolathlon：单例与总体、工具与裁判分层正确。**45次调用成功属于Claude-4-Sonnet的Notion HR轨迹；38.6±2.7%和20.4%属于Claude-4.5-Sonnet在108任务的总体结果。漏项、早停与漏上传图片可以说明可见失败，不足以确定模型或harness主导。终态评分脚本是评测条件，不能写成Agent随时拥有的正确性oracle；环境初始化也不是在线回滚。[[raw/papers/harness/tools/Toolathlon.pdf#page=7|S076 · Table3／§4.1 · p.7]] [[raw/papers/harness/tools/Toolathlon.pdf#page=16|附录C.2 · p.16]] [[raw/papers/harness/tools/Toolathlon.pdf#page=18|附录E.2 · p.18]]
- **Agentless：固定流程反例成立。**77→81→96是在候选补丁选择中加入回归与复现测试的结果，测试生成有额外成本；支持固定流程中验证有用，不与SWE-agent跨模型、跨预算分数构成“自由规划更差”的因果比较。[[raw/papers/harness/workflows/Agentless.pdf#page=14|S072 · §5.2.3 · Table4 · p.14]]

修订后的归因结论应停在：已有接口干预、训练干预与轨迹证据说明若干组件有用；对当前主导瓶颈的判断多为条件性耦合或证据不足。主动验证三步分工可作为解释框架，不作为五类应用都已具备可靠验收能力的事实。该结论没有要求新方向、补充实验或扩展来源。
