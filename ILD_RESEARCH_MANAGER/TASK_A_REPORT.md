# 任务 A：文献核验
状态：首批已提交；独立学术验收待验收；NOT_FROZEN。
提交：b2c6871df5cf388523e68d1b2d4fe241ff695835。
路径：literature/ild-five-trials-20261102/（A 独立工作树/分支）。
五篇主报告身份/摘要已核验；15 行来源清单区分主报告、补充及注册。四项 ClinicalTrials.gov API JSON 已保存并保留 SHA256；当前登记信息首核，不代表历史及全文对照完成。RELIEF 官方 DRKS/EudraCT 身份已核验，NCT 对应仍 UNVERIFIED。
SENSCIS 登记 enrollment 580，摘要至少一次治疗 576，须保留分母语义，待全文解释。
全文、补充材料和完整一致性核验存在缺口。冻结 manifest 为 NOT_FROZEN / approved_for_B=false。总控结构检查不代替独立学术复核。
下一步：合法全文及补充获取、历史注册对照、逐字段双核与冻结审核。审核者/批准日期：UNVERIFIED。

## Round 2 - 2026-11-02
User confirmed U-ILD = Maher pirfenidone unclassifiable progressive fibrosing ILD phase 2. Identity resolved against DOI/PMID/NCT. A acquired institutional accepted DOCX, verified selected Table 1/2 numbers with SHA256; publisher page mapping UNVERIFIED. RELIEF: DRKS00009822 / EudraCT 2014-000861-32 confirmed on official registry; NCT UNVERIFIED. Other primary full texts and supplements remain UNVERIFIED. A NOT_FROZEN; freeze conditions NOT MET; independent review pending.
C populated only two A-verified U-ILD site FVC secondary outcomes (-17.8/-113.0 mL, Table 2, 24 weeks); 43 slots remain null/UNVERIFIED. Structural validator and negative controls passed; this does not certify medical accuracy. No cross-trial efficacy ranking. No main merge.
A SHA: 4acb82098881a9388e4489950e930a48da1c918d
C data SHA: 48348ed401ed2c62ba6739b18491c1fae8a49588
Outstanding: four primary full texts, complete supplements, stable page mapping, analysis/safety denominators, historical registry reconciliation and independent acceptance. No user decision required to continue lawful retrieval; optional provision of institutionally accessible source files may help.

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
