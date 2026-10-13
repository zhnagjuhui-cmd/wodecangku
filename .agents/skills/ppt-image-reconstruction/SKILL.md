---
name: ppt-image-reconstruction
description: Rebuild slide-like images, screenshots, scanned pages, GPT-generated visuals, posters, paper figures, infographic pages, and complex single-slide compositions into editable PowerPoint slides. Use when the user wants an image reconstructed as PPT/PPTX with native text, native shapes, independently cropped panel images, editable tables, separated conclusion/reference layers, and a review-first workflow that rebuilds one page at a time and produces a sample slide before continuing.
---

# Ppt Image Reconstruction

## Overview

Rebuild a visual page into an editable PowerPoint slide rather than placing the full page as one background image. Prioritize editability, structural fidelity, and review checkpoints over speed.

Treat this skill as a strict reconstruction workflow for slide-like visuals. Use it for one-page figures, slide screenshots, GPT-generated layouts, scanned presentation pages, poster panels, summary pages, and complex visual compositions that must become editable PPT/PPTX.

## Non-Negotiable Rules

Follow these rules unless the user explicitly relaxes them:

- Rebuild the page as editable PPT, not as a full-page screenshot pasted onto a slide.
- Native-text all readable text. Use PowerPoint text boxes wherever the source text can be reasonably recovered.
- Native-shape all simple geometry. Rebuild boxes, callouts, arrows, dividers, chips, labels, and panel frames as PowerPoint shapes when practical.
- Crop images by panel. If the page contains multiple charts, photos, insets, or figure panels, crop and place them as separate image objects rather than one merged bitmap.
- Preserve table editability. Rebuild tables as actual PPT tables when feasible, including cell structure and in-cell line wrapping.
- Separate conclusions and references into distinct layers/groups so they can be edited or animated independently.
- Do not use a full-page background image as the main reconstruction strategy.
- Work one page at a time. Produce one sample page first, get feedback or perform self-review, then continue to the next page.

## When To Use This Skill

Use this skill when the request sounds like:

- "Please rebuild this image into editable PPT."
- "Turn this GPT-generated slide image into a PowerPoint."
- "Recreate this figure page as a PPTX with editable text."
- "Do not use a background image; make everything editable."
- "Split each panel and rebuild it slide-by-slide."
- "Keep conclusions and references separate."

Use it especially when the source is:

- A GPT-generated slide image
- A slide screenshot
- A scanned presentation page
- A scientific poster or figure summary page
- A dashboard-like one-pager
- A visual report page with multiple panels
- A dense page that mixes text, shapes, charts, tables, and citations

Do not use this skill for:

- Plain text extraction to Markdown
- Multi-page Word-style flowing documents
- Cases where a full-page bitmap is explicitly acceptable
- Fully automated reconstruction promises when the source is too degraded to support native rebuilding

## Workflow

For detailed step-by-step behavior, see [references/reconstruction-workflow.md](references/reconstruction-workflow.md).
For common failure handling, see [references/error-playbook.md](references/error-playbook.md).
For a page-level task checklist, use `scripts/generate_reconstruction_checklist.py`.

### 1. Triage the source page

Inspect the page before rebuilding:

- Identify whether it is a clean digital image, a GPT-generated image, a screenshot, or a scanned/photographed page.
- Note the dominant structure: title area, section blocks, panel grid, figures, tables, conclusions, references, footnotes.
- Determine whether the layout is better rebuilt as one slide or split across multiple slides. If the user asked for slide-faithful reconstruction, default to one source page -> one slide unless readability would collapse.
- Estimate risk areas: tiny text, low contrast, warped perspective, overlapping annotations, embedded chart labels, dense references, irregular tables.

If the page is low quality or ambiguous, state the main reconstruction risks before proceeding.

### 2. Plan the reconstruction layers

Before building, map the page into editable layers:

- Background surfaces
- Structural shapes
- Title and body text
- Images or chart panels
- Tables
- Conclusions or takeaways
- References, citations, or footnotes

Prefer a layered plan that keeps high-change content editable. If a region is too visually complex to rebuild natively at reasonable effort, isolate that region as a cropped image instead of flattening the whole slide.

### 3. Rebuild in this priority order

Use this order unless the page strongly suggests otherwise:

1. Slide size and page bounds
2. Background color blocks or containers
3. Panel frames and main layout guides
4. Title, subtitle, headers, and labels
5. Tables and structured blocks
6. Cropped panel images
7. Conclusions, callouts, and highlights
8. References and footnotes

This ordering helps preserve alignment and keeps text and tables native.

### 4. Apply reconstruction rules

#### Text

- Recreate readable text as native text boxes.
- Preserve paragraph grouping and approximate hierarchy.
- Do not rasterize text just to match the image more closely.
- If some tiny text is unreadable, note it explicitly and keep that sub-region isolated if necessary.

#### Shapes

- Rebuild simple geometric elements as native shapes.
- Use separate shapes for cards, panels, tags, dividers, arrows, and callouts.
- Do not merge unrelated shapes into a single decorative background object.

#### Images and panels

- Detect individual panels and crop them independently.
- Place each cropped panel as its own object so the user can replace, move, or annotate it later.
- When a figure contains several subpanels, preserve that separability.

#### Tables

- Rebuild tables as PowerPoint tables when cell structure is legible.
- Preserve row/column grouping and in-cell line wrapping.
- Do not fake a table with one image if the table is reasonably reconstructable.

#### Conclusions and references

- Put conclusions, summary boxes, or takeaways in separate editable groups.
- Put references, citations, and footnotes in a separate layer/group from the main conclusion content.
- Keep these groups easy to edit or animate independently.

### 5. Review-first execution

Always use a sample-first flow:

1. Rebuild the first page or first representative slide.
2. Review fidelity and editability.
3. Call out any compromises you made.
4. Continue only after that sample is accepted, or after you revise the sample yourself if the issues are obvious.

When the user provides multiple pages, do not silently process the whole set in one shot unless they explicitly waive the sample-first workflow.

## Decision Rules

Choose the lightest faithful reconstruction method that preserves editability.

- Use native text when the text is readable.
- Use native shapes when the geometry is simple or repeated.
- Use cropped images for complex charts, microscopy figures, photos, and visually dense scientific panels.
- Use native tables when the grid is clear enough to reconstruct.
- Use grouped layers for conclusions and references.

Avoid all-or-nothing behavior. A good reconstruction is often hybrid:

- native text + native shapes + cropped chart panels + native tables

That is preferred over one giant screenshot.

## Project-Derived Heuristics

From the HP reconstruction project, these patterns worked well:

- Keep one slide per source page and use sample-first iteration.
- Rebuild clear section pages as native text plus native shapes instead of flattening them.
- Treat HRCT, pathology, and figure panels as separate crops with captions rebuilt nearby.
- Keep summary, practice-implication, and conclusion slides highly structured and text-first.
- Use tight evidence grouping for drug-evidence slides: main claim, trial boundary, and citation block.

These page types were especially reliable:

- HRCT key-sign pages
- Misconception / differential diagnosis pages
- Practice takeaway pages
- Final summary slides

The following error patterns appeared repeatedly and should be avoided:

- Long text running past the right edge of the slide or out of its container.
- Footer lines or speaker/date text dropping below the reserved bottom band.
- Reusing a large display font size everywhere without a declared role.
- Mixing a paragraph into multiple sibling text boxes when one text frame would stay cleaner.
- Letting citations or footnotes occupy the same visual layer as the conclusion block.

When a page is dense, reflow the text before shrinking it. Prefer shorter sentences, narrower line blocks, or additional subgroups over oversized text.

## Required User-Facing Commitments

When using this skill, make these commitments explicit in the work:

- Rebuild one page at a time.
- Produce a sample page first.
- Favor editability over screenshot fidelity.
- Keep conclusions and references independently editable.
- Avoid full-page background placement as the default.
- Treat long copied text as a reflow problem, not a scaling problem.
- Keep recurring typography within declared role bands.

## What To Report

At the end of each page or sample, report:

- What was rebuilt as native text
- What was rebuilt as native shapes
- What was kept as cropped images
- Whether any table was rebuilt natively
- Any unreadable or uncertain regions
- Whether the page is ready for continuing to the next one
- Whether any text was reflowed to avoid bounds overflow
- Whether footer or citation bands needed extra space

## Example Trigger Requests

- "Please rebuild this GPT image into an editable PPT slide."
- "Do this page first, then wait for my confirmation."
- "Keep all text editable and split the chart panels."
- "Recreate the table with wrapped text in cells."
- "Do not use the full image as the slide background."
- "Keep the conclusions and references on separate layers."

## Examples

See `examples/input/sample-page.png` for a simple source page and `examples/output/sample-page.checklist.json` for its generated checklist.

## Resources (optional)

This first version does not require bundled resources yet. Add scripts or references later only when the same reconstruction steps become repetitive enough to justify deterministic helpers.
