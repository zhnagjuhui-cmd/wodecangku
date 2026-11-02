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
