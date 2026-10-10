"""Generate a bounded quality snapshot from named receipts, not a global score."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'inventory': 'reports/audit_foundation_v1/accepted_reference_20261008/CONTROL_INVENTORY.json',
    'precision': 'reports/audit_precision_v1/VERIFICATION.json',
    'criterion_metrics': 'reports/audit_precision_v1/METRICS_BY_CRITERION.md',
    'replay': 'reports/audit_replay_v1/VERIFICATION.json',
    'service': 'reports/audit_service_v1/RECEIPT.json',
    'ux': 'reports/audit_quality_gate_v1/VERIFICATION.json',
    'claims': '07_Business/03_Market/TDL_GTFS_NETEX_CLAIMS_REGISTER_20261009_REVIEW.json',
    'value': '07_Business/03_Market/AUDIT_VALUE_EVIDENCE_REGISTER_V1.json',
    'backlog': 'reports/TDL_AUDIT_IMPROVEMENT_BACKLOG_V1.md',
}


def build():
    for path in SOURCES.values():
        if not (ROOT/path).is_file():
            raise ValueError('Missing named source: '+path)
    data = {k: json.loads((ROOT/p).read_text(encoding='utf-8')) for k,p in SOURCES.items() if p.endswith('.json')}
    text = (ROOT/SOURCES['backlog']).read_text(encoding='utf-8')
    # Only the progress table, never old counts embedded in sealed receipts.
    progress = text.split('| ID | Estado vigente |')[1]
    states = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r'^\| TDL-AUD-(\d+) \| ([^|]+) \|', progress, re.M)}
    if not set(states).issubset(range(1,25)):
        raise ValueError('Unknown task ID')
    tasks = [{'id': f'TDL-AUD-{i:02}', 'state': states.get(i,'PENDIENTE')} for i in range(1,25)]
    metrics=[]
    def add(id, value, unit, denominator, source, scope, status='DOCUMENTED'):
        metrics.append({'id':id,'value':value,'unit':unit,'denominator':denominator,'measurement_state':status,
                        'source':SOURCES[source], 'scope':scope})
    inv=data['inventory'];p=data['precision'];r=data['replay'];v=data['value']
    if sum(p['counts'].values()) != p['cases']:
        raise ValueError('Reference categories do not reconcile')
    if r['executed_current_rule_scenarios']+r['unimplemented_candidates_preserved'] != r['replay_scenarios']:
        raise ValueError('Replay scope does not reconcile')
    if sum(r['ledger_states'].values()) != r['ledger_cases']:
        raise ValueError('Correction states do not reconcile')
    add('gtfs_controls',len(inv['GTFS']),'controles inventariados',None,'inventory','GTFS Lab; no total de requisitos GTFS')
    add('netex_entries',len(inv['NETEX']),'entradas inventariadas',None,'inventory','NeTEx Lab; Compliance NeTEx separado; no equivalencia con controles GTFS')
    for fmt in ('GTFS','NETEX'):
        add('coverage_total_'+fmt.lower(),None,'proporción de requisitos cubiertos',None,'inventory',fmt+'; universo de requisitos aplicables no fijado','NOT_MEASURED')
    for name,count in p['counts'].items():
        add('reference_'+name.lower(),count,'escenarios de esta categoría',p['cases'],'precision','Banco sintético; categorías no son una tasa global de precisión')
    add('replay_equivalence',r['semantic_equivalent'],'escenarios semánticamente equivalentes',r['replay_scenarios'],'replay','108 ejecutados + 6 no implementados preservados; mismo host, no clean-machine')
    add('external_gtfs_reports',p['external_reports_verified'],'informes de contraste',96,'precision','MobilityData GTFS, 1 caso con excepciones secundarias; no comparador NeTEx')
    add('external_system_error_cases',len(p['external_system_error_cases']),'casos con excepción secundaria',96,'precision','GTFS; IDs conservados en fuente, sin ocultar errores')
    for name,count in r['ledger_states'].items():
        add('correction_'+name.lower(),count,'casos',r['ledger_cases'],'replay','Seis casos sintéticos de 17; 21 reutiliza los mismos, no sumarlos de nuevo')
    add('service_journeys',len(data['service']['journeys']),'recorridos internos',2,'service','Uno por formato; respuestas y aceptación simuladas')
    add('human_independent_review',None,'revisiones independientes',None,'service','No consta revisor humano independiente; no indicador de calidad validado','NOT_MEASURED')
    add('ux_success',None,'participantes con éxito',None,'ux','Sin sesiones; objetivo 4/5 por perfil no alcanzado ni medido','NOT_MEASURED')
    add('claims_internal',data['claims']['claims'],'frases registradas',None,'claims','Uso externo NO; no capacidades de mercado validadas')
    add('primary_value_records',len(v['records']),'registros primarios autorizados',None,'value','Registro vacío; no es tamaño del mercado')
    for name,value in v['results'].items():
        add('commercial_'+name,value,'resultado específico de la dimensión',None,'value','Sin evidencia primaria autorizada; diseño no valida negocio',v['measurement_state'])
    if any(m['value'] is not None for m in metrics if m['measurement_state']=='NOT_MEASURED'):
        raise ValueError('Unmeasured result must be null')
    return {'contract':'TDL_AUDIT_QUALITY_DASHBOARD/1','generated_at_utc':datetime.now(timezone.utc).isoformat(),
            'sources_as_of':'2026-10-09; fechas históricas de cada recibo preservadas',
            'metrics':metrics,'tasks':tasks,'backlog_completed':sum(t['state'].startswith('COMPLETADA') for t in tasks),
            'backlog_total':24,'global_quality_score':None,'sources':SOURCES,
            'interpretation':'Snapshot documental, no rerun de motores ni certificación de vigencia. No agregar formatos/casos/porcentajes de distinto universo.'}


def generate(output):
    output=Path(output).resolve()
    if not output.is_relative_to((ROOT/'reports/audit_quality_management_v1').resolve()) or output.exists():
        raise ValueError('Use new named snapshot under reports/audit_quality_management_v1')
    model=build();output.mkdir(parents=True)
    (output/'DASHBOARD.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Cuadro de gestión — TDL-AUD-24','',model['interpretation'],'',
           f"Backlog: {model['backlog_completed']}/24 completadas en sus alcances. No es porcentaje de calidad.", '',
           '| Indicador | Valor | Unidad | Denominador | Estado / alcance | Evidencia |','|---|---|---|---|---|---|']
    for m in model['metrics']:
        value='NO MEDIDO' if m['value'] is None else str(m['value'])
        denom='NO DETERMINADO' if m['denominator'] is None else str(m['denominator'])
        lines.append(f"| {m['id']} | {value} | {m['unit']} | {denom} | {m['measurement_state']}: {m['scope']} | [Fuente](../../../{m['source']}) |")
    lines += ['', 'Métricas de precisión por criterio, con sus propios denominadores: [tabla](../../../'+SOURCES['criterion_metrics']+').', '',
              '| Tarea | Estado vigente |','|---|---|']
    lines += [f"| {t['id']} | {t['state']} |" for t in model['tasks']]
    (output/'DASHBOARD.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return model


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();m=generate(args.output)
    print(json.dumps({'result':'PASS_DOCUMENTARY_SNAPSHOT','metrics':len(m['metrics']),'tasks':len(m['tasks']),'completed':m['backlog_completed']}))
