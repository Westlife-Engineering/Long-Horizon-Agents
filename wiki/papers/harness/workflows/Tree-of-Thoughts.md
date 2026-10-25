---
type: paper
primary_direction: harness/workflows
source_id: S005
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf]]"
reading_status: 正文与实验附录已核读
ingest_status: complete
---

# Tree of Thoughts: Deliberate Problem Solving with Large Language Models

Tree of Thoughts（ToT）把一次连续输出改成对**部分解**的搜索：模型生成几种下一步，模型评价它们的前景，外部搜索程序决定保留、继续或回退哪些状态。它不是只在提示里加一句“多想几条路径”，也不是原论文已经实现 MCTS；本文实现的是有宽度限制的 BFS 与可剪枝、回溯的 DFS。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=3|S005 · §3 · pp.3–4、Algorithms1–2]]

> [!important] 证据边界
> 主要实验是 24 点、四段创意写作与 5×5 填字。它证明这些有限、可复制的解题状态适合某些搜索策略，不直接证明真实长期 Agent 可以回滚外部环境，也不解决跨窗口状态恢复。完成摄入，主 Agent 内容/结构验收通过；结果未复现。

## 身份与读取范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S005 |
| 作者 | Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan |
| 版本 | NeurIPS 2023 正式会议 PDF；本次归档的是 proceedings 文件，未将其标成未经核实的 arXiv 版本 |
| 原始来源 | [NeurIPS 原始 PDF](https://papers.nips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf)，访问 2026-10-25 |
| 本地原件 | [[raw/papers/harness/workflows/Tree-of-Thoughts.pdf\|Tree-of-Thoughts.pdf]]，14 页 |
| SHA-256 | `6939CADEBD84C8CDCC6FF3C2082B75851A86E2EF82008848D0AF692F80521FA7` |
| 实际读取 | 2026-10-25；正文 pp.1–9、Appendix A–B pp.13–14；实际查看 p.4 Algorithms1–2，p.5 Fig.2，p.6 Table2/Fig.3，p.7 Table3/Figs.4–5，p.8 Fig.6，p.14 Tables7–8 的渲染原页 |
| 未核读范围 | 参考文献未逐篇追索；Appendix A 仅给代码/提示/轨迹链接，链接内代码和全部日志未审计；未复现实验 |
| 综述入口 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=22\|S001 · §4.1.3 · p.22]]，参考文献 [760] |

## 困难：第一步错误，后面再流畅也可能无解

作者关心需要探索和回溯的任务。连续 CoT 可以有多个推理步骤，但一条已采样的链内部不会自动保存每一步的替代分支；CoT-SC 虽采样多条完整链，投票仍主要发生在末端。ToT 把选择提前到中间状态。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=3|S005 · §2–3 · p.3]]

24 点中的例子很直观：从四个数选两个做第一步运算，可能马上失去组成 24 的可能；后面写出更多解释不能恢复那两个原数。作者的错误分析在这个任务中发现大量 CoT 失败发生在第一步，但不据此推广到所有长期任务。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=6|S005 · §4.1 · p.6、Fig.3(b)]]

**本库分析：**ToT 提供任务内分支与状态选择的基础机制，其“长”主要指决策之间有依赖。24 点只有三个 thought 步，创意写作只有一个中间计划步；填字路径最多十次填词。搜索调用多，不等于验证了真实长时程执行。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=5|S005 · Table1 · p.5]] [[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=7|S005 · §4.3 · pp.7–8]]

## 四个设计决定系统实际搜索什么

树节点表示输入加已有 thought 序列，亦即一个部分解。实现 ToT 必须指定 thought 粒度、候选生成方式、评价器和搜索算法；这些不是由“树状思考”四个字自动给出的。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=3|S005 · §3 · pp.3–4]]

| 决定 | 本文实现 | 必须保留的区别 |
| --- | --- | --- |
| Thought 粒度 | 一步算式、一个填词、一个写作计划 | 足够小才能产生不同候选，足够大才能评价；粒度依任务手工设计 |
| 候选生成 | 独立采样多项，或在一次提示中列出若干项 | 多候选不保证覆盖正确分支；重复候选会浪费预算 |
| 状态评价 | 独立判断 sure / likely / impossible 等，或比较候选后投票 | 这些是 LM 启发式，不是已知真实价值；可多次采样聚合 |
| 搜索控制 | BFS 每层保留前 b 个；DFS 优先探索、低值剪枝、回溯 | 程序控制保存哪些状态；本文没有最优性或完备性保证 |

证据：[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=3|S005 · §3 · pp.3–4、Algorithms1–2]]。

```mermaid
flowchart LR
    S[当前部分解] -->|模型提议| C[多个下一步候选]
    C -->|逐项评分或比较投票| V[模型启发式评价]
    V -->|搜索程序保留可探索状态| F[候选集合或 DFS 栈]
    F -->|选择继续或回溯| S
    F -->|终止规则选择| O[最终输出]
```

本库依据 §3 重绘。中间评价和最终输出选择是两个可分别出错的环节；图中的回溯发生在保存的解题状态中，不表示撤销已经发生的真实交易或物理动作。

## 实验怎样支持这种设计

主体使用 2023 年 5 月的 GPT-4 Chat Completion，采样温度 0.7；这是固定历史实验，不是当前模型能力测试。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=5|S005 · §4 · p.5、脚注1]]

| 任务与预算 | 直接结果 | 解读边界 |
| --- | --- | --- |
| 24 点：100 道相对困难题，3 步；每层保留 b=5，状态评价采样3次 | ToT 成功率74%，b=1时45%；CoT平均4%，CoT-SC100条9%；oracle挑选100条CoT中最好为49% | 74%不是与单条CoT等调用或等成本的比较；best-of-100也用了知道正确答案的选择器 |
| 创意写作：100组四句约束；生成5个计划投票选1个，再生成5篇文章投票选1篇 | 作者盲评偏好ToT41组、偏好CoT21组、38组相近；模型连贯性评分也改善 | 人评来自作者子集；测量连贯性，不是科学创新。IO+refine的模型评分还高于不加refine的ToT |
| 填字：20道5×5题，DFS最多100个搜索步；不能直接修改路径中已有字母，通过回溯换路径 | ToT词级60%，整题4/20；按已知正确答案oracle选树中最好状态可达7/20 | 60%词级不能写成60%整题成功；7/20不等于系统实际最终输出 |

定位：[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=5|S005 · §4.1 · pp.5–6、Table2]]；[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=6|S005 · §4.2 · pp.6–7、Fig.5]]；[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=7|S005 · §4.3 · pp.7–8、Table3]]。

## 搜索没有消除评价错误，还可能放大它

填字实验中，模型可能不认识正确但罕见的词，连已经完成的正确棋盘也会被判断为不可解而剪掉。去掉剪枝总体表现变差，却又找到了部分原策略没找到的解；取消回溯的对照也更弱。因而有用的结论是“生成、评价、剪枝、回溯与输出选择相互制约”，不是“自评可靠”或“永远不要剪枝”。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=8|S005 · §4.3 · p.8]]

Appendix B.2 混合不同模型来做生成和评价，显示 24 点中两者都会影响结果，生成质量尤其关键。但 GPT-3.5 版本还将 proposal 示例从1条改为3条，不能把跨模型差异归因于参数规模这一单因素。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=14|S005 · Appendix B.2 · p.14]]

成本也应作为机制的一部分看：正文明确搜索增加调用；Appendix B.3 报告 24 点约5.5k生成 token，接近100条CoT的6.7k，创意写作约需数倍生成量。不同调用的 prompt 成本、评价成本和选择权限不同，不能只按“访问节点数”当作完全相同算力；论文中的美元价格仅是历史实验记录，本页不用于当前费用估算。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=9|S005 · §6 · p.9]] [[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=14|S005 · Appendix B.3 · Tables7–8 · p.14]]

## 放进 Long-Horizon Agents 地图时怎样使用

已整合到 [[wiki/harness/workflows|Harness · 循环与工作流]] 的树状搜索与反馈比较：ToT 让 LM 扮演候选生成器和启发式评价器，程序负责搜索状态；其可撤销的文本部分解与真实环境动作必须区分。主题与论文页已互链，内容与结构已验收；Obsidian 应用未测。

与 [[wiki/papers/harness/workflows/ReAct|ReAct]] 的环境观察回路相比，ToT 主体实验中的分支筛选主要依赖模型自评；最终题目评分与搜索过程中拿到的反馈不是一回事。与 [[wiki/papers/harness/workflows/Arbor|Arbor]] 相比，ToT 的树保存同一问题的解路径，Arbor 的树组织跨实验的假设和认识，两者的节点、边与回传语义不同。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=3|S005 · §3 · pp.3–4]] [[raw/papers/harness/workflows/Arbor.pdf#page=6|S004 · §4.2 · p.6]]

**待检验问题：**当评价器对罕见但正确状态缺乏知识时，应暂存分支、检索外部证据还是继续采样？原文已提出外部检索可缓解知识不确定性的方向，不能把这句话本身当作新的 idea；若继续研究，需限定更具体的失败条件并查新。[[raw/papers/harness/workflows/Tree-of-Thoughts.pdf#page=8|S005 · §4.3、脚注2 · p.8]]

原件及关键图表已核对；代码运行和 Obsidian 中图表、PDF跳转、窄分栏均未实测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/workflows|harness/workflows]]。
