"""One-shot authorized source fact insertion; no other persistent SQL writes.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
RES = OUT.parent / 'resolution'
DB = ROOT / '03_Compliance/databases/transit_compliance.duckdb'
EXPECTED = 'ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668'
ID = 'EU-2017-1926-SF-A09-P03'
PROVISION = 'EU-2017-1926-ART09'
DOCUMENT = 'EU-REG-2017-1926'
COLS = ['source_fact_id', 'source_document_id', 'source_provision_id',
        'legal_reference', 'source_fact_text', 'source_version_date', 'source_uri', 'notes']
CLI = shutil.which('duckdb')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(rows):
    return sorted(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':')) for r in rows)


def content_hash(rows):
    return hashlib.sha256('\n'.join(canonical(rows)).encode('utf-8')).hexdigest()


def arrays(text):
    decoder = json.JSONDecoder()
    result = []
    text = text.strip()
    while text:
        item, end = decoder.raw_decode(text)
        result.append(item)
        text = text[end:].strip()
    return result


def run(sql, readonly=True):
    args = [CLI, '-no-init', '-batch', '-bail', '-json']
    if readonly:
        args.append('-readonly')
    proc = subprocess.run(args + [str(DB)], input=sql.encode('utf-8'),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT)
    stdout = proc.stdout.decode('utf-8')
    stderr = proc.stderr.decode('utf-8')
    if proc.returncode:
        raise RuntimeError(f'DuckDB exit={proc.returncode}: {stderr}\n{stdout}')
    return arrays(stdout)


def query(sql):
    result = run(sql)
    return result[0] if result else []


def literal(value):
    if value is None:
        return 'NULL'
    return "'" + str(value).replace("'", "''") + "'"


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def export(name, rows, columns=None):
    with (OUT / name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sql_fingerprint(table, exclusion=''):
    return f"SELECT count(*) n, sha256(coalesce(string_agg(to_json(t), chr(10) ORDER BY to_json(t)),'')) h FROM {table} t {exclusion}"


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def git():
    return subprocess.check_output(['git', 'status', '--short'], cwd=ROOT).decode('utf-8')


def main():
    # Hash mismatch is checked before report snapshots or opening DuckDB.
    check(sha(DB) == EXPECTED, 'PRE_WRITE_SHA mismatch: STOP without database/report writes')
    check(not DB.with_suffix('.duckdb.wal').exists(), 'Unexpected WAL: STOP')
    proposal = read_csv(RES / 'ARTICLE_9_3_SOURCE_FACT_PROPOSAL.csv')
    check(len(proposal) == 1, 'Expected exactly one proposal')
    p = proposal[0]
    check(p['proposed_source_fact_id'] == ID and p['persistence_status'] == 'PROPOSED_NOT_PERSISTED', 'Proposal identity/status mismatch')
    check(p['source_provision_id'] == PROVISION and p['source_document_id'] == DOCUMENT, 'Proposal traceability mismatch')
    check(p['legal_reference'] == 'Artículo 9, apartado 3', 'Approved Article 9(3) reference mismatch')
    normalized = 'Los Estados miembros efectuarán comprobaciones aleatorias de la exactitud de las declaraciones mencionadas en el artículo 9, apartado 2, letra c).'
    check(p['normalized_fact'] == normalized, 'Normalized proposition changed')
    schema = query('DESCRIBE compliance.source_facts;')
    check([r['column_name'] for r in schema] == COLS, 'Source fact schema mismatch: STOP')
    check([r['column_type'] for r in schema] == ['VARCHAR'] * 5 + ['DATE', 'VARCHAR', 'VARCHAR'], 'Source fact types mismatch')
    check(not query(f'SELECT * FROM compliance.source_facts WHERE source_fact_id={literal(ID)}'), 'Target already exists: STOP')
    provision = query(f'SELECT * FROM source.provisions WHERE provision_id={literal(PROVISION)}')
    check(len(provision) == 1 and provision[0]['document_id'] == DOCUMENT and provision[0]['article'] == '9', 'Provision traceability failed')
    document = query(f'SELECT * FROM source.documents WHERE document_id={literal(DOCUMENT)}')
    check(len(document) == 1, 'Document traceability failed')
    check(p['source_version_date'] == '2024-03-04' and p['source_version_date'] in document[0]['official_url'] and p['source_version_date'] in document[0]['local_file'], 'Document/version traceability failed')
    from pypdf import PdfReader
    corpus = ROOT / p['corpus_local_file']
    check(sha(corpus) == p['corpus_sha256'] == document[0]['source_hash'], 'Consolidated corpus hash mismatch')
    corpus_text = PdfReader(corpus).pages[int(p['corpus_page']) - 1].extract_text()
    compact = lambda s: ''.join(s.split())
    check('3.' + compact(p['source_fact_text']) in compact(corpus_text), 'Literal Article 9(3) not found on approved corpus page')
    universe = read_csv(RES / 'GATE_2_FINAL_ATOMIC_UNIVERSE.csv')
    queue = read_csv(RES / 'GATE_2_FINAL_EXCEPTION_QUEUE.csv')
    resolution = (RES / 'GATE_2_EXCEPTION_RESOLUTION.md').read_text(encoding='utf-8')
    check('cuestiones interpretativas pendientes: 0' in resolution, 'Interpretive issues not zero')
    check(len(universe) == 48 and len({r['final_review_id'] for r in universe}) == 48, 'Universe is not 48 unique rows')
    check(len(queue) == 1 and queue[0]['final_review_id'] == 'G2-045' and queue[0]['issue'] == 'SOURCE_FACT_NOT_PERSISTED', 'Unexpected exception queue')
    dependencies = read_csv(OUT.parent / 'GATE_2_EXTERNAL_DEPENDENCIES.csv')
    check(sum(r['external_dependency'] == 'TRUE' for r in universe) == 7, 'External dependency count changed')
    check('PARTIAL' in json.dumps(dependencies) and len(dependencies) == 7, 'Seven PARTIAL dependencies not preserved')
    catalog = query("SELECT table_schema,table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1,2")
    tables = [r['table_schema'] + '.' + r['table_name'] for r in catalog]
    before = {t: query(f'SELECT * FROM {t}') for t in tables}
    check(len(before['compliance.requirements']) == 3 and len(before['compliance.deadlines']) == 1, 'Requirements/deadlines counts mismatch')
    check(not any(r['source_provision_id'] == PROVISION for r in before['compliance.requirements']), 'Article 9 requirement already materialized')
    sf = {r['source_fact_id']: r for r in before['compliance.source_facts']}
    for r in universe:
        if r['final_review_id'] == 'G2-045':
            check(r['proposed_source_fact_id'] == ID and r['materialization_blocker'] == 'SOURCE_FACT_NOT_PERSISTED' and r['source_fact_text'] == p['source_fact_text'], 'G2-045 mismatch')
        else:
            check(r['materialization_eligible'] == 'TRUE' and not r['materialization_blocker'], f"Existing prerequisite failure: {r['final_review_id']}")
            fact = sf.get(r['source_fact_id'])
            check(fact and fact['source_document_id'] == r['source_document_id'] and fact['source_provision_id'] == r['source_provision_id'], f"Universe traceability failure: {r['final_review_id']}")
        check(r['human_status'] not in ('HOLD', 'REJECT') and r['source_anomaly_dependency'] == 'FALSE', 'Unresolved human decision/Annex anomaly')
    source_hash_checks = []
    for d in before['source.documents']:
        path = Path(d['local_file'])
        if not path.is_absolute():
            path = ROOT / path if (ROOT / path).exists() else ROOT / '03_Compliance' / path
        check(path.exists() and sha(path) == d['source_hash'], f"Legal source hash failed: {d['document_id']}")
        source_hash_checks.append({'document_id': d['document_id'], 'sha256': sha(path), 'status': 'PASS'})
    article_before = [r for r in before['compliance.source_facts'] if r['source_provision_id'] == PROVISION]
    fingerprints = {t: query(sql_fingerprint(t))[0] for t in tables}
    values = {c: p['proposed_source_fact_id'] if c == 'source_fact_id' else p[c] for c in COLS}
    input_paths = [ROOT / 'project_baseline.json'] + [f for f in OUT.parent.rglob('*') if f.is_file() and OUT not in f.parents]
    input_hashes = {str(f.relative_to(ROOT)): sha(f) for f in input_paths}
    git_before = git()
    check(sha(DB) == EXPECTED, 'Database changed during preflight')
    if '--write' not in sys.argv:
        print(json.dumps({'preflight': 'PASS', 'tables': len(tables), 'source_facts': len(sf), 'article_9': len(article_before), 'universe': len(universe), 'source_hashes': len(source_hash_checks)}, indent=2))
        return
    check(not (OUT / 'ARTICLE_9_3_SOURCE_FACT_PRE_WRITE.csv').exists(), 'Prior persistence evidence exists: STOP; do not overwrite')
    export('ARTICLE_9_3_SOURCE_FACT_PRE_WRITE.csv', [{
        'database_sha': EXPECTED, 'source_fact_count_total': len(sf),
        'article_9_source_fact_count': len(article_before), 'target_source_fact_count': 0,
        'requirements_count': 3, 'deadlines_count': 1, 'timestamp': datetime.now(timezone.utc).isoformat()}])
    export('ARTICLE_9_SOURCE_FACTS_BEFORE.csv', article_before, COLS)
    (OUT / 'DATABASE_BEFORE.json').write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'INPUT_HASHES_BEFORE.json').write_text(json.dumps(input_hashes, indent=2), encoding='utf-8')
    (OUT / 'GIT_STATUS_BEFORE.txt').write_text(git_before, encoding='utf-8')
    checks = []
    def assertion(condition, name):
        return f"SELECT CASE WHEN ({condition}) THEN 'PASS' ELSE error({literal(name)}) END AS {name};"
    # The CLI is fail-fast. Any error closes the connection with an uncommitted
    # explicit transaction, causing DuckDB to roll back; COMMIT is not reached.
    sql = 'BEGIN TRANSACTION;\n'
    for t, f in fingerprints.items():
        sql += assertion(f"(SELECT n={f['n']} AND h={literal(f['h'])} FROM ({sql_fingerprint(t)}))", 'pre_' + t.replace('.', '_')) + '\n'
    sql += 'INSERT INTO compliance.source_facts (' + ','.join(COLS) + ') VALUES (' + ','.join(literal(values[c]) for c in COLS) + ');\n'
    match = ' AND '.join(f'{c} IS NOT DISTINCT FROM {literal(values[c])}' for c in COLS)
    sql += assertion(f"(SELECT count(*)=1 FROM compliance.source_facts WHERE {match}) AND (SELECT count(*)=1 FROM compliance.source_facts WHERE source_fact_id={literal(ID)})", 'exact_inserted_row') + '\n'
    for t, f in fingerprints.items():
        exclusion = f'WHERE source_fact_id <> {literal(ID)}' if t == 'compliance.source_facts' else ''
        sql += assertion(f"(SELECT n={f['n']} AND h={literal(f['h'])} FROM ({sql_fingerprint(t, exclusion)}))", 'unchanged_' + t.replace('.', '_')) + '\n'
    sql += 'COMMIT;\n'
    (OUT / 'CONTROLLED_TRANSACTION.sql').write_text(sql, encoding='utf-8')
    check(sha(DB) == EXPECTED, 'Hash changed immediately before write')
    transaction_result = run(sql, readonly=False)
    (OUT / 'TRANSACTION_VALIDATION.json').write_text(json.dumps(transaction_result, indent=2), encoding='utf-8')
    (OUT / 'TRANSACTION_EXIT_CODE.txt').write_text('0\n', encoding='utf-8')
    post_sha = sha(DB)
    after = {t: query(f'SELECT * FROM {t}') for t in tables}
    (OUT / 'DATABASE_AFTER.json').write_text(json.dumps(after, ensure_ascii=False, indent=2), encoding='utf-8')
    target = [r for r in after['compliance.source_facts'] if r['source_fact_id'] == ID]
    check(target == [values], 'Committed target differs from proposal')
    for t in tables:
        preserved = [r for r in after[t] if r['source_fact_id'] != ID] if t == 'compliance.source_facts' else after[t]
        check(canonical(preserved) == canonical(before[t]), f'Unexpected semantic delta: {t}')
    check(len(after['compliance.source_facts']) == len(sf) + 1 and post_sha != EXPECTED, 'Expected DB/source fact delta absent')
    article_after = [r for r in after['compliance.source_facts'] if r['source_provision_id'] == PROVISION]
    export('ARTICLE_9_SOURCE_FACTS_AFTER.csv', article_after, COLS)
    check(read_csv(OUT / 'ARTICLE_9_SOURCE_FACTS_AFTER.csv') == article_after, 'UTF-8 CSV roundtrip failed')
    check(target[0]['source_fact_text'].encode('utf-8').decode('utf-8') == p['source_fact_text'] and not any(s in target[0]['source_fact_text'] for s in ('Ã', 'Â', '�')), 'UTF-8 mojibake')
    export('LEGAL_SOURCE_HASH_CHECKS.csv', source_hash_checks)
    for r in universe:
        if r['final_review_id'] == 'G2-045':
            r['source_fact_id'] = ID
            r['materialization_eligible'] = 'TRUE'
            r['materialization_blocker'] = ''
    export('GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv', universe)
    export('GATE_2_POST_SOURCE_FACT_EXCEPTION_QUEUE.csv', [], list(queue[0]))
    check(all(r['materialization_eligible'] == 'TRUE' for r in universe), '48 prerequisites not satisfied')
    check(all(sha(ROOT / path) == h for path, h in input_hashes.items()), 'Historical evidence/baseline changed')
    test_results = []
    test_paths = [ROOT / '03_Compliance/sql/07_tests/phase_1/test_phase_1_master.sql', ROOT / '03_Compliance/sql/07_tests/phase_2/test_phase_2_master.sql'] + sorted((ROOT / '03_Compliance/sql/07_tests/source').glob('*.sql'))
    for path in test_paths:
        proc = subprocess.run([CLI, '-no-init', '-readonly', '-batch', '-bail', '-json', str(DB)], input=path.read_bytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT)
        log = proc.stdout.decode('utf-8')
        (OUT / (path.stem + '.json')).write_text(log, encoding='utf-8')
        (OUT / (path.stem + '.stderr.txt')).write_bytes(proc.stderr)
        (OUT / (path.stem + '.exit_code.txt')).write_text(str(proc.returncode) + '\n', encoding='utf-8')
        check(proc.returncode == 0, f'Test execution failed: {path.name}')
        for result in arrays(log):
            for r in result:
                if 'status' in r and 'test' in r:
                    test_results.append({'suite': path.stem, **r})
    export('INTEGRITY_TEST_RESULTS.csv', test_results, ['suite', 'test', 'status', 'expected', 'actual'])
    failures = [r for r in test_results if r['status'] != 'PASS']
    phase1 = [r for r in test_results if r['suite'] == 'test_phase_1_master']
    phase2 = [r for r in test_results if r['suite'] == 'test_phase_2_master']
    strict_pass = not failures
    metrics = {
        'SOURCE_FACT_PERSISTENCE': 'PASS' if strict_pass else 'FAIL',
        'source_fact_persisted': 'YES', 'source_fact_id': ID, 'source_provision_id': PROVISION,
        'source_document_id': DOCUMENT, 'transaction_committed': 'YES',
        'PRE_WRITE_SHA': EXPECTED, 'POST_WRITE_SHA': post_sha, 'SHA_changed': 'YES',
        'source_fact_count_before': len(sf), 'source_fact_count_after': len(after['compliance.source_facts']),
        'article_9_source_facts_before': len(article_before), 'article_9_source_facts_after': len(article_after),
        'requirements_before': 3, 'requirements_after': len(after['compliance.requirements']),
        'deadlines_before': 1, 'deadlines_after': len(after['compliance.deadlines']),
        'protected_tables_unchanged': 'YES', 'semantic_DB_delta': '+1 compliance.source_facts row: ' + ID,
        'source_fact_traceability': 'PASS', 'UTF8_roundtrip': 'PASS',
        'Phase_1_tests': 'FAIL' if any(r['status'] != 'PASS' for r in phase1) else 'PASS',
        'Phase_2_tests': 'FAIL' if any(r['status'] != 'PASS' for r in phase2) else 'PASS',
        'final_atomic_universe': 48, 'final_exception_queue': 0, 'interpretive_issues': 0,
        'mechanical_blockers': 0, 'materialization_prerequisites': 'PASS',
        'HUMAN_REVIEW_GATE_2': 'CLOSED' if strict_pass else 'OPEN',
        'READY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION': 'YES' if strict_pass else 'NO',
    }
    for t in ['compliance.requirements', 'compliance.deadlines']:
        metrics[t + '_hash_before'] = content_hash(before[t])
        metrics[t + '_hash_after'] = content_hash(after[t])
    export('ARTICLE_9_3_SOURCE_FACT_PERSISTENCE.csv', [metrics])
    table_delta = [{'table': t, 'count_before': len(before[t]), 'count_after': len(after[t]), 'sha256_before': content_hash(before[t]), 'sha256_after': content_hash(after[t])} for t in tables]
    export('DATABASE_TABLE_DELTA.csv', table_delta)
    note = '\n'.join(f'- {k}: `{v}`' for k, v in metrics.items())
    failure_note = '\n'.join(f"- {r['suite']}: {r['test']} = {r['status']}; expected={r.get('expected')}, actual={r.get('actual')}" for r in failures)
    explanation = '\nEl test histórico Phase 1 mantiene la expectativa requirements=0. Se ejecutó intacto: hay 3 requisitos preexistentes, conservados exactamente. El fallo histórico no es un delta introducido, pero el criterio estricto solicitado impide declarar PASS y cerrar Gate 2. No se alteran tests ni se revierte la inserción autorizada que superó sus verificaciones transaccionales.\n' if failures else ''
    footer = '\nAutor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'
    (OUT / 'ARTICLE_9_3_SOURCE_FACT_PERSISTENCE.md').write_text('# Article 9(3): persistencia controlada\n\n' + note + '\n\n## Tests\n' + failure_note + explanation + '\nLa referencia aprobada es «Artículo 9, apartado 3» (Article 9(3)); la provision general Article 9 tiene paragraph=NULL. La traza del apartado 3 queda acreditada por referencia, texto literal, versión, URI y página 10 del corpus consolidado, no por una provision de párrafo inventada.\n\nSolo se ha reevaluado SOURCE_FACT_NOT_PERSISTED. G2-045.source_fact_id y elegibilidad quedan documentados en el nuevo CSV de universo; los informes históricos y project_baseline.json conservan sus hashes.\n' + footer, encoding='utf-8')
    delta_text = '# Prueba del delta semántico de base\n\nÚnico delta: +1 compliance.source_facts row `' + ID + '`.\n\n| Tabla | Antes | Después | Contenido preexistente |\n|---|---:|---:|---|\n'
    delta_text += '\n'.join(f"| {r['table']} | {r['count_before']} | {r['count_after']} | Sin cambios |" for r in table_delta)
    delta_text += '\n\nDATABASE_BEFORE.json y DATABASE_AFTER.json contienen las filas de todas las tablas persistentes. DATABASE_TABLE_DELTA.csv contiene SHA-256 deterministas sobre JSON por fila (claves ordenadas, Unicode sin escapar, separadores compactos), filas ordenadas lexicográficamente y unidas con LF. Los NULL y tipos JSON se preservan; fechas/timestamps se representan como cadenas DuckDB. Dentro de la transacción se contrastaron conteos y SHA-256 de to_json de cada tabla, excluyendo únicamente el ID nuevo tras INSERT. La comparación posterior completa confirma que no se ha cambiado ninguna fila existente.\n' + footer
    (OUT / 'SOURCE_FACT_DATABASE_DELTA.md').write_text(delta_text, encoding='utf-8')
    if strict_pass:
        (OUT / 'HUMAN_REVIEW_GATE_2_CLOSURE.md').write_text('# Human Review Gate 2\n\nHUMAN_REVIEW_GATE_2 = CLOSED\nGATE_2_FINAL_ATOMIC_UNIVERSE = 48\nGATE_2_INTERPRETIVE_ISSUES = 0\nGATE_2_MECHANICAL_BLOCKERS = 0\nGATE_2_MATERIALIZATION_PREREQUISITES = PASS\nREADY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION = YES\n\nSolo habilita la siguiente etapa controlada. No materializa requisitos.\n' + footer, encoding='utf-8')
    else:
        (OUT / 'HUMAN_REVIEW_GATE_2_STATUS.md').write_text('# Human Review Gate 2: abierto\n\nHUMAN_REVIEW_GATE_2 = OPEN\nREADY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION = NO\n\nPersistencia realizada; 48 prerrequisitos preparatorios satisfechos; 0 bloqueos mecánicos y 0 cuestiones interpretativas. No se genera informe de cierre porque el master histórico Phase 1 devuelve FAIL.\n' + failure_note + explanation + footer, encoding='utf-8')
    git_after = git()
    (OUT / 'GIT_STATUS_AFTER.txt').write_text(git_after, encoding='utf-8')
    check(git_before == git_after, 'Unexpected Git status delta')
    check(sha(DB) == post_sha, 'Database changed during readonly tests')
    (OUT / 'EXECUTION_EXIT_CODE.txt').write_text('0\n' if strict_pass else '1\n', encoding='utf-8')
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    if not strict_pass:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('SOURCE_FACT_PERSISTENCE = FAIL; HUMAN_REVIEW_GATE_2 = OPEN; READY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION = NO', file=sys.stderr)
        print(str(exc), file=sys.stderr)
        sys.exit(1)
