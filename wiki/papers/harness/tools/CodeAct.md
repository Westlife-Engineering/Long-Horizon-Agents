---
type: paper
primary_direction: harness/tools
related_directions:
  - optimization/finetuning
source_id: S014
created: 2026-10-25
updated: 2026-10-25
reading_status: body-and-selected-appendices-read
ingest_status: complete
sources:
  - "[[raw/papers/harness/tools/CodeAct.pdf]]"
---

# CodeAct：以可执行程序作为动作

CodeAct 让模型一次输出一段 Python，用变量保存中间结果、用控制流组合工具，并在执行后根据结果或异常继续行动。需要分开看两项贡献：**CodeAct 是动作表示和执行循环；CodeActInstruct / CodeActAgent 是交互轨迹数据与训练后的模型。** 前者的零样本格式比较不能与后者的微调收益合并归因。[[raw/papers/harness/tools/CodeAct.pdf#page=3|§2.1、§3 · pp.3–8]]

## 来源与阅读范围

| 项目 | 记录 |
| --- | --- |
| ID / 标题 | S014 / Executable Code Actions Elicit Better LLM Agents |
| 作者 | Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, Heng Ji |
| 版本 | ICML 2024，PMLR 235:50208–50232；正式渠道 PDF，共 25 页 |
| 原始 URL / 访问日 | [PMLR](https://proceedings.mlr.press/v235/wang24h.html)；[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/wang24h/wang24h.pdf)；2026-10-25 |
| 原件 / SHA-256 | [[raw/papers/harness/tools/CodeAct.pdf\|CodeAct.pdf]]；`4EBE01E45888404DDF8F2513DC7935D1CB300A830ADAEA0B8AC2F1BFF66B5519` |
| 归档与页码 | 下载文件 wang24h.pdf 原样归档；本文用 PDF 页码，与 PDF 页脚 1–25 一致，区别于 PMLR 卷内页码 |
| 读取 | 2026-10-25；正文 §§1–5 与 Impact Statement（pp.1–9）；附录 A–F、G.1–G.2（pp.14–18）、H（pp.24–25）；G.3 的长篇生成示例仅定位，未逐行核读 pp.19–24，参考文献未逐项核验 |
| 原页图表 | 已看 Fig.1、Tables 2–3、Table 5、Tables A.6–A.8 图像；本文无承担核心论证的专门数学公式 |
| S001 | [[raw/surveys/Towards Long-Horizon Agents.pdf#page=27\|§4.3.2 · pp.27–28 · 引文656]]；书目 p.128 |

## 改变的是动作粒度和反馈入口

模型既能向用户说自然语言，也能向 Python 解释器提交代码。一次代码动作可以调用多个工具、保存对象、循环和分支；解释器结果及异常回到后续上下文，使模型修订后续动作。代码本身的条件分支与模型在下一轮重新决策是两层控制，不应混为同一种“反思”。[[raw/papers/harness/tools/CodeAct.pdf#page=2|§1 · Fig.1 · p.2]] [[raw/papers/harness/tools/CodeAct.pdf#page=3|§2.1 · Fig.2 · pp.3–4]]

| 层次 | 状态怎样改变 | 反馈何时出现 |
| --- | --- | --- |
| 一段代码内部 | 变量存结果，循环/分支组合函数调用 | 由代码逻辑处理返回值，尚未要求模型重采样 |
| Agent 多轮循环 | 将代码输出或异常加入观察，模型决定下一段程序或答案 | 解释器完成本轮动作后 |
| CodeActAgent 训练 | 对筛选后的交互轨迹做监督微调 | 参数更新发生在离线训练，而非每次运行时自动训练 |

这张表是本库按原文机制整理；依据 [[raw/papers/harness/tools/CodeAct.pdf#page=3|§2.1 · pp.3–4]] 与 [[raw/papers/harness/tools/CodeAct.pdf#page=7|§3.1–3.2 · pp.7–8]]。现成 Python 软件扩大可达能力，但前提是库、工具接口、执行环境与必要观察可用；少轮数并不直接表示少底层 API 调用或低总成本。

## 先核对动作表示实验，再看微调实验

**表示比较。**17 个现成模型在 API-Bank level-1 生成单次原子调用，用执行输出匹配衡量正确率；这部分限制为单工具动作，主要观察格式适配。Table 2 并非 CodeAct 全胜：部分 GPT 模型的 JSON 更好。M³ToolEval 则有 82 个人工任务，允许代码组合工具，最多 10 轮，以答案 exact match 判成功。[[raw/papers/harness/tools/CodeAct.pdf#page=4|§2.2–2.3 · pp.4–5]]

Table 3 中 GPT-4-1106-preview 的 CodeAct / JSON / Text 成功率为 74.4 / 52.4 / 53.7%，平均轮数为 5.5 / 7.6 / 7.7；这说明在本文接口与上限下，代码组合有实际用途。**重要限定：**JSON 与 Text 提示明确每轮只能调用一个工具，代码可在一轮循环调用多个，所以这是“动作表示连同执行能力”的比较，不是给定等量底层调用后的纯语法比较。[[raw/papers/harness/tools/CodeAct.pdf#page=5|Table 3 · p.5]] [[raw/papers/harness/tools/CodeAct.pdf#page=17|附录 F.3–F.5 · p.17]]

**训练比较。**CodeActInstruct 从 HotpotQA、MATH、APPS、WikiTableQuestions 和 ALFWorld 生成成功轨迹，筛选多轮及可从错误恢复的行为，最终 7,139 条；再混入 69,230 条通用对话。Llama-2 / Mistral 7B 做全参数 SFT；附录 D 为 4×A100 40GB、5 epochs，实验用第 3 epoch。原文中的 robot planning 数据是 ALFWorld 文本模拟器，不能写成真机器人训练验证。[[raw/papers/harness/tools/CodeAct.pdf#page=6|§3.1、Table 4 · pp.6–7]] [[raw/papers/harness/tools/CodeAct.pdf#page=16|附录 D · p.16]] [[raw/papers/harness/tools/CodeAct.pdf#page=18|G.2 · p.18]]

Table 5 对 MINT 分开域内/域外，常规预算 5 轮；还有 M³ToolEval、MiniWoB++、ScienceWorld 及通用能力任务。Mistral 版在 M³ToolEval 为 12.2%，Llama-2 版仍为 0。附录 H 将后者归因候选指向预训练异常或基础能力，作者无原预训练数据验证，因此这里只记为假说。通用能力也不是一概无损，Mistral 的 MMLU 有下降；Table A.8 表明通用对话混合有维护能力的作用，不能把全部微调收益归给纠错轨迹。[[raw/papers/harness/tools/CodeAct.pdf#page=8|§3.2、Table 5 · p.8]] [[raw/papers/harness/tools/CodeAct.pdf#page=14|Table A.8 · p.14]] [[raw/papers/harness/tools/CodeAct.pdf#page=24|附录 H · pp.24–25]]

## 长程解释与比较边界

**本库推断：**代码把多步局部依赖压进一次可执行动作，变量承担部分中间状态；反馈驱动重写则保留开放的下一轮控制。这能减少模型交互次数，但不能据此宣称解决跨会话记忆或任意持续时长任务。作者自身也提醒模型可能不打印变量就臆测内容，执行代码不是对所有输出的正确性证明。[[raw/papers/harness/tools/CodeAct.pdf#page=9|Impact Statement · p.9]]

附录 A 明确把 Voyager 视为会迭代修复代码的例外，因此不能把先前所有代码 agent 概括为单轮。两者区别应围绕程序动作粒度、观察暴露和技能存储，而不是“是否使用反馈”二分；本批 Voyager 原文的交叉核查见其唯一论文页。TaskWeaver 等比较仍为作者论述，本次未读取其原论文。[[raw/papers/harness/tools/CodeAct.pdf#page=15|附录 A–B · p.15]]

**待检验问题：**如果同时匹配底层工具调用数、执行时间与失败副作用，代码组合相对逐步调用的收益及恢复代价如何变化？本文提供动作粒度这一比较轴，尚不足以宣布新的领域缺口。

## 整合与验收

已整合至 [[wiki/harness/tools|工具、MCP 与技能]] 与 [[wiki/optimization/finetuning|微调的工具接口]]，内容与结构验收通过。未复现实验；Obsidian 表格和来源跳转尚未实测。

## 分类与阅读入口

主归属与交叉方向：[[wiki/harness/tools|harness/tools]] · [[wiki/optimization/finetuning|optimization/finetuning]]。
