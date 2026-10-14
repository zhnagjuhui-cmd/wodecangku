#!/usr/bin/env bash
# Legal fallback for the two pure-Python packages actually repaired here.
# Uses inherited proxy/TLS. Does not alter policies, secrets, global packages,
# or the original skills. Existing document/PDF libraries must already exist.
set -euo pipefail
task_root="$(cd "$(dirname "$0")/../.." && pwd)"
task_sources="$(mktemp -d /tmp/ild-validation-deps.XXXXXX)"
trap 'rm -rf "$task_sources"' EXIT
if [ ! -x "$task_root/.venv-skills-validation/bin/python" ]; then
  python3 -m venv --system-site-packages "$task_root/.venv-skills-validation"
fi
git clone --quiet --depth 1 --branch v2.32.5 https://github.com/psf/requests.git "$task_sources/requests"
git clone --quiet --depth 1 --branch 1.26.20 https://github.com/urllib3/urllib3.git "$task_sources/urllib3"
test "$(git -C "$task_sources/requests" rev-parse HEAD)" = b25c87d7cb8d6a18a37fa12442b5f883f9e41741
test "$(git -C "$task_sources/urllib3" rev-parse HEAD)" = 6f2ad7ca0cdde53751bab29cbc10bcc965bb4387
"$task_root/.venv-skills-validation/bin/python" -m pip install --disable-pip-version-check --no-cache-dir --no-deps --no-build-isolation "$task_sources/urllib3" "$task_sources/requests"
"$task_root/.venv-skills-validation/bin/python" -c 'import requests, urllib3, httpx, docx, pptx, fitz; print("PASS: required runtime imports")'
