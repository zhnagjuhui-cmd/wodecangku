#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_image_meta(path: Path) -> dict:
    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover
        return {"path": str(path), "error": f"Pillow unavailable: {exc}"}

    with Image.open(path) as img:
        aspect = img.width / img.height if img.height else 0
        risks = []
        if img.width < 1200 or img.height < 700:
            risks.append("low_resolution")
        if aspect < 0.9 or aspect > 1.9:
            risks.append("unusual_aspect_ratio")
        return {
            "path": str(path),
            "kind": "image",
            "width": img.width,
            "height": img.height,
            "aspect_ratio": round(aspect, 3),
            "mode": img.mode,
            "format": img.format,
            "risks": risks,
        }


def load_pdf_meta(path: Path) -> dict:
    try:
        import fitz  # type: ignore
    except Exception as exc:  # pragma: no cover
        return {"path": str(path), "error": f"PyMuPDF unavailable: {exc}"}

    doc = fitz.open(path)
    pages = []
    for page in doc:
        rect = page.rect
        pages.append(
            {
                "width": round(rect.width, 2),
                "height": round(rect.height, 2),
                "orientation": "landscape" if rect.width >= rect.height else "portrait",
            }
        )
    return {
        "path": str(path),
        "kind": "pdf",
        "page_count": len(pages),
        "pages": pages,
    }


def build_checklist(meta: dict) -> dict:
    common = [
        "Identify the source type and the dominant page structure.",
        "Mark title, body, panels, tables, conclusions, references, and footers.",
        "Choose one slide per source page unless readability collapses.",
        "Prefer native text and native shapes before cropped images.",
        "Keep conclusions and references in separate layers.",
        "Reserve a safe bottom band for footers or citations.",
        "Treat any overflow text as a reflow problem first.",
    ]

    if meta.get("kind") == "image":
        specific = [
            "Inspect whether the image is a clean digital slide, GPT image, screenshot, or scan.",
            "Crop each panel independently if multiple panels are present.",
            "Rebuild tables natively when the grid is legible.",
            "Rebuild captions and callouts near the related panel.",
            "Run a text-bounds check after reconstruction.",
        ]
    elif meta.get("kind") == "pdf":
        specific = [
            "Inspect every page size and orientation before reconstructing.",
            "Decide whether the PDF should become one slide per page.",
            "Rasterize only the regions that cannot be rebuilt natively.",
            "Check page-by-page for footer collisions and citation overflow.",
        ]
    else:
        specific = ["Unknown source type: inspect manually before proceeding."]

    risks = meta.get("risks", [])
    risk_items = []
    if "low_resolution" in risks:
        risk_items.append("Source is low resolution; expect OCR and text reflow risk.")
    if "unusual_aspect_ratio" in risks:
        risk_items.append("Aspect ratio is unusual; check for cropped headers, footers, or split panels.")
    if not risk_items:
        risk_items.append("No obvious size-based risk flags from the source file.")

    return {
        "source": meta,
        "checklist": {
            "common": common,
            "specific": specific,
            "risk_notes": risk_items,
            "sample_first": [
                "Rebuild the first representative page first.",
                "Review fidelity and editability before continuing.",
                "Only scale to the rest of the deck after the sample is accepted.",
            ],
        },
    }


def to_markdown(result: dict) -> str:
    meta = result["source"]
    lines = []
    lines.append("# Reconstruction Checklist")
    lines.append("")
    lines.append(f"- Source: `{meta.get('path', '')}`")
    if meta.get("kind") == "image":
        lines.append(f"- Type: image")
        lines.append(f"- Size: {meta.get('width')} x {meta.get('height')}")
    elif meta.get("kind") == "pdf":
        lines.append(f"- Type: pdf")
        lines.append(f"- Pages: {meta.get('page_count')}")
    if meta.get("error"):
        lines.append(f"- Error: {meta['error']}")
    lines.append("")
    lines.append("## Common")
    for item in result["checklist"]["common"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Specific")
    for item in result["checklist"]["specific"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Risk Notes")
    for item in result["checklist"]["risk_notes"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Sample First")
    for item in result["checklist"]["sample_first"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a reconstruction checklist for a page image or PDF.")
    parser.add_argument("path", help="Input image or PDF")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}:
        meta = load_image_meta(path)
    elif suffix == ".pdf":
        meta = load_pdf_meta(path)
    else:
        meta = {"path": str(path), "error": f"Unsupported file type: {suffix}"}

    result = build_checklist(meta)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
