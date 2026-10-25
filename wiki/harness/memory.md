---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/harness/memory/HiAgent.pdf]]"
  - "[[raw/papers/harness/memory/MemGPT.pdf]]"
  - "[[raw/papers/harness/memory/A-MEM.pdf]]"
  - "[[raw/papers/harness/memory/ExpeL.pdf]]"
  - "[[raw/papers/harness/memory/ReSum.pdf]]"
  - "[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf]]"
  - "[[raw/papers/harness/verification/Self-MAP.pdf]]"
  - "[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf]]"
  - "[[raw/papers/harness/memory/TRACE.pdf]]"
---

# 上下文与记忆


当前上下文是这次调用实际可见的状态，持久记忆是能够跨越当前窗口、任务或会话存续的信息。综述用“丢弃、压缩、选择”描述工作上下文的维护，用“写入、维护、检索”描述持久记忆操作。二者区别在存续范围与运行时角色，而不只在文件是否落盘。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=23|S001 · §4.2 · Fig.8 · p.23]]

细分导航：Working Context（§4.2.1）；Persistent Memory（§4.2.2）。与 [[wiki/foundations/Formalization#H1–H3 与 C1–C3|C2/C3]] 相关。第一轮 S007–S011 已完成摄入与主题整合，下面是原论文支持的机制比较；内容与结构已验收，Obsidian 应用未测。

### 先区分保存的对象，再问怎样取回

“有记忆”不足以说明后续行为怎样改变。下面沿两个问题比较：**保存的是执行细节、组织后的信息还是经验规则；这些内容怎样重新进入当前决策。** 这是本库依据原文组织的比较轴，不是论文间的性能排名。

| 保存对象与更新边界 | 重新进入决策的方式 | 可回查的原文 |
| --- | --- | --- |
| 当前子目标保留完整行动—观察；完成的子目标改为摘要 | 摘要维持可见进度，需要细节时取回旧轨迹；压缩不等于删除原轨迹 | [[wiki/papers/harness/memory/HiAgent\|HiAgent]]；[[raw/papers/harness/memory/HiAgent.pdf#page=3\|S007 §3 · PDF pp.3–4 / 印刷 pp.32781–32782]] |
| 超出窗口的消息留在 Recall，其他内容可写入 Archival；主上下文单独维护 | 模型经函数读写，队列管理器自动淘汰；heartbeat 可把多步检索连起来 | [[wiki/papers/harness/memory/MemGPT\|MemGPT]]；[[raw/papers/harness/memory/MemGPT.pdf#page=2\|S008 §2 · pp.2–4]] |
| 交互成为带关键词、标签、描述和链接的 notes；新 note 可更新旧 note 组织 | 生成的元信息参与向量检索，关联内容再交给回答模型 | [[wiki/papers/harness/memory/A-MEM\|A-MEM]]；[[raw/papers/harness/memory/A-MEM.pdf#page=3\|S009 Figure 2、§3 · pp.3–5]] |
| 训练任务成败轨迹提炼成可修改的经验规则，成功轨迹另存 | 规则直接加入提示，相似成功轨迹作为示例；无参数更新仍有经验收集阶段 | [[wiki/papers/harness/memory/ExpeL\|ExpeL]]；[[raw/papers/harness/memory/ExpeL.pdf#page=3\|S010 §4、Figure 1 · pp.3–6]] |
| 接近窗口上限时，把搜索历史压成相关证据摘要 | 以“原问题＋摘要”重置上下文并继续搜索；本文用系统阈值触发 | [[wiki/papers/harness/memory/ReSum\|ReSum]]；[[raw/papers/harness/memory/ReSum.pdf#page=3\|S011 §3.1 · p.3]]、[[raw/papers/harness/memory/ReSum.pdf#page=13\|Algorithm 1 · p.13]] |

这组对照澄清了两种容易混淆的扩展：HiAgent / ReSum 主要让**同一任务继续执行**；ExpeL 主要让**不同任务之间复用经验**。MemGPT / A-MEM 提供可跨当前窗口存续的信息与取回机制，其主实验则偏向对话、文档或合成检索。存续范围、操作方式与实际评测任务需要分别登记，不能用“长期记忆”一个词替代三者。[[raw/papers/harness/memory/HiAgent.pdf#page=4|S007 §4.1 · PDF p.4 / 印刷 p.32782]] [[raw/papers/harness/memory/ExpeL.pdf#page=7|S010 §5 · pp.7–9]] [[raw/papers/harness/memory/MemGPT.pdf#page=5|S008 §3 · pp.5–8]] [[raw/papers/harness/memory/A-MEM.pdf#page=5|S009 §4.1 · pp.5–7]]

**补充诊断证据（S036 已完成摄入，应用未测）：**[[wiki/papers/optimization/architecture/Lost-in-the-Middle|Lost in the Middle]] 的开放域 QA 实验中，增加文档后检索召回仍增长，reader 准确率却较早饱和；把 query 同时放在数据前后，明显改善合成 KV 检索，却没有同样消除语义 QA 的位置趋势。因此本库需分别问“是否取回”“如何编排”和“是否被模型使用”；这不是对上述五种记忆方法的直接反证，也不证明重排能够普遍修复 Agent。对应 [[wiki/optimization/architecture|架构基础]] 的有效上下文边界。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=8|S036 §4.2、Fig.9 · p.8]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=9|§5、Fig.11 · pp.9–10]]

**跨用户轮次的记忆补充（S031，已完成摄入）：**[[wiki/papers/harness/verification/Self-MAP|Self-MAP]] 按当前指令与动作检索历史，缩减无关DOM，再为已给定历史动作生成rationale，供微调后的规划模型预测下一步。这里的reflection是在加工记忆解释，并非运行时发现错误后重试；positive element与历史动作的信息权限、静态HTML快照和Turn Success Rate边界见 [[wiki/harness/verification#检查对象决定成功指标|验证对象]]。它补充了省略、指代和任务切换下的记忆使用，不能由“保留旧历史”推断所有旧约束始终有效。[[raw/papers/harness/verification/Self-MAP.pdf#page=5|§4 · PDF pp.5–6 / 印刷8799–8800]] [[raw/papers/harness/verification/Self-MAP.pdf#page=12|Appendix A.2 · PDF p.12 / 印刷8806]]

**学习记忆操作与使用（S055，完成摄入，应用未测）：**[[wiki/papers/optimization/reinforcement-learning/Memory-R1|Memory-R1]]让Manager生成ADD/UPDATE/DELETE/NOOP及内容，再让Answer从60个候选中选择证据回答；二者分阶段RL，训练一方时另一方固定。运行时更新记忆不等于实时更新参数，最终QA reward也不逐条验证存储内容。主要证据为对话问答，LongMemEval采用**oracle版本**；因此不能当作完整大记忆库检索或自主执行的可靠性证据。训练快照与反馈依赖见 [[wiki/optimization/reinforcement-learning#记忆写入和使用也能成为训练接口|Optimization记忆接口]]。[[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=4|§3 · PDF pp.4–5 / 印刷12808–12809]] [[raw/papers/optimization/reinforcement-learning/Memory-R1.pdf#page=14|Appendix B · PDF p.14 / 印刷12818]]

### 来源真实、当前准入与后续使用是三个条件

HiAgent的旧轨迹取回回答“历史细节是否可见”，Self-MAP的历史使用回答“怎样解释当前指令”；团队在执行者缺席期间改变状态以后，还需要判断旧记录现在是否适用。综述外补读[[wiki/papers/harness/memory/TRACE|S066 TRACE]]专门处理这个返回边界：合并离开检查点与缺席更新，应用显式撤销并用模型扫描/核验隐式失效，再逐项检查权限、时效、任务适用性与来源，按预算选择覆盖当前义务的证据。私人经验只有其绑定来源仍在Return View中时才能重新进入上下文。**这已直接覆盖“相关且真实的旧记忆仍可能过期”的机制问题。**已完成摄入，应用未测。[[raw/papers/harness/memory/TRACE.pdf#page=3|S066 §2–3 · pp.3–5]] [[raw/papers/harness/memory/TRACE.pdf#page=19|Appendix C.3–C.4 · p.19]]

| 条件 | 它能说明什么 | 仍不能说明什么 |
| --- | --- | --- |
| 来源可追溯 | 记录绑定哪次观察或确认 | 观察为真、记录仍有效；被取消的订房确认仍有真实来源。[[raw/papers/harness/memory/TRACE.pdf#page=18\|C.1 · p.18]] |
| 当前准入通过 | 在本次身份、任务、状态与义务条件下，记录可进入受控返回视图 | 所有隐式失效都被识别、信息已经被正确使用；scanner/verifier仍会漏检。[[raw/papers/harness/memory/TRACE.pdf#page=18\|C.2–C.4 · pp.18–19]] |
| 后续回答或行动满足要求 | 需要另行观察任务结果 | 不能由签名、来源齐全或局部覆盖直接推出。TRACE有准入正确但回答未采用新约束的失败案例。[[raw/papers/harness/memory/TRACE.pdf#page=24\|C.8 · p.24]] |

TRACE的证据也限定了比较口径：STALE中的VIA映射为把更新用于新问题的IPA问答probe，ManBench-Return中的VIA才直接测候选是否进入视图；后者筛选初始答案正确的episode，Old-Stale还要求多数活跃Agent答对。它不是现实外部操作的完成率。Memora没有一致领先，CUPMem子集比较更准确也更贵；精确预算、分母及准入/使用错误见唯一论文页，不能据统一指标名汇总成通用可靠性。[[raw/papers/harness/memory/TRACE.pdf#page=25|D.1–D.5 · pp.25–27]] [[raw/papers/harness/memory/TRACE.pdf#page=7|Table2 · p.7]] [[raw/papers/harness/memory/TRACE.pdf#page=31|Table7 · p.31]]

### 机制可比较，分数必须留在原条件中

这些来源并不构成同一评测上的五个竞品。HiAgent 使用 GPT-4、五个行动环境、最多 30 步；MemGPT 的召回对照中，普通模型只见历史摘要而系统可搜索完整历史；A-MEM 的主证据是长对话 QA，检索 k 还按模型与题型调整。ExpeL 有训练任务重试和更强模型归纳经验的成本；ReSum 的主要推理比较为固定工具预算下的网页搜索，但默认摘要器本身经过训练。每项提升必须保留这些条件。[[raw/papers/harness/memory/HiAgent.pdf#page=4|S007 §4 · PDF pp.4–5 / 印刷 pp.32782–32783]] [[raw/papers/harness/memory/MemGPT.pdf#page=5|S008 §3.1.1 · p.5]] [[raw/papers/harness/memory/A-MEM.pdf#page=18|S009 Table 8 · p.18]] [[raw/papers/harness/memory/ExpeL.pdf#page=15|S010 Table 4 · p.15]] [[raw/papers/harness/memory/ReSum.pdf#page=4|S011 §3.2、§4.1 · pp.4–5]]

**本库推断：**工作记忆应同时检查“压缩后保留什么”和“丢失后怎样恢复”，持久经验则应检查“生成的解释如何影响以后检索或行动”。HiAgent 的轨迹取回与 MemGPT 的外部历史让恢复通道具体可见；A-MEM 元信息、ExpeL 规则和 ReSum 摘要均包含模型加工后的理解，不能与原始观察自动视为同等可靠。

**待检验问题，尚非已成立研究缺口：**如何区分写入错误、压缩遗漏、检索提前停止和经验规则不适用？如何在匹配探索预算后判断“更好的状态表示”与“更多继续执行机会”的贡献？ReSum 的训练比较正提示这个归因问题：普通 GRPO 训练限 40 次工具调用，ReSum-GRPO 为 60，不能把收益全部归给训练算法的一项变化。详见 [[wiki/optimization/reinforcement-learning|运行状态与策略训练的接口]]。[[raw/papers/harness/memory/ReSum.pdf#page=15|S011 附录 D.2 · p.15]]

## 论文入口与交叉方向

- [[wiki/papers/harness/memory/HiAgent|S007 · HiAgent]]：主归属。
- [[wiki/papers/harness/memory/MemGPT|S008 · MemGPT]]：主归属。
- [[wiki/papers/harness/memory/A-MEM|S009 · A-MEM]]：主归属。
- [[wiki/papers/harness/memory/ExpeL|S010 · ExpeL]]：主归属。
- [[wiki/papers/harness/memory/ReSum|S011 · ReSum]]：主归属。
- [[wiki/papers/harness/tools/Voyager|S015 · Voyager]]：交叉关联；主归属为`harness/tools`。
- [[wiki/papers/harness/verification/Self-MAP|S031 · Self-MAP]]：交叉关联；主归属为`harness/verification`。
- [[wiki/papers/optimization/architecture/Lost-in-the-Middle|S036 · Lost-in-the-Middle]]：交叉关联；主归属为`optimization/architecture`。
- [[wiki/papers/optimization/reinforcement-learning/Memory-R1|S055 · Memory-R1]]：交叉关联；主归属为`optimization/reinforcement-learning`。
- [[wiki/papers/harness/memory/TRACE|S066 · TRACE]]：主归属。

[[wiki/harness/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
