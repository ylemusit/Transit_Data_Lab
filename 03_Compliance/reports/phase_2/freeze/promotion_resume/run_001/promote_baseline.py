"""Authorized metadata promotion; every DuckDB call is read-only.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
Existing failure and review artifacts are never overwritten.
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
FREEZE = OUT.parents[1]
DB = ROOT / '03_Compliance/databases/transit_compliance.duckdb'
GTFS_DB = ROOT / '02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb'
GTFS = 'f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc'
CURRENT = '823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3'
PHASE1 = '52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5'
NEGATIVE = ['textual_fidelity_certified', 'legal_compliance_assessed',
            'format_mapping_completed', 'audit_rules_created', 'phase_3_started']
CREATED = []
CHECKS = []
CLI = shutil.which('duckdb')
NOW = datetime.now(timezone.utc).isoformat()


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write(path, content):
    if path.exists():
        raise RuntimeError('Refusing overwrite: ' + str(path))
    path.write_text(content, encoding='utf-8')
    CREATED.append(path.relative_to(ROOT).as_posix())


def js(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def csvout(path, data):
    if path.exists():
        raise RuntimeError('Refusing overwrite: ' + str(path))
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
    CREATED.append(path.relative_to(ROOT).as_posix())


def check(name, ok, actual=None, expected=None):
    CHECKS.append(dict(check=name, status='PASS' if ok else 'FAIL', actual=actual, expected=expected))
    if not ok:
        raise RuntimeError(f'{name}: expected {expected!r}, actual {actual!r}')


def arrays(raw):
    result = []
    decoder = json.JSONDecoder()
    raw = raw.strip()
    while raw:
        value, end = decoder.raw_decode(raw)
        result.append(value)
        raw = raw[end:].strip()
    return result


def run(sql, name):
    proc = subprocess.run([CLI, '-no-init', '-batch', '-bail', '-readonly', '-json', str(DB)],
                          input=sql.encode(), capture_output=True, cwd=ROOT)
    for suffix, content in [('.json', proc.stdout.decode()), ('.stderr.txt', proc.stderr.decode()),
                            ('.exit_code.txt', str(proc.returncode))]:
        write(OUT / (name + suffix), content)
    check(name + '_EXIT_CODE', proc.returncode == 0, proc.returncode, 0)
    return [r for a in arrays(proc.stdout.decode()) for r in a]


def canonical(data):
    return sorted(json.dumps(r, sort_keys=True, ensure_ascii=False) for r in data)


def git_status():
    return subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=ROOT).decode()


def main():
    check('CLI_AVAILABLE', CLI is not None, CLI, 'duckdb CLI')
    before = sha(DB)
    baseline_path = ROOT / 'project_baseline.json'
    state_path = ROOT / 'PROJECT_CURRENT_STATE.md'
    old = read(baseline_path)
    state = state_path.read_text(encoding='utf-8-sig')
    failure = read(FREEZE / 'PHASE_2_BASELINE_PROMOTION_FAILURE.json')
    candidate = read(FREEZE / 'PHASE_2_FREEZE_CANDIDATE.json')
    review = read(FREEZE / 'FINAL_RESULT.json')
    materialization = read(FREEZE.parent / 'materialization/FINAL_RESULT.json')
    status_before = git_status()
    write(OUT / 'GIT_STATUS_BEFORE.txt', status_before)
    index_path = ROOT / '.git/index'
    index_before = sha(index_path) if index_path.exists() else None
    head_before = (ROOT / '.git/HEAD').read_bytes()
    refs_before = {p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / '.git/refs').rglob('*') if p.is_file()}
    protected = {p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / '03_Compliance').rglob('*')
                 if p.is_file() and OUT not in p.parents}
    js(OUT / 'PROTECTED_FILES_BEFORE.json', protected)
    for path in [baseline_path, state_path]:
        write(OUT / (path.name + '.before'), path.read_text(encoding='utf-8'))
    check('GTFS_SHA_FORMAT', bool(re.fullmatch('[0-9a-f]{64}', GTFS)), len(GTFS), 64)
    check('GTFS_EXISTING_BASELINE', old['gtfs']['database_sha256'] == GTFS, old['gtfs']['database_sha256'], GTFS)
    check('GTFS_LIVE_AND_PREVIOUS_EVIDENCE', sha(GTFS_DB) == failure['gtfs_sha_after'] == failure['gtfs_existing_baseline_sha'] == GTFS, sha(GTFS_DB), GTFS)
    check('COMPLIANCE_ENTRY_SHA', before == candidate['database_sha256'] == CURRENT, before, CURRENT)
    check('PHASE_1_BASELINE', old['compliance']['database_sha256'] == PHASE1, old['compliance']['database_sha256'], PHASE1)
    for name in ['project_baseline.json', 'PROJECT_CURRENT_STATE.md']:
        evidence = failure['protected_files'][name]
        check('PREVIOUS_NO_MUTATION_' + name, sha(ROOT / name) == evidence['before'] == evidence['after'] and evidence['unchanged'], sha(ROOT / name), evidence['before'])
    check('PREVIOUS_FAILURE_CLASS', failure['PHASE_2_BASELINE_PROMOTION'] == 'FAIL' and len(failure['blocking_issues']) == 1 and failure['blocking_issues'][0]['check'] == 'REQUESTED_GTFS_BASELINE_SHA' and failure['blocking_issues'][0]['expected_length'] == 62 and failure['blocking_issues'][0]['actual_length'] == 64, failure['blocking_issues'], 'Single input SHA error')
    check('PREVIOUS_DATABASE_UNCHANGED', failure['DB_SHA_BEFORE'] == failure['DB_SHA_AFTER'] == before and failure['DB_CHANGED_DURING_BASELINE_PROMOTION'] == 'NO')
    check('PREVIOUS_NO_FREEZE_NO_PHASE_3', failure['PHASE_2'] == 'NOT_FORMALLY_FROZEN' and failure['phase_3_started'] is False and not (FREEZE / 'PHASE_2_FORMAL_FREEZE.json').exists() and not (FREEZE / 'PHASE_2_FORMAL_FREEZE.md').exists())
    check('PREVIOUS_GIT_EVIDENCE', failure['git_status_before'] == failure['git_status_after'] == status_before and failure['git_status_equal'] is True and not refs_before and index_before is None)
    check('APPROVED_REVIEW', review['PHASE_2_FINAL_FREEZE_REVIEW'] == 'PASS' and review['FREEZE_BLOCKERS'] == 0 and candidate['ready_for_promotion'] is True and not review['blocking_issues'])
    check('MATERIALIZATION_APPROVED', materialization['REQUIREMENTS_MATERIALIZATION'] == 'PASS' and materialization['POST_WRITE_SHA'] == CURRENT)
    for r in rows(FREEZE / 'PHASE_2_ARTIFACT_INVENTORY.csv'):
        check('INPUT_HASH_' + r['artifact_path'], sha(ROOT / r['artifact_path']) == r['sha256'], sha(ROOT / r['artifact_path']), r['sha256'])
    check('REPRODUCIBILITY', not any(r['classification'] == 'MISSING' for r in rows(FREEZE / 'PHASE_2_REPRODUCIBILITY_MATRIX.csv')))
    # Inspect exact live rows against previously approved evidence. No interpretation or gate regeneration.
    tables = run("SELECT table_schema||'.'||table_name AS id FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1", 'schema')
    live = {}
    for table in tables:
        name = table['id']
        check('SAFE_TABLE_IDENTIFIER_' + name, bool(re.fullmatch(r'[a-z_]+\.[a-z_]+', name)))
        live[name] = run('SELECT * FROM ' + name, 'snapshot_' + name.replace('.', '_'))
    approved = read(FREEZE / 'DATABASE_READ_ONLY_SNAPSHOT.json')
    after_mat = read(FREEZE.parent / 'materialization/DATABASE_AFTER.json')
    check('ALL_TABLES_APPROVED_UNCHANGED', set(live) == set(approved) == set(after_mat) and all(canonical(live[t]) == canonical(approved[t]) == canonical(after_mat[t]) for t in live))
    counts = {'source.provisions': 92, 'compliance.source_facts': 36, 'compliance.requirements': 48,
              'compliance.deadlines': 10, 'mapping.format_coverage': 0, 'audit.rules': 0}
    check('ENTRY_COUNTS', all(len(live[t]) == n for t, n in counts.items()), {t: len(live[t]) for t in counts}, counts)
    check('RECONCILIATION', review['approved_materialized_reconciliation'] == '48/48' and all(review[k] == 0 for k in ['missing', 'duplicates', 'orphans', 'conflicts']))
    check('LIMITS', candidate['external_dependencies_partial'] == 7 and candidate['functional_time_requirements'] == 5 and candidate['explicit_deadlines'] == 10 and all(candidate[k] is False for k in NEGATIVE if k in candidate))
    legal = []
    for document in live['source.documents']:
        path = Path(document['local_file'])
        if not path.is_absolute():
            path = ROOT / '03_Compliance' / path
        actual = sha(path) if path.is_file() else None
        legal.append(dict(document_id=document['document_id'], path=str(path), expected_sha256=document['source_hash'], actual_sha256=actual, status='PASS' if actual == document['source_hash'] else 'FAIL'))
    csvout(OUT / 'LEGAL_SOURCE_HASH_CHECKS.csv', legal)
    check('LEGAL_SOURCE_HASHES', len(legal) == 10 and all(r['status'] == 'PASS' for r in legal))
    suites = [('phase_1/test_phase_1_invariants.sql', 22), ('source/test_eu_2017_1926_master_structure.sql', 22)]
    suites += [('source/test_eu_2017_1926_annex_' + n + '.sql', 9) for n in ['1_1', '1_2', '1_3', '1_4', '2_1', '2_2', '2_3']]
    suites += [('phase_2/test_phase_2_post_materialization_gate.sql', 387)]
    tests = []
    for filename, expected in suites:
        path = ROOT / '03_Compliance/sql/07_tests' / filename
        output = run(path.read_text(encoding='utf-8-sig'), path.stem)
        results = [r for r in output if 'test' in r and 'status' in r]
        check('SUITE_' + path.stem, len(results) == expected and all(r['status'] == 'PASS' for r in results), {'checks': len(results), 'failed': [r for r in results if r['status'] != 'PASS']}, expected)
        tests.append(dict(suite=path.stem, status='PASS', checks=len(results), exit_code=0, sql_sha256=sha(path)))
    csvout(OUT / 'FINAL_TEST_RESULTS.csv', tests)
    print('Read-only prerequisites and all final suites PASS', flush=True)
    promoted = deepcopy(candidate)
    promoted.update(status='FROZEN', candidate_only=False, baseline_promoted=True, phase_3_started=False,
                    final_freeze_review_status='PASS', frozen_at=NOW)
    new = deepcopy(old)
    compliance = new['compliance']
    compliance['baseline_history'] = [dict(phase='Phase 1', status='FROZEN', database_sha256=PHASE1,
                                          historical_baseline=deepcopy(old['compliance']),
                                          provenance='promotion_resume/run_001/project_baseline.json.before')]
    compliance['phase_1']['database_sha256'] = PHASE1
    compliance['phase_1']['freeze_status'] = 'FROZEN'
    compliance['database_sha256'] = CURRENT
    compliance['active_baseline_phase'] = 'Phase 2'
    compliance['status'] = 'FROZEN'
    compliance['phase_2'] = promoted
    compliance['phase_2_sentinel_counts'] = {'compliance.requirements': 48, 'mapping.format_coverage': 0, 'audit.rules': 0}
    compliance['integrity_reason'] = 'Frozen Phase 1 corpus and Phase 2 requirements engine pass; textual fidelity and legal compliance are not certified.'
    for key in NEGATIVE:
        compliance[key] = False
    new['phase_2_readiness']['status'] = 'COMPLETED_FROZEN'
    new['phase_3_readiness'] = {'ready_for_planning': True, 'phase_3_started': False}
    new['baseline_promotion'] = {'promoted_at': NOW, 'scope': promoted['scope'], 'database_access': 'READ_ONLY',
                                 'formal_freeze_record': '03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.json'}
    # Only the two official metadata files are intentionally overwritten.
    baseline_path.write_text(json.dumps(new, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    start = state.index('## Compliance\n')
    end = state.index('## Interoperability\n', start)
    compliance_state = f'''## Compliance

Phase 1 legal corpus = FROZEN. Phase 2 requirements engine = FROZEN.
Alcance: EU-REG-2017-1926, versión consolidada 2024-03-04. Promoción autorizada: {NOW}.

### Database

- Ruta: `03_Compliance/databases/transit_compliance.duckdb`.
- Compliance DB SHA-256: `{CURRENT}`.
- Baseline histórico Phase 1 preservado: `{PHASE1}`.
- Acceso read-only; ninguna escritura en DuckDB durante la promoción.
- Esquemas: `source`, `compliance`, `mapping`, `audit`, `analysis`.

### Estado congelado

| Elemento | Estado |
|---|---|
| provisions | 92 |
| source facts | 36 |
| requirements | 48 aprobados/materializados (48/48) |
| deadlines | 10 registros; 10 fechas explícitas |
| dependencias externas | 7 PARTIAL |
| functional time requirements | 5 |
| Gate 1 | CLOSED |
| Gate 2 | CLOSED |
| materialization | PASS |
| freeze review | PASS; 0 bloqueos |
| mapping.format_coverage | 0; pendiente |
| audit.rules | 0; pendiente |

### Legal corpus y tests

10 documentos con URL oficial, fichero local y SHA-256 válido; 6 relaciones.
Los 92 provisions y las fuentes de Phase 1 permanecen sin cambios.
Validación final read-only: invariantes Phase 1 22/22 PASS; estructura 22/22 PASS;
anexos 7 suites, 63/63 PASS; hashes jurídicos 10/10 PASS; gate posterior 387/387 PASS.
Los tests de estado histórico y su evidencia permanecen intactos.

### Límites y exclusiones

- Annex 1.3 B-I y Annex 1.3 D-I: anomalías conocidas conservadas.
- Siete dependencias externas permanecen PARTIAL; interpretación pendiente.
- Tres valores `source.documents.local_file` son absolutos y no portables.
- textual_fidelity_certified = false; fidelidad textual NO certificada.
- legal_compliance_assessed = false; cumplimiento jurídico NO evaluado.
- format_mapping_completed = false; mapping NO completado.
- audit_rules_created = false; reglas de auditoría NO creadas.
- phase_3_started = false; Phase 3 NOT STARTED.
- Replay controlado con decisiones humanas; Gate 1/2 no tienen generador independiente.

Registros formales: `03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.md`
y `PHASE_2_FORMAL_FREEZE.json`. El FAIL anterior se conserva como
PRECONDITION_INPUT_ERROR / INCORRECT_EXPECTED_GTFS_SHA_IN_INSTRUCTION.

'''
    state = state[:start] + compliance_state + state[end:]
    state = state.replace('- Compliance Phase 1: 24/24 PASS, 10 fuentes con hash válido, 6 relaciones y baseline 2017/1926 de 92 provisions.',
                          '- Compliance Phase 1: FROZEN; baseline histórico preservado, 10 fuentes con hash válido, 6 relaciones y 92 provisions.\n- Compliance Phase 2: FROZEN; 48 requisitos, 36 source facts, 10 deadlines y 7 dependencias PARTIAL.')
    next_start = state.index('## Next planned phase\n')
    next_end = state.index('\n---\n', next_start)
    state = state[:next_start] + '''## Next planned phase

READY_FOR_PHASE_3_PLANNING = YES. Phase 3 NOT STARTED.
Phase 2 está formalmente congelada. Solo se habilita planificación futura;
no se crean mappings, reglas ni decisiones jurídicas en esta promoción.
''' + state[next_end:]
    state = state.replace('IMPLEMENTED:** raw, DuckDB, feed import, integrity baseline y GIS outputs',
                          'IMPLEMENTED:** raw, DuckDB, feed import, integrity baseline verified/frozen y GIS outputs')
    state_path.write_text(state, encoding='utf-8')
    actual_baseline = read(baseline_path)
    baseline_checks = {'JSON_valid': True, 'GTFS_SHA_correct': actual_baseline['gtfs']['database_sha256'] == GTFS,
                       'GTFS_preserved': actual_baseline['gtfs'] == old['gtfs'],
                       'Phase_1_preserved': actual_baseline['compliance']['baseline_history'][0]['historical_baseline'] == old['compliance'] and actual_baseline['compliance']['baseline_history'][0]['database_sha256'] == PHASE1,
                       'Phase_2_FROZEN': actual_baseline['compliance']['phase_2']['status'] == 'FROZEN',
                       'Phase_2_SHA_correct': actual_baseline['compliance']['database_sha256'] == CURRENT,
                       'negative_assertions_preserved': all(actual_baseline['compliance'][k] is False and actual_baseline['compliance']['phase_2'][k] is False for k in NEGATIVE),
                       'unrelated_metadata_preserved': all(actual_baseline[k] == old[k] for k in old if k not in ['compliance', 'phase_2_readiness'])}
    check('PROJECT_BASELINE_VALIDATION', all(baseline_checks.values()), baseline_checks, 'All true')
    js(FREEZE / 'PROJECT_BASELINE_VALIDATION.json', {'status': 'PASS', 'validated_at': NOW, 'sha256': sha(baseline_path), 'checks': baseline_checks})
    current_state = state_path.read_text(encoding='utf-8')
    gtfs_section = lambda text: text[text.index('## GTFS Lab\n'):text.index('## GTFS-RT Lab\n')]
    state_checks = {'Phase_1_FROZEN': 'Phase 1 legal corpus = FROZEN' in current_state,
                    'Phase_2_FROZEN': 'Phase 2 requirements engine = FROZEN' in current_state,
                    'counts_correct': all(v in current_state for v in ['| provisions | 92 |', '| source facts | 36 |', '| requirements | 48', '| deadlines | 10', '| dependencias externas | 7 PARTIAL']),
                    'Compliance_SHA_correct': CURRENT in current_state, 'GTFS_SHA_correct': GTFS in current_state,
                    'GTFS_state_preserved': gtfs_section(current_state).replace('verified/frozen ', '') == gtfs_section(state_path.with_name(state_path.name).read_text(encoding='utf-8')).replace('verified/frozen ', ''),
                    'GTFS_future_layers_pending': all(v in gtfs_section(current_state) for v in ['PLANNED / NOT IMPLEMENTED', '`core`', '`validation`', '`analysis`', 'no existe pipeline GIS reproducible']),
                    'Phase_3_NOT_STARTED': 'Phase 3 NOT STARTED' in current_state and 'phase_3_started = false' in current_state,
                    'negative_assertions_preserved': all(k + ' = false' in current_state for k in NEGATIVE),
                    'no_legal_assessment_claim': 'cumplimiento jurídico NO evaluado' in current_state}
    original_state = (OUT / 'PROJECT_CURRENT_STATE.md.before').read_text(encoding='utf-8')
    state_checks['GTFS_state_preserved'] = gtfs_section(current_state).replace('verified/frozen ', '') == gtfs_section(original_state)
    check('PROJECT_CURRENT_STATE_VALIDATION', all(state_checks.values()), state_checks, 'All true')
    js(FREEZE / 'PROJECT_CURRENT_STATE_VALIDATION.json', {'status': 'PASS', 'validated_at': NOW, 'sha256': sha(state_path), 'checks': state_checks})
    after = sha(DB)
    check('COMPLIANCE_FINAL_SHA', after == before == CURRENT, after, before)
    check('GTFS_FINAL_SHA', sha(GTFS_DB) == GTFS)
    check('PROTECTED_FILES_UNCHANGED', all(sha(ROOT / p) == value for p, value in protected.items()))
    check('GIT_INDEX_UNCHANGED', (sha(index_path) if index_path.exists() else None) == index_before)
    check('GIT_HEAD_REFS_UNCHANGED', (ROOT / '.git/HEAD').read_bytes() == head_before and {p.relative_to(ROOT).as_posix(): sha(p) for p in (ROOT / '.git/refs').rglob('*') if p.is_file()} == refs_before)
    result = dict(PHASE_2_BASELINE_PROMOTION='PASS', PHASE_2='FROZEN', corrected_gtfs_sha=GTFS,
                  gtfs_sha_length=len(GTFS), GTFS_BASELINE_VALIDATION='PASS', DB_SHA_BEFORE=before,
                  DB_SHA_AFTER=after, DB_CHANGED_DURING_BASELINE_PROMOTION='NO',
                  previous_official_compliance_baseline_sha=PHASE1, new_official_compliance_baseline_sha=CURRENT,
                  phase_1_baseline_preserved=True, gtfs_baseline_preserved=True,
                  provisions=92, source_facts=36, requirements=48, deadlines=10, external_dependencies_partial=7,
                  gate_1='CLOSED', gate_2='CLOSED', materialization='PASS', freeze_review='PASS',
                  tests=tests, legal_hashes='PASS (10/10)', baseline_validation='PASS', current_state_validation='PASS',
                  known_limitations=review['known_limitations'] + [{'issue': 'Three absolute local_file paths are not portable', 'classification': 'NON_BLOCKING_KNOWN_LIMITATION'}],
                  blocking_issues=[], PROJECT_BASELINE_UPDATED='YES', PROJECT_CURRENT_STATE_UPDATED='YES',
                  READY_FOR_PHASE_3_PLANNING='YES', previous_failure_class='PRECONDITION_INPUT_ERROR',
                  previous_failure_reason='INCORRECT_EXPECTED_GTFS_SHA_IN_INSTRUCTION',
                  previous_database_mutation='NO', previous_baseline_mutation='NO', previous_current_state_mutation='NO',
                  previous_git_actions='No staging/commit evidenced by historical report, unchanged status and unborn repository; no independent network telemetry for push.',
                  files_modified=['project_baseline.json', 'PROJECT_CURRENT_STATE.md'],
                  git_add_performed=False, commit_performed=False, push_performed=False)
    result.update({k: False for k in NEGATIVE})
    formal = deepcopy(promoted)
    formal.update(PHASE_2='FROZEN', final_tests=tests, legal_hashes='PASS (10/10)',
                  known_limitations=result['known_limitations'], scope_exclusions=['Legal interpretation', 'Textual fidelity certification', 'Legal compliance assessment', 'Format mapping', 'Audit rules', 'Phase 3 execution'],
                  project_baseline_sha256=sha(baseline_path), current_state_sha256=sha(state_path),
                  db_sha_before=before, db_sha_after=after, db_changed=False,
                  validation_evidence=OUT.relative_to(ROOT).as_posix(),
                  approved_candidate_sha256=sha(FREEZE / 'PHASE_2_FREEZE_CANDIDATE.json'))
    js(FREEZE / 'PHASE_2_FORMAL_FREEZE.json', formal)
    report = '# Phase 2 — Formal freeze\n\nPHASE_2 = FROZEN\nScope: EU-REG-2017-1926 requirements engine.\n\n'
    report += f'Compliance SHA before/after: `{CURRENT}`. DB changed: NO.\nGTFS preserved: `{GTFS}`.\nPhase 1 preserved: `{PHASE1}`.\n\n'
    report += '92 provisions; 36 source facts; 48 approved/materialized requirements; 10 deadline records; 7 PARTIAL external dependencies; 5 functional time requirements.\nGate 1 CLOSED; Gate 2 CLOSED; materialization PASS; final freeze review PASS; final tests PASS.\n\n'
    report += '\n'.join(f"- {t['suite']}: PASS ({t['checks']}/{t['checks']}), exit_code=0" for t in tests)
    report += '\n- Legal source hashes: PASS (10/10).\n\nKnown limitations:\n' + '\n'.join('- ' + r['issue'] for r in result['known_limitations'])
    report += '\n\nScope exclusions: no legal interpretation, textual fidelity certification, legal compliance assessment, format mapping, audit rules or Phase 3 execution.\n' + '\n'.join(k + ' = false' for k in NEGATIVE)
    report += f'\n\nproject_baseline.json SHA-256: `{sha(baseline_path)}`.\nPROJECT_CURRENT_STATE.md SHA-256: `{sha(state_path)}`.\nValidation evidence: `{OUT.relative_to(ROOT).as_posix()}`.\n\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'
    write(FREEZE / 'PHASE_2_FORMAL_FREEZE.md', report)
    promotion_report = '# Phase 2 baseline promotion — resumed\n\n' + '\n'.join(f'{k} = {v}' for k, v in result.items() if k not in ['tests', 'known_limitations'])
    promotion_report += '\n\n' + '\n'.join('- ' + r['issue'] for r in result['known_limitations'])
    promotion_report += '\n\nOriginal failure .md/.csv/.json remain unchanged in freeze/. This successful report is stored separately to preserve history.\n\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'
    write(OUT / 'PHASE_2_BASELINE_PROMOTION.md', promotion_report)
    csvout(OUT / 'PHASE_2_BASELINE_PROMOTION.csv', CHECKS)
    write(FREEZE / 'PHASE_2_BASELINE_PROMOTION_RESUME.md', '# Baseline promotion resume\n\nPrevious attempt = FAIL.\nFailure class = PRECONDITION_INPUT_ERROR.\nCause = INCORRECT_EXPECTED_GTFS_SHA_IN_INSTRUCTION (62 hex characters).\nPrevious database/baseline/current-state mutation = NO; hashes verified against original failure evidence.\nNo previous formal freeze or Phase 3 start. Historical Git evidence shows no staging/commit; no independent network telemetry exists for historical push.\nThis is not GTFS_BASELINE_CORRUPTION, COMPLIANCE_DATABASE_FAILURE or PHASE_2_FREEZE_REVIEW_FAILURE.\n\n' + f'Corrected GTFS SHA = `{GTFS}` (64 characters); existing baseline, historical evidence and live DB agree.\n\nPromotion result = PASS; PHASE_2 = FROZEN.\nSuccessful promotion reports: `promotion_resume/run_001/PHASE_2_BASELINE_PROMOTION.md` and `.csv`.\nOriginal failure reports remain unchanged.\nPROJECT_BASELINE_UPDATED = YES.\nPROJECT_CURRENT_STATE_UPDATED = YES.\nREADY_FOR_PHASE_3_PLANNING = YES; phase_3_started = false.\n\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n')
    status_after = git_status()
    write(OUT / 'GIT_STATUS_AFTER.txt', status_after)
    check('GIT_STATUS_EQUAL', status_after == status_before, status_after, status_before)
    result.update(git_status_before=status_before, git_status_after=status_after, git_status_equal=status_before == status_after)
    hash_paths = [baseline_path, state_path, FREEZE / 'PHASE_2_FORMAL_FREEZE.md', FREEZE / 'PHASE_2_FORMAL_FREEZE.json', OUT / 'PHASE_2_BASELINE_PROMOTION.md', FREEZE / 'PHASE_2_BASELINE_PROMOTION_RESUME.md']
    csvout(FREEZE / 'PHASE_2_FREEZE_HASHES.csv', [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p)) for p in hash_paths])
    result['files_created'] = CREATED + [OUT.relative_to(ROOT).as_posix() + '/FINAL_RESULT.json', OUT.relative_to(ROOT).as_posix() + '/ARTIFACT_MANIFEST.csv', Path(__file__).relative_to(ROOT).as_posix()]
    js(OUT / 'FINAL_RESULT.json', result)
    csvout(OUT / 'ARTIFACT_MANIFEST.csv', [dict(path=p, sha256=sha(ROOT / p)) for p in result['files_created'] if not p.endswith('/ARTIFACT_MANIFEST.csv')])
    check('FINAL_PROTECTION', sha(DB) == before and sha(GTFS_DB) == GTFS and all(sha(ROOT / p) == value for p, value in protected.items()))
    print(json.dumps({k: v for k, v in result.items() if k not in ['files_created', 'known_limitations', 'git_status_before', 'git_status_after']}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        failure_path = OUT / 'RESUME_FAILURE.json'
        if not failure_path.exists():
            js(failure_path, {'PHASE_2_BASELINE_PROMOTION': 'FAIL', 'blocking_issue': str(exc), 'checks': CHECKS, 'db_sha_after': sha(DB), 'files_created': CREATED})
        raise
