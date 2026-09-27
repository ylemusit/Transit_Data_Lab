"""Targeted documentary check. No recursion, technical runs, or source hashing."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone

started = time.monotonic()
out = Path(__file__).resolve().parent
market = out.parent
business = market.parent
root = business.parent
reads = {}
checks = []

def read(p):
    p = p.resolve()
    if not p.is_relative_to(business):
        raise RuntimeError('Read outside explicit Business scope')
    data = p.read_bytes()
    reads[str(p.relative_to(root))] = len(data)
    return data.decode('utf-8-sig')

def check(name, ok, detail=None):
    checks.append(dict(name=name, passed=bool(ok), detail=detail))

def rows(name):
    return list(csv.DictReader(read(market / name).splitlines()))

required = ['MARKET_PROBLEM_REGISTER.csv', 'COMMERCIAL_VALIDATION_READINESS.csv',
            'MARKET_VALIDATION_PLAN.md', 'CUSTOMER_DISCOVERY_INTERVIEW_GUIDE.md',
            'COMMERCIAL_VALIDATION_EVIDENCE_MODEL.md',
            'BUSINESS_PHASE_3_VALIDATION_GATE.md', 'RESOURCE_USAGE_POLICY.md']
docs = {n: read(market / n) for n in required}
problems = rows(required[0])
ready = rows(required[1])
expected = {f'PROB-{n:03d}' for n in range(1, 11)}
canonical = read(market / 'PROBLEM_REGISTER.md')
source = read(market / 'MARKET_EVIDENCE_REGISTER.md')
accepted = json.loads(read(market / 'evidence/accepted_evidence.json'))
historic = json.loads(read(market / 'evidence/verification.json'))
capregister = read(business / '02_Capabilities/CAPABILITY_REGISTER.md')
baseline = read(business / '02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md')
proc = read(market / 'PROCUREMENT_EVIDENCE.md')
gaps = read(market / 'MARKET_GAPS.md')
assumptions = read(business / '01_Governance/ASSUMPTIONS_REGISTER.md')
status = read(business / 'BUSINESS_STATUS.md')
decisions = read(business / '01_Governance/DECISION_LOG.md')
gate = docs['BUSINESS_PHASE_3_VALIDATION_GATE.md']

check('10 canonical problems, unique and no inventions',
      len(problems) == len(ready) == 10 and
      {r['problem_id'] for r in problems} == expected ==
      {r['problem_id'] for r in ready} == set(re.findall(r'\| (PROB-\d{3}) \|', canonical)))
check('Required CSV schemas',
      list(problems[0]) == ['problem_id','problem_name','problem_description','affected_actor',
       'segment','evidence_count','procurement_evidence','observed_problem_evidence',
       'regulatory_evidence','provider_evidence','free_alternative_evidence',
       'TDL_capability_relation','current_assumption_relation','notes'] and
      list(ready[0]) == ['problem_id','problem','affected_actor','evidence_level',
       'observed_evidence','procurement_evidence','regulatory_driver','free_alternative',
       'TDL_fit','differentiation_status','key_uncertainty','validation_needed',
       'commercial_validation_candidate'])
eids = {f'MKT-EVD-{n:03d}' for n in range(1, 37)}
check('36 accepted evidence IDs retained and individually traceable',
      len(accepted) == 36 and {r['id'] for r in accepted} == eids ==
      set(re.findall(r'^## (MKT-EVD-\d{3})', source, re.M)) ==
      set(re.findall(r'^\| (MKT-EVD-\d{3}) \|', gate, re.M)))
blocks = re.split(r'\n## ', source)[1:]
check('Each evidence has existing source, locator, limits and review index',
      all('| Fuente |' in b and '| Localizador |' in b and '| Limitaciones |' in b
          and b.splitlines()[0] in gate for b in blocks))
links_ok = True
for r in problems:
    ids = set(re.findall(r'MKT-EVD-\d{3}', str(r)))
    links_ok &= ids <= eids and int(r['evidence_count']) == len(ids)
    original = {b.splitlines()[0] for b in blocks if int(r['problem_id'][-3:]) in
                [int(n) for n in re.findall(r'\d{3}', next(
                    (l for l in b.splitlines() if l.startswith('| Relación problema')), ''))]}
    links_ok &= original <= ids
check('Problem counts are unique IDs and preserve canonical evidence links', links_ok)
pcases = {f'PROC-{n:03d}' for n in range(1, 9)}
check('8 procurement cases accounted for once in classification table',
      set(re.findall(r'^## (PROC-\d{3})', proc, re.M)) == pcases ==
      set(re.findall(r'^\| (PROC-\d{3}) ', gate, re.M)) and
      len(re.findall(r'^\| PROC-\d{3} ', gate, re.M)) == 8)
check('Procurement values and boundaries preserved', all(x in gate for x in [
    '31.866,25', '60.000', '660.810', '134.500', '188.873,75',
    '149.710', '742.605', '145.570.280', '385.709.149,20',
    'NOT TAM','NOT SAM','NOT SOM','NOT TDL REVENUE','NOT EXECUTED PAYMENT TOTAL']))
existing = {f'TDL-CAP-{n:03d}' for n in [1,2,3,4,9,10,11,12,16,18,19]}
current = set(re.findall(r'^\| (TDL-CAP-\d{3}) \| [^\n]+ \| EXISTING \|', capregister, re.M))
check('Only 11 authoritative EXISTING capabilities mapped, states unchanged by review',
      current == existing and set(re.findall(r'^\| (TDL-CAP-\d{3}) \|', gate, re.M)) == existing
      and all(set(re.findall(r'TDL-CAP-\d{3}', r['TDL_fit'])) <= existing for r in ready))
gids = {f'GAP-{n:03d}' for n in range(1,5)}
check('4 original potential gaps accounted for',
      set(re.findall(r'^\| (GAP-\d{3}) ', gate, re.M)) == gids and gids <= set(re.findall(r'GAP-\d{3}', gaps)))
levels = {str(n): sum(r['evidence_level'] == f'LEVEL_{n}' for r in ready) for n in range(7)}
check('No levels 5/6; no forced level 4', levels == {'0':0,'1':1,'2':2,'3':7,'4':0,'5':0,'6':0}, levels)
candidates = {k:[r['problem_id'] for r in ready if r['commercial_validation_candidate']==k]
              for k in ['YES','HOLD','NO']}
check('Candidate conditions and exhaustive YES/HOLD/NO',
      candidates == {'YES':['PROB-001'], 'HOLD':['PROB-002','PROB-005','PROB-006','PROB-007','PROB-008','PROB-009'],
                     'NO':['PROB-003','PROB-004','PROB-010']} and
      all(r['observed_evidence'].startswith('MKT-EVD-') and r['affected_actor'] and
          not r['TDL_fit'].startswith('NO_CURRENT_FIT') and r['key_uncertainty']
          for r in ready if r['commercial_validation_candidate']=='YES'), candidates)
check('Fit and differentiation controlled enums',
      all(r['TDL_fit'].split(':')[0] in ['DIRECT_FIT','PARTIAL_FIT','NO_CURRENT_FIT','UNKNOWN']
          and r['differentiation_status']=='UNPROVEN' for r in ready))
asm = {f'BUS-ASM-{n:03d}':('PARTIALLY_SUPPORTED' if n<=3 else 'UNTESTED') for n in range(1,9)}
review = assumptions.split('## Revisión de readiness')[1]
check('8 assumptions retain authoritative status and proposed change NONE',
      all(f'| {i} | {state} |' in review for i,state in asm.items()) and
      'PROPOSED_STATUS_CHANGE = NONE' in review and
      len(re.findall(r'^\| BUS-ASM-\d{3} \|',review,re.M))==8)
check('Plan contains required 12 sections and five candidate definitions',
      len(re.findall(r'^## \d+\.',docs['MARKET_VALIDATION_PLAN.md'],re.M))==12 and
      all(x in docs['MARKET_VALIDATION_PLAN.md'] for x in ['WHAT_WE_KNOW','WHAT_WE_DO_NOT_KNOW',
       'WHAT_MUST_BE_TESTED','WHO_CAN_VALIDATE_IT','WHAT_EVIDENCE_WOULD_CHANGE_OUR_DECISION']))
check('All seven evidence definitions and seven evidence types',
      all(x in docs['COMMERCIAL_VALIDATION_EVIDENCE_MODEL.md'] for x in [
       'INTERVIEW_EVIDENCE','WORKFLOW_EVIDENCE','PILOT_EVIDENCE','PROCUREMENT_EVIDENCE',
       'WILLINGNESS_TO_PAY_EVIDENCE','SIGNED_PILOT','PAID_PILOT']) and
      all(x in gate for x in ['OBSERVED_PROBLEM','PROCUREMENT_NEED','REGULATORY_DRIVER',
       'STANDARD_REQUIREMENT','PROVIDER_CLAIM','FREE_ALTERNATIVE','INFERENCE']))
check('No affirmative commercial validation or WTP/market claims',
      not re.search(r'(?:MARKET_VALIDATED|DEMAND_VALIDATED|WILLINGNESS_TO_PAY|BUSINESS_MODEL_VALIDATED)\s*=\s*YES',
                    '\n'.join(docs.values())) and
      'MARKET_VALIDATED = NO' in gate and 'DEMAND_VALIDATED = NO' in gate)
check('Phase 3 ongoing, baseline FROZEN, Phase 4 not started',
      'STATUS: IN PROGRESS' in status and 'BUSINESS_CAPABILITY_BASELINE_V1 = FROZEN' in status
      and 'Phase 4 **NOT STARTED**' in status and 'Estado: **FROZEN**' in baseline)
check('Historical prior verification retained, not rerun', historic['verification']=='PASS')
check('Resource thresholds and hash prohibition documented', all(x in docs['RESOURCE_USAGE_POLICY.md']
      for x in ['FULL REPOSITORY HASHING IS PROHIBITED BY DEFAULT','20.000','5 GB','cinco minutos','STOP']))
local_links = []
for name,text in docs.items():
    if name.endswith('.md'):
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' not in target:
                target = target.split('#')[0]
                if target and not target.startswith('readiness_review/'):
                    local_links.append((name,target,(market/target).is_file()))
check('Local document links exist (verification outputs checked after write)',
      all(t[2] for t in local_links))
git_results = {}
for key,args in [('status',['status','--short','--untracked-files=normal']),
                 ('diff_names',['diff','--name-only'])]:
    p = subprocess.run(['git',*args],cwd=root,capture_output=True,text=True,encoding='utf-8')
    git_results[key] = dict(exit_code=p.returncode,output=p.stdout,stderr=p.stderr)
    check('Git '+key+' completed',p.returncode==0)

ok = all(c['passed'] for c in checks)
result = dict(result='PASS' if ok else 'FAIL',date=datetime.now(timezone.utc).isoformat(),
              checks=checks,levels=levels,candidates=candidates,
              resource_guard_triggered='NO',new_external_research='NO',repository_wide_hash='NO',
              measured_verifier_unique_files_read=len(reads),measured_verifier_bytes_read=sum(reads.values()),
              session_files_enumerated=None,session_bytes_read=None,session_elapsed_seconds=None,
              verifier_elapsed_seconds=round(time.monotonic()-started,3),git=git_results,
              scope_limit='Explicit Business write paths; no repeat of prior scope verification. '
              'Grouped untracked Git and historic manifests cannot certify global current immutability.',
              source_reads=reads)
(out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'exit_code.txt').write_text('0\n' if ok else '1\n',encoding='utf-8')
summary=f"{result['result']}: {sum(c['passed'] for c in checks)}/{len(checks)} targeted documentary checks\n"
(out/'verification_stdout.txt').write_text(summary,encoding='utf-8')
# Hash only exact files created/modified in this review, never input/source trees.
modified = [market/n for n in required] + [business/'BUSINESS_STATUS.md',
            business/'01_Governance/ASSUMPTIONS_REGISTER.md',business/'01_Governance/DECISION_LOG.md',
            Path(__file__).resolve(),out/'verification.json',out/'exit_code.txt',out/'verification_stdout.txt']
with (out/'modified_file_hashes.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['path','bytes','sha256'])
    for p in modified:
        if not p.resolve().is_relative_to(business): raise RuntimeError('Hash outside write scope')
        data=p.read_bytes(); w.writerow([p.relative_to(root).as_posix(),len(data),hashlib.sha256(data).hexdigest()])
print(summary,end='')
for c in checks:
    if not c['passed']: print('FAIL:',c['name'],c['detail'])
raise SystemExit(0 if ok else 1)
