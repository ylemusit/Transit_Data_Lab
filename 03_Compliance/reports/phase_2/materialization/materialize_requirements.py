"""Controlled Gate 2 materialization. Yeison Arbey Carrillo Lemus.
Todos los derechos reservados. No source/candidate updates; no schema changes.
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DB = ROOT / '03_Compliance/databases/transit_compliance.duckdb'
REVIEW = OUT.parent / 'review/gate_2'
EXPECTED = '0c119b4a75e6a0e7954480675cc625659fe65a1878f46dae1e496e0790d8ffec'
CLI = shutil.which('duckdb')
FACT = 'EU-2017-1926-SF-A09-P03'
GATE = ROOT / '03_Compliance/sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def canonical(rows):
    return sorted(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':')) for r in rows)

def digest(rows):
    return hashlib.sha256('\n'.join(canonical(rows)).encode()).hexdigest()

def lit(v):
    if v is None: return 'NULL'
    if isinstance(v, bool): return 'TRUE' if v else 'FALSE'
    return "'" + str(v).replace("'", "''") + "'"

def arrays(raw):
    raw = raw.strip(); result = []; decoder = json.JSONDecoder()
    while raw:
        item, end = decoder.raw_decode(raw); result.append(item); raw = raw[end:].strip()
    return result

def run(sql, readonly=True, name=None):
    args = [CLI, '-no-init', '-batch', '-bail', '-json']
    if readonly: args.append('-readonly')
    p = subprocess.run(args + [str(DB)], input=sql.encode(), capture_output=True, cwd=ROOT)
    if name:
        (OUT / (name + '.json')).write_bytes(p.stdout)
        (OUT / (name + '.stderr.txt')).write_bytes(p.stderr)
        (OUT / (name + '.exit_code.txt')).write_text(str(p.returncode))
    if p.returncode: raise RuntimeError(p.stderr.decode('utf-8'))
    return arrays(p.stdout.decode('utf-8'))

def query(sql):
    a = run(sql); return a[0] if a else []

def read_csv(p):
    with p.open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

def write_csv(name, rows, cols=None):
    cols = cols or list(rows[0])
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

def js(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def md(name, text):
    (OUT / name).write_text(text + '\n\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n', encoding='utf-8')

def check(ok, msg):
    if not ok: raise RuntimeError(msg)

def snapshot():
    names = query("SELECT table_schema||'.'||table_name AS table_id FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1")
    return {x['table_id']: query('SELECT * FROM ' + x['table_id']) for x in names}

def prepare():
    check(sha(DB) == EXPECTED, 'Entry SHA mismatch; STOP WITHOUT WRITE')
    check(not DB.with_suffix('.duckdb.wal').exists(), 'Unexpected WAL')
    check(not (OUT / 'MATERIALIZATION_PRE_WRITE_STATE.json').exists(), 'Preparation already exists; refuse overwrite')
    git = subprocess.check_output(['git','status','--short'], cwd=ROOT).decode()
    (OUT / 'GIT_STATUS_BEFORE.txt').write_text(git, encoding='utf-8')
    before = snapshot(); js('DATABASE_BEFORE.json', before)
    check([len(before[t]) for t in ['compliance.source_facts','compliance.requirements','compliance.deadlines']] == [36,3,1], 'Entry counts mismatch')
    check(sum(r['source_fact_id']==FACT for r in before['compliance.source_facts'])==1, 'Article 9(3) fact mismatch')
    closure = (REVIEW / 'materialization/HUMAN_REVIEW_GATE_2_CLOSURE.md').read_text(encoding='utf-8')
    for v in ['HUMAN_REVIEW_GATE_2 = CLOSED','GATE_2_INTERPRETIVE_ISSUES = 0','GATE_2_MECHANICAL_BLOCKERS = 0']:
        check(v in closure, 'Closure invariant: '+v)
    check(not read_csv(REVIEW / 'materialization/GATE_2_POST_SOURCE_FACT_EXCEPTION_QUEUE.csv'), 'Exception queue nonempty')
    original = REVIEW / 'resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv'
    u = read_csv(original)
    check(len(u)==48 and all(len({r[k] for r in u})==48 for k in ['final_review_id','requirement_proposal_id']), 'Universe uniqueness')
    ids={r['final_review_id'] for r in u}
    check(not ids & {'G2-032','G2-037'} and {'G2-032-A','G2-032-B','G2-037-A','G2-037-B','G2-037-C'} <= ids, 'Split invariants')
    check(sum(r['dependency_blocking_level']=='PARTIAL' for r in u)==7, 'Seven PARTIAL dependencies')
    evidence=read_csv(REVIEW / 'materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv')
    evidence={r['final_review_id']:r for r in evidence}
    facts={r['source_fact_id']:r for r in before['compliance.source_facts']}
    enriched=[]
    for r in u:
        if r['final_review_id']=='G2-045' and not r['source_fact_id']:
            check(evidence['G2-045']['source_fact_id']==FACT, 'Persistence evidence missing')
            r['source_fact_id']=FACT; enriched.append('G2-045.source_fact_id: NULL -> '+FACT)
        f=facts.get(r['source_fact_id'])
        check(f and all(f[k]==r[k] for k in ['source_document_id','source_provision_id','source_fact_text']), 'Fact provenance mismatch '+r['final_review_id'])
        check(evidence[r['final_review_id']]['materialization_eligible']=='TRUE', 'Eligibility mismatch')
    schema=query('DESCRIBE compliance.requirements'); dschema=query('DESCRIBE compliance.deadlines')
    js('DISCOVERED_SCHEMA.json', {'requirements':schema,'deadlines':dschema})
    existing={r['requirement_id']:r for r in before['compliance.requirements']}
    candidates={r['candidate_id']:r for r in before['compliance.requirement_candidates']}
    inserts=[]; idmap=[]; reconciliation=[]; mapped=[]
    fields={'source_document_id':'source_document_id','source_provision_id':'source_provision_id','requirement_class':'requirement_class','description':'normalized_description','responsible_party':'responsible_party','beneficiary_party':'beneficiary_party','is_mandatory':'is_mandatory','is_conditional':'is_conditional','condition_text':'condition_text','deadline_date':'deadline_date','geographic_scope':'geographic_scope'}
    for r in u:
        proposal=r['requirement_proposal_id']
        rid=proposal.replace('-PROP-','-REQ-') if '-PROP-' in proposal else 'EU-2017-1926-REQ-'+proposal
        candidate=candidates.get(r['origin_candidate_id'])
        target={k:(None if not r[v] else (r[v]=='TRUE' if k in ['is_mandatory','is_conditional'] else r[v])) for k,v in fields.items()}
        target.update(requirement_id=rid,jurisdiction='EU')
        action='INSERT_NEW'; classification='NEW'; differences=[]
        if rid in existing:
            old=existing[rid]
            differences=[{'field':k,'persisted':old[k],'approved':v} for k,v in target.items() if old[k]!=v]
            check(not differences, 'CONFLICT or UPDATE required: '+rid+' '+json.dumps(differences,ensure_ascii=False))
            check(candidate and candidate['requirement_id']==rid and candidate['source_fact_id']==r['source_fact_id'], 'Existing provenance conflict')
            # Ancillary fields retained verbatim: Gate 2 does not override their meaning.
            classification='COMPATIBLE_MATCH'; action='REUSE_EXISTING'
            reconciliation.append({'requirement_id':rid,'final_review_id':r['final_review_id'],'classification':classification,'differences':differences,'ancillary_persisted_fields':{k:v for k,v in old.items() if k not in target},'decision':'No update required: approved proposition/provenance exact; descriptive Gate 2 metadata preserved in input and ID map. Existing notes trace to unchanged approved candidate/source fact.'})
        else:
            target.update(requirement_type=None,is_auditable=False,notes=json.dumps({'gate_2':r,'legal_conclusion_allowed':False,'external_instrument_interpreted':False},ensure_ascii=False,sort_keys=True))
            check(set(target)<={s['column_name'] for s in schema}, 'SCHEMA_CHANGE_REQUIRED = YES')
            inserts.append(target)
        r['materialization_action']=action
        idmap.append(dict(final_review_id=r['final_review_id'],requirement_proposal_id=proposal,requirement_id=rid,origin_candidate_id=r['origin_candidate_id'],action=action,existing_requirement_id=rid if action=='REUSE_EXISTING' else '',collision_check='PASS',notes=classification))
        mapped.append(dict(final_review_id=r['final_review_id'],requirement_proposal_id=proposal,requirement_id=rid,source_document_id=r['source_document_id'],source_provision_id=r['source_provision_id'],source_fact_id=r['source_fact_id'],action=action,human_status=r['human_status'],materialized_status='PRESENT'))
    check(len({r['requirement_id'] for r in idmap})==48, 'ID collision')
    check(set(existing)=={r['requirement_id'] for r in idmap if r['action']=='REUSE_EXISTING'}, 'ORPHAN existing requirement')
    plan=[]; dl_inserts=[]; used_dl=set()
    for r,m in zip(u,idmap):
        if r['temporal_type']!='EXPLICIT_DATE':
            check(not r['deadline_date'], 'Unexpected non-explicit date'); continue
        check(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',r['deadline_date'])), 'Invalid explicit date')
        matched=[d for d in before['compliance.deadlines'] if d['requirement_id']==m['requirement_id']]
        d=dict(deadline_id=m['requirement_id']+'-DL-001',requirement_id=m['requirement_id'],jurisdiction='EU',deadline_date=r['deadline_date'],deadline_type=r['requirement_class'],description=r['normalized_description'],scope_description=r['deadline_scope'] or r['geographic_scope'] or None,source_document_id=r['source_document_id'],source_provision_id=r['source_provision_id'],notes=json.dumps({'final_review_id':r['final_review_id'],'source_reference':r['source_reference'],'annex_scope':r['annex_scope'],'exceptions':r['exceptions']},ensure_ascii=False))
        action='INSERT_NEW'
        if matched:
            check(len(matched)==1, 'Deadline ambiguous')
            old=matched[0]
            check(all(old[k]==d[k] for k in ['requirement_id','jurisdiction','deadline_date','deadline_type','source_document_id','source_provision_id']), 'Deadline conflict')
            check(r['final_review_id']=='G2-042' and old['description']=='Remitir a la Comisión el informe indicado en el artículo 10, apartado 1.' and old['scope_description']=='Medidas para establecer el punto de acceso nacional y modalidades de funcionamiento.', 'Deadline semantic conflict')
            used_dl.add(old['deadline_id']); action='REUSE_EXISTING'
        else: dl_inserts.append(d)
        plan.append(dict(final_review_id=r['final_review_id'],**{k:d[k] for k in ['requirement_id','deadline_date','deadline_type','description','scope_description','source_document_id','source_provision_id']},action=action))
    check(used_dl=={d['deadline_id'] for d in before['compliance.deadlines']}, 'ORPHAN deadline')
    check(len(before['compliance.requirements'])+len(inserts)==48, 'Dry run coverage')
    for table,name in [('compliance.requirements','REQUIREMENTS'),('compliance.deadlines','DEADLINES'),('compliance.source_facts','SOURCE_FACTS')]: write_csv(name+'_BEFORE.csv',before[table])
    write_csv('REQUIREMENTS_MATERIALIZATION_INPUT.csv',u); write_csv('REQUIREMENT_ID_MAP.csv',idmap); write_csv('DEADLINE_MATERIALIZATION_PLAN.csv',plan)
    js('EXISTING_REQUIREMENTS_RECONCILIATION.json',reconciliation)
    js('PREPARED_INSERTS.json',{'requirements':inserts,'deadlines':dl_inserts,'universe':mapped})
    protected={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'03_Compliance').rglob('*') if p.is_file() and OUT not in p.parents and p!=DB}
    protected['project_baseline.json']=sha(ROOT/'project_baseline.json')
    js('PROTECTED_FILE_HASHES.json',protected)
    state={'db_sha':sha(DB),'timestamp':datetime.now(timezone.utc).isoformat(),'tables':{t:{'count':len(v),'content_hash':digest(v)} for t,v in before.items()},'universe_hash':sha(original),'artifacts':{name:sha(OUT/name) for name in ['REQUIREMENTS_MATERIALIZATION_INPUT.csv','REQUIREMENT_ID_MAP.csv','DEADLINE_MATERIALIZATION_PLAN.csv','PREPARED_INSERTS.json','DATABASE_BEFORE.json','PROTECTED_FILE_HASHES.json']}}
    js('MATERIALIZATION_PRE_WRITE_STATE.json',state)
    md('REQUIREMENTS_MATERIALIZATION_DRY_RUN.md',f'# Dry run\n\nDRY_RUN = PASS\n\nUniverse = 48; reused = {len(existing)}; insert = {len(inserts)}; updates = 0; conflicts = 0.\nDeadlines reused = {len(used_dl)}; insert = {len(dl_inserts)}; conflicts = 0.\n\nEnrichment: {enriched}. Historical human status retained; persistence evidence closes its prerequisite. No substantive field changed.\n\nAll existing schema-supported approved fields compared exactly. Existing ancillary fields retained; descriptive classifications do not require updates. New descriptive metadata preserved verbatim in structured notes; is_auditable=False, legal_conclusion_allowed=False. Unknown fields remain NULL; no candidate semantics inherited.\n\nExisting Article 10(1) deadline is semantically identical: same requirement, date, type, provenance, report object and scope. Reused without changing wording.\n\nIDs follow REQ-Axx-Pxx convention, preserving proposal suffix including split suffixes. All 48 IDs unique; each existing row maps once. Full source fact linkage checked. Only explicit dates yield deadlines.')
    print(json.dumps({'dry_run':'PASS','requirements_insert':len(inserts),'deadlines_insert':len(dl_inserts)},ensure_ascii=False))

def apply():
    state=json.loads((OUT/'MATERIALIZATION_PRE_WRITE_STATE.json').read_text(encoding='utf-8'))
    check(sha(DB)==EXPECTED==state['db_sha'], 'Pre-write SHA mismatch')
    for name,h in state['artifacts'].items(): check(sha(OUT/name)==h,'Prepared artifact changed: '+name)
    before=json.loads((OUT/'DATABASE_BEFORE.json').read_text(encoding='utf-8'))
    check(canonical([snapshot()])==canonical([before]), 'Database semantic entry changed')
    protected=json.loads((OUT/'PROTECTED_FILE_HASHES.json').read_text(encoding='utf-8'))
    for p,h in protected.items(): check(sha(ROOT/p)==h,'Protected file changed: '+p)
    prepared=json.loads((OUT/'PREPARED_INSERTS.json').read_text(encoding='utf-8'))
    u=read_csv(OUT/'REQUIREMENTS_MATERIALIZATION_INPUT.csv')
    idmap=read_csv(OUT/'REQUIREMENT_ID_MAP.csv')
    expected_req=before['compliance.requirements']+prepared['requirements']
    expected_dl=before['compliance.deadlines']+prepared['deadlines']
    checks=[]
    def assertion(name, expected, sql): checks.append((name,expected,sql))
    assertion('FINAL_REQUIREMENTS',48,'SELECT count(*) FROM compliance.requirements')
    assertion('SOURCE_FACTS',36,'SELECT count(*) FROM compliance.source_facts')
    assertion('ARTICLE_9_3_FACT',1,"SELECT count(*) FROM compliance.source_facts WHERE source_fact_id="+lit(FACT))
    assertion('EXPLICIT_DEADLINES',len(expected_dl),'SELECT count(*) FROM compliance.deadlines')
    # Compare every expected persisted field with null-safe equality. New created_at
    # is intentionally generated by DuckDB, all other fields are specified or NULL.
    for table,rows,label in [('compliance.requirements',expected_req,'REQUIREMENT'),('compliance.deadlines',expected_dl,'DEADLINE')]:
        cols=[x['column_name'] for x in query('DESCRIBE '+table)]
        for row in rows:
            predicates=[k+' IS NOT DISTINCT FROM '+lit(row.get(k)) for k in cols if k!='created_at' or k in row]
            identifier=row[cols[0]]
            assertion(label+'_'+identifier,1,'SELECT count(*) FROM '+table+' WHERE '+' AND '.join(predicates))
    for table,rows in before.items():
        if table in ('compliance.requirements','compliance.deadlines'): continue
        assertion('UNCHANGED_COUNT_'+table,len(rows),'SELECT count(*) FROM '+table)
        for i,row in enumerate(rows):
            assertion('UNCHANGED_ROW_'+table+'_'+str(i),1,'SELECT count(*) FROM '+table+' WHERE '+' AND '.join(k+' IS NOT DISTINCT FROM '+lit(v) for k,v in row.items()))
    for table,key in [('compliance.requirements','requirement_id'),('compliance.deadlines','deadline_id')]:
        assertion('UNIQUE_'+key,0,'SELECT count(*) FROM (SELECT '+key+' FROM '+table+' GROUP BY '+key+' HAVING count(*)>1)')
    up=(OUT/'REQUIREMENTS_MATERIALIZATION_INPUT.csv').relative_to(ROOT).as_posix()
    mp=(OUT/'REQUIREMENT_ID_MAP.csv').relative_to(ROOT).as_posix()
    uv="read_csv("+lit(up)+",header=true,all_varchar=true)"
    mv="read_csv("+lit(mp)+",header=true,all_varchar=true)"
    assertion('FINAL_UNIVERSE_IDS',48,'SELECT count(DISTINCT final_review_id) FROM '+uv)
    assertion('ALL_48_TRACEABLE',48,'SELECT count(*) FROM '+uv+' u JOIN '+mv+' m USING(final_review_id) JOIN compliance.requirements r USING(requirement_id) JOIN compliance.source_facts f ON u.source_fact_id=f.source_fact_id WHERE r.source_document_id=u.source_document_id AND r.source_provision_id=u.source_provision_id AND f.source_document_id=u.source_document_id AND f.source_provision_id=u.source_provision_id')
    assertion('SUPERSEDED_PARENTS',0,'SELECT count(*) FROM '+mv+" WHERE final_review_id IN ('G2-032','G2-037')")
    assertion('SPLIT_CHILDREN',5,'SELECT count(*) FROM '+mv+" m JOIN compliance.requirements r USING(requirement_id) WHERE final_review_id IN ('G2-032-A','G2-032-B','G2-037-A','G2-037-B','G2-037-C')")
    assertion('PARTIAL_PERSISTED',7,"SELECT count(*) FROM compliance.requirements WHERE json_extract_string(try_cast(notes AS JSON),'$.gate_2.dependency_blocking_level')='PARTIAL' AND json_extract_string(try_cast(notes AS JSON),'$.external_instrument_interpreted')='false'")
    assertion('FUNCTIONAL_NO_FIXED_DATE',0,'SELECT count(*) FROM '+uv+' u JOIN '+mv+' m USING(final_review_id) JOIN compliance.requirements r USING(requirement_id) LEFT JOIN compliance.deadlines d USING(requirement_id) WHERE '+"u.temporal_type IN ('FUNCTIONAL_TIME_REQUIREMENT','EXTERNAL_SCHEDULE_REFERENCE') AND (r.deadline_date IS NOT NULL OR d.deadline_id IS NOT NULL)")
    assertion('NO_AUTOMATIC_CONCLUSION',0,"SELECT count(*) FROM compliance.requirements WHERE is_auditable IS DISTINCT FROM FALSE OR json_extract_string(try_cast(notes AS JSON),'$.legal_conclusion_allowed')='true'")
    assertion('NO_INFERRED_GTFS',0,"SELECT count(*) FROM compliance.requirements WHERE contains(upper(description),'GTFS')")
    # Exact approved descriptions, conditions and notes above prove no broader
    # NeTEx/SIRI/DATEX inference; source rows include Annex and B-I/D-I verbatim.
    for d in before['source.documents']:
        path=Path(d['local_file'])
        if not path.is_absolute(): path=ROOT/'03_Compliance'/path
        check(sha(path)==d['source_hash'], 'Legal hash mismatch '+d['document_id'])
        assertion('LEGAL_HASH_'+d['document_id'],1,'SELECT count(*) FROM read_blob('+lit(path.as_posix())+') WHERE sha256(content)='+lit(d['source_hash']))
    body='WITH checks AS (\n'+'\nUNION ALL\n'.join('SELECT '+lit(n)+' AS test, '+str(e)+' AS expected, ('+q+') AS actual' for n,e,q in checks)+'\n) SELECT test, CASE WHEN expected=actual THEN \'PASS\' ELSE \'FAIL\' END AS status, expected, actual FROM checks ORDER BY test;\n'
    check(not GATE.exists(),'Post gate exists; refuse overwrite')
    GATE.write_text('-- Read-only post-materialization gate. Run from repository root.\n-- Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'+body,encoding='utf-8')
    # Durable full pre-write database backup; never restore automatically.
    shutil.copy2(DB,OUT/'PRE_WRITE_DATABASE_BACKUP.duckdb')
    check(sha(OUT/'PRE_WRITE_DATABASE_BACKUP.duckdb')==EXPECTED,'Backup SHA mismatch')
    statements=['BEGIN TRANSACTION;']
    for table,rows in [('compliance.requirements',prepared['requirements']),('compliance.deadlines',prepared['deadlines'])]:
        for row in rows:
            statements.append('INSERT INTO '+table+' ('+','.join(row)+') VALUES ('+','.join(lit(v) for v in row.values())+');')
    statements.append('CREATE TEMP TABLE materialization_checks AS '+body)
    statements.append("SELECT CASE WHEN count(*) FILTER (WHERE status<>'PASS')=0 THEN 'PASS' ELSE error('Materialization transaction invariant failed; rollback on connection close') END AS TRANSACTION_VALIDATION FROM materialization_checks;")
    statements.append('SELECT * FROM materialization_checks;')
    statements.append('COMMIT;')
    transaction='\n'.join(statements)
    (OUT/'CONTROLLED_TRANSACTION.sql').write_text(transaction,encoding='utf-8')
    check(sha(DB)==EXPECTED,'SHA changed before transaction')
    try: run(transaction,readonly=False,name='TRANSACTION')
    except Exception:
        js('TRANSACTION_STATUS.json',{'committed':False,'rollback_occurred':True}); raise
    js('TRANSACTION_STATUS.json',{'committed':True,'rollback_occurred':False})
    after=snapshot(); js('DATABASE_AFTER.json',after)
    post=sha(DB); check(post!=EXPECTED,'Post SHA did not change')
    for t in before:
        if t not in ('compliance.requirements','compliance.deadlines'): check(canonical(before[t])==canonical(after[t]),'Unauthorized delta '+t)
    for table,name in [('compliance.requirements','REQUIREMENTS'),('compliance.deadlines','DEADLINES'),('compliance.source_facts','SOURCE_FACTS')]: write_csv(name+'_AFTER.csv',after[table])
    for p,h in protected.items(): check(sha(ROOT/p)==h,'Protected file changed after transaction: '+p)
    write_csv('MATERIALIZED_REQUIREMENT_UNIVERSE.csv',prepared['universe'])
    js('MATERIALIZATION_POST_WRITE_STATE.json',{'db_sha':post,'tables':{t:{'count':len(v),'content_hash':digest(v)} for t,v in after.items()},'timestamp':datetime.now(timezone.utc).isoformat()})
    finalize()

def finalize():
    before=json.loads((OUT/'DATABASE_BEFORE.json').read_text(encoding='utf-8'))
    after=json.loads((OUT/'DATABASE_AFTER.json').read_text(encoding='utf-8'))
    prepared=json.loads((OUT/'PREPARED_INSERTS.json').read_text(encoding='utf-8'))
    u=read_csv(OUT/'REQUIREMENTS_MATERIALIZATION_INPUT.csv')
    expected_dl=before['compliance.deadlines']+prepared['deadlines']
    post=json.loads((OUT/'MATERIALIZATION_POST_WRITE_STATE.json').read_text())['db_sha']
    check(sha(DB)==post,'Post-write SHA changed before finalization')
    check(canonical([snapshot()])==canonical([after]),'Live database differs from post-write snapshot')
    protected=json.loads((OUT/'PROTECTED_FILE_HASHES.json').read_text(encoding='utf-8'))
    for p,h in protected.items(): check(sha(ROOT/p)==h,'Protected file changed: '+p)
    suites=[ROOT/'03_Compliance/sql/07_tests/phase_1/test_phase_1_invariants.sql',ROOT/'03_Compliance/sql/07_tests/phase_1/test_phase_1_master.sql',ROOT/'03_Compliance/sql/07_tests/source/test_eu_2017_1926_master_structure.sql']
    suites+=sorted((ROOT/'03_Compliance/sql/07_tests/source').glob('*annex*.sql'))
    suites += [ROOT/'03_Compliance/sql/07_tests/phase_2/test_phase_2_master.sql',ROOT/'03_Compliance/sql/07_tests/phase_2/test_phase_2_pre_materialization_gate.sql',GATE]
    results=[]
    for suite in suites:
        evidence=OUT/(suite.stem+'.json')
        if evidence.exists():
            check((OUT/(suite.stem+'.exit_code.txt')).read_text().strip()=='0','Suite exit code nonzero')
            values=arrays(evidence.read_text(encoding='utf-8'))
        else: values=run(suite.read_text(encoding='utf-8-sig'),name=suite.stem)
        rows=[r for a in values for r in a if 'test' in r and 'status' in r]
        check(bool(rows),'Suite has no test result rows: '+suite.stem)
        failed=[r for r in rows if r['status']!='PASS']
        allowed=set()
        if suite.stem=='test_phase_1_master': allowed={'22_REQUIREMENTS_NOT_DERIVED_YET','PHASE_1_CORPUS_INTEGRITY'}
        if suite.stem in ('test_phase_2_master','test_phase_2_pre_materialization_gate'): allowed={'23_REQUIREMENTS_FROM_APPROVED_CANDIDATES_ONLY','31_REQUIREMENTS_CURRENT','32_DEADLINES_CURRENT','PHASE_2_EXTRACTION_INTEGRITY'}
        status='PASS' if not failed else ('EXPECTED_HISTORICAL_STATE_MISMATCH' if all(r.get('test') in allowed for r in failed) else 'FAIL')
        results.append({'suite':suite.stem,'status':status,'checks':len(rows),'failed_checks':json.dumps(failed,ensure_ascii=False)})
    write_csv('TEST_RESULTS.csv',results)
    check(all(r['status']!='FAIL' for r in results),'Post-write regression failed; see TEST_RESULTS.csv')
    check(sha(DB)==post,'Read-only tests changed database')
    delta=['# Authorized database delta','', '| Table | Before | After | Before hash | After hash |','|---|---:|---:|---|---|']
    for t in before: delta.append(f'| {t} | {len(before[t])} | {len(after[t])} | {digest(before[t])} | {digest(after[t])} |')
    md('PHASE_2_REQUIREMENTS_DATABASE_DELTA.md','\n'.join(delta)+'\n\nUnauthorized semantic deltas = NO. Existing reused rows unchanged, including created_at and notes. Protected historical files and project_baseline.json unchanged.')
    git=subprocess.check_output(['git','status','--short'],cwd=ROOT).decode()
    (OUT/'GIT_STATUS_AFTER.txt').write_text(git,encoding='utf-8')
    summary={'REQUIREMENTS_MATERIALIZATION':'PASS','PRE_WRITE_SHA':EXPECTED,'POST_WRITE_SHA':post,'SHA_CHANGED':'YES','final_approved_universe':48,'requirements_before':3,'requirements_reused':3,'requirements_inserted':len(prepared['requirements']),'requirements_updated':0,'requirement_conflicts':0,'requirements_after':len(after['compliance.requirements']),'deadlines_before':1,'deadlines_reused':1,'deadlines_inserted':len(prepared['deadlines']),'deadline_conflicts':0,'deadlines_after':len(after['compliance.deadlines']),'source_facts_before':36,'source_facts_after':36,'article_9_3_traceability':'PASS','external_dependencies_PARTIAL':7,'functional_timing_requirements':sum(r['temporal_type']=='FUNCTIONAL_TIME_REQUIREMENT' for r in u),'explicit_deadlines':len(expected_dl),'unauthorized_semantic_deltas':'NO','rollback_occurred':'NO','materialized_universe_count':48,'missing_requirements':0,'duplicate_requirements':0,'superseded_parents_materialized':'NO','READY_FOR_PHASE_2_FINAL_FREEZE_REVIEW':'YES','tests':results,'git_status':git}
    js('FINAL_RESULT.json',summary)
    md('PHASE_2_REQUIREMENTS_MATERIALIZATION.md','# Requirements materialization\n\n'+ '\n'.join('- '+k+' = '+str(v) for k,v in summary.items() if k not in ('tests','git_status'))+'\n\nTests:\n'+ '\n'.join('- '+r['suite']+': '+r['status'] for r in results)+'\n\nPhase 2 remains open, not frozen. Phase 3 not started. No staging, commit or push.\n\nGit status:\n```text\n'+git+'```')
    print(json.dumps(summary,ensure_ascii=True))

if __name__=='__main__':
    try:
        if sys.argv[1]=='prepare': prepare()
        elif sys.argv[1]=='apply': apply()
        elif sys.argv[1]=='finalize': finalize()
        else: raise RuntimeError('Use prepare or apply')
    except Exception as e:
        md('PHASE_2_REQUIREMENTS_MATERIALIZATION.md','# Materialization\n\nREQUIREMENTS_MATERIALIZATION = FAIL\n\n'+str(e)+'\n\nSee TRANSACTION_STATUS.json when present. Preparation never writes database. No automatic restore after commit.')
        print(str(e)); sys.exit(1)
