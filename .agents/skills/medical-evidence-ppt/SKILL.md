---
name: medical-evidence-ppt
description: Create evidence-led, editable Chinese medical academic PPTX decks from recent literature using outline, sample-slide, and full-deck approval gates. Use for medical congress talks, regional or departmental education, KOL lectures, guideline interpretation, clinical-study reviews, disease-management pathways, and similar clinician-facing presentations; do not use for general business decks.
---

# 医学循证 PPT

## 目标

交付证据可追溯、表达合规、逐页带中文讲者备注且真正可编辑的中文医学 PPTX。不得把整页图片或截图包装成“可编辑 PPT”。

## 开始前

确认或从上下文提取：

- 医学主题与暂定标题；
- 总页数或演讲时长；
- 会议场景、科室和听众层级；
- 用户提供的文献、资料库、模板、Logo、产品信息和必须保留内容；
- 语言、讲者备注、互动页、截止时间等交付要求。

若用户明确要求药企推广 PPT 或调用 `pharma-ppt`，先完成该技能规定的逐项需求采集和合规检查，再执行本技能流程。

## 不可跳过的阶段闸门

1. 建立证据库和证据目录。
2. 提交逐页大纲，等待用户确认。
3. 制作一页有代表性的“研究解读页”样张，等待用户确认。
4. 按已批准的大纲与视觉基准完成全套。
5. 渲染并逐页检查，完成页数、备注、证据和可编辑性验证后交付。

大纲获批只授权进入样张；样张获批只授权进入全套。用户限定“仅修改第 N 页”时，只修改该页及其备注，不得顺手改动其他页面。

详细执行顺序见 [references/workflow.md](references/workflow.md)。

## 证据规则

- 默认检索近 5 年核心文献；为建立标准、历史背景或关键试验链条，可保留更早的里程碑研究。
- 优先级：指南/共识与监管文件、高质量原始研究、系统综述/Meta 分析、高质量综述；会议摘要和探索性小样本只能作为补充。
- 只从合法来源获取全文。不得绕过付费墙；“开放获取”标签不等于 PDF 已下载，必须验证文件可打开且确为全文。
- 将证据明确标为：直接证据、桥接证据、背景证据、探索性证据、仅摘要证据。不得用广泛人群的桥接证据冒充目标疾病的直接疗效证据。
- 每项关键研究保留：研究设计、样本量、人群、干预/暴露与对照、终点和时间点、效应量与不确定性、主要局限、证据角色和准确引文。
- 关联性结果不得写成因果关系；不得跨试验作头对头优劣比较；不得把替代终点写成死亡或生存获益；不得作无依据的超说明书宣传。

证据分层、全文状态和措辞边界见 [references/evidence-and-compliance.md](references/evidence-and-compliance.md)。

## 大纲要求

逐页大纲至少列出：页码、页面角色、结论式标题、核心证据与研究类型、关键定量结果、临床解读、局限、拟用视觉和讲者备注重点。大纲必须形成从疾病认识到决策与管理的证据链，而不是文献罗列。

页数分配应服从主题与受众，不机械套用本项目页序。可以覆盖疾病认识、临床研究、指南/共识、表型或分型、治疗路径、特定治疗证据、安全管理与总结等模块。

## 样张要求

选择最难、最能代表全套质量的研究解读页，而非只做封面。样张必须同时验证：

- 文献原图或忠实复现图的呈现方式；
- 研究设计、样本量、关键数据、局限与证据等级；
- 白底、深酒红标题、青绿色结论条的视觉体系；
- 页面元素可编辑性和中文讲者备注。

将 [assets/medical-journal-style-reference.png](assets/medical-journal-style-reference.png) 仅作为视觉风格参考，不得复制其中的疾病结论或数据。

## 视觉与图表

- 默认：白底，深酒红 `#8C0D27` 标题与强调，青绿色 `#087B78` 结论条，深灰正文和冷灰辅助线。
- 研究解读页优先使用论文原始图。若版权、清晰度或版式要求需要重绘，应忠实保留坐标轴、组别、方向、数值、误差/置信区间和统计学标识。
- 不得用生成式图片替代数据图、森林图、Kaplan–Meier 曲线或指南算法。
- 结论要醒目，但不能覆盖不确定性或局限；引文必须在页面上可见。

页面结构与图表规范见 [references/design-system.md](references/design-system.md)。

## 可编辑 PPTX

使用 `presentations` 能力创建或编辑 PPTX。除论文原图等必要位图外，标题、正文、引文、结论条、流程、表格、图例和可重绘图表均应为原生文本/形状/图表对象。论文图应作为独立图片元素嵌入，不得把整页合成为一张背景图。

每页必须添加与该页内容一致的中文讲者备注；不设置互动页，除非用户明确要求。详见 [references/editable-pptx.md](references/editable-pptx.md)。

## 最终验收

交付前必须：

1. 渲染全部页面并逐页检查中文字体、遮挡、裁切、对齐、图表清晰度、引文可读性和视觉一致性。
2. 核对实际页数与目标页数，且每页都有非空讲者备注。
3. 抽查所有研究解读页是否包含设计、样本量、关键结果、局限和证据等级。
4. 检查全文受限、桥接、探索性或会议摘要证据是否显著标注。
5. 检查关键文本和结构是否为原生可编辑对象，并排除整页图片化。
6. 运行：

   ```bash
   python3 scripts/validate_pptx.py output.pptx --expected-slides N --require-notes --require-editable
   ```

7. 确认 PPTX 可打开、ZIP 结构无损、备注页存在，并形成验收报告。

完整清单见 [references/qa-and-handoff.md](references/qa-and-handoff.md)。

## 交付物

- 最终可编辑 PPTX；
- 文献证据目录，注明全文状态与证据角色；
- 已批准的逐页大纲；
- 每页中文讲者备注；
- 使用的论文图和其他素材；
- 页数、备注、可编辑性与逐页视觉检查报告；
- 无法核实、仅摘要或仍受限内容的明确说明。
