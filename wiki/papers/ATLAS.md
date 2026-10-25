---
type: paper
source_id: S048
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/ATLAS.pdf]]"
---

# ATLAS: Agent Tuning via Learning Critical Steps

## 来源与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S048 |
| 作者 | Zhixun Chen、Ming Li、Yuxuan Huang、Yali Du、Meng Fang、Tianyi Zhou |
| 版本 | Findings of ACL 2025 正式版，pp.25334–25349；DOI 10.18653/v1/2025.findings-acl.1299 |
| 原始入口 | [ACL Anthology](https://aclanthology.org/2025.findings-acl.1299/)；访问2026-10-25 |
| Raw | [[raw/papers/ATLAS.pdf\|本地PDF，共16页]] |
| SHA-256 | `0084960ac81c108054d44fc11ed84beb02d4be086fcb04f99464aa3a374290bf` |
| 实际阅读 | 2026-10-25；正文/局限pp.1–9，附录p.14环境尾段、B与D.1 pp.14–15；p.16追加结果选读。已看Fig.3 p.3、目标/选择p.4、Table1 p.6、Tables2–4 p.7。附录A pp.12–13全部环境细节及p.16逐格结果未完整核读，参考文献未逐条核验。 |
| 综述定位 | S001引文81，§5.4.1，PDF p.45；书目p.82 |

以下为直接原文证据与本库分析，未复现实验。印刷页码 = PDF页码 + 25333。

## 它选择的是监督位置，完整历史仍然输入

完整专家轨迹可能含学生已经会做的动作、可替换顺序和专家风格。ATLAS 用选择器识别其中值得学习的步骤，只在这些步骤计算思考和动作的 teacher-forcing 损失。**未被选中的历史仍在输入里**，所以该方法不等于删除70%的上下文，也不等于只需30%的总训练算力。[[raw/papers/ATLAS.pdf#page=3|§3、Fig.3 · PDF pp.3–4 / 印刷 pp.25336–25337]]

| 组件 | 操作 | 信息与监督边界 |
| --- | --- | --- |
| 专家数据 | 使用已有 AgentTraj-L 多环境轨迹 | 训练状态仍来自离线专家，不是在线学生rollout |
| GPT-4o selector | 先归纳轨迹计划/子目标，再选择至多30%步骤并说明类别 | 四类为计划、关键观察、关键动作、自我纠正；这是语义判别，非逐步因果贡献的真值 |
| 学生微调 | 完整轨迹输入，仅选中步骤的thought/action计损失 | 不直接拟合其余步骤，但仍依赖其提供上下文 |

依据：[[raw/papers/ATLAS.pdf#page=4|§3.2–3.3 · PDF p.4 / 印刷 p.25337]]、[[raw/papers/ATLAS.pdf#page=5|§4.2 · PDF p.5 / 印刷 p.25338]]、[[raw/papers/ATLAS.pdf#page=15|Appendix D.1 · PDF p.15 / 印刷 p.25348]]。本库分析：选择的确改变参数更新的监督分布，但没有直接扩展学生失败状态覆盖；“减轻专家偏差”是经验解释，不能写成解决 covariate shift 的保证。

## 证据：少量关键监督有用，但泛化优势须分项看

主模型为 Llama-3.1-8B-Instruct，10个 held-in 环境、4个 held-out 环境；对照包括同骨干完整轨迹SFT、等比例随机/非关键步骤、perplexity选择。Adam、学习率2e-5、3 epochs、batch128、max length8192、4张A100-80GB；作者报告 ATLAS训练约8小时，但本次所读材料没有完整轨迹同配置耗时及selector总成本的完整对照。[[raw/papers/ATLAS.pdf#page=5|§4.1–4.3 · PDF p.5 / 印刷 p.25338]]、[[raw/papers/ATLAS.pdf#page=14|Appendix B.1 · PDF p.14 / 印刷 p.25347]]

主表 held-in 平均60.52→65.91、held-out平均36.18→38.36；这些混合任务reward/成功口径，不能称统一完整任务成功率。Academic反而75→70，不能声称每个新环境都提升。30%随机步骤的held-out平均38.04，距离关键选择38.36仅0.32；没有对应置信区间，不能把该小差值写成稳健显著优势。held-in上65.91对随机59.90的差距较大。[[raw/papers/ATLAS.pdf#page=6|Table1 · PDF p.6 / 印刷 p.25339]]、[[raw/papers/ATLAS.pdf#page=7|Tables2–3 · PDF p.7 / 印刷 p.25340]]

作者在BabyAI/Weather用每步5次rollout估计value作选择对照，所得任务结果与语义选择接近；但这只覆盖两种可复现起点的环境，作者承认有限rollout估值不准、长轨迹成本高、部分环境reset随机目标而无法做。它没有证明GPT选择等于真实因果关键步骤。另一项100任务子集实验从关键步骤后接续且可反复重新初始化，观察到较高结果；这含“给定正确中间状态”的帮助，不能直接代表部署时学生会自主完成这些步骤。[[raw/papers/ATLAS.pdf#page=7|§4.5.4、Table4 · PDF p.7 / 印刷 p.25340]]、[[raw/papers/ATLAS.pdf#page=8|§4.6、Table6 · PDF p.8 / 印刷 p.25341]]、[[raw/papers/ATLAS.pdf#page=15|Appendix B.3 · PDF p.15 / 印刷 p.25348]]

## 适用条件和长程边界

关键步骤识别依赖强选择器、完整专家历史与任务语义；GPT-4o选择优于所测Llama-3.1-70B选择，论文承认闭源模型和语义判断局限。其“30%”是设定上限，作者尝试更大上限却只得到少量额外选中步骤，并未测试所有更高比例。[[raw/papers/ATLAS.pdf#page=6|§4.5.2 · PDF p.6 / 印刷 p.25339]]、[[raw/papers/ATLAS.pdf#page=7|§4.5.5 · PDF pp.7–8 / 印刷 pp.25340–25341]]、[[raw/papers/ATLAS.pdf#page=9|§7 Limitation · PDF p.9 / 印刷 p.25342]]

任务有多步依赖，但原本50–300步的Jericho任务被改为15步内子任务；不能把该held-out结果描述为已解决原始数百步游戏。表中的通用性主要指跨环境任务表现，未像AgentTuning那样给出MMLU/HumanEval等通用语言能力保留检验。[[raw/papers/ATLAS.pdf#page=14|Appendix A · PDF p.14 / 印刷 p.25347]]、[[raw/papers/ATLAS.pdf#page=6|Table1 · PDF p.6 / 印刷 p.25339]]

本库待检验问题：语义上看似关键的步骤，对当前学生究竟有多难、能否替换、是否确实控制成功？本文已有value对照，故不能把“验证关键步骤”直接包装为新研究方向；尚需限定新任务、等预算和可重放条件后再查新。

## 主题联系与验收

已整合至 [[wiki/optimization/Overview#微调|微调]]。与已核读的 [[wiki/papers/AgentTuning|AgentTuning]] 相比，主要变化是损失位置而非通用数据混合；与 [[wiki/papers/AgentGym-RL|AgentGym-RL]] 的在线课程相比，它没有通过训练交互重新采样状态。AgentTraj-L/AgentGym等原始数据论文未因本文引用而自动计已读，也不与AgentGym-RL混为一篇。

主题、索引、队列、互链与摄入日志已同步；主 Agent 内容与结构验收通过，Raw哈希匹配。Obsidian应用未测，未复现实验。
