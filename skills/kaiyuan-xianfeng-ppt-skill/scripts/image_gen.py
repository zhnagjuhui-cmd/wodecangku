#!/usr/bin/env python3
"""Local PPT image wrapper that delegates to the installed gpt-image-2 skill."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, Iterable, List, Optional

from image_quality_gate import assess_image_readability


DEFAULT_SIZE = "landscape"
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_MIN_EDGE_STDDEV = 18.0
DEFAULT_MIN_CONTRAST_STDDEV = 28.0
DEFAULT_OUTPUT_PATH = "output/imagegen/output.png"
DEFAULT_OUTPUT_FORMAT = "png"
DEFAULT_GPT_IMAGE_2_SKILL_DIR = Path.home() / ".codex" / "skills" / "gpt-image-2"


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def _skill_paths() -> tuple[Path, Path]:
    skill_dir = Path(os.getenv("KAIYUAN_GPT_IMAGE_2_SKILL_DIR", DEFAULT_GPT_IMAGE_2_SKILL_DIR)).expanduser()
    script_path = skill_dir / "scripts" / "gpt_image_2.py"
    return skill_dir, script_path


def _ensure_local_gpt_image_2() -> Path:
    skill_dir, script_path = _skill_paths()
    if script_path.exists():
        return script_path
    _die(
        "无对应生图技能包：未找到本地 gpt-image-2 技能。\n"
        f"期望目录：{skill_dir}\n"
        f"期望脚本：{script_path}\n"
        "是否继续生成？如果继续，将只能保留 PPT 结构与装配流程，不能执行生图。"
    )
    return script_path


def _read_prompt(prompt: Optional[str], prompt_file: Optional[str]) -> str:
    if prompt and prompt_file:
        _die("Use --prompt or --prompt-file, not both.")
    if prompt_file:
        if prompt_file == "-":
            return sys.stdin.read().strip()
        path = Path(prompt_file)
        if not path.exists():
            _die(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8").strip()
    if prompt:
        return prompt.strip()
    _die("Missing prompt. Use --prompt or --prompt-file.")
    return ""


def _normalize_output_format(output_format: Optional[str]) -> str:
    if not output_format:
        return DEFAULT_OUTPUT_FORMAT
    fmt = output_format.lower()
    if fmt not in {"png", "jpg", "jpeg", "webp"}:
        _die("output-format must be png, jpg, jpeg, or webp.")
    return "jpeg" if fmt == "jpg" else fmt


def _build_output_paths(out: str, output_format: str, count: int, out_dir: Optional[str]) -> List[Path]:
    ext = "." + output_format
    if out_dir:
        base_dir = Path(out_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
        return [base_dir / f"image_{i}{ext}" for i in range(1, count + 1)]

    output_path = Path(out)
    if output_path.suffix == "":
        output_path = output_path.with_suffix(ext)
    if count == 1:
        return [output_path]
    return [
        output_path.with_name(f"{output_path.stem}-{i}{output_path.suffix}")
        for i in range(1, count + 1)
    ]


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:60] if value else "job"


def _read_jobs_jsonl(path: str) -> List[Dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        _die(f"Input file not found: {file_path}")
    jobs: List[Dict[str, Any]] = []
    for line_no, raw in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        item: Any = json.loads(line) if line.startswith("{") else {"prompt": line}
        if not isinstance(item, dict) or not str(item.get("prompt", "")).strip():
            _die(f"Invalid job on line {line_no}: missing prompt")
        jobs.append(item)
    if not jobs:
        _die("No jobs found in input file.")
    return jobs


def _job_output_path(out_dir: Path, output_format: str, idx: int, prompt: str, explicit_out: Optional[str]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = "." + output_format
    if explicit_out:
        path = Path(explicit_out)
        if path.suffix == "":
            path = path.with_suffix(ext)
        return out_dir / path.name
    return out_dir / f"{idx:03d}-{_slugify(prompt[:80])}{ext}"


def _parse_saved_path(stdout: str, temp_dir: Path) -> Path:
    match = re.search(r"Saved to:\s*(.+)", stdout)
    if match:
        candidate = Path(match.group(1).strip())
        if candidate.exists():
            return candidate
    generated = sorted(temp_dir.glob("*"), key=lambda item: item.stat().st_mtime, reverse=True)
    for candidate in generated:
        if candidate.is_file():
            return candidate
    _die("Local gpt-image-2 skill finished without writing an output file.")
    return temp_dir


def _filter_images(images: Iterable[str]) -> List[str]:
    accepted: List[str] = []
    skipped: List[str] = []
    for image in images:
        if re.match(r"^https?://", image, re.IGNORECASE):
            accepted.append(image)
        else:
            skipped.append(image)
    if skipped:
        _warn(
            "The local gpt-image-2 skill only accepts public image URLs. "
            f"Skipped non-URL image inputs: {', '.join(skipped)}"
        )
    return accepted


def _run_generation_once(
    *,
    script_path: Path,
    prompt: str,
    size: str,
    output_dir: Path,
    images: List[str],
) -> Path:
    # The local gpt-image-2 skill may depend on packages that are available in the
    # host Python environment but not in the PPT runtime venv, so call it with the
    # system Python instead of the current interpreter.
    command = ["python3", str(script_path), prompt, "--size", size, "--output-dir", str(output_dir)]
    for image in images:
        command.extend(["--image", image])
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        _die(
            "Local gpt-image-2 generation failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}"
        )
    return _parse_saved_path(result.stdout, output_dir)


def _generate_with_retries(
    *,
    prompt: str,
    size: str,
    images: List[str],
    max_attempts: int,
    min_edge_stddev: float,
    min_contrast_stddev: float,
) -> Path:
    script_path = _ensure_local_gpt_image_2()
    last_failure: Optional[str] = None
    for attempt in range(1, max_attempts + 1):
        with tempfile.TemporaryDirectory(prefix="kaiyuan-ppt-image-") as temp_dir_raw:
            temp_dir = Path(temp_dir_raw)
            generated = _run_generation_once(
                script_path=script_path,
                prompt=prompt,
                size=size,
                output_dir=temp_dir,
                images=images,
            )
            gate = assess_image_readability(
                generated,
                min_edge_stddev=min_edge_stddev,
                min_contrast_stddev=min_contrast_stddev,
            )
            if gate["passed"]:
                final_copy = temp_dir / generated.name
                persisted = generated if generated == final_copy else final_copy
                if generated != persisted:
                    shutil.copy2(generated, persisted)
                kept = Path(tempfile.mkdtemp(prefix="kaiyuan-ppt-approved-")) / generated.name
                shutil.copy2(generated, kept)
                return kept
            last_failure = gate["reason"]
            _warn(f"Attempt {attempt}/{max_attempts} failed readability gate: {gate['reason']}")
    _die(
        "Image generation completed but the readability gate rejected all attempts.\n"
        f"Last failure: {last_failure or 'unknown'}"
    )
    return Path()


def _copy_result(source: Path, target: Path, force: bool) -> None:
    if target.exists() and not force:
        _die(f"Output already exists: {target} (use --force to overwrite)")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"Wrote {target}")


def _check(_: argparse.Namespace) -> None:
    skill_dir, script_path = _skill_paths()
    available = script_path.exists()
    payload = {
        "available": available,
        "skill_dir": str(skill_dir),
        "script_path": str(script_path),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if not available:
        raise SystemExit(1)


def _generate(args: argparse.Namespace) -> None:
    if args.n != 1:
        _die("This local PPT wrapper only supports --n 1.")
    prompt = _read_prompt(args.prompt, args.prompt_file)
    output_format = _normalize_output_format(args.output_format)
    target = _build_output_paths(args.out, output_format, 1, args.out_dir)[0]
    source = _generate_with_retries(
        prompt=prompt,
        size=args.size,
        images=_filter_images(args.image or []),
        max_attempts=args.max_attempts,
        min_edge_stddev=args.min_edge_stddev,
        min_contrast_stddev=args.min_contrast_stddev,
    )
    _copy_result(source, target, args.force)


def _generate_batch(args: argparse.Namespace) -> None:
    jobs = _read_jobs_jsonl(args.input)
    output_format = _normalize_output_format(args.output_format)
    out_dir = Path(args.out_dir)
    for idx, job in enumerate(jobs, start=1):
        prompt = str(job["prompt"]).strip()
        target = _job_output_path(out_dir, output_format, idx, prompt, job.get("out"))
        source = _generate_with_retries(
            prompt=prompt,
            size=str(job.get("size") or args.size),
            images=_filter_images(job.get("images") or job.get("input_images") or []),
            max_attempts=int(job.get("max_attempts") or args.max_attempts),
            min_edge_stddev=float(job.get("min_edge_stddev") or args.min_edge_stddev),
            min_contrast_stddev=float(job.get("min_contrast_stddev") or args.min_contrast_stddev),
        )
        _copy_result(source, target, args.force)


def _edit(_: argparse.Namespace) -> None:
    _die(
        "The local gpt-image-2 PPT wrapper currently supports generate/generate-batch only. "
        "Edit is not implemented in this skill package."
    )


def _add_shared_generate_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--size", default=DEFAULT_SIZE)
    parser.add_argument("--out", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--out-dir")
    parser.add_argument("--output-format", default=DEFAULT_OUTPUT_FORMAT)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--image", action="append", default=[])
    parser.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS)
    parser.add_argument("--min-edge-stddev", type=float, default=DEFAULT_MIN_EDGE_STDDEV)
    parser.add_argument("--min-contrast-stddev", type=float, default=DEFAULT_MIN_CONTRAST_STDDEV)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate PPT slide images through the local gpt-image-2 skill with a readability retry gate."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Check whether the local gpt-image-2 skill exists")
    check_parser.set_defaults(func=_check)

    generate_parser = subparsers.add_parser("generate", help="Generate one image")
    _add_shared_generate_args(generate_parser)
    generate_parser.set_defaults(func=_generate)

    batch_parser = subparsers.add_parser("generate-batch", help="Generate multiple images from JSONL input")
    _add_shared_generate_args(batch_parser)
    batch_parser.add_argument("--input", required=True)
    batch_parser.set_defaults(func=_generate_batch)

    edit_parser = subparsers.add_parser("edit", help="Edit an image")
    edit_parser.set_defaults(func=_edit)

    args = parser.parse_args()
    if getattr(args, "max_attempts", DEFAULT_MAX_ATTEMPTS) < 1:
        _die("--max-attempts must be >= 1")
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
