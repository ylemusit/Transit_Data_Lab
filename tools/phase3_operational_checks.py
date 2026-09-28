"""Read-only inventory and isolated observation-contract tests; never promotes data.

Run with a NEW --evidence directory. Uses installed DuckDB CLI and stdlib.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import copy
import json
import shutil
from pathlib import Path
from m06_b02_pack import DB, ROOT, query, run, save, sha, snapshot
from phase3_observation_contract import VERSION, encode, decode, content_hash

EXPECTED = '6C7A944FB9EB7983A912AF42C2F5C69C0F29D268F6139D3B5566BF7140788E0F'
SCOPE = 'M06-B02-SCOPE-C07-ET-JOURNEY-DELAY-CANCELLATION'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    out = args.evidence.resolve()
    out.mkdir(parents=True, exist_ok=False)
    require(sha(DB) == EXPECTED and not Path(str(DB) + '.wal').exists(), 'STOP_GLOBAL: DB prestate')
    before = snapshot(DB)
    scopes = {r['scope_unit_id']: r for r in query(DB, 'SELECT * FROM mapping.phase3_mapping_scope_units')}
    mappings = {r['mapping_id']: r for r in query(DB, 'SELECT * FROM mapping.phase3_requirement_capabilities')}
    scope = scopes[SCOPE]
    mapping = mappings[scope['mapping_id']]
    save(out / 'schema.json', query(DB, "SELECT table_schema,table_name,column_name,data_type,is_nullable FROM information_schema.columns WHERE table_schema='audit' OR (table_schema='mapping' AND table_name IN ('phase3_observed_evidence','phase3_representability','phase3_automatability')) ORDER BY 1,2,ordinal_position"))
    save(out / 'constraints.json', query(DB, "SELECT * FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_observed_evidence'"))
    # These bytes test storage only: they are NOT SIRI fixtures or parser output.
    payload = b'{"synthetic_contract_payload":1}\n'
    (out / 'contract_payload.json').write_bytes(payload)
    base = dict(contract_version=VERSION, dataset_id='SYNTHETIC-CONTRACT-ONLY',
                dataset_version='1', dataset_sha256=content_hash(payload),
                inspection_run='contract-test-1', evaluator_version='contract-test/1',
                scope_unit_id=SCOPE, inspection_status='COMPLETED', observed_result='PRESENT',
                errors=[], limitations=['Storage test only; no SIRI inspection or representability assertion.'],
                inspection_extent='COMPLETE_DECLARED_LOCATOR', synthetic=True)
    cases = {}
    for name, status, result, errors in [
        ('present', 'COMPLETED', 'PRESENT', []),
        ('absent', 'COMPLETED', 'ABSENCE_CONFIRMED', []),
        ('boundary', 'COMPLETED', 'INDETERMINATE', []),
        ('not_inspected', 'NOT_INSPECTED', 'INDETERMINATE', []),
        ('failed', 'FAILED', 'INDETERMINATE', ['INJECTED_INSPECTION_FAILURE'])]:
        r = dict(base, inspection_run='contract-test-' + name, inspection_status=status, observed_result=result, errors=errors)
        cases[name] = r
        require(decode(encode(r, scopes), scopes) == r, 'ROUNDTRIP')
        require(encode(r, scopes) == encode(copy.deepcopy(r), scopes), 'DETERMINISM')
    rejected = []
    for name, delta in [
        ('uninspected_absent', dict(inspection_status='NOT_INSPECTED', observed_result='ABSENCE_CONFIRMED')),
        ('failed_absent', dict(inspection_status='FAILED', observed_result='ABSENCE_CONFIRMED', errors=['failure'])),
        ('partial_absent', dict(observed_result='ABSENCE_CONFIRMED', inspection_extent='PARTIAL')),
        ('unknown_enum', dict(observed_result='OPERATOR_NON_COMPLIANT')),
        ('version_mismatch', dict(contract_version='unknown/2')),
        ('unknown_scope', dict(scope_unit_id='missing')),
        ('bad_hash', dict(dataset_sha256='not-a-hash')),
        ('failure_without_reason', dict(inspection_status='FAILED', observed_result='INDETERMINATE')),
        ('indeterminate_without_reason', dict(observed_result='INDETERMINATE', limitations=[])),
        ('errors_on_completed', dict(errors=['error']))]:
        try:
            encode(dict(base, **delta), scopes)
        except ValueError as exc:
            rejected.append(dict(case=name, error=str(exc)))
        else:
            raise RuntimeError('UNDETECTED:' + name)
    save(out / 'contract_cases.json', cases)
    save(out / 'rejected_cases.json', rejected)
    # Actual existing schema and FK/CHECK constraints, on a disposable isolated copy.
    isolated = out / 'contract_isolated.duckdb'
    shutil.copy2(DB, isolated)
    require(sha(isolated) == EXPECTED, 'COPY_HASH')
    lit = lambda value: "'" + value.replace("'", "''") + "'"
    sql = 'BEGIN;\n'
    for name, record in cases.items():
        values = ['P3-CONTRACT-TEST-' + name, mapping['capability_id'], mapping['mapping_id'],
                  'FILE', 'synthetic://contract_payload.json#/', record['observed_result'],
                  '2026-09-28', encode(record, scopes), 'SYNTHETIC_TEST']
        sql += 'INSERT INTO mapping.phase3_observed_evidence VALUES (' + ','.join(map(lit, values)) + ');\n'
    sql += 'COMMIT;'
    (out / 'isolated_insert.sql').write_text(sql, encoding='utf-8')
    result = run(isolated, sql, readonly=False)
    save(out / 'isolated_insert_result.json', result)
    require(result['exit_code'] == 0, 'ISOLATED_INSERT_FAILED')
    rows = query(isolated, "SELECT * FROM mapping.phase3_observed_evidence WHERE evidence_id LIKE 'P3-CONTRACT-TEST-%' ORDER BY evidence_id")
    require(len(rows) == len(cases), 'ROW_COUNT')
    for row in rows:
        name = row['evidence_id'].removeprefix('P3-CONTRACT-TEST-')
        require(decode(row['notes'], scopes) == cases[name], 'PERSISTENCE_ROUNDTRIP')
        require(row['observed_value'] == cases[name]['observed_result'], 'RESULT_COLLISION')
        require(row['mapping_id'] == scope['mapping_id'] and row['capability_id'] == mapping['capability_id'], 'SCOPE_LINK')
    save(out / 'isolated_rows.json', rows)
    # Full-table exact preservation, excluding only the five synthetic test IDs.
    attached = str(DB).replace('\\', '/').replace("'", "''")
    delta = f"ATTACH '{attached}' AS original (READ_ONLY);\n"
    for table in before:
        actual = 'SELECT * FROM ' + table
        if table == 'mapping.phase3_observed_evidence':
            actual += " WHERE evidence_id NOT LIKE 'P3-CONTRACT-TEST-%'"
        expected = 'SELECT * FROM original.' + table
        delta += f"SELECT CASE WHEN NOT EXISTS(({actual} EXCEPT ALL {expected}) UNION ALL ({expected} EXCEPT ALL {actual})) THEN 'PASS' ELSE error('ISOLATED_DRIFT') END;\n"
    dr = run(isolated, delta)
    save(out / 'isolated_protected_delta.json', dr)
    require(dr['exit_code'] == 0, 'ISOLATED_DRIFT')
    # Deliberate transaction error must roll back an inserted row on isolated DB.
    isolated_before = snapshot(isolated)
    rollback = run(isolated, "BEGIN; INSERT INTO mapping.phase3_observed_evidence SELECT 'P3-ROLLBACK',capability_id,mapping_id,evidence_type,locator,observed_value,observed_on,notes,fixture_kind FROM mapping.phase3_observed_evidence LIMIT 1; SELECT error('INJECTED_ROLLBACK'); COMMIT;", readonly=False)
    save(out / 'rollback.json', rollback)
    require(rollback['exit_code'] != 0 and 'INJECTED_ROLLBACK' in rollback['stderr'] and snapshot(isolated) == isolated_before, 'ROLLBACK_FAILED')
    require(sha(DB) == EXPECTED and snapshot(DB) == before, 'STOP_GLOBAL: AUTHORITATIVE_DRIFT')
    save(out / 'summary.json', dict(status='PASS', contract_roundtrips=len(cases), negative_cases_rejected=len(rejected),
         isolated_rows=len(rows), authoritative_rows_added=0, schema_changes=0, rollback='PASS',
         initial_hash=EXPECTED, final_hash=sha(DB), evaluator_hash=sha(ROOT/'tools/phase3_observation_contract.py'),
         test_hash=sha(Path(__file__)), limitation='Storage contract only; no representability, SIRI fixture, parser, audit rule or operational end-to-end PASS.'))
    print((out / 'summary.json').read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
