---
type: paper
source_id: S086
primary_direction: harness/tools
related_directions:
  - harness/verification
created: 2026-10-29
updated: 2026-10-29
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/tau-bench.pdf]]"
---

# τ-bench：动态用户、业务政策与重复成功的测量

**τ-bench 已经把工具使用放进多轮、有状态、需要澄清与授权的完整任务。** 它在零售和航空两个简化业务域中，用可执行 API、LLM 用户和政策文件评价模型＋agent scaffold；最终检查数据库结果与指定回答信息，并用 `pass^k` 测同一任务重复运行时能否次次成功。它能诊断客服式工具交互的脆弱性；分数不等于全面政策合规、真实顾客满意度或生产可靠率。[[raw/papers/harness/tools/tau-bench.pdf#page=3|S086 · §3 · pp.3–5]] [[raw/papers/harness/tools/tau-bench.pdf#page=7|§5 · pp.7–9]]

## 来源身份与实际读取

- **作者与版本：** Shunyu Yao、Noah Shinn、Pedram Razavi、Karthik Narasimhan；ICLR 2025 会议论文，OpenReview `roNSXZpUDN`。归档的是 [ICLR 官方会议版 PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf)，共53页；[会议索引](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html)核对标题、作者和会议。会议版具体修订日期未确认；访问日期2026-10-29。页码均为PDF物理页，与印刷页码相同。
- **原件：** [[raw/papers/harness/tools/tau-bench.pdf|tau-bench.pdf]]；SHA-256 `e2d45d573e1fce753ead1a44cc468ad386dd384e2668450d0a9c0e2c7920ada0`。官方文件原名 `1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf`；临时下载后原样复制，复制前后哈希相同。递归标题、标识与文件哈希查重未发现同篇已存原件或唯一页。
- **版本边界：**同篇早期 [arXiv:2406.12045v1](https://arxiv.org/abs/2406.12045v1) 于2024-06-17提交，50页；仅作临时对照，不另归档。本页以会议版为准，尤其包含预印本没有的 §5.3 用户模拟策略核查。本文不是后续 τ²-bench；未用后续榜单替代论文实验。
- **读取范围：**2026-10-29核读正文 §§1–6（pp.1–10），附录 A（p.12）、B.1 API示例与两域完整政策（pp.12–19）、C.2.1完整失败轨迹（pp.25–30）、D.2完整成功轨迹（pp.48–53）。B.2数据生成与C.2.2／C.2.3曾读早期版并对会议版定位，不计为会议版逐页完整核读；其余数据样例与完整引用文献未逐项审查。另实际回读S080 §6 p.11。
- **原页视觉核查：**会议版p.4 Fig.2、p.5奖励限定与指标公式、p.7 Table 2／Figs.3–4、p.9 Table 4／Fig.6；早期版图表不用于替代会议版页码。读了PDF内展示的API代码，未核读仓库评分器实现、锁定代码commit或运行benchmark；未调用付费API。
- **整合状态：**已整合至 [[wiki/applications/Overview|应用与评测]]、[[wiki/harness/verification|验证]] 及 [[wiki/applications/terminal-bench-comparison|跨基准审视]]。主协调者回核会议版 pp.4–5、9–10，视觉核对 p.5 公式与奖励限定；结构与哈希由本轮统一检查，Obsidian内显示未测。

## 为什么这项测量有用

**作者目标：**客服Agent要一边询问信息、一边操作数据库，还要遵守不完全由API强制的规则；相同诉求换一种表达也应稳定完成。τ-bench把动态对话、工具状态与业务政策组合起来，补足仅评函数名／参数或预先给齐信息的静态任务。关于其他基准缺点的论述在本页仍是作者比较，不自动构成对所有被引工作的独立核验。[[raw/papers/harness/tools/tau-bench.pdf#page=1|§§1–2 · pp.1–3]]

**本库判断：**价值在于检验“符合政策的业务结果是否稳定交付”，而非因为模型低分就证明基准好。这个目标与客服部署需求相符，但作者使用合成且简化的业务域、固定用户意图与唯一目标终态，适合比较和诊断，尚不足以估计真实业务流量的平均表现或经济收益。[[raw/papers/harness/tools/tau-bench.pdf#page=5|§4 · pp.5–6]]

## 一题如何运行：先问全，再做不可重复的换货

附录C.2.1的零售Task 0中，Yusuf希望将同一已送达订单里的键盘换成指定轴体／背光选项，同时把温控器换成兼容Google Home的型号。**用户模拟器知道完整意图，Agent起初只听到想做几项换货；它必须主动把事项收集完整。** 零售政策规定同一订单只能发起一次换货，应在操作前确认全部物品与明细。[[raw/papers/harness/tools/tau-bench.pdf#page=25|App.C.2.1 · pp.25–26]] [[raw/papers/harness/tools/tau-bench.pdf#page=15|App.B.1 · pp.15–17]]

| 阶段 | 实际信息与行动 | 判读 |
| --- | --- | --- |
| 初始权限 | Agent看到政策与API说明；经API查询订单、商品变体；用户指令和参考动作隐藏 | 不是完整需求一次性输入，也不是只补全单个函数调用 |
| 应完成的结果 | 经核实两项偏好与授权，将两个旧物品ID和两个新物品ID合并为一次换货；参考注释给出这一操作 | 正确性依据业务结果；可有不同查询和对话路线 |
| 论文观测的失败 | Agent先单独换键盘，订单变为 `exchange requested`；用户随后提出温控器，第二次调用报非已送达订单不能换货 | 前一次工具成功反而封闭了后续合法操作机会 |
| 结束与验收 | 示例最后转人工；数据库仍只登记了键盘换货，不等于参考的双物品结果 | 工具返回成功、用户说满意、转人工成功都不能代替整题成功 |

逐步证据：[[raw/papers/harness/tools/tau-bench.pdf#page=25|App.C.2.1 · pp.25–30]]；API如何检查状态并写入新状态见 [[raw/papers/harness/tools/tau-bench.pdf#page=13|App.B.1 · pp.13–14]]。表中“封闭后续机会”为本库对该轨迹的解释。

成功例D.2则展示另一面：Agent逐步获知乘客不接受11点前出发，查询一站中转方案，按金卡经济舱政策确定三件免费行李，再拒绝同时用两张旅行凭证，采用250美元凭证加5美元信用卡并取得确认，最后完成255美元的预订。它说明完整任务包含偏好澄清、政策推理与写状态的衔接；这是一条成功示例，不能据此证明全域政策遵循。[[raw/papers/harness/tools/tau-bench.pdf#page=48|App.D.2 · pp.48–53]]

**长程的具体含义：**这里有跨多轮的信息积累、后续依赖和部分不可重复的动作；实验上限是30个Agent动作，包含工具调用和面向用户的回复。该设计能形成上下文内持续执行压力，但“30步上限”“参考写动作数”与实际耗时、全轨迹长度不是同一个量；论文未直接测跨任务学习或长期自主目标维持。[[raw/papers/harness/tools/tau-bench.pdf#page=7|§5 · p.7]] [[raw/papers/harness/tools/tau-bench.pdf#page=9|§5.2、Fig.6 · p.9]]

## 任务从哪里来，哪些现实要求被简化

数据不是来自真实客服会话的随机抽样。作者先受现实业务启发，人工共同设计简化schema、API和政策；再让GPT-4生成采样代码并人工修正；最后人工编写用户场景，用GPT-4-turbo FC反复运行、检查轨迹、修改用户提示，尽量使同一场景有唯一数据库结果。零售每题用超过40次运行检查低成功／零成功题，附录图注为至少40次；这属于构造与质量核查，不应冒充所有模型统一的评测预算。[[raw/papers/harness/tools/tau-bench.pdf#page=5|§4 · p.5]] [[raw/papers/harness/tools/tau-bench.pdf#page=12|App.A、Fig.7 · p.12]]

最终零售115题、航空50题；零售有500用户、50产品、1000订单与15个API，航空有500用户、300航班、2000预订与13个API。选这两域的理由包括易于合成数据、用常识制定政策、可形成多样任务且接近应用。作者未在已读范围报告真实业务频次权重、系统的候选淘汰／去重数量或完整污染核查；不能将165题等同于代表性业务样本。作者也承认用GPT-4-turbo调整用户提示带来curation bias。[[raw/papers/harness/tools/tau-bench.pdf#page=6|§4.1、Table 1 · p.6]] [[raw/papers/harness/tools/tau-bench.pdf#page=10|§6 · p.10]]

**本库分析：**政策保留了身份核验、权限、用户授权、状态转换与支付限制等现实工作逻辑；唯一终态和简化业务规则使自动判分可行，却排除了现实中多个合理结果、偏好变化和复杂服务质量的一部分。API为确定性Python执行，不是让LLM臆测工具返回；但数据库、航班与顾客仍是合成的，不能称为接入真实商家生产系统。[[raw/papers/harness/tools/tau-bench.pdf#page=3|§3 · pp.3–5]] [[raw/papers/harness/tools/tau-bench.pdf#page=15|App.B.1 · pp.15–19]]

## 判分测到了什么，漏掉什么

论文把整题二元奖励定义为

$$r=r_{\mathrm{action}}\,r_{\mathrm{output}}\in\{0,1\}.$$

`r_action`检查最终数据库是否等于参考写动作生成的唯一目标结果；有信息回答要求时，`r_output`检查指定输出。Fig.2例子要求退水瓶且说明退货可省54.04美元、换货可省41.64美元；评分检查这两个数字作为子串出现在面向用户的回答中。**所以“τ-bench只看数据库，完全不看沟通”不准确；“已全面验收沟通和政策遵循”同样不准确。** [[raw/papers/harness/tools/tau-bench.pdf#page=4|§3 Reward、Fig.2 · pp.4–5]]

作者直接给出误放行反例：Agent未取得明确确认就发起退货，依然可能得到 `r=1`。这说明终态约束与过程授权是两个维度。政策要求并不全由工具硬编码：航空某些改签／取消资格须Agent自己判断；零售示例API检查订单状态、物品、支付等，但用户确认主要在说明和政策中要求。[[raw/papers/harness/tools/tau-bench.pdf#page=5|§3 Reward · p.5]] [[raw/papers/harness/tools/tau-bench.pdf#page=13|App.B.1 · pp.13–15]] [[raw/papers/harness/tools/tau-bench.pdf#page=18|App.B.1 · pp.18–19]]

**本库分析：**数字子串存在不保证说明的语义、对应关系或服务态度正确；同义但格式不同的合格回答也可能需要额外处理。这里是对已报告评分规则的覆盖分析，未执行构造攻击，也未证明仓库实现实际出现了这些误判。唯一终态降低了判分主观性，但如果用户模拟偏离预设意图，固定目标可能与当次对话合理结果分离；需要分别核对任务注释、模拟器和verifier，不能只归责模型。[[raw/papers/harness/tools/tau-bench.pdf#page=4|§3 · pp.4–5]] [[raw/papers/harness/tools/tau-bench.pdf#page=9|§§5.3–6 · pp.9–10]]

### 人工验证针对哪一层

| 人的角色 | 论文实际证据 | 不能据此声称 |
| --- | --- | --- |
| 定义需求／出题审题 | 人工设计政策、场景、目标动作，迭代检查低成功轨迹 | 已由真实客户需求分布或独立行业专家验证 |
| 完成任务作基线 | 已读正文与附录未报告受控真人Agent完成率／耗时基线 | 模型已达到或落后于量化人类工作基线 |
| 验收最终成败 | 主要为程序终态与输出规则；已读范围未见对同一批成功／失败终态的独立专家验收一致性、误拒／误放率 | 人工审题等同于最终verifier与人一致 |
| 标注失败原因 | 零售115条轨迹中40条失败，人工找出4条指令错字／歧义并修正；其余36条分类 | 所有失败都来自Agent，或分类比例是跨域普遍因果占比 |
| 检查用户模拟器 | 会议版§5.3在航空比较4种模拟策略，人工归因随机失败轨迹 | 模拟用户已与真人对话分布对齐，或最终评分准确率达96%–98% |

依据：[[raw/papers/harness/tools/tau-bench.pdf#page=5|§4 · p.5]] [[raw/papers/harness/tools/tau-bench.pdf#page=8|§5.2 · p.8]] [[raw/papers/harness/tools/tau-bench.pdf#page=9|§5.3、Table 4 · p.9]]。后两列的限制为本库判读；未报告不等于作者没有做过。

默认用户模型是 `gpt-4-0613`，看到隐藏用户提示和双方完整对话，看不到Agent与工具的交互。会议版另比较直接LLM、ReAct、候选验证、反思修订四种用户策略：固定GPT-4o FC Agent，在航空50题上各运行3轮，再按表中各策略随机抽50条失败轨迹人工归因。Table 4中归于用户的失败占比是2%、2%、4%、4%，对应整体平均成功率36.7%、30.0%、39.3%、40.6%；正文写“小于4%”，与两行恰为4%略有不一致，本页按表保留。[[raw/papers/harness/tools/tau-bench.pdf#page=3|§3 · pp.3–4]] [[raw/papers/harness/tools/tau-bench.pdf#page=9|§5.3、Table 4 · p.9]]

**本库判断：**这提供了“所抽取失败大多不是模拟器错误”的有限支持，比完全未验证模拟器更强；但只抽失败、只有航空与一个Agent，且未报告标注者人数、独立性或一致性，不能估计所有轨迹的模拟器错误率，也不能校准自动评分器的误放行。用户不知政策与用户模型不遵守自身指令是不同原因；作者承认后者的推理、计算、长上下文和遵循能力有限。[[raw/papers/harness/tools/tau-bench.pdf#page=9|§§5.3–6 · pp.9–10]]

## 重复可靠性与实验的可比范围

对每题独立同分布地运行 $n$ 次，其中 $c$ 次成功；论文的无偏估计为

$$\widehat{\mathrm{pass}^{k}}=\mathbb E_{\mathrm{task}}\!\left[\frac{\binom{c}{k}}{\binom{n}{k}}\right],\qquad
\widehat{\mathrm{pass@}k}=1-\mathbb E_{\mathrm{task}}\!\left[\frac{\binom{n-c}{k}}{\binom{n}{k}}\right].$$

前者要求同一题的 $k$ 次**全部成功**，后者只要求**至少一次成功**；$k=1$时二者相同。试验保持任务提示与数据库转移相同，变动主要来自用户／Agent生成；它不是在一个连续会话里得到 $k$ 次重试机会，更不是让系统从 $k$ 个答案里挑最好结果。[[raw/papers/harness/tools/tau-bench.pdf#page=5|§3 Pass^k metric · p.5]]

**本库推导：**若某题真实单次成功率为$p_t$，总体指标分别为 $\mathbb E[p_t^k]$ 与 $\mathbb E[1-(1-p_t)^k]$。不能把全体平均成功率直接取$k$次方替代`pass^k`；任务间难度差异也影响曲线。`pass^k`随$k$下降本身部分来自定义，解释重点是下降幅度、任务异质性及固定模拟条件，不能单凭下降证明某种内存机制是因果瓶颈。

主要协议与结果：

- 主表比较12个模型；主要用原生function calling，政策置于系统提示；Llama-3例外使用文本ReAct，另在OpenAI模型上比较FC／ReAct／Act。不同接口与scaffold条件须保留，不能把全表当纯模型能力排行。每题最多30个Agent动作，主表每题至少3次，Agent温度0、用户温度1。完整模型snapshot、随机种子和所有高$k$曲线的逐模型$n$本次未确认。[[raw/papers/harness/tools/tau-bench.pdf#page=6|§5 · pp.6–7、Table 2]]
- GPT-4o FC的`pass^1`为零售61.2%、航空35.2%，两域等权平均48.2%；**不是将115＋50题按题数加权**。零售`pass^8`低于25%说明此协议下重复稳定完成远弱于偶尔成功；这些是论文时期系统结果，不是当前模型成绩。[[raw/papers/harness/tools/tau-bench.pdf#page=7|§5.1、Table 2、Fig.4 · pp.7–8]]
- 主结果图表未给出可用于独立判断微小名次差异的置信区间／显著性方法；重复尝试不能当成新增独立任务。Fig.6中参考写动作更多的题更难，是跨题相关而非控制长度的因果实验。[[raw/papers/harness/tools/tau-bench.pdf#page=7|Table 2、Figs.3–4 · p.7]] [[raw/papers/harness/tools/tau-bench.pdf#page=9|Fig.6 · p.9]]
- 成本需包括用户模拟。正文报零售每题Agent约0.38美元、用户约0.23美元，却接着写每题运行一轮约200美元；以115题乘0.61美元仅约70.15美元，本次未确认200美元的具体分母或额外成本，不能直接作复现预算。另Table 3的GPT-4o航空有政策起点33.2%与主表35.2%不同，未明确解释；保留差异，不合并为统一受控效应量。[[raw/papers/harness/tools/tau-bench.pdf#page=8|§§5.1–5.2、Table 3 · p.8]]

## 对 Terminal-Bench 定位的反证与保留

S080 §6 p.11将τ-bench列为工具使用基准，随后总体强调自己的专家贡献、多领域长程任务和真实shell，并将其他基准概称为合成环境。**它没有逐项说“τ-bench是单轮题”，因此应修正由分类引出的过强推论，而非替S080制造这句话。** [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

| 比较判断 | τ-bench原文提供的直接证据 | 本库结论 |
| --- | --- | --- |
| 工具使用只测单次调用，未做完整任务 | 动态用户、隐藏意图、确定性API状态、完整成功／失败轨迹 | 这一泛化不成立；τ-bench已经有完整多轮任务。[[raw/papers/harness/tools/tau-bench.pdf#page=3\|§3 · pp.3–5]] |
| 长程依赖是终端基准独有 | 收集全需求后才能执行一次换货；多轮偏好与支付约束 | S080可保留自身更广技术任务与终端操作链的定位，但未证明独占“长程”。[[raw/papers/harness/tools/tau-bench.pdf#page=25\|App.C.2.1 · pp.25–30]] |
| 合成环境就不承担真实工作要求 | 简化模拟仍保留政策、授权、业务状态与沟通约束 | 真实程度有多个维度；生产系统真实性不足与真实需求相关性可以同时成立。[[raw/papers/harness/tools/tau-bench.pdf#page=5\|§4 · pp.5–6]] |
| 终态得分可代表全过程可靠性 | `r=1`仍可能未获授权；`pass^k`另测重复成功 | 两基准均须区分任务终态、过程约束、重复可靠性；不能把平均解决率与`pass^k`互换。[[raw/papers/harness/tools/tau-bench.pdf#page=5\|§3 · p.5]] |

**仍成立的S080增量：**其真实shell承载的软件、系统、科学计算等专家技术任务，与τ-bench两个人工构造的客服业务域不同；τ-bench没有取代这种任务广度、终端产物和专业操作的测试价值。反过来，S080的终端交付并不覆盖τ-bench动态顾客询问与政策授权的全部压力。两篇没有统一任务／模型／预算的横向实验，不能根据各自低分给出总难度排序或“更真实所以更好”的单轴结论。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|S080 · §§1–2 · pp.2–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]] [[raw/papers/harness/tools/tau-bench.pdf#page=5|S086 · §§4–5 · pp.5–7]]

**已整合的澄清：**把“合成／真实”拆为执行是否真实、任务需求是否真实、用户是否真实、样本分布是否代表现实；把“可靠”拆为终态正确、过程合规和重复稳定。这是本库的比较框架，不是论文已验证的新理论或研究缺口。综合见 [[wiki/applications/terminal-bench-comparison|跨基准审视]]；相关入口：[[wiki/applications/Overview|应用与评测]]、[[wiki/harness/verification|验证]]、[[wiki/papers/harness/tools/Terminal-Bench|S080 Terminal-Bench]]。
