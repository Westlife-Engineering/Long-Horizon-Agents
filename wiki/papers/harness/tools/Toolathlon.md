---
type: paper
source_id: S076
primary_direction: harness/tools
related_directions:
  - harness/verification
created: 2026-10-28
updated: 2026-10-28
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/Toolathlon.pdf]]"
---

# Toolathlon：跨应用任务的状态与完成标准

## 来源身份与读取范围

- 标题：The Tool Decathlon: Benchmarking Language Agents for Diverse, Realistic, and Long-Horizon Task Execution；Junlong Li、Wenshuo Zhao、Jian Zhao 等，完整作者见 p.1。
- 版本：[arXiv:2510.25726v2](https://arxiv.org/abs/2510.25726v2)，2026-02-26；[原始PDF](https://arxiv.org/pdf/2510.25726v2)，访问2026-10-28。主归属 tools：本文贡献是工具环境及执行评测，不是训练方法。
- 原件：[[raw/papers/harness/tools/Toolathlon.pdf|36页PDF]]；SHA-256 `A6240DF3A769DAA6D7E995ABD25A0DAB75643DD87EEEF4B2CEF143C91BD9347C`。
- 阅读：2026-10-28，正文§1–2、§3相关配置、§4–5、结论（pp.1–10），附录A–D及E.2概述（pp.14–18），HuggingFace上传末段（pp.27–30）、Notion HR完整刊载轨迹（pp.31–36）。图像检查p.7 Table3；未逐条审参考文献、未读完整上传轨迹pp.19–26、未运行代码或复现。PDF与印刷页码一致。
- 综述入口：S001 §6.5.1，PDF p.63，引文[322]；表7 p.66。身份网页只作版本核实，不留整页快照。

## 任务与已有成效

**论文事实：**108个任务跨32个应用、604个工具；每任务只暴露所需MCP服务器（少于10个），但不进一步筛选各服务器内部工具。模型在统一基本框架内最多100轮，运行三次。Table3中Claude-4.5-Sonnet平均pass@1为38.6±2.7%，三次均成功pass^3仅20.4%；Claude-4-Sonnet为29.9±1.6%。它展示配置间表现差异，不能证明新harness比旧方案更优，也不是部署成功率。[[raw/papers/harness/tools/Toolathlon.pdf#page=5|§2.4 · p.5]] [[raw/papers/harness/tools/Toolathlon.pdf#page=7|§4.1、Table3 · p.7]]

本轮具体任务选择 **Notion HR**：从本地10份PDF简历提取信息，读取Notion岗位及名额、清除样例、按格式填入候选人资料，对无名额岗位的申请者发指定模板邮件。Claude-4-Sonnet的刊载成功轨迹包含45次工具调用；中间两次API格式错误后改用正确调用。这里只证明一个受控任务的成功与恢复，不估计该任务稳定率。[[raw/papers/harness/tools/Toolathlon.pdf#page=18|App.E.2概述 · p.18]] [[raw/papers/harness/tools/Toolathlon.pdf#page=31|成功轨迹 · pp.31–36]]

## 环境、机制与职责

**环境条件：**岗位数据库、PDF原件、工具结构和写入权限可访问；邮件后端等由可初始化的真实软件提供。测试人员有独立终态评测脚本，但这不是每步发给agent的正确性oracle。可重置性支持重复评测，不代表运行中的发信等副作用能撤销。[[raw/papers/harness/tools/Toolathlon.pdf#page=4|§2.2–2.4 · pp.4–5]]

**模型行为：**选择先查页面与岗位再读简历，匹配岗位名额与申请人，决定写入/发信对象，解释API错误并纠正字段；最后自主声明结束。**Harness机制：**执行工具，把错误作为观察返还而不退出；长输出截断后保留缓存及分页/搜索工具；允许丢弃与回查历史，溢出时保留用户输入及最近10轮预览。能力依赖关系不是组件贡献率，本文没有这些机制的逐项消融。[[raw/papers/harness/tools/Toolathlon.pdf#page=14|App.B · pp.14–15]] [[raw/papers/harness/tools/Toolathlon.pdf#page=32|App.E.2 · pp.32–36]]

**本库推断：**它复用信息获取的证据组织、软件工程的执行反馈及状态外置。跨接口增加了身份映射、格式转换、覆盖全部对象及副作用一致性要求：读对简历但写错数据库对象，或选对岗位却漏发/误发，整件事仍未完成。仅增加更多工具不足以保证这些关系持续成立；本文未与固定HR流程或传统自动化做同预算对照。

## 剩余失败及归因边界

- **论文事实：**GitHub→Notion任务漏看部分对象，目标116行只产91行；跨年表格任务在66轮后只做1940年便结束。它们表明覆盖与停止判断失败，不证明缺少哪个固定模块。[[raw/papers/harness/tools/Toolathlon.pdf#page=16|App.C.2 · p.16]]
- 上传案例选对checkpoint、修正了认证/仓库名问题，但缺少README依赖的图片；末段所谓验证查的是本地上传文件夹，未保证远端完整产物。说明局部工具成功和自信声明不能替代端到端验收。[[raw/papers/harness/tools/Toolathlon.pdf#page=18|App.E.2概述 · p.18]] [[raw/papers/harness/tools/Toolathlon.pdf#page=27|上传末段 · pp.27–30]]
- 长输出与低成功率是观察性相关；任务与轨迹不同，不能算长输出的因果消融。GPT-5-high未优于默认配置也不能证明观察一定比推理更重要。模型训练数据、实际token/费用和供应商配置不同，最多支持统一框架下策略表现有差异。[[raw/papers/harness/tools/Toolathlon.pdf#page=8|§4.2–5.3 · pp.8–9]]

**条件性判断：**在这套框架下，存在模型未用好已有资源、未持续执行的直接行为证据；harness的上下文策略与流程约束未被控制替换，当前宜判model–harness耦合，无法排序贡献。没有策略内化训练实验，没有证明移除外部状态管理仍保持能力。

## 已整合主题

[[wiki/applications/Overview|应用与评测]]；本轮结构化讨论见 [[组会/2026-10-28-Application/README|Application组会]]。机制比较见 [[wiki/applications/success-mechanisms|应用成功机制与瓶颈]]。
