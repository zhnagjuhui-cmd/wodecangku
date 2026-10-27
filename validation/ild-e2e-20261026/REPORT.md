> 最新：已完成 [ppt-master 完整制作与验收](presentations/relief-ppt-master_ppt169_20261026/RUN_REPORT.md)，含原生表格、讲者备注和逐页渲染。

> 更新：本轮已补齐渲染及逐页视觉验收；以下保留首轮历史结果，当前能力以 [能力补足报告](capability-check/CAPABILITY_REPORT.md) 为准。不再补全最终全文。

# ILD-Evidence 云端端到端验证报告

测试日期：2026-10-26（UTC）。结论：**部分通过**。当前云端可完成网络检索、合法全文获取（至少一项）、可追溯证据提取及可编辑PPTX生成；不能宣称五项原始PDF全部获取，也未完成PowerPoint/LibreOffice视觉验收。GitHub结果见本报告末尾及 `logs/git_verification.json`。

## 1. 预检与隔离

- 实际项目：`/workspace/wodecangku`，远端 `https://github.com/zhnagjuhui-cmd/wodecangku`，公开仓库。ILD-Evidence 是任务名称，实际GitHub仓库名称为 wodecangku。
- 原始分支 `work`，基线 `f0f40a8c9b647a755e362f120cc4f1d18ae755d7`，开始时无未提交修改。远端默认分支 `main` 与基线相同，另有 `skills-validation-20261014`。
- 隔离工作树 `/workspace/ild-e2e-20261026`，独立分支 `test/ild-e2e-20261026`；原工作树维持 `work`，不切换、不修改main。
- 所有新成果位于本目录 `validation/ild-e2e-20261026/`；未删除或覆盖原有成果。仅提交测试目录。
- 云端状态：observations_current=true，unrestricted/enforced，环境running。联网命令通过执行工具 `with_additional_permissions` 的 network.enabled=true；保留继承代理及TLS验证，未改沙箱策略、代理、路由或环境配置。
- python-pptx、lxml、Pillow、PyMuPDF可用；requests和LibreOffice不可用，专用presentations工具未提供。标准库urllib满足本次检索，无安装行为。

## 2. 技能验证

`python3 -B scripts/check_skills.py`：10项技能及必要文件全部PASS。包括 medical-evidence-ppt、medical-slide-source-update、ppt-master、ppt-image-reconstruction 等；该结果证明文件完整性，不等于各外部接口均可运行。

已阅读医学证据PPT技能、原图更新技能及所选证据/编辑/QA参考。实际采用医学证据规范和现有 `validate_pptx.py`；以可用python-pptx代替缺失presentations能力。此次是用户明确指定的三页端到端测试，直接制作测试件；未宣称经过正式课件的大纲和样张人工审批流程。没有测试收费生图、外部密钥或其他未使用技能。

## 3. 原始研究身份与主要终点

| 研究 | PMID / DOI | 设计 | 样本量口径 | 主要终点 |
|---|---|---|---|---|
| SENSCIS | 31112379 / 10.1056/NEJMoa1903076 | 随机双盲安慰剂对照，SSc-ILD | 原文576例接受至少一剂；注册入组580例，不混为同一口径 | 52周FVC年下降率 |
| INBUILD | 31566307 / 10.1056/NEJMoa1908681 | 随机双盲安慰剂对照Ⅲ期，进展性纤维化ILD | 663例接受治疗；注册663 | 52周FVC年下降率；总体及UIP样人群 |
| TRAIL1 | 36075242 / 10.1016/S2213-2600(22)00260-0 | 随机双盲安慰剂对照Ⅱ期，RA-ILD | 随机123例，63/60 | 52周FVC%较基线下降≥10%或死亡复合终点 |
| RELIEF | 33798455 / 10.1016/S2213-2600(20)30554-3 | 随机双盲安慰剂对照Ⅱb期，四类非IPF进展性ILD | 随机127例，64/63 | 48周FVC占预计值百分比的绝对变化，ITT秩ANCOVA |
| U-ILD | 31578169 / 10.1016/S2213-2600(19)30341-8 | 随机双盲安慰剂对照Ⅱ期，不可分类进展性纤维化ILD | 随机253例，127/126；安全集127/124 | 24周每日家庭肺功能测量的FVC预测变化 |

正式题名、作者、发表年、干预、主要结果及出处见 `literature/evidence.md` 与 `evidence.csv`。TRAIL1在线发表于2022年、期刊2023年；U-ILD在线2019年、期刊2020年，不应视为题录不匹配。

核验方法：Europe PMC REST的MED原始记录（含PMID、DOI、摘要）匹配Crossref正式题名/DOI；SENSCIS、INBUILD、TRAIL1、U-ILD另外读取ClinicalTrials.gov API原始注册JSON核对样本与主要终点；RELIEF读取原PDF并访问DRKS00009822注册入口。RELIEF未做注册历史版本逐字段审计。

重要边界：SENSCIS/INBUILD仍主要依赖正式摘要与注册记录；TRAIL1和U-ILD取得作者稿、核对身份，未将作者稿当作最终排版版逐段全文核验。RELIEF完成目标PDF关键方法与结果核验，未取得补充附录。研究提取不是完整系统综述，也不代表当前指南/适应证审查。

## 4. 实际网络与合法全文下载

| 研究 | 尝试与响应 | 保存结果 | 判断 |
|---|---|---|---|
| SENSCIS | NEJM PDF 403；ZORA返回200但非PDF；ULB旧链接跳转INVALID_ID页面 | 无原始PDF | 失败：访问限制/失效链接；未绕过 |
| INBUILD | NEJM PDF 403；ULB返回200但为INVALID_ID HTML | 无原始PDF | 失败：200不等于下载成功 |
| TRAIL1 | Lancet CONNECT 403；公开机构Figshare API和下载成功 | 作者修订稿DOCX，已解压读正文；非最终版PDF | 作者稿获取成功，原始PDF未获得 |
| RELIEF | Helmholtz公开存档200 application/pdf | PDF 858537字节，11页，已验证签名、解析、题名及正文DOI | 原始论文PDF下载与读取成功 |
| U-ILD | Imperial Spiral公开存档200；下载200 | 作者稿DOCX 799328字节，已解压读正文 | 作者稿获取成功，原始PDF未获得 |

RELIEF SHA-256：`0d61089a16b3e550fd1f41115d3fd45617324efccac80360ae8ead24a2653136`。机构入口：https://push-zb.helmholtz-muenchen.de/deliver.php?id=32778 。文中版权声明All rights reserved；仅在本地研究，未重发布。PDF首页侧栏出现不同DOI后缀30532-4，但题名、作者、正文页眉及MED/Crossref一致指向30554-3；这是需保留的版本异常，不静默忽略。后续正式授课建议用出版社最终版本再次核对。

PubMed五个具体题录均返回203验证HTML，不能把前一轮首页200当作题录或全文已可获取。Europe PMC/Crossref和ClinicalTrials.gov API均实际成功。OpenAlex/Europe PMC的开放标签只用于发现合法来源，不作为已下载证据。未使用非法来源、付费墙绕过或修改代理。

原始PDF/DOCX、全文提取文本、搜索响应和网页均保留本地，但由本目录 `.gitignore` 排除；公开Git仅保存原创摘要、汇总事实、来源清单、脚本、日志与测试课件。下载日志不保留签名下载URL查询参数。

## 5. 中文摘要与三页PPTX

- `literature/RELIEF_summary_zh.md`：中文研究摘要，包含研究设计、效应、CI、P值、安全性及局限。
- `presentations/RELIEF_3slides_test.pptx`：3页，设计/结果/安全性与局限，每页页内引文和中文讲者备注；文字与数据表均为原生可编辑对象。
- “原始数据”指原论文发表的汇总数据，不是个体患者数据。没有虚构IPD、曲线或误差线。
- 忠实保留主要分析P=0.043与Hodges–Lehmann差1.69个百分点（95%CI −0.65至4.03）的区别；不把敏感性分析替代主要终点，不把少量死亡计数解释为死亡获益。
- 原仓库验证脚本PASS：3页、3页非空备注、ZIP无损、无整页图片；进一步python-pptx重开成功、notes关系一一对应、所有对象在页面边界内。
- **视觉验收未通过/尚未执行**：未提供LibreOffice/PowerPoint。对象边界检查不能证明无文字溢出或字体替换。未宣称原生PowerPoint打开或逐页渲染成功。课件是测试文件，非正式授课验收版。

## 6. 成功、限制和修复建议

| 环节 | 结果 | 下一步 |
|---|---|---|
| 环境与隔离 | 通过 | 沿用显式网络权限和独立工作树 |
| 五项研究检索与核心字段 | 通过，全文核验深度不同 | 补齐最终全文后复核方法/附录和勘误 |
| 五项原始PDF全覆盖 | 部分通过：1/5 | 从有效机构存档或有权使用的订阅渠道获取；不绕过验证/付费限制 |
| 证据提取 | 通过 | 正式使用前做独立人工医学复核，尤其RELIEF版本异常与SENSCIS样本口径 |
| PPT生成与结构校验 | 通过 | 保留原生对象和逐页备注 |
| PPT渲染与视觉验收 | 未完成：缺少渲染器 | 在受支持环境提供LibreOffice或PowerPoint后渲染全部3页，检查中文、排版及脚注 |
| 技能完整性 | 10/10通过 | 专用presentations及其他外部技能需另行配置验证 |
| GitHub保存 | 见下方实际结果 | 只推测试分支；无合并、无main更新 |

## 7. 文件与复现

`logs/fetch.json`、`additional_fetch.json`、`final_fetch.json` 记录下载结果；`source_manifest.json`记录来源、哈希和本地文件。`scripts/build_test.py`重建证据与课件；`scripts/fetch_sources.py`读取本地 `original_records.json` 抓取来源。该原始响应未公开提交，首次复现需按source_manifest中的Europe PMC查询重新取得相同记录，不能声称仅克隆Git即可离线重现全文下载。

未执行未知安装脚本，无软件安装，无患者资料，无密钥写入成果。默认分支不修改，原工作区不动。未进行跨试验药物优劣比较。

## 8. GitHub实际验证结果

独立分支 `test/ild-e2e-20261026` 推送成功（exit 0），首个成果提交 `79c4729b8739e82f2e5e9ed74219fb8875b67a29`。远端main仍为基线 `f0f40a8c9b647a755e362f120cc4f1d18ae755d7`；原工作树保持work且无未提交变更。未创建PR、未合并、未推送全文。此结果记录通过后续独立提交同步至同一测试分支。

浏览：https://github.com/zhnagjuhui-cmd/wodecangku/tree/test/ild-e2e-20261026/validation/ild-e2e-20261026
