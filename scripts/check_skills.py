#!/usr/bin/env python3
"""Validate repository skill discovery without network or third-party packages."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
skills = root / ".agents" / "skills"
expected = {
    "ppt-master", "medical-evidence-ppt", "ppt-image-reconstruction",
    "guizang-ppt-skill", "dashi-ppt", "gpt-image-2", "kaiyuan-xianfeng-ppt-skill",
}
project_skills = {"ild-literature-search", "ild-evidence-check", "ild-medical-document"}
found = set()
for directory in sorted(skills.iterdir()):
    if not directory.is_dir():
        continue
    manifest = directory / "SKILL.md"
    assert manifest.is_file(), f"Missing {manifest}"
    text = manifest.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"Missing frontmatter: {manifest}"
    header = text.split("---", 2)[1]
    name = re.search(r"^name:\s*([^\n]+)", header, re.M)
    assert name and name.group(1).strip().strip("\"'") == directory.name, manifest
    assert re.search(r"^description:\s*\S", header, re.M), manifest
    assert directory.name not in found, f"Duplicate {directory.name}"
    found.add(directory.name)
    print(f"OK {directory.name}")
assert expected <= found, f"Missing original skills: {expected - found}"
assert found <= expected | project_skills, f"Unexpected skill set: {found - expected - project_skills}"
for name in found & project_skills:
    assert (skills / name / "scripts").is_dir(), f"Missing scripts for {name}"
assert not (root / "skills").exists(), "Duplicate legacy skill directory"
assert not (root / "skill-packages").exists(), "Duplicate packaged skills"
assert (skills / "gpt-image-2/scripts/gpt_image_2.py").is_file()
assert (skills / "dashi-ppt/project/package.json").is_file()
assert (skills / "ppt-master/LICENSE").is_file()
print(f"PASS: {len(found)} unique skills, seven original skills preserved and required runtime files")
