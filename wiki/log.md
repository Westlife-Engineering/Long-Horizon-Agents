# 操作日志

仅在文件末尾追加。错误通过新条目更正，不改写历史；日期使用 Asia/Shanghai。内容导航见 [[wiki/index|索引]]，维护规则见 [[AGENTS|Schema]]。

## [2026-10-19] schema | 初始化三层架构与最小维护规则

- 依据用户要求及 [[raw/articles/llm-wiki|LLM Wiki 原始理念]]，建立 Raw Sources / Wiki / Schema 三层；将持续整合、可追溯来源和可演化结构作为核心。
- 创建 [[AGENTS|长期规则]]，明确 [[workflows/ingest|Ingest]]、[[workflows/query|Query]]、[[workflows/lint|Lint]] 及共同完成条件。流程当前是 Agent 操作规约，无后台自动化。
- 初始化规模：10 张 Wiki 页面（索引、日志、总览、六个视角、1 张论文页）。技术子方向用页内导航；研究问题放前沿页；没有预建 concepts/research 空目录或独立未读论文页。
- 原始理念文件由根目录 `llm-wiki.md` 归档至 `raw/articles/llm-wiki.md`；归档前后 SHA-256 均为 `DC3EFE98AE62F23DD08ACAD13ABA2E95287BEB20B6BEC2F4AF0423557FE37401`，字节未变。它是方法论来源，不计入学术论文数。

## [2026-10-19] ingest | S001 综述的地图式摄入

- 来源：[[raw/papers/Towards Long-Horizon Agents.pdf|Towards Long-Horizon Agents: A Survey]]，149 页。原名 `Dong 等 - Towards Long-Horizon Agents A Survey.pdf`，从根目录归档至 `raw/papers/`；归档前后 SHA-256 均为 `C62DA7E66A4C3F7251ED8B450F51DF6500B2F850C7C70853779614E3D780E738`。
- 创建唯一 [[wiki/papers/Towards Long-Horizon Agents|论文页]]，记录身份、读取范围、定位与未完成内容。已做地图式阅读及关键图表/公式的视觉核对，未完成全文各方法的逐项精读；所引参考文献原论文均未读取。
- 将实质内容整合至 [[wiki/overview|总览]]、[[wiki/foundations/Formalization|Foundation]]、[[wiki/foundations/Evolution|Evolution]]、[[wiki/harness/Overview|Harness]]、[[wiki/optimization/Overview|Optimization]]、[[wiki/applications/Overview|Application]]、[[wiki/frontier/Overview|Frontier]]，建立与论文页的相互引用并更新 [[wiki/index|索引]]。
- 参考文献 [464]、[544]、[261] 仅核对综述内的书目信息，列为 3 项待阅读线索；独立方法/实验论文已读数仍为 0。
- 记录 [[wiki/frontier/Overview#需保留的原文表述张力|T001]]，以及 3 个本库待检验问题。未决定研究细分方向，未把作者前沿立场改写成已验证结论。
- 校验：归档哈希一致，核心分类对照目录与相关正文，Fig.1/2/3、Eq.1、Table 8 已查看页面图像。结构检查结果另行追加在后续 `lint` 条目中。

## [2026-10-19] lint | 初始化全库检查

- 范围：全部 10 张 Wiki 页面、4 份 Schema 文件与 2 份 Raw 来源。
- 结构检查通过：所有内部文件链接、标题锚点与 PDF 页码有效；索引覆盖全部知识页；无孤立知识页、空白文件或空目录；唯一论文页与七张综合/主题页相互引用；页面元数据齐全。
- 完整性检查通过：两份 Raw 文件 SHA-256 与归档前一致；仅有 1 张独立论文页。检查脚本与提取/渲染产物位于系统临时目录，未加入知识库。
- 内容核对范围：六个视角、Harness 六类、Optimization 七类、应用五类与 Frontier 四轴九方向均对照综述相应正文/目录；定义公式、层级图与前沿表已检查原始页面图像。页内引用区分综述框架、作者展望、本库问题与未读参考文献。
- 未解决：[[wiki/frontier/Overview#需保留的原文表述张力|T001 的适用范围]]；综述所有细分方法和引用工作的独立原文核验尚未完成。结构检查通过不表示已验证这些研究结果。
- 索引与交叉引用已核对，无需额外修改；阅读范围和候选状态见 [[wiki/papers/Towards Long-Horizon Agents|S001 论文页]]。本次仅追加日志，既有条目保持不变。

## [2026-10-19] query | 澄清 Schema、论文页生成流程与讨论成果落点

- 问题：4 份 Schema 文件的分工、综述论文页如何生成，以及 Open Questions 是否有独立目录。
- 核对现有文件：Schema 为 AGENTS.md 与 workflows 下的三份清单；综述页来自初始化时实际执行的地图式 Ingest，阅读范围已登记；未创建独立 Open Questions 页面或目录，现有问题位于 [[wiki/frontier/Overview|前沿页]]。
- 讨论沉淀规则已由 [[workflows/query|Query]] 覆盖：澄清与综合写入相关主题，针对单篇论文的理解更新唯一论文页，待检验问题先在现有页积累；有独立内容时再拆出研究问题页，并维护索引、交叉引用和日志。
- 本次未产生知识页变更；核对索引与现有落点，无需调整目录。此次记录仅澄清维护方式，不新增学术结论。

## [2026-10-19] query | 明确综述来源页用途并撤下自行挑选的阅读清单

- 用户澄清：当前综述用于建立领域地图，尚未确定细分方向；初始化时自行挑选待阅读文献造成了阅读路线已被安排的误解。
- 更正此前初始化决定：撤下 S001 页面中 3 项自行挑选的待阅读文献；旧日志保留当时操作事实，以本条记录当前状态。
- 更新 [[wiki/papers/Towards Long-Horizon Agents|综述来源页]]，在开头明确其作用是记录地图来源、阅读范围和主题落点；同步 [[wiki/index|索引]] 与 [[wiki/frontier/Overview|前沿页]]，去除清单入口。现有探索问题未被用户选为研究方向，也没有对应阅读计划。
- 更新 [[AGENTS|Schema]] 与 [[workflows/ingest|Ingest]]：综述按地图来源组织；仅在用户要求推荐或具体问题需要追索时登记未读线索，不自动从参考文献生成阅读计划。
- 校验：修改后结构检查通过，内部链接、标题锚点、PDF 页码、索引覆盖与主题互链有效；两份 Raw 哈希保持一致。未新增学术结论、论文来源或目录。

## [2026-10-19] schema | 将日志粒度调整为实质性操作

- 修订 [[AGENTS#7. 索引与追加日志|日志规则]] 及三个工作流：普通问答和轻微编辑不记；一次有实质结果的操作合并记一条，通常 1–3 个短要点。取消此前“无知识变更也记录”的要求，减少维护噪声。

## [2026-10-24] query | 从 Foundation 定义展开运行机制与概念理解

- 回读 S001 的 Foundation（PDF pp.7–15），结合用户阅读对话，将 [[wiki/foundations/Formalization|基础理解页]] 从简要定义扩展为问题驱动的解释：串起状态—观察—上下文、完整交互循环、H1–H3，以及固定策略、任务记忆和持久自我演化的区别。
- 标明本库思考与解释例子，补充依赖结构、纠错恢复、反馈与奖励、终止与成功、时间代理的理解；保留 H3/self-evolution 的重叠及用词边界，未将综述转述升级为直接证据。
- 同步 [[wiki/papers/Towards Long-Horizon Agents|S001 阅读范围]] 与 [[wiki/index|索引]]；局部链接、标题锚点、元数据与索引检查通过，原 PDF 哈希一致。仍为 1 篇学术来源，未新增方法论文或阅读计划。


## [2026-10-24] query | 为 Foundation 增加图解与卡片阅读入口

- 按用户的阅读反馈，将基础理解页的四个延伸问题改为判断、Mermaid 小图与可折叠依据/解释；增加 [[wiki/foundations/Foundation-visual.html|交互图解]] 和 [[wiki/foundations/Foundation.canvas|Obsidian 卡片画布]]，索引同步入口。展示视图标记快照日期，完整论证仍归原主题页。
- 保留原有详细内容、证据层级和来源定位；浏览器桌面/窄屏、深色模式及交互检查通过，Canvas 格式与链接已校验但未在 Obsidian 中实测。未新增学术来源或结论，原 PDF 哈希一致。

## [2026-10-25] schema | 将阅读设计与 Obsidian 验收纳入维护

- 更新 [[AGENTS|规则]] 和 Ingest / Query / Lint，新增 [[workflows/presentation|阅读表达清单]]，明确 Codex 的表达设计、关联视图同步与应用验收责任；默认入口待用户比较后决定。
- 完成 [[wiki/foundations/Formalization#从这套基础定义还能多理解什么|A · 图解笔记]] 与 [[wiki/foundations/Foundation.canvas|B · Canvas 问题地图]]：同一组问题摘要通过块引用共享，原详细论证保留；索引并列入口，旧 HTML 标记历史快照，修复表格链接转义。
- Obsidian 1.14.4 已实测图表、折叠与代表性公式、Canvas 引用跟随/回跳及 PDF 页码跳转；检查深浅模式和正常/较窄窗口，修正过宽图。Canvas 窄窗口全览需放大卡片；独立分栏和移动端未测。文件与图文检查通过，Raw 哈希不变；未新增学术来源，等待用户体验反馈。

## [2026-10-25] schema | 选定图解笔记并撤下 Canvas 试点

- 按用户反馈，[[wiki/foundations/Formalization|图解笔记]] 成为默认入口；规则要求图就近承担解释、文字补充论证并减少重复，不以“旧长文前追加图解”作为完成标准。Foundation 的四个问题已归入对应机制段落，循环图先于可展开的公式；其他主题随阅读和更新逐步改进。
- 已撤下生成的展示文件 `wiki/foundations/Foundation.canvas`，清除当前入口；旧日志中的画布链接保留为历史记录，不再是有效阅读入口，替代入口为上述图解笔记。删除根目录 `Obsidian阅读与视觉表达-临时实施计划.md`，选择与长期维护要求已归入正式规则。
- 校验：当前知识页、索引与规则的文件/标题/块链接通过，旧日志中的两处 Canvas 链接作为已说明的历史撤下项保留；原有八个依据/思考块保留，Raw 哈希不变。Obsidian 中已检查重新布局的循环图、可展开公式及大纲跳转，未重测其他未变图的全部显示条件。

## [2026-10-25] schema | 移除独立 skills 测试目录

- 按用户要求，删除 `workflow-trial/`（内含 `lha-group-meeting_20261023/`）：这是独立的 HTML、图解与 PPT 技能试跑产物，不属于正式 Wiki 知识维护。
- 检查项目内含隐藏文件的目录路径与交付文件名引用，未发现其他文件的索引或依赖，无需修改现有索引。正式阅读入口仍为 [[wiki/index|知识库索引]]；Raw 来源与既有知识页保持不变。

## [2026-10-25] schema | 更正试跑目录处置意图并连接 Git 远程

- 用户澄清：此前“移除项目”意为移到项目外，而非删除。此前确实执行了直接删除；原目录没有 Git 备份。现使用留存脚本、原生成图及原 PDF，在项目外 `C:/Users/ZENGZX/Desktop/workflow-trial-recovered/lha-group-meeting_20261023/` 重建主要交付；这是恢复重建，不是原目录逐字节还原，缺失范围见该目录 README。
- 按用户指定的远程仓库初始化本地 Git，设置 `origin` 为 `https://github.com/Westlife-Engineering/Long-Horizon-Agents.git`，本机连接检查通过。忽略 Obsidian 窗口布局等本机状态；恢复目录不纳入本库索引或版本管理。公开远程尚未上传文件。

## [2026-10-25] schema | 接入有边界的自主研究与多 Agent 审查

- 新增 [[workflows/autoresearch|Auto Research]] 与 [[workflows/brainstorm|Brainstorm]]，增强 [[workflows/ingest|Ingest]] 的机制、前提、证据与知识变化分析，同步 Query、Lint、规则入口及索引；用于文献驱动的 idea 探索，不强制生成研究缺口。
- 按用户要求，每篇论文交同模型 subagent 完成摄入和整合，主 Agent 调度并验收；共享文件串行写入，Harness / Optimization 各自阅读与讨论并保留跨模块核查。本轮仅完成规则和启动方案，下一轮才开始从综述引用按选定子方向约 5 篇选读。
- 两个同模型 subagent 已独立审查协议；修正验收后记完成日志、跨模块共用两轮上限等流程边界。链接/表格与 Raw 完整性检查通过，来源数未变。Obsidian 控制接口未能读取最小化窗口，本轮应用渲染与跳转未验收。

## [2026-10-25] schema | 第一轮研究的 Git 检查点与并发约定

- 用户启动 Harness / Optimization 全部一级子方向的第一轮研究，并授权主 Agent 在必要节点提交 Git；已将单一提交者、差异检查、批次验收及不自动推送写入规则。启动规则提交为 `ab4a632`。
- 本轮实际并发上限 4（含主 Agent），按最多 3 个同模型子任务分批派发；所有临时材料限当前项目的 `.research-tmp/` 并排除 Git，遵守用户不改动其他文件夹的要求。范围与预算见 [[wiki/overview#第一轮自主研究|第一轮约定]]；本条仅记录已完成的调度规则调整，论文摄入仍在进行前的选文阶段。

## [2026-10-25] ingest | S007 HiAgent：子目标工作记忆

- 摄入 [[wiki/papers/HiAgent|HiAgent]] 并整合至 [[wiki/harness/Overview#上下文与记忆|上下文与记忆]]，明确当前子目标完整轨迹、已完成子目标摘要与旧轨迹取回的关系；保留 GPT-4、五环境及 30 步预算，未将 Gripper 写成一致提升。
- 内容与结构检查通过，Raw 哈希匹配；本批论文与主题表达的 Obsidian 应用检查尚未完成，未复现实验。

## [2026-10-25] ingest | S008 MemGPT：分层存储与读写控制

- 摄入 [[wiki/papers/MemGPT|MemGPT]]，在 [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] 区分主上下文、外部存储、自动队列管理与模型函数调用；保留对话/文档检索任务边界，以及基线仅见摘要、系统可查完整历史的条件差异。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S009 A-MEM：记忆组织与演化

- 摄入 [[wiki/papers/A-MEM|A-MEM]]，将新 note 关联及旧 note 元信息演化整合至 [[wiki/harness/Overview#上下文与记忆|上下文与记忆]]；限定 LoCoMo/DialSim 问答证据，记录检索 k 按模型/题型变化及并非所有题型领先。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S010 ExpeL：跨任务经验规则

- 摄入 [[wiki/papers/ExpeL|ExpeL]]，在 [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] 区分原始成功轨迹与归纳规则；澄清无参数更新仍有训练任务、重试反馈与更强归纳模型成本，不把规则投票视为事实证据强度。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S011 ReSum：摘要接续与策略适应

- 摄入 [[wiki/papers/ReSum|ReSum]] v3，连接 [[wiki/harness/Overview#上下文与记忆|运行时摘要接续]] 与 [[wiki/optimization/Overview#摘要接续怎样进入策略训练|分段轨迹训练]]；区分策略 training-free 与已训练摘要器，保留 GRPO 40 次、ReSum-GRPO 60 次训练调用预算及仅成功轨迹的成本口径。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。候选归因问题保留为待核查，未宣布研究缺口。

## [2026-10-25] ingest | S032 Longformer：显式 token 的稀疏访问

- 摄入 [[wiki/papers/Longformer|Longformer]] v2，整合至 [[wiki/optimization/Overview#架构基础|架构基础]]，区分局部/全局连接、预训练适配与文档任务证据；保留任务指定全局位置、组合消融和 HotpotQA 过滤条件。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S033 Mamba：输入相关的压缩状态

- 摄入 [[wiki/papers/Mamba|Mamba]] v2，将选择性状态更新与硬件 scan 整合至 [[wiki/optimization/Overview#架构基础|架构基础]]；分开合成关联、DNA/音频百万长度与语言质量证据，保留变 batch 吞吐及未训练 6.9B 的边界。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验，不将架构结果视为长期 Agent 成功证据。

## [2026-10-25] ingest | S034 Kimi Linear：压缩与全局访问的混合

- 摄入 [[wiki/papers/Kimi-Linear|Kimi Linear]] v2，将 KDA / MLA 分层混合整合至 [[wiki/optimization/Overview#架构基础|架构基础]]；区分有限状态层与整模型缓存、1.4T/128k 与 5.7T/1M 结果，以及固定 batch 和扩大 batch 的效率口径。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验；端到端计时硬件与完整 batch 配置未确认。

## [2026-10-25] ingest | S035 GQA：KV 头共享与解码成本

- 摄入 [[wiki/papers/GQA|GQA]] 会议正式版本，在 [[wiki/optimization/Overview#架构基础|架构基础]] 区分头维度共享与时间历史压缩；保留 T5、uptraining 与部署配置，记录计时图表单位不一致，不抄录绝对速度承诺。
- 内容与结构检查通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S036 Lost in the Middle：上下文使用的行为边界

- 摄入 [[wiki/papers/Lost-in-the-Middle|Lost in the Middle]]，连接 [[wiki/optimization/Overview#架构基础|有效上下文]] 与 [[wiki/harness/Overview#上下文与记忆|检索及编排]]；保留位置效应的任务/模型例外，区分检索召回、合成 KV 检索和语义 QA。
- 内容与结构检查通过，Raw 哈希匹配；本地为 arXiv v3，未与综述所引 TACL 版本逐项对齐；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S002 ReAct：思考与行动的反馈循环

- 摄入 [[wiki/papers/ReAct|ReAct]] v3，整合至 [[wiki/harness/Overview#循环与工作流|循环与工作流]]；区分思考写回历史与行动取得环境观察，保留动态调整和失败恢复的边界。
- 内容与结构验收通过、Raw 哈希匹配；ALFWorld 均值与最佳提示值分开，未将跨任务结果直接排名。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S003 ReWOO：计划结构与证据变量

- 摄入 [[wiki/papers/ReWOO|ReWOO]] 固定 v1，在 [[wiki/harness/Overview#循环与工作流|循环与工作流]] 区分预定计划结构与实际工具返回值；补充重复提示成本和未知环境中的预规划限制。
- 内容与结构验收通过、Raw 哈希匹配；保留 Accuracy/EM 差异、相对提升与百分点区别，以及特定工具失效设置。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S004 Arbor：持久假设树与科研状态

- 摄入 [[wiki/papers/Arbor|Arbor]] 固定 v1，将假设、实验事实、解释与实现版本的关联整合至 [[wiki/harness/Overview#循环与工作流|循环与工作流]]；区分语义归纳、分层执行和动作路径搜索。
- 内容与结构验收通过、Raw 哈希匹配；保留 AO 适用范围、归纳与剪枝边界，E_test 准入/最终验证及预算口径仍待核查。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S005 ToT：部分解搜索与模型误剪

- 摄入 [[wiki/papers/Tree-of-Thoughts|Tree of Thoughts]] NeurIPS 会议版，在 [[wiki/harness/Overview#循环与工作流|循环与工作流]] 分开 thought 粒度、候选生成、评价与 BFS/DFS 控制，保留文本状态回溯的条件。
- 内容与结构验收通过、Raw 哈希匹配；保留调用预算、词级/整题/oracle 输出区别和正确状态被误剪的原文反例。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S006 LATS：环境反馈与树搜索

- 摄入 [[wiki/papers/LATS|LATS]] PMLR 会议版，在 [[wiki/harness/Overview#循环与工作流|循环与工作流]] 区分环境观察、模型价值、终局奖励回传和失败反思，明确可回退环境与反馈权限。
- 内容与结构验收通过、Raw 哈希匹配；保留 HotpotQA oracle、搜索后 pass@1、WebShop 平均分/严格成功率及配置待核查项。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S012 Toolformer：调用选择与训练接口

- 摄入 [[wiki/papers/Toolformer|Toolformer]] NeurIPS 正式版主文与独立补充文件，在 [[wiki/harness/Overview#工具、MCP 与技能|工具方向]] 和 [[wiki/optimization/Overview#微调|微调]] 区分调用数据筛选、参数学习与运行时执行。
- 内容与结构验收通过，两份 Raw 哈希匹配；保留单次调用、无链式工具训练及预测损失代理的边界。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S013 AnyTool：失败驱动的工具发现

- 摄入 [[wiki/papers/AnyTool|AnyTool]] PMLR 正式版，将分类层级、候选 API 池和失败后扩大搜索整合至 [[wiki/harness/Overview#工具、MCP 与技能|工具方向]]；区分检索状态更新与参数训练。
- 内容与结构验收通过、Raw 哈希匹配；保留成功率分母、GPT-4 判断和未匹配总成本的消融边界。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S014 CodeAct：程序动作与模型适应

- 摄入 [[wiki/papers/CodeAct|CodeAct]] PMLR 正式版，在 [[wiki/harness/Overview#工具、MCP 与技能|工具方向]] 区分代码内组合与下一轮反馈，在 [[wiki/optimization/Overview#微调|微调]] 分开 CodeActInstruct / CodeActAgent 的训练贡献。
- 内容与结构验收通过、Raw 哈希匹配；保留代码多调用与 JSON/Text 单调用的动作粒度差异，轮数不等于底层调用成本。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S015 Voyager：程序经验与技能复用

- 摄入 [[wiki/papers/Voyager|Voyager]] arXiv v2，将技能检索、代码修复、成功判断和程序入库整合至 [[wiki/harness/Overview#工具、MCP 与技能|工具与技能]]，连接持久经验的保存对象与复用条件。
- 内容与结构验收通过、Raw 哈希匹配；保留 Minecraft 高层接口、复活设置、新世界保留技能及 critic 误判边界，未与综述所引 TMLR 版本逐项对齐。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S016 MCPMark：状态验收与重复稳定性

- 摄入 [[wiki/papers/MCPMark|MCPMark]] arXiv v1，在 [[wiki/harness/Overview#工具、MCP 与技能|工具方向]] 与 [[wiki/harness/Overview#验证|验证]] 区分协议可用、正常终止和最终约束满足，以及 pass@1 / pass@4 / pass^4 的含义。
- 内容与结构验收通过、Raw 哈希匹配；保留任务与服务器覆盖、版本固定和 verifier 完备性边界。未运行 benchmark 或审查全部验证器源码；Obsidian 应用未测。


## [2026-10-25] ingest | S037 TaskCraft：依赖构造与增量核查

- 摄入 [[wiki/papers/TaskCraft|TaskCraft]] arXiv v2，在 [[wiki/optimization/Overview#数据与环境合成|数据与环境合成]] 区分任务依赖扩展、原子执行验证与长链增量语言核查；保留 hop/调用数、筛选模型和实际 SFT 数据范围。
- 内容与结构验收通过，Raw 哈希匹配；论文内数据规模口径差异已留在论文页。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S038 SWE-Gym：环境标签与学习验证器

- 摄入 [[wiki/papers/SWE-Gym|SWE-Gym]] PMLR 正式版，连接 [[wiki/optimization/Overview#数据与环境合成|可执行环境和成功轨迹]] 与 [[wiki/harness/Overview#验证|verifier 重排]]；区分真实测试标签、预测成功率、候选覆盖和最终选择。
- 内容与结构验收通过，Raw 哈希匹配；保留半手工环境成本、易题筛选、scaffold 条件及自训练下降。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S039 WebDreamer：状态预测与执行前规划

- 摄入 [[wiki/papers/WebDreamer|WebDreamer]] arXiv v2，在 [[wiki/optimization/Overview#数据与环境合成|数据与环境]] 和 [[wiki/harness/Overview#分支能否撤回，评价能否被信任|分支规划]] 区分真实交互监督、预测的变化描述、模型评分与执行后观察；保留单步模拟及 Dreamer-7B 的组件边界。
- 内容与结构验收通过，Raw 哈希匹配；未与综述所引 TMLR 正式版逐项对齐，效率与模拟误差限定保留。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S040 TOUCAN：真实返回与合成轨迹筛选

- 摄入 [[wiki/papers/TOUCAN|TOUCAN]] arXiv v1，将真实 MCP 返回、合成任务/用户和模型质量标签整合至 [[wiki/optimization/Overview#数据与环境合成|数据与环境合成]]；区分 1.5M 发布规模与 119.3K 训练子集。
- 内容与结构验收通过，Raw 哈希匹配；保留服务器准入、失败排除、有限人工一致性及局部任务退步。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S041 AgentGym-RL：在线交互课程与状态分布

- 摄入 [[wiki/papers/AgentGym-RL|AgentGym-RL]] arXiv v1，在 [[wiki/optimization/Overview#交互上限怎样改变在线训练|在线 RL]] 解释渐增 horizon；数据/环境和微调队列复用同一来源，明确它不构成 SFT 课程效果的直接证据。
- 内容与结构验收通过，Raw 哈希匹配；保留 WebArena 状态修改任务排除、预算口径、Pass@K 与论文内部叙述/表格冲突。Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S042 DeepSeek-V3：组合配方与分阶段归因

- 摄入 [[wiki/papers/DeepSeek-V3|DeepSeek-V3]] arXiv v2，整合至 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]；区分MTP训练目标、YaRN扩窗、后训练与Agentless工程评测；保留小规模消融及正式训练成本边界。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S043 YaRN：位置延展与有效上下文

- 摄入 [[wiki/papers/YaRN|YaRN]] arXiv v3，整合至 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]；解释分段频率与attention scaling，保留PPL/passkey适用范围；记录v3与S001会议引文的版本边界和PI公式方向不一致。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S044 ProLong：以SFT后下游表现选择训练配方

- 摄入 [[wiki/papers/ProLong|ProLong]] ACL 2025正式版，整合至 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]；整合长短数据混合、训练长度与SFT阶段依赖，区分最终配方和消融初始化；同token对照不等于同算力。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S045 Qwen2-VL：多模态表示与组合Agent证据

- 摄入 [[wiki/papers/Qwen2-VL|Qwen2-VL]] arXiv v2，整合至 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]；连接动态视觉token、M-RoPE与Qwen-Agent多轮实验，区分动作匹配、整任务成功以及高层动作/SAM条件。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S046 DoReMi：代理损失与域采样比例

- 摄入 [[wiki/papers/DoReMi|DoReMi]] NeurIPS 2023正式版，整合至 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]；整合小参考/代理模型的excess loss到大模型重采样路线，保留1024长度、跨尺度迁移和额外搜索成本边界。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S017 固定角色与结构化交接

- 摄入 [[wiki/papers/MetaGPT|MetaGPT]] arXiv v7；把 SOP、共享池、订阅依赖和执行测试反馈整合至编排比较，保留角色/预算混杂与基线提示敏感性。主要落点为 [[wiki/harness/Overview#编排|编排]] 与验证联系。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S018 双账本与动态调度

- 摄入 [[wiki/papers/Magentic-One|Magentic-One]] arXiv v1；整合事实/进展账本、停滞重规划及工具团队分工，区分固定成员、动态调度和跨任务学习。主要落点为 [[wiki/harness/Overview#编排|编排]] 与验证联系。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S019 通信图与提示优化

- 摄入 [[wiki/papers/GPTSwarm|GPTSwarm]] PMLR 会议版；区分边分布学习、节点提示更新和框架展示，明确 GAIA 无节点/边优化，以及填字同题池与 best-state 指标边界。主要落点为 [[wiki/harness/Overview#编排|编排]] 与验证联系。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S020 按结果更新子任务

- 摄入 [[wiki/papers/TDAG|TDAG]] arXiv v2；整合动态任务拆解、定制文档和文本技能，保留分层评分与错误表分母；WebShop/TextCraft 未启用 Agent Generation。主要落点为 [[wiki/harness/Overview#编排|编排]] 与验证联系。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S021 失败分类与因果归因

- 摄入 [[wiki/papers/Multi-Agent-Failures|Multi-Agent-Failures]] NeurIPS 2025 会议版；将职责、信息交接和验证作为诊断轴，保留标注/干预条件与过程标签和终局失败的区别，原文图文计数张力留论文页。主要落点为 [[wiki/harness/Overview#编排|编排]] 与验证联系。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S047 AgentTuning：轨迹混合与通用能力保留

- 摄入 [[wiki/papers/AgentTuning|AgentTuning]] ACL正式版，在 [[wiki/optimization/Overview#状态由谁产生，哪些输出受到监督|微调比较]] 区分固定教师状态、成功筛选和通用数据混合；保留逐任务退步、Mind2Web单步及调参协议描述差异。
- 内容与结构验收通过，Raw哈希匹配；Obsidian应用未测，未复现实验。

## [2026-10-25] ingest | S048 ATLAS：关键步骤监督与完整历史

- 摄入 [[wiki/papers/ATLAS|ATLAS]] ACL正式版，将语义步骤选择、loss mask与状态分布整合至 [[wiki/optimization/Overview#微调|微调]]；保留随机步骤对照、选择器依赖、长游戏拆短与总成本边界。
- 内容与结构验收通过，Raw哈希匹配；Obsidian应用未测，未复现实验。

## [2026-10-25] ingest | S049 Agent Distillation：教师轨迹与测试时动作筛选

- 摄入 [[wiki/papers/Agent-Distillation|Agent Distillation]] NeurIPS正式版，在 [[wiki/optimization/Overview#微调|微调]] 和 [[wiki/harness/Overview#依赖怎样执行，失败以后改哪里|工具执行]] 分开FTP数据改进、离线蒸馏与SAG执行筛选；保留5步任务、固定知识库、计算预算及论文内部未同步边界。
- 内容与结构验收通过，Raw哈希匹配；Obsidian应用未测，未复现实验。

## [2026-10-25] ingest | S050 Agent-R：迭代修复监督与状态一致性边界

- 摄入 [[wiki/papers/Agent-R|Agent-R]] arXiv v3，在 [[wiki/optimization/Overview#学到修订行为以后，环境是否能继续|修复监督]] 及 [[wiki/harness/Overview#分支能否撤回，评价能否被信任|运行恢复]] 解释MCTS再采样、actor判错与修复SFT；保留恢复评测条件和阈值/目标符号疑点。
- 拼接后的环境状态一致性保留为优先核读实现的材料缺口，未判定方法不能恢复。内容与结构验收通过，Raw哈希匹配；Obsidian应用未测，未复现实验。


## [2026-10-25] ingest | S022 IsolateGPT：隔离、授权与警告边界

- 摄入 [[wiki/papers/IsolateGPT|IsolateGPT]] NDSS 2025 正式版，在 [[wiki/harness/Overview#Hooks 与中间件|Hooks 与中间件]] 区分跨应用隔离、可信中介和用户授权；保留单应用内部攻击范围、警告率非自动阻断率及人工等待未计成本的边界。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S023 AgentSpec：规则触发与处置责任

- 摄入 [[wiki/papers/AgentSpec|AgentSpec]] arXiv v3，将事件–谓词–处置机制整合到 [[wiki/harness/Overview#规则来源与执行权是两条轴|Hooks 比较]]；分开程序执行、人工/LLM 处置与自动规则生成，保留正常任务误拒和有限场景证据。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S024 ShieldAgent：规则编译与在线判断

- 摄入 [[wiki/papers/ShieldAgent|ShieldAgent]] arXiv v2；在 [[wiki/harness/Overview#规则来源与执行权是两条轴|Hooks 比较]] 并列 S001 静态分类与原文在线计划、赋值及验证代码生成，区分规则形成时间与执行期模型依赖。
- 保留概率规则模型、条件政策遵从率和数据报告不一致；未与 PMLR 版本逐项对齐。内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S025 InfrastructureSentinel：四处检查与状态新鲜度

- 摄入 [[wiki/papers/InfrastructureSentinel|InfrastructureSentinel]] AAAI/IAAI 2026 正式版，在 [[wiki/harness/Overview#检查通过后，环境和规则还会变化吗|Hooks 状态比较]] 区分输入、计划、执行前再检查与事后审计；检测结果仅为下界，配置、样本量和消融不足，按初步证据保留。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。

## [2026-10-25] ingest | S026 AGrail：可演化检查清单与条件评测

- 摄入 [[wiki/papers/AGrail|AGrail]] ACL 2025 正式版，将可增删检查清单、动作键记忆与模型/工具判断整合到 [[wiki/harness/Overview#Hooks 与中间件|Hooks 与中间件]]；区分记忆更新与参数训练、冻结与测试时适应，以及筛选样本后的条件效用与端到端成功。
- 保留表文数字差异与有限迁移证据，不将清单相似度趋稳写成终身安全保证。内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S027 CRITIC：外部证据与纠错净收益

- [[wiki/papers/CRITIC|CRITIC]]：摄入CRITIC arXiv v4，将外部工具证据、模型critique、输出修订与停止分开；保留oracle权限和正确答案误改，与纠错收益共同评估。主要落点为 [[wiki/harness/Overview#选择误差与纠错净收益要分别测量|验证的选择与纠错]]。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S028 AgentPRM-Xi：过程评分与奖励发放粒度

- [[wiki/papers/AgentPRM-Xi|AgentPRM-Xi]]：摄入Xi等AgentPRM arXiv:2511.08325v1，整合promise/progress训练和搜索选择；明确PPO实验使用末步PRM预测作整轨迹奖励。主要落点为 [[wiki/harness/Overview#验证|验证]] 与 [[wiki/optimization/Overview#过程评分怎样进入策略更新|策略更新接口]]。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S029 Agent-as-a-Judge：按需求取证的评估者

- [[wiki/papers/Agent-as-a-Judge|Agent-as-a-Judge]]：摄入ICML 2025会议版，将工作产物取证、需求依赖、整任务成功与人工一致性区分；明确本文未实测评估反馈驱动执行者在线修复。主要落点为 [[wiki/harness/Overview#检查对象决定成功指标|验证对象与指标]]，内部表述差异保留唯一页。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S030 CorrectBench：纠错与误改的双向指标

- [[wiki/papers/CorrectBench|CorrectBench]]：摄入NeurIPS 2025会议版，补充CR/MR及初始准确率下的纠错净收益关系，记录预算与判断口径；样本和表述差异保留唯一页，不提取统一提升量或外推长程恢复。主要落点为 [[wiki/harness/Overview#选择误差与纠错净收益要分别测量|验证的选择与纠错]]。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S031 Self-MAP：跨轮指令与静态记忆规划

- [[wiki/papers/Self-MAP|Self-MAP]]：摄入ACL 2024 MT-Mind2Web/Self-MAP，连接多轮指令与记忆检索、DOM缩减及历史动作rationale；明确静态HTML快照和TSR为Turn，避免归为在线失败纠错器。主要落点为 [[wiki/harness/Overview#上下文与记忆|上下文与记忆]] 与 [[wiki/harness/Overview#检查对象决定成功指标|验证对象]]。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S051 Search-R1：搜索交互与观察损失屏蔽

- [[wiki/papers/Search-R1|Search-R1]]：摄入 arXiv v5，在 [[wiki/optimization/Overview#先确认训练中是谁产生状态，谁提供反馈|RL 状态与反馈比较]] 区分策略生成的搜索/回答与检索观察；保留终局 EM、检索 token 损失屏蔽、固定 Wiki/E5 和动作预算条件。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S052 ToolRL：细粒度调用奖励与单步训练边界

- [[wiki/papers/ToolRL|ToolRL]]：摄入 NeurIPS 2025 正式版，在 [[wiki/optimization/Overview#先确认训练中是谁产生状态，谁提供反馈|RL 状态与反馈比较]] 解释标准调用匹配奖励；明确多轮数据被拆为带历史单步训练，保留算法对照预算差异和多轮评测边界。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S053 GiGPO：重复状态分组与两级优势

- [[wiki/papers/GiGPO|GiGPO]]：摄入 arXiv v3，在 [[wiki/optimization/Overview#局部比较组从哪里来，决定了什么可被区分|采样与信用分配]] 区分完整轨迹和同状态折扣回报比较；保留重复状态覆盖、匹配和策略上下文差异，不将局部优势当作额外过程标签。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S054 Tree-GRPO：共享前缀采样与树内跨树比较

- [[wiki/papers/Tree-GRPO|Tree-GRPO]]：摄入 arXiv v3，在 [[wiki/optimization/Overview#局部比较组从哪里来，决定了什么可被区分|采样与信用分配]] 区分树采样和优势构造的贡献；保留仅搜索工具的恢复条件、预算记号待复核与理论假设边界。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。


## [2026-10-25] ingest | S055 Memory-R1：分阶段记忆学习与回答器依赖

- [[wiki/papers/Memory-R1|Memory-R1]]：摄入 ACL 2026 正式版，连接 [[wiki/optimization/Overview#记忆写入和使用也能成为训练接口|记忆训练接口]] 与 [[wiki/harness/Overview#上下文与记忆|Harness 记忆]]；区分运行时编辑与参数更新，保留固定另一组件、训练快照差异及 LongMemEval oracle 评测条件。
- 内容与结构验收通过，Raw 哈希匹配；Obsidian 应用未测，未复现实验。
