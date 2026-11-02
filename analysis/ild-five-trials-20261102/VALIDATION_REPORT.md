# C 首批验证报告

日期：2026-11-02。版本：0.1.0。独立学术验收：待验收。

执行：`python3 analysis/ild-five-trials-20261102/scripts/validate_extraction.py`

结果：PASS。五项研究独立记录，45 个候选数字槽均为 null / UNVERIFIED，并包含缺失原因、单位、来源定位、分析集和终点层级字段。sources 为空，说明 C 尚未独立阅读和登记原始来源。

负向验证：复制数据到内存后，删除缺失原因，校验正确拒绝；把尚未核实的 null 填成 0 且仍保留缺失状态，校验正确拒绝。没有修改正式数据文件。

`git diff --check`：通过。文件均新增于本任务目录；未修改历史成果。

本次未做原文数字比对，未验收任何医学结果，没有生成图表、合并分析或课件。机器校验不能证明来源真实或数字准确，A/C 对照和总控签收仍待进行。

Round2: 2 A-verified U-ILD secondary FVC values populated; 43 remain null/UNVERIFIED. Independent acceptance pending.

## 第三轮 2026-11-02
仅消费A ROUND3_VERIFIED_FIELDS.json已核实23项及前轮U-ILD 2项：25/45有值，20/45 null/UNVERIFIED。保留待独立审核、DRAFT_NOT_FOR_PRESENTATION。SENSCIS样本量576表示至少一剂；580随机化另见来源。INBUILD P<0.001以p_operator记录；AE为人数且记录各组分母；RELIEF rank ANCOVA P与Hodges-Lehmann CI不是同一检验。无跨试验排序。

### 第三轮继续核验：五篇主报告均已读取（本节替代前述读取缺口）
桌面TIRAL1副本为TRAIL1正式online全文10页；桌面U-ILD副本为正式online全文11页。均已核对%PDF、题名/DOI、页数和SHA-256，原文件不动且不提交。Documents副本st_flags含0x40000000，属dataless占位；桌面副本不含该标记且已成功读取。
- TRAIL1 online p4 Figure1/Table1：123随机（63/60）；p7 Results、p5 Table2：主要复合终点7/63 vs 9/60，OR0.67（95%CI0.22–2.03），P=0.48；p5 Table2/Fig2：年FVC -66/-146 mL/年，P=0.0082，属于次要终点；p7 Table3：TEAE 62/62 vs 56/60，安全性分母不同于随机分母。原文56/60配94%，保留原报告计数，不把百分比倒推成其他分子；提前停止/低效能，不能宣布主要终点成功。
- U-ILD online p5 Figure1：253 ITT（127/126）；p7 Table2、p6 Results：中心FVC -17.8/-113.0 mL，差95.3（95%CI35.9–154.6），P=0.002，次要终点；主要家庭肺量计预设模型因变异不能应用，primary效应/CI/P四槽保持null，不能用中心结果替代。p9 Table4：TEAE120/127 vs101/124，安全性251不同于ITT253。
- A机器字段共37项，与C37/45非空严格一致；8项null/UNVERIFIED：RELIEF两组FVC变化与any-AE四槽尚未完成字段定义/缺失处理匹配，U-ILD主要效应/CI/P四槽不适用预设模型。null不代表0。
- 独立官方补充包仍未识别/完整审阅；五个主报告均非合并附件本，正文引用appendix不能证明附件已读。方案/SAP、注册历史、完整RoB及独立验收未完成。冻结资格仍NO；NOT_FROZEN；B不启动。

C仅填A已定位的37项。没有把U-ILD次要效应放入primary槽。AE单位/分母保留各文原定义，不直接跨研究合并。
