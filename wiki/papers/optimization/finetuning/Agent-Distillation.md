---
type: paper
primary_direction: optimization/finetuning
related_directions:
  - harness/tools
source_id: S049
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/finetuning/Agent-Distillation.pdf]]"
---

# Distilling LLM Agent into Small Models with Retrieval and Code Tools

## 来源与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S049 |
| 作者 | Minki Kang、Jongwon Jeong、Seanie Lee、Jaewoong Cho、Sung Ju Hwang |
| 版本 | NeurIPS 2025正式会议PDF；身份以本地PDF首页为准 |
| 原始入口 | [NeurIPS proceedings](https://papers.nips.cc/paper_files/paper/2025/hash/99263f9bf46874e2b8b7f104b5063864-Abstract-Conference.html)；访问2026-10-25 |
| Raw | [[raw/papers/optimization/finetuning/Agent-Distillation.pdf\|本地PDF，共38页]] |
| SHA-256 | `b5cdc342bbbd0be2aa4b170f314516a6a3e23004ba68565b07d0dc6f4e43f710` |
| 实际阅读 | 2026-10-25；正文及局限pp.1–10，附录A–D说明pp.20–23；看p.4 Eq.3–4、p.5 Fig.3/Eq.5、p.7 Tables2–3、p.8 Table4/Fig.4、p.20局限原页。pp.24–31详细提示/逐条案例及pp.32–38 checklist未完整核读，引用文献未逐条核验。 |
| 综述定位 | S001引文269，§5.4.3，PDF pp.46–47；书目p.97 |

以下为直接原文证据和明确标注的本库分析；未复现实验。PDF页码与印刷页码相同。

## 核心理解：学会调用外部能力，还需要保留推理与选择的条件

小模型模仿教师CoT，不一定能记住罕见事实或完成准确计算。本文把监督对象扩展为“思考—代码动作—环境观察”轨迹：学生学习如何搜索和运行代码，并在新观察后继续行动。其参数更新是离线教师轨迹SFT，**观察来自环境且不计损失**；不是在学生当前在线状态上查询教师，也不是逐token软分布蒸馏。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=4|§3–4、Eq.2–4 · p.4]]

论文同时改变训练数据与推理时策略，二者需要分开：

| 机制 | 发生阶段与实际操作 | 边界 |
| --- | --- | --- |
| Agent Distillation | 教师用CodeAct风格交互，保留答案正确的轨迹；学生监督学习thought/action | 仍是固定教师访问状态；数据含环境反馈不等于学生在线学习 |
| first-thought prefix（FTP） | 先让教师在CoT提示下生成初始推理，再把首步接到agent首个thought前缀，生成更好的示范 | 仅用于教师轨迹生成；学生推理无需额外FTP调用 |
| self-consistent action generation（SAG） | 测试时每步采N个thought/action，执行代码，过滤解析/执行错误，再按观察结果多数选择 | 增加运行时采样和执行成本；输出一致不等于事实/任务正确 |

依据：[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=5|§4、Fig.3、Eq.5 · p.5]]。SAG若所有候选均失败，会随机保留一个失败动作，把错误返回给后续步骤修正；它没有保证每一步可执行。该工作建立在 [[wiki/papers/harness/tools/CodeAct|CodeAct]] 的代码动作接口上，原论文在本库已独立摄入。

## 实验范围：最多5步的检索与数学任务

教师 Qwen2.5-32B-Instruct，学生为已指令训练的Qwen2.5 0.5/1.5/3/7B；另测Llama-3.2-1B和Phi-4-mini。训练抽取1000 HotpotQA hard和2000 MATH问题，每题生成一条教师轨迹，按答案过滤后约2000条；各方法实际通过数不同，不能视为完全等样本训练。学生用全线性层LoRA rank64，2 epochs、batch8、lr2e-4，4张A100-80GB。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=6|§5 · p.6]]、[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=20|Appendix C/D.1 · pp.20–21]]

检索与RAG共同使用Wikipedia 2018和e5-base-v2，而不是开放实时搜索。四个事实任务是HotpotQA、Bamboogle、MuSiQue、2WikiMultiHopQA；四个数学任务为MATH500、GSM-Hard、AIME、OlymMATH。事实题用GPT-4o-mini判分，数学用exact match；各集最多500题，AIME90题，测试agent最多5步，SAG主设N=8、温度0.4。这里直接支持有限步工具增强推理，不支持长时间自主浏览或持久状态管理。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=6|§5、Table1 · p.6]]

主表显示较强的工具收益，但不是每项都涨：3B完整方法八任务平均36.60，高于7B CoT-distill的33.54；同时3B MATH500为60.2，低于同规模CoT-distill61.8，7B对应67.8也低于72.6。纯SAG对3B AIME甚至从6.7降到0，加入FTP后才升至15.6。因此“更小模型匹敌更大模型”须限定为该混合平均、额外工具和推理采样条件。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=7|Table2 · p.7]]

## 成效归因和限制

FTP在较难数学题帮助更明显，但事实任务中可能减少检索、促使模型直接凭内部知识回答；作者认为这增加幻觉风险。工具提供计算能力，不替代概念推理，precalculus失败分析包括角度范围理解错误。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=8|§7、Fig.4 · pp.8–10]]、[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=21|Appendix D.2–D.3 · pp.21–22]]

效率要同时计算模型token、每步候选数、检索/代码执行和延迟。论文Fig.5用采样数比较CoT自一致与SAG，Fig.6比较生成token；这些不足以证明完整系统成本相同或所有场景更快。本库分析：SAG把动作执行用于筛选，在有外部副作用的环境中，需另证隔离、重放或提交规则，本文检索/数学实验未给出通用解法。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=9|§7、Figs.5–6 · p.9]]、[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=20|Appendix A · p.20]]

**版本内部未同步：**附录A p.20仍说仅实验Qwen系列、未测Llama，但正文p.8 Table4已列Llama-3.2-1B和Phi-4-mini；应按可见主表登记已有结果，而不能照抄该局限。Fig.1列1.5B完整方法平均30.9，Table2为30.55；本页采用具体主表，不拼接数字。[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=1|Fig.1 · p.1]]、[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=7|Tables2–3 · p.7]]、[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=8|Table4 · p.8]]、[[raw/papers/optimization/finetuning/Agent-Distillation.pdf#page=20|Appendix A · p.20]]

最接近的CoT蒸馏工作在本页仅作为作者设置的对照，不因相关工作段落而获独立核读身份。单教师、每题单轨迹、知识库年份和只验证答案的筛选都限制状态/行为覆盖；无法据此确认领域通用最优蒸馏策略。

## 主题联系与验收

已整合至 [[wiki/optimization/finetuning|微调]]，并为 [[wiki/harness/tools|工具接口]] 提供“参数学习与测试时选择共同改变结果”的联系；已整合至工具方向的运行时筛选比较。本库待检验问题是：在同等总执行预算下，失败恢复来自训练示范、反馈利用还是SAG筛选？尚未查新，不称研究缺口。

Optimization、Harness、索引、队列、互链与摄入日志已同步；主 Agent 内容与结构验收通过，Raw哈希匹配。Obsidian应用未测，未复现实验。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/finetuning|optimization/finetuning]] · [[wiki/harness/tools|harness/tools]]。
