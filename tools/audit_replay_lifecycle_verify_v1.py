"""Recompute replay equivalence and correction history from preserved evidence."""
import argparse
from collections import Counter
import json
from pathlib import Path
from tools.audit_corpus_v1 import ROOT,read,sha
from tools.audit_precision_v1 import REFERENCE,investigate
from tools.audit_reference_integrity_v1 import verify
from tools.audit_replay_semantics_v1 import semantic,digest
from tools.audit_lifecycle_v1 import validate,evidence


def check(preparation,ledger_path):
    prep=read(preparation);root=Path(prep['root']).resolve()
    if not root.is_relative_to(Path('P:/TransitDataLab/04_Runtime/AuditQuality').resolve()):raise ValueError('Replay root outside task scope')
    if sha(root/'REPLAY_INPUT_MANIFEST.json')!=prep['input_manifest_sha256'] or sha(root/'RUN_OFFLINE.ps1')!=prep['recipe_sha256']:raise ValueError('Replay recipe identity changed')
    manifest=read(root/'REPLAY_INPUT_MANIFEST.json')
    for name,expected in manifest['files'].items():
        path=(root/name).resolve()
        if not path.is_relative_to(root) or sha(path)!=expected:raise ValueError('Copied input changed')
    for name,expected in manifest['original_files'].items():
        if sha(Path(name))!=expected:raise ValueError('Original input changed')
    result=read(root/'REPLAY_RESULT.json')
    if sha(root/'REPLAY_RESULT.json')!=prep['result_sha256']:raise ValueError('Replay result changed')
    baseline=read(root/'BASELINE.json');cases={c['case_id']:c for c in baseline['cases']};rows=result['rows']
    if len(rows)!=114 or {r['case_id'] for r in rows}!=set(cases):raise ValueError('Incomplete replay')
    for row in rows:
        case=cases[row['case_id']];raw_path=Path(row['raw_path']).resolve()
        if not raw_path.is_relative_to(root/'execution/raw') or sha(raw_path)!=row['raw_sha256']:raise ValueError('Replay RAW changed')
        raw=read(raw_path);review=investigate(case,row['observed'],raw)
        new={'observed':row['observed'],'raw':raw,'classification':row['classification'],'investigation':review}
        old=semantic(baseline['results'][row['case_id']],baseline['normalization_roots']);current=semantic(new,[str(root),str(root/'source')])
        if digest(old)!=row['baseline_semantic_sha256'] or digest(current)!=row['replay_semantic_sha256'] or old!=current or not row['semantic_equivalent']:raise ValueError('Semantic replay difference')
    for module in result['environment']['loaded_evaluator_modules']:
        path=Path(module['path']).resolve()
        if not path.is_relative_to(root/'source') or sha(path)!=module['sha256'] or manifest['files'].get(path.relative_to(root).as_posix())!=module['sha256']:raise ValueError('Evaluator loaded outside pinned source')
    if not result['environment']['fresh_venv'] or not result['environment']['isolated_mode'] or not Path(result['environment']['prefix']).resolve().is_relative_to(root):raise ValueError('Environment not isolated')
    if result['network_guard']['evaluator_network_attempts']!=0 or not result['network_guard']['self_test_blocked']:raise ValueError('Offline execution unproven')
    if result['original_input_guard']['evaluator_read_attempts']!=0 or not result['original_input_guard']['self_test_blocked']:raise ValueError('Original input isolation unproven')
    reference=verify(REFERENCE)
    if reference['manifest_sha256']!=baseline['reference_manifest_sha256']:raise ValueError('Sealed reference changed')
    ledger=read(ledger_path);validate(ledger)
    for event in ledger['events']:
        if event['payload']['type']=='REAUDIT':
            snapshot=read(evidence(event['payload']['evidence']))
            if snapshot['execution_id']!=result['execution_id']:raise ValueError('Ledger not linked to verified replay')
    return {'result':'PASS','replay_scenarios':len(rows),'executed_current_rule_scenarios':108,'unimplemented_candidates_preserved':6,
            'semantic_equivalent':114,'raw_replay_verified':114,'pinned_inputs':len(manifest['files']),
            'original_inputs_verified':len(manifest['original_files']),'loaded_evaluator_modules':len(result['environment']['loaded_evaluator_modules']),
            'reference_manifest_sha256':reference['manifest_sha256'],'network_attempts':0,'original_input_read_attempts':0,
            'ledger_cases':len(ledger['cases']),'ledger_events':len(ledger['events']),
            'ledger_states':dict(Counter(c['technical_state'] for c in ledger['cases'].values())),
            'ledger_head_sha256':ledger['head_sha256'],'same_host':True,'independent_human_review':False,
            'producer_responses':'SYNTHETIC_SIMULATION','client_acceptance':'NOT_OBTAINED',
            'task_states':{'TDL-AUD-16':'COMPLETADA_REPLAY_DELIMITADO','TDL-AUD-17':'COMPLETADA_SEGUIMIENTO_INTERNO'}}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preparation',type=Path,required=True);parser.add_argument('--ledger',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(check(args.preparation,args.ledger),ensure_ascii=False))
