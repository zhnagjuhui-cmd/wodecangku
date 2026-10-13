"""
GPT Image 2 image capability extension for the Kaiyuan Xianfeng API.

Usage:
    $env:LK888_API_KEY = "your-api-key"
    $env:LK888_BASE_URL = "https://provider.example.com"
    python gpt_image_2.py "An orange cat wearing glasses reads by a window"

The API key can also be passed to GPTImage2Client(api_key="...") by host code.
"""

from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


DEFAULT_BASE_URL = "https://api.lk888.ai"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_API_KEY = ""
DEFAULT_SIZE = "2048x2048"
DEFAULT_QUALITY = "high"
DEFAULT_ENV_API_KEYS = ("DEFAULT_API_KEY", "DEFAULT_LK888_API_KEY")
DEFAULT_ENV_BASE_URLS = ("DEFAULT_BASE_URL", "DEFAULT_GPT_IMAGE_2_BASE_URL")
DEFAULT_ENV_MODELS = ("DEFAULT_MODEL",)
DEFAULT_ENV_SIZES = ("DEFAULT_SIZE",)
DEFAULT_ENV_QUALITIES = ("DEFAULT_QUALITY",)

COMMON_SIZE_PRESETS: dict[str, str] = {
    "auto": "auto",
    "1024x1024": "1024x1024 - 1K square",
    "1536x1024": "1536x1024 - 1.5K landscape, 3:2",
    "1024x1536": "1024x1536 - 1.5K portrait, 2:3",
    "2048x2048": "2048x2048 - 2K square",
    "2880x2880": "2880x2880 - 3K square",
    "2560x1440": "2560x1440 - 2K landscape, 16:9",
    "1440x2560": "1440x2560 - 2K portrait, 9:16",
    "2160x3840": "2160x3840 - 4K portrait, 9:16",
    "3840x2160": "3840x2160 - 4K landscape, 16:9",
}

SIZE_ALIASES: dict[str, str] = {
    "1k": "1024x1024",
    "square": "2048x2048",
    "2k": "2048x2048",
    "3k": "2880x2880",
    "portrait": "1440x2560",
    "vertical": "1440x2560",
    "2k-portrait": "1440x2560",
    "2k-vertical": "1440x2560",
    "landscape": "2560x1440",
    "wide": "2560x1440",
    "2k-landscape": "2560x1440",
    "4k-portrait": "2160x3840",
    "4k-vertical": "2160x3840",
    "4k-landscape": "3840x2160",
    "4k-wide": "3840x2160",
}


class GPTImage2Error(RuntimeError):
    """Raised when the GPT Image 2 provider returns an error."""


def normalize_size(size: str) -> str:
    normalized = size.strip().lower()
    normalized = SIZE_ALIASES.get(normalized, normalized)

    if normalized in COMMON_SIZE_PRESETS:
        return normalized
    if re.fullmatch(r"\d{3,4}x\d{3,4}", normalized):
        return normalized

    choices = ", ".join(COMMON_SIZE_PRESETS)
    aliases = ", ".join(SIZE_ALIASES)
    raise ValueError(f"Unsupported size '{size}'. Common sizes: {choices}. Aliases: {aliases}.")


def format_size_presets() -> str:
    lines = ["Common GPT Image 2 sizes:"]
    lines.extend(f"  {value}" for value in COMMON_SIZE_PRESETS.values())
    lines.append("")
    lines.append("Aliases:")
    lines.extend(f"  {alias} -> {size}" for alias, size in SIZE_ALIASES.items())
    return "\n".join(lines)


def first_env_value(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


class GPTImage2Client:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.api_key = (
            api_key
            or first_env_value(*DEFAULT_ENV_API_KEYS, "LK888_API_KEY", "API_KEY")
            or DEFAULT_API_KEY
        )
        if not self.api_key:
            raise GPTImage2Error(
                "Missing API key. Set DEFAULT_API_KEY, LK888_API_KEY, API_KEY, or pass api_key to GPTImage2Client."
            )

        self.base_url = (
            base_url
            or first_env_value(*DEFAULT_ENV_BASE_URLS, "LK888_BASE_URL", "GPT_IMAGE_2_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        if not self.base_url:
            raise GPTImage2Error(
                "Missing base URL. Set DEFAULT_BASE_URL, LK888_BASE_URL, GPT_IMAGE_2_BASE_URL, or patch DEFAULT_BASE_URL."
            )

        self.timeout = timeout
        self.session = requests.Session()
        self.session.trust_env = False

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        prompt: str,
        *,
        images: list[str] | None = None,
        size: str | None = None,
        quality: str | None = None,
        poll_interval: int = 4,
        max_wait_seconds: int = 180,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create an image generation task and return the final provider response.

        The provider documentation describes an async task flow, but one sample
        response returns data[0].url directly. This method supports both shapes.
        """

        resolved_model = first_env_value(*DEFAULT_ENV_MODELS) or DEFAULT_MODEL
        resolved_size = size or first_env_value(*DEFAULT_ENV_SIZES) or DEFAULT_SIZE
        resolved_quality = quality or first_env_value(*DEFAULT_ENV_QUALITIES) or DEFAULT_QUALITY

        payload: dict[str, Any] = {
            "model": resolved_model,
            "prompt": prompt,
            "params": {
                "size": normalize_size(resolved_size),
                "quality": resolved_quality,
            },
        }

        if images:
            payload["params"]["images"] = images
        if extra_params:
            payload["params"].update(extra_params)

        response = self.session.post(
            f"{self.base_url}/v1/media/generate",
            headers=self.headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        created = response.json()

        direct_url = self._extract_direct_url(created)
        if direct_url:
            return {
                "state": "success",
                "is_final": True,
                "result_url": direct_url,
                "raw": created,
            }

        task_id = created.get("task_id") or created.get("id")
        if not task_id and isinstance(created.get("data"), dict):
            data = created["data"]
            task_id = data.get("task_id") or data.get("id")
        if not task_id:
            raise GPTImage2Error(f"Response did not include task_id or url: {created}")

        return self.wait_for_result(
            str(task_id),
            poll_interval=poll_interval,
            max_wait_seconds=max_wait_seconds,
        )

    def wait_for_result(
        self,
        task_id: str,
        *,
        poll_interval: int = 4,
        max_wait_seconds: int = 180,
    ) -> dict[str, Any]:
        deadline = time.monotonic() + max_wait_seconds

        while True:
            status = self.get_status(task_id)
            state = status.get("state")

            if status.get("is_final") is True:
                if state == "success":
                    return status
                if state == "failed":
                    error = status.get("error") or "Image generation failed."
                    raise GPTImage2Error(error)
                raise GPTImage2Error(f"Task ended with unknown state: {status}")

            if time.monotonic() >= deadline:
                raise TimeoutError(f"Timed out waiting for task {task_id}. Last status: {status}")

            time.sleep(poll_interval)

    def get_status(self, task_id: str) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/v1/media/status",
            headers=self.headers,
            params={"task_id": task_id},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def download_result(self, result_url: str, output_dir: str | Path = ".") -> Path:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        parsed = urlparse(result_url)
        name = Path(parsed.path).name or "gpt-image-2-result.png"
        output_path = output_dir / name

        response = self.session.get(result_url, timeout=self.timeout)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return output_path

    @staticmethod
    def _extract_direct_url(response_json: dict[str, Any]) -> str | None:
        data = response_json.get("data")
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict) and isinstance(first.get("url"), str):
                return first["url"]
        if isinstance(response_json.get("result_url"), str) and response_json["result_url"]:
            return response_json["result_url"]
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an image with GPT Image 2.")
    parser.add_argument("prompt", nargs="?", help="Image prompt")
    parser.add_argument("--task-id", help="Poll and download an existing generation task")
    parser.add_argument("--image", action="append", dest="images", help="Reference image URL")
    parser.add_argument(
        "--size",
        default=None,
        help=f"Image size or alias, default: DEFAULT_SIZE env or {DEFAULT_SIZE}. Use --list-sizes to view presets.",
    )
    parser.add_argument(
        "--quality",
        default=None,
        help=f"Image quality, default: DEFAULT_QUALITY env or {DEFAULT_QUALITY}",
    )
    parser.add_argument("--output-dir", default="outputs", help="Directory for downloaded result")
    parser.add_argument("--no-download", action="store_true", help="Print result URL only")
    parser.add_argument("--list-sizes", action="store_true", help="Print common size presets and exit")
    args = parser.parse_args()

    if args.list_sizes:
        print(format_size_presets())
        return

    client = GPTImage2Client()
    if args.task_id:
        result = client.wait_for_result(args.task_id)
    else:
        if not args.prompt:
            parser.error("prompt is required unless --task-id is provided")
        result = client.generate(
            args.prompt,
            images=args.images,
            size=args.size or first_env_value(*DEFAULT_ENV_SIZES) or DEFAULT_SIZE,
            quality=args.quality or first_env_value(*DEFAULT_ENV_QUALITIES) or DEFAULT_QUALITY,
        )

    result_url = result.get("result_url")
    if not result_url:
        raise GPTImage2Error(f"Generation succeeded but no result_url was returned: {result}")

    print(result_url)
    if not args.no_download:
        output_path = client.download_result(result_url, args.output_dir)
        print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
