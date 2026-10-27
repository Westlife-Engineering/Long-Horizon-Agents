# 社交科研观察试跑迁出归档

日期：2026-10-26。按用户明确授权迁出，保留全部试跑原文件及代码摘录。

- 旧根目录：C:/Users/ZENGZX/Desktop/Long-Horizon-Agents/workflow-trial/social-scout_20261026/
- 新根目录：C:/Users/ZENGZX/Desktop/Agent-Research-Radar/archive/social-scout_20261026/
- 映射规则：下表相对路径在两个根目录间一一对应；12 个原文件共 159,927 字节，复制后逐文件核对 SHA-256，再移除旧文件及空目录。旧 workflow-trial 已为空并移除。
- 归档处新增 ARCHIVE.md 与 MIGRATION-SHA256.json；原 12 个文件字节不变，包括历史 AGENTS.md、旧路径文字和代码摘录。历史规则不作为当前执行规则，日常运行不读取归档；当前工作区根 AGENTS.md 已明确此边界。
- Agent-Research-Radar/ACCEPTANCE.md 的旧试跑链接已改为 archive/social-scout_20261026/RUN.md，并链接归档说明。原目录未被 Git 跟踪，迁移不依赖 Git 恢复。
- 本库旧日志保持原样；其中此前 PPT 试跑的撤下与恢复记录不属于本批材料。未更改 Raw、知识页或来源计数；未执行 Git 提交或推送。
- 验收：迁移前后文件数量、字节数、SHA-256 一致；新引用目标存在。未进行 Obsidian 或 Markdown 阅读器界面渲染检查。

## 逐文件映射与 SHA-256

| 相对路径（旧根 → 新根） | 字节数 | SHA-256（迁移前后相同） |
| --- | ---: | --- |
| AGENTS.md | 1885 | ee3d09c5822e4e4786adf11700a976999929035d7e9a3d97a12f7b29f63a1b36 |
| followup-evidence/AGENTS.md | 1729 | 97bbe948105537f634cfbf7b6199b3987f20269fd25755e462876568425276e3 |
| followup-evidence/baseline-sha256.json | 24796 | ed4dd28de9c2a85ab15896c9d57c6ef50f50dc95949e876f65057851380094ea |
| followup-evidence/evidence/metrics/code-excerpts.md | 26503 | 44ce6760aefba1dff6182cad7da8445103da1cdff7144ec3c302452e3987e944 |
| followup-evidence/evidence/root/code-excerpts.md | 33126 | ec658d74ae0f70f58f4fd5e6a703eba95441d32a5aad26b673d061f4121cc39d |
| followup-evidence/evidence/root/dataset-observations.md | 3759 | cd3dbd4688bd485d9e735ef254bfe35ad538e89a1e0e3309bf1f85c37ea14958 |
| followup-evidence/evidence/root/source-manifest.json | 4572 | abb1d92985948559d400e0f93ce1d00f256c8f4595042b6997dacf335301a029 |
| followup-evidence/metrics-review.md | 11753 | 948238447081faf63c8501b8bf8a1996763fb90f537c960af048804b42599b2f |
| followup-evidence/RUN.md | 12707 | 8b05f14d7a3d7b7fc3454bc6fe186bc3cfe8612642e25d0b83f84d9c0652557b |
| followup-evidence/validation.json | 1668 | 93ceb664645f28456566771b9b750d7316ab0e2c936ddc4d7b1041041205c55f |
| RUN.md | 12277 | c59720552bbe666ac03e6a14701627596d8d1e6185caab8d3f16899e2242a741 |
| search-index.json | 25152 | d9f760a6ab1ffc12c24f36339500cf6e81948723aa54872c53a5a8b581185f30 |
