---
name: gpt-image-2
description: Generate, poll, and download images with the GPT Image 2 provider through the bundled Python client. Use when Codex needs to create an image from a text prompt, generate an image from one or more reference image URLs, poll an existing GPT Image 2 task, save generated image files locally, or inspect supported GPT Image 2 size presets and aliases.
---

# GPT Image 2

## Overview

Use this skill to call the GPT Image 2 image API and save the resulting image locally. The reusable client lives in `scripts/gpt_image_2.py` and supports direct result URLs as well as asynchronous task polling.

## Quick Start

Before generating, confirm that an API key is available in `LK888_API_KEY` or `API_KEY`, or set `DEFAULT_API_KEY` inside `scripts/gpt_image_2.py`. If the provider endpoint is not hardcoded in the script, set `LK888_BASE_URL` or `GPT_IMAGE_2_BASE_URL`, or patch `DEFAULT_BASE_URL`.

```powershell
$env:LK888_API_KEY = "your-api-key"
$env:LK888_BASE_URL = "https://provider.example.com"
python scripts/gpt_image_2.py "A precise image prompt" --size 2048x2048 --output-dir outputs
```

## Generate Images

Run the script from the skill directory or pass the absolute script path. Write prompts with the final visual target, subject, composition, style, lighting, and required constraints.

```powershell
python scripts/gpt_image_2.py "A product photo of a matte black desk lamp on a walnut table, soft window light" --size landscape
```

Use `--image` repeatedly when the task should use reference image URLs:

```powershell
python scripts/gpt_image_2.py "Restyle this room as a clean Scandinavian interior" --image "https://example.com/reference.jpg" --size wide
```

Use `--no-download` when only the result URL is needed.

## Poll Existing Tasks

If a generation task already exists, poll it and download the final image:

```powershell
python scripts/gpt_image_2.py --task-id "task_123" --output-dir outputs
```

## Size Selection

Prefer aliases for ordinary requests:

- `square` or `2k` for 2048x2048
- `wide` or `landscape` for 2560x1440
- `portrait` or `vertical` for 1440x2560
- `4k-wide` for 3840x2160
- `4k-portrait` for 2160x3840

Run this command to print the complete current list:

```powershell
python scripts/gpt_image_2.py --list-sizes
```

## Troubleshooting

- If `requests` is missing, install it in the active Python environment.
- If the script reports a missing API key, set `LK888_API_KEY` or `API_KEY`, or put the key in `DEFAULT_API_KEY` inside `scripts/gpt_image_2.py`.
- If the script reports a missing base URL, set `LK888_BASE_URL` or `GPT_IMAGE_2_BASE_URL`, or patch `DEFAULT_BASE_URL` for the provider.
- If generation times out, rerun with `--task-id` when the provider returned a task ID, or increase `max_wait_seconds` from host code that imports `GPTImage2Client`.
