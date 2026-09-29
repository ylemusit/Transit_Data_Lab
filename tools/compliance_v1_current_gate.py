"""COMPLIANCE_V1_CURRENT_GATE: read-only, exact state and operational replay.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
from datetime import datetime
import json
import platform
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from lxml import etree
from m06_b02_pack import DB, ROOT, query, run, save, sha
from compliance_v1_pack import EVIDENCE, FIXTURES, verify, build_package, REQ, literal
from compliance_v1_engine import evaluate, inspect_gtfs, inspect_netex, digest, MAX_BYTES, csv_rows
from compliance_v1_fixtures import build
from compliance_v1_reconcile import reconcile
from phase3_observation_contract import decode
from compliance_v1_transition_candidate import build_candidate, candidate_bytes
import compliance_v1_pack
import compliance_v1_reconcile
from compliance_portable_gate import portable_sql, sources
from protected_resource_preflight import check_resource

CURRENT_PACKAGE_DIR = ROOT/'03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate_final'
HISTORICAL_REPLAY = ROOT/'02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2a_transition_20260929/historical_package_replay.json'
HISTORICAL_PACKAGE_SHA256 = '2f85c9bd92ad603bab696e34c886b3f85ac22c05ba7aa0e90dc10137bb061981'
HISTORICAL_GENERATOR_GIT_BLOB = '14b19af18a99619aab0d4e9fbd8a277f4e1c6826'
CURRENT_PACKAGE_SHA256 = '8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b'
CURRENT_EVALUATOR_SHA256 = '60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb'


def require(ok,message):
    if not ok: raise RuntimeError(message)


def json_stream(s):
    rows=[];decoder=json.JSONDecoder()
    while s.strip():
        s=s.lstrip();obj,n=decoder.raw_decode(s);rows.extend(obj);s=s[n:]
    return rows


def replay_historical_package():
    evaluator_sha='efe3164ddfe33255d9ce94db0e6f410a80ec58c6'
    evaluator_source=subprocess.check_output(['git','cat-file','blob',evaluator_sha],cwd=ROOT)
    generator_source=subprocess.check_output(['git','cat-file','blob',HISTORICAL_GENERATOR_GIT_BLOB],cwd=ROOT)
    previous_engine=sys.modules.get('compliance_v1_engine')
    with tempfile.TemporaryDirectory(prefix='tdl-historical-v1-replay-') as td:
        replay_root=Path(td)
        historical_engine_path=replay_root/'tools/compliance_v1_engine.py'
        historical_engine_path.parent.mkdir(parents=True)
        historical_engine_path.write_bytes(evaluator_source)
        historic_engine=types.ModuleType('compliance_v1_engine')
        historic_engine.__file__=str(historical_engine_path)
        exec(compile(evaluator_source,historic_engine.__file__,'exec'),historic_engine.__dict__)
        sys.modules['compliance_v1_engine']=historic_engine
        try:
            historic_pack=types.ModuleType('compliance_v1_pack_historical_replay')
            historic_pack.__file__=str(replay_root/'tools/compliance_v1_pack.py')
            exec(compile(generator_source,historic_pack.__file__,'exec'),historic_pack.__dict__)
            # The historical package generator hashes its local evaluator path.
            # Keep all captured fixtures/sources and the database read-only in place.
            historic_pack.ROOT=replay_root
            historic_pack.DB=DB
            historic_pack.EVIDENCE=EVIDENCE
            historic_pack.FIXTURES=FIXTURES
            generated=historic_pack.build_package()
        finally:
            if previous_engine is None:
                del sys.modules['compliance_v1_engine']
            else:
                sys.modules['compliance_v1_engine']=previous_engine
    serialized=json.dumps(generated,ensure_ascii=False,indent=2).encode('utf-8').replace(b'\n',b'\r\n')
    return generated,serialized,digest(evaluator_source)


def main():
    global DB
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--db',type=Path);p.add_argument('--gtfs-db',type=Path)
    p.add_argument('--portable',action='store_true');p.add_argument('--legal-root',type=Path)
    a=p.parse_args()
    if a.portable:
        require(a.db is not None and a.gtfs_db is not None and a.legal_root is not None,'PORTABLE_CONFIGURATION_REQUIRED')
        require(a.legal_root.resolve()==ROOT.resolve(),'LEGAL_ROOT_WRONG_CHECKOUT')
        require(sources(a.legal_root.resolve())['status']=='PASS','PORTABLE_LEGAL_SOURCE_FAILURE')
        for name,path,expected in [('compliance_db',a.db,'4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B'),
                                   ('gtfs_raw_db',a.gtfs_db,'F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC')]:
            status=check_resource(dict(name=name,path=str(path.resolve()),sha256=expected,kind='duckdb'))['status']
            require(status=='RESOURCE_READY',name+':'+status)
        DB=a.db.resolve();compliance_v1_pack.DB=DB;compliance_v1_reconcile.DB=DB
    out=a.evidence.resolve();out.mkdir(parents=True,exist_ok=False)
    checks={};initial=sha(DB)
    if a.portable:
        checks['portable_legal_sources']='PASS'
        checks['portable_resource_preflight']='PASS'
    try:
        package=json.loads((EVIDENCE/'package.json').read_text())
        baseline=json.loads((EVIDENCE/'baseline.json').read_text())
        persistence=json.loads((EVIDENCE/'persistence/summary.json').read_text())
        require(initial==persistence['final_hash'],'AUTHORITATIVE_HASH_DRIFT')
        require(not Path(str(DB)+'.wal').exists(),'WAL_PENDING')
        checks['exact_authoritative_delta']=verify(DB,package,baseline)
        require(sha(EVIDENCE/'package.json').lower()==HISTORICAL_PACKAGE_SHA256,'HISTORICAL_PACKAGE_IDENTITY')
        replay=json.loads(HISTORICAL_REPLAY.read_text(encoding='utf-8'))
        require(replay.get('status')=='PASS' and replay.get('byte_identity')=='PASS','HISTORICAL_PACKAGE_REPLAY')
        require(replay.get('historical_evaluator_sha256')=='efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70','HISTORICAL_EVALUATOR_IDENTITY')
        require(replay.get('expected_package_sha256')==HISTORICAL_PACKAGE_SHA256 and replay.get('replayed_package_sha256')==HISTORICAL_PACKAGE_SHA256,'HISTORICAL_REPLAY_SHA')
        replayed_historical_package,historical_serialization,historical_evaluator_sha=replay_historical_package()
        require(historical_evaluator_sha==replay['historical_evaluator_sha256'],'HISTORICAL_EVALUATOR_BYTE_IDENTITY')
        require(replayed_historical_package==package,'HISTORICAL_PACKAGE_GENERATOR_REPLAY')
        require(digest(historical_serialization)==HISTORICAL_PACKAGE_SHA256,'HISTORICAL_PACKAGE_BYTE_REPLAY')
        checks['historical_package_replay']='PASS'
        manifest=json.loads((EVIDENCE/'source_manifest.json').read_text())
        for source in manifest['sources']:
            require(digest((EVIDENCE/'sources'/source['path']).read_bytes())==source['sha256'],'SOURCE_DRIFT:'+source['path'])
        checks['technical_sources']='PASS'
        current_package,current_manifest=build_candidate()
        approved_package=json.loads((CURRENT_PACKAGE_DIR/'package_candidate.json').read_text(encoding='utf-8'))
        approved_manifest=json.loads((CURRENT_PACKAGE_DIR/'transition_manifest.json').read_text(encoding='utf-8'))
        require(current_package==approved_package,'CURRENT_PACKAGE_GENERATOR_REPLAY')
        require(candidate_bytes(approved_package)==(CURRENT_PACKAGE_DIR/'package_candidate.json').read_bytes(),'CURRENT_PACKAGE_SERIALIZATION')
        require(sha(CURRENT_PACKAGE_DIR/'package_candidate.json').lower()==CURRENT_PACKAGE_SHA256,'CURRENT_PACKAGE_IDENTITY')
        require(current_manifest['candidate_package_sha256']==CURRENT_PACKAGE_SHA256,'CURRENT_PACKAGE_GENERATOR_IDENTITY')
        require(approved_manifest.get('candidate_package_sha256')==CURRENT_PACKAGE_SHA256,'APPROVED_POINTER_IDENTITY')
        require(approved_manifest.get('candidate_status')=='APPROVED_CURRENT' and approved_manifest.get('approval_status')=='APPROVED','APPROVED_PACKAGE_LIFECYCLE')
        require(approved_manifest.get('decision')=='APPROVE' and approved_manifest.get('reviewed_by')=='Yeison Arbey Carrillo Lemus','HUMAN_APPROVAL_IDENTITY')
        require(datetime.fromisoformat(approved_manifest['reviewed_at_utc'].replace('Z','+00:00')).utcoffset().total_seconds()==0,'HUMAN_APPROVAL_TIMESTAMP')
        require(approved_manifest.get('evaluator_version_after')=='compliance-v1/2' and approved_manifest.get('evaluator_sha_after')==CURRENT_EVALUATOR_SHA256,'CURRENT_EVALUATOR_IDENTITY')
        require(approved_manifest.get('rule_id')=='V1-RULE-GTFS' and approved_manifest.get('rule_version_after')=='compliance-v1/1','CURRENT_RULE_IDENTITY')
        require(approved_manifest.get('reference_spec_identity_unchanged') is True,'REFERENCE_SPEC_IDENTITY')
        require(current_manifest['transition_reason']=='IMPLEMENTATION_CHANGE' and current_manifest['predecessor_package_sha256']==HISTORICAL_PACKAGE_SHA256,'CURRENT_PACKAGE_LINEAGE')
        pointer=json.loads((ROOT/'03_Compliance/reports/evidence/compliance_v1_current_implementation_v2.json').read_text(encoding='utf-8'))
        require(pointer.get('package_sha256')==CURRENT_PACKAGE_SHA256 and pointer.get('evaluator_sha256')==CURRENT_EVALUATOR_SHA256,'CURRENT_POINTER_IDENTITY')
        require(pointer.get('approval_status')=='APPROVED' and pointer.get('candidate_status')=='APPROVED_CURRENT','CURRENT_POINTER_APPROVAL')
        require(pointer.get('transition_id')=='COMPLIANCE_V1_IMPLEMENTATION_TRANSITION_V1_TO_V2','CURRENT_POINTER_TRANSITION')
        require(pointer.get('semantic_scope')=='Compliance V1' and pointer.get('rule_id')=='V1-RULE-GTFS' and pointer.get('rule_version')=='compliance-v1/1','CURRENT_POINTER_RULE_IDENTITY')
        require(pointer.get('parser_version')=='gtfs-lab-csv/2' and pointer.get('transition_reason')=='IMPLEMENTATION_CHANGE','CURRENT_POINTER_IMPLEMENTATION_IDENTITY')
        require(pointer.get('semantic_rule_change') is False and pointer.get('reference_spec_identity_unchanged') is True,'CURRENT_POINTER_SEMANTIC_IDENTITY')
        require(pointer.get('predecessor_package_sha256')==HISTORICAL_PACKAGE_SHA256 and pointer.get('holdout_accessed') is False,'CURRENT_POINTER_LINEAGE_OR_HOLDOUT')
        checks['current_package_generator_replay']='PASS'
        checks['current_package_identity']=CURRENT_PACKAGE_SHA256
        # Re-run frozen-phase checks, preserving the one superseded state assertion.
        for name,path in [('phase1','phase_1/test_phase_1_invariants.sql'),('phase2','phase_2/test_phase_2_post_materialization_gate.sql')]:
            sql=portable_sql() if a.portable and name=='phase2' else (ROOT/'03_Compliance/sql/07_tests'/path).read_text(encoding='utf-8-sig')
            raw=run(DB,sql)
            save(out/(name+'_raw.json'),raw);require(raw['exit_code']==0,name+'_EXECUTION')
            rows=[r for r in json_stream(raw['stdout']) if 'test' in r and 'status' in r]
            require(len(rows)==(22 if name=='phase1' else (377 if a.portable else 387)),name+'_CHECK_COUNT')
            failures=[r for r in rows if r['status']!='PASS']
            allowed=[dict(test='UNCHANGED_COUNT_audit.rules',status='FAIL',expected=0,actual=2)] if name=='phase2' else []
            require(failures==allowed,name+'_INTEGRITY')
            checks[name]=dict(current_pass=len(rows)-len(allowed),historical=allowed)
        # Exact inventory/configuration, including all 48 IDs and ten coverage rows.
        disposition=json.loads((EVIDENCE/'dispositions.json').read_text(encoding='utf-8'))
        require(disposition==reconcile(),'DISPOSITION_OR_COVERAGE_DRIFT')
        require(disposition['scope']['standby']==['SIRI','GTFS-RT'],'STANDBY_SCOPE')
        checks['scope_coverage_disposition']='PASS'
        cases=json.loads((FIXTURES/'manifest.json').read_text())
        require(len(cases)==28 and len({c['id'] for c in cases})==28,'FIXTURE_COUNT')
        gv=cases[0]['version'];nv=next(c['version'] for c in cases if c['standard']=='NETEX')
        # Fresh deterministic regeneration in a separate environment directory.
        with tempfile.TemporaryDirectory(prefix='tdl-v1-fixtures-') as td:
            regenerated=Path(td)/'fixtures';build(regenerated,gv,nv)
            require((regenerated/'manifest.json').read_bytes()==(FIXTURES/'manifest.json').read_bytes(),'FIXTURE_MANIFEST_REPLAY')
            for c in cases:
                for name in c['files']:
                    b=(FIXTURES/c['id']/name).read_bytes()
                    require(digest(b)==c['hashes'][name],'FIXTURE_HASH:'+c['id'])
                    require(b==(regenerated/c['id']/name).read_bytes(),'FIXTURE_REPLAY:'+c['id'])
            first=[];second=[]
            for c in cases:
                first.append(dict(case=c['id'],expected=c['expected'],**evaluate(dict(c,directory=FIXTURES/c['id']),EVIDENCE/'sources',gv,nv)))
                second.append(dict(case=c['id'],expected=c['expected'],**evaluate(dict(c,directory=regenerated/c['id']),EVIDENCE/'sources',gv,nv)))
        require(first==second==current_package['pilots'],'OPERATIONAL_REPLAY_DRIFT')
        require(all(r['result']==r['expected'] and r['legal_conclusion_allowed'] is False for r in first),'FALSE_POSITIVE')
        save(out/'pilot_replay.json',first)
        checks['pilots']=dict(status='PASS',GTFS=18,NETEX=10,replays=2)
        # Reuse GTFS_Lab's ingestion contract (read_csv, header, all_varchar)
        # in memory. No raw DB import or second persisted GTFS stack.
        for name in ['trips.txt','stops.txt','stop_times.txt']:
            path=FIXTURES/'gtfs-valid'/name
            raw=run(Path(':memory:'),f'SELECT * FROM read_csv({literal(path.as_posix())},header=true,all_varchar=true)',readonly=False)
            require(raw['exit_code']==0,'IN_MEMORY_GTFS_PARSE')
            rows=json.loads(raw['stdout'])
            rows=[{k:('' if v is None else v) for k,v in r.items()} for r in rows]
            require(rows==csv_rows(path.read_bytes())[1],'GTFS_LAB_PARSER_CONTRACT')
        checks['gtfs_lab_ingestion_contract']='PASS'
        # Observation <-> exact dataset, evaluator, scope and result, not only counts.
        scopes={r['scope_unit_id']:r for r in query(DB,'SELECT * FROM mapping.phase3_mapping_scope_units')}
        observations=query(DB,"SELECT * FROM mapping.phase3_observed_evidence WHERE evidence_id LIKE 'V1-%'")
        require(len(observations)==28,'OBSERVATION_COUNT')
        byid={r['dataset_id']:r for r in first}
        for row in observations:
            obs=decode(row['notes'],scopes);r=byid[obs['dataset_id']]
            require(obs['dataset_sha256']==r['dataset_sha256'] and obs['observed_result']==r['observed'],'OBSERVATION_IDENTITY')
            require(row['mapping_id']==scopes[obs['scope_unit_id']]['mapping_id'],'OBSERVATION_SCOPE_LINK')
            require(obs['synthetic'] and row['fixture_kind']=='SYNTHETIC_TEST','SYNTHETIC_PROVENANCE')
        for rule in current_package['tables']['audit.rules']:
            contract=json.loads(rule['validation_expression'])
            require(rule['legal_conclusion_allowed'] is False and rule['requirement_id']==REQ,'RULE_SEMANTICS')
            require(contract['evaluator']=='compliance-v1/2' and contract['evaluator_sha256']==CURRENT_EVALUATOR_SHA256,'EVALUATOR_DRIFT')
            require(contract['rule_id']==rule['rule_id'],'RULE_IDENTITY_DRIFT')
            if contract['standard']=='GTFS':
                require(rule['rule_id']=='V1-RULE-GTFS' and contract['rule_id']=='V1-RULE-GTFS','RULE_IDENTITY_DRIFT')
            require(contract['scope_unit_id'] in scopes,'RULE_SCOPE')
        checks['observation_rule_contract']='PASS'
        # Untrusted input controls, evaluator fault and enum counterexamples.
        xml=(FIXTURES/'netex-valid/fragment.xml').read_bytes()
        schema=EVIDENCE/'sources/NeTEx_publication_EPIP.xsd'
        security={
            'utf16_dtd':inspect_netex(('<!DOCTYPE Line>'+xml.decode()).encode('utf-16'),nv,nv,schema),
            'oversized_xml':inspect_netex(b'x'*(MAX_BYTES+1),nv,nv,schema),
            'missing_schema':inspect_netex(xml,nv,nv,out/'absent.xsd'),
            'oversized_csv':inspect_gtfs({'trips.txt':b'x'*(MAX_BYTES+1),'stops.txt':b'stop_id\nS\n','stop_times.txt':b'trip_id,stop_id\nT,S\n'},gv,gv),
        }
        require(all(r['result']=='INSPECTION_ERROR' for r in security.values()),'SECURITY_FINDING_COLLISION')
        files={name:(FIXTURES/'gtfs-valid'/name).read_bytes() for name in ['trips.txt','stops.txt','stop_times.txt']}
        files['stops.txt']+=b'UNREFERENCED,Other,40,-3,9\n'
        require(inspect_gtfs(files,gv,gv)['result']=='PASS','UNREFERENCED_ENUM_FALSE_POSITIVE')
        save(out/'safety_cases.json',security);checks['data_safety']='PASS'
        # Public engine entrypoint, independent processes; no network at evaluation.
        cli=[]
        for standard,identity,dataset in [('GTFS',gv,FIXTURES/'gtfs-valid'),('NETEX',nv,FIXTURES/'netex-valid/fragment.xml')]:
            command=[sys.executable,'tools/compliance_v1_engine.py','--standard',standard,'--dataset',str(dataset),'--version',identity]
            outputs=[]
            for _ in range(2):
                proc=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
                require(proc.returncode==0,'CLI_EXECUTION');r=json.loads(proc.stdout)
                require(r['result']=='PASS','CLI_PILOT');outputs.append(r)
            require(outputs[0]==outputs[1],'CLI_REPLAY');cli.append(dict(command=command,output=outputs[0]))
        save(out/'cli_replay.json',cli);checks['controlled_process_replay']='PASS'
        checks['protected_gtfs_hash']=sha(a.gtfs_db.resolve() if a.portable else ROOT/'02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb')
        require(checks['protected_gtfs_hash']=='F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC','GTFS_BASELINE_DRIFT')
        require(sha(DB)==initial,'STOP_GLOBAL: READONLY_DRIFT')
        summary=dict(status='PASS',gate='COMPLIANCE_V1_CURRENT_GATE',checks=checks,initial_hash=initial,final_hash=sha(DB),
            environment=dict(python=platform.python_version(),lxml=list(etree.LXML_VERSION),libxml=list(etree.LIBXML_VERSION),
                             duckdb=subprocess.run(['duckdb','--version'],capture_output=True,text=True).stdout.strip()))
        save(out/'summary.json',summary);print(json.dumps(summary,indent=2))
    except Exception as exc:
        save(out/'summary.json',dict(status='FAIL_BLOCKING',error=str(exc),completed_checks=checks,initial_hash=initial,final_hash=sha(DB)))
        raise


if __name__=='__main__':
    main()
