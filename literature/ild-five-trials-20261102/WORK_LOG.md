# A 工作日志

2026-11-02（本批末次记录 UTC 10:31:44；浏览访问按日期记录，不虚构精确秒）：

1. 阅读工作树根 AGENTS.md；仅新增本研究子目录。
2. 浏览工具逐一打开五篇 PubMed 主报告记录，读取文献身份与 Abstract Methods/Results/Interpretation；将论文声明的注册号与独立注册核验区分。
3. 逐一访问期刊正文入口：NEJM 两项与 Lancet 三项均返回 403；NEJM 两项 appendix PDF 入口也返回 403。Lancet 三项的附件直链未取得，不能猜测后标为已下载。
4. 四个 ClinicalTrials.gov 研究页仅得到 11 行动态页面壳；四个 API v2 studies URL 由浏览工具报告不可访问。注册号来自论文，注册字段与版本历史未核验。
5. RELIEF 检索未确认对应 NCT。打开 DRKS 官方记录及 EudraCT 结果页，核实替代注册身份；发现官方附件但没有读取内容。不得把此发现写成全文已审阅。
6. 没有保存论文 PDF、没有生成医学图表、没有冻结证据或启动 B。

可追溯性说明：SOURCE_INVENTORY.csv 和 STUDY_VERIFICATION.md 是本次访问后的人工转录记录；不是网页原始快照。公开 URL 可复查；访问时间变化可能改变页面。失败结果仅代表本次工具路径，不证明论文不可合法获取。

本地自查：运行目录内 CSV/JSON/必需文件结构检查；最终内容等待独立验收。

7. 后续改用获准的本地 urllib 直接请求 ClinicalTrials.gov API，四项均成功；保存未经修改 JSON、SHA-256 和 selected_fields。已读当前身份/状态/入组数/主要终点，历史版本与全文一致性仍 UNVERIFIED。此条更新第 4 条网页访问失败后的获取层级。

8. 本地检查首次发现 CSV 默认 CRLF 被 git diff --check 报为行末空白，已统一 LF；修订注册状态用语，保留当前字段核验与历史对照的界限。

## Round 2: 2026-11-02
U-ILD identity CONFIRMED by user on 2026-11-02: Maher pirfenidone unclassifiable progressive fibrosing ILD phase 2; DOI 10.1016/S2213-2600(19)30341-8; PMID 31578169; NCT03099187.
Accepted DOCX acquired from https://spiral.imperial.ac.uk/bitstreams/3881b1b6-66b5-414f-8763-6f693fbc72b2/download ; ZIP/XML and title checked; SHA256 0be384e12562a332af2102419bb1c1958bbc742fe13e3ab02055fbdc71886cc2. Table 1: ITT 127/126. Table 2: site spirometry FVC predicted mean change at 24 weeks -17.8/-113.0 mL; difference 95.3 (95%CI 35.9 to 154.6), P=0.002; SECONDARY endpoint. Published page mapping UNVERIFIED (accepted DOCX has no stable published pagination). Supplement content present, separate publisher appendix completeness UNVERIFIED.
RELIEF official DRKS record https://drks.de/search/de/trial/DRKS00009822 confirms DRKS00009822 and EudraCT 2014-000861-32 under Further identification numbers. NCT remains UNVERIFIED. Current publication link points to PubMed, not a verified PDF.
SENSCIS/INBUILD/TRAIL1/RELIEF primary full text and supplements remain UNVERIFIED. PMC/publisher searches did not yield verified primary full texts; INBUILD NEJM still403. Reviews cannot substitute. All unavailable page/table locations UNVERIFIED. Freeze eligibility: NO; NOT_FROZEN; independent review, full-text/supplement reconciliation outstanding. Descriptive cross-trial comparison only.

## 第三轮（2026-11-02，以本节更新前轮状态）

初始四工作树均干净；保留前轮文件及提交。mdfind 无结果；find 已覆盖 Documents、Downloads、Desktop、Library/Mobile Documents，包含本项目及仓库现有 literature/skills。文件名命中清单见 LOCAL_PDF_PATHS.md；全目录内容识别的读取失败不能视为文件不存在。原 PDF 未移动、未删除、未提交；版权再分发授权未确认，仅记录路径与 SHA-256。

|研究|已读本地版本|数字及定位|
|---|---|---|
|SENSCIS|11页正式全文，%PDF及SHA-256已核验|PDF p5/刊p2522 Fig1：580随机、4未用药（3不合格、1撤回），576接受治疗，288/288；PDF p8/刊p2525 Table2：52周年FVC -52.4/-93.3 mL/年，差41.0（95%CI 2.9–79.0），P=0.04；PDF p9/刊p2526 Table3：任何AE 283/288、276/288；多重插补P=0.06–0.10，不能忽略敏感性|
|INBUILD|10页正式全文，%PDF及SHA-256已核验|PDF p5/刊p1722 Fig1：663，332/331；PDF p7/刊p1724 Table2：总体52周年FVC -80.8/-187.8 mL/年，差107.0（95%CI 65.4–148.5），P<0.001；PDF p9/刊p1726 Table3：任何AE 317/332、296/331；总体与UIP-like为主要分析人群，未把总体当特定自身免疫亚组结果|
|RELIEF|11页online正式全文，%PDF及SHA-256已核验；以文件印刷online页码定位|p5 Fig1/p6：127随机（64/63）；p6 Results、p7 Fig2：48周Hodges-Lehmann差1.69 FVC预计值百分点（95%CI -0.65–4.03）；rank ANCOVA P=0.043，与该CI是不同统计量，不能伪装成同一检验；提前停止，死亡最差秩及SSD插补限制保留|
|TRAIL1|已定位拼写TIRAL1的本地候选；读取失败/超时|全文及补充数字、页码、表图 UNVERIFIED，不以文件名认定正文|
|U-ILD|本地PDF候选已定位，但读取失败/超时；保留前轮accepted DOCX核验|前轮Table2的中心肺量计次要终点-17.8/-113.0 mL仍有效；正式PDF页码 UNVERIFIED|

机器可追溯字段见 ROUND3_VERIFIED_FIELDS.json（23项本轮核实，另有前轮U-ILD 2项；不等于独立验收）。全部五研究独立补充材料、方案及SAP完整性仍 UNVERIFIED。RELIEF正文明确引用appendix 1并不等于已取得附件；Matteson自身免疫亚组资料不能作为INBUILD主试验补充包。

补充网站 https://ild-evidence-radar-zjh.zhnagjuhui.chatgpt.site 本轮返回Sign in required；web读取失败，浏览器host不可用，未取得任何新文献，不纳入数字来源。网站本地旧HTML亦不当作当前站点全文。

冻结资格：不具备。NOT_FROZEN / approved_for_B=false；缺少可读TRAIL1及U-ILD正式PDF对照、五研究完整附件核验、注册历史/方案/SAP一致性、偏倚风险全项评价、独立审核与总控签收。未自行冻结，B继续等待。
