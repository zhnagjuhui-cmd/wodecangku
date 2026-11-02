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

## 第三轮 2026-11-02（最新状态）
- 开始时四工作树干净，无未提交改动；沿用上轮提交，无main合并，无原文件移动删除。
- 本机mdfind及find完成指定四目录搜索（含本项目、仓库literature/skills）；963条PDF路径，91条关键词候选（含重复/翻译/综述/课件）；路径清单在A分支 literature/ild-five-trials-20261102/LOCAL_PDF_PATHS.md。补充正文内容扫描的读取失败仅记录本地，不能断言未找到的补充材料不存在。
- 已读取SENSCIS、INBUILD、RELIEF主报告，校验%PDF、题名、页数、SHA-256并检查关键结果页渲染。PDF版权再分发权限未确认，未提交PDF，保留本地路径和哈希。
- A本轮23项数字有页码/表图出处；C严格匹配A字段，加上前轮U-ILD 2项，25/45非空、20/45 null/UNVERIFIED。INBUILD P<0.001保留算符；AE按患者人数和分母记录；RELIEF ANCOVA P与Hodges-Lehmann CI分开解释。SENSCIS580随机/576至少一剂差异由Fig1解释。
- TRAIL1候选文件名拼作TIRAL1；U-ILD正式PDF候选均定位，但部分读取Operation canceled或超时；正式PDF身份/数字/哈希尚不能全部核验。五项独立官方补充包、方案/SAP、历史注册一致性、完整偏倚风险及独立验收仍未完成。
- 用户文献站 https://ild-evidence-radar-zjh.zhnagjuhui.chatgpt.site 返回登录页；web不可访问，浏览器host不可用，没有取得可用文献，未用网站支持任何新数字。已请用户在Finder下载候选文件或提供附件目录；不影响已完成的本地可读资料核验。
- 冻结资格：NO。A保持NOT_FROZEN/approved_for_B=false，未签名未冻结；B保持WAITING_FOR_A_FREEZE且本轮无变更。
- A提交：40bb52ce8ccac797aa251bbe4a7895cba3aa4916；C提交：824fdbcb470a0c5565cf4c6499c5ae428f8450e7；B保持：af8dd67501001713cf9aa149ab6b79bad0bdd62d。总控提交以本分支HEAD为准，避免自引用。
- 验证：C结构及两项负控通过；23项A→C逐字段值/定位/单位/分析集精确匹配；总控保护分支/目录归属/B门禁及diff检查通过。均不等于独立学术验收。

### 第三轮最终更新（替代本轮早前25项和正文读取缺口）
五篇主报告均已找到可读本地副本，并校验%PDF、题名/DOI、页数、SHA-256及关键结果页渲染。TRAIL1和U-ILD使用Desktop/新课件副本；Documents占位/超时不再构成主报告获取缺口。所有原PDF未动、未提交。
A已定位37个字段；C37/45非空、8/45 null/UNVERIFIED，与A逐字段严格匹配。TRAIL1主要终点OR0.67（0.22–2.03），P=0.48；FVC为次要终点。U-ILD正式PDF核对前轮中心FVC结果一致，主要家庭肺量计模型不可应用的四槽保持空值并说明，安全分母127/124区别于ITT127/126。RELIEF另外四槽待定义/缺失处理匹配，不补猜测数字。
find覆盖全部指定目录963条路径；91条文件名候选；进一步读取医学资料256个唯一PDF，32个内容命中，路径/哈希清单在A分支LOCAL_READABLE_CANDIDATES.csv。43页Matteson候选是ICMJE作者披露表，不当作结果附件。完整五研究补充包、方案/SAP、历史注册核对、完整偏倚风险和独立验收仍未完成；文献站仍为登录页。本轮未冻结，冻结资格NO；B门禁不变。
最新A SHA：35e485d67c5e65d66528aa5070200909575153d6
最新C SHA：948ba49ed4090d229eb05639ebb65266e5210fe8
B保持SHA：af8dd67501001713cf9aa149ab6b79bad0bdd62d
总控以本分支HEAD为准；main及保护分支不变，无合并。C结构/负控、A→C37字段精确匹配、总控结构检查均通过；不等于独立学术验收。
