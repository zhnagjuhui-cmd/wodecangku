#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def find_gutters(mask: list[float], min_run: int = 18, threshold: float = 0.985) -> list[tuple[int, int]]:
    runs = []
    start = None
    for idx, value in enumerate(mask):
        if value >= threshold and start is None:
            start = idx
        elif value < threshold and start is not None:
            if idx - start >= min_run:
                runs.append((start, idx))
            start = None
    if start is not None and len(mask) - start >= min_run:
        runs.append((start, len(mask)))
    return runs
def main() -> int:
    parser = argparse.ArgumentParser(description="Split a page image into panel crops using whitespace gutters.")
    parser.add_argument("image", help="Input raster image")
    parser.add_argument("--out", required=True, help="Output directory for crops")
    parser.add_argument("--min-run", type=int, default=18, help="Minimum whitespace run length")
    parser.add_argument("--threshold", type=float, default=0.985, help="Whitespace threshold")
    args = parser.parse_args()

    from PIL import Image

    path = Path(args.image)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    with Image.open(path) as img:
        rgb = img.convert("RGB")
        width, height = rgb.size
        pixels = rgb.load()

        horizontal = []
        for y in range(height):
            white = 0
            for x in range(width):
                r, g, b = pixels[x, y]
                if (r + g + b) / 3 >= 250:
                    white += 1
            horizontal.append(white / width if width else 0.0)

        vertical = []
        for x in range(width):
            white = 0
            for y in range(height):
                r, g, b = pixels[x, y]
                if (r + g + b) / 3 >= 250:
                    white += 1
            vertical.append(white / height if height else 0.0)

        h_runs = find_gutters(horizontal, min_run=args.min_run, threshold=args.threshold)
        v_runs = find_gutters(vertical, min_run=args.min_run, threshold=args.threshold)

        # Build a simple grid from gutter boundaries.
        y_bounds = [0]
        for start, end in h_runs:
            mid = (start + end) // 2
            if 0 < mid < rgb.height:
                y_bounds.append(mid)
        y_bounds.append(rgb.height)
        x_bounds = [0]
        for start, end in v_runs:
            mid = (start + end) // 2
            if 0 < mid < rgb.width:
                x_bounds.append(mid)
        x_bounds.append(rgb.width)

        x_bounds = sorted(set(x_bounds))
        y_bounds = sorted(set(y_bounds))

        crops = []
        index = 1
        for yi in range(len(y_bounds) - 1):
            for xi in range(len(x_bounds) - 1):
                x0, x1 = x_bounds[xi], x_bounds[xi + 1]
                y0, y1 = y_bounds[yi], y_bounds[yi + 1]
                if x1 - x0 < 80 or y1 - y0 < 80:
                    continue
                crop = rgb.crop((x0, y0, x1, y1))
                sample = crop.resize((1, 1)).getpixel((0, 0))
                if sum(sample) / 3 > 248:
                    continue
                out = outdir / f"panel-{index:02d}.png"
                crop.save(out)
                crops.append({"path": str(out), "box": [x0, y0, x1, y1]})
                index += 1

    print({"source": str(path), "crops": crops})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
