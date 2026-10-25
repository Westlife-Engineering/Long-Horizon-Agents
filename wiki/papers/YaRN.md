---
type: paper
source_id: S043
created: 2026-10-25
updated: 2026-10-25
reading_status: targeted-primary-read
ingest_status: complete
sources:
  - "[[raw/papers/YaRN.pdf]]"
---

# YaRN: Efficient Context Window Extension of Large Language Models

**核心判断：**YaRN 通过按频率分段调整 RoPE，再缩放 attention logits，使已有模型较省训练地适配更长输入。它直接改变位置表示和注意力分布；实验主要覆盖语言建模、简单 passkey 检索及短任务保持，不等于验证持续任务状态管理。[[raw/papers/YaRN.pdf#page=4|§3 · pp.4–6]] [[raw/papers/YaRN.pdf#page=7|§4 · pp.7–9]]


## 来源身份与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S043 |
| 作者 | Bowen Peng、Jeffrey Quesnelle、Honglu Fan、Enrico Shippole |
| 版本 | arXiv:2309.00071v3，2026-02-06；S001 [477] 指向 ICLR 2024，未与会议版逐段对齐，本页只描述本地 v3 |
| 原始渠道 | [原始发布页](https://arxiv.org/abs/2309.00071v3)；[固定 PDF](https://arxiv.org/pdf/2309.00071v3)；访问 2026-10-25 |
| 本地原件 | [[raw/papers/YaRN.pdf\|YaRN.pdf，共 20 页]] |
| SHA-256 | `E7C0268A796138460C6BA2F67A7CBA5BD922C401AEA94C1FCD09C4B76B883C85` |
| 阅读日期与范围 | 2026-10-25；正文 pp.1–10；附录 A pp.13–15、B pp.16–20；参考文献未逐项核读；看 p.3 Eq.9、p.5 Eqs.10–13、p.6 Eqs.14–15、p.8 Fig.3/Table1、p.19 Table9–10 原页 |
| S001 选择依据 | 引文 [477]，§5.3.2，PDF pp.44；参考文献 PDF p.114；正文角色和书目已回读核对 |

本页按本地 PDF 第一页起计页码。网页只用于身份核对，学术主张以已归档 PDF 为依据；未复现实验。原始下载文件为 `.research-tmp/S043-download.pdf`，归档前后字节与哈希一致。主题、索引、互链与摄入日志已同步；主 Agent 已完成内容与结构验收，Raw 哈希匹配。Obsidian 应用未测。


## 为什么不能把所有位置频率一起缩小

原训练长度 L 外的 token 会使部分 RoPE 维度进入训练未覆盖的相位范围；但对所有维度同等插值，又会损害近邻区分。作者以旋转次数 r=L/λ 区分维度：长波长/低频做插值，短波长/高频保留，中间平滑混合。这里“低频更偏绝对位置、高频更偏相对位置”是作者的机制解释，不能当作逐神经元已验证的功能分工。[[raw/papers/YaRN.pdf#page=4|§3.1–3.2 · pp.4–5]]

| 部件 | 运算与作用 | 适用前提 |
| --- | --- | --- |
| NTK-by-parts | 保留位置 m，改频率为 (1−γ)θ/s+γθ；γ 随旋转次数从0升至1 | 依原始窗口及频率确定分段；Llama 实验用 α=1、β=32，作者要求按模型调参。[[raw/papers/YaRN.pdf#page=5\|§3.2、Eqs.10–13 · p.5]] |
| attention scaling | softmax 前除以温度 t；推荐 1/√t=0.1 ln(s)+1 | 该系数是 LLaMA 上按困惑度拟合，不能当架构无关理论最优值。[[raw/papers/YaRN.pdf#page=6\|§3.3、Eqs.14–15 · p.6]] |
| Dynamic Scaling | 推理时令 s=max(1,l′/L)，随当前长度改变 | KV cache 与 RoPE 缓存须保持位置一致；不是任意已有旋转 cache 都能直接复用。[[raw/papers/YaRN.pdf#page=6\|§3.4 · p.6]] |

> [!warning] 本地版本有需要保留的公式不一致
> p.3 Eq.9 写 PI 的 g(m)=s·m，但本页已定义 s=L′/L；附录 p.13 Eq.16 则写 mL/L′，两者方向相反。已实际查看 p.3 原页，非抽取文本错误。本文解释沿用 §3.2 的 θ/s 和附录的压缩位置含义，不静默修改 Raw，不把 Eq.9 原样当实现规范。[[raw/papers/YaRN.pdf#page=3|§2.2–2.3、Eq.9 · p.3]] [[raw/papers/YaRN.pdf#page=13|Appendix A.1、Eq.16 · p.13]]

## 128K 结果是怎样训练和测出的

Llama 2 7B/13B 在 PG19 的 64K chunks 上先训练 s=16、400 steps，再从该 checkpoint 训练 s=32、额外200 steps；后者训练序列仍为64K，测试扩到128K。Global batch=64，模型架构不额外增加新的记忆模块。不能把400+200写成从零只训200 steps。[[raw/papers/YaRN.pdf#page=7|§4.1 · p.7]]

Table1 用十个至少128K tokens 的 Proof-pile 测试文档、stride256滑窗困惑度；Table9 的128K passkey结果是各已测试长度的平均，而不是“每个位置/每个128K任务均99.4%成功”。Passkey 是无意义干扰中的五位数字，所需推理远少于复杂轨迹状态重建。[[raw/papers/YaRN.pdf#page=8|§4.2–4.3、Table1、Fig.3 · p.8]] [[raw/papers/YaRN.pdf#page=18|Appendix B.5、Table9 · pp.18–19]]

同训练步数的 LLaMA7B/32K 消融支持分段频率与温度组合的效果；Appendix B.2 的400 vs1000 steps是指定8K PI对照，不能把摘要中的“10×更少token/2.5×更少steps”泛化成任何模型的保证。Table4跨公开模型效率比较还含不同数据、长度、规模条件，不是统一算力对照。[[raw/papers/YaRN.pdf#page=8|Fig.3 · p.8]] [[raw/papers/YaRN.pdf#page=9|Table4 · p.9]] [[raw/papers/YaRN.pdf#page=17|Appendix B.2、Table6 · p.17]]

## 窗口延展与真实利用之间

作者自己指出困惑度不能完整预测检索能力，短任务表也有 MMLU 等下降，因而结论里的“no downsides”不能按字面升级为无代价定理。[[raw/papers/YaRN.pdf#page=9|Table2–3 · p.9]] [[raw/papers/YaRN.pdf#page=19|Appendix B.5–B.6 · p.19]]

与本批 [[wiki/papers/ProLong|ProLong]] 的区别是证据目标和训练预算：后者继续预训练后用多类下游任务、SFT前后与短能力保持评估，不能把它的不同配方视为直接否定YaRN。[[wiki/papers/DeepSeek-V3|DeepSeek-V3]] 使用YaRN也是另一模型上的扩窗应用，不是原实验复现。下一步应问目标Agent是否能利用跨步证据，而不是只问接受的token上限；暂属评测要求，不认定新颖性。

## 本库落点与下一条证据

已整合到 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]，主题与本页双向关联。相关方法的比较以本文实际实验为限，未核读的引用不成为独立来源。返回 [[wiki/index|索引]]。
