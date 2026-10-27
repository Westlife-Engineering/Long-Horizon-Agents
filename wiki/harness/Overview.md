---
type: overview
created: 2026-10-19
updated: 2026-10-27
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
---

# Harness：外部运行机制

围绕状态、动作、协作与验收组织运行机制。分类沿用S001作为可修订起点；机制可比较，分数须保留各自条件。


Harness 是围绕模型组织执行的机制：安排何时调用模型、带入什么状态、执行哪些工具、如何协调与检查。[[wiki/surveys/Towards Long-Horizon Agents|S001]] 将它作为长程能力的外化路径，与 [[wiki/optimization/Overview|模型优化]] 共同分析。这里归纳分类与接口责任，尚不评价某个具体方法的优劣。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=20|S001 · §4 · p.20]]

## 方向地图

| 方向 | 这里要区分什么 | 主归属来源 |
| --- | --- | --- |
| [[wiki/harness/workflows\|循环与工作流]] | 三类结构的特点、取舍与组合；反馈时点和分支恢复边界 | 5篇；跨方向见主题页 |
| [[wiki/harness/memory\|上下文与记忆]] | 工作上下文与持久记忆如何配合；保存、准入、取回和使用的边界 | 6篇；跨方向见主题页 |
| [[wiki/harness/tools\|工具、MCP 与技能]] | Tool、函数调用、MCP、工具发现与 skill 的关系；组合、复用与任务验收 | 4篇；跨方向见主题页 |
| [[wiki/harness/orchestration\|编排]] | 控制结构外化、可选编排路线与交接修复 | 6篇；跨方向见主题页 |
| [[wiki/harness/hooks\|Hooks 与中间件]] | 判断与控制怎样配合；政策准备与运行期、执行权与误拒边界 | 5篇；跨方向见主题页 |
| [[wiki/harness/verification\|验证]] | 证据怎样形成并用于评价；维度组合、PRM、纠错与任务成功 | 6篇；跨方向见主题页 |

## 问题与跨模块联系

[[wiki/harness/Questions|已收窄问题、反对证据与关闭条件]]保存本轮完整论证；尚无新颖性已确认的研究缺口。跨模块综合见[[wiki/frontier/Overview|Frontier]]。

选读队列、派发协议与提交流水见[[maintenance/research/R001|R001维护记录]]。新论文整合到相关主题；主归属目录不限制跨方向关联。
