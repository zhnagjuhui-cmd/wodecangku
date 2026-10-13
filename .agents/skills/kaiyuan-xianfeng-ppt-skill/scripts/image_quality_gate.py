#!/usr/bin/env python3
"""Heuristic readability gate for PPT slide images."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from PIL import Image, ImageFilter, ImageStat


def _region_metrics(image: Image.Image) -> Dict[str, float]:
    gray = image.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    gray_stat = ImageStat.Stat(gray)
    edge_stat = ImageStat.Stat(edges)
    return {
        "contrast_stddev": float(gray_stat.stddev[0]),
        "edge_stddev": float(edge_stat.stddev[0]),
        "edge_mean": float(edge_stat.mean[0]),
    }


def _regions(image: Image.Image) -> List[tuple[str, Image.Image]]:
    width, height = image.size
    top = image.crop((0, 0, width, max(1, int(height * 0.34))))
    middle = image.crop((0, int(height * 0.25), width, int(height * 0.75)))
    bottom = image.crop((0, int(height * 0.70), width, height))
    return [
        ("full", image),
        ("top", top),
        ("middle", middle),
        ("bottom", bottom),
    ]


def assess_image_readability(
    image_path: str | Path,
    *,
    min_edge_stddev: float = 18.0,
    min_contrast_stddev: float = 28.0,
) -> Dict[str, Any]:
    path = Path(image_path)
    with Image.open(path) as image:
        metrics = []
        for label, region in _regions(image):
            region_score = _region_metrics(region)
            region_score["region"] = label
            metrics.append(region_score)

    best_edge = max(item["edge_stddev"] for item in metrics)
    best_contrast = max(item["contrast_stddev"] for item in metrics)
    passed = best_edge >= min_edge_stddev and best_contrast >= min_contrast_stddev

    if passed:
        reason = (
            f"passed readability gate: best_edge_stddev={best_edge:.2f}, "
            f"best_contrast_stddev={best_contrast:.2f}"
        )
    else:
        reason = (
            f"failed readability gate: best_edge_stddev={best_edge:.2f} "
            f"(threshold {min_edge_stddev:.2f}), best_contrast_stddev={best_contrast:.2f} "
            f"(threshold {min_contrast_stddev:.2f})"
        )

    return {
        "path": str(path),
        "passed": passed,
        "reason": reason,
        "best_edge_stddev": best_edge,
        "best_contrast_stddev": best_contrast,
        "thresholds": {
            "min_edge_stddev": min_edge_stddev,
            "min_contrast_stddev": min_contrast_stddev,
        },
        "regions": metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    parser.add_argument("--min-edge-stddev", type=float, default=18.0)
    parser.add_argument("--min-contrast-stddev", type=float, default=28.0)
    args = parser.parse_args()

    result = assess_image_readability(
        args.image,
        min_edge_stddev=args.min_edge_stddev,
        min_contrast_stddev=args.min_contrast_stddev,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
