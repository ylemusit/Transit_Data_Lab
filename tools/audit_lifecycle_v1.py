"""Additive GTFS/NeTEx correction ledger; reported correction is not resolution.

Hashes prove integrity, not actor identity or independent human acceptance.
"""
import argparse
from copy import deepcopy
from datetime import datetime,timezone
import json
from pathlib import Path
from tools.audit_corpus_v1 import ROOT,read,write,sha
from tools.audit_replay_semantics_v1 import digest

ALLOWED_ROOTS=(ROOT/'reports/audit_lifecycle_v1',ROOT/'reports/audit_precision_v1',Path('P:/TransitDataLab/04_Runtime/AuditQuality'))
ACTIVE={'FAIL_TECHNICAL','HUMAN_REVIEW_REQUIRED'}
STATUSES={'PASS','FAIL_TECHNICAL','HUMAN_REVIEW_REQUIRED','NOT_EVALUABLE','NOT_APPLICABLE','INSPECTION_ERROR'}


def evidence(ref):
    path=Path(ref['path']).resolve(strict=True)
    if any(p.casefold()=='holdout' for p in path.parts) or not any(path.is_relative_to(r.resolve()) for r in ALLOWED_ROOTS):raise ValueError('Evidence outside permitted task roots')
    if not path.is_file() or sha(path)!=ref['sha256']:raise ValueError('Evidence missing or changed')
    return path


def key(row):
    return digest([row['format'],row['logical_dataset_id'],row['criterion_id'],row['scope_id']])[:24]


def execution(ref):
    model=read(evidence(ref))
    if model['contract']!='TDL_REAUDIT_SNAPSHOT/1' or not model['execution_id']:raise ValueError('Unknown execution snapshot')
    native=read(evidence(model['execution_evidence']))
    actual_id=native.get('execution_id',native.get('run_id'))
    if model['execution_id']!=actual_id:raise ValueError('Execution identity not linked to native receipt')
    native_rows={r['case_id']:r for r in native['rows']};seen=set()
    for row in model['rows']:
        if key(row) in seen:raise ValueError('Duplicate scope identity')
        seen.add(key(row))
        if row['status'] not in STATUSES or not row['rule_version']:raise ValueError('Invalid rule state/version')
        original=native_rows[row['source_case_id']]
        if row['criterion_id']!=original['criterion_id'] or row['format']!=original['format'] or row['status']!=original['observed']['status'] or row['fixture_sha256']!=original['fixture_sha256']:raise ValueError('Snapshot disagrees with executed result')
        if row['raw_evidence']['sha256']!=original['raw_sha256'] or evidence(row['raw_evidence'])!=Path(original['raw_path']).resolve():raise ValueError('RAW evidence not linked')
        raw_rule=original['observed'].get('raw_rule_result')
        if raw_rule:
            version=raw_rule.get('semantic_version',raw_rule.get('version',raw_rule.get('rule_version')))
            coverage=raw_rule.get('coverage',{}).get('state')
            complete=original['observed']['status'] in {'PASS','FAIL_TECHNICAL'} and (coverage in {'FULL','FEATURE_PRESENT_FULLY_AUDITED'} or raw_rule.get('checked_rows',0)>0)
        else:
            findings=original['observed'].get('findings',[])
            version=findings[0]['rule_version'] if findings else '1.0.0'
            complete=bool(findings) and original['observed']['status'] in {'PASS','FAIL_TECHNICAL'}
        if row['rule_version']!=version or row['coverage_complete']!=complete:raise ValueError('Version or coverage not linked to native rule')
    return model


def initial_case(row,execution_id):
    return {'case_id':key(row),'format':row['format'],'logical_dataset_id':row['logical_dataset_id'],
        'criterion_id':row['criterion_id'],'rule_version':row['rule_version'],'scope_id':row['scope_id'],
        'technical_state':'OPEN','producer_status':'NO_RESPONSE','acceptance':'NOT_ACCEPTED',
        'owner_proposed':None,'owner_accepted':None,'date_proposed':None,'date_accepted':None,
        'action_proposed':None,'last_execution_id':execution_id,'last_native_status':row['status'],
        'resolution_evidence':None,'destination_suitability':'NOT_DETERMINED'}


def initialize(ref):
    snapshot=execution(ref)
    cases={key(r):initial_case(r,snapshot['execution_id']) for r in snapshot['rows'] if r['status'] in ACTIVE}
    model={'contract':'TDL_CORRECTION_LEDGER/1','baseline_execution_id':snapshot['execution_id'],
           'baseline_evidence':deepcopy(ref),'cases':cases,'events':[],
           'reference_scope':'Reviewed logical dataset + criterion + scope; no fuzzy automatic finding matching.',
           'external_actor_authentication':False}
    model['genesis_sha256']=digest({'baseline':ref,'cases':cases})
    model['head_sha256']=model['genesis_sha256'];model['state_sha256']=digest(cases)
    return model


def transition(cases,event,baseline_id):
    if not event.get('actor') or event.get('origin') not in {'INTERNAL_REVIEW','PRODUCER_STATEMENT','SYNTHETIC_SIMULATION'}:raise ValueError('Actor/origin required')
    if event['type']=='PRODUCER_RESPONSE' and event['origin']=='INTERNAL_REVIEW':raise ValueError('Internal review cannot masquerade as producer response')
    if event['type']=='ACCEPTANCE' and event['origin']=='PRODUCER_STATEMENT':raise ValueError('Producer statement is not audit acceptance review')
    result=deepcopy(cases);kind=event['type']
    if kind=='REAUDIT':
        snapshot=execution(event['evidence']);new_id=snapshot['execution_id']
        if new_id==baseline_id or any(c['last_execution_id']==new_id for c in result.values()):raise ValueError('Re-audit requires a distinct execution')
        current={key(r):r for r in snapshot['rows']}
        for cid,case in result.items():
            row=current.get(cid)
            case['acceptance']='NOT_ACCEPTED'
            if row is None:
                case.update(technical_state='NOT_EVALUATED',resolution_evidence=None,last_execution_id=new_id,last_native_status='NOT_EVALUABLE');continue
            if row['rule_version']!=case['rule_version']:
                case['technical_state']='NOT_COMPARABLE';case['resolution_evidence']=None
            elif row['status']=='PASS' and row['coverage_complete']:
                case['technical_state']='RESOLVED';case['resolution_evidence']={'snapshot':event['evidence'],'execution_id':new_id,'raw':row['raw_evidence'],'source_case_id':row['source_case_id']}
            elif row['status'] in ACTIVE:
                case['technical_state']='REAPPEARED' if case['technical_state']=='RESOLVED' else 'PERSISTENT';case['resolution_evidence']=None
            else:case['technical_state']='NOT_EVALUATED';case['resolution_evidence']=None
            case['last_execution_id']=new_id;case['last_native_status']=row['status']
        for cid,row in current.items():
            if cid not in result and row['status'] in ACTIVE:
                result[cid]=initial_case(row,new_id);result[cid]['technical_state']='NEW'
        return result
    case=result[event['case_id']]
    if kind=='PROPOSE_ACTION':
        if not event.get('action'):raise ValueError('Missing action')
        case.update(action_proposed=event['action'],owner_proposed=event.get('owner'),date_proposed=event.get('date'),owner_accepted=None,date_accepted=None)
    elif kind=='PRODUCER_RESPONSE':
        if event['reported_state'] not in {'REPORTED_PENDING','REPORTED_CORRECTED','REPORTED_ACCEPTED'} or not event.get('statement'):raise ValueError('Invalid producer statement')
        evidence(event['evidence']);case['producer_status']=event['reported_state']
    elif kind=='ACCEPT_ASSIGNMENT':
        evidence(event['evidence'])
        if not case['action_proposed'] or not event.get('owner'):raise ValueError('Assignment requires proposal and explicit owner')
        case['owner_accepted']=event['owner'];case['date_accepted']=event.get('date')
    elif kind=='ACCEPTANCE':
        evidence(event['evidence'])
        if not event.get('reviewer') or not event.get('rationale'):raise ValueError('Acceptance needs reviewer and rationale')
        if event['decision']=='ACCEPT_CORRECTION':
            if case['technical_state']!='RESOLVED' or not case['resolution_evidence']:raise ValueError('Correction acceptance requires proven resolution')
            case['acceptance']='ACCEPTED_CORRECTION'
        elif event['decision']=='ACCEPT_RISK':case['acceptance']='ACCEPTED_RISK'
        else:raise ValueError('Unknown acceptance decision')
    else:raise ValueError('Unknown event')
    return result


def validate(model):
    genesis=initialize(model['baseline_evidence'])
    if model['contract']!='TDL_CORRECTION_LEDGER/1' or model['baseline_execution_id']!=genesis['baseline_execution_id']:raise ValueError('Baseline execution identity changed')
    if model['genesis_sha256']!=genesis['genesis_sha256']:raise ValueError('Genesis drift')
    cases=genesis['cases'];head=genesis['head_sha256'];executions={model['baseline_execution_id']}
    for index,record in enumerate(model['events'],1):
        body={k:v for k,v in record.items() if k!='event_sha256'}
        if record['sequence']!=index or record['previous_sha256']!=head or digest(body)!=record['event_sha256']:raise ValueError('Event history changed')
        if record['payload']['type']=='REAUDIT':
            identity=execution(record['payload']['evidence'])['execution_id']
            if identity in executions:raise ValueError('Execution already used in this history')
            executions.add(identity)
        cases=transition(cases,record['payload'],model['baseline_execution_id']);head=record['event_sha256']
    if head!=model['head_sha256'] or cases!=model['cases'] or digest(cases)!=model['state_sha256']:raise ValueError('State not derived from verified history')
    return True


def append(model,event):
    validate(model)
    if not event.get('actor') or event.get('origin') not in {'INTERNAL_REVIEW','PRODUCER_STATEMENT','SYNTHETIC_SIMULATION'}:raise ValueError('Actor/origin required; no implicit client acceptance')
    if event['type']=='PRODUCER_RESPONSE' and event['origin']=='INTERNAL_REVIEW':raise ValueError('Internal review cannot masquerade as producer response')
    if event['type']=='ACCEPTANCE' and event['origin']=='PRODUCER_STATEMENT':raise ValueError('Producer statement is not audit acceptance review')
    result=deepcopy(model);cases=transition(result['cases'],event,result['baseline_execution_id'])
    record={'sequence':len(result['events'])+1,'previous_sha256':result['head_sha256'],
            'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'payload':deepcopy(event)}
    record['event_sha256']=digest(record);result['events'].append(record)
    result['head_sha256']=record['event_sha256'];result['cases']=cases;result['state_sha256']=digest(cases)
    validate(result);return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--ledger',type=Path);source.add_argument('--baseline',type=Path)
    parser.add_argument('--event',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.baseline:
        if args.event or args.output is None or args.output.exists():raise ValueError('Initialization requires a new output and no event')
        model=initialize({'path':str(args.baseline.resolve()),'sha256':sha(args.baseline)});write(args.output,model)
    else:model=read(args.ledger)
    if args.event:
        if args.output is None or args.output.exists():raise ValueError('Output must be a new file')
        model=append(model,read(args.event));write(args.output,model)
    else:validate(model)
    print(json.dumps({'result':'PASS','events':len(model['events']),'cases':len(model['cases']),'head_sha256':model['head_sha256']}))
