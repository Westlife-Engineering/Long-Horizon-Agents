---
type: paper
primary_direction: optimization/finetuning
related_directions:
  - optimization/data-environments
source_id: S073
created: 2026-10-28
updated: 2026-10-28
reading_status: selected-body-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/finetuning/UI-TARS.pdf]]"
---

# UI-TARS：把截图、动作与出错后恢复训练到同一模型

UI-TARS以截图输入、坐标与键鼠动作输出运行GUI任务。主要改变训练数据、监督与偏好优化，不是只换一套提示词；“native model”也仍需采集观察、执行动作与管理上下文的外部循环。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=14|§4.1 · pp.14–15]]

## 身份与实际读取

- 来源 S073；标题 *UI-TARS: Pioneering Automated GUI Interaction with Native Agents*；作者 Yujia Qin、Yining Ye、Junjie Fang等35人，完整名单见原文及身份页。
- 版本 arXiv:2501.12326v1，2025-01-21；[身份页](https://arxiv.org/abs/2501.12326v1)；[原始PDF](https://arxiv.org/pdf/2501.12326v1)，访问日2026-10-28。原下载名 `2501.12326v1.pdf` 原样归档为 [[raw/papers/optimization/finetuning/UI-TARS.pdf|UI-TARS.pdf]]，44页，PDF与正文页码一致。
- SHA-256：`999d01bdd86eb39df1c322d7ab2a48f9f10d8f8a6cb2af913591612712b3964e`。
- 实读 pp.14–27（§4方法、§5评估及§6开头），主要核查在线结果与训练机制；查看原页p.21纠错/恢复配对、p.26 Table9、p.27 Fig.8。导言部分定位，完整背景、附录案例和数据示例未读；未审代码或复现。S001进入点：[[raw/surveys/Towards Long-Horizon Agents.pdf#page=60|§6.3.2 · p.60 · [494]]]。

## 环境和机制

运行输入是当前截图、最近N张观察和全部动作/思考历史，实验N=5。截图可跨应用统一获取，动作返回后可以重新观察，但屏幕只暴露部分状态；画面变化也可能来自动画或后台刷新。训练特意加入相邻截图变化描述及非交互变化，帮助区分这些情形；这项设计不等于已经证明每次任务成功。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=15|§4.1–4.2 · pp.15–16]] [[raw/papers/optimization/finetuning/UI-TARS.pdf#page=22|§5 · p.22]]

统一动作包括点击、拖动、输入、等待，以及Finished和CallUser。后者用于登录/认证等需用户介入的情况，不能把增加模型能力解释为取消权限边界。GUI的恢复依赖具体应用状态，例如关错页后重新打开，不能推广为所有动作可逆。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=16|§4.3 · pp.16–17 · Table1]] [[raw/papers/optimization/finetuning/UI-TARS.pdf#page=21|§4.5 · p.21]]

训练组合为GUI感知/grounding、动作轨迹、教程和thought增广；在线轨迹经规则、VLM与人工过滤。反思数据区分“在原状态纠正动作”和“错误已经发生后补偿恢复”，SFT只监督纠正步；DPO使用正确/错误偏好对。以Qwen2-VL为骨干，经持续预训练、优质数据退火、DPO三阶段，数据约50B tokens。这里的长期经验主要经训练进入参数，不宜误读成每次运行自动更新权重。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=17|§4.3–4.6 · pp.17–22]]

## 成效与归因边界

OSWorld为369项网页/桌面任务，截图输入，以在线执行后的任务评估衡量，报告三次平均。72B-SFT在15步预算为18.8%，同尺寸DPO为22.7%；72B-DPO增至50步为24.6%。AndroidWorld为116项、20个应用的模拟器任务，72B-SFT为46.6%。这些数字来自不同评测与配置，不与离线单步准确率混排。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=25|§5.4 · pp.25–26 · Table9]]

SFT→DPO对照支持训练后模型策略仍是性能来源，但它不是单独隔离感知、规划与恢复各能力的实验。跨商业模型对比同时改变训练数据、规模及系统设置，不能证明“原生模型”原则上胜过harness。Table9说明CallUser及未输出Finish的轨迹被视为infeasible；本次未核代码确认其精确计分/分母处理，因此不能当成包含所有不可完成请求的部署成功率。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=26|§5.4 · Table9 · p.26]]

同一个模型通过提示切换有/无thought：三个域内离线基准Bo1时有thought略差，更多候选时变好；AndroidWorld域外Bo1时有thought更好。故“主动思考总有益”不成立，收益取决于任务与采样条件。本文BoN不能直接解释为无需额外选择器的真实在线收益。[[raw/papers/optimization/finetuning/UI-TARS.pdf#page=26|§5.5 · pp.26–27 · Fig.8]]

## 仍不足什么

**本库推断：**训练有效的证据反驳“GUI困难只在harness”；但模型无法自行提供屏幕中不存在的状态、执行权限和外部动作落地，故也不能只靠模型。当前证据最稳妥的判断是模型的感知/grounding/纠错能力与观察执行循环耦合，认证与不可见状态另属环境边界。本文未提供足以把剩余在线失败按模型、harness、环境精确分摊的受控实验，不因界面复杂就指定harness是主瓶颈。

## 整合状态

已整合至 [[wiki/applications/success-mechanisms|应用成功机制与瓶颈]]；过程见 [[组会/2026-10-28-Application/过程/A-软件与GUI|软件与GUI核读]]。共享主题、索引和日志未改；原件与页码检查完成，Obsidian未实测。
