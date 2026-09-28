"""COMPLIANCE_V1_CURRENT_GATE: read-only, exact state and operational replay.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from lxml import etree
from m06_b02_pack import DB, ROOT, query, run, save, sha
from compliance_v1_pack import EVIDENCE, FIXTURES, verify, build_package, REQ, literal
from compliance_v1_engine import evaluate, inspect_gtfs, inspect_netex, digest, MAX_BYTES, csv_rows
from compliance_v1_fixtures import build
from compliance_v1_reconcile import reconcile
from phase3_observation_contract import decode


def require(ok,message):
    if not ok: raise RuntimeError(message)


def json_stream(s):
    rows=[];decoder=json.JSONDecoder()
    while s.strip():
        s=s.lstrip();obj,n=decoder.raw_decode(s);rows.extend(obj);s=s[n:]
    return rows


def main():
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True)
    a=p.parse_args();out=a.evidence.resolve();out.mkdir(parents=True,exist_ok=False)
    checks={};initial=sha(DB)
    try:
        package=json.loads((EVIDENCE/'package.json').read_text())
        baseline=json.loads((EVIDENCE/'baseline.json').read_text())
        persistence=json.loads((EVIDENCE/'persistence/summary.json').read_text())
        require(initial==persistence['final_hash'],'AUTHORITATIVE_HASH_DRIFT')
        require(not Path(str(DB)+'.wal').exists(),'WAL_PENDING')
        checks['exact_authoritative_delta']=verify(DB,package,baseline)
        manifest=json.loads((EVIDENCE/'source_manifest.json').read_text())
        for source in manifest['sources']:
            require(digest((EVIDENCE/'sources'/source['path']).read_bytes())==source['sha256'],'SOURCE_DRIFT:'+source['path'])
        checks['technical_sources']='PASS'
        require(build_package()==package,'PACKAGE_GENERATOR_REPLAY')
        checks['persistence_generator_replay']='PASS'
        # Re-run frozen-phase checks, preserving the one superseded state assertion.
        for name,path in [('phase1','phase_1/test_phase_1_invariants.sql'),('phase2','phase_2/test_phase_2_post_materialization_gate.sql')]:
            raw=run(DB,(ROOT/'03_Compliance/sql/07_tests'/path).read_text(encoding='utf-8-sig'))
            save(out/(name+'_raw.json'),raw);require(raw['exit_code']==0,name+'_EXECUTION')
            rows=[r for r in json_stream(raw['stdout']) if 'test' in r and 'status' in r]
            require(len(rows)==(22 if name=='phase1' else 387),name+'_CHECK_COUNT')
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
        require(first==second==package['pilots'],'OPERATIONAL_REPLAY_DRIFT')
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
        for rule in query(DB,'SELECT * FROM audit.rules'):
            contract=json.loads(rule['validation_expression'])
            require(rule['legal_conclusion_allowed'] is False and rule['requirement_id']==REQ,'RULE_SEMANTICS')
            require(contract['evaluator_sha256']==digest((ROOT/'tools/compliance_v1_engine.py').read_bytes()),'EVALUATOR_DRIFT')
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
        checks['protected_gtfs_hash']=sha(ROOT/'02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb')
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
