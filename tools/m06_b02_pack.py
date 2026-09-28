"""Bounded M06-B02 S1 executor; Python stdlib + installed DuckDB CLI.

All stored columns are semantic: no generated columns exist in these eight
tables. Original seeds remain immutable input. Only their INSERT VALUES are
loaded into TEMP expected tables; historical absence guards are not executed.
Author: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / '03_Compliance/databases/transit_compliance.duckdb'
SEEDS = ROOT / '03_Compliance/sql/03_mappings'
TESTS = ROOT / '03_Compliance/sql/07_tests/phase_3'
INITIAL = '0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F'
ORDER = ['capabilities', 'source_references', 'mappings', 'mapping_reviews',
         'concept_bridges', 'scope_units', 'scope_source_refs']


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest().upper()


def run(db, sql, readonly=True):
    command = ['duckdb', '-batch', '-bail', '-json']
    if readonly:
        command.append('-readonly')
    command.append(str(db))
    proc = subprocess.run(command, input=sql, text=True, encoding='utf-8',
                          capture_output=True, cwd=ROOT)
    return dict(command=command, exit_code=proc.returncode,
                stdout=proc.stdout, stderr=proc.stderr)


def query(db, sql):
    r = run(db, sql)
    if r['exit_code']:
        raise RuntimeError(r)
    return json.loads(r['stdout'] or '[]')


def statements(sql):
    # SQL literals may contain semicolons and escaped single quotes.
    sql = re.sub(r'^\s*--.*$', '', sql, flags=re.M)
    return re.findall(r"(?:'[^']*(?:''[^']*)*'|[^;'])+;", sql)


def guard(condition, label):
    return f"SELECT CASE WHEN {condition} THEN '{label}:PASS' ELSE error('{label}') END AS check_result;\n"


def equal(cols, a='e', b='t'):
    return ' AND '.join(f'{a}.{c} IS NOT DISTINCT FROM {b}.{c}' for c in cols)


def package(db):
    entities = []
    for suffix in ORDER:
        for stmt in statements((SEEDS / f'phase3_m06_b02d_{suffix}_seed.sql').read_text(encoding='utf-8-sig')):
            m = re.fullmatch(r'\s*INSERT INTO (mapping\.\w+)\s*\(([^)]+)\)\s*VALUES\s*(.*);', stmt, re.S | re.I)
            if m:
                table, cols, values = m.groups()
                cols = [c.strip() for c in cols.split(',')]
                entities.append(dict(table=table, cols=cols, values=values,
                                     temp='expected_' + table.split('.')[1]))
    if len(entities) != 8:
        raise RuntimeError('Expected exactly seven entities plus SIRI identity')
    constraints = query(db, "SELECT table_name,constraint_type,constraint_column_names,referenced_table,referenced_column_names FROM duckdb_constraints() WHERE schema_name='mapping' AND constraint_type IN ('PRIMARY KEY','UNIQUE','FOREIGN KEY')")
    for e in entities:
        actual = [r['column_name'] for r in query(db, f"SELECT column_name FROM information_schema.columns WHERE table_schema='mapping' AND table_name='{e['table'].split('.')[1]}' ORDER BY ordinal_position")]
        if set(actual) != set(e['cols']):
            raise RuntimeError('Unclassified semantic/generated columns: ' + e['table'])
        e['constraints'] = [c for c in constraints if c['table_name'] == e['table'].split('.')[1]]
        e['pk'] = next(c['constraint_column_names'] for c in e['constraints'] if c['constraint_type'] == 'PRIMARY KEY')
    return entities


def setup(entities):
    return ''.join(f"CREATE TEMP TABLE {e['temp']} AS SELECT * FROM {e['table']} WHERE false;\nINSERT INTO {e['temp']} ({','.join(e['cols'])}) VALUES {e['values']};\n" for e in entities)


def preflight(entities):
    result = ''
    temps = {e['table'].split('.')[1]: e['temp'] for e in entities}
    # Conservative package-local natural identities, including tables without UNIQUE.
    natural = {
        'phase3_standards': ['standard_kind', 'version', 'profile'],
        'phase3_capabilities': ['standard_id', 'domain', 'entity', 'field_or_element'],
        'phase3_source_references': ['capability_id', 'source_kind', 'url_or_document_id', 'section', 'version'],
    }
    for e in entities:
        t, x, cols = e['table'], e['temp'], e['cols']
        result += guard(f'(SELECT count(*) FROM {x})={1 if t.endswith("phase3_standards") else 9}', 'EXPECTED_COUNT_' + x)
        keys = [c['constraint_column_names'] for c in e['constraints'] if c['constraint_type'] in ('PRIMARY KEY', 'UNIQUE')]
        if t.split('.')[1] in natural:
            keys.append(natural[t.split('.')[1]])
        for i, key in enumerate(keys):
            result += guard(f'NOT EXISTS(SELECT 1 FROM {x} GROUP BY {",".join(key)} HAVING count(*)>1)', f'DUPLICATE_{x}_{i}')
            result += guard(f'NOT EXISTS(SELECT 1 FROM {x} e JOIN {t} t ON {equal(key)} WHERE NOT ({equal(cols)}))', f'CONFLICT_{x}_{i}')
        for i, c in enumerate(e['constraints']):
            if c['constraint_type'] != 'FOREIGN KEY':
                continue
            parent = c['referenced_table']
            union = 'SELECT * FROM mapping.' + parent
            if parent in temps:
                union += ' UNION ALL SELECT * FROM ' + temps[parent]
            match = ' AND '.join(f'e.{a} IS NOT DISTINCT FROM p.{b}' for a, b in zip(c['constraint_column_names'], c['referenced_column_names']))
            nonnull = ' AND '.join('e.' + a + ' IS NOT NULL' for a in c['constraint_column_names'])
            result += guard(f'NOT EXISTS(SELECT 1 FROM {x} e WHERE {nonnull} AND NOT EXISTS(SELECT 1 FROM ({union}) p WHERE {match}))', f'FK_{x}_{i}')
    result += guard("NOT EXISTS(SELECT 1 FROM expected_phase3_requirement_capabilities e LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL OR e.mapping_type IS DISTINCT FROM 'PARTIAL')", 'REQUIREMENTS_PARTIAL')
    result += guard('NOT EXISTS(SELECT 1 FROM expected_phase3_concept_mappings e JOIN mapping.phase3_requirement_concepts c USING(concept_id) JOIN expected_phase3_requirement_capabilities m USING(mapping_id) WHERE c.requirement_id IS DISTINCT FROM m.requirement_id)', 'CONCEPT_ALIGNMENT')
    return result


def inserts(entities):
    return [f"INSERT INTO {e['table']} ({','.join(e['cols'])}) SELECT {','.join('e.'+c for c in e['cols'])} FROM {e['temp']} e WHERE NOT EXISTS(SELECT 1 FROM {e['table']} t WHERE {equal(e['pk'])});\n" for e in entities]


def transaction(db, entities, inject=False):
    # Snapshot every persistent table in this small compliance DB; preserve full
    # old rows, not aggregate counts. No corpus or external databases are read.
    tables = query(db, "SELECT table_schema||'.'||table_name AS name FROM information_schema.tables WHERE table_type='BASE TABLE' ORDER BY 1")
    bytable = {e['table']: e for e in entities}
    sql = setup(entities) + preflight(entities) + 'BEGIN TRANSACTION;\n' + preflight(entities)
    for i, t in enumerate(tables):
        sql += f"CREATE TEMP TABLE before_{i} AS SELECT * FROM {t['name']};\n"
    for i, e in enumerate(entities):
        sql += f"SELECT '{e['table']}' entity, count(*) FILTER(WHERE NOT EXISTS(SELECT 1 FROM {e['table']} t WHERE {equal(e['pk'])})) missing, count(*) FILTER(WHERE EXISTS(SELECT 1 FROM {e['table']} t WHERE {equal(e['cols'])})) matching FROM {e['temp']} e;\n"
        sql += inserts(entities)[i]
        if inject and i == 3:
            sql += "SELECT error('INJECTED_MID_TRANSACTION_FAILURE');\n"
    sql += preflight(entities)
    for i, t in enumerate(tables):
        name = t['name']
        e = bytable.get(name)
        expected = f'SELECT * FROM before_{i}'
        if e:
            expected += f" UNION ALL SELECT e.* FROM {e['temp']} e WHERE NOT EXISTS(SELECT 1 FROM before_{i} t WHERE {equal(e['pk'])})"
        sql += guard(f'NOT EXISTS((SELECT * FROM {name} EXCEPT ALL ({expected})) UNION ALL (({expected}) EXCEPT ALL SELECT * FROM {name}))', 'EXACT_DELTA_' + name.replace('.', '_'))
    validator = (TESTS / 'validate_phase_3_m06_b02d_s1.sql').read_text(encoding='utf-8-sig')
    validator = re.sub(r"SELECT CASE WHEN failures=0 THEN 'PASS' ELSE 'FAIL' END status", "SELECT CASE WHEN failures=0 THEN 'PASS' ELSE error('B02D_POSTCHECK') END status", validator)
    return sql + validator + '\nCOMMIT;\n'


def snapshot(db):
    result = {}
    for t in query(db, "SELECT table_schema||'.'||table_name AS name FROM information_schema.tables WHERE table_type='BASE TABLE' ORDER BY 1"):
        rows = query(db, 'SELECT * FROM ' + t['name'])
        canonical = sorted(json.dumps(r, sort_keys=True, ensure_ascii=False) for r in rows)
        result[t['name']] = {'count': len(rows), 'sha256': hashlib.sha256('\n'.join(canonical).encode()).hexdigest()}
    return result


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['test', 'apply'])
    p.add_argument('--evidence', required=True, type=Path)
    args = p.parse_args()
    out = args.evidence.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if sha(DB) != INITIAL or Path(str(DB) + '.wal').exists():
        raise RuntimeError('Baseline hash/WAL mismatch: STOP GLOBAL')
    entities = package(DB)
    seed_hashes = {str(f.relative_to(ROOT)): sha(f) for f in SEEDS.glob('phase3_m06_b02d_*_seed.sql')}
    if args.mode == 'test':
        save(out / 'before.json', snapshot(DB))
        save(out / 'entities.json', entities)
        baseline = run(DB, (TESTS / 'validate_phase_3_m06_b02d_s1_preflight.sql').read_text(encoding='utf-8-sig'))
        save(out / 'stage0.json', baseline)
        if baseline['exit_code'] or json.loads(baseline['stdout'])[0]['status'] != 'PASS':
            raise RuntimeError('Stage 0 failed')
        sql = transaction(DB, entities)
        (out / 'execution.sql').write_text(sql, encoding='utf-8')
        outcomes = {}
        for label in ['A_fresh', 'C_partial', 'D_conflict', 'E_rollback', 'F_natural_key', 'G_duplicate', 'H_fk']:
            copy = out / (label + '.duckdb')
            if copy.exists():
                raise RuntimeError('Never overwrite isolated evidence: ' + str(copy))
            shutil.copy2(DB, copy)
            if label == 'C_partial':
                r = run(copy, setup(entities) + 'BEGIN;\n' + ''.join(inserts(entities)[:3]) + 'COMMIT;', False)
                save(out / (label + '_setup.json'), r)
                if r['exit_code']:
                    raise RuntimeError(r)
            if label in ('D_conflict', 'F_natural_key'):
                e = entities[0]
                mutation = "UPDATE expected_phase3_standards SET source_metadata='CONFLICT'" if label == 'D_conflict' else "UPDATE expected_phase3_standards SET standard_id='TEST-NATURAL-COLLISION'"
                r = run(copy, setup(entities) + mutation + '; INSERT INTO mapping.phase3_standards SELECT * FROM expected_phase3_standards;', False)
                if r['exit_code']:
                    raise RuntimeError(r)
            before = snapshot(copy)
            test_sql = transaction(copy, entities, inject=label == 'E_rollback')
            if label == 'G_duplicate':
                test_sql = setup(entities) + 'INSERT INTO expected_phase3_standards SELECT * FROM expected_phase3_standards;\n' + preflight(entities)
            if label == 'H_fk':
                test_sql = setup(entities) + "UPDATE expected_phase3_capabilities SET standard_id='NO-SUCH-STANDARD';\n" + preflight(entities)
            r = run(copy, test_sql, False)
            save(out / (label + '.json'), r)
            failing = label not in ('A_fresh', 'C_partial')
            after = snapshot(copy)
            save(out / (label + '_snapshots.json'), dict(before=before, after=after))
            markers = {'D_conflict': 'CONFLICT_', 'E_rollback': 'INJECTED_MID_TRANSACTION_FAILURE',
                       'F_natural_key': 'CONFLICT_', 'G_duplicate': 'EXPECTED_COUNT_', 'H_fk': 'FK_'}
            ok = (r['exit_code'] != 0 and markers[label] in r['stderr'] and after == before) if failing else r['exit_code'] == 0
            outcomes[label] = 'PASS' if ok else 'FAIL_BLOCKING'
            if label == 'A_fresh' and ok:
                after_a = snapshot(copy)
                r2 = run(copy, transaction(copy, entities), False)
                save(out / 'B_second.json', r2)
                outcomes['B_second'] = 'PASS' if r2['exit_code'] == 0 and snapshot(copy) == after_a else 'FAIL_BLOCKING'
        summary = dict(initial_hash=sha(DB), seed_hashes=seed_hashes, tests=outcomes,
                       executor_hash=sha(Path(__file__)), execution_hash=sha(out / 'execution.sql'))
        save(out / 'tests.json', summary)
        print(json.dumps(summary, indent=2))
    else:
        summary = json.loads((out / 'tests.json').read_text(encoding='utf-8'))
        if not all(s == 'PASS' for s in summary['tests'].values()) or len(summary['tests']) != 8:
            raise RuntimeError('Isolated tests not PASS')
        if summary['seed_hashes'] != seed_hashes or summary['executor_hash'] != sha(Path(__file__)):
            raise RuntimeError('Package changed since isolated tests')
        sql = transaction(DB, entities)
        if sha(out / 'execution.sql') != summary['execution_hash'] or sql != (out / 'execution.sql').read_text(encoding='utf-8'):
            raise RuntimeError('Execution SQL changed since isolated tests')
        backup = out / 'authoritative_before.duckdb'
        if backup.exists():
            raise RuntimeError('Backup already exists')
        shutil.copy2(DB, backup)
        if sha(backup) != INITIAL or sha(DB) != INITIAL:
            raise RuntimeError('Backup/source hash mismatch')
        result = run(DB, sql, False)
        save(out / 'authoritative_execution.json', result)
        save(out / 'after.json', snapshot(DB))
        save(out / 'authoritative_result.json', dict(exit_code=result['exit_code'], initial_hash=INITIAL, final_hash=sha(DB)))
        print(json.dumps({'exit_code': result['exit_code'], 'final_hash': sha(DB)}))
        if result['exit_code']:
            raise RuntimeError('Authoritative execution failed: STOP; inspect rollback')


if __name__ == '__main__':
    main()
