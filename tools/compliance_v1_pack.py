"""Reproducible additive V1 package and transactional exact-delta persistence.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from m06_b02_pack import ROOT, DB, query, run, save, sha, snapshot, guard
from phase3_observation_contract import VERSION as OBS_VERSION, encode
from compliance_v1_engine import evaluate, digest, VERSION

EVIDENCE = ROOT/'03_Compliance/reports/evidence/compliance_v1_20260928'
FIXTURES = ROOT/'03_Compliance/fixtures/compliance_v1'
INITIAL = '6C7A944FB9EB7983A912AF42C2F5C69C0F29D268F6139D3B5566BF7140788E0F'
REQ = 'EU-2017-1926-REQ-A04-P01-001'
LIMIT = ('Technical subset only; no complete requirement, Annex, NAP access, '
         'legal compliance or production operator claim. Synthetic datasets.')


def literal(v):
    if v is None: return 'NULL'
    if type(v) is bool: return 'TRUE' if v else 'FALSE'
    return "'"+str(v).replace("'","''")+"'"


def build_package():
    cases=json.loads((FIXTURES/'manifest.json').read_text())
    gv=cases[0]['version']
    nv=next(c['version'] for c in cases if c['standard']=='NETEX')
    specs=[dict(kind='GTFS', mapping='M04-MAP-A04P01-GTFS-TRIP-STOP',
                capability='CAP-GTFS-SCHEDULE-TRIP-STOP-TIMES', version=gv,
                name='Fixed-stop scheduled trip references',
                path='stop_times.trip_id -> trips.trip_id; stop_times.stop_id -> stops.stop_id; stops.location_type in (empty,0)',
                source='gtfs_reference.md', section='stop_times.txt: trip_id, stop_id; stops.txt: location_type'),
           dict(kind='NETEX', mapping='M04-MAP-A04P01-NETEX-PT',
                capability='CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE', version=nv,
                name='EPIP named Line fragment', path='{http://www.netex.org.uk/netex}Line/@id,@version,Name; LineStructure/LineGroup',
                source='_content_NeTEx_EPIP.xsd', section='Line global element; LineStructure; LineGroup; DataManagedObjectAttributeGroup')]
    tables={}
    def add(table, **values):
        tables.setdefault(table,[]).append(values)
    scopes={}
    results=[]
    for s in specs:
        k=s['kind'];concept='V1-CPT-'+k;scope='V1-SCOPE-'+k;scopes[scope]=s
        constraints = dict(scope_unit_id=scope, standard=k, artifact_version=s['version'],
            technical_path=s['path'], source=s['source'], section=s['section'],
            constraints=('Fixed-stop records only; complete three-table inspection; unambiguous parents; flex NOT_EVALUABLE.' if k=='GTFS' else
                'Standalone Line global element validated against complete pinned EPIP XSD set; Name required but empty text permitted; no publication/keyref-wide validation.'),
            limitations=LIMIT,
            registry_relation=('Pinned reference bytes govern this inspector; historical registry revision remains unchanged.' if k=='GTFS' else
                '2021 Data4PT EPIP XSD based on NeTEx 1.3.1, no longer maintained. Does not prove equivalence to historical CEN/TS 16614-4:2017 registry identity or Spanish legal minimum profile.'))
        envelope=json.dumps(constraints,sort_keys=True,ensure_ascii=False)
        add('mapping.phase3_requirement_concepts',concept_id=concept,requirement_id=REQ,concept_code='V1_'+k,
            concept_name=s['name'],concept_description='Operational subset of the already accepted M04 relationship: '+s['name'],
            scope_status='PARTIAL',applicability_conditions=envelope,source_basis='EU-2017-1926-SF-A04-P01; accepted '+s['mapping'],
            review_status='APPROVED',review_outcome='ACCEPTED_WITH_LIMITATIONS',
            review_justification='Technical decomposition under explicit Compliance V1 mission; existing semantic review retained; no new legal interpretation.',
            limitations=LIMIT,created_at='2026-09-28 00:00:00',created_by='Codex / V1 mission',reviewed_at='2026-09-28',
            reviewed_by='Codex technical review / explicit V1 mission',notes='No claim of a new human legal review.')
        add('mapping.phase3_concept_mappings',concept_id=concept,mapping_id=s['mapping'],relation_note='Bounded operational subset; historical mapping and review unchanged.')
        add('mapping.phase3_mapping_scope_units',scope_unit_id=scope,concept_id=concept,mapping_id=s['mapping'],unit_code='V1_'+k,
            unit_name=s['name'],unit_definition=envelope,scope_disposition='INCLUDED',basis_section=s['section'],limitation=LIMIT,
            rationale='Selected by authorized V1 mission within accepted M04 semantic relationship.',review_status='APPROVED',
            reviewed_at='2026-09-28',reviewed_by='Codex technical review / explicit V1 mission',
            decision_document_id='COMPLIANCE_V1_SCOPE',milestone_id='COMPLIANCE_V1')
        ref='V1-SOURCE-'+k
        manifest=json.loads((EVIDENCE/'source_manifest.json').read_text())
        source=next(x for x in manifest['sources'] if x['path']==s['source'])
        add('mapping.phase3_source_references',source_reference_id=ref,capability_id=s['capability'],
            source_kind='OFFICIAL_SPECIFICATION' if k=='GTFS' else 'OFFICIAL_PROFILE',specification_name=s['name'],version=s['version'],
            section=s['section'],url_or_document_id=source['url'],retrieved_on='2026-09-28',reviewed_on='2026-09-28',
            notes=envelope+'; source_sha256='+source['sha256'],fixture_kind=None)
        add('mapping.phase3_scope_source_references',scope_unit_id=scope,source_reference_id=ref,evidence_role='SUPPORT')
        add('mapping.phase3_representability',representability_id='V1-REP-'+k,capability_id=s['capability'],
            representability_state='PARTIAL',explanation='AVAILABLE within exactly the committed scope; PARTIAL for the broader legacy capability. '+envelope,
            conditions=envelope,assessed_on='2026-09-28',review_status='REVIEWED',fixture_kind=None)
        add('mapping.phase3_automatability',automatability_id='V1-AUTO-'+k,mapping_id=s['mapping'],automatability_state='PARTIAL',
            explanation='AUTOMATABLE only for '+scope+'; requirement context HUMAN_REVIEW_REQUIRED.',
            prerequisites=envelope,assessed_on='2026-09-28',review_status='REVIEWED',fixture_kind=None)
        rule_contract=dict(constraints,rule_id='V1-RULE-'+k,evaluator=VERSION,
            evaluator_sha256=digest((ROOT/'tools/compliance_v1_engine.py').read_bytes()),
            result_vocabulary=['PASS','FAIL_TECHNICAL','NOT_EVALUABLE','INSPECTION_ERROR'],
            observation_contract=OBS_VERSION,configuration='max_bytes=1048576; max_rows=10000; complete declared scope required',
            legal_conclusion_allowed=False)
        add('audit.rules',rule_id='V1-RULE-'+k,requirement_id=REQ,rule_family='TECHNICAL_SUBCONDITION',rule_name=s['name'],
            description=LIMIT,target_format='GTFS' if k=='GTFS' else 'NeTEx',target_entity=s['name'],target_field=s['path'],severity='TECHNICAL',
            validation_engine='python tools/compliance_v1_engine.py',validation_expression=json.dumps(rule_contract,sort_keys=True),
            is_automatic=True,legal_conclusion_allowed=False,notes='Active only for V1 scoped engine/lab; not operator legal auditing.')
        for c in [c for c in cases if c['standard']==k]:
            r=evaluate(dict(c,directory=FIXTURES/c['id']),EVIDENCE/'sources',gv,nv)
            if r['result']!=c['expected']: raise RuntimeError('PILOT_FAILED:'+c['id'])
            results.append(dict(case=c['id'],expected=c['expected'],**r))
            status='FAILED' if r['result']=='INSPECTION_ERROR' else ('NOT_INSPECTED' if r['result']=='NOT_EVALUABLE' else 'COMPLETED')
            obs=dict(contract_version=OBS_VERSION,dataset_id=c['id'],dataset_version=c['version'],dataset_sha256=r['dataset_sha256'],
                inspection_run='V1-'+c['id'],evaluator_version=VERSION+';sha256='+r['evaluator_sha256'],scope_unit_id=scope,
                inspection_status=status,observed_result=r['observed'],errors=[r['reason']] if status=='FAILED' else [],
                limitations=[LIMIT,'result='+r['result']+'; reason='+r['reason']],
                inspection_extent='COMPLETE_DECLARED_LOCATOR' if c['complete'] else 'PARTIAL',synthetic=True)
            add('mapping.phase3_observed_evidence',evidence_id='V1-OBS-'+c['id'],capability_id=s['capability'],mapping_id=s['mapping'],
                evidence_type='FILE',locator='03_Compliance/fixtures/compliance_v1/'+c['id']+'/'+r['locator'],
                observed_value=r['observed'],observed_on='2026-09-28',notes=encode(obs,scopes),fixture_kind='SYNTHETIC_TEST')
    # Match physical schema order, including null columns, to enable exact EXCEPT ALL.
    ordered={}
    for table,rows in tables.items():
        schema,name=table.split('.')
        columns=[c['column_name'] for c in query(DB,f"SELECT column_name FROM information_schema.columns WHERE table_schema='{schema}' AND table_name='{name}' ORDER BY ordinal_position")]
        if any(set(r)-set(columns) for r in rows): raise RuntimeError('SCHEMA_MISMATCH')
        ordered[table]=[{col:r.get(col) for col in columns} for r in rows]
    return dict(version=VERSION,initial_hash=INITIAL,tables=ordered,pilots=results)


def temp_sql(package):
    sql=''
    for i,(table,rows) in enumerate(package['tables'].items()):
        sql+=f'CREATE TEMP TABLE v1_expected_{i} AS SELECT * FROM {table} WHERE false;\n'
        for row in rows:
            sql+=f'INSERT INTO v1_expected_{i} VALUES ('+','.join(literal(v) for v in row.values())+');\n'
    return sql


def transaction_sql(db,package,inject=False):
    constraints=query(db,"SELECT schema_name,table_name,constraint_type,constraint_column_names FROM duckdb_constraints() WHERE constraint_type IN ('PRIMARY KEY','UNIQUE')")
    sql=temp_sql(package)+'BEGIN TRANSACTION;\n'
    all_tables=list(snapshot(db))
    for i,table in enumerate(all_tables): sql+=f'CREATE TEMP TABLE v1_before_{i} AS SELECT * FROM {table};\n'
    for i,(table,rows) in enumerate(package['tables'].items()):
        cols=list(rows[0]);x=f'v1_expected_{i}'
        match=' AND '.join(f'e.{c} IS NOT DISTINCT FROM t.{c}' for c in cols)
        for key in [c['constraint_column_names'] for c in constraints if c['schema_name']+'.'+c['table_name']==table]:
            eq=' AND '.join(f'e.{c} IS NOT DISTINCT FROM t.{c}' for c in key)
            sql+=guard(f'NOT EXISTS(SELECT 1 FROM {x} e JOIN {table} t ON {eq} WHERE NOT ({match}))','IDENTITY_COLLISION')
        sql+=f'INSERT INTO {table} SELECT e.* FROM {x} e WHERE NOT EXISTS(SELECT 1 FROM {table} t WHERE {match});\n'
    if inject: sql+="SELECT error('V1_INJECTED_FAILURE');\n"
    for i,table in enumerate(all_tables):
        expected=f'SELECT * FROM v1_before_{i}'
        if table in package['tables']:
            j=list(package['tables']).index(table)
            expected+=f' UNION ALL (SELECT * FROM v1_expected_{j} EXCEPT ALL SELECT * FROM v1_before_{i})'
        sql+=guard(f'NOT EXISTS((SELECT * FROM {table} EXCEPT ALL ({expected})) UNION ALL (({expected}) EXCEPT ALL SELECT * FROM {table}))','EXACT_DELTA_'+str(i))
    return sql+'COMMIT;\n'


def verify(db,package,baseline):
    setup=temp_sql(package)
    checks={}
    for table,previous in baseline['tables'].items():
        select='SELECT * FROM '+table
        if table in package['tables']:
            i=list(package['tables']).index(table)
            exact=run(db,setup+f'SELECT * FROM v1_expected_{i} EXCEPT ALL SELECT * FROM {table};')
            if exact['exit_code'] or json.loads(exact['stdout'] or '[]'):
                raise RuntimeError('PACKAGE_ROW_MISSING_OR_DIFFERENT:'+table)
            select+=f' EXCEPT ALL SELECT * FROM v1_expected_{i}'
        r=run(db,setup+select)
        if r['exit_code']: raise RuntimeError(r)
        rows=json.loads(r['stdout'] or '[]')
        canonical=sorted(json.dumps(row,sort_keys=True,ensure_ascii=False) for row in rows)
        actual=dict(count=len(rows),sha256=hashlib.sha256('\n'.join(canonical).encode()).hexdigest())
        if actual!=previous: raise RuntimeError('STOP_GLOBAL: PROTECTED_DRIFT:'+table)
        checks[table]='PASS'
    if set(snapshot(db))!=set(baseline['tables']): raise RuntimeError('SCHEMA_TABLE_DRIFT')
    return checks


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--persist',action='store_true');a=p.parse_args()
    package_path=EVIDENCE/'package.json'
    baseline=json.loads((EVIDENCE/'baseline.json').read_text())
    if a.prepare:
        if sha(DB)!=INITIAL: raise RuntimeError('STOP_GLOBAL: INITIAL_HASH')
        package=build_package();save(package_path,package)
        save(EVIDENCE/'pilot_results.json',package['pilots'])
        print('PACKAGE_PREPARED',sum(map(len,package['tables'].values())))
    if a.persist:
        if sha(DB)!=INITIAL or Path(str(DB)+'.wal').exists(): raise RuntimeError('STOP_GLOBAL: INITIAL_STATE')
        package=json.loads(package_path.read_text())
        work=EVIDENCE/'persistence';work.mkdir(exist_ok=False)
        isolated=work/'isolated.duckdb';shutil.copy2(DB,isolated)
        sql=transaction_sql(isolated,package)
        (work/'transaction.sql').write_text(sql,encoding='utf-8')
        before=snapshot(isolated)
        rollback=run(isolated,transaction_sql(isolated,package,inject=True),readonly=False)
        save(work/'rollback.json',rollback)
        if rollback['exit_code']==0 or 'V1_INJECTED_FAILURE' not in rollback['stderr'] or snapshot(isolated)!=before:
            raise RuntimeError('STOP_GLOBAL: ROLLBACK_FAILED')
        fresh=run(isolated,sql,readonly=False);save(work/'fresh.json',fresh)
        if fresh['exit_code']: raise RuntimeError(fresh)
        verify(isolated,package,baseline)
        state=snapshot(isolated)
        noop=run(isolated,sql,readonly=False);save(work/'noop.json',noop)
        if noop['exit_code'] or state!=snapshot(isolated): raise RuntimeError('NOOP_FAILED')
        conflict=json.loads(json.dumps(package));conflict['tables']['audit.rules'][0]['rule_name']='CONFLICT_INJECTION'
        cr=run(isolated,transaction_sql(isolated,conflict),readonly=False);save(work/'conflict.json',cr)
        if cr['exit_code']==0 or 'IDENTITY_COLLISION' not in cr['stderr'] or state!=snapshot(isolated): raise RuntimeError('CONFLICT_FAILED')
        if sha(DB)!=INITIAL or snapshot(DB)!=before: raise RuntimeError('STOP_GLOBAL: PREWRITE_DRIFT')
        shutil.copy2(DB,work/'authoritative_before.duckdb')
        ar=run(DB,sql,readonly=False);save(work/'authoritative_write.json',ar)
        if ar['exit_code']: raise RuntimeError(ar)
        checks=verify(DB,package,baseline)
        save(work/'summary.json',dict(status='PASS',initial_hash=INITIAL,final_hash=sha(DB),
            rows_added=sum(map(len,package['tables'].values())),migrations=0,authoritative_transactions=1,
            isolated_rollback='PASS',isolated_noop='PASS',isolated_conflict='PASS',protected_tables=checks))
        print((work/'summary.json').read_text())
