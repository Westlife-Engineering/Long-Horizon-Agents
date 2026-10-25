---
type: paper
source_id: S042
created: 2026-10-25
updated: 2026-10-25
reading_status: targeted-primary-read
ingest_status: complete
sources:
  - "[[raw/papers/DeepSeek-V3.pdf]]"
---

# DeepSeek-V3 Technical Report

**核心判断：**DeepSeek-V3 是架构、数据、目标函数、长上下文适配与后训练的组合报告。它可用来理解能力基础的形成，但整体 benchmark 成绩不能单独证明某种预训练机制改善长程任务。MTP 的“预测未来 token”也不等于已经学会规划未来环境动作。[[raw/papers/DeepSeek-V3.pdf#page=4|§1 · pp.4–6]] [[raw/papers/DeepSeek-V3.pdf#page=10|§2.2 · pp.10–11]]


## 来源身份与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S042 |
| 作者 | DeepSeek-AI；完整贡献作者见 PDF pp.45–46（本次未逐名核验） |
| 版本 | arXiv:2412.19437v2，2025-02-18；S001 引用 2024 年报告条目，未逐版本比较 |
| 原始渠道 | [原始发布页](https://arxiv.org/abs/2412.19437v2)；[固定 PDF](https://arxiv.org/pdf/2412.19437v2)；访问 2026-10-25 |
| 本地原件 | [[raw/papers/DeepSeek-V3.pdf\|DeepSeek-V3.pdf，共 53 页]] |
| SHA-256 | `812A3FD645C80725354DE9D831A6785503007A60681461407F64E97305FA9330` |
| 阅读日期与范围 | 2026-10-25；问题驱动核读 pp.1–11（摘要/目录/引言/架构）、pp.21–35 的 §4–6（数据、扩窗、实验、后训练和局限）；重点看 Fig.3 p.10、Fig.8 p.23、Table4 p.26、Table6 p.31 原页图像；§3 基础设施细节、pp.36–53 的后续展望/参考文献/附录未系统核读 |
| S001 选择依据 | 引文 [110]，§5.3.1，PDF pp.44；参考文献 PDF p.84；正文角色和书目已回读核对 |

本页按本地 PDF 第一页起计页码。网页只用于身份核对，学术主张以已归档 PDF 为依据；未复现实验。原始下载文件为 `.research-tmp/S042-download.pdf`，归档前后字节与哈希一致。主题、索引、互链与摄入日志已同步；主 Agent 已完成内容与结构验收，Raw 哈希匹配。Obsidian 应用未测。


## 训练配方分别改变什么

| 环节 | 实际改变 | 保留的边界 |
| --- | --- | --- |
| MLA 与 MoE | 每个 token 缓存低维 KV 潜变量及解耦位置 key；稀疏激活专家控制计算 | MLA 仍按时间位置保留缓存，不能等同于固定大小的跨历史记忆；本报告借用 V2 架构，V2 原文未在本任务读。[[raw/papers/DeepSeek-V3.pdf#page=7\|§2.1 · pp.7–9]] |
| 负载均衡 | 路由选择加专家偏置，按 batch 过载/欠载调整；gating 权重仍取原 affinity | 正式 V3 仍有很小的序列级辅助损失，不能把“auxiliary-loss-free”译成整模型完全无辅助损失。[[raw/papers/DeepSeek-V3.pdf#page=9\|§2.1.2 · p.9]] |
| MTP | 将前一深度隐藏态和后移一个 token 的 embedding 拼接，串行模块预测更远 token，附加交叉熵 | 训练信号更密、表示可能预先编码未来是作者解释；模块可在推理时丢弃，或另作 speculative decoding。[[raw/papers/DeepSeek-V3.pdf#page=10\|§2.2、Fig.3、Eqs.21–25 · pp.10–11]] |
| 数据与扩窗 | 14.8T tokens，增加数学/代码与多语言；4K 预训练后用 YaRN 做 32K→128K 两阶段 | 数据比例不充分公开；变化包含语料、模型规模、架构与训练，不能用跨代总分拆贡献。[[raw/papers/DeepSeek-V3.pdf#page=21\|§4.1–4.3 · pp.21–23]] |
| 后训练 | 1.5M SFT 实例、R1 专家生成及拒绝采样、规则/模型奖励与 GRPO | 报告的最终聊天模型已接受这些步骤，不能将其代码/数学成绩全归预训练。[[raw/papers/DeepSeek-V3.pdf#page=28\|§5.1–5.2 · pp.28–30]] |

MTP 的因果链在训练 token 序列上成立：额外模块可看到向后移位的真实 token，监督它预测再下一个 token。V3 实配深度 D=1，不是 Fig.3 所示任意多个模块都实际使用。训练时加入未来预测损失，推理时主模型仍可逐 token 生成。[[raw/papers/DeepSeek-V3.pdf#page=11|§2.2 · p.11]] [[raw/papers/DeepSeek-V3.pdf#page=22|§4.2 · p.22]]

## 哪些对照能支持归因

**MTP 有受控但较小规模的消融。**Table4 比较 15.7B/1.33T 与 228.7B/540B 两种 MoE，在相同数据和其他架构下添加一层 MTP，推理均去掉模块。多数指标提高，但不是所有指标；该表不能当作 671B 最终模型或长程 Agent 的单因素对照。[[raw/papers/DeepSeek-V3.pdf#page=26|§4.5.1、Table4 · p.26]]

**负载均衡的作用还涉及约束范围。**§4.5.3 报告 batch-wise auxiliary loss 在 1B/3B 小模型上也达到与 auxiliary-loss-free 相似的 validation loss。因此“取消辅助损失”并非这里唯一可成立的解释；更宽松的 batch 级均衡与专家分化是作者重点讨论的替代机制。正式 V3 的小序列损失与 Table5 全移除辅助损失的消融配置也要分开。[[raw/papers/DeepSeek-V3.pdf#page=27|§4.5.2–4.5.3 · pp.27–28]]

**扩窗不是零训练。**32K 和 128K 阶段各训练 1000 steps，batch 从 1920 降至 480；YaRN 只作用于解耦位置 key。Fig.8 的 NIAH 是 SFT 后结果，不能声称只改 RoPE 就得到同等检索能力。原文 scaling factor 的 t 记法与 YaRN 本地版本不完全一致，本页不把两个公式直接混写。[[raw/papers/DeepSeek-V3.pdf#page=23|§4.3、Fig.8 · p.23]]

**存在工程任务结果，仍受 harness 条件限制。**最终聊天模型 Table6 包括 LongBench v2、FRAMES 和 SWE-Bench Verified；SWE-Bench 使用 Agentless framework，Aider 用 diff 格式，输出上限 8192 tokens。这比单纯短问答更接近工程使用，但没有把预训练单因素与跨上下文长期状态、恢复能力隔离。不要把表中的 resolved 比例改写成“自主长程 Agent 成功率”。[[raw/papers/DeepSeek-V3.pdf#page=30|§5.3.1、Table6 · pp.30–32]]

## 局限与对本库的影响

本库推断：预训练可提供结构化推理基础，但应把“基础模型评测→后训练评测→特定 harness 的工程评测”作为不同证据层。R1 蒸馏的消融实际在 V2.5 上，且伴随响应变长，不能复制成 V3 的同预算因果证明。[[raw/papers/DeepSeek-V3.pdf#page=34|§5.4.1、Table9 · p.34]]

作者承认部署单元较大，限制小团队使用。成本表仅计算正式训练，排除了前期研究和消融；本库不把约 $5.576M 当完整研发预算或当前价格。[[raw/papers/DeepSeek-V3.pdf#page=5|Table1、§1 · p.5]] [[raw/papers/DeepSeek-V3.pdf#page=35|§6 · p.35]]

下一条有价值的证据是固定基础模型、数据/训练预算与 Agent harness 的分阶段对照；本轮尚未据此宣称研究缺口。

## 本库落点与下一条证据

已整合到 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]，主题与本页双向关联。相关方法的比较以本文实际实验为限，未核读的引用不成为独立来源。返回 [[wiki/index|索引]]。
