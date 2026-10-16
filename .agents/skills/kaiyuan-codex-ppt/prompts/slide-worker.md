# 单页 worker 交接模板

```text
你负责一页图片式 PPT 的生成与 QA。你并非唯一工作的代理，不要修改其他代理的文件，不要回滚他人的改动。

技能根目录：<kaiyuan-codex-ppt 的绝对路径>
依赖技能：<codex-imagegen-batch 的绝对路径>/SKILL.md
项目目录：<absolute deck>
唯一任务：<absolute deck>/prompts/slide_<NN>.json
独占运行目录：<job.image_run>
主代理独占：origin_image、slide_jobs.json、slide_run_state.json、deck_spec、outline、speech、最终PPT。

先读取两个 SKILL.md 和任务 JSON。核对当前会话是否有内置图像工具；没有则返回 blocker。只用任务中的完整 prompt、图片和已批准 image_policy；对每张本地参考图自行 view_image，样张标 style，内容图标 reference，修改对象标 target。不能假设父代理的图片上下文已传入。

用 image_gen.py prepare/claim 创建并领取你的独立队列，然后调用内置图像工具。Python 不能生图。工具返回后按宿主要求显示原生图，并用它明确返回的本地路径 record。随后 finish，查看实际输出、尺寸、中文、保留项、数据和样张风格。通过后 approve，并 packet 保存 result.json。

不读取密钥、不上传本地图换URL、不调用外部生图API、不启动其他Codex进程、不改变后端、不用本地绘图/HTML/SVG/Pillow/文字叠加制造最终页面。已批准尺寸后处理由适配器执行并保留原图。质量重试仅按项目授权预算；结果不确定不自动重发。

样张只作风格参考，不能复制样张的标题和内容。遵守 sample_generation_method 的工具与上下文准备；工具没有相应尺寸/模型参数时不能编造。不能获取明确对应的本地文件则报告阻塞。

完成后返回：
backend_used=codex-imagegen-batch / built-in image tool
image_run=<你的独占运行目录>
result_json=<image_run>/result.json
selected_source=<已批准的output路径>
qa_note=<一段真实视觉核验结论，包含实际尺寸及后处理>
```
