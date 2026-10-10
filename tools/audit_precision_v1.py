"""Bounded execution of frozen evaluators against authored synthetic witnesses.

This is evaluator integration, not full pipeline replay or independent validation.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from tools.audit_corpus_v1 import ROOT, read, write, sha
from tools.audit_reference_integrity_v1 import verify

REFERENCE = ROOT / 'reports/audit_reference_bank_v1/accepted_reference_20261009_v1'


def classify(expected, observed):
    state = expected['criterion_state']
    status = observed['status']
    if status == 'UNIMPLEMENTED': return 'UNIMPLEMENTED'
    if observed.get('confounded'): return 'CONFOUNDED_REVIEW'
    if state in {'SATISFIED', 'VIOLATED'}:
        if status not in {'PASS', 'FAIL_TECHNICAL'}: return 'ABSTENTION'
        return {('SATISFIED','PASS'):'TN', ('SATISFIED','FAIL_TECHNICAL'):'FP',
                ('VIOLATED','PASS'):'FN', ('VIOLATED','FAIL_TECHNICAL'):'TP'}[(state,status)]
    if state == 'RECOMMENDATION_UNMET':
        return 'RECOMMENDATION_MATCH' if observed.get('recommendation_met') is False else 'RECOMMENDATION_MISMATCH'
    if state == 'NOT_APPLICABLE':
        return 'STATE_MATCH' if status == 'NOT_APPLICABLE' else 'STATE_DIFFERENCE'
    if state in {'UNKNOWN','REVIEW_REQUIRED'}:
        return 'REVIEW_PRESERVED' if status in {'NOT_EVALUABLE','HUMAN_REVIEW_REQUIRED','INSPECTION_ERROR'} else 'UNSUPPORTED_DETERMINATION_REVIEW'
    raise ValueError('Unknown expectation state: '+state)


def metrics(rows):
    groups=defaultdict(list)
    for row in rows: groups[row['criterion_id']].append(row)
    result=[]
    for rule, values in sorted(groups.items()):
        counts=Counter(v['classification'] for v in values)
        binary=sum(counts[k] for k in ('TP','TN','FP','FN'))
        negative=sum(v['expected']['criterion_state']=='VIOLATED' for v in values)
        positive=sum(v['expected']['criterion_state']=='SATISFIED' for v in values)
        result.append({'criterion_id':rule,'scenarios':len(values),'counts':dict(counts),
            'binary_decisions':binary,'expected_violations':negative,'expected_satisfied':positive,
            'false_positive_rate_decided':counts['FP']/(counts['FP']+counts['TN']) if counts['FP']+counts['TN'] else None,
            'false_negative_rate_decided':counts['FN']/(counts['FN']+counts['TP']) if counts['FN']+counts['TP'] else None,
            'violation_detection_yield':counts['TP']/negative if negative else None,
            'violation_abstentions':sum(v['classification']=='ABSTENTION' and v['expected']['criterion_state']=='VIOLATED' for v in values),
            'interpretation':'Small authored criterion witnesses; abstentions and scope conflicts are not true negatives.'})
    return result


def investigate(case, observed, raw):
    """Explain cross-rule evidence without changing native or expected statuses."""
    rid=case['criterion_id']
    findings=[]
    if rid in {'GTFS-G06-STOP-SEQUENCE','GTFS-G07-SHAPE-SEQUENCE'} and case['variant']=='negative':
        table='stop_times.txt' if 'STOP-SEQUENCE' in rid else 'shapes.txt'
        findings=[f for f in raw.get('g04',{}).get('findings',[]) if f.get('source_file')==table and f.get('rule_id')=='GTFS-G04-PRIMARY-KEY-UNIQUENESS']
        if findings:
            return {'category':'DETECTED_OTHER_RULE','reason':'Duplicate composite key detected by G04; G06/G07 only test non-negative sequence. Not a whole-auditor false negative.', 'linked_findings':findings}
    if rid=='GTFS-G07-COORDINATE-BOUNDS' and case['variant']=='negative':
        findings=[f for f in raw.get('g03',{}).get('field_types',{}).get('findings',[]) if f.get('file')=='shapes.txt' and f.get('field') in {'shape_pt_lat','shape_pt_lon'}]
        if findings:return {'category':'DETECTED_OTHER_RULE','reason':'G03 rejects coordinate value; G07 conservatively abstains after upstream rejection.', 'linked_findings':findings}
    if rid=='GTFS-G03-CSV-STRUCTURE' and observed['status']=='INSPECTION_ERROR':
        return {'category':'FAIL_SAFE_DIAGNOSTIC_DEFECT','reason':'G03 catches csv.Error as phase inspection error; input is not accepted, but no precise syntax finding emitted.', 'error':raw['g03'].get('error')}
    if rid=='GTFS-G03-FILE-CATALOG' and case['variant']=='negative':
        return {'category':'STATUS_SCOPE_DIFFERENCE','reason':'Catalog PASS describes successful inventory; unknown extension is still classified in file_catalog.members. Not a feed-conformance PASS.'}
    if rid=='GTFS-G05-SERVICE-DATE-SET' and case['variant']=='negative':
        return {'category':'STATUS_SCOPE_DIFFERENCE','reason':'G05 PASS describes computation of an empty date set; operational adequacy needs service context. Not verified service availability.'}
    if observed['status'] in {'NOT_EVALUABLE','INSPECTION_ERROR'}:
        return {'category':'ABSTENTION_REQUIRES_REVIEW','reason':'Family or prerequisite has incomplete coverage. No failure-to-detect conclusion without checking earlier rules and focal context.'}
    return {'category':'NO_DISCREPANCY_IDENTIFIED','reason':'Inspect native evidence for criterion scope; no universal inference.'}


def gtfs_observation(path, case, runtime):
    from gtfs_lab.g03_structure import inspect_g03_archive
    from gtfs_lab.ingestion import load_dataset, IngestionError
    from gtfs_lab.validation import validate
    from gtfs_lab.compliance_adapter import inspect_fixed_stop_references
    from gtfs_lab.g04_identity import evaluate_g04
    from gtfs_lab.g05_temporal import evaluate_g05
    from gtfs_lab.g06_operations import evaluate_g06
    from gtfs_lab.g07_spatial import evaluate_g07
    from gtfs_lab.g08_quality import evaluate_g08_run
    rid=case['criterion_id']; g03=inspect_g03_archive(path)
    raw={'g03':g03}; rules=list(g03['rules'])
    if not rid.startswith('GTFS-G03-'):
        try:
            ctx=load_dataset(path,runtime)
        except IngestionError as exc:
            return {'status':'NOT_EVALUABLE','reason':'INGESTION_REJECTED','error':str(exc)},raw
        legacy=validate(ctx); compliance=inspect_fixed_stop_references(ctx)
        g04=evaluate_g04(ctx,g03,legacy); g05=evaluate_g05(ctx,g03,g04)
        g06=evaluate_g06(ctx,g03,g04,g05); g07=evaluate_g07(ctx,g03,g04)
        g08=evaluate_g08_run(ctx,g03)
        raw.update(legacy=legacy,compliance=compliance,g04=g04,g05=g05,g06=g06,g07=g07,g08=g08)
        rules.extend(legacy['rules'])
        for component in (g04,g05,g06,g07,g08):rules.extend(component['rules'])
        rules.append({**compliance,'status':compliance['result']})
    matches=[r for r in rules if r['rule_id']==rid]
    if len(matches)!=1:raise ValueError('Rule result missing or duplicated: '+rid)
    rule=matches[0]
    # A family result can include fields other than the authored criterion.
    # Keep broad results and require a target witness for family-level failure.
    targets={'GTFS-G03-FIELD-TYPE':('routes.txt',{'route_text_color'}),
             'GTFS-G03-HEADER-SCHEMA':('routes.txt',{'agency_id','route_id'}),
             'GTFS-G04-REFERENCE-EXISTENCE':('stops.txt',{'parent_station'}),
             'GTFS-G04-IDENTITY-DOMAIN':('trips.txt',{'service_id'}),
             'GTFS-G04-PRIMARY-KEY-UNIQUENESS':('stops.txt',{'stop_id'})}
    focal=[]
    if rid in targets:
        table,fields=targets[rid]
        for f in rule.get('findings',[]):
            file=f.get('file',f.get('source_file',f.get('table')))
            declared=f.get('source_fields',f.get('fields',[f.get('field')]))
            if isinstance(declared,str):declared=[declared]
            if file==table and fields.intersection(declared):focal.append(f)
    observed={'status':rule['status'],'raw_rule_result':rule,
              'recommendation_met':rule.get('recommendation_met'),
              'adapter':'Original evaluators; raw family status retained; no whole-feed score.'}
    if rid in targets and rule['status']=='FAIL_TECHNICAL' and not focal:
        observed['confounded']=True
        observed['reason']='Family failure without finding linked to focal table/field; inspect raw evidence.'
    observed['focal_findings']=focal
    return observed,raw


def netex_observation(path, case):
    from netex_lab.audit import audit
    raw=audit(path);rid=case['criterion_id']
    rows=[f for f in raw['findings'] if f['rule_id']==rid]
    if rows:
        statuses={r['status'] for r in rows}
        status=next(s for s in ('FAIL_TECHNICAL','INSPECTION_ERROR','NOT_EVALUABLE','HUMAN_REVIEW_REQUIRED','PASS') if s in statuses)
        return {'status':status,'findings':rows,'adapter':'Native finding status'},raw
    if rid=='NETEX-IDENTITY-001' and raw['records'] and all(r['structural_inventory'] is not None for r in raw['records']):
        if any(r['structural_inventory']['duplicate_ids'] for r in raw['records']):raise ValueError('Missing duplicate diagnostic')
        return {'status':'PASS','adapter':'Scoped absence of duplicate-id diagnostic confirmed from structural inventory; not native PASS finding.'},raw
    return {'status':'NOT_EVALUABLE','adapter':'Rule has no result after XML intake rejection; never infer PASS.'},raw


def run(output, runtime):
    output=Path(output);runtime=Path(runtime)
    if output.exists() or runtime.exists():raise ValueError('Use fresh output and runtime directories')
    if not runtime.resolve().is_relative_to(Path('P:/TransitDataLab/04_Runtime').resolve()):raise ValueError('Runtime outside authorized root')
    integrity=verify(REFERENCE); bank=read(REFERENCE/'REFERENCE_BANK.json')
    inv=read(ROOT/'reports/audit_foundation_v1/accepted_reference_20261008/CONTROL_INVENTORY.json')
    protected={r['path']:r['sha256'] for item in inv['GTFS']+inv['NETEX'] for r in [item['implementation']]+item.get('test_sources',[])}
    protected['tools/compliance_v1_engine.py']=sha(ROOT/'tools/compliance_v1_engine.py')
    for name,digest in protected.items():
        if sha(ROOT/name)!=digest:raise ValueError('Protected input drift: '+name)
    sys.path[:0]=[str(ROOT/'02_Data_Engineering/GTFS_Lab'),str(ROOT/'02_Data_Engineering/NeTEx_Lab')]
    output.mkdir(parents=True);runtime.mkdir(parents=True)
    rows=[]
    for case in bank['cases']:
        path=Path(bank['fixture_root'])/case['fixture']
        if path.name!=case['fixture'] or sha(path)!=case['sha256']:raise ValueError('Fixture drift or unsafe path')
        if case['scope']!='CURRENT_RULE_ILLUSTRATION':
            observed={'status':'UNIMPLEMENTED','reason':'Candidate family, no approved evaluator'};raw={}
        elif case['format']=='GTFS_SCHEDULE':observed,raw=gtfs_observation(path,case,runtime)
        else:observed,raw=netex_observation(path,case)
        name=case['case_id']+'.json';raw_path=runtime/'raw'/name;write(raw_path,raw)
        classification=classify(case['expected'],observed)
        investigation=investigate(case,observed,raw)
        if investigation['category']=='DETECTED_OTHER_RULE':classification='DETECTED_OTHER_RULE'
        if investigation['category']=='STATUS_SCOPE_DIFFERENCE':classification='STATUS_SCOPE_DIFFERENCE'
        rows.append({'case_id':case['case_id'],'criterion_id':case['criterion_id'],'format':case['format'],
            'fixture_sha256':case['sha256'],'expected':case['expected'],'observed':observed,
            'initial_comparison':classify(case['expected'],observed),'classification':classification,'investigation':investigation,
            'raw_path':str(raw_path.resolve()),'raw_sha256':sha(raw_path)})
    post=verify(REFERENCE)
    for name,digest in protected.items():
        if sha(ROOT/name)!=digest:raise ValueError('Protected input modified: '+name)
    result={'contract':'TDL_PRECISION_MEASUREMENT/1','run_id':output.name,'executed_at_utc':datetime.now(timezone.utc).isoformat(),
        'reference_manifest_sha256':integrity['manifest_sha256'],'rows':rows,'per_criterion':metrics(rows),
        'counts':dict(Counter(r['classification'] for r in rows)),
        'engine_inputs':protected,'reference_verified_before_and_after':integrity==post,
        'tool_identity':{name:sha(ROOT/'tools'/name) for name in ('audit_precision_v1.py','audit_battery_plan_v1.py','test_audit_precision_v1.py')},
        'external_validator':{'status':'NOT_EXECUTED','reason':'No pinned external GTFS validator included in this execution; lxml is also the NeTEx engine dependency, not an independent comparator.'},
        'holdout_accessed':False,'full_pipeline_replay':False,'independent_human_review':False,
        'global_accuracy':None,'limits':['114 authored synthetic witnesses, not random samples or operator feeds.',
        'Family status may abstain or contain unrelated defects; inspect raw evidence.',
        'Candidate graph is not NeTEx XML. EPIP full controlled text absent.',
        'External comparative validation remains pending; no claim of universal accuracy.']}
    write(output/'MEASUREMENT.json',result)
    return {'output':str(output),'scenarios':len(rows),'counts':result['counts']}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--runtime',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(run(args.output,args.runtime),ensure_ascii=False))
