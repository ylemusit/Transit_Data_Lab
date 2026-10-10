"""Verify the bounded battery design and its precision measurement evidence."""
import argparse
from collections import Counter
from pathlib import Path
import json
from tools.audit_external_review_v1 import review_row
from tools.audit_corpus_v1 import ROOT, read, sha
from tools.audit_precision_v1 import REFERENCE, classify, investigate, metrics
from tools.audit_battery_plan_v1 import validate, source_row
from tools.audit_reference_integrity_v1 import verify


def check(plan_path,measurement_path):
    plan=read(plan_path);validate(plan);measurement=read(measurement_path)
    reference=verify(REFERENCE);bank=read(REFERENCE/'REFERENCE_BANK.json')
    cases={c['case_id']:c for c in bank['cases']}
    rows=measurement['rows']
    if len(rows)!=len(cases) or {r['case_id'] for r in rows}!=set(cases):raise ValueError('Missing or duplicated cases')
    if measurement['reference_manifest_sha256']!=reference['manifest_sha256']:raise ValueError('Reference identity mismatch')
    for row in rows:
        case=cases[row['case_id']]
        if row['criterion_id']!=case['criterion_id'] or row['expected']!=case['expected']:raise ValueError('Expected criterion changed')
        fixture=Path(bank['fixture_root'])/case['fixture']
        if sha(fixture)!=row['fixture_sha256'] or row['fixture_sha256']!=case['sha256']:raise ValueError('Fixture changed')
        raw_path=Path(row['raw_path'])
        if not raw_path.resolve().is_relative_to(Path('P:/TransitDataLab/04_Runtime/AuditQuality').resolve()):raise ValueError('RAW outside execution root')
        if sha(raw_path)!=row['raw_sha256']:raise ValueError('RAW changed')
        initial=classify(row['expected'],row['observed'])
        review=investigate(case,row['observed'],read(raw_path))
        revised=review['category'] if review['category'] in {'DETECTED_OTHER_RULE','STATUS_SCOPE_DIFFERENCE'} else initial
        if row['initial_comparison']!=initial or row['investigation']!=review or row['classification']!=revised:raise ValueError('Comparison review drift')
    if measurement['per_criterion']!=metrics(rows) or measurement['counts']!=dict(Counter(r['classification'] for r in rows)):raise ValueError('Metric mismatch')
    for name,digest in measurement['engine_inputs'].items():
        if sha(ROOT/name)!=digest:raise ValueError('Protected evaluator changed')
    for name,digest in measurement['tool_identity'].items():
        if sha(ROOT/'tools'/name)!=digest:raise ValueError('Measurement tool changed')
    input_paths={'inventory_sha256':ROOT/'reports/audit_foundation_v1/accepted_reference_20261008/CONTROL_INVENTORY.json',
                 'bank_sha256':REFERENCE/'REFERENCE_BANK.json',
                 'gtfs_spec_sha256':ROOT/'03_Compliance/reports/evidence/compliance_v1_20260928/sources/gtfs_reference.md'}
    for key,path in input_paths.items():
        if plan['inputs'][key]!=sha(path):raise ValueError('Plan input drift')
    spec=input_paths['gtfs_spec_sha256'].read_text(encoding='utf8')
    for p in plan['proposals']:
        if 'source_selector' in p:
            selector=p['source_selector'];file=selector['section'].removeprefix('### ')
            if source_row(spec,file,selector['field'])!=selector:raise ValueError('Criterion selector changed')
    if measurement['global_accuracy'] is not None or measurement['holdout_accessed'] or measurement['full_pipeline_replay']:raise ValueError('Unsupported scope claim')
    ext_path=Path(measurement_path).parent.parent/'EXTERNAL_COMPARISON.json'
    review_path=ext_path.parent/'EXTERNAL_REVIEW.json'
    ext=read(ext_path);review=read(review_path)
    if sha(Path(ext['download']['asset']))!=ext['download']['sha256'] or ext['download']['sha256']!=ext['download']['expected_sha256']:raise ValueError('External jar changed')
    if ext['tool_sha256']!=sha(ROOT/'tools/audit_external_comparison_v1.py') or review['review_code_sha256']!=sha(ROOT/'tools/audit_external_review_v1.py'):raise ValueError('External tool drift')
    if review['external_receipt_sha256']!=sha(ext_path) or review['internal_measurement_sha256']!=sha(measurement_path):raise ValueError('External review input drift')
    current_gtfs={c['case_id'] for c in cases.values() if c['format']=='GTFS_SCHEDULE' and c['scope']=='CURRENT_RULE_ILLUSTRATION'}
    if len(ext['rows'])!=96 or {r['case_id'] for r in ext['rows']}!=current_gtfs:raise ValueError('Incomplete external corpus')
    internal={r['case_id']:r for r in rows}
    reviewed=[]
    for row in ext['rows']:
        if row['fixture_sha256']!=cases[row['case_id']]['sha256']:raise ValueError('External fixture mismatch')
        path=Path(row['report_path'])
        if sha(path)!=row['report_sha256'] or read(path)['notices']!=row['notices']:raise ValueError('External report drift')
        syspath=Path(row['system_errors_path'])
        if sha(syspath)!=row['system_errors_sha256'] or read(syspath)['notices']!=row['system_notices']:raise ValueError('External errors drift')
        for name,digest in row['logs'].items():
            if sha(path.parent/name)!=digest:raise ValueError('External log drift')
        if '-svu' not in row['command'] or '-u' in row['command']:raise ValueError('Wrong external invocation')
        reviewed.append(review_row(row,internal[row['case_id']]))
    if reviewed!=review['rows']:raise ValueError('External interpretation drift')
    return {'result':'PASS','cases':len(rows),'raw_verified':len(rows),'protected_inputs_verified':len(measurement['engine_inputs']),
            'reference_manifest_sha256':reference['manifest_sha256'],'plan_proposals':len(plan['proposals']),
            'counts':measurement['counts'],'task_states':{'TDL-AUD-10':'COMPLETADA_DISENO','TDL-AUD-11':'COMPLETADA_DISENO','TDL-AUD-15':'COMPLETADA_MEDICION_DELIMITADA'},
            'independent_human_review':False,'external_comparison_executed':True,'external_reports_verified':len(reviewed),
            'external_system_error_cases':review['external_system_error_cases']}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--plan',type=Path,required=True);parser.add_argument('--measurement',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(check(args.plan,args.measurement),ensure_ascii=False))
