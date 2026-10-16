# User-Supplied Assets

Read this before using paper figures, experiment result charts, screenshots, logos, or other assets that must appear in the deck.

When the user provides paper figures, experiment result charts, screenshots, logos, or other assets that must appear in the deck, treat them as source assets, not as loose visual inspiration.

Recommended project-local asset location:

```text
{base_dir}/{deck_name}/assets/
├── figures/
│   ├── result_01.png
│   └── result_02.png
└── logos/
    └── lab_logo.png
```

Do not place source assets in `origin_image/`; that directory is only for final `slide_XX.png` images.

For slides that must include a user-supplied figure:

- Record the exact asset path or attachment name in `outline.md` for that slide, preferably as a Markdown image reference inside that slide's `Required images` list, then ask the user to confirm the mapping before generation.
- Stay on the fixed codex-imagegen-batch/built-in image path; no upload to obtain public URLs is required or allowed by this workflow.
- Each worker independently inspects every local source/style image with view_image. Label roles in the prompt and task: style, reference or target. If all files are local and the current tool accepts referenced_image_paths, provide absolute paths. If any reference exists only in conversation, follow the current tool's image-context mechanism and limit; do not silently omit an input or mix mutually exclusive input mechanisms.
- Local references are inputs to a generative tool, not a guarantee of pixel-identical reproduction. Check source figures against the originals, including numbers and labels; report or repair changes instead of claiming exact preservation from file attachment alone.
- Ask the model to preserve the supplied figure's data, labels, axes, colors, and visual content, and only compose the surrounding slide layout, title, captions, callouts, and background.
- Do not ask the model to "redraw", "recreate", "imagine", or "generate a similar chart" for result figures unless the user explicitly wants a stylized redraw.
- After generation, inspect the output and ask the user to pay special attention to whether required figures were used correctly.

Example prompt fragment for a result-figure slide:

```json
{
  "source_assets": [
    {
      "path": "{base_dir}/{deck_name}/assets/figures/result_01.png",
      "usage": "embed as the main evidence figure",
      "fidelity": "preserve the figure content; do not redraw or change data, axes, labels, colors, curves, bars, or legends"
    }
  ],
  "visual_elements": {
    "main_visual": "place the supplied result_01.png as a large figure panel, with a short caption and two callouts around it"
  },
  "constraints": [
    "Use the provided figure as an input image, not as a loose style reference.",
    "Do not synthesize a replacement chart.",
    "Keep all numerical values and labels in the supplied figure unchanged."
  ]
}
```
