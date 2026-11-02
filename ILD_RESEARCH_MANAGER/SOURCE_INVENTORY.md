# 来源清单
本清单是检索入口，不是冻结证据。逐项获取/核验状态以 A 分支来源账为准。

|研究|原始论文入口|注册入口|
|---|---|---|
|SENSCIS|https://doi.org/10.1056/NEJMoa1903076 | https://clinicaltrials.gov/study/NCT02597933 |
|INBUILD|https://doi.org/10.1056/NEJMoa1908681 | https://clinicaltrials.gov/study/NCT02999178 |
|TRAIL1|https://doi.org/10.1016/S2213-2600(22)00260-0 | https://clinicaltrials.gov/study/NCT02808871 |
|RELIEF|https://doi.org/10.1016/S2213-2600(20)30554-3 | 原论文报告 EudraCT 2014-000861-32 / DRKS00009822；ClinicalTrials.gov 对应关系 UNVERIFIED |
|U-ILD|https://doi.org/10.1016/S2213-2600(19)30341-8 | https://clinicaltrials.gov/study/NCT03099187 |

2026-11-02 检索 PubMed / NEJM 原始研究记录建立入口。U-ILD 暂映射 Maher 吡非尼酮不可分类进行性纤维化 ILD 研究，需确认缩写含义后冻结。补充材料须从论文官方关联附件核验，不能用相关研究或协议代替。

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
