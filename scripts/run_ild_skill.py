#!/usr/bin/env python3
"""Project-local path discovery and invocation, independent of caller cwd.

This launcher does not add tools to the platform's current session catalogue.
Only the three bounded ILD CLI skills have uniform entry points here.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
entries={'ild-literature-search':'search_trials.py','ild-evidence-check':'verify_evidence.py','ild-medical-document':'generate_document.py'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--list',action='store_true');p.add_argument('skill',nargs='?',choices=entries);p.add_argument('arguments',nargs=argparse.REMAINDER);a=p.parse_args()
    if a.list:
        for manifest in sorted((root/'.agents/skills').glob('*/SKILL.md')):
            s=manifest.read_text();name=re.search(r'^name:\s*(\S+)',s,re.M)
            if not name or name.group(1)!=manifest.parent.name:raise SystemExit(f'Invalid skill manifest: {manifest}')
            print(name.group(1),str(manifest),'CLI' if name.group(1) in entries else 'workflow/component tests; read SKILL.md')
        return 0
    if not a.skill:p.error('Choose a skill or --list')
    manifest=root/'.agents/skills'/a.skill/'SKILL.md';text=manifest.read_text()
    assert re.search(r'^name:\s*'+re.escape(a.skill)+r'\s*$',text,re.M)
    print(f'Loaded repository skill: {manifest}',file=sys.stderr)
    args=a.arguments[1:] if a.arguments[:1]==['--'] else a.arguments
    return subprocess.call([sys.executable,str(manifest.parent/'scripts'/entries[a.skill]),*args],cwd=root)

if __name__=='__main__':raise SystemExit(main())
