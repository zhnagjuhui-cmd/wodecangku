#!/usr/bin/env python3
"""Fail-closed source-integrity and cross-index evidence checks."""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

def norm(s):
    return re.sub(r'\s+', ' ', html.unescape(s).replace('−', '-').replace('–', '-')).strip().lower().rstrip('.')

def text(n):
    return ''.join(n.itertext()) if n is not None else ''

def numbers(s):
    return Counter(re.findall(r'\d+(?:\.\d+)?', norm(s)))

def verify(path):
    records = json.loads(path.read_text())
    results=[]
    for r in records:
        checks={}
        try:
            checks['retrieved']=r['status']=='retrieved'
            if not checks['retrieved']: raise ValueError(r.get('error', 'Not retrieved'))
            for key in ['search_trace', 'pubmed_trace']:
                tr=r[key]; blob=(path.parent/tr['path']).read_bytes()
                checks[key+'_sha256']=hashlib.sha256(blob).hexdigest()==tr['sha256']
            tr=r['europepmc']['trace']; ep_blob=(path.parent/tr['path']).read_bytes()
            checks['europepmc_sha256']=hashlib.sha256(ep_blob).hexdigest()==tr['sha256']
            xml=ET.parse(path.parent/r['pubmed_trace']['path'])
            a=next((a for a in xml.findall('PubmedArticle') if a.findtext('./MedlineCitation/PMID')==r['pmid']),None)
            if a is None: raise ValueError('PMID not present in source XML')
            checks['candidate_selection']=r['pmid'] in r['candidate_pmids']
            doi=next((n.text for n in a.findall('./PubmedData/ArticleIdList/ArticleId') if n.get('IdType')=='doi'), '')
            checks['pubmed_doi']=norm(doi)==norm(r['doi'])
            checks['pubmed_title']=norm(text(a.find('.//ArticleTitle')))==norm(r['title'])
            checks['pubmed_year']=a.findtext('.//JournalIssue/PubDate/Year')==r['year']
            start=a.findtext('.//Pagination/StartPage');end=a.findtext('.//Pagination/EndPage')
            pages=a.findtext('.//Pagination/MedlinePgn') or ('-'.join([start,end]) if start and end else start)
            checks['pubmed_pages']=pages==r['pages']
            source_abstract=[dict(label=n.get('Label','UNLABELED'),text=text(n)) for n in a.findall('.//AbstractText')]
            checks['pubmed_extraction']=source_abstract==r['abstract'] and bool(source_abstract)
            ep=json.loads(ep_blob)['resultList']['result'][0]
            checks['europepmc_id']=ep.get('id')==r['pmid']==r['europepmc']['id']
            checks['europepmc_doi']=norm(ep.get('doi',''))==norm(r['doi'])==norm(r['europepmc']['doi'])
            checks['europepmc_title']=norm(ep.get('title',''))==norm(r['title'])==norm(r['europepmc']['title'])
            checks['europepmc_year']=ep.get('pubYear')==r['year']
            # Remove actual element tags only. A statistical P<0.001 is text,
            # not a tag; a broad <...> expression would delete clinical values.
            ep_text=html.unescape(re.sub(r'</?[A-Za-z][^>]*>', ' ', ep.get('abstractText','')))
            checks['europepmc_extraction']=ep.get('abstractText','')==r['europepmc']['abstract_html'] and bool(ep_text)
            pm_text=' '.join(s['text'] for s in source_abstract)
            pm_numbers=numbers(pm_text); ep_numbers=numbers(ep_text)
            checks['abstract_numbers']=pm_numbers==ep_numbers and bool(pm_numbers)
            result=dict(trial=r['trial'],pmid=r['pmid'],checks=checks,status='PASS' if all(checks.values()) else 'FAIL',
                        numerical_token_count=sum(pm_numbers.values()), only_pubmed=dict(pm_numbers-ep_numbers), only_europepmc=dict(ep_numbers-pm_numbers),
                        source_xpath=r['source_xpath'], evidence_scope='original trial abstract; no full-text or independent trial replication')
        except Exception as e:
            result=dict(trial=r.get('trial'),checks=checks,status='FAIL',error=f'{type(e).__name__}: {e}')
        results.append(result)
    expected={'SENSCIS','INBUILD','TRAIL1','RELIEF','U-ILD'}
    complete={r.get('trial') for r in records}==expected and len(records)==5
    return dict(status='PASS' if complete and all(r['status']=='PASS' for r in results) else 'FAIL', complete_five_trials=complete,
                records_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), results=results,
                limitation='Mechanical identity/integrity/numerical-token verification only. Clinical interpretation and full statistical appraisal require professional review.')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--records',type=Path,required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args()
    result=verify(a.records)
    with a.out.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__': raise SystemExit(main())
