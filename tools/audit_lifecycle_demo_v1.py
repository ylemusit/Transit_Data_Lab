"""Synthetic correction scenarios linked to distinct, actually executed receipts."""
import argparse
import json
from pathlib import Path
from collections import Counter
from tools.audit_corpus_v1 import ROOT,read,write,sha
from tools.audit_lifecycle_v1 import initialize,append,execution,validate,key

PAIRS=[
 ('SYNTH-GTFS-CORRECTED','GTFS-REF-TRIP-ROUTE--negative','GTFS-REF-TRIP-ROUTE--positive'),
 ('SYNTH-GTFS-PERSISTENT','GTFS-REF-SHAPE--negative','GTFS-REF-SHAPE--negative'),
 ('SYNTH-GTFS-NEW','GTFS-REF-SERVICE--positive','GTFS-REF-SERVICE--negative'),
 ('SYNTH-NETEX-CORRECTED','NETEX-XML-001--negative','NETEX-XML-001--positive'),
 ('SYNTH-NETEX-PERSISTENT','NETEX-XSD-001--negative','NETEX-XSD-001--negative'),
 ('SYNTH-NETEX-NEW','NETEX-XML-001--positive','NETEX-XML-001--negative'),
]


def ref(path):return {'path':str(Path(path).resolve()),'sha256':sha(Path(path))}


def snapshot(native_path,phase,output):
    native=read(native_path);index={r['case_id']:r for r in native['rows']};rows=[]
    for alias,before,after in PAIRS:
        case_id=before if phase=='BEFORE' else after;original=index[case_id];obs=original['observed'];rule=obs.get('raw_rule_result')
        if rule:
            version=rule.get('semantic_version',rule.get('version',rule.get('rule_version')))
            coverage=rule.get('coverage',{}).get('state')
            complete=obs['status'] in {'PASS','FAIL_TECHNICAL'} and (coverage in {'FULL','FEATURE_PRESENT_FULLY_AUDITED'} or rule.get('checked_rows',0)>0)
        else:
            findings=obs.get('findings',[]);version=findings[0]['rule_version'] if findings else '1.0.0'
            complete=bool(findings) and obs['status'] in {'PASS','FAIL_TECHNICAL'}
        rows.append({'format':original['format'],'logical_dataset_id':alias,'criterion_id':original['criterion_id'],
              'rule_version':version,'scope_id':'FOCAL_SYNTHETIC_FIXTURE_CURRENT_RULE','source_case_id':case_id,
              'status':obs['status'],'coverage_complete':complete,'fixture_sha256':original['fixture_sha256'],
              'raw_evidence':{'path':original['raw_path'],'sha256':original['raw_sha256']}})
    model={'contract':'TDL_REAUDIT_SNAPSHOT/1','execution_id':native.get('execution_id',native.get('run_id')),
           'execution_evidence':ref(native_path),'rows':rows,'scope_mapping_review':{'reviewer':'Codex authoring agent',
           'origin':'SYNTHETIC_SIMULATION','mapping':'Six explicitly labelled synthetic datasets; reviewed fixture variant pairs, no real producer or automatic cross-feed matching.'}}
    write(output,model);execution(ref(output));return model


def demo(output,replay_path):
    output=Path(output)
    if output.exists():raise ValueError('Use new scenario directory')
    output.mkdir(parents=True)
    baseline_path=ROOT/'reports/audit_precision_v1/run_20261009_final_v1/MEASUREMENT.json'
    snapshot(baseline_path,'BEFORE',output/'BEFORE.json');snapshot(replay_path,'AFTER',output/'AFTER.json')
    statement=output/'SIMULATED_RESPONSE.txt'
    statement.write_text('SIMULACION INTERNA. Productor ficticio comunica correccion. No es respuesta de un cliente real.\nAcuerdo ficticio de responsable y fecha; no es compromiso externo.\nRevision ficticia de aceptacion/cierre.\n',encoding='utf8')
    model=initialize(ref(output/'BEFORE.json'));write(output/'LEDGER_00.json',model)
    identity={c['logical_dataset_id']:cid for cid,c in model['cases'].items()}
    step=0
    def add(event):
        nonlocal model,step
        payload={'actor':'TDL synthetic scenario author','origin':'SYNTHETIC_SIMULATION',**event}
        model=append(model,payload);step+=1;write(output/f'EVENT_{step:02}.json',payload);write(output/f'LEDGER_{step:02}.json',model)
    for alias in ('SYNTH-GTFS-CORRECTED','SYNTH-NETEX-CORRECTED'):
        cid=identity[alias]
        add({'type':'PROPOSE_ACTION','case_id':cid,'action':'Correct the focal synthetic file defect and provide new version for re-audit.','owner':'Proposed synthetic producer role','date':'2026-10-16'})
        add({'type':'PRODUCER_RESPONSE','case_id':cid,'reported_state':'REPORTED_CORRECTED','statement':'Simulated producer reports correction; not verified until re-audit.','evidence':ref(statement)})
        if model['cases'][cid]['technical_state']=='RESOLVED':raise ValueError('Reported correction incorrectly resolved case')
    cid=identity['SYNTH-GTFS-CORRECTED']
    add({'type':'ACCEPT_ASSIGNMENT','case_id':cid,'owner':'Accepted synthetic producer role','date':'2026-10-20','evidence':ref(statement)})
    add({'type':'REAUDIT','evidence':ref(output/'AFTER.json')})
    counts=Counter(c['technical_state'] for c in model['cases'].values())
    if counts!={'RESOLVED':2,'PERSISTENT':2,'NEW':2}:raise ValueError('Unexpected synthetic follow-up result: '+str(counts))
    add({'type':'ACCEPTANCE','case_id':cid,'decision':'ACCEPT_CORRECTION','reviewer':'Simulated internal reviewer','rationale':'Verified focal resolution in distinct execution, simulated acceptance only.','evidence':ref(statement)})
    persistent=identity['SYNTH-GTFS-PERSISTENT']
    add({'type':'ACCEPTANCE','case_id':persistent,'decision':'ACCEPT_RISK','reviewer':'Simulated internal reviewer','rationale':'Synthetic risk acceptance does not mean technical correction.','evidence':ref(statement)})
    validate(model);write(output/'LEDGER_FINAL.json',model)
    result={'contract':'TDL_LIFECYCLE_DEMO/1','before_execution_id':model['baseline_execution_id'],
            'after_execution_id':read(output/'AFTER.json')['execution_id'],'technical_states':dict(counts),'cases':len(model['cases']),
            'events':len(model['events']),'final_ledger':ref(output/'LEDGER_FINAL.json'),
            'producer_statements':'SYNTHETIC_ONLY','human_acceptance':'SIMULATED_NOT_REAL_CLIENT_ACCEPTANCE',
            'source_findings_or_case_contract_modified':False,'destination_suitability':'NOT_DETERMINED'}
    write(output/'DEMO_RECEIPT.json',result);return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--replay',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(demo(args.output,args.replay),ensure_ascii=False))
