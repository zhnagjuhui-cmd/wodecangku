---
name: kaiyuan-xianfeng-ppt-skill
description: Generate visually unified image-based PPT/PPTX decks while keeping the codex-ppt project structure, prompt/job pipeline, notes, and assembly flow. Use when Codex needs a PPT skill package that depends on a locally installed `gpt-image-2` skill for image generation instead of built-in image tools or OpenAI API fallback. If the local `gpt-image-2` skill is missing, stop and ask the user whether to continue without image generation.
---

# Kaiyuan Xianfeng PPT Skill

## Overview

Use this skill to create image-based PPT decks with the same project structure as `codex-ppt`, but route slide generation through the local `gpt-image-2` skill at `~/.codex/skills/gpt-image-2`.

This skill keeps the PPT workflow intact:

- `deck_spec.json`
- `prompts/slide_XX.json`
- `slide_jobs.json` and `slide_run_state.json`
- `origin_image/slide_XX.png`
- `speech.md`
- final `.pptx` assembly

Only the image-generation path changes.

## Workflow

1. Read `docs/workflow-gates-and-progress.md` before advancing phases.
2. Confirm the presentation language before generating any sample slide or full-deck image. Do not assume the language when the user has not stated it clearly.
3. Read `docs/backend-selection.md` before confirming the backend.
4. Use `scripts/prepare_slide_prompts.py` to create per-slide jobs.
5. Use `scripts/image_gen.py` as the local generation wrapper.
6. Use the bundled `record_slide_dispatch.py`, `record_slide_result.py`, and `record_slide_blocker.py` scripts to keep slide state accurate.
7. Use `scripts/assemble_ppt.py` for final PPT assembly.

## Language Confirmation

Before image generation starts, explicitly confirm the PPT language with the user:

- confirm whether the deck should be Chinese, English, or bilingual
- keep the confirmed language consistent across `deck_spec.json`, slide prompts, `speech.md`, and QA
- if the user has not specified the language, ask before generating the sample slide

Use wording equivalent to this:

```text
开始生成之前，我先确认一下这份 PPT 的语言：要生成中文、英文，还是中英双语版本？
```

## Local Image Backend

This skill depends on the local `gpt-image-2` skill:

- Expected skill dir: `~/.codex/skills/gpt-image-2`
- Expected script: `~/.codex/skills/gpt-image-2/scripts/gpt_image_2.py`

Use `scripts/image_gen.py check` before backend confirmation when there is any doubt.

If the local `gpt-image-2` skill is missing:

- stop before generation
- tell the user that there is no matching local image skill
- ask whether to continue without image generation

Do not silently switch to built-in image tools or OpenAI-compatible API fallback.

## Quality Gate

`scripts/image_gen.py` adds a post-generation quality gate:

- inspect generated images with a local readability heuristic
- retry automatically when the image appears too blurry for slide text
- fail explicitly after the retry budget is exhausted instead of silently accepting a poor image

Treat this as a guardrail, not proof of perfect OCR quality. When a slide is especially text-heavy, still visually inspect the selected result before recording it.

## References

- Read `docs/backend-selection.md` for the backend rule and missing-skill behavior.
- Read `docs/cli-api-fallback.md` for wrapper commands and quality-gate options.
- Read `docs/slide-generation-and-subagents.md` before full-deck generation.
- Read `docs/project-assembly-and-reporting.md` before notes and assembly.
- Use `prompts/slide-worker.md` for worker handoff.


## Repository and cloud execution

In this repository, the wrapper first discovers the sibling `../gpt-image-2` skill. `KAIYUAN_GPT_IMAGE_2_SKILL_DIR` overrides discovery; the original user-local path remains a fallback. Run `scripts/image_gen.py check` before image generation. API credentials, requests/Pillow dependencies and provider network access must be supplied by the execution environment; never change image backends silently.
