#!/usr/bin/env python3
# coding: utf-8
"""Local PPT dependencies only. No credentials, provider configuration or network probes."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('doctor','bootstrap'))
    p.add_argument('--home',type=Path,default=Path(os.environ.get('KAIYUAN_CODEX_PPT_HOME',str(Path.home()/'.kaiyuan-codex-ppt'))))
    a=p.parse_args()
    home=a.home.expanduser().resolve()
    python=home/'.venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    if a.command=='bootstrap':
        home.mkdir(parents=True,exist_ok=True)
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(home/'.venv')
        req=Path(__file__).resolve().parent.parent/'requirements.txt'
        subprocess.run([str(python),'-m','pip','install','-r',str(req)],check=True)
    modules=('pptx','PIL','filelock')
    code="import importlib.util,json; print(json.dumps({m:importlib.util.find_spec(m) is not None for m in ['pptx','PIL','filelock']}))"
    probe=subprocess.run([str(python) if python.exists() else sys.executable,'-c',code],capture_output=True,text=True)
    print(json.dumps({'runtime_home':str(home),'python':str(python) if python.exists() else sys.executable,
                      'packages':json.loads(probe.stdout),'generation':'Codex built-in image tool, checked by agent'},indent=2))
    return 0 if probe.returncode==0 and all(json.loads(probe.stdout).values()) else 1


if __name__=='__main__':
    raise SystemExit(main())
