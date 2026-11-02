# A 独立验收清单

状态：待验收；以下勾选仅为执行自查，不代表总控验收。

- [x] 五项研究均有主报告题名、首作者、年份、DOI、PMID 与原始记录 URL。
- [x] 分开摘要、全文、补充材料和注册平台；未核实内容标 UNVERIFIED。
- [x] RELIEF 使用原论文实际注册号，不强填 NCT。
- [x] U-ILD 映射明确写为待总控确认。
- [x] 来源清单含访问日期、获取层级、失败/未审阅原因。
- [ ] 五篇合法完整全文经标题、页数、文件头与 SHA-256 验证。
- [ ] 五研究补充材料/方案/SAP/历史版本取得并逐项核对。
- [ ] ClinicalTrials.gov 四项原始注册字段及历史终点独立核验；RELIEF NCT 检索歧义解除。
- [ ] 人群、分析集、分母、终点、效应量、CI、P 值、安全性及缺失数据处理逐字段来源定位。
- [ ] 完成偏倚风险和适用范围评价，禁止直接跨研究疗效排序。
- [ ] 第二位验收者核验并登记姓名/日期/意见；总控签收。
- [ ] 生成包含来源文件 SHA-256、证据版本和受限条目的冻结清单后，B 才能引用。

本批文件解析/存在性由本地脚本检查；最终内容和来源一致性仍待独立复核。

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

### 第三轮继续核验：五篇主报告均已读取（本节替代前述读取缺口）
桌面TIRAL1副本为TRAIL1正式online全文10页；桌面U-ILD副本为正式online全文11页。均已核对%PDF、题名/DOI、页数和SHA-256，原文件不动且不提交。Documents副本st_flags含0x40000000，属dataless占位；桌面副本不含该标记且已成功读取。
- TRAIL1 online p4 Figure1/Table1：123随机（63/60）；p7 Results、p5 Table2：主要复合终点7/63 vs 9/60，OR0.67（95%CI0.22–2.03），P=0.48；p5 Table2/Fig2：年FVC -66/-146 mL/年，P=0.0082，属于次要终点；p7 Table3：TEAE 62/62 vs 56/60，安全性分母不同于随机分母。原文56/60配94%，保留原报告计数，不把百分比倒推成其他分子；提前停止/低效能，不能宣布主要终点成功。
- U-ILD online p5 Figure1：253 ITT（127/126）；p7 Table2、p6 Results：中心FVC -17.8/-113.0 mL，差95.3（95%CI35.9–154.6），P=0.002，次要终点；主要家庭肺量计预设模型因变异不能应用，primary效应/CI/P四槽保持null，不能用中心结果替代。p9 Table4：TEAE120/127 vs101/124，安全性251不同于ITT253。
- A机器字段共37项，与C37/45非空严格一致；8项null/UNVERIFIED：RELIEF两组FVC变化与any-AE四槽尚未完成字段定义/缺失处理匹配，U-ILD主要效应/CI/P四槽不适用预设模型。null不代表0。
- 独立官方补充包仍未识别/完整审阅；五个主报告均非合并附件本，正文引用appendix不能证明附件已读。方案/SAP、注册历史、完整RoB及独立验收未完成。冻结资格仍NO；NOT_FROZEN；B不启动。

### 搜索结束补记
指定四根目录find已完成；全963路径的限时内容检索已结束，另对可读取医学资料按哈希去重，读取256个唯一PDF，32个首两页关键词命中，路径/哈希/页数见LOCAL_READABLE_CANDIDATES.csv。并未将综述、课件、翻译或亚组报告当作五主报告附件。43页Matteson文件首面为ICMJE Disclosure Form（INBUILD自身免疫亚组作者披露），不是主报告正文或结果补充材料。未识别的附件仍UNVERIFIED，不声称不存在。
