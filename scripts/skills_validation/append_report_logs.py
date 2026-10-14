#!/usr/bin/env python3
"""Append the actual command index to a new report, refusing duplicate append."""
import json
from pathlib import Path
import shlex

root=Path(__file__).resolve().parents[2]
report=root/'SKILLS_VALIDATION_REPORT.md';source=report.read_text()
marker='<!-- generated-command-index -->'
if marker in source:raise SystemExit('Command index already appended; refusing duplicate')
logs=[]
for p in (root/'outputs/skills_validation_20261014/logs').glob('*.json'):
    logs.append((p,json.loads(p.read_text())))
logs.sort(key=lambda x:(x[1]['utc'],x[1]['name']))
lines=['',marker,'','| 测试 | 返回码 | 日志 |','| --- | --- | --- |']
for path,j in logs:lines.append(f"| {j['name']} | {j['returncode']} | [{path.name}]({path.relative_to(root)}) |")
for path,j in logs:
    lines.extend(['',f"### {j['name']}",'',f"UTC：{j['utc']}；返回码：{j['returncode']}；工作目录：`{j['cwd']}`。",'', '```bash',shlex.join(j['argv']),'```'])
    if j['stderr'].strip():
        lines.extend(['','stderr（完整错误/诊断）：','```text',j['stderr'].strip(),'```'])
    if j['returncode']!=0 and j['stdout'].strip():
        lines.extend(['','stdout（前 2500 字符，全文见对应 JSON 日志）：','```text',j['stdout'].strip()[:2500],'```'])
    elif j['stdout'].strip():
        s=j['stdout'].strip();lines.extend(['','stdout 摘要（全文见日志）：','```text',s[:260]+(' …' if len(s)>260 else ''),'```'])
report.write_text('\n'.join(line.rstrip() for line in (source+'\n'.join(lines)).splitlines())+'\n')
print('Appended',len(logs),'actual command records')
