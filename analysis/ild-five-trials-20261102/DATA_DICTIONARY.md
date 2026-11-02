# study_extraction 数据字典 v0.1.0

## 顶层和研究记录

`schema_version/dataset_version` 分别记录结构及数据版本。`release_status` 本批固定为 DRAFT_NOT_FOR_PRESENTATION。`studies` 是五项独立记录，不构成汇总分析。

`study_id` 为用户指定代号，不替代经核实的论文或注册身份。`record_version` 为研究记录版本；`extracted_by/extracted_at` 为提取责任及日期。`verification_status` 为 UNVERIFIED 或 VERIFIED；`review_status` 为 PENDING_INDEPENDENT_REVIEW 或 APPROVED；`reviewer/reviewed_at` 未复核时为 null，结构建立者不得代签独立医学验收。

`population/intervention/comparator/primary_endpoint/follow_up/analysis_population/endpoint_hierarchy` 需原始来源支持，未核实保持 null。研究级 `missing_reason` 解释尚未核实的设计字段。

`sources` 每项需包含 source_id、source_type（ORIGINAL_ARTICLE / SUPPLEMENT / REGISTRY）、url、doi、pmid、nct、accessed_at、source_version、access_level（FULL_TEXT / ABSTRACT_ONLY / METADATA_ONLY）、file_sha256。未下载时 file_sha256 可为 null；实际文件按字节计算 SHA256。摘要可读不能写成全文可得。

## 指标记录

|字段|要求|
|---|---|
|metric_id|候选指标名，实际提取前按真实终点细化|
|value|null 或真实数值，缺失不填 0|
|unit|数值非空时必填，保留原文单位|
|analysis_population|ITT、mITT、safety 等需原文定义|
|endpoint_hierarchy|PRIMARY / KEY_SECONDARY / SECONDARY / EXPLORATORY / SAFETY|
|timepoint|真实时点或期间，不混同年化与定点变化|
|effect_measure|difference、OR、HR、count 等及方向|
|missing_reason|值为 null 时必填，有数值时为 null|
|verification_status|字段级 UNVERIFIED / VERIFIED|
|source_id|必须匹配 sources 中唯一 source_id|
|source_location|页码、表、图、段落或注册字段|
|source_version|论文版本、补充日期或注册更新时间|
|review_status|PENDING_INDEPENDENT_REVIEW / APPROVED|

任何数字必填单位、分析集、终点层级、时点、效应类型及来源定位。未复核数字仍标 UNVERIFIED，不能直接进入课件。

缺失原因使用 SOURCE_NOT_YET_INDEPENDENTLY_REVIEWED、NOT_REPORTED、NOT_APPLICABLE 或 ACCESS_UNAVAILABLE；后面三类需来源或判断说明。本批全部为第一类。

原文 p<阈值不得伪装成精确 p 值；后续应增加 operator 字段保留不等式。置信区间须保留置信水平、同一效应量及分析人群。候选 adverse_events 字段在实际提取前必须拆明具体事件、分母、事件人数或事件次数，本批不填数值。

机器校验只检查结构及缺失值约束，不能替代来源核对和独立医学验收。

第三轮：p_operator保留<或=，primary_p_value为阈值/值，应连同算符读取；AE字段明确any AE、patients及denominator，绝非事件次数。RELIEF primary_effect及CI为Hodges-Lehmann，P来自rank ANCOVA；不得按同一检验解释。sample_size须连同analysis_population读取。研究整体状态仍UNVERIFIED代表未完成全部设计和附件核验。

### 第三轮继续核验：五篇主报告均已读取（本节替代前述读取缺口）
桌面TIRAL1副本为TRAIL1正式online全文10页；桌面U-ILD副本为正式online全文11页。均已核对%PDF、题名/DOI、页数和SHA-256，原文件不动且不提交。Documents副本st_flags含0x40000000，属dataless占位；桌面副本不含该标记且已成功读取。
- TRAIL1 online p4 Figure1/Table1：123随机（63/60）；p7 Results、p5 Table2：主要复合终点7/63 vs 9/60，OR0.67（95%CI0.22–2.03），P=0.48；p5 Table2/Fig2：年FVC -66/-146 mL/年，P=0.0082，属于次要终点；p7 Table3：TEAE 62/62 vs 56/60，安全性分母不同于随机分母。原文56/60配94%，保留原报告计数，不把百分比倒推成其他分子；提前停止/低效能，不能宣布主要终点成功。
- U-ILD online p5 Figure1：253 ITT（127/126）；p7 Table2、p6 Results：中心FVC -17.8/-113.0 mL，差95.3（95%CI35.9–154.6），P=0.002，次要终点；主要家庭肺量计预设模型因变异不能应用，primary效应/CI/P四槽保持null，不能用中心结果替代。p9 Table4：TEAE120/127 vs101/124，安全性251不同于ITT253。
- A机器字段共37项，与C37/45非空严格一致；8项null/UNVERIFIED：RELIEF两组FVC变化与any-AE四槽尚未完成字段定义/缺失处理匹配，U-ILD主要效应/CI/P四槽不适用预设模型。null不代表0。
- 独立官方补充包仍未识别/完整审阅；五个主报告均非合并附件本，正文引用appendix不能证明附件已读。方案/SAP、注册历史、完整RoB及独立验收未完成。冻结资格仍NO；NOT_FROZEN；B不启动。

C仅填A已定位的37项。没有把U-ILD次要效应放入primary槽。AE单位/分母保留各文原定义，不直接跨研究合并。
