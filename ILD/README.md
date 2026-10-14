# ILD 医学研究工作区

## 目录用途

| 目录 | 用途 |
| --- | --- |
| IPF/、CTD-ILD/、PPF/、RILI/、nfHP/ | 按主题整理问题、文献索引及研究笔记；具体适用人群以原始来源为准 |
| Pipeline/ | 研究流程、任务清单和运行记录 |
| trials/ | 按试验保存元数据索引及后续核验记录 |
| evidence_cards/ | 经审阅的证据卡片，逐条附来源位置与适用边界 |
| KOL_brief/ | 专家交流简报和待讨论问题 |
| PPT_source/ | 课件大纲、引文、图表数据及合法素材 |

此目录用于主题组织；既有 literature/、presentations/、scripts/ 和 outputs/ 保持原位，主题文件可链接这些成果。

## 五项研究索引

| 研究 | PMID | 索引 |
| --- | --- | --- |
| SENSCIS | 31112379 | [metadata.json](trials/SENSCIS/metadata.json) |
| INBUILD | 31566307 | [metadata.json](trials/INBUILD/metadata.json) |
| RELIEF | 33798455 | [metadata.json](trials/RELIEF/metadata.json) |
| TRAIL1 | 36075242 | [metadata.json](trials/TRAIL1/metadata.json) |
| U-ILD | 31578169 | [metadata.json](trials/U-ILD/metadata.json) |

索引来自已完成的元数据验证，只有原始论文元数据及摘要层面的核验，不代表完整临床证据卡已完成。U-ILD 在此指吡非尼酮用于未分类进展性纤维化 ILD 的 phase 2 原始试验。

## 追溯要求

- 每条关键结论保留 PMID/DOI、原始链接、来源位置、分析集、终点时间、效应量及不确定性。
- 区分原始试验论文、方案、新闻公告、会议摘要和推测；仅摘要与未核实字段明确标注。
- 不编造结果，不将跨人群证据直接改写为目标疾病疗效。
- 原始响应快照路径从仓库根目录解析；本地存在不意味着该快照已提交 Git。
- 新文件采用独立名称或版本，保留旧稿；正式 PPT 继续执行证据、大纲、样张及验收流程。
