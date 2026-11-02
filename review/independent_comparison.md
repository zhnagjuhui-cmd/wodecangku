# 独立抽取逐项比对

盲抽取锁定提交：`eacf14c8b7a76c19518e780399c43e700160be79`。先提交，再读取 A/C 数值。盲抽取文件保持原提交字节不变。

结果：**数值一致 39/45；不一致 0；一方缺失 0；双方缺失 6**。39 个有值字段全部一致（39/39）。若计入缺失状态相容，45/45 相容；不能称 45 个数值全部核实。

A 对照表：`literature/ild-five-trials-20261102/ROUND4_VERIFIED_FIELDS.json`（39行）。C 对照表：`analysis/ild-five-trials-20261102/study_extraction.json`（45项）。输入提交和文件 SHA-256 见 `comparison_summary.json`。不将 ROUND3 旧版数值混入本次对照。

每项原文文件、PDF 物理页码（从1计）、表图号和逐字摘录见 [盲抽取记录](independent_extraction.json)。A/C 完整文件出处和原文路径可由上述文件及盲抽取 sources 交叉定位。

| 序号 | 研究 / 字段 | 盲抽取 | A | C | 判定 | 独立出处 | A/C 原记录出处 |
|---|---|---:|---|---|---|---|---|
| 1 | SENSCIS / sample_size | 576 | 576 | 576 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 1 | PDF p5, Figure 1; journal p2522; randomized 580, untreated 4 |
| 2 | SENSCIS / primary_effect | 41.0 | 41.0 | 41.0 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 2 / Table 2 | PDF p8 / journal p2525, Table 2 |
| 3 | SENSCIS / primary_ci_lower | 2.9 | 2.9 | 2.9 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 2 / Table 2 | PDF p8 / journal p2525, Table 2 |
| 4 | SENSCIS / primary_ci_upper | 79.0 | 79.0 | 79.0 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 2 / Table 2 | PDF p8 / journal p2525, Table 2 |
| 5 | SENSCIS / primary_p_value | =0.04 | =0.04 | =0.04 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 2 / Table 2 | PDF p8 / journal p2525, Table 2 |
| 6 | SENSCIS / treatment_fvc_change | -52.4 | -52.4 | -52.4 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 2 / Table 2 | PDF p8 / journal p2525, Table 2 |
| 7 | SENSCIS / control_fvc_change | -93.3 | -93.3 | -93.3 | 一致 | SENSCIS 主报告 PDF p4，Results / Figure 2 / Table 2 | PDF p8 / journal p2525, Table 2 |
| 8 | SENSCIS / treatment_adverse_events | 283 | 283 | 283 | 一致 | SENSCIS 主报告 PDF p9，Table 3 | PDF p9 / journal p2526, Table 3 |
| 9 | SENSCIS / control_adverse_events | 276 | 276 | 276 | 一致 | SENSCIS 主报告 PDF p9，Table 3 | PDF p9 / journal p2526, Table 3 |
| 10 | INBUILD / sample_size | 663 | 663 | 663 | 一致 | INBUILD 主报告 PDF p4，Results / Figure 1 | PDF p5, Figure 1; journal p1722 |
| 11 | INBUILD / primary_effect | 107.0 | 107.0 | 107.0 | 一致 | INBUILD 主报告 PDF p1，Summary / Table 2 (PDF p7) | PDF p7 / journal p1724, Table 2 |
| 12 | INBUILD / primary_ci_lower | 65.4 | 65.4 | 65.4 | 一致 | INBUILD 主报告 PDF p1，Summary / Table 2 (PDF p7) | PDF p7 / journal p1724, Table 2 |
| 13 | INBUILD / primary_ci_upper | 148.5 | 148.5 | 148.5 | 一致 | INBUILD 主报告 PDF p1，Summary / Table 2 (PDF p7) | PDF p7 / journal p1724, Table 2 |
| 14 | INBUILD / primary_p_value | <0.001 | <0.001 | <0.001 | 一致 | INBUILD 主报告 PDF p1，Summary / Table 2 (PDF p7) | PDF p7 / journal p1724, Table 2 |
| 15 | INBUILD / treatment_fvc_change | -80.8 | -80.8 | -80.8 | 一致 | INBUILD 主报告 PDF p1，Summary / Table 2 (PDF p7) | PDF p7 / journal p1724, Table 2 |
| 16 | INBUILD / control_fvc_change | -187.8 | -187.8 | -187.8 | 一致 | INBUILD 主报告 PDF p1，Summary / Table 2 (PDF p7) | PDF p7 / journal p1724, Table 2 |
| 17 | INBUILD / treatment_adverse_events | 317 | 317 | 317 | 一致 | INBUILD 主报告 PDF p9，Table 3 | PDF p9 / journal p1726, Table 3 |
| 18 | INBUILD / control_adverse_events | 296 | 296 | 296 | 一致 | INBUILD 主报告 PDF p9，Table 3 | PDF p9 / journal p1726, Table 3 |
| 19 | TRAIL1 / sample_size | 123 | 123 | 123 | 一致 | TRAIL1 主报告 PDF p6，Results / Figure 1 | PDF online p4 Figure 1; Table 1 |
| 20 | TRAIL1 / primary_effect | 0.67 | 0.67 | 0.67 | 一致 | TRAIL1 主报告 PDF p7，Results / Table 2 | PDF online p7 Results; Table 2 p5 |
| 21 | TRAIL1 / primary_ci_lower | 0.22 | 0.22 | 0.22 | 一致 | TRAIL1 主报告 PDF p7，Results / Table 2 | PDF online p7 Results; Table 2 p5 |
| 22 | TRAIL1 / primary_ci_upper | 2.03 | 2.03 | 2.03 | 一致 | TRAIL1 主报告 PDF p7，Results / Table 2 | PDF online p7 Results; Table 2 p5 |
| 23 | TRAIL1 / primary_p_value | =0.48 | =0.48 | =0.48 | 一致 | TRAIL1 主报告 PDF p7，Results / Table 2 | PDF online p7 Results; Table 2 p5 |
| 24 | TRAIL1 / treatment_fvc_change | -66 | -66 | -66 | 一致 | TRAIL1 主报告 PDF p5，Table 2 / Figure 2 | PDF online p5 Table 2/Figure 2; p7 Results |
| 25 | TRAIL1 / control_fvc_change | -146 | -146 | -146 | 一致 | TRAIL1 主报告 PDF p5，Table 2 / Figure 2 | PDF online p5 Table 2/Figure 2; p7 Results |
| 26 | TRAIL1 / treatment_adverse_events | 62 | 62 | 62 | 一致 | TRAIL1 主报告 PDF p7，Results / Table 3 | PDF online p7 Table 3/Results |
| 27 | TRAIL1 / control_adverse_events | 56 | 56 | 56 | 一致 | TRAIL1 主报告 PDF p7，Results / Table 3 | PDF online p7 Table 3/Results |
| 28 | RELIEF / sample_size | 127 | 127 | 127 | 一致 | RELIEF 主报告 PDF p6，Results / Figure 1 | PDF p5, Figure 1; p6 Results |
| 29 | RELIEF / primary_effect | 1.69 | 1.69 | 1.69 | 一致 | RELIEF 主报告 PDF p6，Results (Hodges-Lehmann) | PDF online p6 Results; Figure 2 p7; abstract p1 |
| 30 | RELIEF / primary_ci_lower | -0.65 | -0.65 | -0.65 | 一致 | RELIEF 主报告 PDF p6，Results (Hodges-Lehmann) | PDF online p6 Results; Figure 2 p7; abstract p1 |
| 31 | RELIEF / primary_ci_upper | 4.03 | 4.03 | 4.03 | 一致 | RELIEF 主报告 PDF p6，Results (Hodges-Lehmann) | PDF online p6 Results; Figure 2 p7; abstract p1 |
| 32 | RELIEF / primary_p_value | =0.043 | =0.043 | =0.043 | 一致 | RELIEF 主报告 PDF p6，Results (rank ANCOVA) | PDF online p6 Results; Figure 2 p7; abstract p1 |
| 33 | RELIEF / treatment_fvc_change | -36.6 | -36.6 | -36.6 | 一致 | RELIEF 主报告 PDF p7，Table 2 | PDF online p7, Table 2 and footnote |
| 34 | RELIEF / control_fvc_change | -114.4 | -114.4 | -114.4 | 一致 | RELIEF 主报告 PDF p7，Table 2 | PDF online p7, Table 2 and footnote |
| 35 | RELIEF / treatment_adverse_events | NOT_FOUND | 未列入已核实数值表 | 缺失 / NOT_REPORTED | 双方缺失 | RELIEF 主报告 PDF p7，Results; Table 3 (PDF p9) reports SAE only | Main p7/p9; appendix1 PDF p9-12, Tables S6-S8; appendix2 protocol/SAP |
| 36 | RELIEF / control_adverse_events | NOT_FOUND | 未列入已核实数值表 | 缺失 / NOT_REPORTED | 双方缺失 | RELIEF 主报告 PDF p7，Results; Table 3 (PDF p9) reports SAE only | Main p7/p9; appendix1 PDF p9-12, Tables S6-S8; appendix2 protocol/SAP |
| 37 | U-ILD / sample_size | 253 | 253 | 253 | 一致 | U-ILD 主报告 PDF p5，Results / Figure 1 | PDF online p5 Figure 1/Results |
| 38 | U-ILD / primary_effect | NOT_FOUND | 未列入已核实数值表 | 缺失 / NOT_APPLICABLE | 双方缺失 | U-ILD 主报告 PDF p5，Results / Figure 2 | PDF online p1 Summary; pp5-6 Results |
| 39 | U-ILD / primary_ci_lower | NOT_FOUND | 未列入已核实数值表 | 缺失 / NOT_APPLICABLE | 双方缺失 | U-ILD 主报告 PDF p5，Results / Figure 2 | PDF online p1 Summary; pp5-6 Results |
| 40 | U-ILD / primary_ci_upper | NOT_FOUND | 未列入已核实数值表 | 缺失 / NOT_APPLICABLE | 双方缺失 | U-ILD 主报告 PDF p5，Results / Figure 2 | PDF online p1 Summary; pp5-6 Results |
| 41 | U-ILD / primary_p_value | NOT_FOUND | 未列入已核实数值表 | 缺失 / NOT_APPLICABLE | 双方缺失 | U-ILD 主报告 PDF p5，Results / Figure 2 | PDF online p1 Summary; pp5-6 Results |
| 42 | U-ILD / treatment_fvc_change | -17.8 | -17.8 | -17.8 | 一致 | U-ILD 主报告 PDF p7，Table 2 | PDF online p7 Table 2; p6 Results |
| 43 | U-ILD / control_fvc_change | -113.0 | -113.0 | -113.0 | 一致 | U-ILD 主报告 PDF p7，Table 2 | PDF online p7 Table 2; p6 Results |
| 44 | U-ILD / treatment_adverse_events | 120 | 120 | 120 | 一致 | U-ILD 主报告 PDF p9，Table 4 | PDF online p9 Table 4; p7 Results |
| 45 | U-ILD / control_adverse_events | 101 | 101 | 101 | 一致 | U-ILD 主报告 PDF p9，Table 4 | PDF online p9 Table 4; p7 Results |

## 不一致及一方缺失

均无；无需数值裁决。P 值同时比对运算符，INBUILD 为 `<0.001`，不能写成 `=0.001`。

## 双方缺失的裁决建议

- RELIEF / treatment_adverse_events、control_adverse_events：盲抽取为 NOT_FOUND。A 未列入39个已核实数值；C 为 NOT_REPORTED。主报告 p7 为叙述，p9 Table 3 仅 SAE。阶段2才获知并读取正式 appendix 1，PDF p9 Table S6 只列发生率≥5%的具体AE；p10–11 Table S7为SAE；p12 Table S8为按免疫抑制分层的具体AE。各项人数有重叠，不能相加成“至少一次任意AE”总人数。保留缺失。
- U-ILD / primary_effect、primary_ci_lower、primary_ci_upper、primary_p_value：盲抽取为 NOT_FOUND；C 为 NOT_APPLICABLE，A 不列为已核实数值。主报告 PDF p5明确预设居家肺功能模型无法应用。保留结构化缺失；不以现场肺功能次要终点95.3 mL及其区间、P代替。NOT_FOUND是本轮检索状态，不与C的统计性NOT_APPLICABLE构成数值冲突。

## 统计解释及来源范围

- RELIEF 的1.69（95% CI −0.65至4.03）为Hodges–Lehmann估计；P=0.043为含诊断组因子的rank ANCOVA，不能解释成同一检验的区间/P配对。
- RELIEF −36.6/−114.4 mL为48周未插补事后观察均值，实际有效n=35/32；不是年化速率或主要FVC %预计值。
- U-ILD −17.8/−113.0 mL为24周现场肺功能次要终点预测均值，Table 2脚注有效n=118/119；C记录ITT总人群253作为总体框架，但不应让读者误以为253人均有该项有效测量。建议后续版本加effective_n；本复核不修改C。
- AE安全性分母：SENSCIS 288/288，INBUILD 332/331，TRAIL1 62/60，U-ILD 127/124；与随机分组总人数区分。
- A/C与独立抽取引用同一原文的不同页或表格，不因此判为不一致。

## 盲法限制

阶段1五个官方附件候选URL均403，未取得附件。`LOCAL_PDF_PATHS.md`未给出后来A来源清单中的4份附件路径。阶段2才读取该清单并打开本机附件，身份与SHA-256相符；这些附件审阅是**非盲补充核验**，不能追认成阶段1盲抽取。见 `stage2_supplement_review.json`。Git worktree创建时自动显示基线提交标题中的汇总字段数，属被动暴露；阶段1未打开已填值、核验文件或报告。基线标题未用于填数。
