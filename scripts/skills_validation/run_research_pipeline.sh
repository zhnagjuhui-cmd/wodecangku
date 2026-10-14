#!/usr/bin/env bash
# Requires allowed outbound access for the first stage, no browser or API key.
set -euo pipefail
task_root="$(cd "$(dirname "$0")/../.." && pwd)"
task_output="${1:?Provide a NEW absolute output directory}"
case "$task_output" in /*) ;; *) echo 'Output directory must be absolute' >&2; exit 2;; esac
if [ -e "$task_output" ]; then echo 'Output directory already exists; refusing overwrite' >&2; exit 2; fi
mkdir -p "$task_output"
task_python="$task_root/.venv-skills-validation/bin/python"
"$task_python" "$task_root/scripts/run_ild_skill.py" ild-literature-search -- --out "$task_output/literature"
"$task_python" "$task_root/scripts/run_ild_skill.py" ild-evidence-check -- --records "$task_output/literature/records.json" --out "$task_output/verification.json"
"$task_python" "$task_root/scripts/run_ild_skill.py" ild-medical-document -- --records "$task_output/literature/records.json" --verification "$task_output/verification.json" --out "$task_output/documents"
