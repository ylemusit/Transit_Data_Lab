"""Read-only reconciliation; never imports or reruns the persistence script.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
MAT = Path(__file__).resolve().parent
OUT = MAT / 'test_baseline_reconciliation_evidence'
DB = ROOT / '03_Compliance/databases/transit_compliance.duckdb'
EXPECTED = '0c119b4a75e6a0e7954480675cc625659fe65a1878f46dae1e496e0790d8ffec'
ID = 'EU-2017-1926-SF-A09-P03'
CLI = shutil.which('duckdb')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(rows):
    return sorted(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':')) for r in rows)


def arrays(raw):
    decoder = json.JSONDecoder()
    result = []
    raw = raw.strip()
    while raw:
        value, end = decoder.raw_decode(raw)
        result.append(value)
        raw = raw[end:].strip()
    return result


def run(sql):
    return subprocess.run([CLI, '-no-init', '-readonly', '-batch', '-bail', '-json', str(DB)],
                          input=sql.encode('utf-8'), cwd=ROOT, capture_output=True)


def query(sql):
    proc = run(sql)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode('utf-8'))
    results = arrays(proc.stdout.decode('utf-8'))
    return results[0] if results else []


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def write_csv(path, data, columns):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)


def check(ok, message):
    if not ok:
        raise RuntimeError('TEST_BASELINE_RECONCILIATION=FAIL: ' + message)


def lit(value):
    return "'" + str(value).replace("'", "''") + "'"


def main():
    check(sha(DB) == EXPECTED, 'entry SHA mismatch; STOP')
    check(not DB.with_suffix('.duckdb.wal').exists(), 'unexpected WAL')
    before = json.loads((MAT / 'DATABASE_BEFORE.json').read_text(encoding='utf-8'))
    after = json.loads((MAT / 'DATABASE_AFTER.json').read_text(encoding='utf-8'))
    catalog = query("SELECT table_schema || '.' || table_name AS table_id FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1")
    check({r['table_id'] for r in catalog} == set(after), 'persistent table catalog changed')
    live = {name: query('SELECT * FROM ' + name) for name in after}
    check(all(canonical(live[t]) == canonical(after[t]) for t in after), 'live differs from post-write snapshot')
    target = [r for r in live['compliance.source_facts'] if r['source_fact_id'] == ID]
    check(len(target) == 1 and len(live['compliance.source_facts']) == 36, 'source fact entry state')
    check(len(live['compliance.requirements']) == 3 and len(live['compliance.deadlines']) == 1, 'requirements/deadlines entry state')
    for table in before:
        retained = [r for r in after[table] if r['source_fact_id'] != ID] if table == 'compliance.source_facts' else after[table]
        check(canonical(retained) == canonical(before[table]), 'prior authorized delta mismatch: ' + table)
    check(len(after['compliance.source_facts']) == len(before['compliance.source_facts']) + 1, 'prior delta is not +1')
    check((MAT / 'TRANSACTION_EXIT_CODE.txt').read_text().strip() == '0', 'prior transaction exit code')
    transaction = json.loads((MAT / 'TRANSACTION_VALIDATION.json').read_text())
    check(transaction and all(v == 'PASS' for a in transaction for r in a for v in r.values()), 'prior transaction assertions')
    universe_path = MAT / 'GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv'
    queue_path = MAT / 'GATE_2_POST_SOURCE_FACT_EXCEPTION_QUEUE.csv'
    universe = rows(universe_path)
    check(len(universe) == 48 and len({r['final_review_id'] for r in universe}) == 48, 'atomic universe entry state')
    check(not rows(queue_path), 'exception queue entry state')
    check(all(r['materialization_eligible'] == 'TRUE' and not r['materialization_blocker'] and r['human_status'] not in ('HOLD','REJECT') for r in universe), 'mechanical/human entry blockers')
    resolution = MAT.parent / 'resolution/GATE_2_EXCEPTION_RESOLUTION.md'
    check('cuestiones interpretativas pendientes: 0' in resolution.read_text(encoding='utf-8'), 'interpretive issues entry state')
    check(sha(DB) == EXPECTED, 'SHA changed during entry verification')
    frozen = ROOT / '03_Compliance/sql/07_tests/phase_1/test_phase_1_master.sql'
    phase2 = ROOT / '03_Compliance/sql/07_tests/phase_2/test_phase_2_master.sql'
    invariant = frozen.with_name('test_phase_1_invariants.sql')
    gate = phase2.with_name('test_phase_2_pre_materialization_gate.sql')
    policy = ROOT / '03_Compliance/TEST_BASELINE_POLICY.md'
    report = MAT / 'TEST_BASELINE_RECONCILIATION.md'
    closure = MAT / 'HUMAN_REVIEW_GATE_2_CLOSURE.md'
    for path in [OUT, invariant, gate, policy, report, closure, MAT / 'TEST_BASELINE_RECONCILIATION.csv']:
        check(not path.exists(), 'refuse to overwrite ' + str(path))
    protected = [p for p in (ROOT / '03_Compliance').rglob('*') if p.is_file() and p != Path(__file__).resolve()]
    protected.append(ROOT / 'project_baseline.json')
    original_hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    git_before = subprocess.check_output(['git','status','--short'], cwd=ROOT).decode('utf-8')
    OUT.mkdir()
    (OUT / 'GIT_STATUS_BEFORE.txt').write_text(git_before, encoding='utf-8')
    (OUT / 'PROTECTED_FILE_HASHES_BEFORE.json').write_text(json.dumps(original_hashes, indent=2), encoding='utf-8')
    header = '-- Read-only cumulative-database regression. Run from repository root.\n-- Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'
    original = frozen.read_text(encoding='utf-8')
    start = original.index('    UNION ALL', original.index("'21_DUPLICATE_PROVISION_IDS'"))
    end = original.index('),', start)
    inv = original[:start] + original[end:]
    for table in ['compliance.requirements','mapping.format_coverage','audit.rules']:
        inv = re.sub(r'\s+AND \(SELECT COUNT\(\*\) FROM ' + re.escape(table) + r'\) = 0', '', inv)
    inv = inv.replace('PHASE_1_CORPUS_INTEGRITY', 'PHASE_1_INVARIANT_REGRESSION')
    check('NOT_DERIVED_YET' not in inv and 'NOT_CREATED_YET' not in inv, 'invariant extraction failed')
    invariant.write_text(header + inv, encoding='utf-8')
    up = universe_path.relative_to(ROOT).as_posix()
    qp = queue_path.relative_to(ROOT).as_posix()
    dp = (MAT.parent / 'GATE_2_EXTERNAL_DEPENDENCIES.csv').relative_to(ROOT).as_posix()
    additions = []
    def add(name, expected, expression):
        additions.append(f"    UNION ALL SELECT '{name}', {expected}, ({expression})")
    add('29_SOURCE_FACTS_CURRENT',36,'SELECT count(*) FROM compliance.source_facts')
    add('30_ARTICLE_9_3_EXACTLY_ONCE',1,f'SELECT count(*) FROM compliance.source_facts WHERE source_fact_id={lit(ID)}')
    add('31_REQUIREMENTS_CURRENT',3,'SELECT count(*) FROM compliance.requirements')
    add('32_DEADLINES_CURRENT',1,'SELECT count(*) FROM compliance.deadlines')
    add('33_FINAL_ATOMIC_UNIVERSE',48,f"SELECT count(DISTINCT final_review_id) FROM read_csv('{up}',header=true,all_varchar=true)")
    add('34_EXCEPTION_QUEUE',0,f"SELECT count(*) FROM read_csv('{qp}',header=true,all_varchar=true)")
    add('35_MECHANICAL_BLOCKERS',0,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) WHERE materialization_eligible IS DISTINCT FROM 'TRUE' OR coalesce(materialization_blocker,'')<>''")
    add('36_UNRESOLVED_HUMAN_DECISIONS',0,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) WHERE human_status IS NULL OR human_status IN ('HOLD','REJECT')")
    add('37_EXTERNAL_DEPENDENCIES',7,f"SELECT count(*) FROM read_csv('{dp}',header=true,all_varchar=true) WHERE external_dependency='TRUE' AND dependency_blocking_level='PARTIAL'")
    add('38_UNIVERSE_EXTERNAL_DEPENDENCIES',7,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) WHERE external_dependency='TRUE' AND dependency_blocking_level='PARTIAL'")
    add('39_SOURCE_ANOMALY_DEPENDENCIES',0,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) WHERE source_anomaly_dependency IS DISTINCT FROM 'FALSE'")
    add('40_UNIVERSE_FACT_TRACEABILITY',0,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) u LEFT JOIN compliance.source_facts f ON u.source_fact_id=f.source_fact_id WHERE f.source_fact_id IS NULL OR u.source_document_id IS DISTINCT FROM f.source_document_id OR u.source_provision_id IS DISTINCT FROM f.source_provision_id OR u.source_fact_text IS DISTINCT FROM f.source_fact_text")
    add('41_ANNEX_ANOMALY_RECORDS_RETAINED',2,"SELECT count(*) FROM source.provisions WHERE provision_id IN ('EU-2017-1926-ANNEX-1.3-B-I','EU-2017-1926-ANNEX-1.3-D-I')")
    # Actual file content checks, rather than trusting a precomputed PASS flag.
    legal_checks = []
    for d in live['source.documents']:
        path = Path(d['local_file'])
        if not path.is_absolute():
            path = ROOT / path if (ROOT / path).exists() else ROOT / '03_Compliance' / path
        check(path.is_file() and sha(path) == d['source_hash'], 'legal source hash ' + d['document_id'])
        legal_checks.append({'document_id': d['document_id'], 'sha256': sha(path), 'status':'PASS'})
        sql_path = path.as_posix() if Path(d['local_file']).is_absolute() else path.relative_to(ROOT).as_posix()
        add('LEGAL_HASH_' + d['document_id'],1,f"SELECT count(*) FROM read_blob({lit(sql_path)}) WHERE sha256(content)={lit(d['source_hash'])}")
    add('42_INTERPRETIVE_ISSUES',0,"SELECT CASE WHEN contains(content, 'cuestiones interpretativas pendientes: 0') THEN 0 ELSE 1 END FROM read_text('03_Compliance/reports/phase_2/review/gate_2/resolution/GATE_2_EXCEPTION_RESOLUTION.md')")
    # Domain guards inspect proposed semantics; they do not purport to assess legal compliance.
    add('43_NO_GTFS_OBLIGATION_INFERENCE',0,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) WHERE contains(upper(normalized_description),'GTFS')")
    for fmt in ['NeTEx','SIRI']:
        add('44_NO_UNIVERSAL_' + fmt.upper(),0,f"SELECT count(*) FROM read_csv('{up}',header=true,all_varchar=true) WHERE contains(upper(normalized_description),'{fmt.upper()}') AND (is_conditional IS DISTINCT FROM 'TRUE' OR coalesce(condition_text,'')='' OR NOT (contains(lower(normalized_description),' o ') OR contains(lower(normalized_description),'compatible')))")
    gate_sql = phase2.read_text(encoding='utf-8').replace('), evaluated AS (', '\n' + '\n'.join(additions) + '\n), evaluated AS (')
    gate.write_text(header + gate_sql, encoding='utf-8')
    policy.write_text('''# Política de baseline de tests

`test_phase_1_master.sql` es PHASE_1_FROZEN_STATE_TEST: valida la instantánea histórica de Phase 1. PHASE_1_FROZEN_REQUIREMENTS_COUNT = 0 permanece cierto para esa instantánea. El master y su evidencia nunca se reescriben para ajustarlos a datos actuales.

Los tests 01–21 y las condiciones estructurales del agregado son invariantes del corpus protegido: documentos, referencias, unicidad, relaciones y estructura 2017/1926. `test_phase_1_invariants.sql` conserva esas comprobaciones y manifiestos. Los tests 22–24 y las tres condiciones de tablas vacías del agregado son PHASE_STATE_TESTS: requirements, format_coverage y audit.rules pueden evolucionar. Se excluyen los tres de la suite de invariantes, aunque los dos últimos aún pasen en Phase 2.

Los masters estructural y de anexos son invariantes del corpus protegido. En el master Phase 2, 01–13 y 24–28 son contratos de integridad/trazabilidad; 17–20 protegen el corpus Phase 1; 14–16, 21–23 son condiciones del alcance y estado de Phase 2. No se presupone que estas últimas sean invariantes de fases posteriores.

Los tests de gate actual validan la fase activa. `test_phase_2_pre_materialization_gate.sql` exige 36 facts, 3 requirements, 1 deadline, universo propuesto de 48, cola y bloqueos vacíos, traza de fuentes, hashes y siete dependencias PARTIAL. Se ejecuta desde la raíz con DuckDB `-readonly`. La condición interpretativa verifica la decisión humana documentada, no produce una nueva interpretación jurídica. Las guardas de formatos inspeccionan propuestas y sus condiciones/alternativas; no certifican cumplimiento jurídico.

Una base acumulativa posterior no debe satisfacer condiciones históricas mutables ya superadas. Ejecutar el master Phase 1 contra Phase 2 produce EXPECTED_HISTORICAL_STATE_MISMATCH, incluido el FAIL agregado causado por requirements=0; no CURRENT_DATABASE_INTEGRITY_FAILURE. Un fallo adicional de invariantes sí bloquea el cierre.

Cada cambio de base exige verificación de delta específica de fase. Esta conciliación es exclusivamente read-only y compara todas las tablas con DATABASE_AFTER.json; revalida el delta anterior de +1 source_fact contra DATABASE_BEFORE.json. La transacción anterior es SOURCE_FACT_TRANSACTION=PASS; el FAIL global original se clasifica POST_WRITE_TEST_GATE_FAIL por HISTORICAL_PHASE_STATE_ASSERTION_APPLIED_TO_LATER_PHASE_DB. Los informes originales se conservan.

project_baseline.json solo se promueve en una congelación formal; no con cada escritura controlada. Cerrar Gate 2 permite iniciar una futura materialización autorizada: no congela ni cierra Phase 2, no evalúa cumplimiento, no completa mappings/reglas y no habilita Phase 3.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
''', encoding='utf-8')
    write_csv(OUT / 'LEGAL_SOURCE_HASH_CHECKS.csv', legal_checks, ['document_id','sha256','status'])
    suites = [frozen, invariant, phase2, gate, MAT / 'test_article_9_3_source_fact.sql'] + sorted((ROOT / '03_Compliance/sql/07_tests/source').glob('*.sql'))
    results = []
    for path in suites:
        proc = run(path.read_text(encoding='utf-8'))
        (OUT / (path.stem + '.json')).write_bytes(proc.stdout)
        (OUT / (path.stem + '.stderr.txt')).write_bytes(proc.stderr)
        (OUT / (path.stem + '.exit_code.txt')).write_text(str(proc.returncode) + '\n')
        check(proc.returncode == 0, 'suite execution: ' + path.stem)
        parsed = [r for a in arrays(proc.stdout.decode('utf-8')) for r in a if 'test' in r and 'status' in r]
        check(bool(parsed), 'empty suite: ' + path.stem)
        results.extend({'suite':path.stem, **r} for r in parsed)
        failed = {r['test'] for r in parsed if r['status'] != 'PASS'}
        if path == frozen:
            check(failed == {'22_REQUIREMENTS_NOT_DERIVED_YET','PHASE_1_CORPUS_INTEGRITY'}, 'unexpected historical mismatch')
        else:
            check(not failed, 'suite failures: ' + str(failed))
    write_csv(OUT / 'TEST_RESULTS.csv', results, ['suite','test','status','expected','actual'])
    check(target[0]['source_fact_text'].encode('utf-8').decode('utf-8') == target[0]['source_fact_text'] and not any(s in target[0]['source_fact_text'] for s in ('Ã','Â','�')), 'target UTF-8')
    check(all(sha(ROOT / p) == h for p,h in original_hashes.items()), 'original evidence/baseline changed')
    final_sha = sha(DB)
    check(final_sha == EXPECTED, 'final database SHA changed; STOP')
    metrics = {'TEST_BASELINE_RECONCILIATION':'PASS','DB_SHA_BEFORE':EXPECTED,'DB_SHA_AFTER':final_sha,'DB_UNCHANGED':'YES','ARTICLE_9_3_SOURCE_FACT_COUNT':1,'SOURCE_FACT_TRANSACTION':'PASS','PHASE_1_HISTORICAL_MASTER':'FAIL (23/24; aggregate FAIL)','HISTORICAL_MISMATCH_CLASSIFICATION':'EXPECTED_HISTORICAL_STATE_MISMATCH','PRIOR_AGGREGATE_FAIL':'POST_WRITE_TEST_GATE_FAIL','REASON':'HISTORICAL_PHASE_STATE_ASSERTION_APPLIED_TO_LATER_PHASE_DB','PHASE_1_FROZEN_REQUIREMENTS_COUNT':0,'PHASE_1_INVARIANT_REGRESSION':'PASS','STRUCTURAL_2017_1926':'PASS','ANNEX_TESTS':'PASS','LEGAL_HASHES':'PASS','PHASE_2_TESTS':'PASS','PHASE_2_PRE_MATERIALIZATION_GATE':'PASS','REQUIREMENTS_COUNT':3,'DEADLINES_COUNT':1,'FINAL_ATOMIC_UNIVERSE':48,'EXCEPTION_QUEUE':0,'INTERPRETIVE_ISSUES':0,'MECHANICAL_BLOCKERS':0,'SOURCE_FACT_TRACEABILITY':'PASS','UTF8':'PASS','DATABASE_INTEGRITY':'PASS','PRIOR_AUTHORIZED_SEMANTIC_DELTA':'+1 source_fact only; requirements delta=0; deadlines delta=0','THIS_RECONCILIATION_DB_DELTA':0,'HUMAN_REVIEW_GATE_2':'CLOSED','READY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION':'YES'}
    write_csv(MAT / 'TEST_BASELINE_RECONCILIATION.csv', [{'metric':k,'value':v} for k,v in metrics.items()], ['metric','value'])
    body = '\n'.join(f'- {k} = `{v}`' for k,v in metrics.items())
    report.write_text('# Conciliación del baseline de tests\n\n' + body + '\n\nEl FAIL histórico y todos los archivos previos conservan su SHA-256. El agregado PHASE_1_CORPUS_INTEGRITY también falla por la misma condición histórica. La nueva suite conserva 21 checks y el agregado estructural, sin las condiciones de estado 22–24.\n\nEvidencia durable: test_baseline_reconciliation_evidence/TEST_RESULTS.csv, stdout JSON completo, stderr y exit_code por suite; hashes de archivos previos y de fuentes jurídicas. DATABASE_BEFORE/AFTER originales verifican el delta previo; todas las tablas actuales coinciden con AFTER.\n\nPhase 2 sigue abierta y sin congelar; no se evalúa cumplimiento ni se inicia Phase 3.\n\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n', encoding='utf-8')
    closure.write_text('''# Human Review Gate 2: cierre

HUMAN_REVIEW_GATE_2 = CLOSED
GATE_2_FINAL_ATOMIC_UNIVERSE = 48
GATE_2_INTERPRETIVE_ISSUES = 0
GATE_2_MECHANICAL_BLOCKERS = 0
ARTICLE_9_3_SOURCE_FACT = PERSISTED
SOURCE_FACT_TRANSACTION = PASS
PHASE_1_HISTORICAL_MASTER = EXPECTED_STATE_MISMATCH_ON_PHASE_2_LIVE_DB
PHASE_1_INVARIANT_REGRESSION = PASS
PHASE_2_PRE_MATERIALIZATION_GATE = PASS
READY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION = YES

Todas las condiciones de cierre se acreditan en TEST_BASELINE_RECONCILIATION.md/csv y test_baseline_reconciliation_evidence. La decisión humana de G2-045 READY_PENDING_SOURCE_FACT_PERSISTENCE conserva su historia; el prerrequisito se cumplió con la persistencia acreditada. No se alteran los CSV históricos.

Este documento es el cierre actual de Gate 2 y sucede temporalmente a HUMAN_REVIEW_GATE_2_STATUS.md, que conserva el resultado anterior OPEN/FAIL. Solo cierra la revisión humana y sus prerrequisitos de trazabilidad para las 48 propuestas. No materializa requisitos, no cierra/congela Phase 2, no evalúa cumplimiento jurídico, no completa mappings ni reglas y no habilita Phase 3. Las siete dependencias externas siguen PARTIAL.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
''', encoding='utf-8')
    git_after = subprocess.check_output(['git','status','--short'], cwd=ROOT).decode('utf-8')
    (OUT / 'GIT_STATUS_AFTER.txt').write_text(git_after, encoding='utf-8')
    check(all(sha(ROOT / p) == h for p,h in original_hashes.items()) and sha(DB) == EXPECTED, 'final preservation verification')
    created = [invariant,gate,policy,report,closure,MAT/'TEST_BASELINE_RECONCILIATION.csv',Path(__file__).resolve()] + sorted(OUT.glob('*'))
    write_csv(OUT / 'FILES_CREATED.csv', [{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in created], ['path','sha256'])
    (OUT / 'EXECUTION_EXIT_CODE.txt').write_text('0\n')
    (OUT / 'FINAL_VERIFICATION.json').write_text(json.dumps({'metrics':metrics,'protected_files_preserved':len(original_hashes),'git_before':git_before,'git_after':git_after,'suites':len(suites),'tests':len(results)}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
