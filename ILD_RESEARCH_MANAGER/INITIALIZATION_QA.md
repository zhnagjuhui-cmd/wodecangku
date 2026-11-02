# 初始化 QA（结构通过，学术待验收）

2026-11-02 总控检查：

- main 基线 f0f40a8c9b647a755e362f120cc4f1d18ae755d7 保持不变；两个指定历史分支 SHA 见 BRANCH_LEDGER.json。
- 四分支与独立工作树存在；相对基线仅新增归属目录文件，未删除/覆盖既有成果；未合并任何分支。
- A：15 行来源清单可解析；四项注册 JSON 的 NCT ID 与保存 SHA256 一致；NOT_FROZEN 且 approved_for_B=false。
- C：总控重跑脚本，五研究45个空值字段通过；两项负向输入均被拒绝。医学数字未提取。
- B：INPUT_GATE 状态 WAITING_FOR_A_FREEZE，A/C版本未填，未制作医学内容。
- A/C/B 本地提交已推送；总控分支提交后推送，最终四分支远端 SHA 在交付回执核对。

复现：python3 ILD_RESEARCH_MANAGER/validate_initialization.py（需保留同级工作树布局）；C脚本位于独立 C 工作树 analysis/ild-five-trials-20261102/scripts/validate_extraction.py。

此检查只证明初始化和文件结构，不能替代来源全文核验、数字双核、A冻结或课件验收。FINAL_QA_REPORT.md 仍待验收。
