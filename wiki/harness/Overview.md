---
type: topic
created: 2026-10-19
updated: 2026-10-19
sources:
  - "[[raw/papers/Towards Long-Horizon Agents.pdf]]"
---

# Harness：外部运行机制

Harness 是围绕模型组织执行的机制：安排何时调用模型、带入什么状态、执行哪些工具、如何协调与检查。[[wiki/papers/Towards Long-Horizon Agents|S001]] 将它作为长程能力的外化路径，与 [[wiki/optimization/Overview|模型优化]] 共同分析。这里归纳分类与接口责任，尚不评价某个具体方法的优劣。[[raw/papers/Towards Long-Horizon Agents.pdf#page=20|S001 · §4 · p.20]]

## 页内导航

[[wiki/harness/Overview#循环与工作流|循环与工作流]] · [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] · [[wiki/harness/Overview#工具、MCP 与技能|工具、MCP 与技能]] · [[wiki/harness/Overview#编排|编排]] · [[wiki/harness/Overview#Hooks 与中间件|Hooks 与中间件]] · [[wiki/harness/Overview#验证|验证]]

## 循环与工作流

决定模型调用、行动、观察与状态更新如何接续。综述区分沿单条轨迹推进的线性流程、显式维护子目标的计划—执行流程，以及比较候选路径的分支流程。分类回答的是如何控制执行，不直接保证哪种结构效果更好。[[raw/papers/Towards Long-Horizon Agents.pdf#page=20|S001 · §4.1 · p.20]]

细分导航：Linear Workflows（§4.1.1）；Plan-Execute Workflows（§4.1.2）；Branching Workflows（§4.1.3）。后续阅读关注：失败时由谁重规划，状态如何传给下一步？

## 上下文与记忆

当前上下文是这次调用实际可见的状态，持久记忆是能够跨越当前窗口、任务或会话存续的信息。综述用“丢弃、压缩、选择”描述工作上下文的维护，用“写入、维护、检索”描述持久记忆操作。二者区别在存续范围与运行时角色，而不只在文件是否落盘。[[raw/papers/Towards Long-Horizon Agents.pdf#page=23|S001 · §4.2 · Fig.8 · p.23]]

细分导航：Working Context（§4.2.1）；Persistent Memory（§4.2.2）。与 [[wiki/foundations/Formalization#H1–H3 与 C1–C3|C2/C3]] 相关。待核读问题：保留的信息是否改变下一步决策，压缩是否丢失关键约束？

## 工具、MCP 与技能

这一组件规定 Agent 怎样访问外部能力、发现可用工具，以及复用程序性经验。综述将工具接口/协议、主动工具发现、技能库分开组织；工具接口与“如何完成一段工作”的可复用技能承担不同角色。[[raw/papers/Towards Long-Horizon Agents.pdf#page=26|S001 · §4.3 · p.26]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=2|§4.3.1–4.3.3 目录 · p.2]]

细分导航：Tool Interfaces and Protocols；Active Tool Discovery；Skill Libraries。这里只保留主题入口，尚未核读具体协议文档或技能方法论文。

## 编排

编排把工作分配到多个执行循环：拆分任务和角色，决定协调拓扑，调整路由/协调策略，再通过协议交换消息与产物。这是工作组织问题；不能由“用了多个 Agent”直接推出能力提升。[[raw/papers/Towards Long-Horizon Agents.pdf#page=29|S001 · §4.4 · Fig.9 · p.29]]

细分导航：Decomposition and Roles；Coordination Topologies；Orchestration Optimization；Agent Protocols。后续需要核查角色分工、通信、重复劳动与验证对端到端表现的影响。

## Hooks 与中间件

Hooks 在运行流程的特定位置介入，让动作继续、阻止动作或交接控制。综述按规则来源与适应性分成预定义规则、用户定义策略、运行时自适应信号三类。Hooks 可以使用规则或模型判断，因此不应一概当成形式化安全保证。[[raw/papers/Towards Long-Horizon Agents.pdf#page=31|S001 · §4.5 · Fig.10 · p.31]]

细分导航：Pre-defined Rule-based Hooks；Custom User-defined Hooks；Runtime-adaptive Hooks。与 [[wiki/frontier/Overview|可信性前沿]] 相连。

## 验证

验证检查状态、行动、输出或副作用是否满足要求。综述按三条轴组织：**检查什么**（正确性、安全性、指令遵循、验证器一致性）、**何时检查**（步骤中、运行结束）、**怎样产生判断**（自动标签/隐式奖励、验证器引导搜索、验证计算分配）。拦截机制与判断机制可以协作，但不是同一个角色。[[raw/papers/Towards Long-Horizon Agents.pdf#page=34|S001 · §4.6–4.6.1 · p.34]]；[[raw/papers/Towards Long-Horizon Agents.pdf#page=36|§4.6.2–4.6.3 · pp.36–37]]

细分导航：Assessment Targets；Verification Levels；Verifier Strategies。与 [[wiki/optimization/Overview#Agentic Reinforcement Learning|训练中的信用分配]]、[[wiki/applications/Overview|评测的成功判据]] 相关；运行时检查有效，不自动证明它可作为可靠训练奖励。

## 后续如何增长

当前六类都是有内容的导航段落，不对应六个空文件夹。新论文进入后，将它实际提供的机制、证据与限制写入相关段落，并链接唯一论文页；当内容需要独立比较时，再拆成如 `Context and Memory.md` 或 `Verification.md` 的页面。

返回 [[wiki/index|索引]]。
