---
type: paper
primary_direction: harness/orchestration
related_directions:
  - harness/verification
source_id: S017
created: 2026-10-25
updated: 2026-10-25
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/orchestration/MetaGPT.pdf]]"
---

# MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework

> [!info] 状态
> 原文核读、主题整合与主 Agent 内容/结构验收已完成；未复现实验，Obsidian 应用未测。

## 来源身份与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S017 |
| 作者 | Sirui Hong、Mingchen Zhuge、Jiaqi Chen 等，完整 15 人名单见 PDF p.1 |
| 锁定版本 | arXiv:2308.00352v7，2024-11-01；PDF 标注 ICLR 2024 |
| 原始发布页 | [MetaGPT](https://arxiv.org/abs/2308.00352) |
| 下载原件 | [原始 PDF](https://arxiv.org/pdf/2308.00352v7)；访问 2026-10-25 |
| Raw | [[raw/papers/harness/orchestration/MetaGPT.pdf\|MetaGPT.pdf，29 页]] |
| SHA-256 | `17582E47647FAC8EAA3681FEADE41C8408310C4133ACC5C6823565FBE880E1AC` |
| 阅读日期与范围 | 2026-10-25；正文 §§1–5（pp.1–9）；附录 A.1（p.15）、B 示例开头（p.17）、C–D（pp.23–25）、E（p.26）；实际查看 p.4 Fig.2、p.9 Table3、p.17 示例和 p.24 表格。未逐项核读 pp.18–22 示例代码、全部参考文献、pp.27–29 全部附加材料。 |
| S001 引用路线 | 引文 219，§4.4.1；§4.4.4，PDF pp.29,30；书目 pp.93 |

本页页码均按所存 PDF 第一页计数；除 GPTSwarm 的会议卷页码外，引用采用 PDF 内页码。下载后验证标题与哈希，以不覆盖方式归档。作者/版本按实际原件登记，不沿用综述的不同署名。

## 为什么要把协作写成标准流程

**原文陈述：**复杂软件任务的跨文件依赖与交接容易受到级联幻觉影响。MetaGPT 把人类软件公司的 SOP 写成角色、工作顺序和中间产物格式，改变的是推理时 harness；主实验不是对基础 LLM 的参数训练。它希望让下一角色接收可用的需求和接口，而不只是一段自由对话。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=1|§1 · pp.1–2]] [[raw/papers/harness/orchestration/MetaGPT.pdf#page=4|§3 · pp.4–6]]

## 谁分工，什么状态传下去

以下是本库按原文重绘的顺序示意；箭头表示产物依赖，不保证产物正确。

```mermaid
flowchart LR
 A[需求] --> B[产品经理：PRD]
 B --> C[架构师：接口与结构]
 C --> D[项目经理：任务分配]
 D --> E[工程师：代码]
 E --> F[执行测试]
 F -->|失败且未超重试上限| E
 F -->|通过| G[后续任务与交付]
```

角色向共享 message pool 发布结构化文档，各角色按 profile 订阅相关消息；依赖满足才触发行动。工程师使用需求、设计、代码与调试历史，并写/执行测试；测试通过或最多三次重试后结束该纠错循环。这里的反馈是局部代码修订，不能直接等同于任意运行阶段的全局重新规划。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=4|§3.1、Fig.2 · pp.4–5]] [[raw/papers/harness/orchestration/MetaGPT.pdf#page=6|§§3.2–3.3 · p.6]]

**本库推断：**SOP 把分工与信息交接约束外化，但结构化文档仍可能保存错误解释；共享池可达也不等于接收者正确使用。附录 B 的 p.17 用户要求画图 app，而紧接 PRD 写成 color meter，显示示例文本本身存在不一致；本库只记录此处张力，不据单页判定实际运行失败率。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=17|Appendix B · p.17]]

## 实验究竟支持什么

| 核读证据 | 可支持的判断及限制 |
| --- | --- |
| HumanEval 164、MBPP 427 题；GPT-4 与可执行反馈 | 作者报告反馈提高 pass@1；pass@1 是最终单候选口径，内部仍可执行和重试，不能读成单次 LLM 调用。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=6\|§§3.3–4.2 · pp.6–8]] |
| SoftwareDev 有 70 项，主要比较选 7 项；可执行性由人评 1–4 分 | 保留代码可执行性、人工修订与 token 成本的区别；“更多代码”“每行更少 token”均不是功能正确性的替代量。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=7\|§4.1 · p.7]] [[raw/papers/harness/orchestration/MetaGPT.pdf#page=23\|Appendix C.1 · p.23]] |
| Table3 角色消融使用两项任务平均 | 增加角色同时增加文档、调用与开销，未隔离“角色数”这一因果变量；不推广为越多 Agent 越好。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=9\|§4.4、Table3 · p.9]] |
| Appendix C 的 GPT-4 HumanEval 提示/解析比较 | 主图引用的 67% 基线不是唯一可比设置；本地 API 实验中代码提取、系统提示改变得分。比较必须保留处理方式。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=24\|Appendix C.2、Table7 · pp.24–25]] |

主表 Table1 可执行性为 3.75，附表 Table4 为 3.9；本次不合并成一个全数据集数字，实验子集/统计口径应进一步对照代码。主文项目独立运行；A.1 描述基于历史总结更新角色约束提示的初步探索，不等于主实验已验证跨任务自我演化。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=8|Table1 · p.8]] [[raw/papers/harness/orchestration/MetaGPT.pdf#page=24|Table4 · p.24]] [[raw/papers/harness/orchestration/MetaGPT.pdf#page=15|Appendix A.1 · p.15]]

## 对编排理解的改变与边界

本篇为固定专业角色＋结构化产物＋订阅依赖提供直接证据。与本批 Magentic-One 的工具能力分工比较时，应比较分工轴与状态责任；不能按不同基准上的分数排名。作者与 ChatDev 的比较属于本文实验和作者解读，本次未独立摄入 ChatDev 原论文。作者还明确 UI/前端、多模态支持与人工中断/checkpoint 能力的限制。[[raw/papers/harness/orchestration/MetaGPT.pdf#page=25|Appendix D.1 · p.25]]

待检验的是“结构化交接中的错误由谁检测、按什么依据退回”，目前属于本库比较问题，尚未查新为研究缺口。

## 主题联系与验收状态

已整合到 [[wiki/harness/orchestration|Harness · 编排]]；涉及反馈检查时联系 [[wiki/harness/verification|验证]]。共享主题与索引已同步，已通过主 Agent 内容/结构验收并完成摄入。关键页码和 Raw 哈希已检查，Obsidian 应用渲染与来源跳转未测。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/orchestration|harness/orchestration]] · [[wiki/harness/verification|harness/verification]]。
