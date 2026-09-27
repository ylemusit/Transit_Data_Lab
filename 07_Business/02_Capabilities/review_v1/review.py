"""Revisión read-only; salidas exclusivamente en este directorio Business.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
Ejecutar una sola vez antes de la congelación; no sobrescribe evidencia previa.
"""
from pathlib import Path
import csv, hashlib, json, re, subprocess, zipfile
from collections import Counter
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
assert not (OUT / 'checks.json').exists(), 'La revisión ya existe; no sobrescribir.'
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def text(p): return p.read_text(encoding='utf-8-sig')
def csvrows(p):
    with p.open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))
def save(name, v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def inventory():
    paths=[]
    for area in ['02_Data_Engineering','03_Compliance','reports']:
        paths.extend(p for p in (ROOT/area).rglob('*') if p.is_file())
    paths.extend(ROOT/n for n in ['PROJECT_CURRENT_STATE.md','project_baseline.json','.gitignore'])
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)}
before=inventory(); save('technical_before.json',before)
checks=[]
def check(name, ok, detail):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def arrays(s):
    decoder=json.JSONDecoder(); pos=0; rows=[]
    while pos<len(s):
        if s[pos].isspace(): pos+=1; continue
        v,end=decoder.raw_decode(s,pos); rows.extend(v); pos=end
    return rows
def query(label,db,sql):
    command=['duckdb','-no-init','-batch','-bail','-readonly','-json',str(ROOT/db)]
    r=subprocess.run(command,input=sql,capture_output=True,text=True,encoding='utf-8')
    (OUT/(label+'.stdout.json')).write_text(r.stdout,encoding='utf-8')
    (OUT/(label+'.stderr.txt')).write_text(r.stderr,encoding='utf-8')
    (OUT/(label+'.exit_code.txt')).write_text(str(r.returncode),encoding='utf-8')
    (OUT/(label+'.sql')).write_text(sql,encoding='utf-8')
    check(label+'_exit',r.returncode==0,{'command':command,'exit_code':r.returncode})
    return arrays(r.stdout) if r.returncode==0 else []
idx=ROOT/'07_Business/02_Capabilities/EVIDENCE_INDEX.md'; s=text(idx)
rows=re.findall(r'\| \[([^\]]+)\]\(([^)]+)\) \| `([a-f0-9]{64})` \|',s)
check('evidence_count',len(re.findall(r'^### TDL-EVD-',s,re.M))==28,28)
check('path_count',len(rows)==len(set(r[0] for r in rows))==76,len(rows))
for name,link,expected in rows:
    p=(idx.parent/link).resolve(); actual=sha(p) if p.is_file() else None
    check('path:'+name,actual==expected and p==ROOT/name,{'expected':expected,'actual':actual})
reg=text(idx.parent/'CAPABILITY_REGISTER.md'); blocks=re.split(r'^## TDL-CAP-',reg,flags=re.M)[1:]
counts=Counter()
for b in blocks:
    cap='TDL-CAP-'+b[:3]; state=re.search(r'\| Estado \| ([A-Z_]+) \|',b).group(1); counts[state]+=1
    ev=set(re.findall(r'TDL-EVD-\d{3}',b))
    check('capability_links:'+cap,bool(ev) and all(cap in s.split('### '+id)[1].split('<a id=')[0] for id in ev),sorted(ev))
    for field in ['Limitaciones','Dependencias','Afirmación comercial permitida','Afirmaciones NO permitidas']:
        check(cap+':'+field,bool(re.search(r'\| '+field+r' \| .+ \|',b)),field)
check('distribution',dict(counts)=={'EXISTING':11,'PENDING_VERIFICATION':3,'PLANNED':4,'IN_DEVELOPMENT':2},dict(counts))
db='02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb'
sentinel=query('sentinel',db,text(ROOT/'02_Data_Engineering/GTFS_Lab/sql/07_tests/test_gtfs_lab_integrity.sql'))
statuses=Counter(r['status'] for r in sentinel)
check('sentinel_expected_warning',dict(statuses)=={'PASS':42,'FAIL':4},dict(statuses))
check('sentinel_absent_layers',set(r['check_name'] for r in sentinel if r['status']=='FAIL')=={'analysis','core','validation','validation.results'},[r for r in sentinel if r['status']=='FAIL'])
rawcols=query('raw_columns',db,"SELECT table_name,column_name,data_type FROM information_schema.columns WHERE table_schema='raw' ORDER BY 1,2;")
check('raw_varchar',len({r['table_name'] for r in rawcols})==7 and all(r['data_type']=='VARCHAR' for r in rawcols),len(rawcols))
zip_path=ROOT/'02_Data_Engineering/GTFS_Lab/feeds/raw/20260924_020003_Consorcio_Asturias.zip'
with zipfile.ZipFile(zip_path) as z:
    names=[n for n in z.namelist() if not n.endswith('/')]
    pairs=[{'entry':n,'zip_sha':hashlib.sha256(z.read(n)).hexdigest(),'extracted_sha':sha(ROOT/'02_Data_Engineering/GTFS_Lab/feeds/extracted/20260924_020003_Consorcio_Asturias'/n)} for n in names]
check('asturias_zip_extraction',len(pairs)==7 and all(r['zip_sha']==r['extracted_sha'] for r in pairs),pairs)
cdb='03_Compliance/databases/transit_compliance.duckdb'
catalog=query('compliance_catalog',cdb,'SELECT table_schema,table_name FROM information_schema.tables ORDER BY 1,2;')
tables=['source.documents','source.relationships','source.provisions','compliance.requirements','compliance.source_facts','compliance.deadlines','mapping.format_coverage','mapping.format_equivalences','audit.rules','audit.runs','audit.results']
countrows=query('compliance_counts',cdb,' UNION ALL '.join("SELECT '"+t+"' AS tbl, count(*) AS n FROM "+t for t in tables)+';')
current={r['tbl']:r['n'] for r in countrows}
expected={'source.documents':10,'source.relationships':6,'source.provisions':92,'compliance.requirements':48,'compliance.source_facts':36,'compliance.deadlines':10,'mapping.format_coverage':0,'mapping.format_equivalences':0,'audit.rules':0,'audit.runs':0,'audit.results':0}
check('compliance_counts',current==expected,current)
run=ROOT/'03_Compliance/reports/phase_2/freeze/promotion_resume/run_001'
for r in csvrows(run/'LEGAL_SOURCE_HASH_CHECKS.csv'):
    actual=sha(Path(r['path']))
    check('legal_source:'+r['document_id'],actual==r['expected_sha256']==r['actual_sha256'],actual)
for suite in csvrows(run/'FINAL_TEST_RESULTS.csv'):
    name=suite['suite']; results=arrays(text(run/(name+'.json')))
    tests=[r for r in results if 'test' in r and 'status' in r]
    sqlpath=next(ROOT/n for n,_,_ in rows if n.endswith('/'+name+'.sql'))
    check('persisted_suite:'+name,len(tests)==int(suite['checks']) and all(r['status']=='PASS' for r in tests) and text(run/(name+'.exit_code.txt')).strip()=='0' and sha(sqlpath)==suite['sql_sha256'],{'checks':len(tests),'status_counts':dict(Counter(r['status'] for r in tests)),'sql_sha256':sha(sqlpath)})
for suffix in ['REQUIREMENTS','SOURCE_FACTS','DEADLINES']:
    count=len(csvrows(ROOT/('03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_'+suffix+'.csv')))
    check('snapshot:'+suffix,count=={'REQUIREMENTS':48,'SOURCE_FACTS':36,'DEADLINES':10}[suffix],count)
for name,_,_ in rows:
    if name.endswith('.manifest.json'):
        manifest=json.loads(text(ROOT/name)); artifact=ROOT/name.removesuffix('.manifest.json')
        check('manifest:'+name,sha(artifact)==manifest['sha256'] and artifact.stat().st_size==manifest['size_bytes'],manifest)
census=json.loads(text(ROOT/'02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/source_census.json'))
check('census_five',len(census['operators'])==5,[o['operator'] for o in census['operators']])
for o in census['operators']:
    p=ROOT/'02_Data_Engineering/GTFS_Lab/20_clientes_reales'/o['original_zip']
    if not p.is_file(): p=Path(o['original_zip'])
    check('census_zip:'+o['benchmark_id'],p.is_file() and sha(p)==o['original_zip_sha256'],{'path':str(p),'expected':o['original_zip_sha256']})
diff=csvrows(ROOT/'02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/differential_matrix.csv')
check('comparison_descriptive',len({r['benchmark_id'] for r in diff})==5 and {r['comparison_class'] for r in diff} <= {'UNKNOWN','NOT_COMPARABLE'},dict(Counter(r['comparison_class'] for r in diff)))
after=inventory(); save('technical_after.json',after)
check('technical_unchanged',before==after,{'files':len(before),'added':sorted(after.keys()-before.keys()),'removed':sorted(before.keys()-after.keys()),'changed':[n for n in before.keys()&after.keys() if before[n]!=after[n]]})
save('checks.json',checks)
summary={'status':'PASS' if all(r['status']=='PASS' for r in checks) else 'FAIL','checks':len(checks),'failures':[r for r in checks if r['status']=='FAIL'],'distribution':dict(counts),'evidences':28,'paths':76}
save('summary.json',summary); print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(0 if summary['status']=='PASS' else 1)
