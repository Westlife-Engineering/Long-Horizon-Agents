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
