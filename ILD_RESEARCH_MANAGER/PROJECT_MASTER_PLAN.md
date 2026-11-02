# ILD 科研项目总控计划
日期：2026-11-02。范围：SENSCIS、INBUILD、TRAIL1、RELIEF、U-ILD。

基线 origin/main：f0f40a8c9b647a755e362f120cc4f1d18ae755d7。
总控 codex/ild-manager；A codex/ild-literature（literature/）；C codex/ild-analysis（analysis/）；B codex/ild-presentation（presentations/）。各分支从同一 main 基线建立，使用同级独立 worktree。

## 工作顺序与交接
1. A 逐项核对原始论文、补充材料、注册记录；提交可追溯证据包，独立验收后冻结。
2. C 独立定义并提取数字，不复制 A 数值作为独立核验；与 A 对照差异，保留原始值和分析定义。
3. B 仅接受 A 已冻结版本，数字还须经 C 验收；先大纲与样张审核，再全套课件。本轮仅建立等待目录。
4. 总控记录分支 SHA、检查交付和冲突，必要时将已验收成果整合到总控分支；本轮不合并任何分支，不合并 main。

## 冻结要求
A 提交 freeze manifest：版本、明确提交 SHA、文件 SHA256、研究清单、核验层级、未解决项、审核者和批准日期。总控签署前 NOT_FROZEN；B 入口须核对 SHA 与清单。任何更正生成新版本，禁止静默替换。

## 当前里程碑
仓库和分支初始化；A 首批身份/来源核验；C study_extraction 结构；B WAITING_FOR_A_FREEZE。所有学术交付与 FINAL_QA_REPORT 均待验收。
