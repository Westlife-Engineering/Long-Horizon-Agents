---
type: paper
source_id: S083
primary_direction: harness/tools
related_directions:
  - harness/verification
created: 2026-10-29
updated: 2026-10-29
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/SWE-Lancer.pdf]]"
---

# SWE-Lancer：真实付费来源、端到端验收与经济价值代理

**一句结论：**SWE-Lancer 在受限 Docker 环境中，用真实历史付费软件任务及其改造任务评价“模型＋scaffold”的补丁交付和方案选择；真实付款与真实执行环境有直接依据，但收入指标是历史赏金加权成绩，工程师审题也不能替代对模型产物的独立验收。它足以限制“其他 benchmark 都是合成环境、缺少经济价值”的泛化，不能推翻 Terminal-Bench 跨专业终端任务的覆盖增量。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=2|S083 · §1、Figs.1–2 · pp.2–5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=28|App.A.11 · p.28]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

## 身份、版本与阅读范围

- **标题与作者：**SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?；Samuel Miserendino、Michele Wang（共同第一作者）、Tejal Patwardhan、Johannes Heidecke。
- **锁定版本：**ICML 2025，PMLR 267:44412–44450，会议日期 2025-07-13 至 2025-07-19；[PMLR 官方条目](https://proceedings.mlr.press/v267/miserendino25a.html)、[官方 PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/miserendino25a/miserendino25a.pdf)，访问日期 2026-10-29。OpenReview ID 为 `xZXhFg43EI`，直接下载返回 HTTP 403，因此从会议出版方的官方仓库获取；不将搜索摘要中的“1,500+”作为本文版本数据。arXiv 身份 `2502.12115` 已作导航核对，本次未另取 arXiv 版本，会议论文 DOI 未确认。
- **原件：**[[raw/papers/harness/tools/SWE-Lancer.pdf|39 页会议 PDF]]，SHA-256 `54EDDA990A407F1FE1E945018F1C2710D469E55077A0272D313B33DA11CB65F9`。先递归身份与全 Raw PDF 哈希查重，再从临时下载件原样复制；哈希一致。官方 URL 的 `main` 可变，本页证据锁定于此哈希保存件。
- **实际阅读：**2026-10-29 读取正文 §§1–6、Impact Statement（PDF pp.1–10），附录 A.1–A.8（pp.13–20）、A.9–A.12（pp.20–29）、A.13 两类示例提示（pp.29–37）、A.14–A.15（pp.37–39）；参考文献作身份定位，未追读其引用论文。关键原页视觉核对 p.2 Figs.1–2、p.7 Table 1／Fig.10、p.16 Fig.12／A.5–A.6、p.20 A.9、p.28 A.11／Table 6。PDF 内印刷页码与 PDF 页序一致；PMLR 卷内书目页码另为 44412–44450。
- **比较回读：**S080 本地固定 v1 的 PDF p.2 §1／§2.1、p.11 §6；本次没有运行 benchmark、检查官方实现、下载任务数据或复现实验。论文的测试覆盖宣称不等于代码审计结果。
- **归属：**主归属 `harness/tools`，作为可执行软件任务评测；任务评分与人工核查交叉 `harness/verification`。本轮已整合至 [[wiki/applications/terminal-bench-comparison|跨基准审视]]，验收范围见页末。

## 测量价值：真实付款锚定了什么

**原文陈述：**任务来自 Expensify 开源仓库、在 Upwork 发布、由付费贡献者实际完成；赏金是历史实际付款，不是作者估算。IC SWE 要修补程序，SWE Manager 要从真实投稿方案中选择历史获选者。这给“任务确实有人愿意付钱解决”提供了比专家觉得有用更具体的锚点。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=2|§1 · p.2]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|§2.2 · p.5]]

**本库分析：**测量适合观察选定软件外包任务上的自主交付与技术判断；不能据总分估计所有软件工作、当前市场收入或劳动替代率。评分中的“赚到钱”是**通过后计入历史赏金**，并没有模型真正签约、交付获客户付款的部署实验；Manager 得分也不是模型履行了管理岗位的全部职责。§3.6 的成本分析另算模型 API 费用与失败后的人工回退，承认历史价格可能不适用于当前、验证可超过 24 小时；故赏金、净收益、实时验收成本是不同量。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=4|§2.1 · p.4]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=8|§3.6、§4 · pp.8–9]]

“26 天解决一题”是 GitHub 从开题到关闭的日历时间，包含讨论等待，不是工程师连续工作时间，也不是 Agent 的依赖链长度；Diamond IC 平均改 2 个文件、69 行同样只是任务规模代理。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=3|§1 · p.3]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=29|App.A.12、Tables 8、10 · p.29]]

## 一题怎样走完：离线下载不应打开新标签页

论文给出的 IC 实例价值 $500：用户 A 给 B 发附件，B 离线后打开附件并点下载；预期为禁用下载按钮，实际却打开新标签页。问题注明 MacOS Chrome／Safari、版本 1.3.58-0 和复现步骤。以下将该实例与通用评测协议连成流程，不冒充本次执行记录。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=29|App.A.13 · pp.29–30]]

| 阶段 | 被测系统获得什么、做什么 | 最终含义 |
| --- | --- | --- |
| 输入与环境 | 问题标题、原始描述、赏金和问题修复前的仓库快照；预装依赖的 Docker，关闭互联网，移除 Git remote 与未来提交 | 可检查真实代码，不能网上找答案或向维护者追问 |
| 调查与修改 | scaffold 允许浏览代码、编辑文件、运行终端命令；修改下载按钮／离线处理相关逻辑 | 指令要求交付代码，不能只留建议或 TODO |
| 调试反馈 | 调用 `user-tool` 后，Playwright 模拟用户操作，留下文字轨迹、HTML 快照及截图文件；模型可反复调用 | **没有最终成败标签**；主实验模型不读取图像，只能使用文本反馈 |
| 交付与验收 | Agent 结束后应用补丁，运行模型不可见的全部对应 E2E 测试 | 全通过才计成功并计入该题赏金；模型自称完成不算成功 |

流程依据：[[raw/papers/harness/tools/SWE-Lancer.pdf#page=3|§2 · pp.3–5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=16|App.A.5 · p.16]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=19|App.A.8 · p.19]]。**教学反例：**若只避免新标签页却仍允许离线下载按钮处于可点击状态，就可能没有满足题面；论文未展示本题实际测试代码，本次不能保证该反例一定被现有测试捕获。

Manager 是另一条评测路径：给问题、修复前仓库和至少两个方案，可读代码，但不要求实现补丁；写出 `manager_decisions.json` 的方案 ID，再与历史经理选择对照。它是对**方案选择结果**评分，不是 IC 端到端功能测试。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=4|§2 · p.4]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=20|App.A.8 · p.20]]

## 来源筛选、规模与改造边界

| 会议版集合 | IC SWE | Manager | 总计与历史金额权重 |
| --- | --- | --- | --- |
| Full | 764／$414,775 | 724／$585,225 | 1,488 任务，$1,000,000 |
| Diamond 公开集 | 237／$236,300 | 265／$264,500 | 502 任务，$500,800 |
| 私有 holdout | IC 金额 $178,475 | 其余 Manager 金额 | 合计 $499,200；IC 包含工程师改造环境 |

前两行直接来自 [[raw/papers/harness/tools/SWE-Lancer.pdf#page=7|Table 1 · p.7]]；第三行来自 [[raw/papers/harness/tools/SWE-Lancer.pdf#page=28|App.A.11 · p.28]]，不另把“1,400+”或“1,500+”摘要概数当成另一份已读任务集。

筛选要求开源、明确付款、历史已解决、题意足够清晰且原 PR 在本地确实修好；Manager 还要求至少两个充分说明的提案。100 名专业工程师参与评审，正文说 IC 三位、Manager 两位；高于 $5,000 的 IC 由十位有经验工程师检查环境和覆盖。A.6 又泛称每题至少三位，**人数口径存在正文／附录差异，不擅自合并成所有任务统一三人独立盲审**。清晰性和测试覆盖 rubric 均只接受多数人评 0 的题；论文未给完整候选数、各阶段剔除率和 Diamond 随机抽样设计，因此“unbiased／representative”保留为作者主张。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=3|§1 · p.3]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|§2.2 · p.5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=16|App.A.6 · pp.16–17]]

**不能把 1,488 个任务理解成 1,488 个互不相关的原始历史问题。** 同一 GitHub issue 可派生 IC 与 Manager；A.11 还明确把私有 IC 的题意和测试固定，让熟悉仓库的工程师以不同但等价方式重注入 bug。它仍以真实需求为基础，但执行初态含人工改造；模型结果的有效独立样本单位不能仅按任务总数默认。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|§2.2 第3步 · p.5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=28|App.A.11 · p.28]]

覆盖有明显集中：Diamond IC 的 176/237 属客户端逻辑、41/237 属 UI/UX，208/237 是 bugfix；基础设施／DevOps 为 0，Full 也仅有 3 个 Manager 任务涉及该类。单公司、单仓库、单平台带来相关性及外推限制。作者明确承认不能覆盖从零开发和更广泛全职软件工作。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=28|App.A.12、Tables 6–7 · pp.28–29]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=8|§4 · pp.8–9]]

## 判分可信性：工程师参与了哪一层

**IC 的直接证据是测试构造与检查。** 专业工程师手写 Playwright E2E，以登录、上传、跨账户操作等完整用户流程检查补丁；三轮验证涵盖质量、覆盖与公平，另自动检查修复状态通过、破损状态失败。相比只看局部函数，这种测试能发现跨组件行为问题；但正确历史补丁通过、原 bug 失败，并不能证明所有正确替代解通过、所有错误补丁失败。A.6 rubric 的“覆盖所有可能解”是工程师评分目标，不是形式证明。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=3|§1 · p.3]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=17|App.A.6–A.7 · p.17]]

**Manager 的 99% 是另一层证据。** §2 报告额外工程师验证与历史获选方案达 99% agreement；这支持标签与工程师复核较一致。但本次已读范围未报告该验证的分母、抽样、盲评、分歧处理或区间，更没有把它作为 IC 模型补丁逐题人审的一致率。历史经理可能在多个技术上可行方案中做权衡，匹配历史选择不是证明所有其他方案无效。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=1|§1 · p.1]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=4|§2 · p.4]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=13|App.A.3 · p.13]]

**需要保留的具体张力：题面与后续需求是否一致。** A.9 的邮编案例称：最初问题是输入逗号没有报错，而 E2E 还依据 GitHub 讨论检查国家特定格式、无邮编国家等完整范围；o1／Claude 修好所述逗号问题仍被判失败。另一方面 A.6 的清晰性评审要求只看 issue／代码／文档，不读下方评论；IC 提示模板也没有 Manager 那样显式提供全部候选方案及讨论。故这里存在**测试范围是否超过可见要求的风险**。论文自身足以提出核查问题，尚不足以直接裁定误拒：有些要求可能由已有代码、文档或题面附件表达，且模型改动也可能破坏既有功能。要裁定需逐题检查确切输入、初态、测试与补丁，本次未做。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=16|App.A.6 · pp.16–17]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=19|App.A.8–A.9 · pp.19–22]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=25|App.A.9 · pp.25–26]]

**当前证据状态：**有专业测试构造、原始修复对照和 rubric 审核；未在已读正文／附录发现以独立现实验收者对同一批模型补丁逐题盲评、估计误放行／误拒绝的系统性研究。A.7 用另一基准的作弊个例论证 E2E 较抗投机，没有提供 SWE-Lancer 本身的系统对抗攻击成功率；“更难作弊”可以是设计理由，不能据此称不可攻破。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=17|App.A.7 · p.17]]

## 比较协议、统计与结果边界

主实验为 GPT-4o `gpt-4o-2024-08-06`、o1（High；精确快照未确认）、Claude `claude-3-5-sonnet-20240620`，基本 scaffold 相同；IC 主实验均启用 user tool，Manager 任务不适用该工具。A.5 规定每 rollout 最多 100 次工具调用、3 小时、temperature 1.0；除 pass@k 实验外每题一次 rollout。图像／视频输入不支持，user tool 保存截图不等于模型看到了截图。A.4 p.15 的比较文字却称 GPT-4o 能摄入截图，与 §5／A.5 冲突；本页按主设置限定，保留冲突而不擅自修订。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|§3.1 · p.5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=9|§5 · p.9]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=15|App.A.4–A.5 · pp.15–16]]

| Diamond 主实验（IC 启用 user tool；Manager 不适用） | IC pass@1 | IC 赏金加权 earn rate | Manager pass@1 |
| --- | --- | --- | --- |
| GPT-4o | 8.0% | 6.0% | 37.0% |
| o1 High | 16.5% | 12.1% | 41.5% |
| Claude 3.5 Sonnet | 26.2% | 24.5% | 44.9% |

数据：[[raw/papers/harness/tools/SWE-Lancer.pdf#page=7|Table 1 · p.7]]。**解释：**计数成功率与金额加权率回答不同问题；同一模型在 Full 与 Diamond 的任务分布也不同。主榜未给逐任务配对差值的不确定性，p.5 脚注明言单次运行可有显著波动；不把小差距当作已证实优势，更不和 S080 的不同年代模型／任务／harness 成绩比较高低。

§3.3 的 pass@k 是 k 次中至少一次成功的估计，不能当成模型自己可靠选出正确补丁；§3.6 五次运行的成本分析另假定可快速知道成功后停止、失败交人工。o1 五次机会后节省 33.5% 的结果依赖该选择与回退条件，只计 API 等设定成本，不等于端到端部署净收益；正文给 API 成本的 95% 区间，不是主榜成功率的区间。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=6|§3.3 · p.6]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=8|§3.6 · p.8]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=37|App.A.14 · p.37]]

增加 o1 reasoning effort 使 Diamond IC pass@1 从 9.3% 到 16.5%，说明在此任务与 scaffold 下增加测试时计算可改善结果；移除 user tool 时 o1 为 13.1%，GPT-4o 仍为 8.0%，不能把工具使用叙述等同于所有模型都获益。论文对“定位快、根因理解弱”的分析来自所选轨迹，未给可推广的随机诊断样本及独立标注一致性；开源模型附录也明确仅一 seed、默认 scaffold 可能 elicitation 不足。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=7|Table 1、§3.5 · pp.7–8]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=20|App.A.9 · pp.20–28]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=38|App.A.15 · pp.38–39]]

## 对 Terminal-Bench 哪些说法构成反证，哪些仍成立

S080 §6 先列 SWE-Lancer 为软件工程基准，再强调专家贡献、跨域长程任务与真实 shell；它没有逐项宣称 SWE-Lancer 没有真实付款，也没有声称首先发明终态判分。本表限制的是 §6 的宽泛措辞及可能的过度解读，不把未说过的“首创”强加给作者。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

| 待判断命题 | 本次原文核查后的结论 |
| --- | --- |
| 其他基准是合成环境，真实 shell 是区别 | **作为对 SWE-Lancer 的概括不成立。** 它在真实 Docker／终端执行代码并用真实应用浏览器流程测试；但私有 IC 初态有人工重注入。因此应分开任务来源、环境真实性、初态改造，不能用一个“synthetic”概括。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=5\|§3.1 · p.5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=28\|A.11 · p.28]] |
| 专家出题即可确保经济价值，构成独有优势 | **不能如此推导。** SWE-Lancer 已有历史真实付款锚点；S080 专家来源支持相关性，但不自动证明市场价值或覆盖。S083 的金额同样不是部署收入或净利润。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=2\|§1 · p.2]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=8\|§3.6 · p.8]] |
| 终态／产物验收是 S080 独有增量 | **不成立，但这不是 S080 明说的首创主张。** SWE-Lancer 已在补丁执行后按 E2E 功能验收，不要求复现人类操作序列；S080 将此类结果驱动设计用于更广的容器状态任务。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=2\|Fig.1 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=2\|S080 §2.1 · p.2]] |
| S080 扩展到软件工程之外的专业终端工作 | **仍有支持。** SWE-Lancer 的单仓库客户端／UI／bugfix 集中和缺少基础设施任务与此增量相容；“full-stack 多类别”不等于科学计算、系统管理等跨专业广度。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=28\|Tables 6–7 · pp.28–29]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=2\|S080 §§1–2 · p.2]] |
| 专家验证过的 E2E 即代表真实验收 | **两篇都必须继续限定。** SWE-Lancer 提供强于空泛真实性口号的质量检查，也留下可见需求／完整讨论范围的张力；这支持 S080 对 specification 与测试一致性单列审查的必要性，不能宣称哪方 verifier 已更准确。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=20\|A.9 · pp.20–22]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11\|S080 §7 · p.11]] |

## 主题落点与交接

- [[wiki/applications/Overview|Application]]：真实任务来源、执行环境与部署外推分开；经济价值有历史付费锚点，但不把加权 benchmark 分数写成实际收入。
- [[wiki/harness/verification|验证]]：工程师出题／审测试、历史方案选择复核、模型产物独立验收属于不同证据层；邮编案例保留需求范围待查，不能直接定性误判。
- [[wiki/papers/harness/tools/Terminal-Bench|S080 唯一页]]：收窄 §6 真实／合成对立，保留跨专业终端覆盖的实质增量。

以上落点已由主线程整合，综合见 [[wiki/applications/terminal-bench-comparison|跨基准审视]]。主协调者回核 pp.2、4–5、8–9、16、20、28，并视觉检查 p.2；Raw 哈希和本页链接／表格格式纳入本轮统一检查。Obsidian 应用内显示未测，benchmark 未复现。
