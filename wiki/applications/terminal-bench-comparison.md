---
type: topic
created: 2026-10-29
updated: 2026-10-29
sources:
  - "[[raw/papers/harness/tools/Terminal-Bench.pdf]]"
  - "[[raw/papers/harness/tools/SWE-bench.pdf]]"
  - "[[raw/papers/harness/tools/SWE-Lancer.pdf]]"
  - "[[raw/papers/harness/tools/AppWorld.pdf]]"
  - "[[raw/papers/harness/tools/OSWorld.pdf]]"
  - "[[raw/papers/harness/tools/tau-bench.pdf]]"
---

# 读过前作后，Terminal-Bench 还进步在哪里？

**本库结论：有实际增量，但证据支持的是“补充了一组困难、跨技术领域的终端工作与较系统的审查流程”，不是“比既有 benchmark 全面更真实、更有效”。** 真实执行、真实问题来源、结果验收、跨应用和长程交互都已有前作。Terminal-Bench 将这些要素围绕终端技术工作重新组合，其覆盖与使用价值成立；评分有效性、经济价值预测和部署可靠性相对前作更优，尚无直接比较证明。下面按八项原文主张给证据，不给总质量分。

最明确需要收窄的是 §6 对其他基准“合成环境”的概括：OSWorld 运行真实操作系统，SWE-Lancer 在真实容器中允许终端命令；AppWorld 虽然模拟应用，却有真实程序执行和可检验的数据库状态。环境真实性不是一条从“合成”到“真实 shell”就能排出的质量顺序。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]] [[raw/papers/harness/tools/OSWorld.pdf#page=3|S085 · §§2.2–3.1 · pp.3–5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|S083 · §3.1 · p.5]] [[raw/papers/harness/tools/AppWorld.pdf#page=3|S084 · §2 · pp.3–4]]

## 对照对象为什么是这五篇

本轮不是全面综述。五篇均为 S080 §6 点名的工作，参考文献身份见 S080 pp.12–17；这里阅读其原论文，未把 SWE-agent／SWE-Gym 当作 SWE-bench。选文理由是各自能检验一条关键主张，而非下载所有相关工作。固定版本、SHA-256、具体阅读与未读范围登记在唯一来源页。

| 原论文与固定版本 | 它实际测什么 | 本轮最有价值的比较 |
| --- | --- | --- |
| [[wiki/papers/harness/tools/SWE-bench\|S082 SWE-bench]]，arXiv v2／ICLR 2024 标识 | 给真实 issue 和仓库，生成补丁，再运行修复与回归测试 | 真实问题与结果验收已存在；Python 仓库维护的覆盖有限 |
| [[wiki/papers/harness/tools/SWE-Lancer\|S083 SWE-Lancer]]，ICML 2025／PMLR | 完成 Expensify 的工程任务，或选择历史工程方案；关联历史报酬 | 经济价值有更具体的来源锚点；终端不是新出现的接口 |
| [[wiki/papers/harness/tools/AppWorld\|S084 AppWorld]]，arXiv v1／ACL 2024 camera-ready 标识 | 在模拟日常应用中写代码调用 API，改变状态、完成跨应用任务 | 合成带来可控性、状态差分和任务变体，不等于缺乏测量价值 |
| [[wiki/papers/harness/tools/OSWorld\|S085 OSWorld]]，NeurIPS 2024 | 在真实 OS 与应用中经桌面操作完成任务，含跨应用和 CLI | 对“其他环境不真实”的直接反例；GUI 与 CLI 是任务条件差异 |
| [[wiki/papers/harness/tools/tau-bench\|S086 τ-bench]]，ICLR 2025 会议版 | 同时与模拟用户和 API 交互，结合政策完成目标 | 用户澄清、政策与跨尝试可靠性不能由终端平均成功率替代 |

任务定义的直接依据：[[raw/papers/harness/tools/SWE-bench.pdf#page=3|S082 · §2.2 · p.3]]；[[raw/papers/harness/tools/SWE-Lancer.pdf#page=4|S083 · §§2–3.1 · pp.4–5]]；[[raw/papers/harness/tools/AppWorld.pdf#page=5|S084 · §§3.1–3.3 · pp.5–6]]；[[raw/papers/harness/tools/OSWorld.pdf#page=3|S085 · §§2–3 · pp.3–6]]；[[raw/papers/harness/tools/tau-bench.pdf#page=3|S086 · §3 · pp.3–5]]。

主文锁定 [[wiki/papers/harness/tools/Terminal-Bench|S080，arXiv:2601.11868v1]]，研究对象为 **Terminal-Bench 2.0 数据集**。Harbor 是运行框架，Terminus 2 是其中一种被测 scaffold。本文不使用当前在线榜单，也不跨论文排列模型成绩。WebArena／VisualWebArena、科学专项基准本轮未核读；MCPMark／Toolathlon 的已有阅读见 S080 原笔记，此处不将其冒称为 §6 的直接比较对象。

## 八项主张经过反证后剩下什么

下表中的“原主张”是原文的缩写，后两列是**本库分析**；作者的设计目标、实验观察和有条件展望分别处理。

| 编号与原主张定位 | 最强反证或替代解释 | 判断与仍成立部分 |
| --- | --- | --- |
| C1：其他基准使用合成环境，本文使用真实 shell；§6 p.11 | OSWorld 的真实 VM／OS；SWE-Lancer 的容器与终端 | **泛化比较不成立。** 围绕 shell 的技术任务定位仍成立，真实执行并非独占 |
| C2：专家、多样、长程构成独特定位；§§1、6 pp.2、11 | AppWorld 已有多应用依赖；OSWorld 已有跨应用真实工作 | **组合贡献部分支持。** 相对软件维护和消费应用，新增长程技术工作覆盖；未证明所有维度都更广 |
| C3：这些特点确保真实且有经济价值；§6 p.11 | 专家供题不是工作分布抽样；SWE-Lancer 已提供实际历史报酬 | **价值动机合理，“确保”过强。** 专业相关性有依据，劳动市场价值或预测效度未证实 |
| C4：困难任务、较长运行支持长程潜力；§§2.2、2.4、4.1 pp.3、5、7 | 人类估时不是实测；API 次数／运行时间含探索和重复；低分也可含规范／环境误差 | **困难条件内成立，抽象能力结论不足。** 可用于困难终端系统的压力测试，不能独立测出长程规划能力 |
| C5：Specificity／Solvability／Integrity 验证；§2.3 pp.4–5 | 参考解和审查只覆盖有限情况；前作已采用结果与副作用检查 | **质控证据成立，完备性未证。** 不能把“测试当且仅当正确”的审查目标当作已证明的性质 |
| C6：中性 scaffold；模型选择通常更重要；§§3.1、4 pp.6–7 | 简化接口仍含摘要／工具设计；非完整因子对照、不同预算与跨度 | **在已测组合中有观察，一般归因未证。** Terminus 2 提供共同接口，未证明对模型无偏 |
| C7：趋势延续后可能可靠完成大多数明确定义终端任务；§4.2 pp.7–8 | 平均成功、反复成功、工作分布外推是不同问题；τ-bench／AppWorld已有相应区分 | **保留为作者条件性预测。** 历史组合成绩改善成立；部署可靠性未由该趋势验证 |
| C8：ABC 高分和排名体现严谨；App.B.5 pp.27–28、Table 3 p.82 | 开发者自评及参与式审查不是独立效度比较，部分关键项仍缺证 | **流程自查有价值。** 不据此判断总体质量胜过其他基准 |

各项原文及反证的直接定位在下文；“未证实”不等于反面已经成立。尤其 C2 并非作者声称每项设计都是首次，C7 也不是无条件承诺。

### C1–C2：真实 shell 与覆盖，究竟新增了什么

**OSWorld 是实质反例，而非仅标题相似。** 它用 VM 启动 Ubuntu 等真实操作系统，初始化文件和应用，以鼠标／键盘动作操作，再从文件、配置或界面状态验收。其示例经 PyAutoGUI 打开终端、输入 `ffmpeg` 命令提取字幕。不能因 VM、重置或人工造题就称执行环境是虚构的；同理，Terminal-Bench 的容器和人工整理任务也并非整个真实生产工作原封搬入。[[raw/papers/harness/tools/OSWorld.pdf#page=3|S085 · §§2.2–2.4 · pp.3–5]] [[raw/papers/harness/tools/OSWorld.pdf#page=36|App.D.5.1 · p.36]]

SWE-Lancer 的 baseline 已可在 Docker 中浏览仓库、修改文件和执行终端命令。SWE-bench 更早把真实 GitHub issue、仓库与开发者测试组成可执行评价，且允许与参考补丁不同的实现。因而“真实工作来源＋真实执行＋按结果评分”不能被记成 Terminal-Bench 首创。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|S083 · §3.1 · p.5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=2|S082 · §§2.1–2.3 · pp.2–3]] [[raw/papers/harness/tools/SWE-bench.pdf#page=20|App.A.4 · pp.20–21]]

**仍成立的增量是任务集合的落点。** S080 的类别包括软件、系统管理、安全、科学计算、数据和模型训练；软件工程是最大类但非多数。相比锁定 Python 仓库的 SWE-bench，或来自单一 Expensify 产品的 SWE-Lancer，它确实补充了若干技术工作类型。相对 AppWorld 的日常服务和 OSWorld 的桌面操作，则更像能力切面的互补：关注的技术任务不同，不意味着消费服务、视觉定位、人与 agent 协商也覆盖得更多。分类标签本身可能交叉，不能用类别数直接当“广度分”。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|S080 · §2.4、Fig.4 · p.5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=9|S082 · §7 · p.9]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=8|S083 · §4 · pp.8–9]] [[raw/papers/harness/tools/AppWorld.pdf#page=3|S084 · §2.1 · p.3]] [[raw/papers/harness/tools/OSWorld.pdf#page=5|S085 · §§3.1–3.3 · pp.5–6]]

### C3–C4：专业相关、经济价值、难度与长程需要不同证据

Terminal-Bench 从 93 名贡献者的 229 题选出 89 题，依据作者难度估计及审查质量。人工参考解和工作案例使任务动机具体，也支持“存在可行工作流程”；这种有意选题适合寻找前沿系统弱点，但不是现实工作随机样本。作者估计专家／初级工程师耗时，未等同于真人完成实验。任务数 89 与 Table 1、Table 2 的 74 口径仍未解释，不能据此推算全行业耗时或价值。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|S080 · §2.2 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=5|§2.4、Table 1 · p.5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=81|Table 2 · p.81]]

**SWE-Lancer 使“经济价值”有了更具体的可比参照。** 它关联实际支付给自由职业工程师的历史报酬，强于仅由任务专业性推断付费意愿；但其 benchmark payout 也不是模型现实净收益。论文承认单公司／平台覆盖限制，且成本分析的多次尝试情境假设可以快速识别正确解，现实验收可能很慢；私有 IC 子集还将历史 bug 以不同等价方式重新植入。结论因此是“经济联系更可追溯”，不是“SWE-Lancer 已完整测出劳动市场价值”。[[raw/papers/harness/tools/SWE-Lancer.pdf#page=2|S083 · §1 · p.2]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=8|§§3.6–4 · pp.8–9]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=28|App.A.11 · p.28]]

**困难也不是单一刻度。** S080 的运行时间和调用次数显示环境可以承载长交互，但既含必要步骤也含排错、重复和接口成本；其 Fig.7 对比作者预测与 Terminus 2 的经验难度，并没有隔离领域知识、规划深度和执行稳定性。OSWorld 有真人操作基线，但被试、界面和任务不同，也不能拿它的人类耗时去换算 S080 任务更难多少。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=7|S080 · §§4.1–4.3 · pp.7–9]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=21|App.A.2、Fig.10 · p.21]] [[raw/papers/harness/tools/OSWorld.pdf#page=7|S085 · §3.4 · p.7]]

本库的正面判断是：只要选题可解、验收合理，有意困难的集合就能支持系统区分和失败诊断；无需先证明劳动市场代表性才有价值。要进一步声明抽象“长程能力”提高，则还需按领域知识、动作依赖和预算控制的证据。本轮没有运行这类实验。

### C5：更开放的环境，不自动带来更好的判分

以三种具体任务看评价对象：S080 的 COBOL 迁移例要求交付 Python 程序并保留输入输出行为；SWE-bench 检查新补丁通过修复测试且不破坏原本通过项；AppWorld 的购物／支付任务检查预期数据库变化，并约束不应改变的状态。这些都属于结果验收，差别在“正确结果”被形式化到多细，而非有没有运行代码。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|S080 · Fig.2 · p.3]] [[raw/papers/harness/tools/SWE-bench.pdf#page=21|S082 · App.A.4 · p.21]] [[raw/papers/harness/tools/AppWorld.pdf#page=5|S084 · §3.2、Figs.2–3 · pp.3、5–6]]

AppWorld 把变化分成必须发生和允许发生两类，以数据库 diff 检查是否有额外改动，并用场景变体检查不同初态下能否完成。模拟和可控数据库是这种审查的助力；但 API 代码覆盖率不是任务判分器的语义完备性，具体断言仍须审。OSWorld 则明确承认完整计算机环境很难高效发现所有副作用，现有评价较少覆盖不必要破坏。这是**可控性与开放性的设计取舍**，不能把开放环境的丰富度当成 verifier 天然优势。[[raw/papers/harness/tools/AppWorld.pdf#page=4|S084 · §2.2 · p.4]] [[raw/papers/harness/tools/AppWorld.pdf#page=6|§§3.2–3.3 · p.6]] [[raw/papers/harness/tools/OSWorld.pdf#page=49|S085 · App.E · p.49]]

Terminal-Bench 的贡献是把双向规范检查、参考解／空操作、人工轨迹审查和对抗作弊检查组合为明确流程；值得复用。可是原文的“所有可接受终态都通过、所有不可接受终态都失败”是审查标准。参考解通过只证明一个见证，找出若干漏洞也不是证明没有其他漏洞。原文自身承认缺陷影响尚未量化、存在非确定性，因而目前不能确定这些投入究竟把误放行／误拒绝降低到多少，更不能断言低于五个前作。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|S080 · §2.3、Fig.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=25|App.B.2–B.5 · pp.25–28]]

**人工证据必须对准同一对象。** S080 的人工一致性主要校准失败诊断器；SWE-Lancer 的 99% 是工程方案选择标签的复核，不是所有 IC 工程产物的验收准确率；OSWorld 的人类得分是解题基线；τ-bench §5.3 的人工检查针对模拟用户造成的失败，不是完整政策遵循判分。不能把这些数字拼成 verifier 排名。反过来，没有统一人工评分实验也不自动否定确定性测试：需求对应、反例测试和覆盖审计同样是有效证据。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=9|S080 · §§4.4–4.5 · pp.9–10]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=4|S083 · §2 · p.4]] [[raw/papers/harness/tools/OSWorld.pdf#page=7|S085 · §3.4 · p.7]] [[raw/papers/harness/tools/tau-bench.pdf#page=9|S086 · §5.3、Table 4 · p.9]]

τ-bench 还提供一个明确边界：终态和必需回答都正确，仍可能在未取得用户确认时操作。论文自己说明其 reward 并不足以保证整段交互合规。这个反例说明“对同一最终产物评分一致”与“整个工作过程可接受”也要分开；它不证明 S080 的具体任务已存在同类漏洞。[[raw/papers/harness/tools/tau-bench.pdf#page=4|S086 · §3 Reward · pp.4–5]]

### C6–C7：组合成绩提高，不等于一般归因或可靠部署

S080 主榜为每个模型选最高表现 scaffold；Terminus 2 内部也含终端输出捕获和上下文摘要，因此只是相对简化的共同接口。作者用 Codex CLI 内两个模型的大跨度差异，与 Gemini 2.5 Pro 的两个 scaffold 差异作例，提出模型通常更重要。原表也显示同一 GPT-5 在 Codex CLI 与 Terminus 2 上存在明显差异；这些观察支持“两个因素都可改变表现”，不能由选定跨度推出普遍优先级。本库不重做显著性检验，也不把不同组合视为等预算。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=3|S080 · Fig.1 · p.3]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|§§3–4 · pp.6–7]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=51|App.F · p.51]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=81|Table 2 · p.81]]

五篇前作的评分与预算也不相同：SWE-bench 原始实验主要是检索＋补丁生成；SWE-Lancer 有工具调用与时间限额、主结果单次尝试；OSWorld 的原始 baseline 限 15 步；AppWorld 按方法配置迭代并报任务／场景完成；τ-bench 限 30 动作且多次试验。相同模型名称也不足以让这些成绩可直接排名，何况模型年代、版本、可见信息和环境均有差异。[[raw/papers/harness/tools/SWE-bench.pdf#page=4|S082 · §4 · pp.4–5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=16|S083 · App.A.5 · p.16]] [[raw/papers/harness/tools/OSWorld.pdf#page=7|S085 · §4.1 · p.7]] [[raw/papers/harness/tools/AppWorld.pdf#page=7|S084 · §4 · pp.7–8]] [[raw/papers/harness/tools/tau-bench.pdf#page=7|S086 · §5 · p.7]]

**“可靠”需要另一个指标。** τ-bench 的 `pass^k` 要求同一任务的 k 次独立试验全部成功；`pass@k` 是至少一次成功；AppWorld 的 SGC 要求同一场景的所有变体成功。后者测试不同条件的一致性，并非重复采样同一题。S080 报告重复运行的平均解决率与区间，不能把它当作上述任一指标。其趋势图为每个模型选择最佳 harness，再从这组困难题外推到“大多数明确定义终端工作”，仍缺任务分布和可靠性两层依据。[[raw/papers/harness/tools/tau-bench.pdf#page=5|S086 · §3 Pass^k · p.5]] [[raw/papers/harness/tools/AppWorld.pdf#page=6|S084 · §3.2 · p.6]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=7|S080 · §4.2、Fig.6 · pp.7–8]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=21|App.A · p.21]]

### C8：清单高分是自查记录，不是总体胜出的实验

S080 附录报告 ABC 排名靠前，同时说明 ABC 作者参与开发，部分问题在协作中修复；这支持流程改进，不能当作独立审查盲测。Table 3 的若干条目得分与“是否有完整结果效度证据”也不是同一问题，例如未量化不可避免缺陷的影响、没有私有测试集。本文没有独立核读 ABC 原论文或复算榜单，所以仅评价 S080 对该清单的使用，不否定整个 ABC 方法。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=27|S080 · App.B.5 · pp.27–28]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=82|Table 3 · p.82]]

污染也属于取舍：Terminal-Bench 的公开任务、参考解和联网运行，方便开放研究但留下训练／检索泄漏风险；canary 不是防故意污染保证。SWE-Lancer 限制联网并设私有改造子集，缓解部分风险，却增加外部独立复核限制。没有一种安排凭设计名称就能宣称污染已解决。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=10|S080 · §5 · pp.10–11]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=28|App.B.5 · p.28]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=5|S083 · §3.1 · p.5]] [[raw/papers/harness/tools/SWE-Lancer.pdf#page=28|App.A.11 · p.28]]

## 最后如何评价它的进步

| 进步类型 | 本轮结论 | 成立范围 |
| --- | --- | --- |
| 新增覆盖 | **有直接支持** | 相对 SWE-bench／SWE-Lancer，扩展到多种非软件维护的终端技术工作；相对 AppWorld／OSWorld 是不同任务切面 |
| 设计取舍 | **有明确价值，非单向升级** | shell／容器便于技术任务和工具组合；模拟应用便于控制与状态差分；GUI／用户交互另有测量目标 |
| 质量控制与基础设施 | **有可复用贡献** | S080 的审题、失败轨迹和对抗审查流程；Harbor 的统一格式与多 agent 运行支持。未实测部署效率或证明同类首创 |
| 实证优越 | **仅限自身条件内的系统观察** | 基准仍能区分所测组合并显示未完成任务；没有控制实验证明比五个前作更能预测实际工作表现 |
| 专业验收、经济收益、一般可靠性 | **部分动机支持，关键外推未证实** | 仍需独立终态审查、目标工作分布与跨次／跨变体可靠性证据 |

上表是前述证据的综合判断。Harbor 的具体范围来自 [[raw/papers/harness/tools/Terminal-Bench.pdf#page=6|S080 · §3.4 · p.6]]；它的框架贡献不等于 Terminal-Bench 2.0 的任务覆盖，更不等于 Terminus 2 对所有模型公平无偏。

**最能改变当前判断的下一项证据：独立专业验收审计。** 对固定版本 Terminal-Bench，按任务领域和现有判分成败分层抽取真实产物／终态，纳入边界与可疑取巧解；让未参与出题的适任评审者先按公开任务需求盲评，再与 verifier 对照，并保留人工分歧。分别估计误放行、误拒绝及它们是否改变系统排序，单列环境故障。若大部分所谓能力失败实际来自规范／测试问题，本文对其“困难技术任务诊断价值”的正面判断就应下调；若审计误差低且跨系统稳定，则可加强信任。要声称**优于前作**，仍须在匹配目标与抽样规则的前作产物上实施对应审计，不能只审 S080 就得出比较结论。这是实验建议，本轮未执行。

之后才是现实工作预测：在独立抽取、与目标用户相关的新工作任务上，检验该分数是否比现有指标提供额外预测信息，并控制系统与预算。此项目前属于证据需求，不是已经确认的新研究缺口。

## 阅读与维护边界

五篇对照均实际读取正文及与判断有关的附录，具体范围以唯一页为准；主协调者另外回读决定性页，并视觉核对关键公式、流程和实例。没有运行 benchmark、复现实验或审完每个任务源码；没有借代理共识增加证据权重。τ-bench 使用最终取得的 ICLR 2025 会议版，包含 §5.3 模拟用户错误分析，不能沿用早期 v1 的缺项判断。

本页是跨论文综合入口，不替代 [[wiki/papers/harness/tools/Terminal-Bench|S080 唯一笔记]] 和五份来源页。返回 [[wiki/applications/Overview|应用与评测]]；验证对象的区分见 [[wiki/harness/verification|验证]]；选文、版本和验收过程见 [[maintenance/research/2026-10-29-terminal-bench-review|本轮维护记录]]。结构检查与 Obsidian 内显示分别验收，应用未测。
