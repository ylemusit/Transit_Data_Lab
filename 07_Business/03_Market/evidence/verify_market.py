from pathlib import Path
import hashlib,json,re,sys,subprocess

ROOT=Path(__file__).resolve().parents[3]
MARKET=ROOT/'07_Business/03_Market'
OUT=MARKET/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,pass_=bool(ok),detail=detail))
before=json.loads((OUT/'scope_before.json').read_text(encoding='utf-8'))
after={}
for p in ROOT.rglob('*'):
 if p.is_file() and not any(x in p.relative_to(ROOT).parts for x in ['.git','07_Business']):after[p.relative_to(ROOT).as_posix()]=sha(p)
differences=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
check('outside_business_unchanged',not differences,{'before_count':len(before),'after_count':len(after),'differences':differences})
expected={'CAPABILITY_REGISTER.md':'39506abb74cf0437802603c7915d90ba62fce29ff38f6c21277cdabc577a4c15','EVIDENCE_INDEX.md':'f8bdcf9a49f09352fe754decc1c87881091c56c23edec4cff344c9eb2c691b41','CAPABILITY_GAPS.md':'2b33a86971f8f860039a9f2a0144da14a67867ef0c26ccb801a94ce96264e01d'}
capdir=ROOT/'07_Business/02_Capabilities'
for n,h in expected.items():check('frozen_'+n,sha(capdir/n)==h,{'expected':h,'actual':sha(capdir/n)})
aggregate=''.join(n+' '+h+'\n' for n,h in expected.items())
check('baseline_aggregate',hashlib.sha256(aggregate.encode()).hexdigest()=='5e0635956f40c6fbf27d6c6b16fcac8d4762f3fc1c93793d628c7df24dea30c2')
descriptor=(capdir/'BUSINESS_CAPABILITY_BASELINE_V1.md').read_text(encoding='utf-8')
check('descriptor_frozen','Estado: **FROZEN**' in descriptor)
names=['MARKET_EVIDENCE_REGISTER.md','CUSTOMER_SEGMENTS.md','PROBLEM_REGISTER.md','PROCUREMENT_EVIDENCE.md','COMPETITOR_LANDSCAPE.md','REGULATORY_DEMAND.md','MARKET_GAPS.md']
for n in names:check('document_'+n,(MARKET/n).exists() and (MARKET/n).stat().st_size>500)
registry=(MARKET/names[0]).read_text(encoding='utf-8')
ids=re.findall(r'^## (MKT-EVD-\d{3})$',registry,re.M)
check('evidence_unique_36',len(ids)==36 and len(set(ids))==36)
known=set(ids);missing=[];links=[]
docs=[MARKET/n for n in names]+[ROOT/'07_Business/BUSINESS_STATUS.md',ROOT/'07_Business/01_Governance/ASSUMPTIONS_REGISTER.md',ROOT/'07_Business/01_Governance/DECISION_LOG.md']
for p in docs:
 s=p.read_text(encoding='utf-8')
 for i in re.findall(r'MKT-EVD-\d{3}',s):
  if i not in known:missing.append([p.name,i])
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
  if target.startswith(('http:','https:')):continue
  local=target.split('#')[0]
  if local and not (p.parent/local).exists() and not local.endswith('verification.json'):links.append([p.name,target])
check('evidence_references_resolve',not missing,missing)
check('local_links_resolve',not links,links)
capids=set(re.findall(r'^\| (TDL-CAP-\d{3}) ',(MARKET/'MARKET_GAPS.md').read_text(encoding='utf-8'),re.M))
check('exactly_11_existing_in_matrix',capids=={'TDL-CAP-'+x for x in ['001','002','003','004','009','010','011','012','016','018','019']},sorted(capids))
for label,file,pattern,num in [('segments','CUSTOMER_SEGMENTS.md',r'^\| SEG-\d{3} ',15),('problems','PROBLEM_REGISTER.md',r'^\| PROB-\d{3} ',10),('obligations','REGULATORY_DEMAND.md',r'^\| OBL-\d{3} ',12),('providers','COMPETITOR_LANDSCAPE.md',r'^\| COMP-\d{3} ',11),('procurements','PROCUREMENT_EVIDENCE.md',r'^## PROC-\d{3}',8)]:
 count=len(re.findall(pattern,(MARKET/file).read_text(encoding='utf-8'),re.M));check(label+'_count',count==num,count)
status=(ROOT/'07_Business/BUSINESS_STATUS.md').read_text(encoding='utf-8')
check('status_in_progress','PHASE: BUSINESS PHASE 3 — MARKET EVIDENCE' in status and 'STATUS: IN PROGRESS' in status)
check('no_later_phase_directories',not any((ROOT/'07_Business'/n).exists() for n in ['04_Offering','05_Economics','06_Legal_and_Compliance','07_Go_to_Market']))
source_checks=[]
for p in OUT.glob('source_manifest*.json'):
 for r in json.loads(p.read_text(encoding='utf-8')):
  if r['status']=='SAVED':source_checks.append((r['name'],r.get('bytes',0)>0 and sha(OUT/r['file'])==r['sha256']))
for r in json.loads((OUT/'tuvisa_sources.json').read_text(encoding='utf-8')):
 if 'sha256' in r:source_checks.append((r['name'],sha(OUT/(r['name']+'.pdf'))==r['sha256']))
check('saved_source_hashes_match',all(v for _,v in source_checks),{'checked':len(source_checks),'failed':[n for n,v in source_checks if not v]})
check('economic_arithmetic',31866.25+60000+188873.75+660810==941550 and 31866.25+60000+188873.75+795310==1076050)
git_status=subprocess.run(['git','status','--short'],cwd=ROOT,capture_output=True,text=True)
git_diff=subprocess.run(['git','diff','--stat'],cwd=ROOT,capture_output=True,text=True)
(OUT/'git_status_after.txt').write_text(git_status.stdout,encoding='utf-8')
(OUT/'git_diff_after.txt').write_text(git_diff.stdout,encoding='utf-8')
result={'date':'2026-09-27','verification':'PASS' if all(c['pass_'] for c in checks) else 'FAIL','checks':checks,'document_sha256':{str(p.relative_to(ROOT)):sha(p) for p in docs},'baseline_descriptor_sha256':sha(capdir/'BUSINESS_CAPABILITY_BASELINE_V1.md'),'limitations':['Automated checks cover document structure, references, source hashes and scope; source interpretation reviewed manually.','Git repository untracked; empty diff is not proof of unchanged files.','Legal source EU only partial primary excerpts; no legal certification.'],'market_evidence_result':'PASS for A-G, no commercial validation'}
(OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(result['verification'],len(checks),'checks; outside Business',len(after),'files; sources',len(source_checks))
for c in checks:
 if not c['pass_']:print(c)
sys.exit(0 if result['verification']=='PASS' else 1)
