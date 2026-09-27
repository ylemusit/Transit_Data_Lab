"""Verificación documental acotada; no consulta red ni fuentes técnicas."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone

out = Path(__file__).resolve().parent
market = out.parent
business = market.parent
root = business.parent
review = market / 'STAGE_1_GATE_REVIEW.md'
annex = market / 'STAGE_1_EVIDENCE_REUSE.md'
checks = []

def check(name, passed, detail=None):
    checks.append({'name': name, 'passed': bool(passed), 'detail': detail})

text = review.read_text(encoding='utf-8')
check('15 requested review sections', len(re.findall(r'^## \d+\.', text, re.M)) == 15)
check('Conservative execution and readiness', 'STAGE_1_EXECUTION = INCOMPLETE' in text and 'GATE_READINESS = NOT_READY_FOR_HUMAN_GATE' in text)
check('Four conclusion classes', all(c in text for c in ('FACT', 'SUPPORTED INTERPRETATION', 'ASSUMPTION', 'UNKNOWN')))
check('Human gate remains pending', 'HUMAN_GATE_DECISION = PENDING' in text and 'Stage 2 = NOT AUTHORIZED' in text)
check('No assumption state change', 'PROPOSED_STATUS_CHANGE = NONE' in text)
check('Criteria omission explicit', all(c in text for c in ('No existe en el roadmap una lista', 'No se inventan.', '| FAIL |')))
annex_text = annex.read_text(encoding='utf-8')
ids = re.findall(r'^## (MKT-EVD-\d+)$', annex_text, re.M)
check('36 distinct reused evidence IDs', ids == [f'MKT-EVD-{i:03}' for i in range(1, 37)])
register = (market / 'MARKET_EVIDENCE_REGISTER.md').read_text(encoding='utf-8-sig')
blocks = re.split(r'^## (MKT-EVD-\d+)\s*$', register, flags=re.M)
metadata_errors = []
for i in range(1, len(blocks), 2):
    eid, body = blocks[i:i+2]
    fields = dict(re.findall(r'^\| ([^|]+) \| (.*?) \|\s*$', body, re.M))
    if not all(k in fields for k in ('Tipo', 'Descripción', 'Fuente', 'Fecha fuente', 'Fecha consulta', 'Geografía', 'Limitaciones')):
        metadata_errors.append(eid)
    section = annex_text.split('## '+eid+'\n', 1)[1].split('\n## ', 1)[0]
    for k in ('Tipo', 'Descripción', 'Fuente', 'Fecha fuente', 'Fecha consulta', 'Geografía', 'Limitaciones'):
        if fields.get(k, '') not in section:
            metadata_errors.append(eid+': '+k)
check('Evidence metadata and limits retained verbatim', not metadata_errors, metadata_errors)
missing = []
for path in (review, annex):
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if '://' in link or link.startswith('#'):
            continue
        target = (path.parent / link.split('#', 1)[0]).resolve()
        if not target.exists() and target not in (out / 'verification.json', out / 'exit_code.txt'):
            missing.append({'document': path.name, 'target': link})
check('Local review and evidence links resolve', not missing, missing)
for directory, key in (('evidence', 'verification'), ('readiness_review', 'result')):
    data = json.loads((market / directory / 'verification.json').read_text(encoding='utf-8-sig'))
    code = (market / directory / 'exit_code.txt').read_text(encoding='utf-8-sig').strip()
    historical_checks = data['checks']
    check('Persisted full historical result: '+directory, data[key] == 'PASS' and code == '0' and all(c.get('passed', c.get('pass_', False)) for c in historical_checks))
git = {}
for name, args in (('status', ['status', '--short']), ('diff_names', ['diff', '--name-only']), ('diff_check', ['diff', '--check'])):
    proc = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True)
    git[name] = {'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    check('Git '+name+' completed', proc.returncode == 0)
changed = [review, annex, business / 'BUSINESS_STATUS.md', business / '01_Governance' / 'DECISION_LOG.md', Path(__file__).resolve()]
result = {
    'date': datetime.now(timezone.utc).isoformat(),
    'package_verification': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
    'stage_1_execution': 'INCOMPLETE',
    'gate_readiness': 'NOT_READY_FOR_HUMAN_GATE',
    'stage_2': 'NOT AUTHORIZED',
    'checks': checks,
    'modified_document_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in changed},
    'git': git,
    'new_external_evidence': 0,
    'assumption_changes': [],
    'repository_wide_hash': False,
    'resource_guard_triggered': False,
    'limitations': ['Structure and references only; no human gate approval.', 'Historical evidence reused without rerun or external refresh.', 'Hashes only of files written in this execution; no current V1 hash certification.', 'Grouped untracked Git cannot prove global immutability.'],
}
out.mkdir(exist_ok=True)
(out / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
code = 0 if result['package_verification'] == 'PASS' else 1
(out / 'exit_code.txt').write_text(str(code)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(code)
