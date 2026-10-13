# Local GPT-Image-2 Wrapper

Use this reference after the backend has been confirmed as the local `gpt-image-2` skill.

Let `{skill_root}` mean the directory containing `SKILL.md`.

## Dependency Check

Check whether the local skill exists:

```bash
python {skill_root}/scripts/image_gen.py check
```

If this check fails, stop and ask the user whether to continue without image generation.

## Generate One Slide

Basic command:

```bash
python {skill_root}/scripts/image_gen.py generate \
  --prompt-file {prompt_file} \
  --size landscape \
  --out {base_dir}/{deck_name}/origin_image/slide_01.png
```

## Quality Gate

The wrapper adds a readability retry gate after each generation:

- it measures edge sharpness and grayscale contrast in several image regions
- it retries automatically when the result looks too blurry for slide text
- it fails explicitly after the retry budget is exhausted

Useful knobs:

```bash
python {skill_root}/scripts/image_gen.py generate \
  --prompt-file {prompt_file} \
  --size landscape \
  --max-attempts 4 \
  --min-edge-stddev 18 \
  --min-contrast-stddev 28 \
  --out {base_dir}/{deck_name}/origin_image/slide_01.png
```

## Batch Generation

```bash
python {skill_root}/scripts/image_gen.py generate-batch \
  --input {jobs_jsonl} \
  --out-dir {base_dir}/{deck_name}/generated_batch
```

Each JSONL line may be either:

- a plain prompt string
- or a JSON object with at least `prompt`

Optional per-job overrides:

- `out`
- `size`
- `max_attempts`
- `min_edge_stddev`
- `min_contrast_stddev`
- `images`

## Input Images

The local `gpt-image-2` skill only accepts public image URLs.

- `http://` and `https://` images are forwarded
- local filesystem image paths are skipped with a warning

Do not treat this wrapper as a strict local-asset preservation path.

## Editing

`edit` is intentionally unsupported in this skill package. If a slide needs localized repair, regenerate it with a tighter prompt or have the user approve a workflow change.
