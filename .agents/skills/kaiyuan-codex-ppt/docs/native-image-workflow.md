# 单页队列适配与 CLI

所有命令里的路径应为绝对路径；{skill_root} 是本技能目录。安装依赖和队列的实际生图能力分开检查。Python 不调用图像模型，prepare/claim 后必须由 Codex 调用内置工具。

## 任务与策略

样张任务（大纲、风格、后端已确认后创建；样张属于实际最终页号）：

```json
{
  "slide": 1,
  "prompt": "生成中文16:9整页PPT。标题：湖泊水循环。正文三点：蒸发、凝结、降水。使用确认的清爽专业风，白底深蓝字。无水印、无页码。",
  "operation": "generate",
  "input_images": [],
  "image_policy": {
    "target_size": "2560x1440",
    "fit": "verify",
    "approved": false,
    "accept_actual_size": false,
    "auto_quality_retry": false,
    "max_attempts": 3,
    "min_edge_stddev": 18,
    "min_contrast_stddev": 28
  }
}
```

只有用户明确同意后才能将 approved 设为 true，并启用其实际选择的处理。例如授权留边到目标尺寸可设 fit=contain；授权接受原生实际尺寸可设 accept_actual_size=true；不能因为 approved=true 就打开所有选项。不同尺寸/处理政策应先在样张上确认效果。

input_images 每项可用 path 或 conversation，加 input_role=style/reference/target；role/fidelity 为可读的详细约束。完整提示词仍写出图片角色及保留要求。edit/style-transfer 需要 target；已有图像的修复建立独立版本任务，禁止覆盖既有队列。

## 执行循环

```sh
python3 {skill_root}/scripts/image_gen.py prepare --job {job_json} --run-dir {deck}/image_runs/slide_01
python3 {skill_root}/scripts/image_gen.py claim --run-dir {deck}/image_runs/slide_01
```

读取返回 job，逐张 view_image，再调用当前内置工具。此环境所有参考图为本地文件时传 referenced_image_paths；有仅存在对话中的参考时按工具说明使用 num_last_images_to_include，不混用。新回话看不到附件则重新附图；不默默跳过。

此环境生成返回后用 generatedImage(result) 呈现原生图。使用明确对应的工具输出路径记录，不能挑目录里“最新图片”。

```sh
python3 {skill_root}/scripts/image_gen.py record --run-dir {run} --image {generated_local_path} --tool-name image_gen.imagegen
python3 {skill_root}/scripts/image_gen.py finish --run-dir {run}
```

finish 按预先批准的策略调用 codex-imagegen-batch 的 finish，保留 originals/ 原图和 outputs/ 交付图，运行原有清晰度启发式。主体、中文、数据、构图和参考图保真仍由 Codex 查看图片核验。清晰度分数不代表 OCR 正确。

```sh
python3 {skill_root}/scripts/image_gen.py approve --run-dir {run} --qa-note '已核对中文、布局、样张风格和参考图；尺寸处理符合批准策略。'
python3 {skill_root}/scripts/image_gen.py packet --run-dir {run}
```

approve 仅在尺寸、透明性、文件完整性和启发式门控通过时完成；packet 输出并保存 result.json，供主代理接收。正文为图像，不能声称原生可编辑。

## 样张登记

先展示样张，用户批准后：

```sh
python3 {skill_root}/scripts/image_gen.py sample --run-dir {sample_run} --deck {deck} --user-approved
```

登记会复制成 origin_image/slide_XX.png（既有文件不覆盖），生成 sample_receipt.json。将返回的方法契约写入 deck_spec.json 的 sample_generation_method，并使用其中 approved_sample_path 为全套样张风格引用。prepare_slide_prompts.py 验证登记、已完成队列与文件哈希，不允许绕过样张确认。

## 恢复与质量重试

```sh
python3 {skill_root}/scripts/image_gen.py status --run-dir {run}
python3 {skill_root}/scripts/image_gen.py retry --run-dir {run} --reason quality
```

quality 重试仅在任务 needs_review 且项目已批准 auto_quality_retry 时允许；总次数不能超过 max_attempts。claim 后由 Codex 再次调用工具，脚本不会生成。已完成结果不重发；图片已生成则先恢复保存。

结果不确定时只有明确接受重复生成风险后才能：

```sh
python3 {skill_root}/scripts/image_gen.py retry --run-dir {run} --reason uncertain --ack-duplicate-risk
```

本地状态轮询使用 codex-imagegen-batch/scripts/image_jobs.py poll --queue {run}/queue，一次最多55秒；它不查询服务端进度。单个运行目录只负责一页；不同页面队列可并行。

脚本 generate/generate-batch/edit 命令会明确拒绝，不会假装通过 shell 调用内置模型。缺少工具直接报告 blocker。

回归测试可以在独立临时目录使用 sample --test-fixture 和 prepare_slide_prompts.py --test-fixture。测试登记不标记 user_approved，不能用于授权正式课件。

恢复已有队列时先 status，再按状态行动：pending 才 claim；running 先核对调用结果，不能直接再生成；generated 先 finish；needs_review 先查看输出再 approve 或按授权质量重试；completed 直接 packet。prepare 对完全相同的任务/策略是幂等的，但不会把 active/完成项重置为 pending。
