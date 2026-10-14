#!/usr/bin/env python3
"""Meaningful negative checks: altered metadata/source must block intake."""
import copy
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
path=root/'.agents/skills/ild-evidence-check/scripts/verify_evidence.py'
spec=importlib.util.spec_from_file_location('evidence',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
out=root/'outputs/skills_validation_20261014'
source=out/'literature_final/records.json';records=json.loads(source.read_text())
assert module.verify(source)['status']=='PASS'
cases=[]
with tempfile.TemporaryDirectory(prefix='ild-negative-check-') as tmp:
    tmp=Path(tmp);shutil.copytree(source.parent/'raw',tmp/'raw')
    bad=copy.deepcopy(records);bad[0]['doi']='10.0000/invalid-test-doi';p=tmp/'records.json';p.write_text(json.dumps(bad))
    checked=module.verify(p);assert checked['status']=='FAIL' and not checked['results'][0]['checks']['pubmed_doi'];cases.append('wrong DOI rejected')
    p.write_text(source.read_text());raw=tmp/records[0]['pubmed_trace']['path'];raw.write_bytes(raw.read_bytes()+b'\n')
    checked=module.verify(p);assert checked['status']=='FAIL' and not checked['results'][0]['checks']['pubmed_trace_sha256'];cases.append('modified source rejected')
    p.write_text(json.dumps(bad));doc_out=tmp/'blocked-document'
    command=[sys.executable,str(root/'.agents/skills/ild-medical-document/scripts/generate_document.py'),'--records',str(p),'--verification',str(out/'verification_final.json'),'--out',str(doc_out)]
    process=subprocess.run(command,capture_output=True,text=True)
    assert process.returncode!=0 and not doc_out.exists();cases.append('changed records block document creation')
    assert 'BLOCKED' in process.stderr
result=dict(status='PASS',cases=cases)
with args.out.open('x') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
