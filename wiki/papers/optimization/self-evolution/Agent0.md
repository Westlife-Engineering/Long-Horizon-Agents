---
type: paper
primary_direction: optimization/self-evolution
source_id: S064
created: 2026-10-25
updated: 2026-10-25
reading_status: problem-driven-read
ingest_status: complete
sources:
  - "[[raw/papers/optimization/self-evolution/Agent0.pdf]]"
---

# Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning

## 来源与实际阅读

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S064 |
| 作者 | Peng Xia、Kaide Zeng、Jiaqi Liu、Can Qin、Fang Wu、Yiyang Zhou、Caiming Xiong、Huaxiu Yao |
| 版本 | arXiv:2511.16043v2，2026-09-21；PDF标注COLM 2026；DOI 10.48550/arXiv.2511.16043 |
| 原始入口 | [Agent0](https://arxiv.org/abs/2511.16043v2)；访问2026-10-25 |
| 原件 | [[raw/papers/optimization/self-evolution/Agent0.pdf\|本地PDF，共23页]] |
| SHA-256 | `0E7D3EB30168C97F1C50AF433FE48326C79DFD14EDF326CC1FAC14DFA296B52C` |
| 实际阅读 | 2026-10-25；正文pp.1–10；附录A–D pp.16–20超参数、提示、沙箱、评测与轮次，F p.23算法；看pp.4–6奖励/ADPO公式、p.8消融/循环曲线及p.19轮数表。pp.21–22案例未逐题核验。 |
| S001定位 | 引文704，§5.7.2，PDF p.55；书目 pp.132 |

正文PDF页码与印刷页码一致。未逐项核读参考文献，未审查代码或复现实验。

## 代码反馈扩展能力，最终标签仍为多数票

Agent0把Python解释器接入出题者—执行者循环，并改变课程奖励与策略更新。两者从同一base模型初始化，交替冻结后训练；没有外部训练题/人工答案，仍依赖预训练模型、数学出题提示、工具实现和奖励规则。它与[[wiki/papers/optimization/self-evolution/R-Zero|R-Zero]]最重要的比较轴是增加了外部计算反馈，而非从零知识开始。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=3|§3.1–3.2、Figure 2 · pp.3–4]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=17|附录A.2–A.3 · p.17]]

| 信号 | 用途 | 有限含义 |
| --- | --- | --- |
| 答案一致率 | 出题难度、筛任务、调更新权重 | 自身众数一致，不等于正确 |
| Python结果/报错 | 插入上下文继续推理 | 未替换多数票最终标签 |
| 工具调用次数 | 给课程Agent奖励，有封顶 | 诱发调用不证明调用必要 |
| 伪标签匹配 | executor轨迹终局0/1奖励 | 不是独立真值验证 |

依据[[raw/papers/optimization/self-evolution/Agent0.pdf#page=4|§3.2 · Eq.2–5 · p.4]]、[[raw/papers/optimization/self-evolution/Agent0.pdf#page=5|§3.3.1 · Eq.6–7 · p.5]]；第三列为本库解释。调用计数依输出标记，封顶的设计意图是避免无效堆调用，不能因此认定代理奖励投机已被排除。

## 多轮轨迹与ADPO改变什么

出现Python代码块时生成暂停，沙箱执行并返回stdout/stderr，再放回历史继续，直到最终答案。这是工具调用—观察—继续推理的轨迹；附录D.1另做1–4轮课程交互实验，不能合并成已经验证真实长程浏览/办公。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=5|§3.3.1 · p.5]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=17|A.3 · pp.17–18]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=19|D.1、Table 9 · p.19]]

ADPO对低一致率题降低advantage权重，同时放宽上方clipping范围，分别减弱噪声标签牵引与允许低概率轨迹探索；它没有纠正伪标签本身。正文以单调函数描述缩放与clip，已核读材料未明确全部函数实现，不能据此宣称复现。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=5|§3.3.2、Eq.8 · pp.5–6]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=23|Algorithm 1 · p.23]]

## 三轮有效性与长期稳定不能互换

实验为Qwen3-4B/8B-Base，数学出题后评测数学及SuperGPQA/MMLU-Pro/BBEH；通常greedy pass@1，AMC/AIME是mean@32。base加工具本身已有收益，完整方案优势不能全部归于共演化。数学评测另用GPT-4o judge；预训练污染或生成题/测试题去重本次未核实。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=6|§4.1、Tables 1–2 · pp.6–7]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=18|Table 8、附录C · pp.18–19]]

Table 3消融课程训练、工具奖励、重复惩罚、ADPO和多轮，支持其在所测条件的作用。Figure 4仅覆盖三个共演化轮次；Table 5固定首轮executor测新题通过率下降、工具次数上升，说明“相对该executor更难且更用工具”，不证明内在难度、质量或长期稳定性单调上升。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=8|§4.3、Tables 3–5、Figure 4 · pp.8–9]]

## 报告歧义与核查项

- 公式为 $|\hat p-0.5|\le0.25$，10次取样应保留3–7个一致答案，§4.1却写0.3–0.8；未读代码不消解该差异。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=5|Eq.7 · p.5]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=6|§4.1 · p.6]]
- Tables 2–4的Overall/General AVG列集合不同；Table 2还列MATH AVG，而Table 4单列General。不能直接搬用摘要18%/24%作为统一增益或跨论文排名。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=7|Tables 1–2 · p.7]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=8|Tables 3–4 · p.8]]
- 正文称工具促进双方，但附录curriculum提示主要是数学出题；课程Agent直接调用工具权限、多轮生成协议尚需代码核实。可以确认executor沙箱回路，不扩写成双方任意工具环境共同演化。[[raw/papers/optimization/self-evolution/Agent0.pdf#page=2|Figure 1 · p.2]] [[raw/papers/optimization/self-evolution/Agent0.pdf#page=17|Table 7、A.3 · p.17]]

**本库综合：**“无外部数据”与“无外部信息”不同，Python提供外部计算信息。三轮成绩尚未回答R-Zero已有更长迭代失稳；可保留反馈来源、伪标签可靠性与长期稳定的联合诊断问题，尚未完成新颖性查新。

## 主题联系与验收

已整合至 [[wiki/optimization/self-evolution|Optimization · 自我演化]]，论文与主题互链、队列及索引已同步；内容与结构经主Agent验收通过，Raw哈希匹配，已完成摄入。Obsidian渲染、操作与来源跳转未测。

返回 [[wiki/index|索引]]。

## 分类与阅读入口

主归属与交叉方向：[[wiki/optimization/self-evolution|optimization/self-evolution]]。
