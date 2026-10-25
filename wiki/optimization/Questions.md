---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/C3.pdf]]"
  - "[[raw/papers/optimization/distillation/DAgger-LLM.pdf]]"
  - "[[raw/papers/optimization/finetuning/Agent-R.pdf]]"
  - "[[raw/papers/optimization/self-evolution/Environment-Tuning.pdf]]"
  - "[[raw/papers/optimization/self-evolution/R-Quest.pdf]]"
---

# Optimization：第一轮问题与关闭依据

## 第一轮Brainstorm结案


本轮在七个一级方向的已读材料上先形成独立首稿，再互评、定向补读并完成第二轮修订，保留 **O-A、O-B两项供亲读调查的材料问题，没有新颖性已确认的研究缺口**。代码核查解决部分实现疑问，C3与R-Quest关闭部分宽泛动机；这些结果不等于选定研究方向。以下区分原文证据、本库推断与尚缺材料，未执行所提实验，同模型意见一致不增加证据强度。

### O-A：局部比较组究竟提供什么信用信息

**状态与范围。** 从“尚不知道分组键”收窄为“实际组的比较条件与更新含义待核”。范围限GiGPO所测可重复访问的数字环境及已审公开实现；讨论局部回报排序可以怎样解释，不预设分组错误或训练受损。

**支持证据。** GiGPO原文在同状态后比较折扣回报，并与episode优势组合。官方公开commit `20bd331bdbc9026a5668e11362178e10ab7400c8`中，分组anchor与含历史、步数的策略输入分开；分组没有另加历史或预算键，同轨迹重复访问可入组，均值含自身，标准化可选，组合优势之后进入actor ratio clip。该commit未被确认为论文实验版本，也未取得可核实际组样本，因此不能量化决策条件差异、相关性或损害。[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf#page=5|S053 §4.2–4.3 · pp.5–6]]；[[wiki/papers/optimization/reinforcement-learning/GiGPO#公开实现核查：分组观察与策略输入分别保存|固定版本、源码行号与原件哈希]]。

**最近工作与剩余区别。** Tree-GRPO主动共享前缀采分支；C3进一步规定可恢复的完整因果状态、冻结行为策略、独立替代和接续、非自适应次数，给出可执行反事实参照。GiGPO复用自然访问的重复状态；剩余问题是实际组中哪些差异影响决策，以及信号变化来自条件混合、组规模、样本相关性还是归一化。C3的严格条件解释其估计对象，不能直接变成GiGPO必须满足的算法前提。[[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=4|S054 §3.1–3.2 · pp.4–5]] [[raw/papers/optimization/reinforcement-learning/C3.pdf#page=4|S068 §2.3–2.4 · pp.4–5]] [[raw/papers/optimization/reinforcement-learning/C3.pdf#page=15|A.2 · pp.15–16]]

**最强反对。** 不同历史不自动使动作无关baseline产生策略梯度偏差。GiGPO Appendix C只对episode优势、常数分母`Fnorm=1`给出固定N下的`N/(N−1)·AE=RLOO`缩放；它反对“自包含必有方向错误”，也没有证明随机step组、相关样本、std及完整clipped混合目标无偏。更细分组还可能令样本减少甚至无组可比；局部排序更易解释，不保证终局策略更好。[[raw/papers/optimization/reinforcement-learning/GiGPO.pdf#page=16|S053 Appendix C · pp.16–17]] [[raw/papers/optimization/reinforcement-learning/Tree-GRPO.pdf#page=10|S054 Table4 · p.10]]

**下一证据与关闭条件。** 优先取得论文运行版本/配置及组成员的anchor、策略上下文、步数、轨迹身份、return和有效组规模，再判断差异是否决策相关。有限检索未定位样本，不证明作者未公开。若没有相关差异，关闭具体错误合并解释；若现有分析已覆盖该配方，或只是已知缩放/方差且无异常需解释，关闭“修复分组”的方法动机。只有材料支持进一步区分时，才考虑获授权后固定rollout、匹配组规模的比较；不能先把改key当改进方案。

亲读顺序：GiGPO pp.5–6、16–19及已审代码→C3 p.4、pp.15–16、26。重点分清估计对象、实际更新与采样成本。C3有限预算诊断排除无法排序的组，每个替代另给四次接续，不能与训练共享叶子的预算或GiGPO复用既有轨迹直接等同。[[raw/papers/optimization/reinforcement-learning/C3.pdf#page=26|S068 B.5 · p.26]]

### O-B：哪些学生失败前缀真正进入训练

**状态与范围。** 保留材料问题，暂缓“按诊断调节辅助退出”的方法主张。限定S057的软件修复任务、OpenHands接口与教师/学生混合采样，先核对“访问→标注→保留→更新”，不把教师执行比例当教师查询成本或恢复状态覆盖率。

**支持证据。** S057每个访问状态查询教师标签，实际执行者可以是教师或学生；DAgger、AggreVaTe、OPD均过滤无有效最终patch提交的整条轨迹，保留数随批次变化。这里的 **valid submission不等于passing tests**：Table5将在线方法的Valid submissions与SFT的Passing patches明确分列。已访问和已标注的失败前缀，未必进入更新；这是数据路径事实，不能直接推出筛选损害。[[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=4|S057 §3.2 · pp.4–5]] [[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=18|F.2/Table5 · p.18]]

**最近工作与剩余区别。** DAgger/AggreVaTe已有混合执行与学生前缀后接管，Agent-R已有失败恢复训练，Environment-Tuning已有撤去增强反馈阶段。因此“让学生犯错后救场”“最终撤辅助”均不能直接称为新方法。保留区别是辅助信息权限、实际访问分布和最终入训分布的分解。固定前缀撤提示主要改变信息，自由运行还改变状态占据，最终过滤再次选择样本；诊断能区分它们，不证明据此选课程有效。[[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=17|S057 F.1 · p.17]] [[raw/papers/optimization/finetuning/Agent-R.pdf#page=11|S050 §4.4/Table3 · p.11]] [[raw/papers/optimization/self-evolution/Environment-Tuning.pdf#page=5|S065 §3.2 · p.5]]

**最强反对。** 教师既可能避免进入坏状态，也可能救回失败前缀，使其标签得以保留；过滤也可能只清理基础设施异常或无用轨迹。S057独立学生测试已有正面结果，未测的筛选解释不能推翻它。动作CE与OPD监督目标不同，同β或同批任务数亦不足以匹配训练材料和总成本。[[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=8|S057 §4.3–4.4/Table4 · p.8]] [[raw/papers/optimization/distillation/DAgger-LLM.pdf#page=18|F.2 · p.18]]

**下一证据与关闭条件。** 核读valid定义/实现、过滤前后轨迹及状态统计、排除原因、教师介入位置、可用标签与全部采样成本。若主要删除基础设施坏样本，关闭关键失败监督流失解释；若已有保留数、失败类型及成本匹配的分析足以解释效果，关闭该归因缺口。材料不足则暂停，不能以未见消融认定研究空白，也不预告新课程收益。亲读顺序：S057 p.4→pp.17–18→p.8，先指出执行者、标签者、保留单位和测试对象。

### 已关闭的宽泛提法与适用边界

O-C的“坏题与重复导致自演化失稳，加入验证和去重”已被R-Quest直接覆盖，不保留第三张候选卡。其题目修复、有效性与新颖度干预支持有限实验条件下的改善；初始化外部标注及每轮10%标注回放仍在，新增题仍有多数票伪标签和额外判定成本。不能升级为零外部监督、同预算效率更高或无限持续进步；这些边界也不自动构成新研究缺口。[[raw/papers/optimization/self-evolution/R-Quest.pdf#page=3|S069 §2 · pp.3–4]] [[raw/papers/optimization/self-evolution/R-Quest.pdf#page=7|§4.3 · pp.7–9]] [[raw/papers/optimization/self-evolution/R-Quest.pdf#page=14|A.1–A.2 · pp.14–15]] [[raw/papers/optimization/self-evolution/R-Quest.pdf#page=19|C.2 · p.19]]

七方向的关闭针对本轮宽泛创新表述，不表示该方向研究完毕；原始论证与适用条件保留在对应综述段。

| 方向 | 本轮不再保留的宽泛提法；已有证据入口 |
| --- | --- |
| 架构基础 | 更长窗口或更省KV自然解决长期记忆；见[[wiki/optimization/architecture#容量、检索、任务质量和效率分别举证\|容量、访问与任务证据]]。 |
| 数据与环境合成 | 多生成真实工具轨迹就解决数据质量；见[[wiki/optimization/data-environments#筛选不只改变质量，也改变能学到的状态\|执行与筛选条件]]。 |
| 预训练与中期训练 | PPL/找针改善足以预测Agent收益；见[[wiki/optimization/pretraining#可接受长度、可用证据与任务成功分别测试\|代理指标与任务测试]]。 |
| 微调 | 只需关键步监督或失败恢复；见[[wiki/optimization/finetuning#状态由谁产生，哪些输出受到监督\|监督位置与状态来源]]。 |
| Agentic RL | 从终局反馈增加局部信用尚无方法；见[[wiki/optimization/reinforcement-learning#局部比较组从哪里来，决定了什么可被区分\|GiGPO、Tree-GRPO与C3]]，收窄为O-A。 |
| On-Policy Distillation | 给学生错误状态教师反馈或撤辅助即是创新；见[[wiki/optimization/distillation#状态由谁产生，教师能看到什么\|执行与教师信息权限]]，收窄为O-B。 |
| 自我演化 | 加验证、去重即可填补持续演化空白；见[[wiki/optimization/self-evolution#持续进步是待检验属性，不是循环名称\|R-Zero与R-Quest边界]]。 |

跨模块只保留两个接口：O-A的反事实参照受[[wiki/harness/workflows#分支能否撤回，评价能否被信任|状态恢复能力]]约束，保存文本不保证外部世界可重置；O-B的入训选择需对齐[[wiki/harness/verification#检查对象决定成功指标|验收对象与成功指标]]，局部通过、有效提交和终局成功分别登记。上述联系是本库综合，不表示这些方法已联合训练；查新范围与未读近邻按本轮统一记录核对。



[[wiki/optimization/Overview|返回模块地图]]。
