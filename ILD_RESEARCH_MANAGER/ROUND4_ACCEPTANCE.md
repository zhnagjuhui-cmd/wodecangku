# 第四轮冻结条件检查

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

|条件|结论|
|---|---|
|五主报告身份与路径哈希|已核对|
|45槽处置/数字可填|已审查45；可填39；留空6|
|全部五研究结果补充材料|未齐：SENSCIS/INBUILD结果附件403|
|五研究方案/SAP选定部分对照|已做，存在版本时序未解项|
|完整注册历史|UNVERIFIED|
|偏倚风险|五域初评，独立信号问题裁决待完成|
|第二独立学术复核|未完成；仅同代理重新抽取|
|总控签收/用户冻结|未签收；未冻结|
