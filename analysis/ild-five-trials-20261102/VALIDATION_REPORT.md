# C 首批验证报告

日期：2026-11-02。版本：0.1.0。独立学术验收：待验收。

执行：`python3 analysis/ild-five-trials-20261102/scripts/validate_extraction.py`

结果：PASS。五项研究独立记录，45 个候选数字槽均为 null / UNVERIFIED，并包含缺失原因、单位、来源定位、分析集和终点层级字段。sources 为空，说明 C 尚未独立阅读和登记原始来源。

负向验证：复制数据到内存后，删除缺失原因，校验正确拒绝；把尚未核实的 null 填成 0 且仍保留缺失状态，校验正确拒绝。没有修改正式数据文件。

`git diff --check`：通过。文件均新增于本任务目录；未修改历史成果。

本次未做原文数字比对，未验收任何医学结果，没有生成图表、合并分析或课件。机器校验不能证明来源真实或数字准确，A/C 对照和总控签收仍待进行。

Round2: 2 A-verified U-ILD secondary FVC values populated; 43 remain null/UNVERIFIED. Independent acceptance pending.
