---
type: paper
source_id: S008
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/MemGPT.pdf]]"
reading_status: 方法与主要实验核读
ingest_status: complete
---

# MemGPT：把上下文管理变成可执行操作

MemGPT 给有限上下文的 LLM 配上外部存储、读写函数与控制流：模型可以把内容写出当前窗口，之后检索回来，并连续调用函数完成多步查找。外部容量与当前可见上下文因此分离；**外部存下了，不等于模型此刻已经知道或必然能找回**。[[raw/papers/MemGPT.pdf#page=2|S008 · §2 · pp.2–4]]

## 身份与阅读范围

| 项目 | 登记 |
| --- | --- |
| 标题 | MemGPT: Towards LLMs as Operating Systems |
| 作者 | Charles Packer、Sarah Wooders、Kevin Lin、Vivian Fang、Shishir G. Patil、Ion Stoica、Joseph E. Gonzalez；按本版 PDF 登记 |
| 标识与版本 | arXiv:2310.08560v2，2024-02-12，13 页；不将综述参考文献作者表替代本版身份 |
| 原始来源 | [arXiv](https://arxiv.org/abs/2310.08560)；[v2 PDF](https://arxiv.org/pdf/2310.08560v2)，访问 2026-10-25 |
| Raw | [[raw/papers/MemGPT.pdf\|MemGPT.pdf]] |
| SHA-256 | `9F674BCFF69C86F11C813DCFAD613D8841F5F8ED17979E3C4DF06A91DF7762E0` |
| 实际阅读 | 2026-10-25；摘要与正文方法、实验 pp.1–8；实际查看 p.3 Figure 3、p.5 Table 2/3、p.7 Figure 7/8；附录未完整核读，未复现实验 |
| 综述入口 | S001 §4.2.2 / Table 3，pp.25–26；参考文献 [464]（p.113） |

## 哪些状态由谁维护

| 位置 | 内容与更新者 | 对执行的作用 |
| --- | --- | --- |
| Main context | 静态系统指令、可写 working context、FIFO 消息队列 | 模型每次实际看到的输入 |
| Recall storage | 队列管理器保存完整消息历史 | 模型用搜索函数召回被移出窗口的对话 |
| Archival storage | 模型通过函数保存任意文本 | 持久存储事实或文档，之后检索回窗口 |
| Function executor | 校验并执行模型发出的操作，返回结果或错误 | 将文本意图变成真实读写，并反馈容量或参数错误 |

表据 §2、Figure 3。working context 的修改由模型经函数执行；FIFO 的追加和淘汰由队列管理器执行，不能把全部内存管理都说成模型自主决定。[[raw/papers/MemGPT.pdf#page=2|§2.1–2.2 · pp.2–3]] [[raw/papers/MemGPT.pdf#page=3|Figure 3、§2.3 · p.3]]

```mermaid
flowchart LR
    A[外部事件或用户输入] --> B[模型读取主上下文]
    B --> C[发出读写或检索函数]
    C --> D[执行器返回结果或错误]
    D --> E{请求 heartbeat?}
    E -->|是，继续处理| B
    E -->|否| F[让出控制，等待新事件]
```

本库控制流示意，依据 §2.3–2.4。`request_heartbeat=true` 使函数调用后立即继续一轮模型推理，从而完成多个连续查询；这与只在每条用户消息时调用一次模型不同。[[raw/papers/MemGPT.pdf#page=3|§2.3–2.4 · pp.3–4]]

队列达到警告阈值时，系统提醒模型提前保存重要内容；达到淘汰阈值时，队列管理器移除旧消息，并把旧递归摘要和新淘汰内容形成新摘要。原消息仍留在 recall storage。文中的 70%、100%、50% 是阈值示例，不是所有实现必须使用的配置。[[raw/papers/MemGPT.pdf#page=3|§2.2 · p.3]]

## 证据支持到哪里

对话实验基于 Multi-Session Chat 的五段会话，额外生成第六段问答来测旧信息召回；使用 LLM judge 的正确率及 ROUGE-L recall。Table 2 的 GPT-4 组显示 32.1% 到 92.5%，但基线仅收到历史摘要，MemGPT 可以搜索完整历史。它支持这套记忆系统在该检索任务有用，不能视为“相同信息可达性与调用预算下只改变一个模块”的纯消融。对话开场的 embedding 相似度也是代理指标，不等于长期真实用户满意度。[[raw/papers/MemGPT.pdf#page=5|§3.1、Table 2/3 · pp.5–6]]

文档问答使用 NaturalQuestions-Open / Wikipedia 的 50 个问题；普通上下文基线主要接收一次检索所得文档，而 MemGPT 可重复查询和分页访问档案。结果同时涉及检索策略与外部可达文档量，不能仅归为窗口长度效应。论文也报告模型可能在找到答案前停止分页。[[raw/papers/MemGPT.pdf#page=6|§3.2.1 · pp.6–7]]

嵌套 key-value 测试要求沿 UUID 映射连续查询，展示控制流与多步检索的配合。GPT-4 版较稳定，GPT-3.5 等版本会因函数调用能力不足而退化；因此“提供了操作接口”不保证基础模型会可靠使用。Figure 7/8 是合成检索任务证据，不能直接推广为网页操作或机器人长程完成率。[[raw/papers/MemGPT.pdf#page=7|§3.2.2、Figure 7/8 · pp.7–8]]

## 局限与继续追问

**本库推断：**该工作的关键贡献是一套可操作的“写出—检索—控制权接续”机制。所谓无限上下文是外部存储与分页的设计目标，不是无限期准确、无成本运行的实验结论。重要前提包括可靠函数调用、可搜索的历史，以及模型知道何时保存和何时继续找。

**待检验问题：**读写策略造成的信息遗漏，与检索策略提前停止，能否在长任务评测中分别归因？本次正文给出后一现象，但未建立完整失效分解；当前是理解和评测问题，尚无限定范围的查新结论。

## 主题联系与整合状态

已整合至 [[wiki/harness/Overview#上下文与记忆|Harness：上下文与记忆]]：持久存储并不替代 working context，控制流是两者之间的接口。与 [[wiki/papers/HiAgent|HiAgent]] 比较旧轨迹恢复通道，但两者任务、模型与预算不同，不做性能排名。主题与索引已同步，内容与结构验收通过；Obsidian 未测。
