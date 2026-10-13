#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


def parse_float(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    m = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(m.group(0)) if m else default


def text_content(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def approx_width(text: str, font_size: float) -> float:
    return len(text) * font_size * 0.58


def check_svg(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    view_box = root.attrib.get("viewBox")
    width = parse_float(root.attrib.get("width"), 0)
    height = parse_float(root.attrib.get("height"), 0)
    if view_box:
        _, _, vb_w, vb_h = [parse_float(part) for part in view_box.split()]
        canvas_w, canvas_h = vb_w, vb_h
    else:
        canvas_w, canvas_h = width, height

    results = []
    namespace_match = re.match(r"\{.*\}", root.tag)
    ns = namespace_match.group(0) if namespace_match else ""

    for node in root.iter(f"{ns}text"):
        text = text_content(node)
        if not text:
            continue
        x = parse_float(node.attrib.get("x"), 0.0)
        y = parse_float(node.attrib.get("y"), 0.0)
        font_size = parse_float(node.attrib.get("font-size"), 36.0)
        est_w = approx_width(text, font_size)
        est_h = font_size * 1.2
        bbox = {
            "x0": round(x, 1),
            "y0": round(y - est_h, 1),
            "x1": round(x + est_w, 1),
            "y1": round(y, 1),
        }
        overflow = bbox["x1"] > canvas_w or bbox["y0"] < 0 or bbox["y1"] > canvas_h
        results.append(
            {
                "text": text,
                "font_size": font_size,
                "bbox": bbox,
                "overflow": overflow,
            }
        )

    font_sizes: dict[float, int] = {}
    for item in results:
        font_sizes[item["font_size"]] = font_sizes.get(item["font_size"], 0) + 1

    repeated_sizes = {str(size): count for size, count in font_sizes.items() if count > 2}
    overflows = [item for item in results if item["overflow"]]
    return {
        "path": str(path),
        "canvas": {"width": canvas_w, "height": canvas_h},
        "text_count": len(results),
        "overflow_count": len(overflows),
        "repeated_font_sizes": repeated_sizes,
        "overflow_items": overflows[:20],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SVG text bounds and repeated font sizes.")
    parser.add_argument("path", help="SVG file")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = check_svg(Path(args.path))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
