"""Bounded final B02 coverage persistence; no schema or mapping changes.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from m06_b02_pack import DB, ROOT, equal, guard, query, run, save, setup, sha, snapshot

INITIAL = '657A48BF6472F958980646193F8CBAA81C01F316D2385D0F4E81F7EF13BAA791'
BASELINE = ROOT / '03_Compliance/reports/phase_3/evidence/m06_b02_orchestrated_20260928_04/authoritative_before.duckdb'
COLS = ['coverage_id', 'requirement_id', 'coverage_state', 'semantic_review_outcome',
        'justification', 'limitations', 'identified_paths', 'review_status',
        'reviewed_by', 'reviewed_at', 'reviewed_against_baseline']


def coverage_entity():
    rows = []
    for part, suffix, categories, rationale, limits in [
        ('P01', '002', ['DATEX-' + c for c in ['4-SN-A','4-SN-B','4-SN-C','4-SN-D','5-SN-A','5-SN-B','5-SN-C']],
         'Evaluated B02 scope: ROAD_STATUS_DISRUPTION only. Persisted C01 category-specific partial mappings support a bounded part of the road dynamic-data requirement. PARTIAL is a semantic review, not a ratio of mappings. DATEX II RTTI RRP 2022/670 evidence; individual releases remain unresolved.',
         'Not exhaustive; not observed implementation; not legal compliance conclusion. 5-SN-D deferred: profile/identity ambiguity. Frozen 2015/962 literal reference preserved; 2022/670 succession context is not a legal substitution. Other dynamic road-data scope and exact releases not established.'),
        ('P02', '001', ['SIRI-ET','SIRI-SX'],
         'Evaluated B02 scope: conditional Annex 2.1/2.2 concepts, with support limited to PASSENGER_RT_STATUS_DISRUPTION through C07 ET/SX. SIRI 2.1 / EPIP-RT CEN/TS 15531-7:2025. The accepted partial mappings support PARTIAL semantic coverage without establishing all concepts; no count-based percentage.',
         'Not exhaustive; not observed implementation; not legal compliance conclusion. Gaps: C04 Article 5(2) road applicability; C08 normative FM/facility element path; CM guaranteed-connections bridge; U01 PARKING_TARIFF minimum general profile/version/elements and applicability; U02 SHARED_VEHICLE_AVAILABILITY modal profile/element evidence; U03 PARKING_AVAILABILITY on/off-street minimum profile and crosswalk. All deferred for closure; exact profile constraints and representability not established.')]:
        paths = ';'.join('MAPPING:M06-B02-MAP-A05-' + part + '-' + suffix + '-' + c for c in categories)
        rows.append(['M06-B02-COV-A05-' + part + '-' + suffix,
                     'EU-2017-1926-REQ-A05-' + part + '-' + suffix,
                     'PARTIAL', 'ACCEPTED_WITH_LIMITATIONS', rationale, limits, paths,
                     'REVIEWED', 'Yeison Arbey Carrillo Lemus', '2026-09-28',
                     'M06_B02_FINAL_CLOSURE_2026-09-28; S1+B02A; PRE_DB_SHA256=' + INITIAL])
    literal = lambda s: "'" + s.replace("'", "''") + "'"
    return dict(table='mapping.phase3_requirement_coverage', cols=COLS,
                pk=['coverage_id'], temp='expected_closure_coverage',
                values=',\n'.join('(' + ','.join(map(literal, row)) + ')' for row in rows))


def transaction(db, inject=False):
    e = coverage_entity()
    check = guard(f"NOT EXISTS(SELECT 1 FROM {e['temp']} e JOIN {e['table']} t ON e.coverage_id=t.coverage_id OR e.requirement_id=t.requirement_id WHERE NOT ({equal(COLS)}))", 'COVERAGE_CONFLICT')
    check += guard(f"NOT EXISTS(SELECT 1 FROM {e['temp']} e LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL)", 'COVERAGE_REQUIREMENT')
    tables = query(db, "SELECT table_schema||'.'||table_name AS name FROM information_schema.tables WHERE table_type='BASE TABLE' ORDER BY 1")
    sql = 'BEGIN;\n' + setup([e]) + check
    for i, t in enumerate(tables):
        sql += f"CREATE TEMP TABLE before_{i} AS SELECT * FROM {t['name']};\n"
    sql += f"INSERT INTO {e['table']} SELECT e.* FROM {e['temp']} e WHERE NOT EXISTS(SELECT 1 FROM {e['table']} t WHERE {equal(e['pk'])});\n"
    if inject:
        sql += "SELECT error('INJECTED_ROLLBACK');\n"
    sql += check
    for i, t in enumerate(tables):
        expected = f'SELECT * FROM before_{i}'
        if t['name'] == e['table']:
            expected += f" UNION ALL SELECT e.* FROM {e['temp']} e WHERE NOT EXISTS(SELECT 1 FROM before_{i} t WHERE {equal(e['pk'])})"
        sql += guard(f"NOT EXISTS((SELECT * FROM {t['name']} EXCEPT ALL ({expected})) UNION ALL (({expected}) EXCEPT ALL SELECT * FROM {t['name']}))", 'EXACT_DELTA_' + str(i))
    return sql + 'COMMIT;\n'


def validate(db, out, coverage=False):
    command = [sys.executable, str(ROOT / 'tools/m06_b02_validate.py'), '--db', str(db), '--baseline', str(BASELINE), '--evidence', str(out)]
    if coverage:
        command.append('--closure-coverage')
    p = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', cwd=ROOT)
    save(out.parent / (out.name + '_command.json'), dict(command=command, exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr))
    if p.returncode:
        raise RuntimeError('Validator failed: ' + str(out))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['test', 'apply'])
    p.add_argument('--evidence', type=Path, required=True)
    a = p.parse_args()
    out = a.evidence.resolve()
    if sha(DB) != INITIAL or Path(str(DB) + '.wal').exists():
        raise RuntimeError('STOP GLOBAL: initial hash/WAL mismatch')
    if a.mode == 'test':
        out.mkdir(parents=True, exist_ok=False)
        validate(DB, out / 'pre_validation')
        sql = transaction(DB)
        (out / 'execution.sql').write_text(sql, encoding='utf-8')
        inventory = {}
        for table in ['phase3_requirement_concepts','phase3_requirement_capabilities','phase3_mapping_reviews','phase3_concept_mappings','phase3_mapping_scope_units','phase3_source_references','phase3_scope_source_references','phase3_standards','phase3_capabilities','phase3_requirement_coverage']:
            inventory[table] = query(DB, 'SELECT * FROM mapping.' + table)
        inventory['constraints'] = query(DB, "SELECT * FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_requirement_coverage'")
        save(out / 'inventory.json', inventory)
        outcomes = {}
        for name in ['fresh','conflict','rollback']:
            target = out / (name + '.duckdb')
            shutil.copy2(DB, target)
            if name == 'conflict':
                r = run(target, setup([coverage_entity()]) + "UPDATE expected_closure_coverage SET coverage_id='CONFLICT-ID',justification='CONFLICT' WHERE coverage_id LIKE '%P01%'; INSERT INTO mapping.phase3_requirement_coverage SELECT * FROM expected_closure_coverage WHERE coverage_id='CONFLICT-ID';", False)
                assert r['exit_code'] == 0, r
            before = snapshot(target)
            r = run(target, transaction(target, inject=name == 'rollback'), False)
            save(out / (name + '.json'), r)
            after = snapshot(target)
            save(out / (name + '_snapshots.json'), dict(before=before, after=after))
            if name == 'fresh':
                assert r['exit_code'] == 0, r
                validate(target, out / 'isolated_validation', True)
                r2 = run(target, sql, False)
                save(out / 'noop.json', r2)
                assert r2['exit_code'] == 0 and snapshot(target) == after
                outcomes['noop'] = 'PASS'
            else:
                assert r['exit_code'] != 0 and before == after
                assert ('COVERAGE_CONFLICT' if name == 'conflict' else 'INJECTED_ROLLBACK') in r['stderr']
            outcomes[name] = 'PASS'
        assert sha(DB) == INITIAL
        save(out / 'tests.json', dict(tests=outcomes, executor_hash=sha(Path(__file__)), validator_hash=sha(ROOT / 'tools/m06_b02_validate.py'), sql_hash=sha(out / 'execution.sql')))
        print(json.dumps(outcomes))
    else:
        tests = json.loads((out / 'tests.json').read_text())
        assert tests['tests'] == dict(noop='PASS', fresh='PASS', conflict='PASS', rollback='PASS')
        assert tests['executor_hash'] == sha(Path(__file__)) and tests['validator_hash'] == sha(ROOT / 'tools/m06_b02_validate.py')
        assert tests['sql_hash'] == sha(out / 'execution.sql')
        sql = transaction(DB)
        assert sql == (out / 'execution.sql').read_text(encoding='utf-8')
        backup = out / 'authoritative_before.duckdb'
        assert not backup.exists()
        shutil.copy2(DB, backup)
        assert sha(backup) == INITIAL and sha(DB) == INITIAL
        r = run(DB, sql, False)
        save(out / 'authoritative_execution.json', r)
        save(out / 'authoritative_result.json', dict(initial_hash=INITIAL, final_hash=sha(DB), exit_code=r['exit_code']))
        assert r['exit_code'] == 0, r
        validate(DB, out / 'post_validation', True)
        save(out / 'final_rows.json', query(DB, "SELECT * FROM mapping.phase3_requirement_coverage WHERE coverage_id LIKE 'M06-B02-%' ORDER BY coverage_id"))
        print(json.dumps(dict(result='PASS', final_hash=sha(DB))))


if __name__ == '__main__':
    main()
