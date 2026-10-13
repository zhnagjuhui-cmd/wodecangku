# Error Playbook

## Common Failures

### Text overflow

- Reflow text instead of shrinking it.
- Split into shorter lines or a smaller text group.
- Expand the band if the footer or citation area is colliding.

### Repeated oversized typography

- Keep recurring typography in declared role bands.
- Do not reuse a large display size everywhere unless it is intentional.

### Footer collision

- Reserve a bottom band early.
- Keep speaker lines, dates, and page labels out of the main content band.

### Citation collision

- Put citations in a separate layer.
- Do not let citations share the same visual block as the conclusion.

### Paragraph fragmentation

- Prefer one text frame with tspans over many sibling boxes for one paragraph.
- Keep semantically independent text blocks separate.

### Over-flattened panels

- Split charts, figures, and photos into independent cropped panels.
- Avoid one bitmap covering multiple logical regions.

## Best-Practice Fix Order

1. Reflow text.
2. Reallocate vertical space.
3. Split or merge text frames.
4. Crop panels.
5. Separate citation and conclusion bands.
6. Only then consider size reduction.
