"""Verificación acotada del amendment; sin red, fuentes técnicas ni hash global."""
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
roadmap = business / '01_Governance/BUSINESS_MASTER_ROADMAP.md'
review = market / 'STAGE_1_CRITERIA_REEVALUATION.md'
gap = market / 'STAGE_1_EVIDENCE_GAP_PLAN.md'
decision = business / '01_Governance/DECISION_LOG.md'
status = business / 'BUSINESS_STATUS.md'
changed = [roadmap, review, gap, decision, status, Path(__file__).resolve()]
texts = {p: p.read_text(encoding='utf-8-sig') for p in changed}
checks = []

def check(name, passed, detail=None):
    checks.append({'name': name, 'passed': bool(passed), 'detail': detail})

expected = [f'S1-ENTRY-{i:02}' for i in range(1, 4)] + [f'S1-EXIT-{i:02}' for i in range(1, 13)]
for path in (roadmap, review):
    ids = re.findall(r'^\| (S1-(?:ENTRY|EXIT)-\d+) \|', texts[path], re.M)
    check(path.name + ': 15 criteria in order, no omissions or duplicates', ids == expected)
rows = re.findall(r'^\| (S1-(?:ENTRY|EXIT)-\d+) \| ([A-Z_]+) \|', texts[review], re.M)
check('Criterion results: 14 PASS and EXIT-09 insufficient', dict(rows) == {eid: ('INSUFFICIENT_EVIDENCE' if eid == 'S1-EXIT-09' else 'PASS') for eid in expected})
for path in (review, status, decision):
    check(path.name + ': conservative current outcome', all(s in texts[path] for s in ('STAGE_1_EXECUTION = INCOMPLETE', 'GATE_READINESS = NOT_READY_FOR_HUMAN_GATE', 'STAGE_1_GATE = NOT_REACHED')))
check('Decision ID unique', len(re.findall(r'^\| BUS-DEC-024 \|', texts[decision], re.M)) == 1)
check('Roadmap formal name and categories', all(s in texts[roadmap] for s in ('STAGE 1 — DESK MARKET DISCOVERY / EVIDENCE BASELINE', 'LEGAL OBLIGATION', 'FORMAL REQUIREMENT', 'STANDARD', 'RECOMMENDATION', 'BEST PRACTICE', 'POTENTIAL GAP', 'NOT_APPLICABLE')))
check('Gap plan only five authorized columns and one affected criterion', re.findall(r'^\| ([^\n]+) \|$', texts[gap], re.M)[0].split(' | ') == ['Criterio afectado', 'Evidencia existente', 'Evidencia faltante', 'Tipo de fuente necesaria', 'Pregunta que debe resolverse'] and len(re.findall(r'^\| S1-EXIT-09 \|', texts[gap], re.M)) == 1 and len(re.findall(r'^\|', texts[gap], re.M)) == 3)
register = (market / 'MARKET_EVIDENCE_REGISTER.md').read_text(encoding='utf-8-sig')
annex = (market / 'STAGE_1_EVIDENCE_REUSE.md').read_text(encoding='utf-8-sig')
eids = [f'MKT-EVD-{i:03}' for i in range(1, 37)]
check('Existing register and reused annex retain 36 IDs', all(re.findall(r'^## (MKT-EVD-\d+)\s*$', t, re.M) == eids for t in (register, annex)))
baseline = (business / '02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md').read_text(encoding='utf-8-sig')
check('Five counted capabilities documented EXISTING', all(f'**TDL-CAP-{i:03}**' in baseline.split('## Capacidades EXISTING', 1)[1].split('## Documentos integrantes', 1)[0] for i in (1, 2, 3, 4, 11)))
check('All eight ASM reviewed without state change', all(f'BUS-ASM-{i:03}' in texts[review] for i in range(1, 9)) and 'PROPOSED_STATUS_CHANGE = NONE' in texts[review])
old = (market / 'STAGE_1_GATE_REVIEW.md').read_text(encoding='utf-8-sig')
check('Previous incomplete attempt remains explicit', 'STAGE_1_EXECUTION = INCOMPLETE' in old and 'roadmap no enumera criterios' in old and 'Primera ejecución' in texts[review])
missing = []
for path in changed:
    if path.suffix != '.md':
        continue
    for link in re.findall(r'\]\(([^)]+)\)', texts[path]):
        if '://' in link or link.startswith('#'):
            continue
        target = (path.parent / link.split('#', 1)[0]).resolve()
        if not target.exists() and target not in (out / 'verification.json', out / 'exit_code.txt'):
            missing.append({'document': path.name, 'target': link})
check('Local references resolve', not missing, missing)
git = {}
for name, args in (('status', ['status', '--short']), ('diff_names', ['diff', '--name-only']), ('diff_check', ['diff', '--check'])):
    proc = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True)
    git[name] = {'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    check('Git ' + name, proc.returncode == 0)
result = {
    'date': datetime.now(timezone.utc).isoformat(),
    'package_verification': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
    'stage_1_execution': 'INCOMPLETE', 'gate_readiness': 'NOT_READY_FOR_HUMAN_GATE',
    'stage_1_gate': 'NOT_REACHED', 'stage_2': 'NOT AUTHORIZED',
    'criteria': dict(rows), 'checks': checks,
    'modified_document_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in changed},
    'git': git, 'new_external_evidence': 0, 'assumption_changes': [],
    'repository_wide_hash': False, 'resource_guard_triggered': False,
    'limitations': ['Document structure and references only; criterion judgments are in the review.', 'No human gate approval, external freshness or global immutability certification.', 'Historical attempt/evidence untouched; no historical verifier rerun.', 'Only six written files hashed; V1 and technical sources not hashed.'],
}
(out / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
code = 0 if result['package_verification'] == 'PASS' else 1
(out / 'exit_code.txt').write_text(str(code) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(code)
