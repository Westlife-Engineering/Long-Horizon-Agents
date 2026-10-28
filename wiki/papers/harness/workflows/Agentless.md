---
type: paper
primary_direction: harness/workflows
related_directions:
  - harness/verification
source_id: S072
created: 2026-10-28
updated: 2026-10-28
reading_status: selected-body-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/workflows/Agentless.pdf]]"
---

# Agentless：固定定位、修复与验证流程也能完成仓库修复

Agentless 的“less”不表示没有模型或外部运行机制：它把流程顺序固定，让模型在各阶段做局部判断，避免自由决定下一项工具操作。v2包含定位、补丁生成、补丁验证三个阶段，不宜沿用早期两阶段摘要。[[raw/papers/harness/workflows/Agentless.pdf#page=6|§3 · pp.6–9]]

## 身份与实际读取

- 来源 S072；标题 *Agentless: Demystifying LLM-based Software Engineering Agents*；作者 Chunqiu Steven Xia、Yinlin Deng、Soren Dunn、Lingming Zhang。
- 版本 arXiv:2407.01489v2，2024-10-29；[身份页](https://arxiv.org/abs/2407.01489v2)；[原始PDF](https://arxiv.org/pdf/2407.01489v2)，访问日2026-10-28。原下载名 `2407.01489v2.pdf` 原样归档为 [[raw/papers/harness/workflows/Agentless.pdf|Agentless.pdf]]，25页，正文PDF页码与页脚一致。
- SHA-256：`1675c2dcd5ecaef47e8a4356062f60be642cee82e1bbacb044c9d047dce4c856`。
- 实读 pp.6–15：§3方法、§4设置、§5实验及消融、§6.1描述质量部分；查看原页p.12 Table2与测试质量说明、p.14 Table4及Figs.6–7。前部背景仅定位，p.15其余分类及后文未完整核读；未审代码/复现。S001进入点：[[raw/surveys/Towards Long-Horizon Agents.pdf#page=58|§6.1.3 · p.58 · [703]]]。

## 机制与环境条件

先用仓库树和embedding找可疑文件，再用类/函数骨架缩小相关元素，最后找具体编辑位置；对四组位置分别采样补丁，避免把所有候选位置合并成过长上下文。修复输出search/replace小差异。原代码、可执行测试和可独立应用的补丁让候选试验较易组织与复查，但权限仅覆盖评测仓库中的执行，不证明生产系统可以任意回滚。[[raw/papers/harness/workflows/Agentless.pdf#page=6|§3.1–3.2 · pp.6–8]]

验证有三个不同职责：模型生成“测什么”，流程执行测试，规则依据结果筛选候选。系统在原仓库运行复现测试，保留能报告原问题的候选并以归一化多数票选择；回归测试先在原仓库确认通过，再由模型排除可能随需求改变的旧测试。补丁先按回归失败最少筛选，再看复现测试是否报解决；如果没有补丁通过复现测试，退回仅用回归结果。**本库推断：**这降低了某些坏测试造成的误拒，但不能保证所选检查覆盖真实需求。[[raw/papers/harness/workflows/Agentless.pdf#page=8|§3.3 · pp.8–9]]

## 证据：为何不能把测试执行当成可信验证

实验用 GPT-4o `gpt-4o-2024-05-13`，SWE-bench Lite 300题，每题四组位置×10补丁，并生成40个复现测试候选；最终单补丁Resolved 96/300（32%），平均推理成本0.70美元。比较表主要引用外部结果，模型、预算和实现不同，不能据此声称“固定流程因果优于自主agent”。[[raw/papers/harness/workflows/Agentless.pdf#page=9|§4–5.1 · pp.9–11 · Table1]]

| 固定候选上的选择方式 | 解决数/300 |
| --- | --- |
| 多数票 | 77 |
| 再加回归测试 | 81 |
| 再加生成复现测试 | 96 |

这支持测试筛选有增益，但同时增加测试生成成本。[[raw/papers/harness/workflows/Agentless.pdf#page=14|§5.2.3 · Table4 · p.14]]

**关键反证：**213个所选测试能在原代码输出“问题复现”，只有94个在应用开发者真实修复后输出“问题解决”；真实补丁只用于这项事后评估，未用于实际选择。测试能运行、能触发原错误与能正确判断修复是三件事。作者将部分失败解释为issue信息不足；不能据这项统计单独确定每个测试为何错误。[[raw/papers/harness/workflows/Agentless.pdf#page=11|§5.1.3 · pp.11–12]]

## 剩余瓶颈如何归因

候选中存在正确解仍可能选错：Fig.6全候选可解126题，最终选出96题。它说明当前选择存在余量，不能推出任何特定新选择方法必然有效。骨架比完整文件在定位上表现更好，提示上下文组织与模型利用能力耦合；其原因“长上下文使模型困惑”属于作者解释。[[raw/papers/harness/workflows/Agentless.pdf#page=12|§5.2.1 · Table2 · pp.12–13]] [[raw/papers/harness/workflows/Agentless.pdf#page=14|§5.2.2 · Fig.6 · p.14]]

作者人工检查认为10%题目描述信息不足，包含未指明的命名/错误字符串或多种合法解释。这里部分失败来自任务规格与评测环境，不能全算模型能力不足。[[raw/papers/harness/workflows/Agentless.pdf#page=15|§6.1 · Fig.8a · p.15]]

## 整合状态

已整合至 [[wiki/applications/success-mechanisms|应用成功机制与瓶颈]]；与 [[wiki/papers/harness/tools/SWE-agent|S071 SWE-agent]] 作机制对照；过程见 [[组会/2026-10-28-Application/过程/A-软件与GUI|软件与GUI核读]]。未修改共享页，未实测Obsidian。
