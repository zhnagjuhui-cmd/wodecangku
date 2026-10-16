#!/usr/bin/env python3
"""Local queue only; Codex's built-in image tool performs generation."""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time

SIZES = {'square':'2048x2048','2k':'2048x2048','wide':'2560x1440',
         'landscape':'2560x1440','portrait':'1440x2560','vertical':'1440x2560',
         '4k-wide':'3840x2160','4k-portrait':'2160x3840'}
TERMINAL = {'completed','failed','cancelled'}
ACTIVE = {'running','generated','needs_review'}


def now():
    return datetime.now(timezone.utc).isoformat()


def emit(obj):
    print(json.dumps(obj,ensure_ascii=False,indent=2),flush=True)


def size(value):
    if not isinstance(value,str):
        raise ValueError('size must be a string')
    value = SIZES.get(value,value)
    if value != 'auto':
        if not re.fullmatch(r'[1-9][0-9]*x[1-9][0-9]*',value):
            raise ValueError('size must be auto, an alias, or WIDTHxHEIGHT')
        w,h = map(int,value.split('x'))
        if w*h > 100_000_000:
            raise ValueError('local processing limit: 100 million pixels')
    return value


def inspect_image(path):
    from PIL import Image, ImageOps
    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        transparent = im.convert('RGBA').getchannel('A').getextrema()[0] < 255
        return {'size':list(im.size),'transparent':transparent}


def normalize(raw,index,base):
    if not isinstance(raw,dict):
        raise ValueError('each job must be an object')
    allowed = {'id','prompt','size','operation','references','preserve','avoid','transparent_background'}
    if set(raw)-allowed:
        raise ValueError('unknown job fields: '+', '.join(sorted(set(raw)-allowed)))
    jid = raw.get('id','image-%03d'%index)
    if not isinstance(jid,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}',jid):
        raise ValueError('id must contain 1-64 letters/digits/_/-')
    prompt = raw.get('prompt')
    if not isinstance(prompt,str) or not prompt.strip():
        raise ValueError('prompt must be a nonempty string')
    operation = raw.get('operation','generate')
    if operation not in {'generate','edit','style-transfer'}:
        raise ValueError('invalid operation')
    refs = raw.get('references',[])
    if not isinstance(refs,list):
        raise ValueError('references must be an array')
    normalized, target_transparent = [], False
    for ref in refs:
        if not isinstance(ref,dict) or set(ref)-{'path','conversation','role'}:
            raise ValueError('invalid reference fields')
        role = ref.get('role','reference')
        if role not in {'target','style','reference'} or ('path' in ref)==('conversation' in ref):
            raise ValueError('reference needs path or conversation and a valid role')
        out = {'role':role}
        if 'path' in ref:
            if not isinstance(ref['path'],str) or not ref['path']:
                raise ValueError('reference path must be a nonempty string')
            path = Path(ref['path']).expanduser()
            path = (base/path).resolve()
            if not path.is_file():
                raise ValueError('missing reference: '+str(path))
            out['path'] = str(path)
            if role=='target':
                target_transparent |= inspect_image(path)['transparent']
        else:
            if not isinstance(ref['conversation'],str) or not ref['conversation'].strip():
                raise ValueError('conversation reference needs a description')
            out['conversation'] = ref['conversation']
        normalized.append(out)
    if operation!='generate' and not any(r['role']=='target' for r in normalized):
        raise ValueError('edit/style-transfer requires a target reference')
    job = {'id':jid,'prompt':prompt,'size':size(raw.get('size','auto')),
           'operation':operation,'references':normalized}
    for key in ('preserve','avoid'):
        value = raw.get(key,[])
        if not isinstance(value,list) or any(not isinstance(v,str) for v in value):
            raise ValueError(key+' must be an array of strings')
        job[key] = value
    transparent = raw.get('transparent_background',target_transparent)
    if type(transparent) is not bool:
        raise ValueError('transparent_background must be boolean')
    job.update(transparent_background=transparent,status='pending',attempts=0,history=[])
    return job


def event(job,status,**details):
    job['status'] = status
    job['history'].append({'time':now(),'status':status,**details})


def save(root,data):
    data['updated_at'] = now()
    fd,tmp = tempfile.mkstemp(prefix='.queue-',dir=root)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp,root/'queue.json')
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def locked(root):
    with (root/'.queue.lock').open('a+b') as f:
        if os.name=='nt':
            import msvcrt
            f.seek(0)
            f.write(b'0')
            f.flush()
            f.seek(0)
            msvcrt.locking(f.fileno(),msvcrt.LK_LOCK,1)
        else:
            import fcntl
            fcntl.flock(f,fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name=='nt':
                f.seek(0)
                msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
            else:
                fcntl.flock(f,fcntl.LOCK_UN)


def load(root):
    with (root/'queue.json').open(encoding='utf-8') as f:
        data = json.load(f)
    if data.get('version')!=1 or data.get('backend')!='codex-built-in':
        raise ValueError('unsupported queue format')
    return data


def summary(data):
    return {'backend':data['backend'],'counts':dict(Counter(j['status'] for j in data['jobs'])),
            'jobs':[{k:j[k] for k in ('id','status','attempts','size','output','validation') if k in j}
                    for j in data['jobs']]}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def unique(folder,jid,suffix):
    path,count = folder/(jid+suffix),2
    while path.exists():
        path = folder/('%s-v%d%s'%(jid,count,suffix))
        count += 1
    return path


def finish(root,job,fit):
    from PIL import Image, ImageOps
    source = Path(job.get('original',job.get('source_image','')))
    if not source.is_file():
        raise ValueError('record a valid generated image first')
    info = inspect_image(source)
    requested = None if job['size']=='auto' else tuple(map(int,job['size'].split('x')))
    if fit!='verify' and requested is None:
        raise ValueError('post-processing requires a concrete target size')
    originals,outputs = root/'originals',root/'outputs'
    originals.mkdir(exist_ok=True)
    outputs.mkdir(exist_ok=True)
    if 'original' not in job:
        suffix = source.suffix.lower() or '.img'
        original = originals/(job['id']+'-'+digest(source)[:12]+suffix)
        if original.exists():
            if digest(original)!=digest(source):
                raise ValueError('original filename collision')
        else:
            with source.open('rb') as src,original.open('xb') as dst:
                shutil.copyfileobj(src,dst)
        job['original'] = str(original)
        source = original
    suffix = source.suffix if fit=='verify' else '.png'
    output = unique(outputs,job['id'],suffix)
    if fit=='verify':
        with source.open('rb') as src,output.open('xb') as dst:
            shutil.copyfileobj(src,dst)
    else:
        with Image.open(source) as im:
            im = ImageOps.exif_transpose(im).convert('RGBA')
            if fit=='cover':
                im = ImageOps.fit(im,requested,method=Image.Resampling.LANCZOS)
            elif fit=='stretch':
                im = im.resize(requested,Image.Resampling.LANCZOS)
            else:
                contained = ImageOps.contain(im,requested,method=Image.Resampling.LANCZOS)
                color = (0,0,0,0) if job['transparent_background'] else (255,255,255,255)
                im = Image.new('RGBA',requested,color)
                im.alpha_composite(contained,((requested[0]-contained.width)//2,
                                             (requested[1]-contained.height)//2))
            with output.open('xb') as f:
                im.save(f,format='PNG')
    actual = inspect_image(output)
    ow,oh = info['size']
    scale = 1.0
    if requested and fit!='verify':
        ratios = requested[0]/ow,requested[1]/oh
        scale = min(ratios) if fit=='contain' else max(ratios)
    validation = {'original_size':info['size'],'requested_size':job['size'],
                  'actual_size':actual['size'],'size_matches':requested is None or actual['size']==list(requested),
                  'transparent':actual['transparent'],
                  'transparency_ok':not job['transparent_background'] or actual['transparent'],
                  'fit':fit,'upscaled':scale>1.0,'sha256':digest(output)}
    job.update(output=str(output),validation=validation)
    event(job,'needs_review',output=str(output),validation=validation)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    sub.add_parser('sizes')
    for name in ('init','claim','record','finish','approve','status','poll','fail','retry','cancel'):
        p = sub.add_parser(name)
        p.add_argument('--queue',type=Path,required=True)
        if name=='init':
            source = p.add_mutually_exclusive_group(required=True)
            source.add_argument('--jobs',type=Path)
            source.add_argument('--prompt')
            p.add_argument('--size',default='auto')
        if name in {'record','finish','approve','fail','retry','cancel'}:
            p.add_argument('--id',required=True)
        if name=='record':
            p.add_argument('--image',type=Path,required=True)
        if name=='finish':
            p.add_argument('--fit',choices=('verify','contain','cover','stretch'),default='verify')
        if name=='approve':
            p.add_argument('--accept-actual-size',action='store_true')
        if name in {'fail','cancel'}:
            p.add_argument('--reason',required=True)
        if name=='retry':
            p.add_argument('--ack-duplicate-risk',action='store_true',required=True)
        if name=='poll':
            p.add_argument('--timeout',type=float,default=30)
            p.add_argument('--interval',type=float,default=2)
    args = parser.parse_args()
    if args.command=='sizes':
        emit({'aliases':SIZES,'note':'Request/validation targets; native output size is not guaranteed.'})
        return 0
    root = args.queue.expanduser().resolve()
    if args.command=='init':
        if args.jobs:
            source = args.jobs.expanduser().resolve()
            raw = [json.loads(line) for line in source.read_text(encoding='utf-8').splitlines() if line.strip()]
            base = source.parent
        else:
            raw,base = [{'prompt':args.prompt,'size':args.size}],Path.cwd()
        jobs = [normalize(r,i+1,base) for i,r in enumerate(raw)]
        if not jobs or len({j['id'] for j in jobs})!=len(jobs):
            raise ValueError('queue must be nonempty and ids unique')
        root.mkdir(parents=True,exist_ok=False)
        with locked(root):
            data = {'version':1,'backend':'codex-built-in','created_at':now(),'jobs':jobs}
            save(root,data)
        emit({'queue':str(root),**summary(data)})
        return 0
    if args.command=='poll':
        if not 0<=args.timeout<=55 or not 0.1<=args.interval<=10:
            raise ValueError('timeout must be 0..55 and interval 0.1..10 seconds')
        deadline,previous = time.monotonic()+args.timeout,None
        while True:
            data = load(root)
            state = summary(data)
            if state!=previous:
                emit(state)
                previous = state
            if all(j['status'] in TERMINAL for j in data['jobs']):
                return 0 if all(j['status']=='completed' for j in data['jobs']) else 2
            remaining = deadline-time.monotonic()
            if remaining<=0:
                return 3
            time.sleep(min(args.interval,remaining))
    with locked(root):
        data = load(root)
        if args.command=='status':
            emit(summary(data))
            return 0
        if args.command=='claim':
            if any(j['status'] in ACTIVE for j in data['jobs']):
                raise ValueError('active job exists; resume it before claiming another')
            job = next((j for j in data['jobs'] if j['status']=='pending'),None)
            if job is None:
                emit({'job':None,**summary(data)})
                return 0
            job['attempts'] += 1
            event(job,'running')
        else:
            job = next((j for j in data['jobs'] if j['id']==args.id),None)
            if job is None:
                raise ValueError('unknown job id')
            state = job['status']
            if args.command=='record':
                if state!='running':
                    raise ValueError('record requires running state')
                source = args.image.expanduser().resolve()
                inspect_image(source)
                job['source_image'] = str(source)
                event(job,'generated',source_image=str(source))
            elif args.command=='finish':
                if state not in {'generated','needs_review'}:
                    raise ValueError('finish requires generated or needs_review state')
                finish(root,job,args.fit)
            elif args.command=='approve':
                if state!='needs_review':
                    raise ValueError('approve requires needs_review state')
                check = job['validation']
                if not check['transparency_ok']:
                    raise ValueError('required transparency is missing')
                if not check['size_matches'] and not args.accept_actual_size:
                    raise ValueError('size mismatch: accept actual size or choose authorized fit')
                if digest(job['output'])!=check['sha256']:
                    raise ValueError('output changed after validation')
                job['accepted_actual_size'] = args.accept_actual_size
                event(job,'completed',accepted_actual_size=args.accept_actual_size)
            elif args.command=='retry':
                if state not in {'running','generated','needs_review','failed'}:
                    raise ValueError('only uncertain or failed jobs may be retried')
                for key in ('source_image','original','output','validation','accepted_actual_size'):
                    job.pop(key,None)
                event(job,'pending',ack_duplicate_risk=True)
            else:
                if state in TERMINAL:
                    raise ValueError('terminal job requires explicit retry')
                event(job,'failed' if args.command=='fail' else 'cancelled',reason=args.reason)
        save(root,data)
        emit(job)
    return 0


if __name__=='__main__':
    try:
        sys.exit(main())
    except (ValueError,OSError,KeyError,ImportError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr)
        sys.exit(2)
