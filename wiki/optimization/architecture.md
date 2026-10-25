---
type: topic
created: 2026-10-25
updated: 2026-10-25
sources:
  - "[[raw/surveys/Towards Long-Horizon Agents.pdf]]"
  - "[[raw/papers/optimization/architecture/Longformer.pdf]]"
  - "[[raw/papers/optimization/architecture/Mamba.pdf]]"
  - "[[raw/papers/optimization/architecture/Kimi-Linear.pdf]]"
  - "[[raw/papers/optimization/architecture/GQA.pdf]]"
  - "[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf]]"
---

# 架构基础


先问长轨迹能否被表示、训练和高效处理。综述按显式上下文、压缩状态、混合架构组织历史表示方式，并将高吞吐机制作为另一条轴：解码或缓存更省，不等于旧证据一定能被准确取回。[[raw/surveys/Towards Long-Horizon Agents.pdf#page=37|S001 · §5.1 · p.37]]；[[raw/surveys/Towards Long-Horizon Agents.pdf#page=40|§5.1.3–5.1.4 · p.40]]

细分导航：Explicit-Context Architectures；Compressed-State Architectures；Hybrid Architectures；High-Throughput Mechanisms。本轮 S032–S036 已完成原文摄入与主题整合，内容与结构已验收；Obsidian 应用未测。

### 历史留在哪里，下一步怎样使用

这四种机制不能只按“支持多少 token”排列。先看历史的表示，再看模型是否仍能直接访问某个位置；最后单独核对效率。下表是本库依据已读原文构建的比较轴，不是同一基准上的性能排名。

| 机制 | 历史如何保留与访问 | 成立条件与直接证据 |
| --- | --- | --- |
| **显式 token + 稀疏连接** | Longformer 保留 token 表示，多数位置在局部窗口内交换信息，少量任务指定全局位置连通全序列 | 固定窗口和受控全局位置数支撑线性长度成本；全局位置由任务给定，不是已经学会自主识别所有重要状态。[[wiki/papers/optimization/architecture/Longformer\|S032 Longformer]]；[[raw/papers/optimization/architecture/Longformer.pdf#page=3\|§3.1、Fig.2 · pp.3–4]] |
| **有限递归状态** | Mamba 不逐 token 留存可寻址历史，让输入相关的 Δ、B、C 决定旧状态延续、写入和读出 | 内容选择与状态大小共同决定保留什么；scan 的实现解决 GPU 计算成本，不能证明任意细节都可恢复。[[wiki/papers/optimization/architecture/Mamba\|S033 Mamba]]；[[raw/papers/optimization/architecture/Mamba.pdf#page=5\|§3.1–3.3、Algorithm 2 · pp.5–7]] |
| **压缩层 + 全局层** | Kimi Linear 每三层 KDA 插入一层全局 MLA；KDA 用通道遗忘与 delta 修正更新矩阵状态，全局层保留历史访问 | 固定状态仅适用于 KDA；全模型仍保留增长的 KV 和全注意力项。3:1 是所测配置的折中。[[wiki/papers/optimization/architecture/Kimi-Linear\|S034 Kimi Linear]]；[[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=4\|§3、Eq.1 · p.4]]、[[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=6\|§4、Fig.3 · p.6]]、[[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=8\|§5.2、Table 1 · p.8]] |
| **KV 头共享** | GQA 让多组 query 共享更少的 KV 头，每个时间位置仍保留；它改变头维度存储与读取成本 | 不是时间历史压缩或检索算法；原文对照基于经 uptraining 的 T5 encoder–decoder。[[wiki/papers/optimization/architecture/GQA\|S035 GQA]]；[[raw/papers/optimization/architecture/GQA.pdf#page=2\|§2.2、Fig.2 · PDF p.2 / 印刷 p.4896]]、[[raw/papers/optimization/architecture/GQA.pdf#page=3\|§3、Table 1 · PDF p.3 / 印刷 p.4897]] |

### 容量、检索、任务质量和效率分别举证

**可运行很长，不代表所有任务都利用了那么长的历史。** Mamba 的百万长度结果包含小词表合成关联任务，以及 DNA / 音频序列；这些不能直接替代百万自然语言 token 的任意检索。Kimi Linear 主长上下文对照是 1.4T 训练后的 128k 测试，而 1M RULER 属于另一个 5.7T checkpoint；不能把两组结果拼成同一个受控实验。[[raw/papers/optimization/architecture/Mamba.pdf#page=10|S033 §4.1 · pp.10–11]] [[raw/papers/optimization/architecture/Mamba.pdf#page=13|§4.3–4.4 · pp.13–14]] [[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=12|S034 §5.5、Table 5 · p.12]] [[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=28|Appendix D · p.28]]

**显式访问也需要行为检查。** [[wiki/papers/optimization/architecture/Lost-in-the-Middle|S036 Lost in the Middle]] 固定问题和证据、改变证据位置，在所测旧模型的多文档 QA 中观察到位置差异；但 Claude 的合成 KV 检索近乎完美，Llama-2 7B 主要呈近因偏好。因此它支持“检查位置和干扰”的评测要求，不建立所有模型都遵守的 U 形定律，也没有直接评测 Mamba 或 Kimi Linear。[[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=5|S036 §2.3、Fig.5 · p.5]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=7|§3.2、Fig.7 · p.7]] [[raw/papers/optimization/architecture/Lost-in-the-Middle.pdf#page=16|Appendix E、Fig.16 · p.16]]

**吞吐结果保留部署条件。** Mamba 的生成比较在 A100、2048-token prompt、128-token 输出下改变 batch；Kimi Linear 的 batch=1 图与扩大 batch 后约 6.3× 的论述不能混用；GQA 则按各模型优化批量与分片。它们说明资源配置下的计算行为，不是完整 Agent 运行耗时或成功率。模型质量、任务成功与工具等待需另行测量。[[raw/papers/optimization/architecture/Mamba.pdf#page=36|S033 Appendix E.5 · p.36]] [[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=13|S034 Fig.7 · p.13]] [[raw/papers/optimization/architecture/Kimi-Linear.pdf#page=16|§6.3 · p.16]] [[raw/papers/optimization/architecture/GQA.pdf#page=3|S035 §3.1–3.2 · PDF p.3 / 印刷 p.4897]]

**待检验阅读问题，尚未查新：**当未来目标尚未出现时，压缩状态需要保留哪些关联，全局访问又能恢复哪些细节？将位置/干扰检查迁移到 Agent 轨迹时，必须保持任务语义和时序依赖，不能任意洗牌后仍当成同一任务。现有证据让问题具体化，尚未证明它是未被研究的缺口；与 [[wiki/harness/memory|运行时状态选择]] 共同讨论。

## 论文入口与交叉方向

- [[wiki/papers/optimization/architecture/Longformer|S032 · Longformer]]：主归属。
- [[wiki/papers/optimization/architecture/Mamba|S033 · Mamba]]：主归属。
- [[wiki/papers/optimization/architecture/Kimi-Linear|S034 · Kimi-Linear]]：主归属。
- [[wiki/papers/optimization/architecture/GQA|S035 · GQA]]：主归属。
- [[wiki/papers/optimization/architecture/Lost-in-the-Middle|S036 · Lost-in-the-Middle]]：主归属。

[[wiki/optimization/Overview|返回模块地图]] · [[maintenance/research/R001|本轮选读理由与维护记录]]。
