# B：训练范式与动向

2026-10-28；独立首稿。尚未读取A／C首稿，未进入交叉审查。本稿从共同S001证据和新增S077出发，目标是准备与学长交流的问题，不把待澄清之处标成研究空白，也不提出解决方案。

## 六个宏观问题（独立首稿）

### B1．Agentic RL 相比推理模型后训练中的 RL，最实质的变化发生在哪里？

**背景／理由：**S001把学习对象从单次回答扩展到交互轨迹；R1主要在一次输出中展开推理，也明确保留工具使用和软件工程训练限制。二者可以共享GRPO等算法，但Agent的动作会改变随后看到的环境和状态，难点未必只是输出更长。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=47|S001 §5.5 · pp.47–48]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=10|S077 §6 · pp.10–11]]

**追问：**在您的经验里，最容易让原来的推理RL配方失效的是交互状态、反馈延迟，还是环境本身的变化？

### B2．说“RL带来了能力增长”，我们具体想区分哪几种增长？

**背景／理由：**R1-Zero既提高解题正确率，也增加推理长度和反思词；但训练中调整过长度上限，词频本身也不能确认新的推理机制。由此可以区分更稳定地用出已有能力、学到更好的策略组合，以及进入原来很难达到的任务范围，而不先规定哪一种才算“真能力”。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=3|S077 §2.1–2.3 · pp.3–5]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=38|C.2 · pp.38–39]]

**追问：**哪一种现象会让您相信增长能迁移到新任务，而不只是当前题目上更会分配思考预算？

### B3．SFT、RL和OPD的分工，应该由训练阶段决定，还是由可获得的监督决定？

**背景／理由：**R1正式配方交替使用SFT和RL；它的小模型蒸馏是固定数据上的SFT，并非OPD。S001的OPD则围绕学生自己到达的状态提供指导。因此不能把三者简单排成先后升级，也不能把“有教师”与“有奖励”看成必然互斥。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=6|S077 Fig.2、§3 · pp.6–8]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=60|F · pp.60–62]] [[raw/surveys/Towards Long-Horizon Agents.pdf#page=52|S001 §5.6 · pp.52–53]]

**追问：**当教师质量、验证器可靠性和交互成本同时受限时，您通常先依据什么判断哪种训练信号更值得投入？

### B4．我们感觉“业界越来越偏向RL”，究竟是在说公开叙事、训练配方，还是实际资源投入？

**背景／理由：**近期Kimi K3.1 Pro官方说明强调扩大的后训练计算与多领域联合RL，DeepSeek-V4.1-Flash-1017说明也点名带自反馈的RL。它们足以说明部分团队公开重视该路线；两份发布说明不足以估计全行业计算／人力占比，更不能推出SFT或预训练正在被替代。[Kimi，2026-10-24，Advancing the Frontier of Open Intelligence](https://www.kimi.com/en/blog/kimi-k3-1-pro)；[DeepSeek，2026-10-17，Build complete projects from scratch](https://api-docs.deepseek.com/news/news261017/)。

**追问：**如果把“训练模型的算力”与“构造环境、验证器和高质量数据的人力”分开看，您观察到的投入重点还是RL本身吗？

### B5．当RL扩展到长期任务时，当前最先卡住的通常是什么？

**背景／理由：**S001同时讨论信用分配、稳定更新、采样与交互结构；R1曾因软件工程评估耗时而限制相关RL规模。近期Kimi说明又把沙箱、rollout调度和环境质检与RL框架一起列出。算法、可用经验和训练系统可能相互限制，不能从最终分数直接读出瓶颈。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=47|S001 Fig.12、§5.5 · pp.47–52]] [[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=11|S077 §6 · p.11]]；[Kimi官方说明，同上节](https://www.kimi.com/en/blog/kimi-k3-1-pro)。

**追问：**在您接触的任务中，哪个限制一旦缓解，最可能改变整个训练方案，而不是只带来小幅提速？

### B6．怎样判断训练后的模型更适合长期做事，而不只是某套系统的分数更高？

**背景／理由：**R1的SWE结果采用Agentless，近期官方Agent评测也明确不同harness、轮数或时间预算；同一模型的能力会和外部流程共同决定结果。最终成功率重要，但仍需理解成本、错误后继续执行及跨环境表现，否则难判断增长来自哪里。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=40|S077 D.1 · p.40]]；[Kimi官方说明，Footnotes／Agentic benchmarks](https://www.kimi.com/en/blog/kimi-k3-1-pro)。

**追问：**如果只能保留少数几类评价，您最希望它们揭示哪种容易被总成功率掩盖的能力或退化？

## 核读与检索记录

### 学术正文预算

- 候选论文实际筛选 **1/4**：DeepSeek-R1，原始身份为 arXiv:2501.12948，当前v2（2026-01-04），v1（2025-01-22）；选择理由是直接核对推理RL、正式产品配方与离线蒸馏的分工。未把搜索结果列表中出现的其他论文升级为筛选对象或已读来源。
- 核读 **1/1**：[[wiki/papers/optimization/reinforcement-learning/DeepSeek-R1|S077唯一页]]，86页版本，实际阅读及原页核对范围见该页。Raw固定为 `raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf`，SHA-256 `b191b0a365a64b4ab2791d117069ed17a2933d03554a662ced58b37df52018f4`。未下载任何额外附件／源码。
- 共同S001回核重点：p.37整章入口，pp.43–48的预／中期训练、SFT及RL入口，pp.50–55的更新、采样、OPD、自我演化；重要判断只引用实际核读段落。已有主题前半用于定位；没有把其原论文比较当成本轮新核读证据。

### 近期官方说明与使用边界

检索日期2026-10-28，渠道web搜索／官方网页。实际查询词：`site.qwen.ai 2026 reinforcement learning agentic post training`；`site.kimi.com blog 2026 reinforcement learning agentic`；`site.z.ai blog 2026 reinforcement learning GLM`；`site.qwen.ai QwenGyre October 12 2026`。搜索摘要仅用于找官方入口；没有读取其他论文全文。

| 说明 | 结果与位置 | 本稿用途和限制 |
| --- | --- | --- |
| [Kimi K3.1 Pro Tech Blog](https://www.kimi.com/en/blog/kimi-k3-1-pro)；[官方目录](https://www.kimi.com/en/blog/)标2026-10-24 | 完整网页可读；重点为“Advancing the Frontier of Open Intelligence”首段和Footnotes | 仅支持厂商公开说明的训练方向和评测条件；不复制排行，不把厂商自述当独立归因实验。原网页HTML已临存`.tmp/B/Kimi31.html`供主Agent最小快照分类，非R1材料 |
| [DeepSeek-V4.1-Flash-1017 Release](https://api-docs.deepseek.com/news/news261017/)；页面导航标2026-10-17 | “Build complete projects from scratch”直接说明使用带self-feedback的RL | 支持第二家团队近期公开路线表述；没有披露完整配方、投入占比或消融，不追读链接中的完整技术报告 |
| [GLM-5.3](https://z.ai/blog/glm-5.3)；搜索标2026-08-14 | 搜索结果可见，但直接网页抽取空；本地请求仅返回598字节壳页 | 未获得正文，不作实质证据；计入尝试核查的第3份，停止扩展 |

QwenGyre检索只返回可用的二手报道线索，未核到一手发布正文；不采纳技术或性能陈述，也未打开其论文正文。三份说明尝试中的两份成功、一个阻塞；数量是边界而不是质量保证。

**总体证据边界：**当前样本仅能支持“近期两家团队的公开说明重视RL及其配套系统”。没有行业抽样框、统一统计或实际资源账目；“公开热度”“配方中采用”“资源投入占比”是三个待区分对象，不能互相代替。发布日期、本文访问日和原论文实验时间分别登记，不以R1早期实验代表2026年10月最新水平。

## 给主Agent的整合交接

- S077处于已读待整合；共享主题、索引、日志未写。建议把R1与Agentic RL的边界、SFT／RL配方关系及“离线蒸馏不等于OPD”整合到已有主题，来源页再改为实际完成状态。
- 非S077的Kimi与DeepSeek发布说明若在最终正文保留实质论据，需由主Agent按目录规则保存最小必要网页快照并登记；不得塞进`raw/web/S077-DeepSeek-R1/`。
- 适合独立回读的关键页：S077 p.3（长度上限变化）、p.6（两次回到V3-Base的Fig.2）、p.27（SFT大多单轮）、p.40（Agentless与采样口径）、pp.61–63（蒸馏比较与基座经验）。
- 视觉核对只针对原PDF证据；本文问题列表没有新图，Obsidian未测。临时提取文本、重复PDF和页面渲染在`.tmp/B/`，验收后清理。

## 第二轮修订

待一次交叉审查后追加；以上独立首稿保留，不以覆盖方式抹去判断变化。


### 接续身份与唯一一次交叉审查

按用户后续指定，第二轮由 gpt-6-astra／high 接手续作；已读取上方B首稿及C前提稿，不将接续工作算成另一次独立首轮，也不新增轮次。C的审查通过任务消息交付；可回看 [[组会/2026-10-28-Optimization-RL/过程/C-前提与反证|C的审查与补读记录]]。首稿原文保留，以下记录改变了哪些判断。

| C的质疑或判断 | B的核查与处理 | 状态 |
| --- | --- | --- |
| B1／B3／B5／B6的R1学术依据支持，但不能混同推理输出与环境交互 | B重新读取并查看v2原页p.3、p.6、p.40、pp.61–63；保留两类训练可能重叠的边界，不按算法名称分类 | 保留，措辞收窄 |
| B2要区分成功概率、有限采样覆盖与迁移；C对S078的核读不支持用大k结果宣布RL永远无法新增能力 | 本题本来不裁决“真能力”；修订后明确采样覆盖不等于实际能识别并选中正确结果，未采到也不能证明概率为零。S078的具体实验由C负责，B未另行核读，不冒充第二份独立确认 | 保留，改成测量对象问题 |
| B3不能预设SFT不泛化；C报告S079在特定底座、长CoT和优化条件下有跨域推理改善，且SFT–GRPO未匹配总FLOPs | 本题继续按状态来源、监督和预算讨论组合，不把SFT／RL／OPD排成升级序列。S079只作为C传来的边界提醒，正式论文结论须由主Agent回核其唯一页与原页 | 保留，不增加普遍胜负结论 |
| C未独立核验B4及其他官网论据，判外部内容无法判断；支持“厂商自述不代表行业投入”的限制 | B复读原已保存的两份官方HTML，哈希与web-evidence.json一致；Kimi正文确实列出联合RL和配套系统，DeepSeek正文确实写self-feedback RL。没有新开第四页或追读技术报告；此处仍不是独立效果归因 | 保留，两份官方自述，不称行业统计 |

### 定向原页复核与新增限定

- **版本和长度。** 本地原件仍为86页arXiv v2，SHA-256与首稿登记一致。p.3写明8.2k步以后最大输出长度从32,768改成65,536，作者同时说明性能与输出长度出现跃升；不能把这个跃升当作训练条件不变的自发思考增长。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=3|S077 §2.1 · p.3]]
- **配方的数据回流。** Fig.2中冷启动SFT和第二次SFT分别从V3-Base参数起步，R1-Zero／Dev2通过采样数据影响后续模型；不能画成同一组参数从Zero一路连续训练到最终R1。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=6|S077 §3、Fig.2 · p.6]]
- **评测系统。** D.1明确SWE-Bench Verified采用Agentless。它支持“最终结果包含模型与harness的共同作用”，不识别所有改进分别属于哪一方，也不能由该分数推出已经进行了完整多轮工具RL训练。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=40|S077 D.1 · p.40]]
- **蒸馏与底座。** Table16比较强教师离线蒸馏与本文Qwen2.5-32B纯RL路线，并非统一监督来源和总预算的SFT／RL裁决；Table17的Qwen2-Math-7B-Zero对照是Instruct与GPT-4o，**并非同一7B基座训练前后**。已将后一点写入S077唯一页，防止把“7B也有好结果”进一步升级为严格的RL因果对照。G.1的早期小基座失败经验也不支持“小模型都不能RL”。[[raw/papers/optimization/reinforcement-learning/DeepSeek-R1.pdf#page=61|S077 F.1、Tables16–17、G.1 · pp.61–63]]

### 六个宏观问题的第二轮定稿建议

以下为交流问题，不是六个未解决研究缺口。背景仍沿用首稿对应原页；没有新问题需要第三轮讨论。

1. **从推理模型的RL走向Agentic RL，最实质的训练变化发生在哪里？** 关注动作如何改变下一次可见状态、后续反馈及采样条件，允许两类系统重叠。追问：实践中最容易使原配方不再适用的是哪一种依赖，为什么？
2. **说RL带来了能力增长时，我们究竟在测哪一种增长？** 区分有限预算下成功更稳定、采样覆盖扩大、可观察策略变化，以及新任务或新环境上的迁移；不先分“真／假能力”。追问：哪种证据最能帮助您区分这些变化，又排除了哪些替代解释？
3. **SFT、RL和OPD各自的作用，怎样随可获得的状态、监督和预算而变化？** R1显示SFT与RL可以交替配合，其离线蒸馏不等于OPD；不能由固定示范的覆盖限制推出SFT不可能泛化。追问：当教师、验证器和交互成本同时受限时，您会先看哪一种条件来决定组合？
4. **“业界越来越重视RL”，是在说公开发布、实际配方，还是资源投入发生了变化？** 两份近期说明只确认两家团队公开强调RL；缺少行业抽样和资源账目。追问：如果把模型训练算力与环境、验证器、数据构造的人力分开，您观察到的重心会不会不同？
5. **RL扩展到长期任务时，最先限制继续进步的通常是什么？** 保留反馈可靠性、经验获得、更新稳定性与训练系统之间的相互制约，不先指定算法为唯一瓶颈。追问：在您接触的任务中，哪个限制一旦缓解，最可能改变整体训练安排？
6. **怎样判断训练后的模型更适合长期做事，改善又能迁移到哪些变化条件？** 固定或记录harness、预算和环境；成功率、失败后继续执行、成本与迁移分别回答不同问题。追问：如果只能保留少数评价，您最希望它们揭示哪种会被总分掩盖的能力或退化？

### 第二轮交接与停止点

S077的核心判断没有被推翻，新增Table17对照限定并补齐p.40／p.63视觉核读登记。S077仍为已读待整合，未修改共享主题、索引和日志；仅主Agent完成整合与验收后才能改为完成。B官方说明预算仍为3份尝试、2份成功，不继续扩张；两份原HTML的保存身份及正式归档由主Agent处理。B不把C对S078／S079的交接当成本人读取或新增独立证据。达到两轮停止，Obsidian未测，临时原页图与提取文本待全轮验收后清理。
