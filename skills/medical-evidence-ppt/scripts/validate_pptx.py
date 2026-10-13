#!/usr/bin/env python3
"""Validate slide count, speaker notes, ZIP integrity, and basic editability."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def numbered_parts(names: list[str], prefix: str, stem: str) -> dict[int, str]:
    pattern = re.compile(rf"^{re.escape(prefix)}/{re.escape(stem)}(\d+)\.xml$")
    parts: dict[int, str] = {}
    for name in names:
        match = pattern.match(name)
        if match:
            parts[int(match.group(1))] = name
    return parts


def text_length(xml_bytes: bytes) -> int:
    root = ET.fromstring(xml_bytes)
    return len("".join(node.text or "" for node in root.findall(".//a:t", NS)).strip())


def slide_metrics(xml_bytes: bytes) -> dict[str, int | bool]:
    root = ET.fromstring(xml_bytes)
    text_chars = text_length(xml_bytes)
    shape_count = len(root.findall(".//p:sp", NS))
    picture_count = len(root.findall(".//p:pic", NS))
    graphic_frame_count = len(root.findall(".//p:graphicFrame", NS))
    native_text_shapes = sum(
        1 for shape in root.findall(".//p:sp", NS) if shape.findall(".//a:t", NS)
    )
    image_only = picture_count > 0 and native_text_shapes == 0 and graphic_frame_count == 0
    return {
        "text_chars": text_chars,
        "shape_count": shape_count,
        "native_text_shapes": native_text_shapes,
        "picture_count": picture_count,
        "graphic_frame_count": graphic_frame_count,
        "image_only": image_only,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path, help="PPTX file to validate")
    parser.add_argument("--expected-slides", type=int, help="Required slide count")
    parser.add_argument("--require-notes", action="store_true", help="Require notes on every slide")
    parser.add_argument(
        "--require-editable",
        action="store_true",
        help="Fail when a slide appears to be only a full-page image",
    )
    parser.add_argument(
        "--min-note-chars",
        type=int,
        default=20,
        help="Minimum extracted characters for each speaker note (default: 20)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    if not args.pptx.is_file():
        print(json.dumps({"ok": False, "errors": [f"File not found: {args.pptx}"]}, ensure_ascii=False, indent=2))
        return 2

    try:
        with zipfile.ZipFile(args.pptx) as archive:
            corrupt = archive.testzip()
            if corrupt:
                errors.append(f"Corrupt ZIP member: {corrupt}")

            names = archive.namelist()
            slides = numbered_parts(names, "ppt/slides", "slide")
            notes = numbered_parts(names, "ppt/notesSlides", "notesSlide")

            slide_details: dict[str, dict[str, int | bool]] = {}
            image_only_slides: list[int] = []
            for index, name in sorted(slides.items()):
                metrics = slide_metrics(archive.read(name))
                slide_details[str(index)] = metrics
                if metrics["image_only"]:
                    image_only_slides.append(index)

            missing_or_short_notes: list[int] = []
            for index in sorted(slides):
                note_name = notes.get(index)
                if not note_name or text_length(archive.read(note_name)) < args.min_note_chars:
                    missing_or_short_notes.append(index)

    except (zipfile.BadZipFile, ET.ParseError, OSError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2

    slide_count = len(slides)
    if args.expected_slides is not None and slide_count != args.expected_slides:
        errors.append(f"Expected {args.expected_slides} slides, found {slide_count}")
    if args.require_notes and missing_or_short_notes:
        errors.append(f"Missing or short speaker notes on slides: {missing_or_short_notes}")
    elif missing_or_short_notes:
        warnings.append(f"Missing or short speaker notes on slides: {missing_or_short_notes}")
    if args.require_editable and image_only_slides:
        errors.append(f"Slides appear image-only and are not natively editable: {image_only_slides}")
    elif image_only_slides:
        warnings.append(f"Slides appear image-only: {image_only_slides}")

    report = {
        "ok": not errors,
        "file": str(args.pptx.resolve()),
        "slide_count": slide_count,
        "notes_part_count": len(notes),
        "notes_missing_or_short": missing_or_short_notes,
        "image_only_slides": image_only_slides,
        "errors": errors,
        "warnings": warnings,
        "slide_details": slide_details,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
