---
type: paper
primary_direction: harness/verification
related_directions:
  - harness/memory
source_id: S031
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/verification/Self-MAP.pdf]]"
---

# On the Multi-turn Instruction Following for Conversational Web Agents

## 多轮指令依赖历史，但历史并非全部都有用

**原文问题：**用户说“订两张”“用这个邮箱”时，当前短句依赖前几轮实体、动作和网页状态。单轮任务的完整指令不再够用；把所有HTML与历史塞进上下文又会带入噪声。MT-Mind2Web因此把Mind2Web已有专家行动序列重组、拆分并改写成对话，共720个会话、3525组指令/行动序列，平均约5轮。它是构造的离线对话数据，不是自然线上用户会话记录。[[raw/papers/harness/verification/Self-MAP.pdf#page=3|§3、Fig.2 · PDF pp.3–4 / 印刷8797–8798]]

**机制身份：**Self-MAP是记忆增强规划与监督训练方法。其reflection主要为历史动作补充解释，而非识别失败轨迹后在线重试。原文明确说明静态评测限制使其不收集错误轨迹进行反思。[[raw/papers/harness/verification/Self-MAP.pdf#page=5|§4.2 · PDF p.5 / 印刷8799]]

```mermaid
flowchart LR
    H[历史指令与行动及HTML] -->|语义加轨迹相似度| R[检索相关记忆]
    R -->|删除无关DOM| S[简化环境片段]
    S -->|解释已给定历史动作| E[补充rationale]
    E -->|与当前指令和候选元素拼接| P[微调规划模型]
    P -->|预测| A[下一元素和操作]
```

本库重绘，表示输入处理到动作预测的信息流，不表示在线错误检测反馈。[[raw/papers/harness/verification/Self-MAP.pdf#page=5|§4、Fig.3 · PDF pp.5–6 / 印刷8799–8800]]

## 检索、简化、解释分别改变什么

- **Multifaceted matching：**把当前用户指令和已执行动作作为检索查询，使用ada-002 embedding与余弦相似度，避免只按一句话语义匹配整段历史。实验选K=3。[[raw/papers/harness/verification/Self-MAP.pdf#page=5|§4.1 · PDF p.5 / 印刷8799]] [[raw/papers/harness/verification/Self-MAP.pdf#page=12|Appendix A.2 · PDF p.12 / 印刷8806]]
- **Memory simplification：**用DeBERTa排序DOM候选，缩减历史HTML，也缩减当前网页候选。这里改变可用证据和上下文占用，候选漏检也会限制动作生成。[[raw/papers/harness/verification/Self-MAP.pdf#page=5|§4.2 · PDF p.5 / 印刷8799]]
- **Memory refinement：**gpt-3.5-turbo-1106依据历史HTML、指令与给定动作生成rationale；附录仅抽取positive element对应HTML，缺失正例时用固定解释。它使用标注/已给定历史行动的信息来解释，不是模型独立证明当前待执行动作正确。[[raw/papers/harness/verification/Self-MAP.pdf#page=12|Appendix A.2 · PDF p.12 / 印刷8806]] [[raw/papers/harness/verification/Self-MAP.pdf#page=16|Table 9 · PDF p.16 / 印刷8810]]
- **Planning：**把处理后的记忆、当前指令、当前历史与候选元素输入Flan-T5 base/large，监督微调预测element与operation。生成式和多选式输出是不同接口；本文结果包含参数训练，不能归因于免训练harness。[[raw/papers/harness/verification/Self-MAP.pdf#page=6|§4.3、§5.1 · PDF p.6 / 印刷8800]]

## 成绩是静态下一步/一轮预测，不是整段会话闭环成功

600个训练会话，测试分cross-task 34、cross-website 42、cross-subdomain 44个会话。正文的SSR要求当前步骤元素和操作同时正确，TSR要求一轮用户指令内所有步骤成功；采用先按task再总体的macro平均。**TSR的T是Turn，不是整个对话Task。**[[raw/papers/harness/verification/Self-MAP.pdf#page=4|Table 1、§3.2 · PDF p.4 / 印刷8798]] [[raw/papers/harness/verification/Self-MAP.pdf#page=6|§5.1 · PDF p.6 / 印刷8800]]

Flan-T5base 的三个测试分组中，Self-MAP TSR分别24.7/18.2/20.8；Table 3去掉简化后降到20.7/16.6/15.9，支持在本设置中清理上下文的重要性。refinement不是每一项指标都提升，例如cross-website元素准确率去掉refinement后略高；Flan-T5large也不是所有SSR格都优于基线。因而结论应落在具体组件、split和主指标上。[[raw/papers/harness/verification/Self-MAP.pdf#page=6|Table 2 · PDF p.6 / 印刷8800]] [[raw/papers/harness/verification/Self-MAP.pdf#page=7|Table 3 · PDF p.7 / 印刷8801]]

增加检索数量并不单调提升，Fig.4在K较大时出现下降；作者将其解释为引入无关会话信息。该实验不证明K=3是其他任务的通用最优值。[[raw/papers/harness/verification/Self-MAP.pdf#page=7|§5.4、Fig.4 · PDF pp.7–8 / 印刷8801–8802]]

作者明确只评估HTML快照，无法据此评估动态交互；未证明错误行动改变网页后的恢复，也未测试多模态视觉导航。Table 4在单A5000上报告的是预测下一动作运行时间，不能外推完整线上会话总延迟。[[raw/papers/harness/verification/Self-MAP.pdf#page=9|Table 4、Limitation · PDF p.9 / 印刷8803]]

## 与记忆和验证主题的联系

**本库推断：**它补充的是“遵循对象跨用户轮次变化”的评测需求：当前指令可能省略、指代或切换任务，应追踪相关历史而非默认所有旧约束永久有效。方法的主要落点应同时连到 [[wiki/harness/memory|上下文与记忆]]；放在验证选读队列不等于它就是独立verifier。

与已读 [[wiki/papers/harness/memory/HiAgent|HiAgent]] 的子目标工作记忆、[[wiki/papers/harness/memory/A-MEM|A-MEM]] 的长期笔记演化可比较被保存对象，但环境、训练与指标不同。本文对Synapse/MINDACT的相关工作描述仍是原文转述，未把未核读原作计为直接来源。后续若讨论在线多轮指令恢复，需要另有动态环境、预测历史而非标注历史和会话全程成功的证据；当前属于材料缺口，未宣称新颖研究缺口。

## 来源身份与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S031 |
| 作者 | Yang Deng、Xuan Zhang、Wenxuan Zhang、Yifei Yuan、See-Kiong Ng、Tat-Seng Chua |
| 版本 | ACL 2024 Long Papers正式版，印刷pp.8795–8812 |
| 标识符 | ACL:2024.acl-long.477；DOI:10.18653/v1/2024.acl-long.477 |
| 原始入口 | [发布页](https://aclanthology.org/2024.acl-long.477/)；[本次 PDF](https://aclanthology.org/2024.acl-long.477.pdf) |
| 原件 | [[raw/papers/harness/verification/Self-MAP.pdf\|Self-MAP.pdf · 18 页]] |
| SHA-256 | `ED109A774E62ACB8C37700CBD6E8DF6EC0DE48937B0043407B532CD1E2B85B91` |
| 获取与阅读日期 | 2026-10-25；下载原字节以不覆盖方式归档，身份按该 PDF 首页核对 |
| S001 追索 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=35\|§4.6.1 · PDF pp.35 · 引文 118]]；参考文献 PDF pp.85 |

核读正文PDF pp.1–9（印刷8795–8803），附录A.2/B/C说明pp.12–16（印刷8806–8810）；查看p.5 Fig.3、p.6 Table 2、p.7 Table 3/Fig.4、p.12配置图像。附录末尾完整案例表pp.17–18未逐项核对，未复现训练与在线网站操作。正文引用同时保留PDF及印刷页定位。

**主题整合：**已整合至 [[wiki/harness/verification|Harness · 验证]]，内容与结构已验收。同时在 [[wiki/harness/memory|上下文与记忆]] 建立短桥。尚未复现实验；按本轮要求不进行ComputerUse，Obsidian公式、表格、折叠、来源跳转及宽窄窗口均未实测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/verification|harness/verification]] · [[wiki/harness/memory|harness/memory]]。
