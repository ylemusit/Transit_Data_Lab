"""Read-only post-S1 validation; preserves historical validator expectations.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import json
import re
from pathlib import Path
from m06_b02_pack import run, query, save, snapshot, sha, package, setup, preflight, equal, TESTS

# Only pre-population assertions superseded by the expressly approved +9 batch.
# Their replacement is B02D plus exact old-row preservation and full row equality.
HISTORICAL = {
    'm06_b02c_scope_schema': {'EMPTY_SCOPE_STATE', 'GLOBAL_MAPPINGS', 'LEGACY_SCOPE_ASSIGNMENTS', 'B02_MAPPINGS', 'B02_BRIDGES', 'B02_SCOPE_ROWS', 'B02_SOURCE_BRIDGES'},
    'm06_b02a_requirement_concepts': {'B02_BRIDGES', 'B02_MAPPINGS', 'PROTECTED_COUNTERS'},
    'm06_b02a_populated_schema': {'B02_MAPPINGS', 'B02_BRIDGES', 'LEGACY_MAPPINGS'},
    'm06_b01_candidates': {'TOTALS'},
    'm05b_family_baseline_v1': {'NONPILOT_MAPPINGS'},
}
NAMES = ['m06_b02d_s1', 'm06_b02c_scope_schema', 'm06_b02a_requirement_concepts',
         'm06_b02a_populated_schema', 'level_a', 'm04_pilot', 'm04b_semantic_coverage',
         'm05b_family_baseline_v1', 'm06_b01_candidates', 'exception_accounting']


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', required=True, type=Path)
    p.add_argument('--evidence', required=True, type=Path)
    p.add_argument('--baseline', required=True, type=Path)
    p.add_argument('--closure-coverage', action='store_true', help='Validate the two authorized final-closure coverage rows as an additional exact delta.')
    a = p.parse_args()
    coverage_entities = []
    if a.closure_coverage:
        from m06_b02_closure import coverage_entity
        coverage_entities = [coverage_entity()]
        HISTORICAL['m04b_semantic_coverage'] = {'NON_PILOT_COVERAGE'}
        HISTORICAL['m06_b02d_s1'] = {'B02_COVERAGE_UNCHANGED'}
        HISTORICAL['m06_b02c_scope_schema'].update({'B02_COVERAGE', 'COVERAGE_GLOBAL'})
        HISTORICAL['m06_b02a_populated_schema'].add('B02_COVERAGE')
    a.evidence.mkdir(parents=True, exist_ok=True)
    before_hash = sha(a.db)
    results = {}
    for name in NAMES:
        sql = (TESTS / ('validate_phase_3_' + name + '.sql')).read_text(encoding='utf-8-sig')
        raw = run(a.db, sql)
        save(a.evidence / (name + '.json'), raw)
        if name in ('m04_pilot', 'exception_accounting'):
            baseline = run(a.baseline, sql)
            save(a.evidence / (name + '_baseline.json'), baseline)
            if raw['exit_code'] or baseline['exit_code']:
                results[name] = {'status': 'FAIL_BLOCKING', 'error': raw['stderr'] + baseline['stderr']}
                continue
            current = json.JSONDecoder().raw_decode(raw['stdout'])[0][0]
            previous = json.JSONDecoder().raw_decode(baseline['stdout'])[0][0]
            if name == 'm04_pilot':
                status_key = 'm04_pilot_structural_validation'
                ignored = {status_key, 'non_pilot_mappings'}
                ok = previous[status_key] == 'PASS' and current['non_pilot_mappings'] == 9 and all(current[k] == v for k, v in previous.items() if k not in ignored)
            else:
                ok = current['global_exception_accounting'] == 'PASS' and current == previous
            results[name] = {'status': 'PASS' if ok else 'FAIL_BLOCKING', 'original_result': current}
            continue
        prefix = re.split(r'\),\s*(?:summary|totals) AS\s*\(|\)\s*SELECT CASE WHEN', sql, maxsplit=1, flags=re.I)[0]
        # The first matching final CTE boundary must follow checks AS.
        detail_sql = prefix + ') SELECT * FROM checks;'
        detail = run(a.db, detail_sql)
        save(a.evidence / (name + '_checks.json'), detail)
        failures = []
        historical = []
        if raw['exit_code'] or detail['exit_code']:
            results[name] = {'status': 'FAIL_BLOCKING', 'error': raw['stderr'] + detail['stderr']}
            continue
        for row in json.loads(detail['stdout']):
            key = row.get('check_name')
            values = [v for k, v in row.items() if k != 'check_name' and isinstance(v, (int, float))]
            if any(v != 0 for v in values):
                (historical if key in HISTORICAL.get(name, set()) else failures).append(row)
        results[name] = dict(status='FAIL_BLOCKING' if failures else 'PASS',
                             failures=failures, historical_state_mismatches=historical)
    entities = package(a.db)
    exact = setup(entities) + preflight(entities)
    entities += coverage_entities
    exact += setup(coverage_entities)
    for e in entities:
        exact += f"SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM {e['temp']} e WHERE NOT EXISTS(SELECT 1 FROM {e['table']} t WHERE {equal(e['cols'])})) THEN 'PASS' ELSE error('MISSING_EXPECTED_ROW') END AS exact_rows;\n"
    r = run(a.db, exact)
    save(a.evidence / 'row_exact.json', r)
    old = snapshot(a.baseline)
    new = snapshot(a.db)
    # SQL compares full multisets, not hashes alone. Old rows must all survive;
    # additions are exactly the expected package, and all other tables unchanged.
    escaped = str(a.baseline.resolve()).replace('\\', '/').replace("'", "''")
    delta = f"ATTACH '{escaped}' AS baseline (READ_ONLY);\n" + setup(entities)
    bytable = {e['table']: e for e in entities}
    for table in old:
        expected = f'SELECT * FROM baseline.{table}'
        if table in bytable:
            e = bytable[table]
            expected += f" UNION ALL SELECT e.* FROM {e['temp']} e WHERE NOT EXISTS(SELECT 1 FROM baseline.{table} t WHERE {equal(e['pk'])})"
        delta += f"SELECT CASE WHEN NOT EXISTS((SELECT * FROM {table} EXCEPT ALL ({expected})) UNION ALL (({expected}) EXCEPT ALL SELECT * FROM {table})) THEN 'PASS' ELSE error('PROTECTED_OR_DELTA_DRIFT') END AS exact_delta;\n"
    dr = run(a.db, delta)
    save(a.evidence / 'protected_delta.json', dr)
    save(a.evidence / 'snapshots.json', dict(before=old, after=new))
    results['row_exact'] = {'status': 'PASS' if r['exit_code'] == 0 else 'FAIL_BLOCKING'}
    results['protected_delta'] = {'status': 'PASS' if dr['exit_code'] == 0 else 'FAIL_BLOCKING'}
    results['readonly_hash'] = {'status': 'PASS' if before_hash == sha(a.db) else 'FAIL_BLOCKING', 'hash': sha(a.db)}
    save(a.evidence / 'summary.json', results)
    print(json.dumps(results, indent=2))
    if any(v['status'] != 'PASS' for v in results.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
