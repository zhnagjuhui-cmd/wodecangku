# 任务状态
|任务|状态|本轮交付|验收|
|---|---|---|---|
|总控|INITIALIZED|计划、契约、来源和版本台账|待验收|
|A 文献|FIRST_BATCH_READY / NOT_FROZEN|五研究首批核验与注册JSON快照|待独立验收|
|C 数据|FIRST_BATCH_READY|study_extraction 结构与缺失规则；结构检查通过|学术待独立验收|
|B 表达|WAITING_FOR_A_FREEZE|目录和门禁|待验收；不得开始医学内容|
|最终整合|PENDING|无分支合并|待验收|

精确提交见 BRANCH_LEDGER.json。结构检查通过不代表文献、数字或课件验收通过。

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

## 第四轮（2026-11-02，最新总控记录）

- 用户指令：先补补充材料及剩余8槽、核验后再决定冻结；本轮未自行冻结。A NOT_FROZEN，approved_for_B=false；B保持WAITING_FOR_A_FREEZE。
- 新取得12份官方PDF：SENSCIS/INBUILD/TRAIL1/U-ILD方案+SAP各2份共8份；RELIEF补充1/2、TRAIL1补充、U-ILD补充共4份。另取得RELIEF 2017方案发表XML。文件身份/页数/路径/SHA-256与失败日志见A ROUND4_SOURCE_FILES.json。PDF只留本机local-audit/round4，不提交，原文件不移动删除。未识别新增既存本地目标附件；不声称不存在。
- 45槽均已审查；39/45为已核实可填数字（第三轮37/45），6槽仍null/UNVERIFIED。新增RELIEF两组48周FVC -36.6/-114.4 mL，主文online p7 Table2，事后、未插补、可用配对35/32；不替换主要百分点终点。RELIEF任何AE患者并集2槽未报告，不加总preferred terms或用SAE替代；U-ILD主要模型无法应用4槽保持空，不搬用次要中心FVC。
- 方案/SAP与当前注册/发表报告选定终点对照见A ROUND4_PROTOCOL_REGISTRY_REVIEW.md。SENSCIS/INBUILD主要终点及分析人群相符；TRAIL1方案版本与SAP/实际锁库时序、RELIEF中期后最终SAP预先性仍需追溯；U-ILD SAP包含2018和2020版本，后者不可回填为2019预设结果。四NCT完整历史接口403，RELIEF完整官方历史亦未取得，历史一致性UNVERIFIED，未以当前快照替代。
- 五研究RoB五域初评见A ROUND4_RISK_OF_BIAS.md，保持待独立裁决；不能把效能不足自动当偏倚或把未显著当阳性。
- 同一代理重新打开五份原始PDF抽取对照，原有37项数值一致；新增2项亦经文本和结果页视觉核对。ROUND4_REEXTRACTION_COMPARISON.json覆盖45槽。此为重复核对，不是真正第二独立审核；独立验收仍PENDING，未冒签。
- C只消费A39项已核实数字，逐项值/单位/分析集/层级/时间点/定位/P算符/AE分母匹配；data_quality_report.md已更新。结构和两项负控通过，13新源文件及五主报告原哈希复验通过。这些检查不等于独立学术验收。跨试验仅描述性比较。
- 冻结条件结论：**不满足，不建议当前冻结A**。尚缺两NEJM结果附件、完整注册历史及部分版本时序证据、独立学术复核/RoB裁决。剩余6槽中4项为原报告模型不可用，并非必须猜填到45/45；未来冻结须以明确缺失机制和证据边界验收，仍由用户决定。
- A分支codex/ild-literature：ee5371fd5e4f8f8ca64d6118e690009323375e49
- C分支codex/ild-analysis：0dbe6ade63a8c8f35cf6da3c431ebfef87d8c7ce
- B分支codex/ild-presentation保持：af8dd67501001713cf9aa149ab6b79bad0bdd62d
- 总控SHA以本分支HEAD为准，避免自引用；main和保护分支未合并、未变更。只提交各归属目录，保留前三轮成果。
