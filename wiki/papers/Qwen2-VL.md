---
type: paper
source_id: S045
created: 2026-10-25
updated: 2026-10-25
reading_status: targeted-primary-read
ingest_status: complete
sources:
  - "[[raw/papers/Qwen2-VL.pdf]]"
---

# Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution

**核心判断：**Qwen2-VL 既有多模态感知机制，也有基于 Qwen-Agent 的多轮任务实验。应保留这部分正面证据，同时区分视觉问答、动作匹配与完整任务成功；实验没有单独把Agent收益归因给M-RoPE、动态分辨率或预训练。[[raw/papers/Qwen2-VL.pdf#page=4|§2.1 · pp.4–5]] [[raw/papers/Qwen2-VL.pdf#page=10|Table5 · p.10]] [[raw/papers/Qwen2-VL.pdf#page=12|§3.2.7 · pp.12–13]]


## 来源身份与阅读范围

| 项目 | 记录 |
| --- | --- |
| 来源 ID | S045 |
| 作者 | Peng Wang、Shuai Bai、Sinan Tan、Shijie Wang、Zhihao Fan、Jinze Bai、Keqin Chen、Xuejing Liu、Jialin Wang、Wenbin Ge、Yang Fan、Kai Dang、Mengfei Du、Xuancheng Ren、Rui Men、Dayiheng Liu、Chang Zhou、Jingren Zhou、Junyang Lin |
| 版本 | arXiv:2409.12191v2，2024-10-03；S001引同一arXiv作品但未指定版本 |
| 原始渠道 | [原始发布页](https://arxiv.org/abs/2409.12191v2)；[固定 PDF](https://arxiv.org/pdf/2409.12191v2)；访问 2026-10-25 |
| 本地原件 | [[raw/papers/Qwen2-VL.pdf\|Qwen2-VL.pdf，共 52 页]] |
| SHA-256 | `30BB0F6C9BABF910295D6B7CD34B6F54824236F68782664C3C93FBF4803275D0` |
| 阅读日期与范围 | 2026-10-25；正文 pp.1–16（架构/三阶段训练/视觉与视频实验/Agent/消融）；看 pp.4–5 Fig.2–3、p.10 Table5、pp.14–15 Table7–8/Fig.4–5；pp.17–52 的参考文献及演示附录未系统核读，不据演示声称普遍任务成功 |
| S001 选择依据 | 引文 [644]，§5.3.3，PDF pp.44；参考文献 PDF p.127；正文角色和书目已回读核对 |

本页按本地 PDF 第一页起计页码。网页只用于身份核对，学术主张以已归档 PDF 为依据；未复现实验。原始下载文件为 `.research-tmp/S045-download.pdf`，归档前后字节与哈希一致。主题、索引、互链与摄入日志已同步；主 Agent 已完成内容与结构验收，Raw 哈希匹配。Obsidian 应用未测。


## 视觉输入怎样成为可用上下文

| 环节 | 机制 | 解决的问题与保留条件 |
| --- | --- | --- |
| 动态分辨率 | ViT用2D-RoPE，按图像尺寸产生可变token；MLP将相邻2×2 token合并 | 保护细节和长宽比，同时控制输入开销；“any resolution”受像素、token和显存预算约束。[[raw/papers/Qwen2-VL.pdf#page=4\|§2.1、Fig.2 · p.4]] |
| M-RoPE | temporal/height/width三组位置；文字三组ID相同，图像时间不变，视频时间递增 | 表达空间和时间关系，位置ID跨度不同于把一切摊成1D；并非显式三维世界模型。[[raw/papers/Qwen2-VL.pdf#page=5\|§2.1、Fig.3 · p.5]] |
| 图像视频统一 | 视频2fps采样、时间深度2的3D卷积；图像视为两相同帧 | 训练每视频最多16384 tokens，通过帧分辨率调节预算；采样和压缩可能损失细节。[[raw/papers/Qwen2-VL.pdf#page=5\|§2.1 · p.5]] |
| 训练适配 | 先训ViT，再全参数，最后冻结ViT训LLM；SFT含多模态对话和Agent交互 | 前两阶段合计1.4T包含图像及文本tokens，但只监督文本tokens，不能当1.4T纯文本监督量。[[raw/papers/Qwen2-VL.pdf#page=5\|§2.2 · pp.5–7]] |

这里改变的是观察编码、语言模型参数和交互格式。闭环运行仍须外部执行动作并返回图像；M-RoPE本身不会执行工具、验证目标或保存跨会话记忆。下面是本库按§2.2.1和§3.2.7重绘的信息流。

```mermaid
flowchart LR
 O[当前图像观察] --> C[与观察动作历史组成上下文]
 C --> M[Qwen2-VL 推理与选择动作]
 M --> T[Qwen-Agent 执行动作]
 T --> E[环境转移]
 E -->|返回新观察| O
```

Agent实验保留32K上下文内的历史，动作后追加观察。不能把视频长度外推到80K的结果直接当作Agent实验也使用80K。[[raw/papers/Qwen2-VL.pdf#page=7|§2.2.1 · p.7]] [[raw/papers/Qwen2-VL.pdf#page=13|§3.2.7 · p.13]] [[raw/papers/Qwen2-VL.pdf#page=15|§3.3.2 · p.15]]

## 哪些确实是 Agent 证据

Table5的Agent结果针对72B模型，模型和环境配置、反馈类型各不相同，不能合并成一个通用成功率。

| 任务 | 报告指标与实现 | 可支持到哪里 |
| --- | --- | --- |
| 内部视觉function calling | TM函数类型、EM参数匹配；图像经LVLM提取信息后由LLM构造问答/调用 | 直接测选择与参数，不直接测完整任务完成；评测数据构造依赖模型。[[raw/papers/Qwen2-VL.pdf#page=12\|§3.2.7 · p.12]] |
| AITZ手机UI | tap/input/swipe的类型与具体坐标/文字/方向匹配 | TM89.6、EM72.1是动作匹配，不是72.1%多步任务成功。[[raw/papers/Qwen2-VL.pdf#page=10\|Table5 · p.10]]；[[raw/papers/Qwen2-VL.pdf#page=13\|§3.2.7 · p.13]] |
| ALFRED | AI2THOR中的高层GotoLocation/Pickup等动作，并引入SAM辅助对象操作；valid-unseen | SR67.8、GC75.8分别是整任务与子目标结果；是模拟环境下组合系统证据，不是实机低层控制验证。[[raw/papers/Qwen2-VL.pdf#page=10\|Table5 · p.10]]；[[raw/papers/Qwen2-VL.pdf#page=13\|§3.2.7 · p.13]] |
| 卡牌游戏与导航 | 卡牌任务SR；R2R/REVERIE valid-unseen SR | 导航未全面领先：Qwen2-VL显著低于专用模型；作者将其与地图信息不完整/无结构联系，但未用独立消融证明原因。[[raw/papers/Qwen2-VL.pdf#page=13\|§3.2.7 · p.13]] |

## 感知消融不自动解释任务成功

动态图像token与固定token的Table7在7B上表明不同任务最佳分辨率不同；扩大图像并非单调改善，OCR过度放大会下降。M-RoPE的Table8用 **Qwen2-1.5B+ViT-L预训练模型**，视频指标总体更好但部分图像指标下降；不是72B Agent任务消融。[[raw/papers/Qwen2-VL.pdf#page=14|§3.3.1、Table7、Fig.4 · p.14]] [[raw/papers/Qwen2-VL.pdf#page=15|§3.3.2、Table8 · p.15]]

Fig.5的72B在Video-MME medium视频上测试8K至80K输入，曲线并非单调且没有展示对照1D版本的同一长度曲线。它支持该模型在此视频QA条件下可外推，不能独立证明全由M-RoPE导致。Video-MME整体评测最多抽768帧，也不能把长视频分钟数当作持续实时交互时长。[[raw/papers/Qwen2-VL.pdf#page=12|§3.2.6 · p.12]] [[raw/papers/Qwen2-VL.pdf#page=15|Fig.5 · p.15]]

## 本库获得的修订与仍缺的证据

本批比较需要逐篇检查系统、任务和归因。Qwen2-VL提供直接多轮系统结果，但未在本次所读范围充分报告每任务运行步数/失败恢复分解、同预算训练组件消融及Agent数据的具体配比；不以这些缺失否认已报告结果。完整定位/导航来源的原论文未在本任务独立读取，比较仍是本报告的实验/作者转述。

下一条证据是固定Qwen-Agent、动作权限、视觉token预算和模型规模，区分感知失误、历史状态丢失与规划失败；本轮仅列证据缺口，不宣布创新点。

## 本库落点与下一条证据

已整合到 [[wiki/optimization/Overview#预训练与中期训练|预训练与中期训练]]，主题与本页双向关联。相关方法的比较以本文实际实验为限，未核读的引用不成为独立来源。返回 [[wiki/index|索引]]。
