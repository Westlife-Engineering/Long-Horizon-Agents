---
type: paper
source_id: S084
reading_status: body-and-selected-appendices-read
ingest_status: complete
created: 2026-10-29
updated: 2026-10-29
sources:
  - "[[raw/papers/harness/tools/AppWorld.pdf]]"
primary_direction: harness/tools
related_directions:
  - harness/verification
---

# AppWorld：可执行的应用世界与状态验收

**AppWorld 的合成应用执行真实的程序与数据库更新，并把目标达成、允许副作用和场景变体一致性分开检查。** 这为跨应用 Agent 提供了有明确机制的测量，但并不代表真实生产服务或现实用户分布。[[raw/papers/harness/tools/AppWorld.pdf#page=3|§2.1 · p.3]] [[raw/papers/harness/tools/AppWorld.pdf#page=6|§3.2 · p.6]] 与 Terminal-Bench 的比较见 [[wiki/applications/terminal-bench-comparison|跨基准审视]]，下文保留单篇证据与限定。

## 来源与读取范围

- **来源 ID：S084**；标题：*AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents*。
- 作者：Harsh Trivedi、Tushar Khot、Mareike Hartmann、Ruskin Manku、Vinty Dong、Edward Li、Shashank Gupta、Ashish Sabharwal、Niranjan Balasubramanian。
- 固定版本：[arXiv:2407.18901v1](https://arxiv.org/abs/2407.18901v1)，2024-07-26；官方元数据标为 ACL'24 Camera Ready。下载原址：[固定版本 PDF](https://arxiv.org/pdf/2407.18901v1)，访问与读取日期 2026-10-29。arXiv DOI：10.48550/arXiv.2407.18901；会议 DOI 本次未核实。
- 原始文件：[[raw/papers/harness/tools/AppWorld.pdf|AppWorld.pdf]]；SHA-256：`2ca1feab1559d678c28706acca11caab54a8a76c64dcf9e14d46f7bd33f21487`。从下载文件原样复制，前后哈希一致；递归查重未发现既有同文来源页或 PDF。
- **实际已读**：正文 §§1–8（PDF pp.1–10）；附录 A–J（pp.13–27，含公开任务的 setup、参考解、evaluation）；K 的 API predictor、FullCodeRefl、ReAct 提示及 PlanExec 提示开头（pp.27–33）。视觉核对 Fig.2–3、Table 1–3、Fig.4、评分公式及 Listing 3 末段（pp.3、5–8、27）。页码与此 arXiv PDF 印刷页码一致。
- **未读／未做**：参考文献不逐项核读；K 后续提示 pp.34–51、L 文档示例 pp.52–55 未精读；未下载／核读独立仓库实现，未安装或运行 benchmark，未调用付费 API；论文内代码清单的静态阅读不等于实现复现。未进行 Obsidian 应用内验收。

## 测量的价值与位置

**原文陈述。** AppWorld 把数字助手任务做成“自然语言需求 → 查应用资料与文档 → 交互式写代码 → 改变应用状态 → 程序验收”。目标是跨日常应用、读中间结果后继续决定行动的自动化能力。其贡献包含可控执行环境和任务集两层：9 个应用、457 个 API、101 张数据库表、106 个虚构人物；任务并非要求复现唯一 API 调用串，而是达到符合目标的终态。[[raw/papers/harness/tools/AppWorld.pdf#page=2|§§1–2 · pp.2–4]]

**本库判断。** 它适合比较既定模型与 harness 在跨应用、带干扰项和状态副作用的任务中能否完成交付，也适合研究文档探索、程序组合和状态追踪。这里的困难有明确机制基础，不只由低分倒推出有价值。但作者构造的日常任务及分布不能直接估计真实用户总体的成功率或经济价值；作者也承认任务来自北美、欧洲机构研究者，未必代表其他地区数字生活。[[raw/papers/harness/tools/AppWorld.pdf#page=5|§§3.1–3.3 · pp.5–6]] [[raw/papers/harness/tools/AppWorld.pdf#page=10|§§7–8 · p.10]]

### 合成应用怎样产生真实状态执行

这里“合成”指应用的自建实现、虚构人物及其活动数据，不是由 LLM 临时编造每次工具响应。应用用 FastAPI、SQLite、SQLModel 实现：发送邮件会写入发送者和接收者的邮件／线程表；下单会改变订单、购物车、库存并触发确认邮件；授权、分页、错误反馈也有程序实现。运行前可恢复数据库和冻结时间，使“今天”“本月”等指令有固定含义。[[raw/papers/harness/tools/AppWorld.pdf#page=3|§§2.1–2.3 · pp.3–4]]

执行 shell 基于 IPython，代码变量跨轮保留；执行异常、API 错误、超时会返回给 agent。实验采用 Python 函数形式调用 API，也可走 REST；SQLite 与 FastAPI TestClient 使调用和服务可在同一进程中执行。它因此有真实代码执行和持久状态，**但不是任意操作系统终端工作**：系统级文件／进程操作受到限制，模拟 FileSystem 应用也不能直接等同宿主文件系统。[[raw/papers/harness/tools/AppWorld.pdf#page=13|App.C · pp.13–14]]

**本库判断。** 可控状态带来可重置、可比对副作用、无真实付款后果等测量收益；同时省去了线上服务变化、真实外部资源和多模态界面的复杂性。真实执行、生产环境保真度与真实用户代表性是不同轴，不能用一个“真实／合成”二分代替核查。本文限于单个 supervisor 交给单个 assistant 自主完成任务，UI 和多 agent 协调是后续扩展。[[raw/papers/harness/tools/AppWorld.pdf#page=2|§1 · p.2]] [[raw/papers/harness/tools/AppWorld.pdf#page=10|§7 · p.10]]

## 一题从输入到动作再到评分

公开例题 `b0a8eae` 要求：读取 Simple Note 中的锻炼计划，开始播放一个能覆盖今天锻炼时长的 Spotify 播放列表，避免中途换列表。它保留了跨应用信息依赖，且能完整看到生成、解题和评分三段代码。[[raw/papers/harness/tools/AppWorld.pdf#page=23|App.J · Listings 1–3 · pp.23–27]]

1. **初始信息与隐藏数据。** Agent 得到用户身份和任务描述，可以通过 Supervisor 获取账户信息，通过 ApiDocs 获取接口说明；期望答案／私有 evaluation data 不交给 agent。Setup 选择日期、准备多种日期时长与多个播放列表，只让一个列表足够长，其他列表时长接近但偏短；重置播放器与队列，变换笔记标题。正确列表歌曲 ID 与当天时长另存私有数据。[[raw/papers/harness/tools/AppWorld.pdf#page=5|§3.1 · p.5]] [[raw/papers/harness/tools/AppWorld.pdf#page=23|Listing 1 · pp.23–25]]
2. **行动与反馈。** 获取密码并登录 Simple Note，分页检索和读取笔记，根据冻结日期识别当天时长；登录 Spotify、分页获取列表，查询歌曲时长并求和，选择够长的列表播放。API 返回数据与错误供继续决策。公开参考解使用预知笔记结构的解析代码，因此它证明该环境和验收存在可行解，不等于普通模型在无内部知识条件下能一次写出解。[[raw/papers/harness/tools/AppWorld.pdf#page=6|§3.3 · p.6]] [[raw/papers/harness/tools/AppWorld.pdf#page=25|Listing 2 · pp.25–26]]
3. **终止与交付。** 调用 `supervisor.complete_task`；非问答任务不需要解释性答案。交付是播放器状态，不是“已播放”的文字声明。脚手架也可因调用上限而结束。[[raw/papers/harness/tools/AppWorld.pdf#page=7|§4 · p.7]] [[raw/papers/harness/tools/AppWorld.pdf#page=26|Listings 2–3 · p.26]]
4. **自动评分。** Listing 3 检查答案、记录 task completion 状态，并断言变化的应用模型只有 `spotify.MusicPlayer`；主用户播放器正在播放；队列总时长达到阈值；队列歌曲 ID 集合等于预先保存的合格列表集合。并非必须按参考解的查询顺序操作。[[raw/papers/harness/tools/AppWorld.pdf#page=26|Listing 3 · pp.26–27]]

**教学反例（本库构造，未执行）：**只返回“已完成”而没有播放会被播放状态检查拒绝；修改锻炼笔记以缩短所需时长会引入其他表变化，并不能改变私有时长阈值；播放另一个不够长的列表会失败。这说明验收包含实体状态和无关改动保护，而不是看回答措辞。

**静态审查的边界。** 此例公开清单只限制改变的模型名称，再检查主用户的 MusicPlayer；没有显式展示“该表其他用户行不变”的断言。集合相等也不直接检验歌曲顺序或重复次数。这是清单的覆盖疑点，**未运行可达反例，不能记成已确认漏洞**；是否允许或能够产生这些状态，还依赖实际 API 和未核读的通用测试逻辑。它提示应区分框架的无关状态保护目标与每题断言是否完整实现。[[raw/papers/harness/tools/AppWorld.pdf#page=27|App.J · Listing 3 · p.27]]

## 任务来源、划分与“长程”证据

任务由作者团队开发，而非从真实用户委托中随机采样，也不是众包或 LLM 直接出题。Base DB 通过经测试的 API 程序化生成，精确语义重要的文本由人编写；少量无需精确语义的支付消息等内容借助 ChatGPT，并经迭代人工审查。Setup 加入可解前提、干扰、支付卡过期等障碍及不同条件的 contrast set；每个场景有生成、参考解和评分代码，经过代码审查与测试。已读范围没有报告完整候选池／剔除计数，不能推定为按模型失败筛出的样本。[[raw/papers/harness/tools/AppWorld.pdf#page=4|§§2.3–3.1 · pp.4–5]] [[raw/papers/harness/tools/AppWorld.pdf#page=7|§3.4 · p.7]]

- **规模与计数单位：**250 个 task scenarios，每个 3 个任务，共 750。Train 105、Dev 60、Test-N 168、Test-C 417。三个同场景变体用于检验在条件变化下是否稳定完成，不能视为 750 个完全独立的问题模板。[[raw/papers/harness/tools/AppWorld.pdf#page=6|§3.4 · pp.6–7]]
- **划分：**Test-C 包含至少使用 Amazon 或 Gmail 中一个指定“未见应用”API 的全部任务；余下部分随机分入 Train、Dev、Test-N，作者称其同分布。这里“未见”相对 benchmark 训练／提示任务，不是声称预训练模型从未接触 Amazon/Gmail。它测新应用接口使用和跨应用组合，同时 Test-C 本身也更复杂；不能将分数下降全部归因于组合泛化或宣称严格只留出新组合的受控切分。正文没有展开随机划分的场景级实现，本次未核读划分代码。[[raw/papers/harness/tools/AppWorld.pdf#page=7|§3.4 · Table 2 · p.7]]
- **交互规模：**Table 2 的 Test-N* 是 Train、Dev、Test-N 的并集，不是仅 Test-N。其参考解平均 42.5 次 API 调用、41.3 行代码；Test-C 平均 46.8 次调用、56.9 行，最大 649 次调用，平均 10.5 个不同 API、最多 6 个应用。这是参考解的执行／程序复杂性代理，不是模型轮数、真人耗时或持续数小时的实测。[[raw/papers/harness/tools/AppWorld.pdf#page=7|Table 2 · p.7]]
- **交互为何必要：**作者用自由文本笔记为例，强调有些题必须先看到中间内容再理解和决定后续代码；即使响应 schema 完整，也不能只凭初始任务知道笔记内容。其“理论上不能一次写完”的强表述应保留为作者观点，适用边界涉及是否允许程序内部另调用语言理解组件，不是本文证明的一般计算不可能性定理。[[raw/papers/harness/tools/AppWorld.pdf#page=13|App.A · p.13]]

**数值不一致保留。** §1 报告每题评价测试平均 8、最多 22，但 Table 2 的 Test-C 最多为 24；§5 将平均代码行数写为 41.3，而 §1 全集概述为约 50，41.3 实际对应 Table 2 的 Test-N*。引用具体统计时按表的分母写出，不能静默合并。[[raw/papers/harness/tools/AppWorld.pdf#page=2|§1 · p.2]] [[raw/papers/harness/tools/AppWorld.pdf#page=7|Table 2 · p.7]] [[raw/papers/harness/tools/AppWorld.pdf#page=9|§5 · p.9]]

## 判分可信性：保护什么，证据到了哪层

**原文机制。** 评分比较起始与终止数据库：要求必需变化集合包含于实际 diff，且实际 diff 不超出必需变化与允许变化的并集。允许变化用于接纳多个合理终态，例如下单后购物车恢复原状或清空都可接受；也可关联数据库表检查 diff 行外的属性。约 15% 任务是问答，还需对固定答案。TGC 是所有测试通过的任务比例；SGC 是一个场景内全部三个变体均通过的场景比例，**不是同一道题随机重跑三次的 pass^3**。[[raw/papers/harness/tools/AppWorld.pdf#page=5|§3.2 · pp.5–6]]

| 证据层 | 本文实际提供 | 可以支持什么／不能替代什么 |
| --- | --- | --- |
| API 环境行为 | 约 1,780 个单元测试，报告 API 实现覆盖率 98%；提供错误与权限等测试名示例 | 支持实现经过系统测试；代码覆盖率不是任务验收语义正确率。[[raw/papers/harness/tools/AppWorld.pdf#page=4\|§2.2 · p.4]] [[raw/papers/harness/tools/AppWorld.pdf#page=22\|App.I · Table 11 · p.22]] |
| 每题可解与回归检查 | 人写参考解能通过相应 evaluation；作者明确参考解可用少量内部知识 | 支持给定题与测试存在可行解，不证明所有正确解都会通过，也不是真人限时基线。[[raw/papers/harness/tools/AppWorld.pdf#page=6\|§3.3 · p.6]] |
| 终态／副作用验收 | required/allowed diff 规则与公开单题断言 | 有明确需求映射，优于只匹配某条参考轨迹；每题覆盖仍需审查，不能推出任意未预见破坏均被挡住。[[raw/papers/harness/tools/AppWorld.pdf#page=6\|§3.2 · p.6]] [[raw/papers/harness/tools/AppWorld.pdf#page=27\|Listing 3 · p.27]] |
| 人类参照 | 作者设计、审查任务，编写解法；人工查看 GPT-4o 错误 | 已读范围未报告真人同条件成功率／实测耗时，也未报告对同一批终态独立人工验收与自动判分的一致性。不能把出题与诊断人员当成人类基线或评分校准。[[raw/papers/harness/tools/AppWorld.pdf#page=7\|§§3.4–4.3 · pp.7–9]] |

**本库判断。** 程序状态评价适合这类确定性目标，不需要一律改用人类或 LLM judge；但稳健性的核心是断言与需求一致、覆盖等价解和意外副作用。终态差分还可能无法区分“从未改变”与“先改变再恢复”，论文 diff 算法明确会忽略恢复后的同值行；因此不能直接用它证明轨迹中从未发生违规行为。对实际邮件／付款等不可逆事件，若真实风险不完全保留在终态数据中，还需不同的验证对象。[[raw/papers/harness/tools/AppWorld.pdf#page=14|App.D · pp.14–15]]

## 实验协议与结果应怎样读

本文比较的是 **模型 + 提示／文档获取 + 交互预算 + 上下文截断** 的组合。模型包括 `gpt-4o-2024-05-13`、`gpt-4-turbo-2024-04-09`、Llama-3-70b-chat、DeepSeek-Coder-33b-instruct，以及自带专用模型的 CodeAct、ToolLLaMA；使用 greedy decoding。部分模型因 Test-N 初步结果和成本／限流未继续在 Test-C 评估，因此不是所有候选模型的完备横向矩阵。[[raw/papers/harness/tools/AppWorld.pdf#page=8|§4.2 · p.8]] [[raw/papers/harness/tools/AppWorld.pdf#page=17|App.E.7、F.5 · pp.17–18]]

| 方法 | 信息与预算要点 |
| --- | --- |
| ReAct | 自行按需查 API 文档；一条简化示例，最多 100 次 LLM 调用；轨迹超过 20,000 字符先删较旧 observation、保留最后两步输出，必要时再删旧整步。 |
| PlanExec | 先计划再逐步用 ReAct 执行；planner 3-shot、executor 5-shot；同类截断。论文该附录未清楚给出整个规划执行组合统一调用上限。 |
| FullCodeRefl | 输入预测出的 API 文档，3-shot，先整段代码后据异常反思，最多 5 次重试；错误前已产生的数据库变化保留。 |
| IPFunCall | 批量独立 API 调用，3-shot；最多 15 轮，每轮可有多个函数调用，因此不等于 15 次 API 调用。 |

以上取自 [[raw/papers/harness/tools/AppWorld.pdf#page=15|App.E.1–E.4 · pp.15–17]] 与 [[raw/papers/harness/tools/AppWorld.pdf#page=29|App.K · Listing 6 · pp.29–30]]。这些预算不是等 token、等时间或等费用；FullCodeRefl 的异常重试也不是获得评分 oracle 后反复选答案。CodeAct 另限 10 次交互，并把原方法的 oracle 停止条件改成完成调用或上限。[[raw/papers/harness/tools/AppWorld.pdf#page=17|App.E.6 · p.17]]

主表中 GPT-4o + ReAct 在 Test-N 的 TGC/SGC 为 **48.8/32.1**，Test-C 为 **30.2/13.0**。同一 GPT-4o 换 FullCodeRefl 后分别为 33.9/26.8、19.2/12.2，说明不能只说“GPT-4o 能力分数”。把参考解所用 API 作为 oracle 提供，ReAct 的 TGC 提升至 54.8、35.2，仍有明显余量；这是文档检索不足不能独立解释全部失败的证据，但不排除检索是部分任务瓶颈，也不证明其他具体失误的因果份额。[[raw/papers/harness/tools/AppWorld.pdf#page=8|§§4.2–4.3 · Table 3 与 oracle 对照 · p.8]]

人工错误分析列出不看环境而臆测、API schema 使用错、只满足部分指令、常识混淆、忘记前态重复工作等现象；没有在该段报告抽样数、标注者一致性或每类频率，因此这里只作为观察线索。Table 3 未提供跨随机重复的方差、置信区间或逐任务显著性检验；三个同场景变体是任务条件变化，不是重复 seed。不能依据小幅分差下稳定排名结论。[[raw/papers/harness/tools/AppWorld.pdf#page=8|§§4.2–4.3 · pp.8–9]] [[raw/papers/harness/tools/AppWorld.pdf#page=17|App.E.7、F.2–F.3 · pp.17–18]]

历史费用估计以 2024-06 OpenAI 价格为口径：Test-N 的 GPT-4o 每例 ReAct 约 $0.70、PlanExec $1.33、IPFunCall $0.33、FullCodeRefl $0.02。这是作者的模型费用估算，不是当前价格或总运行成本；巨大成本差也限制将方法准确率视为等预算比较。[[raw/papers/harness/tools/AppWorld.pdf#page=17|App.E.8 · p.17]]

## 对 Terminal-Bench 定位的反证与仍成立的增量

已回读 [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]] 及 [[raw/papers/harness/tools/Terminal-Bench.pdf#page=16|S080 · References · p.16]]：S080 将 AppWorld 放在 computer use 一组，强调自己的多样、长程、专家采集和真实 terminal shell。以下为读过双方指定原文后的**本库比较**，不比较两者异条件总分。

| 要检验的理解 | AppWorld 的直接反证／限定 | Terminal-Bench 仍可成立的定位 |
| --- | --- | --- |
| 多应用、多步任务以前没有得到测量 | 9 应用、依赖中间信息的代码交互、几十次参考 API 调用和最多 6 应用，早已超出单次调用。[[raw/papers/harness/tools/AppWorld.pdf#page=7\|§3.4 · Table 2 · p.7]] | S080 可以强调终端上不同专业任务的组合与来源，不宜把“多领域＋长程”本身写为独有。 |
| 合成环境意味着没有真实执行 | API 实际读写数据库，Python 状态跨轮保留，并处理权限、分页及跨应用后果。[[raw/papers/harness/tools/AppWorld.pdf#page=3\|§2 · pp.3–4]] | S080 的自由终端／实际软件环境与 AppWorld 的自建应用 API 确有接口、资源与保真度差异。 |
| 真实 shell 自动带来更可信评分 | AppWorld 已有允许多条解法的状态 diff、无关变化保护及可执行参考解。[[raw/papers/harness/tools/AppWorld.pdf#page=5\|§§3.2–3.3 · pp.5–6]] | 需要逐项比较测试覆盖、需求一致性、对抗检查；环境类型不能单独给评分可信性排序。 |
| AppWorld 是 GUI 导航基准 | 本文实验通过代码／API；作者把 UI 交互明确区分为另一模态。[[raw/papers/harness/tools/AppWorld.pdf#page=18\|App.G · pp.18–19]] | S080 的宽泛 computer-use 分类可作导航，但具体对照必须写清 API coding 与 terminal 操作。 |

**最强反对意见与结论。** AppWorld 的确牺牲了开放真实服务的若干复杂性，人工设计数据也没有证明部署代表性；它不能直接代替真实终端评测。但这支持的是不同受控条件下的互补测量，不能支持“synthetic 因而无效”或“Terminal-Bench 首次测长程多领域”。AppWorld 的核心增量是可控应用世界、复杂交互任务与过程无关的状态验收；S080 仍可在真实终端工作接口、任务来源和专业任务范围上主张增量，需另外验证这些增量是否带来所声称的现实价值。

## 主题落点与后续边界

已整合至 [[wiki/applications/Overview|应用与评测]]、[[wiki/harness/verification|验证]] 与 [[wiki/applications/terminal-bench-comparison|跨基准审视]]，并与 [[wiki/papers/harness/tools/Terminal-Bench|Terminal-Bench]] 互链。主协调者回核 pp.3–8 及 p.6 原页公式；原件哈希、链接、页码与表格转义由本轮统一检查。最值得保留的澄清是“合成来源、真实执行、现实保真与验收可信性分开判断”，以及“场景变体鲁棒性不等于同题重复运行可靠性”。未复现实验，Obsidian 内显示未测。
