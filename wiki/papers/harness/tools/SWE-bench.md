---
type: paper
source_id: S082
primary_direction: harness/tools
related_directions:
  - harness/verification
created: 2026-10-29
updated: 2026-10-29
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/SWE-bench.pdf]]"
---

# SWE-bench：真实仓库修复如何转化为可执行的评测

**SWE-bench 用真实 GitHub issue、仓库快照和维护者合入 PR 所带的测试，测量系统能否提交满足指定功能与回归检查的补丁；它已经具备真实任务来源和结果导向验收，但不等于完整的软件工程质量或经济价值测量。** 这同时限定了“Terminal-Bench 才真实／才按结果评分”的强读法，也保留了 Terminal-Bench 扩展到软件维护以外工作的定位。前者不是 S080 明确逐项提出的排他主张，不应反过来把它当作稻草人。[[raw/papers/harness/tools/SWE-bench.pdf#page=2|S082 · §§1–2.1 · p.2]] [[raw/papers/harness/tools/SWE-bench.pdf#page=21|App.A.4 · p.21]] [[raw/papers/harness/tools/SWE-bench.pdf#page=9|§7 · p.9]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

## 来源身份与读取范围

- **标题与作者：** SWE-bench: Can Language Models Resolve Real-World GitHub Issues?；Carlos E. Jimenez、John Yang（共同第一作者）、Alexander Wettig、Shunyu Yao、Kexin Pei、Ofir Press、Karthik Narasimhan。PDF 标明 ICLR 2024 conference paper。
- **固定版本：** [arXiv:2310.06770v2](https://arxiv.org/abs/2310.06770v2)，2024-04-05；[官方下载 URL](https://arxiv.org/pdf/2310.06770v2)，DOI `10.48550/arXiv.2310.06770`。2026-10-29 核对官方版本历史：v1 为 2023-10-10，v2 为 2024-04-05，v3 为 2024-11-11。本次选 ICLR 2024 时期的固定 v2；不是最新 v3，也不引入 SWE-bench Lite／Verified 或现行榜单数字。
- **会议身份：** S080 引用的 [OpenReview VTF8yNQM66](https://openreview.net/forum?id=VTF8yNQM66) 在本次访问中返回浏览器验证页；arXiv 官方页面链接至同一会议记录，PDF 标明会议身份。未取得 OpenReview PDF，不能声称两个服务器文件字节相同。
- **原件：** [[raw/papers/harness/tools/SWE-bench.pdf|52 页 PDF]]，6,461,687 bytes；SHA-256 `fbc077933af2941ad911128f0d8c136515d22e2a77e2bc3d6cc08e98440afbb1`。从官方下载临时文件 `SWE-bench-v2.pdf` 原样复制至现路径，归档前后哈希一致；归档前递归检查文件名、论文身份及 Raw 哈希，未发现同篇原件／独立来源页。
- **实际阅读：** 2026-10-29 核读正文 §§1–10（pp.1–11）；App.A.1–A.5 的构造、执行验证、评分和统计（pp.16–24），A.6 开发集（pp.24–26）、B 训练设置（p.25）、C 结果及诊断（pp.25–29）、D 推理与提示词（pp.29–32）、E（p.32）、F 中 Table 25 案例（pp.33–34）。关键图表视觉核对 pp.2、6、8、17、20、21 的 Fig.2、Figs.4–8／Tables 5–6、9–10 及评分文字；页码与印刷页码一致。
- **未核读／未运行：** 参考文献不算新增来源；F 其余完整案例 pp.35–52 未逐项核读。未读取版本对应代码、逐条数据或测试实现，未运行基准，未复现实验。另回读 S080 pp.2–4、6、11，确保下文比较对应其实际表述。

## 测什么，为什么值得测

**原文目标：**把代码评测从独立小函数扩展到已有仓库中解决真实 issue。目标能力包括定位相关代码、理解模块之间的关系、在多处作协调修改，以及保持已有功能；输入是问题描述和完整仓库，交付是补丁。可评价检索、长上下文方法或交互 Agent，但论文主实验只实现简单检索加一次补丁生成。因此，基准可支持的系统范围与本文实际测量的系统范围必须分开。[[raw/papers/harness/tools/SWE-bench.pdf#page=2|§§1–2 · pp.2–3]] [[raw/papers/harness/tools/SWE-bench.pdf#page=4|§4.1 · pp.4–5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=9|§7 · p.9]]

**本库判断：**真实用户报错、开发者提供并合入解决方案，是任务需求和实际使用的直接来源证据，足以支持研究软件维护能力的动机；它没有按职业工作频率、报酬或节省工时抽样，不能把总解决率解释成平均生产率、岗位替代率或经济收益。多文件修改也不能自动折算为人类工时或 Agent 行动长度。原文给出的参考补丁平均修改 1.7 个文件、3 个函数、32.8 行，是产物规模统计，不是长程执行测量。[[raw/papers/harness/tools/SWE-bench.pdf#page=3|§2.3 · p.3]] [[raw/papers/harness/tools/SWE-bench.pdf#page=4|Table 1 · p.4]] [[raw/papers/harness/tools/SWE-bench.pdf#page=16|App.A.1 · p.16]]

## 一道题怎样走完：Sphinx 的配置行为修复

选原文 §5.1 的 `sphinx-doc__sphinx-8713`。用户指出 `napoleon_use_param` 应当同样影响 “Other Parameters” 文档段落：目前该段落总像配置为 False 时那样输出。问题描述还给出怀疑的代码位置、复现例子和版本信息。[[raw/papers/harness/tools/SWE-bench.pdf#page=8|§5.1、Fig.6 · p.8]]

1. **初始信息与环境：**按 PR 的 base commit 还原仓库。基准定义提供问题和仓库；此案例实验使用 oracle 检索，只把参考补丁修改过的文件正文等送入模型，共 1,558 行／20,882 tokens。它透露了应看哪些文件，但没有把参考补丁或隐藏测试作为模型输入。[[raw/papers/harness/tools/SWE-bench.pdf#page=8|§5.1 · p.8]] [[raw/papers/harness/tools/SWE-bench.pdf#page=20|App.A.4、Fig.8 · pp.20–21]]
2. **行动与反馈：**本文 baseline 依据固定输入生成一份 diff；不是让模型在交互终端里反复执行、查看测试并修复。单题一次生成、greedy decoding，随后由评测器应用补丁和运行测试，结果不反馈为下一次生成。[[raw/papers/harness/tools/SWE-bench.pdf#page=30|App.D.2–D.3 · pp.30–31]]
3. **终止与交付：**提交 patch；评测端重置仓库、启用版本对应环境、安装代码、加上 test patch，再应用模型 patch。应用失败时有一次程序化格式修复：删去不必要的上下文行、重算头部行号；仍失败或无法运行测试则计 0。这是评测 harness 的辅助处理，不是模型自行修复成功。[[raw/papers/harness/tools/SWE-bench.pdf#page=21|App.A.4 · p.21]]
4. **验收与本例失败：**所有 `FAIL_TO_PASS`（F2P）和 `PASS_TO_PASS`（P2P）测试必须出现且通过；缺失也算失败。本例模型找对了函数，却让它始终按配置 True 的路径格式化，没有保留 False 分支；相应测试捕捉到该错误。Fig.6 展示 45 passed、2 failed，因此“修改了正确函数”仍不等于完成。真正通过需要同时满足配置切换后的行为与受测旧行为，不要求 patch 文本与参考 PR 相同。[[raw/papers/harness/tools/SWE-bench.pdf#page=8|§5.1、Fig.6 · p.8]] [[raw/papers/harness/tools/SWE-bench.pdf#page=21|App.A.4 · p.21]]

**现实工作对齐的范围：**保留了真实代码依赖、用户需求和回归风险；本文 baseline 去掉了开发者常用的交互调试和多轮反馈，oracle 还增加了真实工程师未必知道的定位信息。验收也没有重演代码审查、长期维护与部署表现。因此它测到的是这组输入／生成／测试条件下的修复交付，不能把与人类工作有关的来源直接等同于人机同条件比较。[[raw/papers/harness/tools/SWE-bench.pdf#page=5|§§4.1–4.2 · p.5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=9|§7 · p.9]] [[raw/papers/harness/tools/SWE-bench.pdf#page=30|App.D.2 · p.30]]

## 来源、筛选和覆盖决定分数代表谁

正文以约 90,000 PR 概括候选；Table 10 的精确流水是 **93,139 PR → 11,407 转换候选 → 2,294 验证后任务**，来自 12 个流行 Python 仓库。App.A.1 说明候选检索从 2023 年 8 月下载量靠前的 PyPI 包出发；选择流行项目的理由是维护、文档、贡献规范和测试较好。这是有意选择，不是软件工作总体的随机样本。[[raw/papers/harness/tools/SWE-bench.pdf#page=2|§2.1 · p.2]] [[raw/papers/harness/tools/SWE-bench.pdf#page=16|App.A.1 · p.16]] [[raw/papers/harness/tools/SWE-bench.pdf#page=20|Table 10 · p.20]]

筛选要求 PR 已合入、关联已解决 issue、修改测试文件；将原 PR 拆成参考代码补丁与测试补丁，在修复前后运行相关测试，保留至少一个 F2P，并排除安装／运行失败。为减少要求猜新函数或类名的题，原文还排除修复前日志含 `ImportError`／`AttributeError` 的候选。后者是启发式排除，不证明剩余题目没有隐含要求。未见以某个待测模型失败为准的选题步骤。[[raw/papers/harness/tools/SWE-bench.pdf#page=16|App.A.1 · p.16]] [[raw/papers/harness/tools/SWE-bench.pdf#page=19|App.A.3 · pp.19–20]]

**覆盖支持与限制：**任务不仅是 bug，也包含功能等请求；仓库涵盖 Web 框架、可视化、机器学习、科学计算及开发工具。然而任务角色仍是维护 Python 软件，而不是直接完成这些领域的全部专业工作。Django 有 850 题、Flask 只有 11 题，按任务平均的总分明显受仓库分布影响；“12 仓库”不能直接当成 12 个职业领域的均衡覆盖。以上筛选还偏向已有成功 PR、可安装、贡献测试的工作，排除了大量真实但不易自动判分的需求。最后一句是本库根据筛选条件所作的外推边界。[[raw/papers/harness/tools/SWE-bench.pdf#page=20|Table 10 · p.20]] [[raw/papers/harness/tools/SWE-bench.pdf#page=21|App.A.5 · p.21]] [[raw/papers/harness/tools/SWE-bench.pdf#page=23|Table 12 · p.23]]

**污染与版本：**构造时仅保留 PR 初始 commit 前的问题讨论，试图避免泄漏解决细节；未来可按模型训练日期选新 issue 是作者提出的机制，不是本次已证明所有预训练数据无污染。按年份的低分／无一致趋势只能削弱简单背诵解释，不能证明没有记忆贡献。另需注意 App.A.2 为复现保留完整 mirror 历史；若后续交互 Agent 可访问它，应另核对未来提交是否被隔离，不能由本文静态 baseline 推定已解决这一泄漏通道。[[raw/papers/harness/tools/SWE-bench.pdf#page=16|App.A.1 · p.16]] [[raw/papers/harness/tools/SWE-bench.pdf#page=18|App.A.2 · p.18]] [[raw/papers/harness/tools/SWE-bench.pdf#page=26|App.C.4 · p.26]]

## Verifier 有什么证据，又没保证什么

**实际评分对象是受测行为，不是参考答案字符串。** F2P 检查修复行为，P2P 检查受测旧行为；两组都全过才记解决。只修好 F2P 却破坏 P2P 是 `Breaking Resolved`，不是成功；`FAIL_TO_FAIL` 与 `PASS_TO_FAIL` 不纳入最终验收。因此“所有测试都过”必须限定为这两组，不能理解为整仓所有测试、所有隐藏需求均通过。[[raw/papers/harness/tools/SWE-bench.pdf#page=21|App.A.4–A.5 · p.21]] [[raw/papers/harness/tools/SWE-bench.pdf#page=28|Table 22 · p.28]]

| 证据 | 实际支持 | 不能由此推出 |
| --- | --- | --- |
| PR 已合入；测试随原开发工作产生 | 需求和至少一份解决方案有真实维护流程背景 | 所有模型生成补丁会得到维护者同样认可 |
| 同一候选修复前后跑测试，要求至少一个 F2P | 空修改不能满足该判据，参考解可消除受测失败 | 测试覆盖全部需求，或所有有效替代解都会通过 |
| P2P 及缺失测试计失败 | 保护已选测试覆盖的已有功能 | 未执行的模块、长期维护和性能也安全 |
| 11 个生成结果的定性检查 | 具体案例帮助解释修复错误和风格问题 | 独立专家验收与 verifier 的总体一致率 |

定位：[[raw/papers/harness/tools/SWE-bench.pdf#page=16|App.A.1 · p.16]] [[raw/papers/harness/tools/SWE-bench.pdf#page=19|App.A.3–A.4 · pp.19–21]] [[raw/papers/harness/tools/SWE-bench.pdf#page=8|§5.1 · p.8]]。表中“不能推出”是本库分析；已读范围没有报告代表性产物的独立专业验收、误放行／误拒绝率或评审者一致性，不能将未报告写成测量无效。

**允许替代解与专业质量仍有距离。** Table 25 的 HuberRegressor 案例中，Claude 2 加入自己的布尔转浮点逻辑，通过测试；参考补丁则使用已有 `check_X_y` 的 dtype 参数。作者认为模型方案可能效率更差并带来风格／组织不一致。这提供了一个“通过测试不等于同等工程质量”的具体案例；§7 明确承认仅靠执行测试不足以保证生成代码全面、高效和易读。[[raw/papers/harness/tools/SWE-bench.pdf#page=33|App.F、Table 25 · pp.33–34]] [[raw/papers/harness/tools/SWE-bench.pdf#page=9|§7 · p.9]]

**潜在误拒也值得单独检查。** Fig.7 的分类器问题描述允许“推广支持二分类”或“报错”；图中所示测试选择了 `ValueError` 并匹配特定错误信息。**本库推断／教学反例：**若有实现正确推广二分类支持、因而不抛出该异常，它可能满足所示 issue 的一个分支却被这段测试拒绝。这是从同图的规范与断言得到的覆盖风险，不是本次运行出的误拒，不证明完整 issue／代码中没有进一步约束，更不能据一图估计错误率。[[raw/papers/harness/tools/SWE-bench.pdf#page=17|App.A.1、Fig.7 · p.17]]

## 实验测到了什么，不该怎样比较

**本文系统与预算：**GPT-3.5 为 `gpt-3.5-turbo-16k-0613`，GPT-4 为 `gpt-4-32k-0613`，另测 Claude 2 与基于 CodeLlama-Python 微调的 SWE-Llama 7B／13B。BM25 把文件填入 13k／27k／50k 上限，按模型能容纳的配置测试并报告最好结果；oracle 用参考补丁所改文件，oracle-collapsed 更使用真实编辑位置周围 ±15 行。后两者是带答案定位信息的诊断条件，不能作为无特权部署表现。[[raw/papers/harness/tools/SWE-bench.pdf#page=4|§§3–4.1 · pp.4–5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=6|Table 6 · p.6]]

每题一次 greedy 生成，没有报告多次运行的方差或置信区间。GPT-4 的 BM25 与 oracle 仅测约 25% 随机子集，oracle-collapsed 则测全量；Table 20 提供其他模型在同子集的结果，因此主表不能直接作全量等预算排名。各模型上下文长度、tokenizer、训练方式和可覆盖题目不同，Table 14 还显示生成补丁数量及自动修补率不同。论文未提供足以据此重建统一美元／时间预算的细节，本次不做显著性或效率排名。[[raw/papers/harness/tools/SWE-bench.pdf#page=5|Tables 2–4 · p.5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=24|Table 14 · p.24]] [[raw/papers/harness/tools/SWE-bench.pdf#page=27|Table 20 · p.27]] [[raw/papers/harness/tools/SWE-bench.pdf#page=30|App.D.2 · p.30]]

固定 v2 的 Claude 2 在 BM25 下解决率为 1.96%，oracle 为 4.80%；这是当时简单检索／一次生成系统的困难程度证据，**不是今日模型能力上限，也不能与 Terminal-Bench 约 63% 直接比较难度**。BM25 上下文扩展提高相关文件召回却降低解决率，说明检索信息量与模型有效利用信息不是同一个量；但不能仅靠这些结果把全部失败归因于长期规划。[[raw/papers/harness/tools/SWE-bench.pdf#page=5|Tables 2–3 · p.5]] [[raw/papers/harness/tools/SWE-bench.pdf#page=6|§5 · p.6]] [[raw/papers/harness/tools/SWE-bench.pdf#page=26|Table 18 · p.26]]

训练／测试还须分开：SWE-Llama 的约 19,000 训练候选来自另外 37 个仓库，去掉超过 30k tokens 的样本后约 10,000 条用于训练；训练候选不像测试集那样要求测试改动。仓库分离只支持这份微调数据与评测仓库的隔离，不能升级为底座预训练去污染证明。[[raw/papers/harness/tools/SWE-bench.pdf#page=4|§3 · p.4]]

## 对 Terminal-Bench 主张的定向核查

S080 §6 先分类列举相关基准，再强调专家贡献、多样长程任务，并从这些属性推到困难、真实和经济价值；随后与其他基准的 synthetic environments 作对比。**它没有明确逐一断言 SWE-bench 不真实，也没有明确声称终态评分由自己首创。** 以下反证针对宽泛措辞可能支持的强解释，保留原文实际贡献。[[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

| S080 的定位／可能的强读法 | S082 的直接证据 | 核查结论 |
| --- | --- | --- |
| 真实 shell 相对其他基准的 synthetic environments | 真实 issue、真实维护 PR、完整代码快照、原生测试框架与版本环境（S082 pp.2–3、19–21） | **限定。** shell 接口是真实的一种维度，不能把 SWE-bench 的任务和执行代码笼统归为虚构；但其原论文 baseline 的确没有交互终端闭环 |
| 结果导向允许不同解题路线（S080 §2.1） | 不比较 patch 文本；按 F2P＋P2P 验收，允许不同于参考 PR 的修改（S082 pp.3、21、33–34） | **共同属性。** 这不是终态容器验收形式完全相同，但足以排除“此前只能模仿参考轨迹”的读法 |
| 跨领域任务比软件工程评测广 | 12 个 Python 仓库仍主要测软件维护；科学库本身不等于科学工作全集（S082 pp.9、23） | **支持有限定位。** TB 在任务角色／交付类型上扩展；不能从领域数推出测量更可靠或总体职业代表性更好 |
| 专家来源确保困难、真实且经济上有价值 | 已合入维护 PR 已有现实需求，但同样未测雇佣价值、节省时间或总体代表性（S082 pp.16–21） | **削弱推论而非否定价值。** 专家／开发者来源是支持证据，不是经济价值的充分验证；两篇均需外部工作验收才能作更强外推 |
| 困难、跨步骤任务构成新增价值 | S082 已要求大仓库定位、跨文件协调，但主实验没有测交互轨迹长度（S082 pp.3–5、30） | **部分共同、部分区别。** TB 扩大连续交互操作空间有意义；不能说长上下文、跨文件依赖或复杂工作此前不存在，也不能跨年代以低分排列难度 |

比较原文定位：[[raw/papers/harness/tools/Terminal-Bench.pdf#page=2|S080 · §§1–2.1 · p.2]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]；表内 S082 定位均指本页固定 v2，详证见相应正文段落。这里比较任务、协议和证据强度，不比较跨基准模型总分。

**本库综合：**Terminal-Bench 的可信增量应放在“更广的终端工作类型＋交互环境＋逐题审查流程”的具体组合上，而不是从“真实 shell／专家出题”直接推导现实代表性、经济收益或测试完备。SWE-bench 提供了已经存在的真实软件维护和结果验收反例，同时也展示了同一种限制：现实来源、通过测试和专业认可之间仍有推论距离。该综合不证明 Terminal-Bench 任务无价值，也不确认新的研究空白。[[raw/papers/harness/tools/SWE-bench.pdf#page=9|S082 · §7 · p.9]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=4|S080 · §2.3 · pp.4–5]] [[raw/papers/harness/tools/Terminal-Bench.pdf#page=11|S080 · §6 · p.11]]

## 主题落点与验收

已整合至 [[wiki/applications/Overview|应用与评测]]、[[wiki/harness/verification|验证]] 和 [[wiki/applications/terminal-bench-comparison|跨基准审视]]，与 [[wiki/papers/harness/tools/Terminal-Bench|S080 Terminal-Bench]] 形成双向比较。主协调者回核 pp.2–3、9、20–21；原件复制哈希、链接、PDF 页码与表格转义由本轮统一检查。未复现、未审查完整测试源码，Obsidian 显示与来源跳转未实测。
