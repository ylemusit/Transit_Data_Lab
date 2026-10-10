"""Internal service journey: immutable, evidence-linked stage records.

This adapter records internal synthetic exercises, never external delivery or
client consent. Native executions and correction ledger retain their authority.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from tools.audit_corpus_v1 import ROOT, read, sha
from tools.audit_lifecycle_v1 import execution, validate as validate_ledger
from tools.audit_replay_semantics_v1 import digest

RUNTIME = Path('P:/TransitDataLab/04_Runtime/AuditQuality')
REPORT = ROOT / 'reports/audit_service_v1'
STAGES = ('RECEIVED', 'SCOPE_AGREED_INTERNAL', 'ANALYSIS_REFERENCED',
          'REVIEWED_INTERNAL', 'DELIVERED_INTERNAL', 'RESPONSE_RECORDED',
          'REAUDITED', 'ACCEPTANCE_RECORDED')
ROLES = ('Recepción de datos', 'Responsable del servicio', 'Analista del formato',
         'Revisor de auditoría', 'Responsable de entrega', 'Gestor de respuestas',
         'Analista del formato', 'Responsable del servicio')
ROOTS = (RUNTIME, REPORT, ROOT / 'reports/audit_lifecycle_v1',
         ROOT / 'reports/audit_precision_v1')


def reference(path):
    return {'path': str(Path(path).resolve()), 'sha256': sha(Path(path))}


def evidence(ref):
    path = Path(ref['path']).resolve(strict=True)
    if any(p.casefold() == 'holdout' for p in path.parts):
        raise ValueError('Protected evidence')
    if not path.is_file() or not any(path.is_relative_to(r.resolve()) for r in ROOTS):
        raise ValueError('Evidence outside internal service roots')
    if sha(path) != ref['sha256']:
        raise ValueError('Evidence changed')
    return path


def save(path, model):
    path = Path(path).resolve()
    if not path.is_relative_to(RUNTIME.resolve()) and not path.is_relative_to(REPORT.resolve()):
        raise ValueError('Output outside internal service roots')
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: previous versions are never replaced.
    with path.open('x', encoding='utf-8') as stream:
        json.dump(model, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def start(service_id, format_name):
    if not service_id or format_name not in {'GTFS_SCHEDULE', 'NETEX'}:
        raise ValueError('Service identity and supported format required')
    model = {'contract': 'TDL_INTERNAL_SERVICE_JOURNEY/1', 'service_id': service_id,
             'format': format_name, 'scope': 'INTERNAL_SYNTHETIC_REFERENCE_WORKFLOW',
             'events': [], 'state': {}, 'external_delivery': False,
             'client_acceptance': 'NOT_OBTAINED', 'actor_authentication': False}
    model['genesis_sha256'] = digest({k: v for k, v in model.items() if k != 'events'})
    model['head_sha256'] = model['genesis_sha256']
    return model


def package_check(ref, snapshot_ref, format_name):
    path = evidence(ref); model = read(path)
    snap = execution(snapshot_ref)
    rows = [r for r in snap['rows'] if r['format'] == format_name]
    if (model['contract'] != 'TDL_INTERNAL_SERVICE_DELIVERY/1'
            or model['format'] != format_name or model['snapshot'] != snapshot_ref
            or model['execution_id'] != snap['execution_id'] or model['rows'] != rows):
        raise ValueError('Delivery identity/source/version mismatch')
    for name, expected in model['files'].items():
        target = (path.parent / name).resolve(strict=True)
        if not target.is_relative_to(path.parent) or sha(target) != expected:
            raise ValueError('Delivery inventory changed or escaped package')
    if not {'DIRECCION.md', 'TECNICO.md'} <= set(model['files']):
        raise ValueError('Both audiences required')
    for i, row in enumerate(rows, 1):
        if model['files'].get(f'evidence/RAW_{i:02}.json') != row['raw_evidence']['sha256']:
            raise ValueError('Delivery omitted or substituted native evidence')
    return model


def ledger_check(ref, prior_ref, baseline_id):
    model = read(evidence(ref)); validate_ledger(model)
    if model['baseline_execution_id'] != baseline_id:
        raise ValueError('Unrelated correction history')
    if prior_ref:
        prior = read(evidence(prior_ref)); validate_ledger(prior)
        if (model['genesis_sha256'] != prior['genesis_sha256']
                or model['events'][:len(prior['events'])] != prior['events']):
            raise ValueError('Correction history rolled back or diverged')
    return model


def reduce_stage(state, event, format_name):
    result = deepcopy(state); stage = event['stage']; refs = event['evidence']
    if event.get('origin') != 'INTERNAL_SYNTHETIC_EXERCISE' or not event.get('actor'):
        raise ValueError('Internal origin/actor required; no client attribution')
    if event.get('external_delivery', False) or event.get('client_acceptance', False):
        raise ValueError('This adapter cannot authorize external acts')
    for ref in refs.values():
        evidence(ref)
    if stage == 'RECEIVED':
        snap = execution(refs['snapshot']); rows = [r for r in snap['rows'] if r['format'] == format_name]
        if not rows:
            raise ValueError('No input of requested format')
        result.update(baseline_snapshot=refs['snapshot'], baseline_execution_id=snap['execution_id'],
                      input_versions=[{'dataset': r['logical_dataset_id'], 'source_case_id': r['source_case_id'],
                                       'sha256': r['fixture_sha256']} for r in rows])
    elif stage == 'SCOPE_AGREED_INTERNAL':
        plan = read(evidence(refs['plan'])); snap = execution(result['baseline_snapshot'])
        expected = sorted({r['criterion_id'] for r in snap['rows'] if r['format'] == format_name})
        if (plan['format'] != format_name or plan['criteria'] != expected
                or plan['agreement_origin'] != 'INTERNAL_SCENARIO_PLAN'
                or plan['profile_claim'] != 'NOT_EVALUATED'):
            raise ValueError('Scope disagrees with received evidence')
        result['scope_plan'] = refs['plan']
    elif stage == 'ANALYSIS_REFERENCED':
        if refs['snapshot'] != result['baseline_snapshot']:
            raise ValueError('Analysis substituted a received version')
        execution(refs['snapshot'])
        result['analysis_mode'] = 'EXISTING_EXECUTED_EVIDENCE_NO_NEW_ENGINE_RUN'
    elif stage == 'REVIEWED_INTERNAL':
        review = read(evidence(refs['review']))
        if (review['snapshot'] != result['baseline_snapshot'] or review['format'] != format_name
                or review['result'] != 'PASS_WITH_LIMITATIONS'
                or review['review_kind'] != 'AUTHOR_SELF_REVIEW'
                or review['human_emission_approval'] is not False):
            raise ValueError('Review not linked or overclaims human approval')
        result['review'] = refs['review']
    elif stage == 'DELIVERED_INTERNAL':
        package_check(refs['package'], result['baseline_snapshot'], format_name)
        ledger_check(refs['ledger'], None, result['baseline_execution_id'])
        result.update(delivery_v1=refs['package'], latest_ledger=refs['ledger'],
                      handoff='INTERNAL_ONLY_NOT_SENT_TO_CLIENT')
    elif stage == 'RESPONSE_RECORDED':
        ledger = ledger_check(refs['ledger'], result['latest_ledger'], result['baseline_execution_id'])
        responses = [e for e in ledger['events'] if e['payload']['type'] == 'PRODUCER_RESPONSE'
                     and ledger['cases'][e['payload']['case_id']]['format'] == format_name]
        if not responses or any(e['payload']['origin'] != 'SYNTHETIC_SIMULATION' for e in responses):
            raise ValueError('Synthetic response evidence required')
        if any(e['payload']['type'] == 'REAUDIT' for e in ledger['events']):
            raise ValueError('Response stage cannot import a future re-audit/closure')
        result.update(latest_ledger=refs['ledger'], responses='SYNTHETIC_ONLY')
    elif stage == 'REAUDITED':
        snap = execution(refs['snapshot'])
        ledger = ledger_check(refs['ledger'], result['latest_ledger'], result['baseline_execution_id'])
        audits = [e for e in ledger['events'] if e['payload']['type'] == 'REAUDIT']
        if (snap['execution_id'] == result['baseline_execution_id'] or not audits
                or audits[-1]['payload']['evidence'] != refs['snapshot']):
            raise ValueError('Distinct linked re-audit required')
        package_check(refs['package'], refs['snapshot'], format_name)
        result.update(latest_ledger=refs['ledger'], reaudit_snapshot=refs['snapshot'],
                      reaudit_execution_id=snap['execution_id'], delivery_v2=refs['package'])
    elif stage == 'ACCEPTANCE_RECORDED':
        ledger = ledger_check(refs['ledger'], result['latest_ledger'], result['baseline_execution_id'])
        if any(c['last_execution_id'] != result['reaudit_execution_id'] for c in ledger['cases'].values()):
            raise ValueError('Acceptance substituted a different re-audit')
        result['latest_ledger'] = refs['ledger']
        result['cases'] = {k: v for k, v in ledger['cases'].items() if v['format'] == format_name}
        result['technical_states'] = dict(Counter(c['technical_state'] for c in result['cases'].values()))
        result['acceptance_states'] = dict(Counter(c['acceptance'] for c in result['cases'].values()))
        result['journey_completed'] = True
        result['issues_all_resolved'] = all(c['technical_state'] == 'RESOLVED' for c in result['cases'].values())
        result['client_acceptance'] = 'NOT_OBTAINED'
    result['stage'] = stage
    return result


def validate(model):
    genesis = start(model['service_id'], model['format'])
    for name in ('contract', 'scope', 'external_delivery', 'client_acceptance', 'actor_authentication', 'genesis_sha256'):
        if model[name] != genesis[name]:
            raise ValueError('Service identity or internal boundaries changed')
    state = {}; head = genesis['head_sha256']
    for i, record in enumerate(model['events']):
        body = {k: v for k, v in record.items() if k != 'event_sha256'}
        if (i >= len(STAGES) or record['sequence'] != i + 1 or record['previous_sha256'] != head
                or record['payload']['stage'] != STAGES[i] or digest(body) != record['event_sha256']
                or record['role_proposed'] != ROLES[i] or record['person_assigned'] is not None):
            raise ValueError('Journey sequence/history/roles changed')
        state = reduce_stage(state, record['payload'], model['format']); head = record['event_sha256']
    if state != model['state'] or head != model['head_sha256']:
        raise ValueError('State is not derived from evidence history')
    return True


def advance(model, event):
    validate(model); i = len(model['events'])
    if i >= len(STAGES) or event.get('stage') != STAGES[i]:
        raise ValueError('Stage out of order or journey already complete')
    state = reduce_stage(model['state'], event, model['format'])
    result = deepcopy(model)
    record = {'sequence': i + 1, 'previous_sha256': model['head_sha256'],
              'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
              'role_proposed': ROLES[i], 'person_assigned': None, 'payload': deepcopy(event)}
    record['event_sha256'] = digest(record); result['events'].append(record)
    result['head_sha256'] = record['event_sha256']; result['state'] = state
    validate(result); return result


def build_package(output, snapshot_ref, format_name):
    output = Path(output).resolve()
    if not output.is_relative_to(RUNTIME.resolve()) or output.exists():
        raise ValueError('New private runtime package required')
    output.mkdir(parents=True)
    snap = execution(snapshot_ref); rows = [r for r in snap['rows'] if r['format'] == format_name]
    counts = dict(Counter(r['status'] for r in rows)); files = []
    tech = [f'# Detalle técnico interno — {format_name}', '',
            'Escenarios sintéticos focales; no es un feed de operador ni una auditoría nueva.',
            f"Ejecución de referencia: `{snap['execution_id']}`.", '']
    for i, row in enumerate(rows, 1):
        target = output / 'evidence' / f'RAW_{i:02}.json'; target.parent.mkdir(exist_ok=True)
        original = evidence(row['raw_evidence']); shutil.copyfile(original, target)
        if sha(target) != row['raw_evidence']['sha256']:
            raise ValueError('RAW copy changed')
        files.append(target)
        tech += [f"## {row['logical_dataset_id']}",
                 f"Criterio `{row['criterion_id']}` versión `{row['rule_version']}`; estado `{row['status']}`.",
                 f"Fuente/variante: `{row['source_case_id']}`; SHA-256 `{row['fixture_sha256']}`.",
                 f"Cobertura completa focal: {row['coverage_complete']}. [Evidencia RAW](evidence/{target.name}).", '']
    (output / 'TECNICO.md').write_text('\n'.join(tech), encoding='utf-8')
    (output / 'DIRECCION.md').write_text(
        f'# Resumen interno — {format_name}\n\nTres escenarios sintéticos. Estados: {json.dumps(counts)}.\n\n'
        'La cobertura se limita a los criterios/variantes enumerados. No acredita destino, perfil ni cumplimiento legal.\n\n'
        '[Ir al detalle técnico](TECNICO.md). Propuesta: revisar incidencias y acordar respuesta; no hay cliente real.\n', encoding='utf-8')
    files += [output / 'TECNICO.md', output / 'DIRECCION.md']
    model = {'contract': 'TDL_INTERNAL_SERVICE_DELIVERY/1', 'format': format_name,
             'snapshot': snapshot_ref, 'execution_id': snap['execution_id'], 'rows': rows,
             'files': {p.relative_to(output).as_posix(): sha(p) for p in files}}
    save(output / 'PACKAGE.json', model); package_check(reference(output / 'PACKAGE.json'), snapshot_ref, format_name)
    return reference(output / 'PACKAGE.json')


def demo(output):
    output = Path(output).resolve()
    if not output.is_relative_to(RUNTIME.resolve()) or output.exists():
        raise ValueError('Use a new service runtime directory')
    output.mkdir(parents=True)
    source = ROOT / 'reports/audit_lifecycle_v1/scenarios_20261009_final_v2'
    before = reference(source / 'BEFORE.json'); after = reference(source / 'AFTER.json')
    receipt = {'task': 'TDL-AUD-21', 'result': 'PASS_INTERNAL_WITH_LIMITATIONS', 'journeys': [],
               'external_contact': False, 'new_engine_execution': False}
    for fmt in ('GTFS_SCHEDULE', 'NETEX'):
        case = output / fmt; case.mkdir()
        rows = [r for r in execution(before)['rows'] if r['format'] == fmt]
        save(case / 'SCOPE_PLAN.json', {'format': fmt, 'criteria': sorted({r['criterion_id'] for r in rows}),
            'profile_claim': 'NOT_EVALUATED', 'agreement_origin': 'INTERNAL_SCENARIO_PLAN',
            'destination': 'INTERNAL_REFERENCE_ONLY', 'client_agreement': False})
        save(case / 'REVIEW.json', {'format': fmt, 'snapshot': before, 'result': 'PASS_WITH_LIMITATIONS',
             'review_kind': 'AUTHOR_SELF_REVIEW', 'human_emission_approval': False,
             'checks': ['version_identity', 'coverage_and_units', 'raw_hashes', 'both_audiences', 'synthetic_limits'],
             'reviewer': 'Codex authoring agent', 'independent_reviewer': None})
        v1 = build_package(case / 'DELIVERY_V1', before, fmt); v2 = build_package(case / 'DELIVERY_V2', after, fmt)
        evidence_sets = [{'snapshot': before}, {'plan': reference(case / 'SCOPE_PLAN.json')},
            {'snapshot': before}, {'review': reference(case / 'REVIEW.json')},
            {'package': v1, 'ledger': reference(source / 'LEDGER_00.json')},
            {'ledger': reference(source / 'LEDGER_04.json')},
            {'snapshot': after, 'ledger': reference(source / 'LEDGER_06.json'), 'package': v2},
            {'ledger': reference(source / 'LEDGER_08.json')}]
        model = start('TDL-SERVICE-20261009-' + fmt, fmt); save(case / 'JOURNEY_00.json', model)
        for i, (stage, refs) in enumerate(zip(STAGES, evidence_sets), 1):
            event = {'stage': stage, 'actor': 'Codex internal exercise',
                     'origin': 'INTERNAL_SYNTHETIC_EXERCISE', 'evidence': refs}
            save(case / f'EVENT_{i:02}.json', event); model = advance(model, event)
            save(case / f'JOURNEY_{i:02}.json', model)
        validate(model)
        receipt['journeys'].append({'format': fmt, 'events': len(model['events']),
            'final_record': reference(case / 'JOURNEY_08.json'),
            'versions_preserved': ['DELIVERY_V1', 'DELIVERY_V2'],
            'technical_states': model['state']['technical_states'],
            'acceptance_states': model['state']['acceptance_states'], 'client_acceptance': 'NOT_OBTAINED'})
    save(output / 'RECEIPT.json', receipt); return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--demo', type=Path); group.add_argument('--record', type=Path)
    group.add_argument('--start', dest='service_id')
    parser.add_argument('--format', choices=['GTFS_SCHEDULE', 'NETEX'])
    parser.add_argument('--event', type=Path); parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.demo:
        print(json.dumps(demo(args.demo), ensure_ascii=False))
    else:
        model = start(args.service_id, args.format) if args.service_id else read(args.record)
        if args.event:
            model = advance(model, read(args.event))
        validate(model)
        if args.service_id or args.event:
            if not args.output:
                raise ValueError('New output required')
            save(args.output, model)
        print(json.dumps({'result': 'PASS', 'events': len(model['events']), 'state': model['state']}, ensure_ascii=False))
