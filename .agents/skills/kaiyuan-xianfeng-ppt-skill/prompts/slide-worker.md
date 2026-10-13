# Slide Worker Prompt

Use this template when dispatching a slide subagent after the sample slide is approved and full-deck generation is authorized.

```text
Generate slide <N> for this PPT deck.

Deck dir: <absolute deck dir>
Slide job file: <absolute deck dir>/prompts/slide_<NN>.json
Output target owned by parent: <absolute deck dir>/origin_image/slide_<NN>.png
Selected image backend: local gpt-image-2 skill via scripts/image_gen.py
Sample generation method copied from the approved sample:
- backend_used: <exact backend label recorded by parent>
- tool_name: <scripts/image_gen.py>
- mode: <generate>
- model/config: <size, retry budget, readability thresholds>
- prompt_source: <approved sample prompt source>
- input_context_preparation: <how style/context images were prepared>
- approved_sample_path: <absolute path to approved origin_image/slide_XX.png>
- handoff_rule: use this same backend/tool/mode; return a blocker if unavailable

Read the JSON job file, then follow its `prompt` field exactly.
Use the selected backend only:
- run `scripts/image_gen.py generate`
- do not switch to built-in image tools
- do not switch to OpenAI-compatible API fallback

If the local `gpt-image-2` skill is missing, stop and return:
blocker=missing local gpt-image-2 skill

Forbidden for final slide image creation:
- local drawing or rendering scripts
- Pillow-generated slides
- SVG, HTML/CSS, or canvas screenshots
- python-pptx/PptxGenJS/native PPT layout screenshots
- manually composited text, card, chart, or image overlays

Before returning, visually check:
- Chinese text is readable and not garbled
- the image is not obviously blurry
- style matches the approved sample slide
- no overlapping or truncated important content

Return only:
backend_used=local gpt-image-2 skill via scripts/image_gen.py
selected_source=/absolute/path/to/generated/image.png
qa_note=<one sentence>
```
