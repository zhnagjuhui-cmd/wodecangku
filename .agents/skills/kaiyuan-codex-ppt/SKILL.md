---
name: kaiyuan-codex-ppt
description: 配合 codex-imagegen-batch 与 Codex 内置图像工具制作统一风格的图片式 PPTX，保留大纲、风格、一页样张审核、逐页子代理、讲稿和组装流程；本地参考图可直接使用，无需第三方密钥、接口地址或公开图片 URL。
---

# kaiyuan-codex-ppt

## 工作方式

保留原开源先锋的图片式 PPT 工作流：deck_spec.json、prompts/slide_XX.json、slide_jobs.json、slide_run_state.json、origin_image/slide_XX.png、speech.md 和最终 PPTX。正文是一张整页图片，讲者备注可编辑；不声称图片文字和图表是原生可编辑对象。

唯一生图路径：读取已安装的 **codex-imagegen-batch/SKILL.md**，由 Codex 或其逐页子代理调用当前会话的内置图像工具。Python 只管理任务和文件，不会生图。不得调用外部生图接口、读取密钥、要求 URL、另开 Codex 进程或偷偷切换后端。内置工具仍联网并消耗 Codex 额度。

## 阶段与审核

先读 [docs/workflow-gates-and-progress.md](docs/workflow-gates-and-progress.md)。顺序保持：资料读取和素材提取 → 语言与大纲确认 → 风格确认 → 后端及项目图片策略确认 → 一页样张批准 → 逐页并行生成 → QA、备注、组装。

- 用户已明确的信息不重复询问；用户明确授权跳过某确认时按其授权执行。
- 大纲未批准前不创建正式 deck_spec、speech、提示词任务、全套图片或 PPTX；必要的内部草稿用 .draft. 文件名。
- 有必用原图时，在大纲阶段先确认图与页面的对应关系。
- 语言必须明确，并贯穿大纲、提示词、讲稿与 QA。
- 样张是代表性内容页，批准后复用，不重复生成该页。

风格与样张见 [docs/outline-style-and-sample.md](docs/outline-style-and-sample.md)；10 种原有参考风格保留在 references/。用户提供 PDF/PPTX 风格时先渲染代表页查看，不凭 XML 或文本猜风格。

## 依赖和项目策略

读 [docs/backend-selection.md](docs/backend-selection.md)，运行 `scripts/image_gen.py check` 检查本地依赖。它只检查技能文件；主代理和每个 worker 还须确认自身会话存在内置图像工具。依赖缺失或 worker 没有工具时记录 blocker，不切换外部接口。

在样张阶段将以下 image_policy 一次确认，写入样张任务和 deck_spec，由所有页面继承：

- target_size（默认请求 2560x1440）与 fit（默认 verify，仅校验）。
- accept_actual_size（默认 false）。工具原生像素不保证满足请求；不得伪报原生 2K/4K。
- approved（用户是否已授权尺寸后处理/接受实际尺寸/自动质量重试）。
- auto_quality_retry（默认 false）、max_attempts（默认 3，包含首次生成）。
- 原有清晰度门控阈值：min_edge_stddev=18、min_contrast_stddev=28。

只有明确批准项目策略后才能自动执行 contain/cover/stretch、接受实际尺寸或有预算的质量重试。原图始终保留。结果不确定时不得自动重发。用户只批准一个策略，不等于批准所有处理选项。尺寸/重试授权属于当前项目，不是修改全局 codex-imagegen-batch 的行为。

## 样张和生产

具体 CLI 与任务字段见 [docs/native-image-workflow.md](docs/native-image-workflow.md)。

1. 准备一页样张任务，`image_gen.py prepare` 建独立队列，`claim` 领取；查看每张本地参考图并标明 style/reference/target。
2. 使用内置工具生成（此环境为 image_gen.imagegen）；返回后立即呈现原生图片结果，不打印 base64。将明确对应的本地输出 `record`，再 `finish`，视觉核验后 `approve`。
3. 向用户展示样张，批准后用 `sample --user-approved` 登记；将返回的 sample_generation_method 和 approved_style_reference 写入 deck_spec。
4. 用 prepare_slide_prompts.py 创建正式逐页任务。该脚本保留原逐页上下文及样张风格引用，增加 image_policy 与每页独立 image_run。
5. 全套生成仍使用子代理，一页一个 job，按可用槽位分批派发；不能因为方便而全部串行。如果运行环境不能派发则报告阻塞，由用户改变要求后才改执行方式。
6. 每个 worker 的 image_runs/slide_XX 是独立队列，因此可以并行且不违反 codex-imagegen-batch 的单队列限制。子代理不写 PPT 总状态或 origin_image。
7. 主代理用 record_slide_dispatch.py 记录真实 agent ID。worker 读取 [prompts/slide-worker.md](prompts/slide-worker.md) 的交接任务，完成自己的队列和 QA，返回 result.json 路径。
8. 主代理查看返回图，用 record_slide_result.py 接收已完成队列的结果，验证后端、哈希、页面、派发任务及来源，复制到 origin_image。
9. 失败用 record_slide_blocker.py 记录；已有图片先恢复保存与核验。进度以脚本状态和真实文件为依据，不捏造服务端百分比。

派发、恢复细节见 [docs/slide-generation-and-subagents.md](docs/slide-generation-and-subagents.md)。

## 参考图与修复

本地参考图的绝对路径直接传入工具；对话附件按工具的图片上下文规则处理。每个 worker 自己 view_image，不把父代理看过图片等同于 worker 已看到。

按 [docs/user-supplied-assets.md](docs/user-supplied-assets.md) 保留必用原图及其数据、标签和轴线；生成后核对，不能保证逐像素无损。批准样张只作风格引用，不复制其标题和内容。

局部修复使用内置编辑工具；为修复建立新版本任务/队列，将旧页面作为 target，保留不变项；不要用 Pillow、HTML/SVG 或文字叠加伪装成生图。尺寸处理是可授权的后处理，和生成后端分开记录。

## 讲稿、组装与交付

读 [docs/project-assembly-and-reporting.md](docs/project-assembly-and-reporting.md)。保持原 speech.md 的 Slide N 标题、可朗读讲稿及独立“注意点”格式。组装前每页必须为 accepted/recorded，图片、哈希、页数顺序与备注对应检查通过。

assemble_ppt.py 保留原有 16:9/4:3 图片装配和压缩方式，新增代码级组装前检查，避免把未完成页面装入 PPT。新运行环境只安装 python-pptx、Pillow、filelock；不包含接口配置或认证。

交付项目、PPTX、逐页图片、讲稿及实际后端/尺寸/后处理/重试记录。保存风格供以后复用时，读 [docs/style-library.md](docs/style-library.md)，只保存视觉规则。
