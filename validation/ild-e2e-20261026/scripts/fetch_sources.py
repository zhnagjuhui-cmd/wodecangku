import urllib.request, urllib.parse, json, pathlib, hashlib, re, datetime
BASE=pathlib.Path(__file__).resolve().parents[1]; L=BASE/'literature'; (L/'pdfs').mkdir(exist_ok=True)
records=json.loads((L/'original_records.json').read_text()); log=[]
def fetch(label,url,suffix):
 item={'label':label,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'ILD-Evidence-validation/1.0'})
  with urllib.request.urlopen(req,timeout=25) as r: data=r.read(25000000);item.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(data))
  if data.startswith(b'%PDF'):
   import fitz
   d=fitz.open(stream=data,filetype='pdf'); text='\n'.join(p.get_text() for p in d);item.update(pages=len(d),pdf=True,sha256=hashlib.sha256(data).hexdigest());(L/'pdfs'/f'{label}.pdf').write_bytes(data);(L/f'{label}_pdf_text.txt').write_text(text)
  else:(L/f'{label}.{suffix}').write_bytes(data);item['pdf']=False
 except Exception as e:item['error']=str(e)
 log.append(item); print(json.dumps(item,ensure_ascii=False),flush=True)
 (BASE/'logs'/'fetch.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
for name,r in records.items():
 fetch(name+'_pubmed','https://pubmed.ncbi.nlm.nih.gov/'+r['id']+'/?format=pubmed','txt')
 fetch(name+'_crossref','https://api.crossref.org/works/'+urllib.parse.quote(r['doi'],safe=''),'json')
 urls=[x['url'] for x in r.get('fullTextUrlList',{}).get('fullTextUrl',[]) if x.get('availabilityCode')=='F']
 if not urls: urls=['https://www.nejm.org/doi/pdf/10.1056/NEJMoa1903076'] if name=='SENSCIS' else ['https://www.thelancet.com/journals/lanres/article/PIIS2213-2600(22)00260-0/fulltext']
 for i,u in enumerate(urls):fetch(name+'_open_'+str(i),u.replace('http://hdl.handle.net','https://hdl.handle.net'),'html')
for name,nct in [('SENSCIS','NCT02597933'),('INBUILD','NCT02999178'),('TRAIL1','NCT02808871'),('U-ILD','NCT03099187')]:fetch(name+'_registry','https://clinicaltrials.gov/api/v2/studies/'+nct,'json')
