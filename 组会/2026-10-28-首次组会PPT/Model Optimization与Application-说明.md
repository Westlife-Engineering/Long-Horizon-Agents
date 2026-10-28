# Model Optimization 与 Application：当前交付说明

更新日期：2026-10-28。

## 当前文件与页序

- `首次组会-完整汇报.pptx`：17 页，前 10 页为用户最新的 Foundation / Harness，后 7 页为本次精简续篇。合并稿封面已补全四部分范围，全文页码连续。
- `首次组会-Model Optimization与Application.pptx`：独立续篇 7 页，保留可单独修改的版本。
- `Model Optimization与Application-内容源.json`：同步删除页面，并加入两段讲述稿。可编辑结构以最新 PPTX 为准。
- [[组会/2026-10-28-首次组会PPT/Optimization与Application-两页讲述方案|两页讲述方案]]：含节奏、可直接讲的版本、表达边界和原始证据。两段稿件也进入两份 PPT 对应页的演讲者备注。

| 原续篇页码 | 当前续篇页码 | 合并稿页码 | 内容 |
| --- | --- | --- | --- |
| 1 | 1 | 11 | Model Optimization 总览 |
| 2 | 2 | 12 | 训练更新与经验反馈关系图 |
| 3 | 3 | 13 | Agentic RL 四个设计维度 |
| 5 | 4 | 14 | 能力内化的证据需要分层 |
| 6 | 5 | 15 | Application 接口总览 |
| 7 | 6 | 16 | Model、Harness 与环境的配合 |
| 8 | 7 | 17 | 已有成效依赖可用信息与有效反馈 |

按用户要求删除原续篇第 4 页“学习信号与训练状态需要一起看”和第 9 页“组件有效与主要瓶颈是两种判断”。原第 5、8 页的讲述方案分别约 75–90 秒、90–110 秒。7 页续篇完整讲述约 9 分钟，时间仅为估计。

## 依据与表达

主要内容从 [[wiki/optimization/Overview|Optimization 总览]]、[[wiki/optimization/Questions|Optimization 问题]]、[[wiki/optimization/reinforcement-learning|Agentic RL]]、[[wiki/applications/Overview|Application 总览]]、[[wiki/applications/success-mechanisms|应用机制综合]] 提炼，学术证据仍回到各页备注中的原始 PDF。

Agentic RL 表格依据 S001 §5.5、Fig.12（PDF pp.47–52），四个维度可以组合，不是固定顺序或互斥算法。能力内化的三个证据视角、跨应用机制与教学情境均保留本库归纳身份，不宣称新研究缺口。讲述方案的案例出处另在方案文档列明；原论文结果未复现。

## 合并与检查范围

本次使用的 Foundation / Harness 是 10 页最新稿，SHA-256 为 `DC9AD18F71A7335EE1E233BA25605839740E524CE082FE7BA700E0CFD1FCE6E3`，源文件未改。合并稿仅更新封面范围、续篇页码及指定两页的备注。原有页面正文通过逐页文本比对，图片与原生表格保留；插入后显式恢复续篇背景，保持原色。

两份成品均通过结构、尺寸、字体、页数、原生表格、布局与 Artifact Tool 导入检查。合并稿有 7 张原生表格。已通过本机 PowerPoint 导出全部 17 页并扫描全稿，单独检查封面及追加的 7 页；未进行现场投影或逐个对象拖动测试。

- 合并稿 SHA-256：`78A36896AEA69F81712A103FF39067861D7D5DE54825AB47BC1DB8A13239935D`
- 精简续篇 SHA-256：`8B9D60DCB3DA036AE55EEED57BD9580A19CDA64763EE596E8A1C77E1050F1527`

本次临时文件限 `.tmp/merge-final/`，验收后清理；原任务临时目录及其依赖链接不在清理范围内。未修改 Raw、正式 Wiki、旧计划或 Harness 原稿，未提交或推送。
