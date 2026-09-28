"""Read-only Phase 3 disposition inventory. Planning, never legal classification.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
from collections import Counter
from pathlib import Path
from m06_b02_pack import DB, query, save, sha

REASONS = {
    'F01': ('Falta evidencia contextual de acceso/designación/descubrimiento.', 'No acredita operación NAP.', 'Evidencia NAP identificable y contrato de inspección acotado.'),
    'F02': ('Perfil, constraints o aplicabilidad incompletos.', 'No acredita representación de todo el requisito.', 'Perfil versionado y crosswalk revisado por scope.'),
    'F03': ('Faltan registros fechados de disponibilidad y ámbito.', 'No acredita satisfacción temporal.', 'Registros de publicación y aplicabilidad revisados.'),
    'F04': ('Faltan contexto de metadatos, procedencia y solicitud.', 'Campos técnicos no prueban deber contextual.', 'Contrato y evidencia de procedencia/solicitud revisados.'),
    'F05': ('Sin historial observable de cambios/correcciones.', 'No puede evaluar actualización.', 'Historial versionado y contrato de comparación revisados.'),
    'F06': ('Sin métricas/criterios y evidencia de calidad/notificación.', 'No puede atribuir fallo de calidad.', 'Criterio acotado revisado y evidencia de ejecución.'),
    'F07': ('Sin evidencia de decisiones de reutilización/presentación.', 'No evalúa neutralidad ni ranking.', 'Casos y criterios revisados con evidencia contextual.'),
    'F08': ('Sin contrato ni observación de intercambio de resultados.', 'No evalúa solicitud/respuesta.', 'Interfaz y caso solicitud/respuesta revisados.'),
    'F09': ('Requiere registros institucionales/procedimentales.', 'Un formato no acredita actuación institucional.', 'Revisión humana con registros de autoridad/proceso.'),
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--evidence', type=Path, required=True)
    a = p.parse_args()
    a.evidence.mkdir(parents=True, exist_ok=False)
    initial = sha(DB)
    rows = query(DB, """SELECT r.requirement_id,r.requirement_class,f.family_id,c.coverage_state,c.coverage_id
    FROM compliance.requirements r JOIN mapping.phase3_requirement_families f USING(requirement_id)
    LEFT JOIN mapping.phase3_requirement_coverage c USING(requirement_id)
    WHERE f.relation_type='PRIMARY_FAMILY' ORDER BY f.family_id,r.requirement_id""")
    if len(rows) != 48 or len({r['requirement_id'] for r in rows}) != 48:
        raise RuntimeError('STOP_GLOBAL: SCOPE_RECONCILIATION')
    for r in rows:
        reason, impact, reopen = REASONS[r['family_id']]
        r.update(disposition='PARTIAL' if r['coverage_id'] else 'DEFERRED', reason=reason, impact=impact, reopen_condition=reopen)
    save(a.evidence/'requirements.json', rows)
    mappings = query(DB, 'SELECT * FROM mapping.phase3_requirement_capabilities ORDER BY mapping_id')
    existing = {r['mapping_id']:r for r in query(DB, 'SELECT * FROM mapping.phase3_automatability')}
    scopes = query(DB, 'SELECT * FROM mapping.phase3_mapping_scope_units ORDER BY scope_unit_id')
    autos = []
    for m in mappings:
        old = existing.get(m['mapping_id'])
        matched = [s for s in scopes if s['mapping_id']==m['mapping_id']]
        autos.append(dict(mapping_id=m['mapping_id'], scope_units=[s['scope_unit_id'] for s in matched],
            decision='PARTIALLY_AUTOMATABLE' if old else 'DEFERRED',
            basis=old['explanation'] if old else 'No representability contract demonstrated for this persisted scope; no parser/rule proof.',
            prerequisites=old['prerequisites'] if old else 'Versioned profile constraints, representability, controlled fixtures and false-positive validation.',
            persisted_state=old['automatability_state'] if old else None,
            operational_automation_proven=False))
    save(a.evidence/'automatability.json', autos)
    coverage = query(DB, 'SELECT * FROM mapping.phase3_requirement_coverage ORDER BY coverage_id')
    states = Counter(r['coverage_state'] for r in coverage)
    if len(coverage)!=10 or states != Counter(PARTIAL=9, UNRESOLVED=1):
        raise RuntimeError('STOP_GLOBAL: COVERAGE_STATE')
    save(a.evidence/'coverage.json', coverage)
    header = '# Phase 3 — disposición por requisito\n\nPlanificación operativa; no nueva interpretación jurídica. Sin escrituras DB.\n\n'
    header += '| Requirement | Familia | Disposición | Coverage actual | Razón | Impacto | Reapertura |\n|---|---|---|---|---|---|---|\n'
    for r in rows:
        header += '| ' + ' | '.join(str(r[k] or 'Sin decisión') for k in ['requirement_id','family_id','disposition','coverage_state','reason','impact','reopen_condition']) + ' |\n'
    header += '\nYeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'
    (a.evidence/'requirements.md').write_text(header,encoding='utf-8')
    if sha(DB)!=initial:
        raise RuntimeError('STOP_GLOBAL: DB_DRIFT')
    summary = dict(requirements=48, families=dict(Counter(r['family_id'] for r in rows)),
        disposition=dict(Counter(r['disposition'] for r in rows)), coverage=dict(states),
        automatability=dict(Counter(r['decision'] for r in autos)), scope_units=len(scopes),
        automated_proven=0, initial_hash=initial, final_hash=sha(DB))
    save(a.evidence/'summary.json',summary)
    print(summary)


if __name__ == '__main__':
    main()
