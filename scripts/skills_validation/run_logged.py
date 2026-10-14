#!/usr/bin/env python3
"""Run a non-secret validation command, preserving exact argv and output."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('--timeout', type=int, default=45)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    root = Path(__file__).resolve().parents[2]
    out = root / 'outputs/skills_validation_20261014/logs'
    out.mkdir(parents=True, exist_ok=True)
    record = dict(name=args.name, argv=command, cwd=str(root), utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        p = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=args.timeout)
        record.update(returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)
    except subprocess.TimeoutExpired as e:
        record.update(returncode=124, stdout=(e.stdout or b'').decode() if isinstance(e.stdout, bytes) else e.stdout or '', stderr='TIMEOUT')
    path = out / (args.name + '.json')
    with path.open('x', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return record['returncode']

if __name__ == '__main__':
    sys.exit(main())
