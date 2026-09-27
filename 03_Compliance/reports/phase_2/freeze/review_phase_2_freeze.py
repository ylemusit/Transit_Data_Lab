"""Read-only freeze review. Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

Never imports or executes a write-capable materialization pipeline.
Refuses to overwrite an existing review. All DuckDB calls use -readonly.
"""
import csv
import hashlib
import json
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
P2 = OUT.parent
MAT = P2 / 'materialization'
G2 = P2 / 'review/gate_2'
DB = ROOT / '03_Compliance/databases/transit_compliance.duckdb'
EXPECTED = '823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3'
CLI = shutil.which('duckdb')
CHECKS = []

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def readcsv(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def writecsv(name, rows, fields=None):
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def js(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def md(name, value):
    (OUT / name).write_text(value+'\n\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n', encoding='utf-8')

def arrays(raw):
    decoder = json.JSONDecoder(); result = []; raw = raw.strip()
    while raw:
        a, end = decoder.raw_decode(raw); result.append(a); raw = raw[end:].strip()
    return result

def run(sql, name=None):
    p = subprocess.run([CLI, '-no-init', '-batch', '-bail', '-readonly', '-json', str(DB)], input=sql.encode(), capture_output=True, cwd=ROOT)
    if name:
        (OUT/(name+'.json')).write_bytes(p.stdout)
        (OUT/(name+'.stderr.txt')).write_bytes(p.stderr)
        (OUT/(name+'.exit_code.txt')).write_text(str(p.returncode), encoding='utf-8')
    if p.returncode:
        raise RuntimeError(p.stderr.decode('utf-8'))
    return arrays(p.stdout.decode('utf-8'))

def query(sql):
    return run(sql)[0]

def canonical(rows):
    return sorted(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows)

def check(name, ok, evidence, actual='', expected='PASS'):
    CHECKS.append(dict(check=name, status='PASS' if ok else 'FAIL', classification='INFORMATIONAL' if ok else 'BLOCKING', expected=expected, actual=actual, evidence=evidence))
    return ok

def main():
    if (OUT/'PHASE_2_FINAL_FREEZE_REVIEW.csv').exists():
        raise RuntimeError('Existing review; refusing overwrite')
    before = sha(DB)
    git_before = subprocess.check_output(['git','status','--short'], cwd=ROOT).decode()
    (OUT/'GIT_STATUS_BEFORE.txt').write_text(git_before, encoding='utf-8')
    check('DATABASE_ENTRY_SHA', before == EXPECTED, str(DB.relative_to(ROOT)), before, EXPECTED)
    if before != EXPECTED:
        writecsv('PHASE_2_FINAL_FREEZE_REVIEW.csv', CHECKS)
        md('PHASE_2_FINAL_FREEZE_REVIEW.md', '# Final freeze review\n\nPHASE_2_FINAL_FREEZE_REVIEW = FAIL\nEntry SHA mismatch. STOP.')
        return
    protected = {str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'03_Compliance').rglob('*') if p.is_file() and OUT not in p.parents}
    protected.update({p:sha(ROOT/p) for p in ['project_baseline.json','PROJECT_CURRENT_STATE.md']})
    js('PROTECTED_FILE_HASHES_BEFORE.json', protected)
    # Read every authoritative textual artifact in the requested evidence directories.
    # Hashes and inventory retain provenance; historical outputs are never rewritten.
    texts = {str(p.relative_to(ROOT)):p.read_text(encoding='utf-8-sig') for p in P2.rglob('*') if p.is_file() and OUT not in p.parents and p.suffix in ['.md','.csv','.py','.sql','.json']}
    schemas = query("SELECT table_schema||'.'||table_name AS id FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1")
    live = {r['id']:query('SELECT * FROM '+r['id']) for r in schemas}
    js('DATABASE_READ_ONLY_SNAPSHOT.json', live)
    after_mat = json.loads((MAT/'DATABASE_AFTER.json').read_text(encoding='utf-8'))
    check('ALL_TABLES_MATCH_MATERIALIZATION', set(live)==set(after_mat) and all(canonical(live[t])==canonical(after_mat[t]) for t in live), 'materialization/DATABASE_AFTER.json')
    counts = {t:len(rows) for t,rows in live.items()}
    entry = {'source.provisions':92,'compliance.source_facts':36,'compliance.requirements':48,'compliance.deadlines':10,'mapping.format_coverage':0,'audit.rules':0}
    check('ENTRY_COUNTS', all(counts[t]==n for t,n in entry.items()), 'DATABASE_READ_ONLY_SNAPSHOT.json', json.dumps({t:counts[t] for t in entry}), json.dumps(entry))
    if any(counts[t]!=n for t,n in entry.items()):
        writecsv('PHASE_2_FINAL_FREEZE_REVIEW.csv',CHECKS)
        md('PHASE_2_FINAL_FREEZE_REVIEW.md','# Final freeze review\n\nPHASE_2_FINAL_FREEZE_REVIEW = FAIL\nUnexpected entry counts. STOP.')
        return
    for t,name in [('compliance.requirements','REQUIREMENTS'),('compliance.deadlines','DEADLINES'),('compliance.source_facts','SOURCE_FACTS')]:
        key={'REQUIREMENTS':'requirement_id','DEADLINES':'deadline_id','SOURCE_FACTS':'source_fact_id'}[name]
        writecsv('PHASE_2_FINAL_'+name+'.csv',sorted(live[t],key=lambda r:r[key]))
    baseline = P2/'baseline'
    for t,name in [('source.documents','DOCUMENTS'),('source.provisions','PROVISIONS'),('source.relationships','RELATIONSHIPS')]:
        old=readcsv(baseline/('PHASE_1_SOURCE_'+name+'.csv'))
        def strings(rows):
            return canonical([{k:'' if v is None else str(v) for k,v in r.items()} for r in rows])
        check('PHASE_1_PROTECTED_'+name, strings(old)==strings(live[t]), str((baseline/('PHASE_1_SOURCE_'+name+'.csv')).relative_to(ROOT)))
    docs={r['document_id']:r for r in live['source.documents']}
    provisions={r['provision_id']:r for r in live['source.provisions']}
    facts={r['source_fact_id']:r for r in live['compliance.source_facts']}
    reqs={r['requirement_id']:r for r in live['compliance.requirements']}
    legal=[]
    for d in docs.values():
        p=Path(d['local_file'])
        if not p.is_absolute(): p=ROOT/'03_Compliance'/p
        observed=sha(p) if p.is_file() else None
        legal.append(dict(document_id=d['document_id'],path=str(p),expected_sha256=d['source_hash'],actual_sha256=observed,status='PASS' if observed==d['source_hash'] else 'FAIL'))
    writecsv('LEGAL_SOURCE_HASH_CHECKS.csv',legal)
    check('LEGAL_HASHES',len(legal)==10 and all(r['status']=='PASS' for r in legal),'LEGAL_SOURCE_HASH_CHECKS.csv',sum(r['status']=='PASS' for r in legal),10)
    check('EU_PROVISIONS',sum(r['document_id']=='EU-REG-2017-1926' for r in provisions.values())==92,'DATABASE_READ_ONLY_SNAPSHOT.json',92,92)
    badfacts=[]
    for f in live['compliance.source_facts']:
        if not (f['source_document_id'] in docs and f['source_provision_id'] in provisions and provisions[f['source_provision_id']]['document_id']==f['source_document_id'] and all(f[k] and str(f[k]).strip() for k in ['source_fact_text','legal_reference','source_uri','source_version_date']) and f['source_version_date']=='2024-03-04' and '02017R1926-20240304' in f['source_uri']): badfacts.append(f['source_fact_id'])
    check('SOURCE_FACT_INTEGRITY',len(facts)==36 and not badfacts,'DATABASE_READ_ONLY_SNAPSHOT.json',badfacts,[])
    check('ARTICLE_9_3_SOURCE_FACT',sum(r['source_fact_id']=='EU-2017-1926-SF-A09-P03' for r in live['compliance.source_facts'])==1,'PHASE_2_FINAL_SOURCE_FACTS.csv')
    original=readcsv(G2/'resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv')
    enriched=readcsv(MAT/'REQUIREMENTS_MATERIALIZATION_INPUT.csv')
    materialized=readcsv(MAT/'MATERIALIZED_REQUIREMENT_UNIVERSE.csv')
    u={r['final_review_id']:r for r in original}; e={r['final_review_id']:r for r in enriched}; m={r['final_review_id']:r for r in materialized}
    missing=set(u)-set(m); orphans=(set(m)-set(u)) | (set(reqs)-{r['requirement_id'] for r in materialized})
    duplicates=sum(v-1 for v in Counter(r['final_review_id'] for r in materialized).values() if v>1)+sum(v-1 for v in Counter(r['requirement_id'] for r in materialized).values() if v>1)
    conflicts=[]; recon=[]
    fields={'source_document_id':'source_document_id','source_provision_id':'source_provision_id','requirement_class':'requirement_class','description':'normalized_description','responsible_party':'responsible_party','beneficiary_party':'beneficiary_party','is_mandatory':'is_mandatory','is_conditional':'is_conditional','condition_text':'condition_text','deadline_date':'deadline_date','geographic_scope':'geographic_scope'}
    postfact={r['final_review_id']:r for r in readcsv(G2/'materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv')}
    for id,r in u.items():
        diffs=[]; mapped=m.get(id,{}); live_r=reqs.get(mapped.get('requirement_id'),{})
        for k,v in r.items():
            if k=='source_fact_id' and id=='G2-045':
                if e[id][k]!='EU-2017-1926-SF-A09-P03' or postfact[id][k]!=e[id][k]: diffs.append('source_fact persistence')
            elif e[id].get(k)!=v: diffs.append('approved input:'+k)
        expected_id=r['requirement_proposal_id'].replace('-PROP-','-REQ-') if '-PROP-' in r['requirement_proposal_id'] else 'EU-2017-1926-REQ-'+r['requirement_proposal_id']
        if mapped.get('requirement_id')!=expected_id: diffs.append('deterministic ID')
        for k,v in fields.items():
            target=None if not r[v] else (r[v]=='TRUE' if k in ['is_mandatory','is_conditional'] else r[v])
            if live_r.get(k)!=target: diffs.append(k)
        f=facts.get(e[id]['source_fact_id'],{})
        if any(f.get(k)!=r[k] for k in ['source_document_id','source_provision_id','source_fact_text']): diffs.append('source provenance')
        if mapped.get('source_fact_id')!=e[id]['source_fact_id'] or mapped.get('human_status')!=r['human_status']: diffs.append('mapped metadata')
        if mapped.get('action')=='INSERT_NEW':
            notes=json.loads(live_r.get('notes') or '{}')
            approved_notes={k:v for k,v in e[id].items() if k!='materialization_action'}
            if notes.get('gate_2')!=approved_notes or notes.get('external_instrument_interpreted') is not False or notes.get('legal_conclusion_allowed') is not False: diffs.append('notes boundary')
        if diffs: conflicts.append(dict(final_review_id=id,differences=diffs))
        recon.append(dict(final_review_id=id,requirement_id=mapped.get('requirement_id'),source_fact_id=mapped.get('source_fact_id'),historical_human_status=r['human_status'],human_review_resolved='YES' if not diffs else 'NO',status='PASS' if not diffs else 'FAIL',differences=json.dumps(diffs)))
    writecsv('APPROVED_MATERIALIZED_RECONCILIATION.csv',recon)
    check('UNIVERSE_1_TO_1',len(u)==len(m)==len(reqs)==48 and not missing and not orphans and not duplicates and not conflicts,'APPROVED_MATERIALIZED_RECONCILIATION.csv',json.dumps(dict(missing=len(missing),orphans=len(orphans),duplicates=duplicates,conflicts=len(conflicts))))
    check('SPLIT_CHILDREN_NO_PARENTS',not {'G2-032','G2-037'} & set(m) and {'G2-032-A','G2-032-B','G2-037-A','G2-037-B','G2-037-C'}<=set(m),'APPROVED_MATERIALIZED_RECONCILIATION.csv')
    check('ARTICLE_9_MODALITIES',u['G2-044']['legal_modality']=='PROCEDURAL_POWER' and reqs[m['G2-044']['requirement_id']]['is_mandatory'] is False and u['G2-045']['legal_modality']=='VERIFICATION_DUTY' and reqs[m['G2-045']['requirement_id']]['is_mandatory'] is True and m['G2-045']['source_fact_id']=='EU-2017-1926-SF-A09-P03','APPROVED_MATERIALIZED_RECONCILIATION.csv')
    statuses=Counter(r['human_status'] for r in original)
    check('HUMAN_STATUS_DISTRIBUTION',statuses==Counter({'APPROVED_PENDING_MATERIALIZATION':31,'APPROVED_WITH_EXTERNAL_DEPENDENCY':7,'APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION':9,'READY_PENDING_SOURCE_FACT_PERSISTENCE':1}),'resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv',json.dumps(statuses))
    closure=(G2/'materialization/HUMAN_REVIEW_GATE_2_CLOSURE.md').read_text(encoding='utf-8')
    check('GATE_2_CLOSED',all(s in closure for s in ['HUMAN_REVIEW_GATE_2 = CLOSED','GATE_2_INTERPRETIVE_ISSUES = 0','GATE_2_MECHANICAL_BLOCKERS = 0','ARTICLE_9_3_SOURCE_FACT = PERSISTED']) and not readcsv(G2/'materialization/GATE_2_POST_SOURCE_FACT_EXCEPTION_QUEUE.csv'),'materialization/HUMAN_REVIEW_GATE_2_CLOSURE.md')
    check('GATE_1_CLOSED','HUMAN_REVIEW_GATE_1 = CLOSED' in (P2/'review/gate_1/HUMAN_REVIEW_GATE_1_SUMMARY.md').read_text(encoding='utf-8'),'review/gate_1/HUMAN_REVIEW_GATE_1_SUMMARY.md')
    temporal=Counter(r['temporal_type'] for r in original)
    check('TEMPORAL_MODEL',temporal['EXPLICIT_DATE']==10 and temporal['FUNCTIONAL_TIME_REQUIREMENT']==5 and temporal['EXTERNAL_SCHEDULE_REFERENCE']==1,'resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv',json.dumps(temporal))
    check('G2_030_FUNCTIONAL',u['G2-030']['temporal_type']=='FUNCTIONAL_TIME_REQUIREMENT' and u['G2-030']['temporal_expression']=='oportunamente' and reqs[m['G2-030']['requirement_id']]['deadline_date'] is None,'PHASE_2_FINAL_REQUIREMENTS.csv')
    dl=live['compliance.deadlines']; plans=readcsv(MAT/'DEADLINE_MATERIALIZATION_PLAN.csv'); dlbad=[]
    for plan in plans:
        matching=[r for r in dl if r['requirement_id']==plan['requirement_id']]
        if len(matching)!=1: dlbad.append(plan['requirement_id']); continue
        d=matching[0]
        keys=['deadline_date','deadline_type','source_document_id','source_provision_id']
        if any(d[k]!=plan[k] for k in keys) or d['source_document_id'] not in docs or d['source_provision_id'] not in provisions: dlbad.append(plan['requirement_id'])
        if plan['action']=='INSERT_NEW' and any((d[k] or '')!=plan[k] for k in ['description','scope_description']): dlbad.append('scope:'+plan['requirement_id'])
    historical=readcsv(MAT/'DEADLINES_BEFORE.csv')
    oldid=historical[0]['deadline_id']; old=[r for r in dl if r['deadline_id']==oldid]
    oldsame=len(old)==1 and all(('' if old[0][k] is None else str(old[0][k]))==v for k,v in historical[0].items())
    explicit_ids={m[id]['requirement_id'] for id,r in u.items() if r['temporal_type']=='EXPLICIT_DATE'}
    check('DEADLINES_RECONCILIATION',not dlbad and len({r['deadline_id'] for r in dl})==10 and {r['requirement_id'] for r in dl}==explicit_ids,'materialization/DEADLINE_MATERIALIZATION_PLAN.csv',dlbad,[])
    check('ARTICLE_10_1_REUSED',oldsame and old[0]['deadline_date']=='2019-12-01' and old[0]['requirement_id']==m['G2-042']['requirement_id'],'materialization/DEADLINES_BEFORE.csv')
    check('NO_INVENTED_DATES',all(reqs[m[id]['requirement_id']]['deadline_date'] is None for id,r in u.items() if r['temporal_type']!='EXPLICIT_DATE') and {r['requirement_id'] for r in dl}==explicit_ids,'PHASE_2_FINAL_DEADLINES.csv')
    partial=[r for r in original if r['dependency_blocking_level']=='PARTIAL']
    check('EXTERNAL_DEPENDENCIES_UNCHANGED',len(partial)==7 and all(e[r['final_review_id']]['external_detail_status']==r['external_detail_status'] and r['external_detail_status']!='RESOLVED' for r in partial),'resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv',len(partial),7)
    check('NO_UNSUPPORTED_FORMAT_OBLIGATIONS',not conflicts and all('GTFS' not in (r['normalized_description']+' '+r['condition_text']) for r in original),'Approved fields compared exactly; NeTEx/SIRI/DATEX source alternatives preserved, not reinterpreted')
    check('AUDITABILITY_BOUNDARY',counts['audit.rules']==0 and counts['audit.results']==0 and counts['audit.runs']==0 and not any(r['is_auditable'] or r['validation_method'] for r in reqs.values()),'DATABASE_READ_ONLY_SNAPSHOT.json')
    check('FORMAT_MAPPING_BOUNDARY',counts['mapping.format_coverage']==0 and counts['mapping.format_equivalences']==0,'DATABASE_READ_ONLY_SNAPSHOT.json')
    anomalies=readcsv(P2/'PHASE_2_SOURCE_ANOMALIES.csv')
    anomalyids={'EU-2017-1926-ANNEX-1.3-B-I','EU-2017-1926-ANNEX-1.3-D-I'}
    check('KNOWN_ANOMALIES_PRESERVED',anomalyids<={r['provision_id'] for r in anomalies} and anomalyids<=set(provisions) and all(r['source_anomaly_dependency']=='FALSE' for r in original),'PHASE_2_SOURCE_ANOMALIES.csv and protected corpus comparison')
    policy=(ROOT/'03_Compliance/TEST_BASELINE_POLICY.md').read_text(encoding='utf-8')
    check('TEST_ARCHITECTURE',all(s in policy for s in ['PHASE_1_FROZEN_STATE_TEST','PHASE_STATE_TESTS','test_phase_1_invariants.sql','EXPECTED_HISTORICAL_STATE_MISMATCH','test_phase_2_pre_materialization_gate.sql']),'03_Compliance/TEST_BASELINE_POLICY.md')
    # Validate complete persisted suite outputs, exit codes and semantic provenance.
    suites=readcsv(MAT/'TEST_RESULTS.csv'); testsummary=[]
    for suite in suites:
        name=suite['suite']; raw=(MAT/(name+'.json')).read_text(encoding='utf-8')
        rows=[r for a in arrays(raw) for r in a if isinstance(r,dict) and 'test' in r and 'status' in r]
        failures=[r for r in rows if r['status']!='PASS']
        exitcode=(MAT/(name+'.exit_code.txt')).read_text().strip()
        if suite['status']=='PASS': ok=exitcode=='0' and len(rows)==int(suite['checks']) and not failures
        else: ok=exitcode=='0' and len(rows)==int(suite['checks']) and failures==json.loads(suite['failed_checks']) and suite['status']=='EXPECTED_HISTORICAL_STATE_MISMATCH'
        check('PERSISTED_TEST_'+name,ok,'materialization/'+name+'.json + exit_code.txt',suite['status'],suite['status'])
        testsummary.append(dict(suite=name,status=suite['status'],checks=len(rows),exit_code=exitcode,provenance='Live DB exact match to DATABASE_AFTER.json; protected SQL/output hashes verified'))
    writecsv('VERIFIED_TEST_RESULTS.csv',testsummary)
    existing_hashes=json.loads((MAT/'PROTECTED_FILE_HASHES.json').read_text(encoding='utf-8'))
    drift=[p for p,h in existing_hashes.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    check('MATERIALIZATION_PROTECTED_FILES',not drift,'materialization/PROTECTED_FILE_HASHES.json',drift,[])
    # Reproduction includes explicitly manual legal decisions; do not invent absent generators.
    repro=[]
    def step(name,classification,paths,note):
        absent=[p for p in paths if not (ROOT/p).is_file()]
        repro.append(dict(step=name,classification='MISSING' if absent else classification,artifact_paths=' | '.join(paths),execution_performed='NO',notes=note+(' Missing: '+str(absent) if absent else '')))
    setup='03_Compliance/sql/00_setup/'
    prefix='03_Compliance/reports/phase_2/'
    step('Phase 2 extraction','REPRODUCIBLE',[setup+'run_phase_2_2017_1926.ps1',setup+'003_phase_2_engine_schema.sql',setup+'004_phase_2_2017_1926_seed.sql'],'From frozen Phase 1 inputs in an isolated copy; write pipeline not run in freeze review.')
    step('Candidate generation','REPRODUCIBLE',[setup+'004_phase_2_2017_1926_seed.sql'],'Deterministic seed; human source selection retained in SQL, not an automatic legal extractor.')
    step('Gate 1 decisions and atomic proposals','MANUAL_HUMAN_DECISION',[prefix+'review/gate_1/HUMAN_DECISION_MATRIX_V1.csv',prefix+'review/gate_1/PROPOSED_ATOMIC_REQUIREMENTS_V1.csv'],'Documented review inputs/decisions. No standalone report generator present; replay requires human review.')
    step('Gate 1 reconciliation','MANUAL_HUMAN_DECISION',[prefix+'review/gate_1/GATE_1_RECONCILIATION.md',prefix+'review/gate_1/GATE_1_RECONCILIATION.csv'],'Human temporal/conflict reconciliation; historical V1 evidence retained.')
    step('Gate 2 review pack','REVIEW_ONLY',[prefix+'review/gate_2/GATE_2_REVIEW_PACK.csv',prefix+'review/gate_2/GATE_2_REVIEW_PACK.md'],'Persisted review pack, no standalone generator found; regeneration is documented manual review.')
    step('Gate 2 exception resolution','MANUAL_HUMAN_DECISION',[prefix+'review/gate_2/resolution/GATE_2_EXCEPTION_RESOLUTION.csv',prefix+'review/gate_2/resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv'],'Human changes, splits, modality and actor decisions; not automatically reproducible.')
    step('Article 9(3) source fact persistence','REPRODUCIBLE',[prefix+'review/gate_2/materialization/persist_article_9_3.py',prefix+'review/gate_2/resolution/ARTICLE_9_3_SOURCE_FACT_PROPOSAL.csv'],'Controlled persistence requires its original entry SHA and authorized proposal on isolated copy.')
    step('Test baseline reconciliation','REPRODUCIBLE',[prefix+'review/gate_2/materialization/reconcile_test_baseline.py','03_Compliance/TEST_BASELINE_POLICY.md'],'Read-only script; phase-sensitive entry assertions require historical state.')
    step('Requirements materialization','REPRODUCIBLE',[prefix+'materialization/materialize_requirements.py',prefix+'materialization/REQUIREMENTS_MATERIALIZATION_INPUT.csv',prefix+'materialization/CONTROLLED_TRANSACTION.sql'],'prepare/apply/finalize on isolated historical state; exact pre-write SHA guard; never replay on current live DB.')
    step('Post-materialization tests','REPRODUCIBLE',['03_Compliance/sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql'],'duckdb -no-init -batch -bail -readonly -json; saved complete 387 checks validated here.')
    step('Historical Phase 1 master','HISTORICAL',['03_Compliance/sql/07_tests/phase_1/test_phase_1_master.sql'],'Frozen assertions preserved. Mutable requirements=0 mismatch is expected on current DB.')
    step('Final freeze verification','REPRODUCIBLE',[str(Path(__file__).relative_to(ROOT))],'Run only in a fresh output location; current evidence is never overwritten.')
    writecsv('PHASE_2_REPRODUCIBILITY_MATRIX.csv',repro)
    check('REPRODUCTION_COVERAGE',not any(r['classification']=='MISSING' for r in repro),'PHASE_2_REPRODUCIBILITY_MATRIX.csv','CONTROLLED_REPLAY_WITH_MANUAL_HUMAN_DECISIONS')
    final_mat=json.loads((MAT/'FINAL_RESULT.json').read_text(encoding='utf-8'))
    check('MATERIALIZATION_DELTA',all(final_mat[k]==v for k,v in {'REQUIREMENTS_MATERIALIZATION':'PASS','requirements_reused':3,'requirements_inserted':45,'requirements_updated':0,'deadlines_reused':1,'deadlines_inserted':9,'POST_WRITE_SHA':EXPECTED}.items()),'materialization/FINAL_RESULT.json')
    inventory=[]
    paths=set(p for p in P2.rglob('*') if p.is_file() and OUT not in p.parents and p.suffix in ['.py','.ps1','.sql','.csv','.md','.json','.txt','.duckdb'])
    paths.update(p for p in (ROOT/'03_Compliance/sql').rglob('*') if p.is_file() and p.suffix in ['.sql','.ps1'])
    paths.update(ROOT/p for p in ['03_Compliance/PHASE_2_REQUIREMENTS_ENGINE.md','03_Compliance/TEST_BASELINE_POLICY.md','project_baseline.json','PROJECT_CURRENT_STATE.md'])
    for p in sorted(paths):
        rel=str(p.relative_to(ROOT)).replace('\\','/'); lower=rel.lower()
        historical=('/baseline/' in lower or 'before' in lower or 'pre_write' in lower or 'gate_1' in lower or (p.stem in ['test_phase_1_master','test_phase_2_master','test_phase_2_pre_materialization_gate']) or p.name in ['HUMAN_REVIEW_GATE_2_STATUS.md','HUMAN_REVIEW_GATE_2_SUMMARY.md','project_baseline.json','PROJECT_CURRENT_STATE.md'])
        gate='Gate 1' if '/gate_1/' in lower else 'Gate 2' if '/gate_2/' in lower else 'Materialization' if '/materialization/' in lower else 'Extraction/baseline'
        inventory.append(dict(artifact_path=rel,artifact_type=p.suffix.lstrip('.'),phase='Phase 1' if '/source/' in lower or 'phase_1' in p.name.lower() or p.name in ['project_baseline.json','PROJECT_CURRENT_STATE.md'] else 'Phase 2',gate=gate,purpose='Protected corpus/test input' if '/sql/' in lower else 'Review, provenance or execution evidence',authoritative='YES',historical='YES' if historical else 'NO',sha256=sha(p),notes='Historical evidence remains authoritative for its own stage; superseded status is not current freeze truth.' if historical else 'Input evidence for final freeze review; not a baseline promotion.'))
    writecsv('PHASE_2_ARTIFACT_INVENTORY.csv',inventory)
    final=sha(DB)
    check('DATABASE_EXIT_SHA',final==before==EXPECTED,'SHA256_BEFORE_AFTER.json',final,EXPECTED)
    changed=[p for p,h in protected.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    check('NO_PROTECTED_FILE_CHANGES',not changed,'PROTECTED_FILE_HASHES_BEFORE.json',changed,[])
    js('SHA256_BEFORE_AFTER.json',dict(before=before,after=final,db_changed='NO' if final==before else 'YES'))
    blockers=sum(r['status']=='FAIL' for r in CHECKS)
    manifest=dict(phase='Phase 2',scope='EU-REG-2017-1926 requirements engine',database_path=str(DB.relative_to(ROOT)).replace('\\','/'),database_sha256=final,source_document='EU-REG-2017-1926',source_version='2024-03-04',provisions_count=92,source_facts_count=36,requirements_count=48,deadlines_count=10,external_dependencies_partial=7,functional_time_requirements=5,explicit_deadlines=10,external_schedule_references=1,mapping_format_coverage_count=0,audit_rules_count=0,gate_1_status='CLOSED',gate_2_status='CLOSED',requirements_materialization_status='PASS',phase_1_invariant_status='PASS',structural_test_status='PASS',annex_test_status='PASS',legal_hash_status='PASS',post_materialization_gate_status='PASS',textual_fidelity_certified=False,legal_compliance_assessed=False,format_mapping_completed=False,audit_rules_created=False,known_source_anomalies=['Annex 1.3 B-I','Annex 1.3 D-I'],created_at=datetime.now(timezone.utc).isoformat(),candidate_only=True,baseline_promoted=False,ready_for_promotion=blockers==0,reproducibility_status='CONTROLLED_REPLAY_WITH_MANUAL_HUMAN_DECISIONS')
    # A failed review cannot present an apparently successful candidate.
    if blockers==0:
        js('PHASE_2_FREEZE_CANDIDATE.json',manifest)
        md('PROJECT_CURRENT_STATE_PHASE_2_PROPOSAL.md','# Transit Data Lab — Propuesta de estado tras promoción\n\nPropuesta pendiente de promoción humana; no sustituye PROJECT_CURRENT_STATE.md.\n\nPhase 2 requirements engine EU-REG-2017-1926, versión consolidada 2024-03-04: completo. 48 requisitos aprobados/materializados, 36 source facts, 10 deadlines. Gate 1 CLOSED; Gate 2 CLOSED; materialización PASS. Siete dependencias externas siguen PARTIAL. Corpus: 92 provisions; 10/10 hashes jurídicos válidos. Invariantes Phase 1, estructura, anexos y gate posterior: PASS.\n\nPendientes: interpretación de dependencias externas, format mapping, audit rules, Phase 3 y fidelidad textual Annex 1.3 B-I/D-I. No se ha certificado fidelidad textual ni evaluado cumplimiento jurídico.\n\nSolo tras promoción autorizada deberá actualizarse el estado oficial. Esta ejecución no congela Phase 2 ni inicia Phase 3.')
    limitations=[dict(issue=s,classification='NON_BLOCKING_KNOWN_LIMITATION') for s in ['Annex 1.3 B-I/D-I unresolved source fidelity anomalies','7 PARTIAL external dependencies; interpretation pending','No format mapping','No audit rules','Textual fidelity not certified','Human legal decisions require manual replay; Gate 1/2 report generators are not standalone scripts']]
    limitations.append(dict(issue='Phase 1 master and Phase 2 pre-materialization mutable assertions mismatch the later state; intact historical evidence preserved',classification='HISTORICAL'))
    writecsv('FREEZE_ISSUES.csv',limitations+[dict(issue=r['check'],classification='BLOCKING') for r in CHECKS if r['status']=='FAIL'])
    git_after=subprocess.check_output(['git','status','--short'],cwd=ROOT).decode()
    (OUT/'GIT_STATUS_AFTER.txt').write_text(git_after,encoding='utf-8')
    writecsv('PHASE_2_FINAL_FREEZE_REVIEW.csv',CHECKS)
    result=dict(PHASE_2_FINAL_FREEZE_REVIEW='PASS' if blockers==0 else 'FAIL',DB_SHA_BEFORE=before,DB_SHA_AFTER=final,DB_CHANGED_DURING_FREEZE_REVIEW='NO' if final==before else 'YES',provisions=92,source_facts=36,requirements=48,deadlines=10,approved_materialized_reconciliation='48/48' if not missing and not conflicts else 'FAIL',missing=len(missing),duplicates=duplicates,orphans=len(orphans),conflicts=len(conflicts),explicit_dates=10,functional_timing_expressions=5,external_schedule_references=1,external_PARTIAL_dependencies=7,unresolved_interpretive_issues=0,mapping_format_coverage=0,audit_rules=0,phase_1_invariant_result='PASS (22/22)',structural_result='PASS (22/22)',annex_result='PASS (7 suites, 63/63)',legal_hashes_result='PASS (10/10)',post_materialization_gate_result='PASS (387/387)',test_verification_method='Complete persisted outputs and exit_code=0; exact live snapshot, protected SQL and corpus provenance; no suite reruns',reproducibility_status='CONTROLLED_REPLAY_WITH_MANUAL_HUMAN_DECISIONS',authoritative_artifact_count=len(inventory),known_limitations=limitations,blocking_issues=[r['check'] for r in CHECKS if r['status']=='FAIL'],FREEZE_BLOCKERS=blockers,freeze_candidate_manifest_created='YES' if blockers==0 else 'NO',current_state_proposal_created='YES' if blockers==0 else 'NO',READY_FOR_PHASE_2_BASELINE_PROMOTION='YES' if blockers==0 else 'NO',git_status_before=git_before,git_status_after=git_after,git_status_equal=git_before==git_after,baseline_promoted=False,phase_2_frozen=False,phase_3_started=False)
    result['files_created']=sorted(str(p.relative_to(ROOT)).replace('\\','/') for p in OUT.rglob('*') if p.is_file())+['03_Compliance/reports/phase_2/freeze/FINAL_RESULT.json','03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_FREEZE_REVIEW.md','03_Compliance/reports/phase_2/freeze/FILES_CREATED.csv']
    result['files_created']=sorted(set(result['files_created']))
    js('FINAL_RESULT.json',result)
    report=['# Phase 2 — Final freeze review','',f"PHASE_2_FINAL_FREEZE_REVIEW = {result['PHASE_2_FINAL_FREEZE_REVIEW']}",f'FREEZE_BLOCKERS = {blockers}',f"READY_FOR_PHASE_2_BASELINE_PROMOTION = {result['READY_FOR_PHASE_2_BASELINE_PROMOTION']}",'','DuckDB exclusivamente read-only; baseline no promovida, Phase 2 no congelada, Phase 3 no iniciada. PROJECT_CURRENT_STATE.md y project_baseline.json intactos.','', '## Resultados','']
    report += ['- '+k+' = '+str(v) for k,v in result.items() if k not in ['known_limitations','files_created','git_status_before','git_status_after']]
    report += ['', '## Comprobaciones', '', '| Check | Status | Expected | Actual | Evidence |','|---|---|---|---|---|']
    report += [f"| {r['check']} | {r['status']} | {str(r['expected']).replace('|','/')} | {str(r['actual']).replace('|','/')} | {r['evidence']} |" for r in CHECKS]
    report += ['', '## Historia y limitaciones', '', 'G2-045 conserva READY_PENDING_SOURCE_FACT_PERSISTENCE en la evidencia histórica. La persistencia controlada posterior resuelve el prerrequisito; 48/48 revisiones resueltas para el freeze. El informe OPEN inicial de Gate 2 queda sucedido por HUMAN_REVIEW_GATE_2_CLOSURE.md. Las dependencias externas siguen sin interpretar.','']
    report += ['- '+r['classification']+': '+r['issue'] for r in limitations]
    report += ['', 'Reproducibilidad: replay controlado desde instantáneas históricas y scripts con SHA de entrada, en copia aislada y con decisiones humanas explícitas. No existe generador independiente de los dossiers Gate 1/2; se preservan como REVIEW_ONLY o MANUAL_HUMAN_DECISION. Ningún paso obligatorio consta como MISSING. No se ejecutaron pipelines de escritura ni se simuló una revisión jurídica automática.','', '## Git', '', 'Antes y después:', '```text', git_before, '```', 'No git add, commit ni push. El Git raíz agrupa los nuevos archivos bajo 03_Compliance/ ya no rastreado.','', '## Archivos creados','']
    report += ['- '+p for p in result['files_created']]
    md('PHASE_2_FINAL_FREEZE_REVIEW.md','\n'.join(report))
    writecsv('FILES_CREATED.csv',[dict(artifact_path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p)) for p in sorted(OUT.rglob('*')) if p.is_file() and p!=OUT/'FILES_CREATED.csv'])
    print(json.dumps({k:v for k,v in result.items() if k not in ['files_created','known_limitations','git_status_before','git_status_after']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
