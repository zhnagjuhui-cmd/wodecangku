# 任务清单与命令

以下命令从技能目录执行，其他位置使用助手绝对路径。`--queue` 是运行目录，不是 JSON 文件；原图与状态不写入技能安装目录。

## 创建

```sh
python3 scripts/image_jobs.py init --queue /absolute/project/image-run --prompt '清晨山间湖泊，写实摄影，无文字' --size landscape
python3 scripts/image_jobs.py init --queue /absolute/project/batch-run --jobs jobs.jsonl
```

JSONL 每行一个任务，参考图相对路径相对于 JSONL 所在目录解析，队列保存绝对路径：

```jsonl
{"id":"lake","operation":"generate","prompt":"清晨湖泊，写实摄影，无文字","size":"landscape"}
{"id":"watercolor","operation":"style-transfer","prompt":"改为清透水彩画","size":"2560x1440","references":[{"path":"source.png","role":"target"}],"preserve":["小屋位置","山体轮廓","湖岸构图"]}
{"id":"background","operation":"edit","prompt":"仅把背景改为纯白","size":"square","references":[{"path":"product.png","role":"target"}],"preserve":["产品形状","颜色","文字"]}
```

operation: generate/edit/style-transfer。references 每项为 path 或 conversation 二选一，加 role: target/style/reference。例如 `{"conversation":"本轮上传的第1张图","role":"target"}`。对话参考图不得超出宿主工具数量限制。

可选 preserve、avoid 为字符串数组；transparent_background 为布尔。编辑含透明区域的本地 target，未指定透明选项时自动保留透明要求；对话参考由 Codex 查看后记录。size 可 auto、正整数 WIDTHxHEIGHT 或别名，不照搬 API 尺寸限制作为内置工具的能力承诺。

别名：square/2k=2048x2048，wide/landscape=2560x1440，portrait/vertical=1440x2560，4k-wide=3840x2160，4k-portrait=2160x3840。`sizes` 可查看。它们是请求和验证目标，内置工具可能返回其他尺寸。

## Codex 执行循环

```sh
python3 scripts/image_jobs.py claim --queue /absolute/project/image-run
```

返回完整任务 JSON，有 active 任务时拒绝领取下一项。Codex 阅读并调用内置图像工具；脚本不会生图。

确认对应本地结果后立即记录并保存：

```sh
python3 scripts/image_jobs.py record --queue /absolute/project/image-run --id image-001 --image /absolute/generated/lake.png
python3 scripts/image_jobs.py finish --queue /absolute/project/image-run --id image-001
python3 scripts/image_jobs.py approve --queue /absolute/project/image-run --id image-001
```

record 保存 source_image 和历史，进入 generated；finish 保留 originals/ 原图及 outputs/ 交付图，进入 needs_review。approve 需尺寸、透明性校验通过、文件哈希未变，且 Codex 已完成视觉核验。命令不能检查语义。

用户接受实际尺寸而无须后处理：

```sh
python3 scripts/image_jobs.py approve --queue /absolute/project/image-run --id image-001 --accept-actual-size
```

用户明确选择精确尺寸后处理后：

```sh
python3 scripts/image_jobs.py finish --queue /absolute/project/image-run --id image-001 --fit contain
```

已有输出会生成 -v2 等新版本，不覆盖。contain 保留全图并留边；cover 居中裁切；stretch 拉伸。均可能改变像素，只在明确授权时使用。报告 original_size、actual_size、requested_size、fit、upscaled。

## 进度与恢复

```sh
python3 scripts/image_jobs.py status --queue /absolute/project/image-run
python3 scripts/image_jobs.py poll --queue /absolute/project/image-run --timeout 30 --interval 2
python3 scripts/image_jobs.py fail --queue /absolute/project/image-run --id image-001 --reason '调用结果不确定，需确认后重试'
python3 scripts/image_jobs.py retry --queue /absolute/project/image-run --id image-001 --ack-duplicate-risk
python3 scripts/image_jobs.py cancel --queue /absolute/project/image-run --id image-001 --reason '用户取消'
```

status 显示状态计数与每项状态，poll 状态变化时输出，到全部 terminal 或超时退出。terminal=completed/failed/cancelled。退出码 0=成功，2=错误或轮询发现失败/取消，3=轮询超时；needs_review 不算完成。

重试保留历史；每次 claim 递增 attempts。先恢复文件保存，再考虑重新生成。running 状态可能已生图，重发可能重复消耗额度。cancel 仅改变本地状态，不能取消宿主工具。分享技能包时不附私密队列或参考图。
