#!/usr/bin/env python3
# coding: utf-8
"""Validate final image/state correspondence before existing PPT assembly."""
from pathlib import Path
import json
import re
from PIL import Image
from image_gen import BACKEND, packet, sha


def validate_deck(directory,aspect_ratio='16:9'):
    deck = Path(directory).resolve()
    jobs = json.loads((deck/'slide_jobs.json').read_text(encoding='utf-8'))
    if jobs.get('selected_backend')!=BACKEND:
        raise ValueError('deck backend does not match built-in image workflow')
    slides = jobs.get('slides',[])
    if not slides or [s['number'] for s in slides]!=list(range(1,len(slides)+1)):
        raise ValueError('slide numbers must be complete, unique and in presentation order')
    expected = {f"slide_{s['number']:02d}.png" for s in slides}
    actual = {p.name for p in (deck/'origin_image').iterdir() if p.is_file() and re.match(r'^slide_\d+\.',p.name)}
    if actual!=expected:
        raise ValueError('missing/extra final slide files: '+str(sorted(actual^expected)))
    w,h = map(int,aspect_ratio.split(':'))
    checks = []
    for slide in slides:
        if slide['status'] not in {'accepted','recorded'}:
            raise ValueError(slide['slide_id']+' is not ready: '+slide['status'])
        result = slide.get('result') or {}
        path = deck/slide['out']
        if not path.resolve().is_relative_to(deck):
            raise ValueError('final image must remain inside the deck directory')
        if sha(path)!=result.get('final_image_sha256'):
            raise ValueError('final image hash mismatch: '+slide['slide_id'])
        receipt = packet(Path(result['image_run']))
        if receipt['slide_id']!=slide['slide_id']:
            raise ValueError('image queue belongs to another page')
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            if abs((im.width/im.height)/(w/h)-1)>0.005:
                raise ValueError('page ratio would be stretched during assembly: '+slide['slide_id'])
            checks.append({'slide':slide['slide_id'],'size':list(im.size),'sha256':sha(path)})
    speech = deck/'speech.md'
    if speech.exists():
        from assemble_ppt import load_speaker_notes
        notes = load_speaker_notes(str(deck))
        if set(notes)!={s['number'] for s in slides}:
            raise ValueError('speaker notes do not correspond to every slide')
    return {'slide_count':len(slides),'aspect_ratio':aspect_ratio,'checks':checks}
