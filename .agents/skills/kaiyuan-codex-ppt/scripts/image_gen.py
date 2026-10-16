#!/usr/bin/env python3
# coding: utf-8
"""Bridge PPT slide jobs to codex-imagegen-batch. No network or generation calls."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from image_quality_gate import assess_image_readability

BACKEND = 'codex-imagegen-batch / built-in image tool'
TOOL = 'image_gen.imagegen'
DEFAULT_POLICY = {'target_size':'2560x1440','fit':'verify','approved':False,
                  'accept_actual_size':False,'auto_quality_retry':False,'max_attempts':3,
                  'min_edge_stddev':18.0,'min_contrast_stddev':28.0}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path,value):
    path = Path(path)
    temp = path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    os.replace(temp,path)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def copy_png_once(source,target):
    """Atomic non-overwriting copy; identical prior copy is a recoverable no-op."""
    from PIL import Image
    source,target=Path(source),Path(target)
    with Image.open(source) as im:
        im.load()
        if target.exists():
            with Image.open(target) as previous:
                if previous.format!='PNG' or previous.size!=im.size or previous.convert('RGBA').tobytes()!=im.convert('RGBA').tobytes():
                    raise ValueError('existing final image differs; refusing to overwrite')
            return
        target.parent.mkdir(parents=True,exist_ok=True)
        fd,tmp=tempfile.mkstemp(prefix='.image-',suffix='.png',dir=target.parent)
        os.close(fd)
        try:
            if im.format=='PNG':
                shutil.copy2(source,tmp)
            else:
                im.save(tmp,format='PNG')
            os.link(tmp,target)
        finally:
            Path(tmp).unlink(missing_ok=True)


def skill_dir(override=None):
    if override or os.environ.get('KAIYUAN_CODEX_IMAGEGEN_SKILL_DIR'):
        candidates = [Path(override or os.environ['KAIYUAN_CODEX_IMAGEGEN_SKILL_DIR']).expanduser()]
    else:
        candidates = [Path(__file__).resolve().parents[2]/'codex-imagegen-batch',
                      Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills/codex-imagegen-batch']
    for p in candidates:
        if (p/'SKILL.md').is_file() and (p/'scripts/image_jobs.py').is_file():
            return p.resolve()
    raise ValueError('codex-imagegen-batch is missing; no alternate backend will be used')


def native(run,command,*args):
    bridge = read(run/'bridge.json')
    executable = Path(bridge['image_skill'])/'scripts/image_jobs.py'
    if not executable.is_file():
        raise ValueError('image skill moved; restore dependency before resuming')
    proc = subprocess.run([sys.executable,str(executable),command,'--queue',str(run/'queue'),*map(str,args)],
                          capture_output=True,text=True)
    if proc.returncode:
        raise ValueError(proc.stderr.strip() or proc.stdout.strip() or 'queue command failed')
    return json.loads(proc.stdout)


def job_state(run):
    data = read(run/'queue/queue.json')
    if data.get('backend')!='codex-built-in' or len(data.get('jobs',[]))!=1:
        raise ValueError('PPT requires one built-in image job per page queue')
    return data['jobs'][0]


def policy(raw):
    result = {**DEFAULT_POLICY,**raw}
    if set(result)-set(DEFAULT_POLICY):
        raise ValueError('unknown image policy field')
    for key in ('approved','accept_actual_size','auto_quality_retry'):
        if type(result[key]) is not bool:
            raise ValueError(key+' must be boolean')
    if result['fit'] not in {'verify','contain','cover','stretch'}:
        raise ValueError('invalid fit policy')
    if (result['fit']!='verify' or result['accept_actual_size'] or result['auto_quality_retry']) and not result['approved']:
        raise ValueError('post-processing, accepting actual size and automatic quality retry require approved policy')
    if type(result['max_attempts']) is not int or not 1<=result['max_attempts']<=10:
        raise ValueError('max_attempts must be 1..10')
    for key in ('min_edge_stddev','min_contrast_stddev'):
        if not isinstance(result[key],(int,float)) or result[key]<0:
            raise ValueError('readability thresholds must be nonnegative')
    return result


def prepare(job_path,run,image_skill):
    job_path = job_path.resolve()
    j = read(job_path)
    number = int(j['slide'])
    if number<1:
        raise ValueError('slide number must be positive')
    jid = 'slide_%02d'%number
    pol = policy(j.get('image_policy',{}))
    references = []
    for image in j.get('input_images',[]):
        role = image.get('input_role')
        if role is None:
            description = str(image.get('role','')).lower()
            role = 'style' if 'style' in description else 'target' if 'target' in description else 'reference'
        if role not in {'target','style','reference'}:
            raise ValueError('invalid input_role')
        if 'conversation' in image:
            references.append({'conversation':image['conversation'],'role':role})
        else:
            value = image.get('path') or image.get('attachment')
            if not isinstance(value,str) or not value.strip():
                raise ValueError('reference needs local path or conversation description')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://',value):
                raise ValueError('reference URL is not accepted; supply a local image file')
            path = Path(value).expanduser()
            if not path.is_absolute():
                path = job_path.parent/path
            path = path.resolve()
            if not path.is_file():
                raise ValueError('missing local reference: '+str(path))
            references.append({'path':str(path),'role':role})
    raw = {'id':jid,'prompt':j['prompt'],'size':pol['target_size'],
           'operation':j.get('operation','generate'),'references':references,
           'preserve':j.get('preserve',[]),'avoid':j.get('avoid',[])}
    if 'transparent_background' in j:
        raw['transparent_background'] = j['transparent_background']
    signature = hashlib.sha256(json.dumps({'job':raw,'policy':pol},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    if (run/'bridge.json').exists():
        existing = read(run/'bridge.json')
        if existing['signature']!=signature:
            raise ValueError('job/policy changed; use a new versioned run directory, never overwrite an existing run')
        return {'run_dir':str(run),'resumed':True,'job':job_state(run)}
    run.mkdir(parents=True,exist_ok=False)
    (run/'input.jsonl').write_text(json.dumps(raw,ensure_ascii=False)+'\n',encoding='utf-8')
    bridge = {'version':1,'slide_id':jid,'job_file':str(job_path),'job_sha256':sha(job_path),
              'signature':signature,'image_skill':str(image_skill),'backend':BACKEND,
              'tool_name':TOOL,'policy':pol,'created_at':now()}
    write(run/'bridge.json',bridge)
    proc = subprocess.run([sys.executable,str(image_skill/'scripts/image_jobs.py'),'init',
                           '--queue',str(run/'queue'),'--jobs',str(run/'input.jsonl')],capture_output=True,text=True)
    if proc.returncode:
        raise ValueError('queue initialization failed: '+proc.stderr.strip())
    return {'run_dir':str(run),'job':job_state(run)}


def quality(run):
    j = job_state(run)
    if not j.get('output'):
        raise ValueError('finish the generated image before checking readability')
    pol = read(run/'bridge.json')['policy']
    gate = assess_image_readability(j['output'],min_edge_stddev=pol['min_edge_stddev'],
                                    min_contrast_stddev=pol['min_contrast_stddev'])
    write(run/'quality.json',gate)
    return gate


def packet(run):
    b,j = read(run/'bridge.json'),job_state(run)
    if j['status']!='completed':
        raise ValueError('image job is not completed; current status='+j['status'])
    if sha(j['output'])!=j['validation']['sha256']:
        raise ValueError('output changed since approval')
    if not b.get('generation') or not b.get('review'):
        raise ValueError('generation provenance or visual review is missing')
    original_sha = sha(j['original'])
    if original_sha!=b['generation']['source_sha256']:
        raise ValueError('generated original changed')
    return {'backend_used':BACKEND,'backend_family':'built-in-image-tool','tool_name':TOOL,
            'image_skill':'codex-imagegen-batch','image_run':str(run),'slide_id':j['id'],
            'job_file':b['job_file'],'job_sha256':b['job_sha256'],
            'selected_source':j['output'],'selected_source_sha256':sha(j['output']),
            'generated_original':j['original'],'generated_original_sha256':original_sha,
            'validation':j['validation'],'policy':b['policy'],'attempts':j['attempts'],
            'qa_note':b['review']['qa_note'],'quality':read(run/'quality.json')}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    s = p.add_subparsers(dest='command',required=True)
    check = s.add_parser('check')
    check.add_argument('--image-skill')
    prep = s.add_parser('prepare')
    prep.add_argument('--job',type=Path,required=True)
    prep.add_argument('--run-dir',type=Path,required=True)
    prep.add_argument('--image-skill')
    for name in ('claim','record','finish','approve','packet','status','retry','sample'):
        c = s.add_parser(name)
        c.add_argument('--run-dir',type=Path,required=True)
        if name=='record':
            c.add_argument('--image',type=Path,required=True)
            c.add_argument('--tool-name',default=TOOL)
        if name=='approve':
            c.add_argument('--qa-note',required=True)
        if name=='retry':
            c.add_argument('--reason',choices=('quality','uncertain'),required=True)
            c.add_argument('--ack-duplicate-risk',action='store_true')
        if name=='sample':
            c.add_argument('--deck',type=Path,required=True)
            approval = c.add_mutually_exclusive_group(required=True)
            approval.add_argument('--user-approved',action='store_true')
            approval.add_argument('--test-fixture',action='store_true')
    for name in ('generate','generate-batch','edit'):
        s.add_parser(name,help='Unavailable in Python; Codex must execute the built-in image tool')
    a = p.parse_args()
    if a.command=='check':
        result = {'dependency_available':True,'image_skill_dir':str(skill_dir(a.image_skill)),
                  'backend':BACKEND,'tool_name':TOOL,'tool_availability':'must be checked by Codex in current session',
                  'python_can_generate':False,'network_configuration_required':False}
    elif a.command in {'generate','generate-batch','edit'}:
        raise ValueError('Python cannot call the built-in image tool. Use prepare/claim, then let Codex call '+TOOL)
    elif a.command=='prepare':
        result = prepare(a.job,a.run_dir.expanduser().resolve(),skill_dir(a.image_skill))
    else:
        run = a.run_dir.expanduser().resolve()
        b,j = read(run/'bridge.json'),job_state(run)
        jid = j['id']
        if a.command=='claim':
            result = native(run,'claim')
        elif a.command=='record':
            if a.tool_name!=TOOL:
                raise ValueError('only the selected built-in image tool is accepted')
            source = a.image.expanduser().resolve()
            from PIL import Image
            with Image.open(source) as im:
                im.verify()
            if j['status']=='running':
                # Persist provenance before the native queue transition so a crash is resumable.
                b['generation'] = {'tool_name':TOOL,'source_image':str(source),'source_sha256':sha(source),'recorded_at':now()}
                b.pop('review',None)
                write(run/'bridge.json',b)
                result = native(run,'record','--id',jid,'--image',source)
            elif j['status'] in {'generated','needs_review','completed'}:
                expected=Path(j.get('original',j.get('source_image','')))
                if not expected.is_file() or sha(expected)!=sha(source):
                    raise ValueError('recovery source does not match the existing generated image')
                if b.get('generation') and b['generation']['source_sha256']!=sha(source):
                    raise ValueError('recovery source differs from recorded provenance')
                b['generation'] = b.get('generation') or {'tool_name':TOOL,'source_image':str(source),'source_sha256':sha(source),'recorded_at':now(),'recovered':True}
                write(run/'bridge.json',b)
                result = j
            else:
                raise ValueError('record requires running or an existing generated result')
        elif a.command=='finish':
            result = native(run,'finish','--id',jid,'--fit',b['policy']['fit'])
            result['readability_gate'] = quality(run)
        elif a.command=='approve':
            if not a.qa_note.strip():
                raise ValueError('a visual QA note is required')
            gate = quality(run)
            if not gate['passed']:
                raise ValueError('readability heuristic rejected result; inspect and repair or obtain an approved threshold change')
            extra = ['--accept-actual-size'] if b['policy']['accept_actual_size'] else []
            # Persist the review first, so a crash after native approval can recover its packet.
            b['review'] = {'qa_note':a.qa_note,'reviewed_at':now()}
            write(run/'bridge.json',b)
            native(run,'approve','--id',jid,*extra)
            result = packet(run)
            write(run/'result.json',result)
        elif a.command=='packet':
            result = packet(run)
            write(run/'result.json',result)
        elif a.command=='retry':
            if j['attempts']>=b['policy']['max_attempts']:
                raise ValueError('attempt budget exhausted')
            if a.reason=='quality':
                if j['status']!='needs_review' or not b['policy']['approved'] or not b['policy']['auto_quality_retry']:
                    raise ValueError('quality retry needs a reviewed result and an approved automatic retry policy')
            elif not a.ack_duplicate_risk:
                raise ValueError('uncertain result needs explicit --ack-duplicate-risk; never auto-resubmit')
            result = native(run,'retry','--id',jid,'--ack-duplicate-risk')
        elif a.command=='sample':
            result = packet(run)
            deck = a.deck.expanduser().resolve()
            out = deck/'origin_image'/(jid+'.png')
            copy_png_once(result['selected_source'],out)
            method = {'backend_used':BACKEND,'tool_name':TOOL,'skill':'codex-imagegen-batch',
                      'mode':'generate','approved_sample_path':str(out),'image_run':str(run),
                      'sample_sha256':sha(out),'size':result['validation']['actual_size'],
                      'input_context_preparation':'worker view_image, then referenced_image_paths',
                      'handoff_rule':'use the same built-in tool; return a blocker if unavailable'}
            write(deck/'sample_receipt.json',{'user_approved':a.user_approved,'test_fixture':a.test_fixture,'sample_generation_method':method,'result':result})
            result = method
        else:
            result = {'slide_id':jid,'state':j,'policy':b['policy']}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)
