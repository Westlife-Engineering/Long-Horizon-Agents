---
type: overview
created: 2026-10-19
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
---

# Optimization：能力内化与训练

围绕表示、数据、训练目标与反馈组织能力内化。分类沿用S001作为可修订起点；机制可比较，分数须保留各自条件。


[[wiki/surveys/Towards Long-Horizon Agents|S001]] 按架构基础及六个能力发展环节组织这一主线，共七个入口。它讨论如何把长程行为逐步内化到策略及可训练模块；这是一种组织框架，不意味着每篇方法都必须依次完成七个环节。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=37|S001 · §5 · p.37]]

## 方向地图

| 方向 | 这里要区分什么 | 主归属来源 |
| --- | --- | --- |
| [[wiki/optimization/architecture\|架构基础]] | 表示历史、访问证据与计算成本 | 5篇；跨方向见主题页 |
| [[wiki/optimization/data-environments\|数据与环境合成]] | 生成对象、真实执行与筛选后的分布 | 4篇；跨方向见主题页 |
| [[wiki/optimization/pretraining\|预训练与中期训练]] | 扩窗、数据配方、感知与代理指标 | 5篇；跨方向见主题页 |
| [[wiki/optimization/finetuning\|微调]] | 状态来源、监督位置与环境继续执行 | 5篇；跨方向见主题页 |
| [[wiki/optimization/reinforcement-learning\|Agentic Reinforcement Learning]] | 反馈、局部信用、采样与交互课程 | 7篇；跨方向见主题页 |
| [[wiki/optimization/distillation\|On-Policy Distillation]] | 学生状态、教师权限与最终入训过滤 | 5篇；跨方向见主题页 |
| [[wiki/optimization/self-evolution\|自我演化]] | 任务、轨迹、模型共同更新及真值锚点 | 6篇；跨方向见主题页 |

## 问题与跨模块联系

[[wiki/optimization/Questions|已收窄问题、反对证据与关闭条件]]保存本轮完整论证；尚无新颖性已确认的研究缺口。跨模块综合见[[wiki/frontier/Overview|Frontier]]。

选读队列、派发协议与提交流水见[[maintenance/research/R001|R001维护记录]]。新论文整合到相关主题；主归属目录不限制跨方向关联。
