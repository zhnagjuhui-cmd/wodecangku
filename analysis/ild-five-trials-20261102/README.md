# C 数据分析：首批结构交付

分支：`codex/ild-analysis`。状态：结构已建立，医学数字尚未提取，待独立验收。

本批独立于 A 建立结构，未读取 A 的工作成果，也未从记忆填入研究数据。`study_extraction.json` 包含 SENSCIS、INBUILD、TRAIL1、RELIEF、U-ILD 五项研究，各保留九项候选指标。候选字段不代表研究一定报告该指标。医学数值全部为 `null`，状态为 `UNVERIFIED`，不能解释为零事件、零效应或无差异。

- `DATA_DICTIONARY.md`：字段、单位、定位与缺失语义。
- `ACCEPTANCE_CHECKLIST.md`：结构与医学验收分开。
- `scripts/validate_extraction.py`：不依赖第三方库的校验脚本。
- `VALIDATION_REPORT.md`、`WORK_LOG.md`：执行证据。

运行：`python3 analysis/ild-five-trials-20261102/scripts/validate_extraction.py`。脚本以自身位置定位数据，可从任意目录运行。

下一批 C 应自行读取原文、补充材料及注册记录，建立带精确定位的数字记录，再与 A 交叉复核。B 只能引用 A 冻结版本，C 草稿不能绕过冻结门槛。禁止跨研究疗效排名或未经方案支持的合并分析。

## 第三轮 2026-11-02
仅消费A ROUND3_VERIFIED_FIELDS.json已核实23项及前轮U-ILD 2项：25/45有值，20/45 null/UNVERIFIED。保留待独立审核、DRAFT_NOT_FOR_PRESENTATION。SENSCIS样本量576表示至少一剂；580随机化另见来源。INBUILD P<0.001以p_operator记录；AE为人数且记录各组分母；RELIEF rank ANCOVA P与Hodges-Lehmann CI不是同一检验。无跨试验排序。

### 第三轮继续核验：五篇主报告均已读取（本节替代前述读取缺口）
桌面TIRAL1副本为TRAIL1正式online全文10页；桌面U-ILD副本为正式online全文11页。均已核对%PDF、题名/DOI、页数和SHA-256，原文件不动且不提交。Documents副本st_flags含0x40000000，属dataless占位；桌面副本不含该标记且已成功读取。
- TRAIL1 online p4 Figure1/Table1：123随机（63/60）；p7 Results、p5 Table2：主要复合终点7/63 vs 9/60，OR0.67（95%CI0.22–2.03），P=0.48；p5 Table2/Fig2：年FVC -66/-146 mL/年，P=0.0082，属于次要终点；p7 Table3：TEAE 62/62 vs 56/60，安全性分母不同于随机分母。原文56/60配94%，保留原报告计数，不把百分比倒推成其他分子；提前停止/低效能，不能宣布主要终点成功。
- U-ILD online p5 Figure1：253 ITT（127/126）；p7 Table2、p6 Results：中心FVC -17.8/-113.0 mL，差95.3（95%CI35.9–154.6），P=0.002，次要终点；主要家庭肺量计预设模型因变异不能应用，primary效应/CI/P四槽保持null，不能用中心结果替代。p9 Table4：TEAE120/127 vs101/124，安全性251不同于ITT253。
- A机器字段共37项，与C37/45非空严格一致；8项null/UNVERIFIED：RELIEF两组FVC变化与any-AE四槽尚未完成字段定义/缺失处理匹配，U-ILD主要效应/CI/P四槽不适用预设模型。null不代表0。
- 独立官方补充包仍未识别/完整审阅；五个主报告均非合并附件本，正文引用appendix不能证明附件已读。方案/SAP、注册历史、完整RoB及独立验收未完成。冻结资格仍NO；NOT_FROZEN；B不启动。

C仅填A已定位的37项。没有把U-ILD次要效应放入primary槽。AE单位/分母保留各文原定义，不直接跨研究合并。

## 第四轮（2026-11-02，最新）
状态：DRAFT_NOT_FOR_PRESENTATION；A NOT_FROZEN；独立学术验收未通过。

- 数字非空且由A核实：39/45（上一轮37/45）；45槽均完成本轮审查，不能表述45/45数字已核实。
- 本轮新增仅RELIEF两项：48周FVC变化 -36.6/-114.4 mL；主报告online p7 Table2及脚注。可用配对观察35/32人，不作插补，事后分析，层级EXPLORATORY；不能替代FVC预计值百分点主要终点，不年化，不用于跨试验排名。
- 6项保持null/UNVERIFIED：RELIEF任何AE患者并集计数两项（NOT_REPORTED，附件仅有特定事件与SAE）；U-ILD预设家庭肺量计主要效应/CI下界/CI上界/P四项（NOT_APPLICABLE，模型无法应用，不能搬用中心肺量计）。null不等于0。
- 既有37项与重新从五篇原文抽取的值一致；INBUILD P<0.001保留算符；TRAIL1原文56/60与94%不一致，保留原计数，百分比不另入数字字段；RELIEF appendix1 S7的百分比与正文计数不一致，未将其转作any-AE。
- 全39项逐字段与A ROUND4_VERIFIED_FIELDS.json核对：值、单位、分析集、层级、时间点、来源定位、P算符/安全分母一致。A新增来源账及哈希见A分支ROUND4_SOURCE_FILES.json；PDF留本地不提交。
- 复抽由同一代理执行，不满足第二独立审核者要求；review_status保持PENDING_INDEPENDENT_REVIEW，不将结构检查当医学验收。
- SENSCIS/INBUILD独立结果附件仍缺；注册历史抓取403；U-ILD SAP含2020后续修订，原2018 SAP与后续分析必须分开；TRAIL1晚期SAP与方案版本及模型差异仍需追溯。仅描述性跨试验比较。
