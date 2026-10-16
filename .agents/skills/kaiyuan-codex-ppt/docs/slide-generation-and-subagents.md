# 逐页生成、子代理及状态回传

保留原有一页一个子代理的生产方式。大纲、风格、后端和一页样张批准后，才准备全套正式任务。父代理负责全套上下文、任务、origin_image、QA、讲稿和装配；worker 只负责其分配的提示词任务及独立生图队列。

## 正式任务

```sh
python3 {skill_root}/scripts/prepare_slide_prompts.py --spec {deck}/deck_spec.json --out-dir {deck}
python3 {skill_root}/scripts/slide_job_status.py {deck} --json
```

prepare 保留原 deck_context、local_context、图片映射和完整视觉提示词；增加 image_policy、operation 和 image_run。sample_generation_method 必须来自已登记样张。全局样张只作 style 输入；每页所需源图片明确为 reference 或 target。worker 不知道父对话、前后页或论文背景，必要内容全部写入 job。

保持同一视觉身份，但按页面语义变化布局：封面、章节、问题背景、流程、对比、数据证据、架构、总结。保留原 references 风格库和 layout.intent，不把所有页面做成同一个三卡布局。

prepare 不允许重置已派发状态；恢复时直接使用原任务。若修改提示词/策略，建立新版本任务或项目，不通过 --force 清空运行历史。

## 派发

可用时必须用子代理，一页一个完整 job，并按实际可用槽位分批派发。队列默认最大6并发，宿主可能更低。使用 prompts/slide-worker.md 模板。成功 spawn 后立即记录真实 ID：

```sh
python3 {skill_root}/scripts/record_slide_dispatch.py {deck} --slide slide_02 --agent-id {actual_agent_id} --prompt-file prompts/slide_02.json
```

每页自己的 image_runs/slide_XX 内只有一项任务，满足 codex-imagegen-batch 的单队列单 active 限制。worker 必须检查自己具有内置图像工具，读取依赖技能，查看参考图后执行。父代理看过图片不能代替 worker 查看。不可用时返回 blocker，不能另开 CLI、生图接口或静默改为串行。

## 回传与主代理接收

worker 完成 prepare/claim → 内置生成 → record/finish → 视觉 QA → approve，返回 image_run、result.json、selected_source 和 QA。一页的完整记录保留在该队列，不写 origin_image 或 PPT 总状态。

父代理查看选定图片后接收：

```sh
python3 {skill_root}/scripts/record_slide_result.py {deck} --slide slide_02 --agent-id {actual_agent_id} --backend-used 'codex-imagegen-batch / built-in image tool' --image-run {deck}/image_runs/slide_02 --selected-source {approved_output_path} --qa-note '文字、参考图、布局及样张风格通过检查。'
```

接收验证：同一 agent、任务文件未改变、对应页面独立队列已 completed、来源路径与哈希匹配、固定内置后端。原图与后处理字段分开记录。主代理将文件归档为 origin_image/slide_XX.png；非 PNG 输入只转封装，不改变内容；不覆盖已有最终页。

状态映射：pending/running/generated/needs_review 均不能在 PPT 中标 recorded；只有 queue completed 且父代理完成接收才 recorded。批准样张为 accepted。失败或取消用 blocker 记录，避免组装缺页课件：

```sh
python3 {skill_root}/scripts/record_slide_blocker.py {deck} --slide slide_02 --agent-id {actual_agent_id} --reason '当前worker没有内置图像工具'
```

修复/恢复保留历史，先恢复已有生成图片，结果不确定不自动重发。已记录最终页若需要修改，要保留旧版本、创建新任务并明确批准替换；本技能不默默覆盖。

最终目录仅收 slide_01.png、slide_02.png 等正式页面；草稿和弃选图片保留在 image_runs 或 drafts。全部 recorded/accepted 后，逐页检查并组装。

## 阻塞恢复

原 worker 恢复后，明确重新开放已有派发：

```sh
python3 {skill_root}/scripts/resume_slide.py {deck} --slide slide_02 --agent-id {original_agent_id} --reason '依赖已恢复，继续保存已有结果'
```

需换 worker 时用 --reassign，随后重新 spawn 并记录 dispatch。两种方式都保留 recovery_history 和原生图队列；重新派发不等于重新生成。新 worker 先按 native-image-workflow.md 的状态表恢复，running 状态尤其不能直接重发。
