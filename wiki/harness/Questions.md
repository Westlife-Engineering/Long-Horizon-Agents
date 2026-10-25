---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/harness/memory/TRACE.pdf]]"
  - "[[raw/papers/harness/verification/SpecRover.pdf]]"
  - "[[raw/papers/harness/orchestration/BRIDGE.pdf]]"
  - "[[raw/papers/harness/memory/HiAgent.pdf]]"
  - "[[raw/papers/harness/hooks/AGrail.pdf]]"
  - "[[raw/papers/harness/hooks/AgentSpec.pdf]]"
  - "[[raw/papers/harness/hooks/InfrastructureSentinel.pdf]]"
---

# Harness：第一轮问题与关闭依据

## 第一轮Brainstorm结案


2026-10-25，两轮讨论及定向补读后结案。**本轮没有新颖性已确认的研究候选；优先亲读 H-B，H-F 只有取得连续产物证据后才进入第二梯队。** 排序依据是现象能否定位、下一条区分证据是否明确，不是角色投票。六个机制方向的宽泛构思已对照现有工作检查；下面保留问题状态，避免以后重复提出已覆盖的机制。

这两张卡的起点不同：H-B 已有可定位实例，缺的是实例解释与责任归因；H-F 连目标现象的连续证据仍待取得。因此前者可以立即帮助理解论文，后者不能仅凭逻辑上可能发生便升级为研究课题。以下“下一条证据”是重新开启调查的门槛，不是自动执行的新一轮计划。

### H-B：准入正确后，约束为什么仍未被使用

**状态与范围：本库材料缺口，优先亲读；关闭“检测过期记忆”的宽泛创新主张。** 先限于 TRACE 返回问答中可见的新旧状态、返回视图与回答，不外推到外部工具执行。最近已读工作就是 [[wiki/papers/harness/memory/TRACE|TRACE]]：它已经处理显式及隐式失效、来源与权限门控、预算内义务覆盖；“准入正确后仍可能用错”也已被作者直接观察，不能重新包装成首次发现。[[raw/papers/harness/memory/TRACE.pdf#page=4|S066 Fig.2、§3 · pp.4–5]]

**引出问题的原证据。** Appendix C.8 的第一例让旧偏好在更新已出现后继续生效，属于失效识别错误；第二例已排除旧设备习惯、准入并取回借用设备的新事实，回答却没有把它用于单机绑定许可的购买问题。后一例支持区分“进入上下文”与“实际应用”，但表现是弃答，不是已发生工具误操作。[[raw/papers/harness/memory/TRACE.pdf#page=24|S066 C.8 · p.24]]

**剩余区别与价值（本库推断）。** 这里要查明该例究竟缺证据、未使用已知约束，还是采取了过度保守的回答策略，从而判断改进应落在准入还是回答端；不再设计一个相同的记忆层。指标也要逐项核对：STALE 的 VIA 映射为更新应用探针 IPA，而 ManBench-Return 的 VIA 才直接测有效候选准入，不能用统一名称反推失败发生在哪一层。[[raw/papers/harness/memory/TRACE.pdf#page=25|S066 D.1–D.5 · pp.25–27]]

**最强反对。** 弃答可能源于许可问题的解释分歧、缺少其他购买信息或通用推理能力，未必需要新记忆结构；单例也不说明这种错误的总体占比。下一条证据是该例完整 Return View、实际检索结果、问题、回答和评分依据的逐项对应，而非再增加一个检查节点。如果以后扩到工具任务，还须另有动作及终局记录，不能只换任务名称就主张新贡献。

**关闭条件。** 若完整记录显示关键约束未送达，回到准入问题；若现有信息足以支持合理弃答，关闭该例“约束未用”的解释。若同证据、同预算下简单明确提示就解决差异，应关闭复杂准入设计的动机；若已有核读近邻完成同条件诊断，则转为已有理解。暂时拿不到完整记录只表示材料受阻，不证明问题不存在。

### H-F：修复过程中是否真的破坏了其他稳定需求

**状态与范围：本库材料缺口，条件性第二梯队。** 限同一部分达标产物、连续修订、身份和适用版本稳定的需求集合，且产物可回放、判据可独立复核。最近已读 [[wiki/papers/harness/verification/SpecRover|SpecRover]] 已把意图、补丁、复现测试、回归测试和重试接成闭环，故“回归失败后修复”已有覆盖。[[wiki/papers/harness/orchestration/BRIDGE|BRIDGE]] 的局部提交还要求不破坏既有活跃依赖边，不能把“修一处兼顾其他依赖”独自作为新意。[[raw/papers/harness/verification/SpecRover.pdf#page=4|S070 Fig.2、§III.C–D · pp.4–5]] [[raw/papers/harness/orchestration/BRIDGE.pdf#page=13|S067 A.1 · p.13]]

**证据与反对必须一起读。** SpecRover 明确说明新需求可合法改变函数签名，使旧回归测试拒绝正确补丁。因此旧测试由过到不过并不自动证明需求退化；非目标要求也可能因共享依赖被合法替代。其 Table II 仅统计生成过复现测试的 119 个任务，correct 标签与人工语义参照、验收通过之间的确切衔接仍未完全确认，不能充当逐轮稳定需求真值。[[raw/papers/harness/verification/SpecRover.pdf#page=5|S070 §III.D · p.5]] [[raw/papers/harness/verification/SpecRover.pdf#page=7|S070 §V.A–B、Table II · pp.7–8]]

**剩余区别与价值（本库推断）。** 要调查的是“修好目标要求，同时破坏原本满足的非目标要求”的真实转移，再决定有限预算下重查什么。整题仍失败、首次补丁漏修、测试过拟合都不能证明这个过程；作者未报告逐轮需求向量，也不等于领域没有相关研究。最强反对是中间退化可能是完成最终修复所必需，逐轮单调并非正确目标；还须排除裁判口径漂移。

**下一条证据与关闭条件。** 先找现存连续产物对，逐项登记需求版本、修订目标与独立判定，确认目标 0→1、非目标 1→0，并观察后续是否恢复。只有现象成立，才值得调查同预算的全量新鲜复核与按改动影响复核；本轮不启动实验。若所有实例均由需求变更、旧测试过时、误判或必要中间状态解释，关闭该现象解释；若已核读近邻测过同样转移及验证分配，关闭创新主张。仅未找到记录则暂缓。

### 其他候选的关闭与暂缓记录

| 稳定问题 | 本轮状态与决定性边界 | 何时才值得重开 |
| --- | --- | --- |
| H-A：初始假完成经压缩固化 | 低优先级暂缓。HiAgent 摘要会再评价完成，并能取回失败子目标轨迹；TRACE 的后来失效不补足初始误判链。[[raw/papers/harness/memory/HiAgent.pdf#page=4\|S007 §3.3–3.4 · PDF p.4／印刷32782]] | 找到同一实例的错误完成声明、摘要、真实反证、取回时点和后续失败；若摘要已纠错或反证已取回，关闭“隐藏反证”解释。 |
| H-C：清单 A→B→A 干扰 | 暂缓。AGrail 会共享及覆写动作清单，但仍传入当前规则、请求和环境，并能补缺项；不能写成盲用旧授权。[[raw/papers/harness/hooks/AGrail.pdf#page=14\|S026 B.1、Algorithms1–3 · PDF pp.14–15／印刷8117–8118]] | 需要检索、删改、重建、漏检的版本链，排除当前规则本来就被误解；没有这条链不设计分区记忆。 |
| H-D：代码批执行检查边界 | 宽泛构思关闭，接口实现未核。AgentSpec 已使用 CodeAct；Sentinel 已要求执行前重查状态。[[raw/papers/harness/hooks/AgentSpec.pdf#page=6\|S023 §5.1 · p.6]] [[raw/papers/harness/hooks/InfrastructureSentinel.pdf#page=4\|S025 §4.4 · p.4]] | 只在具体 wrapper／服务端映射显示未覆盖边界后重开；未核实现不能宣称有绕过漏洞。 |
| H-E：交接修复与终局失败归因 | 宽泛交接诊断、成对修复已有 BRIDGE 覆盖。Table13 有局部通过而终局失败例，作者归因为后续独立步骤。[[raw/papers/harness/orchestration/BRIDGE.pdf#page=4\|S067 §3 · pp.4–6]] [[raw/papers/harness/orchestration/BRIDGE.pdf#page=18\|Appendix E、Table13 · p.18]] | 完整合同、消费边依据及失败后缀仍可核查；若后缀证实错误独立，就不能据此要求更强交接机制。不另开第三张问题卡。 |

亲读先走 TRACE p.24→pp.4–5→pp.25–27，辨别现象、机制与指标；条件允许再读 SpecRover pp.4–5→pp.7–8，对照 BRIDGE p.13。EvoClaw 仍为未读受阻线索，REAgent 未完整摄入，均不承担覆盖证据。两轮讨论到此停止；材料阅读不等于实现审计或复现，内容与结构已核对，Obsidian 应用未测。



[[wiki/harness/Overview|返回模块地图]]。
