"""Local structural checks only; not scientific acceptance."""
import json, subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
base='f0f40a8c9b647a755e362f120cc4f1d18ae755d7'
checks=[]
def git(repo,*args):
 return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
repo=root/'wodecangku'
for ref,sha in {'main':base,'origin/main':base,'origin/skills-validation-20261014':'8a32c6fd5047ce09e002a7e66dfb5fdd6edee765','origin/test/ild-e2e-20261026':'4ded82c3e25c47742ee7cf6491cb210819f80202'}.items():
 assert git(repo,'rev-parse',ref)==sha,ref
 checks.append('unchanged '+ref)
for name,branch,owned in [('wodecangku','manager','ILD_RESEARCH_MANAGER/'),('ild-literature','literature','literature/ild-five-trials-20261102/'),('ild-analysis','analysis','analysis/ild-five-trials-20261102/'),('ild-presentation','presentation','presentations/ild-five-trials-20261102/')]:
 r=root/name
 assert git(r,'branch','--show-current')=='codex/ild-'+branch
 git(r,'merge-base','--is-ancestor',base,'HEAD')
 changes=git(r,'diff','--name-status',base,'HEAD')
 for line in changes.splitlines():
  status,path=line.split('\t',1)
  assert status=='A' and path.startswith(owned),(name,line)
 git(r,'diff','--check')
 checks.append('branch/ownership/diff '+branch)
gate=json.loads((root/'ild-presentation/presentations/ild-five-trials-20261102/INPUT_GATE.json').read_text())
assert gate['status']=='WAITING_FOR_A_FREEZE'
assert gate['a_commit_sha'] is None and gate['c_accepted_commit_sha'] is None
checks.append('B waiting gate')
print(json.dumps({'status':'PASS_STRUCTURAL_ONLY','checks':checks,'scientific_acceptance':'PENDING'},ensure_ascii=False,indent=2))
