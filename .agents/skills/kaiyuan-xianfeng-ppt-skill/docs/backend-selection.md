# Backend Selection

Read this before confirming the image backend or generating the first sample slide.

This skill uses one generation path only:

1. local `gpt-image-2` skill, through `scripts/image_gen.py`

## Decision Rules

- Confirm whether the local `gpt-image-2` skill exists before generating the sample slide.
- Use `scripts/image_gen.py check` for the dependency check when needed.
- Do not silently switch to built-in image tools.
- Do not silently switch to OpenAI-compatible API fallback.
- If the local `gpt-image-2` skill is missing, stop and ask the user whether to continue without image generation.
- When the local skill exists, keep that backend fixed for the sample slide and the full deck.

## Missing-Skill Message

Use wording equivalent to this:

```text
我检查了当前 PPT 技能依赖的本地 `gpt-image-2` 生图技能，当前没有找到对应技能包，因此现在还不能继续执行生图。

无对应生图技能包，是否继续生成？

如果继续，我只能保留 PPT 项目结构、讲稿和装配流程，不能实际生成新的幻灯片图片。
```

## Confirmation Text

```text
我检查到当前环境已经安装本地 `gpt-image-2` 生图技能，因此这份 PPT 会固定使用本地 `gpt-image-2` 技能包作为出图后端；生成后还会经过一层本地清晰度门控，遇到文字疑似模糊的结果会自动重试。可以开始生成 1 页样张吗？
```
