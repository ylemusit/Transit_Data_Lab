from pathlib import Path
import urllib.request, hashlib, json, concurrent.futures, re
from html.parser import HTMLParser
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
SOURCES = {
 'tuvisa_notice': 'https://www.euskadi.eus/anuncio_contratacion/desarrollo-despliegue-y-validacion-datos-transporte-avanzados-formatos-gtfs-gtfs-rt-siri-y-netex/web01-tramite/es/',
 'attg_notice': 'https://www.euskadi.eus/web01-tramite/es/contenidos/anuncio_contratacion/expjaso16796/es_doc/es_arch_expjaso16796.html',
 'attg_ppt': 'https://www.contratacion.euskadi.eus/webkpe00-kpeperfi/es/contenidos/anuncio_contratacion/expjaso16796/es_doc/adjuntos/pliego_bases_tecnicas1.pdf',
 'ctm_document': 'https://contrataciondelestado.es/wps/wcm/connect/PLACE_es/Site/area/docAccCmpnt?DocumentIdParam=9259f10b-7ff6-4991-b8d1-6d948a5fc1a5&cmpntname=GetDocumentsById&source=library&srv=cmpnt',
 'puglia_purchase': 'https://trasparenza.regione.puglia.it/sites/default/files/2024-07/078_DIR_2024_00076_DeterminaPUB.pdf',
 'wiltshire_award': 'https://www.find-tender.service.gov.uk/Notice/023202-2022',
 'bods_notice': 'https://www.find-tender.service.gov.uk/Notice/025414-2023',
 'ley9_consolidated': 'https://www.boe.es/eli/es/l/2025/12/03/9/con',
 'eu_2024_490': 'https://eur-lex.europa.eu/eli/reg_del/2024/490/oj/spa/pdf',
 'eu_2017_1926': 'https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:02017R1926-20240304',
 'nap_catalog': 'https://nap.transportes.gob.es/Files/List?showFilterTT=true',
 'moveuskadi': 'https://www.euskadi.eus/contenidos/ds_movilidad/md_ideeu_moveuskadi/es_def/index.shtml',
 'enroute_chouette': 'https://enroute.mobi/fr/chouette',
 'enroute_operator': 'https://enroute.mobi/fr/operator',
 'trillium_terms': 'https://trilliumtransit.com/gtfs-maintenance-terms-of-service/',
 'trillium_gtfs': 'https://trilliumtransit.com/gtfs/',
 'ito_quality': 'https://www.itoworld.com/inside-ito/why-ito/data-quality/',
 'mobilitydata_readme': 'https://raw.githubusercontent.com/MobilityData/gtfs-validator/master/README.md',
 'mobilitydata_rules': 'https://gtfs-validator.mobilitydata.org/rules.html',
 'mobilitydata_web': 'https://gtfs-validator.mobilitydata.org/',
 'rt_validator': 'https://raw.githubusercontent.com/MobilityData/gtfs-realtime-validator/master/README.md',
 'otp_formats': 'https://docs.opentripplanner.org/en/latest/features-explained/Netex-Siri-Compatibility/',
 'gtfs_best_practices': 'https://gtfs.org/documentation/schedule/schedule-best-practices/',
 'siri_france': 'https://normes.transport.data.gouv.fr/normes/siri/profil-france/',
 'netex_france': 'https://normes.transport.data.gouv.fr/normes/netex/elements_communs/',
 'entur_siri': 'https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370373/General+information+SIRI',
}
class TextParser(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]; self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.skip+=1
  if t in ('p','div','br','h1','h2','h3','li','tr'): self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'): self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def collect(item):
 name,url=item
 try:
  with urllib.request.urlopen(url,timeout=35) as r:
   b=r.read(); ct=r.headers.get('Content-Type',''); actual=r.url; charset=r.headers.get_content_charset() or 'utf-8'
  ext='.pdf' if b.startswith(b'%PDF') else '.html' if 'html' in ct else '.md'
  p=OUT/(name+ext);p.write_bytes(b)
  if ext=='.pdf': text='\n'.join(f'PAGE {i+1}\n'+(x.extract_text() or '') for i,x in enumerate(PdfReader(p).pages))
  else:
   try: text=b.decode(charset)
   except UnicodeDecodeError:text=b.decode('latin-1')
   if ext=='.html': parser=TextParser();parser.feed(text);text=''.join(parser.parts)
  text=re.sub(r'\n[ \t]*\n+', '\n\n', text)
  (OUT/(name+'.txt')).write_text(text,encoding='utf-8')
  return dict(name=name,url=url,resolved_url=actual,consulted='2026-09-27',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),file=p.name,status='SAVED')
 except Exception as e:return dict(name=name,url=url,consulted='2026-09-27',status='UNAVAILABLE',error=str(e))
if __name__=='__main__':
 results=list(concurrent.futures.ThreadPoolExecutor(6).map(collect,SOURCES.items()))
 (OUT/'source_manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 for r in results:print(r['name'],r['status'],r.get('bytes',r.get('error')))
