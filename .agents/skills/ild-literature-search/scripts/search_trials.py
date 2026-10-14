#!/usr/bin/env python3
"""Bounded original-publication metadata search; no paywall or proxy bypass."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import time
import xml.etree.ElementTree as ET
import httpx

TRIALS = {
    'SENSCIS': ('SENSCIS[Title/Abstract] AND Distler[Author] AND 2019[Date - Publication]', 'nintedanib for systemic sclerosis-associated interstitial lung disease'),
    'INBUILD': ('nintedanib[Title] AND progressive[Title] AND fibrosing[Title] AND 2019[Date - Publication]', 'nintedanib in progressive fibrosing interstitial lung diseases'),
    'TRAIL1': ('pirfenidone[Title] AND rheumatoid[Title] AND randomised[Title]', 'safety, tolerability, and efficacy of pirfenidone in patients with rheumatoid arthritis-associated interstitial lung disease'),
    'RELIEF': ('RELIEF[Title] AND pirfenidone[Title]', 'pirfenidone in patients with progressive fibrotic interstitial lung diseases other than idiopathic pulmonary fibrosis'),
    'U-ILD': ('pirfenidone[Title] AND unclassifiable[Title] AND placebo-controlled[Title] NOT design[Title]', 'pirfenidone in patients with unclassifiable progressive fibrosing interstitial lung disease: a double-blind, randomised, placebo-controlled, phase 2 trial'),
}

def normalized(s):
    return re.sub(r'\s+', ' ', s.replace('–', '-').replace('−', '-')).strip().lower().rstrip('.')

def content(node):
    return ''.join(node.itertext()) if node is not None else ''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--replay', type=Path, help='Reparse a prior successful response directory without network')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    raw = args.out / 'raw'; raw.mkdir()
    requests_log = []
    records = []
    cached = json.loads((args.replay/'requests.json').read_text()) if args.replay else []
    # trust_env preserves proxy/CA; verify is never disabled.
    client = httpx.Client(timeout=15, follow_redirects=True, trust_env=True)
    def get(name, url, params):
        if args.replay:
            match=next(t for t in cached if t['path']==f'raw/{name}.response')
            if str(httpx.Request('GET',url,params=params).url)!=match['url']:
                raise ValueError('Replay query differs from saved query')
            blob=(args.replay/match['path']).read_bytes()
            if hashlib.sha256(blob).hexdigest()!=match['sha256']:raise ValueError('Replay hash mismatch')
            response=httpx.Response(match['status'],content=blob,request=httpx.Request('GET',match['url']))
            utc=match['utc']
        else:
            time.sleep(0.4)  # NCBI anonymous request budget, sequential within process
            response = client.get(url, params=params)
            response.raise_for_status()
            blob = response.content
            utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
        path = raw / (name + '.response')
        path.write_bytes(blob)
        trace = dict(url=str(response.url), utc=utc, status=response.status_code,
                     sha256=hashlib.sha256(blob).hexdigest(), bytes=len(blob), path=str(path.relative_to(args.out)), transport='verified local replay' if args.replay else 'live HTTP')
        requests_log.append(trace)
        return response, trace
    for trial, (query, title_match) in TRIALS.items():
        item = dict(trial=trial, query=query, source_type='published original clinical trial; abstract only', full_text_status='not requested / not verified')
        try:
            response, trace = get(trial + '_search', 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
                                  dict(db='pubmed', term=query, retmode='json', retmax=20))
            search = response.json()['esearchresult']; ids = search['idlist']
            item.update(search_trace=trace, count=int(search['count']), candidate_pmids=ids)
            if not ids: raise ValueError('No PubMed candidates')
            if int(search['count']) > 20: raise ValueError('Search truncated; refine query before claiming unique selection')
            response, xml_trace = get(trial + '_pubmed', 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',
                                      dict(db='pubmed', id=','.join(ids), retmode='xml'))
            xml = ET.fromstring(response.content)
            candidates = [(article, content(article.find('.//ArticleTitle'))) for article in xml.findall('PubmedArticle')]
            selected = [(a, t) for a, t in candidates if normalized(t).startswith(title_match)
                        and 'study protocol' not in normalized(t) and 'design of' not in normalized(t)
                        and 'Randomized Controlled Trial' in [content(n) for n in a.findall('.//PublicationType')]]
            item['candidate_titles'] = [dict(pmid=a.findtext('.//MedlineCitation/PMID'), title=t) for a, t in candidates]
            if len(selected) != 1: raise ValueError(f'Original title match is not unique: {len(selected)}')
            a, title = selected[0]
            citation = a.find('MedlineCitation'); article = citation.find('Article')
            pmid = citation.findtext('PMID')
            doi = next((n.text for n in a.findall('./PubmedData/ArticleIdList/ArticleId') if n.get('IdType') == 'doi'), None)
            if not doi: raise ValueError('Missing DOI in PubMed original record')
            abstract = [dict(label=n.get('Label', 'UNLABELED'), text=content(n)) for n in article.findall('./Abstract/AbstractText')]
            authors = [dict(last=n.findtext('LastName'), initials=n.findtext('Initials'), collective=n.findtext('CollectiveName')) for n in article.findall('./AuthorList/Author')]
            start=article.findtext('./Pagination/StartPage'); end=article.findtext('./Pagination/EndPage')
            pages=article.findtext('./Pagination/MedlinePgn') or ('-'.join([start,end]) if start and end else start)
            date=article.find('./Journal/JournalIssue/PubDate')
            item.update(pmid=pmid, doi=doi, title=title, authors=authors,
                        journal=article.findtext('./Journal/Title'), year=article.findtext('./Journal/JournalIssue/PubDate/Year'),
                        publication_date=' '.join(content(n) for n in date) if date is not None else None,
                        volume=article.findtext('./Journal/JournalIssue/Volume'), issue=article.findtext('./Journal/JournalIssue/Issue'),
                        pages=pages,
                        publication_types=[content(n) for n in article.findall('./PublicationTypeList/PublicationType')],
                        abstract=abstract, pubmed_trace=xml_trace, pubmed_url=f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',
                        doi_url=f'https://doi.org/{doi}', source_xpath=f"PubmedArticle[MedlineCitation/PMID='{pmid}']/MedlineCitation/Article")
            response, ep_trace = get(trial + '_europepmc', 'https://www.ebi.ac.uk/europepmc/webservices/rest/search',
                                     dict(query=f'EXT_ID:{pmid} AND SRC:MED', format='json', resultType='core'))
            matches=response.json()['resultList']['result']
            if len(matches) != 1: raise ValueError('Europe PMC identity not unique')
            ep=matches[0]
            item['europepmc'] = dict(id=ep.get('id'), doi=ep.get('doi'), title=ep.get('title'), year=ep.get('pubYear'),
                                     abstract_html=ep.get('abstractText', ''), isOpenAccess=ep.get('isOpenAccess'), trace=ep_trace)
            item['status']='retrieved'
        except Exception as e:
            item.update(status='blocked', error=f'{type(e).__name__}: {e}')
        records.append(item)
        print(trial, item['status'], item.get('pmid', ''), item.get('error', ''), flush=True)
    client.close()
    (args.out/'requests.json').write_text(json.dumps(requests_log, ensure_ascii=False, indent=2))
    (args.out/'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    return 0 if all(i['status']=='retrieved' for i in records) else 1

if __name__ == '__main__':
    raise SystemExit(main())
