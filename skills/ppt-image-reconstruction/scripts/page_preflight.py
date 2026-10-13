#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def classify_page(width: int, height: int) -> dict:
    aspect = width / height if height else 0
    orientation = "landscape" if aspect >= 1 else "portrait"
    risks = []
    if width < 1200 or height < 700:
        risks.append("low_resolution")
    if aspect < 0.9 or aspect > 1.9:
        risks.append("unusual_aspect_ratio")
    if width > 2400 or height > 2400:
        risks.append("very_large_image")
    return {
        "width": width,
        "height": height,
        "aspect_ratio": round(aspect, 3),
        "orientation": orientation,
        "risks": risks,
    }


def inspect_image(path: Path) -> dict:
    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover
        return {"path": str(path), "error": f"Pillow unavailable: {exc}"}

    with Image.open(path) as img:
        info = classify_page(img.width, img.height)
        info.update({"path": str(path), "mode": img.mode, "format": img.format})
        return info


def inspect_pdf(path: Path) -> dict:
    try:
        import fitz  # type: ignore
    except Exception as exc:  # pragma: no cover
        return {"path": str(path), "error": f"PyMuPDF unavailable: {exc}"}

    doc = fitz.open(path)
    pages = []
    for index, page in enumerate(doc):
        rect = page.rect
        pages.append(
            {
                "page": index + 1,
                "width": round(rect.width, 2),
                "height": round(rect.height, 2),
                "orientation": "landscape" if rect.width >= rect.height else "portrait",
            }
        )
    return {"path": str(path), "pages": pages, "page_count": len(pages)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a page image or PDF before reconstruction.")
    parser.add_argument("path", help="Input image or PDF")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}:
        result = inspect_image(path)
    elif suffix == ".pdf":
        result = inspect_pdf(path)
    else:
        result = {"path": str(path), "error": f"Unsupported file type: {suffix}"}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
