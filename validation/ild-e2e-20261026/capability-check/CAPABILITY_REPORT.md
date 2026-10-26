# 能力补足报告

日期：2026-10-26（Asia/Taipei）。按本轮范围未补全文献、未发起新的文献下载。

## 已完成

- 当前环境已有 `soffice`，实测版本 LibreOfficeDev 26.8.0.0.alpha0。上一轮只查找libreoffice命令即判定缺少渲染器不充分，本报告更正该结论。
- 无需安装软件或更改环境安全配置，使用独立临时LibreOffice用户配置完成PPTX到PDF转换。
- 三页分别导出PNG并实际查看：中文Noto Sans CJK SC显示正常；标题、正文、表格、数值、CI和引文完整；无可见遮挡或裁切。
- 原三页测试件保留，另存RELIEF_3slides_validated.pptx：更新过时的“未渲染”状态文字、提高表头对比度；医学数据及引用不变。
- 新PPTX结构检查PASS：3页、3页非空中文备注、可编辑文本与表格、ZIP无损。备注不显示于普通PDF，另由PPTX结构检查验证。
- 新增可复用render_pptx.py：优先发现soffice或libreoffice，独立临时配置、120秒超时、新输出目录防覆盖、PDF页数校验、PNG导出、备注检查、可选引用检查和JSON日志。

## 复用

从仓库根目录执行（输出目录须不存在）：

```bash
python3 -B validation/ild-e2e-20261026/capability-check/render_pptx.py INPUT.pptx NEW_OUTPUT_DIRECTORY --citation 33798455
```

依赖：现有python-pptx、PyMuPDF、soffice及中文字体。不依赖requests或专用presentations工具；它们不是本次可编辑课件流程的必要阻塞项。专用工具并未安装或被声称可用。

## 验收边界

本次通过的是LibreOfficeDev渲染与逐页视觉验收，不等同于微软PowerPoint兼容性认证。首次转换出现Fontconfig缓存目录警告，但PDF生成成功且字体实际显示正常；后续脚本日志保留实际输出。既有最终全文覆盖和医学版本问题不在本轮范围内。

## 成果

- RELIEF_3slides_validated.pptx：可编辑验收版。
- validated-render/RELIEF_3slides_validated.pdf：演示PDF，不是文献原始全文。
- validated-render/slide-1.png 至slide-3.png：逐页渲染。
- validated-render/render_check.json、structure_check.json：验收记录。

仍使用test/ild-e2e-20261026分支；不修改main，不上传原始文献全文。
