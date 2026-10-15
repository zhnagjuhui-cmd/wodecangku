# 文献状态与证据边界

建议每条文献记录以下字段：
`citation_id, slide_physical, footer_label, title, authors, year, doi, pmid, population, design, endpoint, followup, analysis_set, source_status, version, local_path, source_url, figure, panel, pdf_page, verification, unresolved`。
允许多页对应同一文献、一页对应多条文献；新增引用后同步清单及页内来源。

## 状态分别统计

- 正式期刊PDF全文：能解析正文并确认题录。
- 正式HTML/XML全文：确认有Methods/Results等正文，未必有完整图片。
- 作者接受稿：标明版本及与最终发表稿的差别。
- 会议摘要、研究者报告、企业幻灯：单独分类，不计正式期刊全文。
- 仅摘要/题录：不能声称完整全文已读。
- 待准确识别：中文小字、扫描件或题录不完整。

下载数量需按研究与文件分别统计，避免将译本、重复PDF、会议材料或PDF/HTML两个格式计作两个新增研究。

## 容易混淆的结果

- 随机入组人数不等于主要分析人数，访视实际人数也可能继续减少。
- 百分点与相对百分比不同；两组中位数之差不必等于Hodges–Lehmann组间估计。
- Bayesian可信区间/后验概率与频率学派置信区间/P值不能相互转写。
- 主要终点、探索性终点及事后排除离群值的分析须分别呈现。
- 延长期全部接受同一治疗后，按原随机组列出的结果不等于持续安慰剂对照。
- 影像变化不自动证明纤维化逆转；标志物关联不自动成为治疗阈值。
- 临床前小鼠、人源细胞实验不等于患者疗效；机制和研发阶段不等于确证性结果。

## 本流程中的可迁移例子

INCREASE（DOI 10.1056/NEJMoa2008470）研究PH-ILD、16周6分钟步行距离；TETON研究IPF、52周FVC。前者适合作为后者背景，但不能替换后者结果图。这是人群与终点匹配的例子，不要求每次任务引用这些研究。

本地“Pirfenidone: a new option for radiation-induced lung injury?”是评论；其正文含目标RCT的DOI仍不意味着它就是RCT原文。题名、论文类型及自身DOI需要同时核对。
