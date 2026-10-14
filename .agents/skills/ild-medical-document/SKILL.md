---
name: ild-medical-document
description: Generate traceable Chinese ILD publication catalogues and evidence-intake documents in Markdown and editable DOCX from records that passed ild-evidence-check. Reopen outputs to verify citations and structure; do not claim a full-text review or clinical PPT workflow.
---

# ILD 医学文档生成

依赖：Python、python-docx；PDF 导出可选 LibreOffice。无需浏览器、收费 API 或特定 presentations 工具。

```bash
<python> <skill-root>/scripts/generate_document.py --records <records.json> --verification <verification.json> --out <new-doc-dir>
```

必须通过核验并匹配 records.json 哈希，失败时阻止生成。输出中文 Markdown、可编辑 DOCX、重读验证 JSON。文献目录含题名、作者、年份、期刊、PMID、DOI、研究类型、可访问状态、源位置与哈希。仅摘要注明未全文核验。

本技能交付文献元数据/证据入库文档，不替代专业临床审阅、GRADE 评级或医学 PPT 的大纲/样张确认流程。不得自动把原始摘要数字归结为临床疗效、不填补未报告字段、不输出未经审核治疗推荐。图表与临床解读须在另行确认的课件流程中执行。
