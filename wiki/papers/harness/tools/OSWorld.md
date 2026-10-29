---
type: paper
source_id: S085
reading_status: body-and-selected-appendices-read
ingest_status: complete
created: 2026-10-29
updated: 2026-10-29
sources:
  - "[[raw/papers/harness/tools/OSWorld.pdf]]"
primary_direction: harness/tools
related_directions:
  - harness/verification
---

# OSWorld：真实桌面中的行动、终态验收与人类基线

**OSWorld 已在真实操作系统与应用中测跨应用工作，并允许经桌面进入终端；真实执行不是 Terminal-Bench 独占。** 它的人类基线和作者试做提供不同层的证据，最终验收仍明确缺少完整副作用检查。[[raw/papers/harness/tools/OSWorld.pdf#page=3|§§2–3 · pp.3–7]] [[raw/papers/harness/tools/OSWorld.pdf#page=36|App.D.5.1 · p.36]] [[raw/papers/harness/tools/OSWorld.pdf#page=49|App.E · p.49]] 与 Terminal-Bench 的关系见 [[wiki/applications/terminal-bench-comparison|跨基准审视]]。

## 来源与读取边界

- **来源 ID：S085。** Tianbao Xie、Danyang Zhang、Jixuan Chen、Xiaochuan Li、Siheng Zhao、Ruisheng Cao、Toh Jing Hua、Zhoujun Cheng、Dongchan Shin、Fangyu Lei、Yitao Liu、Yiheng Xu、Shuyan Zhou、Silvio Savarese、Caiming Xiong、Victor Zhong、Tao Yu，*OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments*，NeurIPS 2024 Datasets and Benchmarks Track。
- **固定原件：**[[raw/papers/harness/tools/OSWorld.pdf|NeurIPS 2024 会议版 PDF]]，55 页，36,705,248 字节；SHA-256：`cabfb4bd4f45440946e7f1fbabe9a8c1751c9d17f62ec24101e62b8adf49f33f`。页码均为 PDF 页码，本版本与印刷页码一致。
- **渠道与版本核对：**2026-10-29 访问 [NeurIPS 官方记录](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html)及[固定会议版 PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d413e48f84dc61244b6be550f1cd8f5-Paper-Datasets_and_Benchmarks_Track.pdf)。官方记录列 DOI `10.52202/079017-1650`。本次 OpenReview `tN61DTr4Ed` 页面返回浏览器验证，未用它补写版本历史；未声称已与各 arXiv 版本逐字对齐。网页仅用于身份核对，未归档页面。
- **实际读取：**2026-10-29 读取正文 pp.1–10；附录 A–C pp.16–32；D.1–D.4 pp.32–35；定向读取 D.5 pp.36、41–46，D.6、E–G pp.47–55。D.5 pp.37–40 的其余轨迹本次未逐项核读，参考文献 pp.11–15 未逐条追索。视觉核对 Fig.2（p.3）、Table 1（p.4）、Table 4/Fig.4（p.7）、Table 5（p.8）、Figs.11–12（pp.34–35）及 p.43 命令轨迹。
- **边界：**未读取对应历史提交的 benchmark 代码、未启动虚拟机或复现实验。本页描述会议版论文中的任务与基线，不引入后来的 OSWorld 修订或榜单。本库按计算机行动接口归入 `harness/tools`，终态检查交叉至 `harness/verification`。

## 它测什么，为什么值得测

**本库测量定位：**在可重置的真实桌面操作系统内，用有初始状态、自然语言目标和执行式验收的任务，测量“模型＋观察预处理＋动作生成与执行 harness”完成计算机工作的表现。它补充的是跨应用、跨 GUI/CLI、从进行中的工作状态接手任务的评测条件；不是单独测基础模型，也不是证明已经覆盖全部现实工作。论文明确将文件、软件与窗口布局设到中间状态，再开放实际交互。[[raw/papers/harness/tools/OSWorld.pdf#page=2|§1 · p.2]] [[raw/papers/harness/tools/OSWorld.pdf#page=3|§§2.1–2.2、Fig.2 · pp.3–4]]

**价值有直接支持，代表性只获部分支持。**真实应用状态、截图定位、软件操作知识和跨应用协作都是这种助手必须面对的要求；任务来源可追到实际指南与用户问题。但选择依据是热度、帮助性与多样性，工作流还包含作者组合和设计的场景。Datasheet 明确承认没有统计验证现实任务代表性。因此，它适合诊断所选任务分布中的失败，不能仅由总分估计现实用户工作被替代的比例。[[raw/papers/harness/tools/OSWorld.pdf#page=5|§§3.1–3.2 · pp.5–6]] [[raw/papers/harness/tools/OSWorld.pdf#page=50|App.G.2 · p.50]]

### 对 Terminal-Bench 的“synthetic environments”概括构成什么反证

S080 在相关工作列出 OSWorld 等计算机使用基准，随后以其他基准的 synthetic environments 对照真实 terminal shell。**本库判断：不能把这句话扩读为“OSWorld 运行的是玩具或仿造操作系统、不能进入真实 shell”。** OSWorld 的实际机制是虚拟机中的真实 OS 与应用，虚拟化提供隔离、快照和重置；论文给出 Agent 打开终端、键入并执行 `ffmpeg` 的实例，不是只由标题推断真实性。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]] [[raw/papers/harness/tools/OSWorld.pdf#page=3|S085 · §2.2 · p.3]] [[raw/papers/harness/tools/OSWorld.pdf#page=16|App.A.1 · p.16]] [[raw/papers/harness/tools/OSWorld.pdf#page=34|App.D.4、Fig.11 · p.34]] [[raw/papers/harness/tools/OSWorld.pdf#page=36|App.D.5.1 · p.36]]

需要保留三层区别：

| 层次 | 本版本可直接确认的事实 | 不能顺势推出的结论 |
| --- | --- | --- |
| 环境 | VM 运行真实 Ubuntu/Windows，任务涉及真实桌面和网页应用；主集为 Ubuntu | 虚拟机不等于仿造应用；但真实应用也不证明任务样本具有总体代表性 |
| 任务 | 指令、初始文件、窗口状态和验收由作者构造；有来源改编与工作流组合 | “人工构造任务”与“模拟环境”不是同一属性 |
| 接口 | 基线用 Python 格式的 `pyautogui` 代码操作鼠标键盘；可以打开终端、输入 shell 命令 | 不等于实验提供了任意直接 Python 执行器或与 Terminal-Bench 相同的 shell 工具接口 |

依据：[[raw/papers/harness/tools/OSWorld.pdf#page=3|§§2.2–2.4 · pp.3–5]] [[raw/papers/harness/tools/OSWorld.pdf#page=6|§3.2 · p.6]] [[raw/papers/harness/tools/OSWorld.pdf#page=28|App.C.2 · pp.28–29]]；最后一列为本库辨析。比较 Terminal-Bench 时，应改用任务领域、默认交互接口、观察信息、预算与验收覆盖等具体维度；本页只反驳上述过宽解释，不替 S080 猜测 synthetic 的精确定义。

**Python 与 shell 的证据边界。**App.A.3 定义主要动作空间为 `pyautogui`，另有为潜在 RL 用途设计的 `computer_13`；C.2 要求返回一行或多行 Python 动作代码，每轮独立，不共享前轮变量，并禁止自行截图及 `locateCenterOnScreen`。提示还提供 VM 的 sudo 密码。它直接证明“以 Python 表达桌面动作”和“桌面内可执行 shell 命令”；本次未核读历史运行器，故不把 Python 代码载体写成“任意 Python API 访问权限已验证”。App.A.2 还称环境实现了 terminal output 观察，但主实验四种输入条件未将它单列，不能据此说所有基线直接收到终端 stdout。[[raw/papers/harness/tools/OSWorld.pdf#page=16|App.A.2–A.3 · pp.16–19]] [[raw/papers/harness/tools/OSWorld.pdf#page=28|App.C.2–C.3 · pp.28–29]]

## 一题怎样从输入走到得分

以 Table 1 的“清除 Amazon 保存的 cookies”为例，**这是论文任务及简化 evaluator，不是本库运行记录**：

1. **初始化与输入：**恢复任务 VM 快照，按配置准备文件、软件和界面状态。Agent 得到自然语言指令及该条件下的截图／过滤后的 a11y tree／组合观察。初始状态可以已经打开软件，并非一律从空白桌面开始。[[raw/papers/harness/tools/OSWorld.pdf#page=4|§2.2、Table 1 · p.4]] [[raw/papers/harness/tools/OSWorld.pdf#page=22|App.B.5 · p.22]]
2. **行动与反馈：**生成鼠标、键盘动作，通过桌面更改浏览器状态；下一轮获得更新后的部分观察。默认最多 15 轮，一轮可有多行动作代码，故“15 轮”不是“15 次单个点击”。也可以输出 `WAIT`、`DONE` 或 `FAIL`。[[raw/papers/harness/tools/OSWorld.pdf#page=3|§2.1 · p.3]] [[raw/papers/harness/tools/OSWorld.pdf#page=5|Table 2 · p.5]] [[raw/papers/harness/tools/OSWorld.pdf#page=28|App.C.2.1 · p.28]]
3. **终止与评分：**环境在动作结束后取 cookie 数据，以 `.amazon.com` 的域名规则检查删除结果。`DONE` 是 Agent 的结束动作，不是成功证据；真正判分来自环境状态检查。截图上关闭浏览器或声称已经清理，都不能替代该检查。后一句是依据检查机制构造的教学辨析，非论文观测到的特定失败。[[raw/papers/harness/tools/OSWorld.pdf#page=4|§2.2、Table 1 · p.4]]

再看 Fig.2 的记账任务：配置准备收据与现有 `.xlsx` 并打开 Calc，Agent 根据收据更新表；评估阶段激活相关窗口、取回最终文件及云端参考文件，再用 `compare_table` 的指定工作表／范围规则比较。这显示**可见的工作资料、参考产物和最终检查器是不同角色**。论文展示的基线 prompt 输入是指令与观察，不是参考答案；但本次没有审计文件权限，不能保证所有评价资产在实际 VM 内都不可读。评估后处理可能包含保存文件，评分对象也因此是规定后处理后的状态。[[raw/papers/harness/tools/OSWorld.pdf#page=3|Fig.2、§2.2 · pp.3–4]] [[raw/papers/harness/tools/OSWorld.pdf#page=22|App.B.6.1 · pp.22–23]]

**开放解法仍须尊重指令。**论文展示一个字幕任务：Agent 用桌面操作打开终端，输入 `ffmpeg` 提取字幕及生成无字幕视频，作者标为成功。另一题明确要求“用 GIMP 截取视频”，Agent 改用 `ffmpeg`，作者标注虽然产物做成但没有遵从指定工具。后例证明结果与过程要求可能分离；它没有报告该例的程序 evaluator 实际返回值，故不能据此断言“verifier 已被成功骗过”。[[raw/papers/harness/tools/OSWorld.pdf#page=34|App.D.4、Fig.11 · pp.34–35]] [[raw/papers/harness/tools/OSWorld.pdf#page=43|App.D.5.3 · p.43]]

## 任务从哪里来，与真人怎样对齐

主基准为 **369 个 Ubuntu 任务**，其中 268 个单应用、101 个多应用工作流；84 个整合自已有基准，30 个刻意不可行任务；这些是交叉属性，不是互斥加总的四组。还有 43 个由 Ubuntu 任务适配的 Windows 分析任务。系统框架宣称跨 OS 支持，但 App.B.1 明确没有在 macOS 上开发 benchmark，不能把主榜读成三个系统都测过。[[raw/papers/harness/tools/OSWorld.pdf#page=5|§§3–3.3 · pp.5–6、Table 3]] [[raw/papers/harness/tools/OSWorld.pdf#page=19|App.B.1 · p.19]] [[raw/papers/harness/tools/OSWorld.pdf#page=21|Tables 8–9 · p.21]]

九位计算机科学学生作者用约三个月构造任务，来源包括官方指南、教程、论坛和课程，按浏览量／投票体现的热度、帮助性与多样性筛选；跨应用问题较少，作者将已有例子组合，并加入日常场景启发的设计。每例由另外两位作者检查可行性、歧义和来源对齐，再由未参与该例标注的两位作者试做、反馈，四轮检查还修订了真人与模型实验中暴露的问题。该流程提供任务质量控制证据；未报告从完整候选池到纳入集合的数量，也未证明没有测试集调参影响。[[raw/papers/harness/tools/OSWorld.pdf#page=5|§3.2 · pp.5–6]] [[raw/papers/harness/tools/OSWorld.pdf#page=53|App.G.3 · p.53]]

**真人基线确实做了任务并计时，不是作者估时。**参与者为有基础软件使用技能、尚未接触样本或相关软件的计算机专业大学生；作者记录每题耗时和完成正确性。OSWorld 中位耗时 111.94 秒、总体正确率 72.36%；同一评价设置下另抽 100 个 WebArena 任务，报告 35.38 秒和 88%。这支持“对该参与者群体和所选样本，OSWorld 更耗时、成功更少”，不能泛化为全体用户或两个现实工作领域的难度顺序。[[raw/papers/harness/tools/OSWorld.pdf#page=7|§3.4、Fig.4 · p.7]]

人类与基线面对实际软件，但人类熟悉度、可用时间、低层动作成本与模型的有限轮数并未完全对齐；§3.4 未完整报告人数、每题分配／重复数、人类限时和最终人工判定准则。因此 72.36% 可作任务解题参照，不应读作等资源竞赛，也不应作为“一次 Agent 失败对应一个真人可替代工作”的换算系数。按真人耗时分 easy/medium/hard 的分析只是难度代理；论文自身还指出代码可解任务对模型较容易、简单 GUI 编辑反而困难。[[raw/papers/harness/tools/OSWorld.pdf#page=7|§§3.4–4.1 · p.7]] [[raw/papers/harness/tools/OSWorld.pdf#page=32|App.D.1、Table 15 · pp.32–33]] [[raw/papers/harness/tools/OSWorld.pdf#page=35|App.D.4 · p.35]]

## 最终 verifier 验了什么，人工证据支持到哪一层

论文包含 134 个评价脚本／函数，按任务取得文件、设置、cookie、a11y tree 或应用内部信息；不是用一个通用语言模型裁判判全部任务。例如 Office 任务查最终文件的内容或属性，Thunderbird 的邮件草稿任务查发送前撰写窗口，VS Code 设置任务查设置 JSON 或扩展取得的内部信号。**“执行式”描述取得状态并按规则计算，并不保证规则覆盖完整用户意图。**[[raw/papers/harness/tools/OSWorld.pdf#page=4|§2.2、Table 1 · p.4]] [[raw/papers/harness/tools/OSWorld.pdf#page=6|§3.3、Table 3 · p.6]] [[raw/papers/harness/tools/OSWorld.pdf#page=22|App.B.6 · pp.22–23]]

§2.1 的最终 reward 可为 1、0 或介于其间的部分完成分；准确判断不可行也可得到正向评价。主表称 success rate，但本次在正文和 C.1–C.7 未找到将所有部分分、聚合和重复运行连起来的完整公式。因此不能把所有表中百分数未经核对都改写为严格的二元整题通过比例，也不能凭小数自行推断重复次数。[[raw/papers/harness/tools/OSWorld.pdf#page=3|§2.1 · p.3]] [[raw/papers/harness/tools/OSWorld.pdf#page=8|Table 5 · p.8]] [[raw/papers/harness/tools/OSWorld.pdf#page=27|App.C · pp.27–32]]

| 人工参与层次 | 实际证据 | 支持范围 |
| --- | --- | --- |
| 定义／审查任务 | 作者改写来源、两位其他作者审可行性和歧义 | 提高规范与场景质量，不等于需求总体代表性 |
| 试做与检查验收 | 两位未参与标注的作者试做；反馈包括严重误放行、误拒绝，联合修订；实验期间再修 | 对具体验收器有人工质量控制，但属于开发过程中的修订证据 |
| 真人解题基线 | CS 大学生完成任务、计时并记录是否正确 | 衡量这些参与者的任务表现，不是评价同一批 Agent 终态的判分一致率 |
| 最终判分的人类对照 | 已读范围未报告独立盲评样本、逐项一致率、误放行／误拒绝率或人际一致性 | 不能将“72.36% 人类成功率”或作者复核转换为 verifier 准确率；也不能据缺少这一实验一票否决所有确定性检查 |

定位：[[raw/papers/harness/tools/OSWorld.pdf#page=6|§3.2 · p.6]] [[raw/papers/harness/tools/OSWorld.pdf#page=7|§3.4 · p.7]] [[raw/papers/harness/tools/OSWorld.pdf#page=52|App.G.3 · pp.52–53]]。最后一列为本库证据解释。

**已明确承认的覆盖缺口比抽象担忧更重要。**App.E 指出评价函数主要关注任务完成正确性，很少关注不必要的损害；作者尚未找到高效检测潜在副作用的方法。所以“最终得分正确”不能自动升级为安全、无副作用、满足全部专业工作质量标准。这是原文承认的限制，不是本库由缺少人工一致率臆测得出。[[raw/papers/harness/tools/OSWorld.pdf#page=49|App.E · p.49]]

## 协议、结果与能支持的结论

主实验比较 a11y tree、截图、截图＋a11y tree、SoM 四种观察方式；保留最近三组 observation–action，temperature 1.0、top-p 0.9、每次最多生成 1,500 tokens，每任务最多 15 轮和 30 分钟。SoM 来自过滤后的 a11y tree 标框与编号，不是原 SoM 的分割模型；a11y tree 按可见性、标签、坐标等规则过滤。因而观察预处理和动作接口本身属于被测系统条件。[[raw/papers/harness/tools/OSWorld.pdf#page=7|§4.1 · pp.7–8]] [[raw/papers/harness/tools/OSWorld.pdf#page=27|App.C.1–C.5 · pp.27–30]]

C.1 明确列 `gpt-3.5-turbo-16k`、`gpt-4-0125-preview`、`gpt-4-vision-preview`、`gemini-pro` 和 `gemini-pro-vision`；Table 5 还涵盖 Mixtral、Llama-3、Qwen-Max、Claude-3-Opus、GPT-4o 等，但没有在该节完整锁定全部模型 API 快照。成本表只统计部分模型／输入条件，标注 **2024 年 4 月**，不能当作当前价格或全实验等预算比较。[[raw/papers/harness/tools/OSWorld.pdf#page=8|Table 5 · p.8]] [[raw/papers/harness/tools/OSWorld.pdf#page=27|App.C.1 · p.27]] [[raw/papers/harness/tools/OSWorld.pdf#page=31|App.C.7、Table 14 · pp.31–32]]

Table 5 的 GPT-4＋a11y tree 为 12.24%，GPT-4V＋截图为 5.26%，同模型加入 a11y tree 为 12.17%，SoM 为 11.77%。这显示在这些历史模型与 harness 下，输入形式会大幅改变观测成绩，且不能默认 SoM 或增加信息总能改善。**不做显著性结论：**已读实验设置未报告主表重复次数、随机种子、置信区间或统计检验；四种输入不是同成本配置。论文的“强规划、弱执行”来自事后案例与错误归类，不能据此宣布某个单一组件是全部失败的因果瓶颈。[[raw/papers/harness/tools/OSWorld.pdf#page=8|§4.2、Table 5 · pp.8–9]] [[raw/papers/harness/tools/OSWorld.pdf#page=34|App.D.4 · pp.34–35]]

**长程证据应按实际条件读。**369 题中 101 个跨应用工作流、多步状态转换及部分可见观察都构成持续执行压力；本库将其视为任务内协调证据，不视为跨任务记忆或跨上下文长期自主性的直接证据。§5 的上下文与分辨率实验只在约 10% 的样本上进行；窗口扰动实验选的是原先表现较好的 28 题。它们为 grounding、历史利用和界面稳健性提供诊断线索，不能外推为全任务集或现代模型的一般规律。[[raw/papers/harness/tools/OSWorld.pdf#page=6|§3.3 · p.6]] [[raw/papers/harness/tools/OSWorld.pdf#page=9|§5 · pp.9–10]]

本版本还有可见的**数字更新不同步**：p.2 称跨应用最高 6.57%，而 Table 5 的 GPT-4o＋a11y tree 为 7.56%；p.8 正文概括 workflow 为低于 5%，表中也有超过者。读者应保留表格具体条件，不沿用这些概括作为最高值。Table 15 的 easy／medium／hard 占比加总为 99%，且 feasible／infeasible 的成绩与 Table 5 总分不能直接对上；本次未取得原始结果解释差异，故不据该表复算总体成绩。[[raw/papers/harness/tools/OSWorld.pdf#page=2|§1 · p.2]] [[raw/papers/harness/tools/OSWorld.pdf#page=8|§4.2、Table 5 · p.8]] [[raw/papers/harness/tools/OSWorld.pdf#page=32|Table 15 · p.32]]

## 使用边界与主题落点

**本库使用判断：**适合研究真实桌面上的动作落地、软件知识、跨应用协调及终态验证；比较系统时应锁定会议版对应任务、应用版本、观察／动作接口、预算与评分规则。不能只据论文总分声称现实工作覆盖、安全可靠性、跨系统通用性或长期自主能力已经被充分测得。Ubuntu 主集、Windows 小规模适配和跨 OS 相关性分析不等于所有系统都验证过；外部资源也不保证长期保持不变。[[raw/papers/harness/tools/OSWorld.pdf#page=19|App.B.1–B.2 · p.19]] [[raw/papers/harness/tools/OSWorld.pdf#page=33|App.D.3 · p.33]] [[raw/papers/harness/tools/OSWorld.pdf#page=49|App.E · p.49]] [[raw/papers/harness/tools/OSWorld.pdf#page=51|App.G.2 · p.51]]

本页对已有认识的修订是：**真实 shell、真实 OS、人工构造任务、GUI 默认接口和执行式验收可以同时成立；不能用 synthetic／real 一条轴替代逐层比较。**另一个持久区分是：作者试做验收、真人基线与最终 verifier 的独立人工一致性回答不同问题。

已整合至 [[wiki/applications/Overview|应用与评测]]、[[wiki/harness/verification|验证]] 与 [[wiki/applications/terminal-bench-comparison|跨基准审视]]。主协调者回核 pp.3–8、36、49，并视觉检查 p.36 的真实终端实例；原件复制前后哈希相同，链接与结构由本轮统一检查。Obsidian 内渲染与跳转未测，未复现实验。
