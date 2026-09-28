"""Current V1 planning dispositions; never modifies frozen requirements.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
from collections import Counter
from m06_b02_pack import DB, query, save
from phase3_scope_inventory import REASONS
from compliance_v1_pack import EVIDENCE, REQ


def reconcile():
    rows=query(DB,"""SELECT r.requirement_id,r.description,f.family_id,c.coverage_state
       FROM compliance.requirements r JOIN mapping.phase3_requirement_families f USING(requirement_id)
       LEFT JOIN mapping.phase3_requirement_coverage c USING(requirement_id)
       WHERE f.relation_type='PRIMARY_FAMILY' ORDER BY r.requirement_id""")
    if len(rows)!=48 or len({r['requirement_id'] for r in rows})!=48:
        raise RuntimeError('SCOPE_IDENTITY_COLLISION')
    for row in rows:
        rid=row['requirement_id'];family=row['family_id']
        reason,impact,reopen=REASONS[family]
        if '-A05-' in rid or rid.endswith(('A04-P01-002','A04-P01-004')):
            state='OUT_OF_SCOPE_V1';auto='OUT_OF_SCOPE_V1'
            reason='DEFERRED_BY_PRODUCT_SCOPE: realtime, road format or spatial-network track outside committed GTFS/NeTEx pilots.'
            impact='Historical obligation, mapping, review and coverage remain unchanged; no operational V1 claim.'
            reopen='GTFS + NeTEx V1 stable AND the relevant future track explicitly opened.'
        elif family in ('F03','F09'):
            state='HUMAN_REVIEW_REQUIRED';auto='HUMAN_REVIEW_REQUIRED'
        elif row['coverage_state']:
            state='PARTIAL';auto='PARTIALLY_AUTOMATABLE'
        else:
            state='DEFERRED';auto='DEFERRED'
        if rid==REQ:
            reason='Two operational technical subscopes demonstrated; broad NAP/static/historical/observed obligation not demonstrated.'
            impact='No claim that the full legal requirement is delivered.'
            reopen='Additional reviewed scopes and contextual NAP evidence.'
        row.update(disposition=state,automatability=auto,reason=reason,impact=impact,reopen_condition=reopen,
                   targets=['GTFS_TARGET','NETEX_TARGET'] if rid==REQ else [])
    families=[]
    for family in sorted(REASONS):
        members=[r for r in rows if r['family_id']==family]
        state='PARTIAL_WITH_ACCEPTED_LIMITS' if any(r['coverage_state'] for r in members) else 'DEFERRED'
        reason,impact,reopen=REASONS[family]
        families.append(dict(family_id=family,requirements=len(members),disposition=state,reason=reason,impact=impact,reopen_condition=reopen))
    mappings=query(DB,'SELECT mapping_id,capability_id FROM mapping.phase3_requirement_capabilities ORDER BY mapping_id')
    mapping_disposition=[]
    for m in mappings:
        scope='OUT_OF_SCOPE_V1' if m['mapping_id'].startswith('M06-B02-') else 'PARTIAL'
        m.update(disposition=scope,operational_in_v1=m['mapping_id'] in ('M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT'))
        mapping_disposition.append(m)
    coverage=query(DB,'SELECT * FROM mapping.phase3_requirement_coverage ORDER BY coverage_id')
    return dict(scope=dict(primary=['GTFS','NeTEx'],standby=['SIRI','GTFS-RT'],
                          standby_reason='DEFERRED_BY_PRODUCT_SCOPE',reopen_condition='GTFS + NeTEx V1 stable AND explicit future realtime track'),
                requirements=rows,families=families,mappings=mapping_disposition,coverage=coverage,
                counts=dict(requirements=dict(Counter(r['disposition'] for r in rows)),families=dict(Counter(f['disposition'] for f in families))))


if __name__=='__main__':
    data=reconcile();save(EVIDENCE/'dispositions.json',data)
    lines=['# Compliance V1 — disposiciones vigentes','',
           'Planificación del producto; no cambia interpretación, texto ni cobertura jurídica.','',
           '| Requirement | Familia | Disposición | Automatizabilidad | Razón | Impacto | Reapertura |',
           '|---|---|---|---|---|---|---|']
    for r in data['requirements']:
        lines.append('| '+' | '.join(str(r[k]) for k in ['requirement_id','family_id','disposition','automatability','reason','impact','reopen_condition'])+' |')
    lines+=['','## Familias','','| Familia | Requisitos | Disposición | Razón | Impacto | Reapertura |','|---|---|---|---|---|---|']
    for r in data['families']:
        lines.append('| '+' | '.join(str(r[k]) for k in ['family_id','requirements','disposition','reason','impact','reopen_condition'])+' |')
    lines+=['','Yeison Arbey Carrillo Lemus. Todos los derechos reservados.','']
    (EVIDENCE/'dispositions.md').write_text('\n'.join(lines),encoding='utf-8')
    print(data['counts'])
