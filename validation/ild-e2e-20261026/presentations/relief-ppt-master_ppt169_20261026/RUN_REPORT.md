# RELIEF：ppt-master 完整流程验收

结论：本次三页课件的 Default Generate PPTX 路径已跑通，最终文件通过结构检查及 LibreOffice 逐页视觉验收。未测试 Microsoft PowerPoint 客户端。

## 验收文件

- [可编辑 PPTX](exports/relief-ppt-master_20261026_235721_native_charts_tables.pptx)
- [PDF 预览](rendered-release/relief-ppt-master_20261026_235721_native_charts_tables.pdf)
- [中文证据摘要](sources/RELIEF_summary_zh.md)、[讲者备注](notes/total.md)
- [文件哈希与原生表格核对](release_manifest.json)

## 实际流程与结果

| 环节 | 结果 |
|---|---|
| 仓库与技能预检 | 独立测试工作树和分支；attribution_guard 通过，未修改上游技能 |
| 方案确认 | 用户明确“按建议执行，后续设计由你决定”；按 delegated 路径，记录 decisions.md，未伪造 UI 回执 |
| 设计规范 | design_spec.md 与 spec_lock.md；16:9，中文学术白底，三页为设计、结果、安全性与局限 |
| 执行 | 手写三页 SVG；首屏检查后完成其余页，再完成最终质量检查 |
| 讲者备注 | total.md 分割为三份，全部嵌入 PPTX |
| 导出 | finalize 后 svg_to_pptx.py --native-charts-and-tables；3 页、1 个原生表格、可编辑文字，无整页位图 |
| 结构验证 | medical_validation.json：通过；3 页均有备注，无缺页或纯图片页 |
| 视觉验证 | LibreOfficeDev 26.8 转 PDF，三页 PNG 逐页查看；最终版无发现的文字截断或重叠 |
| 实时预览 | Flask 3.1.2 及依赖仅安装于本项目 .runtime；技能 live server 在云端 localhost:5050 启动，不代表用户浏览器可直接访问 |

SVG 检查为 0 errors、1 warning：结果表同格内置信区间和死亡处理说明被识别为拆分段落。两者语义独立，保留独立文本；最终渲染正常。导出 postflight 为 passed-with-warnings，quality_gate passed。

前两次试稿存在第一页面文字框宽度导致的截断/换行，已修正源 SVG 并重新执行最终检查、finalize、导出与渲染。旧试稿保留在本地且通过 .gitignore 排除发布；唯一验收版为 235721。未直接修改导出的 PPTX。

本设计不使用外部图像、图标、图表、动画或配音，相应条件步骤不适用；没有调用付费生成接口。Flask 缺失通过官方 wheel 的项目内安装补足，没有执行远程安装脚本，没有修改系统代理或沙箱策略。

## 医学出处与边界

Behr J 等，Lancet Respir Med. 2021;9:476–486。PMID 33798455；DOI 10.1016/S2213-2600(20)30554-3。引用原论文已发表汇总数据，不是个体患者原始数据。127 例随机，64/63；主要分析 P=0.043，Hodges–Lehmann 组间差 1.69 个百分点（95% CI −0.65 至 4.03），预设斜率敏感性分析 3.53（0.21 至 6.86）。不同统计程序分开解释。

死亡和严重感染为描述性事件计数；不据此声称生存获益、安全等效或各 ILD 亚型有效。研究提前终止、缺失数据和异质性限制解释。沿用此前核验材料，不补全全文，不新增下载；附录未获取的限制仍保留在备注中。原 PDF 首页侧栏 DOI 异常及正文题录核对结果见备注。

## 保存与后续

仅向 test/ild-e2e-20261026 保存课件、原创摘要、SVG、备注和验证记录；不包含原始论文 PDF、运行依赖或预览缓存。主分支不修改。提交与推送结果以 Git 历史及交付回复为准。

后续若用于正式授课，建议在目标 PowerPoint 版本确认字体兼容性，并按课程问题补充指南和其他研究比较；当前三页验证不构成完整系统综述。

使用仓库 [ppt-master](../../../../.agents/skills/ppt-master/SKILL.md) 工作流，保留其上游署名与 MIT 许可，未修改技能代码。
