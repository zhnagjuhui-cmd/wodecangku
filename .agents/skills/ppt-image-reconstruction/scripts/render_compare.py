#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def load_image(path: Path):
    from PIL import Image

    with Image.open(path) as img:
        return img.convert("RGB").copy()


def fit_to_height(img, target_h: int):
    if img.height == target_h:
        return img
    scale = target_h / img.height
    target_w = max(1, int(round(img.width * scale)))
    return img.resize((target_w, target_h))


def side_by_side(left, right, gap: int = 24, pad: int = 24):
    from PIL import Image, ImageDraw

    left = fit_to_height(left, max(left.height, right.height))
    right = fit_to_height(right, max(left.height, right.height))
    height = max(left.height, right.height) + pad * 2
    width = left.width + right.width + gap + pad * 2
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(left, (pad, pad))
    canvas.paste(right, (pad + left.width + gap, pad))
    draw.rectangle((pad, pad, pad + left.width - 1, pad + left.height - 1), outline="black", width=2)
    draw.rectangle(
        (pad + left.width + gap, pad, pad + left.width + gap + right.width - 1, pad + right.height - 1),
        outline="black",
        width=2,
    )
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a side-by-side comparison of source and rebuilt slides.")
    parser.add_argument("source", help="Source image")
    parser.add_argument("rebuild", help="Rebuilt image")
    parser.add_argument("--out", required=True, help="Output comparison PNG")
    args = parser.parse_args()

    source = load_image(Path(args.source))
    rebuild = load_image(Path(args.rebuild))
    compare = side_by_side(source, rebuild)
    compare.save(args.out)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
