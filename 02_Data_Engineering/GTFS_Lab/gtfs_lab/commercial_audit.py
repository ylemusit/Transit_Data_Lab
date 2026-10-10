"""Add an evidence-bound transport report and offline QGIS atlas to a sealed R3.

This is a presentation workflow, not a new audit or a legal compliance engine.
No source, frozen engine or existing delivery is modified.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import re
import shutil
import subprocess
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from .commercial_content import CATALOGUE_TRANSLATIONS, DISPOSITIONS, LEGAL, LEGACY_RULES, RULES, STATUS
from .professional_audit import digest, read, verify_package, write


def load_tables(source):
    names = ('routes', 'trips', 'stops', 'stop_times', 'shapes', 'frequencies')
    with zipfile.ZipFile(source) as z:
        return {n: list(csv.DictReader(io.StringIO(z.read(n + '.txt').decode('utf-8-sig')))) for n in names}


def load_legal_context(path, project_root):
    """Verify captured legal context without promoting it to a legal verdict."""
    document = read(Path(path))
    if document.get('contract') != 'TDL_LEGAL_CONTEXT_UPDATE/1' or document.get('legal_conclusion_allowed') is not False:
        raise ValueError('Invalid legal context boundary')
    sources = document.get('sources', [])
    identities = [r['source_id'] for r in sources]
    required = {'ES-RD-450-2026', 'ES-RD-662-2012', 'ES-LAW-37-2007',
                'ES-LAW-18-2015', 'EU-GDPR', 'EU-INSPIRE', 'EU-OPEN-DATA'}
    if len(set(identities)) != len(identities) or not required.issubset(identities):
        raise ValueError('Incomplete legal context identities')
    root = Path(project_root).resolve()
    for row in sources:
        if row.get('capture_status') not in {'CAPTURED_BOE_ORIGINAL_AND_ANALYSIS', 'CAPTURED_OPERATIONAL_DOCUMENT'}:
            raise ValueError('Uncaptured legal context source')
    captures = sources + document.get('frozen_sources', []) + [
        r['consolidated_capture'] for r in sources if 'consolidated_capture' in r]
    for capture in captures:
        relative = Path(capture.get('local_path', capture.get('path', '')))
        if not str(relative) or relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Invalid legal context path')
        target = (root / relative).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError('Legal context capture unavailable')
        if digest(target) != capture.get('sha256'):
            raise ValueError('Legal context source hash mismatch')
    return document


def row_for(tables, occurrence):
    """R3 normalized locators are one-based DATA rows, including G03 ROW:n."""
    match = re.fullmatch(r'(\w+)\.txt:(?:data_row|ROW):(\d+)', occurrence['normalized_locator'])
    if not match:
        raise ValueError('Unsupported normalized locator: ' + occurrence['normalized_locator'])
    table, number = match[1], int(match[2])
    if number < 1 or number > len(tables[table]):
        raise ValueError('Locator outside source table')
    return table, number, tables[table][number - 1]


def feature(geometry, properties):
    return dict(type='Feature', geometry=geometry, properties=properties)


def load_catalogue(path):
    document=read(Path(path))
    if not isinstance(document,dict) or 'requirements' not in document:
        raise ValueError('Use the final Compliance V1 dispositions catalogue, not an earlier reconciliation')
    rows=document['requirements']
    expected=dict(PARTIAL=6,HUMAN_REVIEW_REQUIRED=12,DEFERRED=20,OUT_OF_SCOPE_V1=10)
    if dict(Counter(r['disposition'] for r in rows))!=expected or len({r['requirement_id'] for r in rows})!=48:
        raise ValueError('Review changed final catalogue before generation')
    if any(not r.get('description') for r in rows):raise ValueError('Requirement descriptions are required')
    return rows


def point(row):
    lon, lat = float(row['shape_pt_lon']), float(row['shape_pt_lat'])
    if not math.isfinite(lon) or not math.isfinite(lat) or not -180 <= lon <= 180 or not -90 <= lat <= 90:
        raise ValueError('Invalid coordinate')
    return [lon, lat]


def prepare_atlas(model, tables):
    routes = {r['route_id']: r for r in tables['routes']}
    trips = {r['trip_id']: r for r in tables['trips']}
    shape_routes, stop_routes = defaultdict(set), defaultdict(set)
    for trip in trips.values():
        if trip['shape_id'].strip():
            shape_routes[trip['shape_id']].add(trip['route_id'])
    for stop in tables['stop_times']:
        if stop['trip_id'] in trips:
            stop_routes[stop['stop_id']].add(trips[stop['trip_id']]['route_id'])
    shape_rows = defaultdict(list)
    for n, row in enumerate(tables['shapes'], 1):
        shape_rows[row['shape_id']].append((int(row['shape_pt_sequence']), n, row))
    previous = {}
    lines = []
    for sid, values in sorted(shape_rows.items()):
        values.sort()
        if len({v[0] for v in values}) != len(values):
            raise ValueError('Ambiguous shape sequence')
        for before, after in zip(values, values[1:]):
            previous[after[1]] = before
        coords = [point(v[2]) for v in values]
        if len(coords) < 2:
            raise ValueError('Shape cannot be rendered as line')
        for rid in sorted(shape_routes[sid]) or ['']:
            if rid and rid not in routes:
                raise ValueError('Shape refers to unknown route')
            lines.append(feature(dict(type='LineString', coordinates=coords), dict(route_id=rid, shape_id=sid)))
    events, case_details, seen = [], [], set()
    route_cases = defaultdict(Counter)
    for case in model['cases']:
        rows, affected, unmapped = [], set(), 0
        for occurrence in case['occurrences']:
            key = (case['case_id'], occurrence['normalized_locator'])
            if key in seen:
                continue
            seen.add(key)
            table, n, row = row_for(tables, occurrence)
            related = set()
            if table == 'routes': related = {row['route_id']}
            elif table == 'trips': related = {row['route_id']}
            elif table == 'frequencies': related = {trips[row['trip_id']]['route_id']} if row['trip_id'] in trips else set()
            elif table == 'stops': related = stop_routes[row['stop_id']]
            elif table == 'shapes': related = shape_routes[row['shape_id']]
            if related - set(routes): raise ValueError('Unknown affected route')
            affected.update(related)
            if not related: unmapped += 1
            for rid in related: route_cases[rid][case['case_id']] += 1
            item = dict(locator=occurrence['normalized_locator'], data_row=n, table=table, values=row,
                        route_ids=sorted(related), source_record_id=occurrence['source_record_id'])
            if table == 'shapes':
                if n not in previous: raise ValueError('Distance finding has no preceding vertex')
                before = previous[n]
                item['previous'] = dict(data_row=before[1], values=before[2])
                a, b = point(before[2]), point(row)
                if float(before[2]['shape_dist_traveled']) != float(row['shape_dist_traveled']):
                    raise ValueError('Source no longer demonstrates repeated distance')
                equal = a == b
                if equal != (case['case_id'] == 'PAL-G07-DUP'):
                    raise ValueError('Source geometry disagrees with case classification')
                item['coordinate_pair_equal'] = equal
                for rid in sorted(related) or ['']:
                    events.append(feature(dict(type='Point', coordinates=b),
                                          dict(route_id=rid, shape_id=row['shape_id'], case_id=case['case_id'],
                                               data_row=n, previous_row=before[1], distance=row['shape_dist_traveled'])))
            rows.append(item)
        if len(rows) != case['reconciled_event_count']:
            raise ValueError('Case event accounting changed')
        example = rows[0]
        if case['case_id'] == 'PAL-G07-EQUAL':
            # Largest coordinate separation makes the pattern visible; not a risk ranking.
            example = max(rows, key=lambda r: sum((a-b)**2 for a,b in zip(point(r['values']), point(r['previous']['values']))))
        case_details.append(dict(case_id=case['case_id'], route_ids=sorted(affected),
                                 event_count=len(rows), events_without_route=unmapped, example=example, events=rows))
    atlas_routes = []
    spatial_routes = {f['properties']['route_id'] for f in events if f['properties']['route_id']}
    for rid in sorted(spatial_routes):
        route = routes[rid]
        atlas_routes.append(dict(route_id=rid, label=route.get('route_short_name') or rid,
                                 name=route.get('route_long_name', ''), cases=dict(route_cases[rid]),
                                 image=f'mapas/{rid}.png'))
    unassigned = defaultdict(Counter)
    for event in events:
        props=event['properties']
        if not props['route_id']: unassigned[props['shape_id']][props['case_id']]+=1
    unassigned_shapes=[dict(shape_id=sid,cases=dict(counts),image=f'mapas/sin_viaje_{sid}.png') for sid,counts in sorted(unassigned.items())]
    return dict(routes=atlas_routes, unassigned_shapes=unassigned_shapes, case_details=case_details,
                lines=dict(type='FeatureCollection', features=lines),
                points=dict(type='FeatureCollection', features=events),
                route_count=len(routes), shape_count=len(shape_rows),
                note='Un evento se cuenta una vez por caso; puede relacionarse con varias líneas. No sumar líneas para obtener eventos únicos.')


def validation_matrix(model, compliance, source_matrix=None):
    result = []
    for rule in model['matrix']:
        key = rule['rule_id'].split('-', 2)[2]
        if key not in RULES: raise ValueError('Missing client explanation: ' + key)
        title, analysis = RULES[key]
        cases = [c for c in model['cases'] if rule['rule_id'] in {o['rule_id'] for o in c['occurrences']}]
        status = rule['status']
        action = (' '.join(c['action'] for c in cases) if cases else
                  'Revisar el registro técnico, documentar la causa que impide evaluar y repetir esta comprobación con evidencia suficiente.' if status == 'NOT_EVALUABLE' else
                  'Confirmar la condición de aplicación al definir el destino y reevaluar si cambia el contenido.' if status == 'NOT_APPLICABLE' else
                  'Conservar el resultado y repetir el control en la siguiente versión de los datos.')
        if key.startswith('FEED-') and key.endswith('-DECLARED'):
            action = 'Acordar e incorporar la fecha o versión de publicación correspondiente, si procede para el destino. Repetir el control; no se presenta la ausencia como infracción legal.'
        coverage=rule['coverage']
        if coverage and 'evaluated' in coverage:
            coverage_text=(f"Controles evaluados: {coverage['evaluated']}; no aplicables: {coverage['not_applicable']}; "
                           f"no evaluables: {coverage['not_evaluable']}. Estos denominadores pueden contar controles, no entidades únicas.")
        elif coverage and coverage.get('presence')=='ABSENT':
            coverage_text='Dato recomendado ausente; no se ha comprobado un valor de ese campo.'
        else:
            coverage_text='La matriz no declara un denominador numérico de cobertura.'
        result.append(dict(rule_id=rule['rule_id'], title=title, analysis=analysis,
                           check=f"Resultado registrado en RUN02. Hallazgos: {rule['finding_count']}. " +
                                 coverage_text,
                           validation=STATUS.get(status, status), status=status,
                           assessment='Resultado limitado al criterio implantado; no acredita exactitud del servicio real ni cumplimiento legal.',
                           solution=action, case_ids=[c['case_id'] for c in cases],
                           legal_mapping='NO_DIRECT_LEGAL_MAPPING_DOCUMENTED',
                           source='03_SOURCE_DELIVERY/engine_run/engine_report.json',
                           technical_reference=rule['specification_reference'], raw=rule))
    if compliance.get('legal_conclusion_allowed') is not False:
        raise ValueError('Unsupported Compliance legal boundary')
    result.append(dict(rule_id=compliance['rule_id'], title='Relaciones de paradas fijas y viajes',
                       analysis='Control acotado de que las referencias inspeccionadas resuelven a viajes y paradas/plataformas.',
                       check='Evidencia: compliance.json; motivo: ' + compliance['reason'],
                       validation=STATUS.get(compliance['result'], compliance['result']), status=compliance['result'],
                       assessment='La prueba aporta evidencia técnica parcial al requisito europeo A04-P01-001. No permite conclusión legal.',
                       solution='Conservar esta evidencia y completar el expediente documental de UE-01.',
                       case_ids=[], legal_mapping='DOCUMENTED_PARTIAL', source='03_SOURCE_DELIVERY/compliance.json'))
    if source_matrix is not None:
        for rule in source_matrix:
            if rule['stage']!='LEGACY' or rule['rule_id']==compliance['rule_id']:continue
            rid=rule['rule_id']
            if rid not in LEGACY_RULES:raise ValueError('Missing legacy client explanation: '+rid)
            title,analysis=LEGACY_RULES[rid]
            cases=[c for c in model['cases'] if rid in {o['rule_id'] for o in c['occurrences']}]
            result.append(dict(rule_id=rid,title=title,analysis=analysis,
                               check='Resultado registrado por el comprobador anterior. Hallazgos: '+str(rule['finding_count'])+'. No se declara un denominador de cobertura en esta matriz.',
                               validation=STATUS.get(rule['result'],rule['result']),status=rule['result'],
                               assessment='Resultado técnico en su alcance; no hay correspondencia legal directa documentada. La aplicabilidad detallada no viene declarada en la matriz fuente.',
                               solution=' '.join(c['action'] for c in cases) if cases else 'Conservar el resultado y repetir el control en la siguiente versión de los datos.',
                               case_ids=[c['case_id'] for c in cases],legal_mapping='NO_DIRECT_LEGAL_MAPPING_DOCUMENTED',
                               source='03_SOURCE_DELIVERY/report/client_report.json#validation_matrix',raw=rule))
        source_ids={r['rule_id'] for r in source_matrix}
        if source_ids!={r['rule_id'] for r in result}:raise ValueError('Commercial matrix omits or adds a source validation')
        if len(result)!=len({r['rule_id'] for r in result}):raise ValueError('Duplicate commercial validation')
        for row in result:
            source_rows=[r for r in source_matrix if r['rule_id']==row['rule_id']]
            if any(r['result']!=row['status'] for r in source_rows):raise ValueError('Source validation status mismatch')
            row['source_matrix_row_count']=len(source_rows)
    return result
    return result


def report(output, model, atlas, checks, requirements):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether
    from reportlab.platypus.tableofcontents import TableOfContents
    results = output / '01_RESULTADOS'
    styles = dict(body=ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14, spaceAfter=8),
                  title=ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=25, leading=29, textColor=colors.HexColor('#143747'), spaceAfter=15),
                  h=ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#143747'), spaceAfter=10),
                  small=ParagraphStyle('small', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=6),
                  map=ParagraphStyle('map', fontName='Helvetica', fontSize=8.5, leading=11, spaceAfter=3))
    story = []
    def p(text, style='body'): return Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])
    def add(text, style='body'): story.append(p(text, style))
    def field(label, text):
        story.append(Paragraph('<b>'+escape(label)+':</b> '+escape(str(text)), styles['body']))
    def page(title):
        if story: story.append(PageBreak())
        add(title, 'h')
    def source_note():
        add('Fuente: fichero recibido y ejecución RUN02. Las conclusiones se limitan al alcance comprobado.', 'small')
    add('TRANSIT DATA LAB', 'small')
    add('Calidad de la información\ndel servicio de transporte', 'title')
    add('Palma | Informe para dirección y responsables de explotación', 'h')
    add('Revisión comercial R4 · 8 de octubre de 2026', 'body')
    add('Se han identificado seis tipos de incidencia que requieren corrección o revisión con el productor de los datos. Todavía no se ha verificado una versión corregida ni se ha determinado la aptitud para un destino concreto.')
    field('Qué aporta este informe', 'Explica qué sucede, a qué líneas se relaciona, qué puede significar para la información del servicio y qué debe hacerse para cerrar cada caso.')
    cover=model['coverage']
    event_count=format(cover['reconciled_event_count'],',').replace(',','.')
    record_count=format(cover['source_record_count'],',').replace(',','.')
    field('Dimensión de la revisión', f"{atlas['route_count']} líneas declaradas; {atlas['shape_count']} trazados. {event_count} eventos únicos documentados en {record_count} registros; {cover['duplicate_source_reference_count']} referencias repetidas entre comprobadores.")
    field('Lectura recomendada', 'Decisiones y seis fichas de actuación primero; después, atlas de líneas y anexos de comprobaciones y cobertura normativa.')
    field('Estado', 'Preparado para revisión del responsable. Sin emisión ni envío al cliente. El informe técnico R3 se conserva sin cambios en esta entrega.')
    add('Identificación: '+model['identity']['client_audit_id']+' / '+model['identity']['audit_execution_id'], 'small')
    add('Huella de la fuente: '+model['identity']['source_sha256'], 'small')
    page('Guía de lectura')
    add('El cuerpo principal explica las actuaciones. El atlas localiza las incidencias cartográficas. Los anexos documentan las comprobaciones y las evidencias normativas pendientes. El índice y los marcadores permiten ir directamente a cada apartado.')
    toc=TableOfContents()
    toc.levelStyles=[ParagraphStyle('toc',fontName='Helvetica',fontSize=10,leading=14,spaceBefore=8,leftIndent=0,firstLineIndent=0)]
    story.append(toc)
    page('Decisiones y secuencia de trabajo')
    for s in model['presentation']['steps']:
        field(str(s['order']) + '. Actuación', s['action'])
        field('Motivo', s['basis']); field('Información necesaria', s['missing'])
    field('Responsables', 'El productor corrige los datos; explotación valida horarios y servicio; cartografía revisa los trazados; el responsable de publicación confirma destino y obligaciones; auditoría verifica el cierre con una nueva ejecución comparable.')
    field('Prioridad', 'La secuencia organiza el trabajo. No se asigna urgencia ni perjuicio al viajero sin datos de uso e impacto.')
    page('Cómo interpretar resultados y mapas')
    add('Una línea es el servicio identificado para el viajero. Un viaje es un recorrido programado. Un trazado es la secuencia de puntos utilizada para dibujarlo; una línea puede tener varios trazados y un trazado puede servir a varios viajes.')
    add('Los planos relacionan trazados, viajes y líneas mediante los identificadores del fichero. No se deduce una línea por el nombre del trazado. Los puntos muestran incidencias cartográficas; no representan cancelaciones ni interrupciones del servicio.')
    add('Azul: itinerarios de la línea. Rojo: puntos coincidentes con distancia repetida. Naranja: puntos distintos con la misma distancia. Gris: resto de la red como contexto. Norte arriba. No se ha utilizado cartografía externa para verificar el recorrido real.')
    add('El atlas incluye todas las líneas vinculadas a los dos casos cartográficos. Se presentan tres mapas por página A4. Las escalas varían y se indican en cada imagen; las incidencias próximas pueden superponerse. Los ejemplos ampliados muestran el defecto que una vista general no permite distinguir.')
    add('Colores, referencias vacías y límites horarios se explican con valores concretos. Dibujarlos no demostraría el fallo, por lo que esas fichas indican expresamente que no necesitan mapa.')
    add('Los anexos recogen también resultados sin incidencias, no aplicables y no evaluables. Una recomendación ausente y una falta de evidencia nunca se convierten en conformidad.')
    for case, detail in zip(model['cases'], atlas['case_details']):
        page(case['title'])
        add(case['case_id']+' | '+str(detail['event_count'])+' eventos únicos | '+str(len(detail['route_ids']))+' líneas relacionadas', 'small')
        field('Análisis', case['observation'])
        field('Criterio y comprobación', case['criterion'])
        field('Valoración', case['impact_known'])
        field('Solución', case['action'])
        field('Cómo validar y cerrar', case['closure_criteria'])
        ex = detail['example']; row = ex['values']
        label = ', '.join(ex['route_ids']) or 'Sin correspondencia de línea acreditada'
        field('Ejemplo de la fuente', ex['locator']+'; línea(s): '+label)
        if ex['table'] == 'routes': text = 'El color del texto contiene un espacio: '+repr(row['route_text_color'])+'. Un espacio no equivale a un campo vacío.'
        elif ex['table'] == 'stops': text = 'Parada '+row['stop_id']+' ('+row['stop_name']+'). Estación principal: '+repr(row['parent_station'])+'. Confirmar si procede una jerarquía antes de corregir.'
        elif ex['table'] == 'trips': text = 'Viaje '+row['trip_id']+'; referencia de trazado: '+repr(row['shape_id'])+'. No puede dibujarse el trazado pretendido a partir de esa referencia.'
        elif ex['table'] == 'frequencies':
            def seconds(value):
                h,m,s=map(int,value.split(':'));return h*3600+m*60+s
            def clock(value):return f'{value//3600:02d}:{value%3600//60:02d}:{value%60:02d}'
            start,end,interval=seconds(row['start_time']),seconds(row['end_time']),int(row['headway_secs'])
            last=start+((end-start-1)//interval)*interval
            text = ('Viaje '+row['trip_id']+'; franja '+row['start_time']+' a '+row['end_time']+'; separación '+row['headway_secs']+
                    ' segundos. La sucesión matemática sitúa la última salida anterior al fin en '+clock(last)+
                    ' y la siguiente en '+clock(last+interval)+'. Si ese es el horario pretendido, el fin debe quedar estrictamente entre ambas; coincide con la segunda. Explotación debe confirmar las salidas deseadas antes de ajustar el intervalo.')
        else:
            before=ex['previous']['values']
            text = 'Trazado '+row['shape_id']+'; puntos '+before['shape_pt_sequence']+' y '+row['shape_pt_sequence']+'; distancia '+before['shape_dist_traveled']+' y '+row['shape_dist_traveled']+'. Las unidades de distancia deben confirmarse con el productor.'
        add(text)
        field('Mapa', 'Ejemplo ampliado en la siguiente página y localización por línea en el atlas.' if ex['table']=='shapes' else 'No necesario para demostrar este defecto. La evidencia es el valor o relación del fichero descrito arriba.')
        add('Líneas relacionadas: '+', '.join(detail['route_ids'])+'.', 'small')
        if detail['events_without_route']: add(str(detail['events_without_route'])+' eventos sin correspondencia de línea acreditada.', 'small')
        if ex['table']=='shapes':
            page('Ejemplo cartográfico · '+case['case_id'])
            story.append(Image(str(results/'mapas'/('ejemplo_'+case['case_id']+'.png')), width=495, height=335))
            add(text)
            before=ex['previous']['values']
            field('Comprobación numérica', 'Coordenadas anterior: '+str(point(before))+'; actual: '+str(point(row))+'. La distancia acumulada permanece igual. Unidades de las coordenadas: grados; orden longitud, latitud.')
            field('Qué se aprecia', 'Los dos vértices ocupan la misma posición. El marcador representa ambos; la tabla numérica demuestra la repetición.' if ex['coordinate_pair_equal'] else 'Hay desplazamiento entre los vértices, aunque el dato de distancia no avanza. No se atribuye la causa a redondeo sin evidencia.')
            field('Selección del ejemplo', 'Primera ocurrencia documentada del caso.' if ex['coordinate_pair_equal'] else 'Mayor separación de coordenadas del caso, para hacer visible el patrón. No es una clasificación de gravedad.')
            field('Solución y cierre', case['action'])
            source_note()
    for offset in range(0, len(atlas['routes']), 3):
        page('Atlas · líneas con incidencias cartográficas')
        for route in atlas['routes'][offset:offset+3]:
            spatial = {k:v for k,v in route['cases'].items() if k.startswith('PAL-G07')}
            block=[p('Línea '+route['label']+' · '+route['name'], 'map'),
                   Image(str(results/route['image']), width=495, height=170),
                   p('Referencia '+route['route_id']+' | Coincidentes: '+str(spatial.get('PAL-G07-DUP',0))+' | Distintos con igual distancia: '+str(spatial.get('PAL-G07-EQUAL',0)), 'map')]
            story.append(KeepTogether(block)); story.append(Spacer(1,7))
        add('Fuente: GTFS recibido. Las cifras son eventos relacionados con cada línea; no viajeros ni expediciones canceladas.', 'small')
    for offset in range(0,len(atlas['unassigned_shapes']),3):
        page('Atlas · trazados sin vínculo con viajes')
        for item in atlas['unassigned_shapes'][offset:offset+3]:
            block=[p('Trazado '+item['shape_id']+' · línea no determinada','map'),
                   Image(str(results/item['image']),width=495,height=170),
                   p('Coincidentes: '+str(item['cases'].get('PAL-G07-DUP',0))+' | Distintos con igual distancia: '+str(item['cases'].get('PAL-G07-EQUAL',0)),'map')]
            story.append(KeepTogether(block));story.append(Spacer(1,7))
        add('Análisis: el trazado existe, pero ningún viaje lo referencia en la fuente. No se puede asignar a una línea con evidencia suficiente. Solución: el productor debe confirmar si es material residual o aportar la relación prevista; auditoría comprobará esa correspondencia y el cierre cartográfico.', 'small')
    page('Anexo · todas las comprobaciones de la ejecución')
    add('Se presentan las 24 reglas del motor, las siete del comprobador anterior y el control acotado de Compliance: 32 controles distintos. La matriz fuente tiene 33 filas porque Compliance aparece en dos proyecciones del mismo resultado. Los 12 registros del comprobador anterior sobre referencias de trazado se reconcilian con el caso PAL-G04-SHAPE; no son 12 fallos adicionales.')
    add('No hay una correspondencia legal directa documentada para cada regla GTFS. GTFS es una especificación técnica; una obligación contractual de usarla debe acreditarse. La única vinculación legal documentada aquí es parcial y corresponde al control V1-RULE-GTFS.')
    for n, check in enumerate(checks):
        if n % 3 == 0: page('Comprobaciones · '+str(n+1)+' a '+str(min(n+3,len(checks))))
        block=[p(check['title'],'h'),p(check['rule_id'],'small')]
        for label,key in [('Análisis','analysis'),('Comprobación','check'),('Validación','validation'),('Valoración','assessment'),('Solución / seguimiento','solution')]:
            block.append(Paragraph('<b>'+label+':</b> '+escape(check[key]), styles['small']))
        block.append(p('Vínculo legal: '+('parcial documentado; ver UE-01.' if check['legal_mapping']=='DOCUMENTED_PARTIAL' else 'no documentado para esta regla; no permite emitir dictamen legal.'),'small'))
        block.append(p('Evidencia: '+check['source'],'small'))
        story.append(KeepTogether(block)); story.append(Spacer(1,18))
    page('Anexo · alcance normativo y evidencias pendientes')
    add('La revisión identifica referencias europeas, estatales y autonómicas relacionadas con la información del transporte. El catálogo del programa no cubre de forma completa estas obligaciones. No se emite una declaración global de cumplimiento ni un inventario jurídico exhaustivo.')
    add('Las fuentes oficiales se consultaron el 08/10/2026. Los textos consolidados sirven para consulta; la aplicabilidad debe documentarse para el operador, contrato, servicio, tipo de dato y fecha relevantes. Las referencias nuevas no se incorporan como reglas aprobadas al motor congelado.')
    for entry in LEGAL:
        page(entry['level']+' · '+entry['title'])
        add(entry['id']+' | '+entry['source'],'small')
        for label,key in [('Análisis','analysis'),('Comprobación disponible','check'),('Validación','validation'),('Valoración','assessment'),('Solución y evidencia para cerrar','solution')]: field(label,entry[key])
        if entry['url']: story.append(Paragraph('<link href="'+escape(entry['url'])+'" color="#176B87">Fuente oficial consultada</link>',styles['body']))
        field('Autoridad de las fuentes', ', '.join(entry['authority_types']))
        add('Revisión contextual completada a '+entry['as_of']+'. Aplicabilidad al conjunto: NO DETERMINADA por la evidencia disponible.', 'small')
        add('Resultado normativo: PENDIENTE DE DETERMINAR. Este estado no declara un incumplimiento probado.', 'small')
    counts=Counter(r['disposition'] for r in requirements)
    page('Catálogo europeo · cobertura y plan de cierre')
    add('Los siguientes 48 registros describen la cobertura del catálogo interno, no 48 pruebas ejecutadas sobre el fichero de Palma. Se conservan sus identificadores y motivos para que no queden obligaciones ocultas bajo un resultado global.')
    for key,count in sorted(counts.items()): field(DISPOSITIONS.get(key,key),str(count))
    add('Ningún requisito figura con cobertura completa. En cada ficha, el motivo explica la falta de evidencia; la condición de reapertura concreta el siguiente trabajo. El expediente deberá añadir responsable nominal y fecha acordada.')
    add('Fuera del alcance de V1 significa que el producto no realiza esa comprobación; no excluye la obligación jurídica del operador o de la administración.', 'small')
    for offset in range(0,len(requirements),3):
        page('Catálogo europeo · requisitos '+str(offset+1)+' a '+str(min(offset+3,len(requirements))))
        for req in requirements[offset:offset+3]:
            block=[p(req['description'],'body'),p(req['requirement_id'],'small'),p(DISPOSITIONS.get(req['disposition'],req['disposition']),'small')]
            for label,value in [('Análisis y comprobación pendiente',req['reason']),('Validación','Cobertura del catálogo; no hay un resultado específico del fichero para esta obligación.'),('Valoración',req['impact']),('Solución / evidencia requerida',req['reopen_condition'])]:
                block.append(Paragraph('<b>'+label+':</b> '+escape(CATALOGUE_TRANSLATIONS.get(value,value)),styles['small']))
            story.append(KeepTogether(block));story.append(Spacer(1,12))
    page('Condiciones de aceptación y siguiente entrega')
    for text in ['Confirmar destino, consumidor de los datos y condiciones de uso con el responsable del servicio.',
                 'Recibir correcciones del productor y los horarios, jerarquías y trazados que se pretendían publicar.',
                 'Repetir la auditoría sobre la nueva fuente y comprobar cada criterio de cierre; documentar también efectos secundarios.',
                 'Completar el expediente normativo con obligaciones aplicables, evidencias y decisiones justificadas.',
                 'Revisar los mapas y la comprensión del informe con el responsable antes de emitirlo.']:
        add(text)
    add('El informe técnico preservado, la matriz detallada, las correspondencias de líneas y el proyecto QGIS acompañan este documento. El proyecto y sus capas son locales; no se ha enviado el fichero a servicios de mapas.')
    def footer(canvas, doc):
        canvas.setStrokeColor(colors.HexColor('#C4D3D8'));canvas.line(48,40,A4[0]-48,40)
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#455E69'))
        canvas.drawString(48,27,'TDL | Palma | RUN02 · R4 | Revisión previa a emisión')
        canvas.drawRightString(A4[0]-48,27,str(doc.page))
    toc_titles={'Decisiones y secuencia de trabajo','Cómo interpretar resultados y mapas',
                'Atlas · líneas con incidencias cartográficas','Atlas · trazados sin vínculo con viajes',
                'Anexo · todas las comprobaciones de la ejecución','Anexo · alcance normativo y evidencias pendientes',
                'Catálogo europeo · cobertura y plan de cierre','Condiciones de aceptación y siguiente entrega'}|{c['title'] for c in model['cases']}
    class TransportDoc(SimpleDocTemplate):
        def beforeDocument(self):self.toc_seen=set();self.heading_number=0
        def afterFlowable(self, flowable):
            if isinstance(flowable,Paragraph) and flowable.style.name=='h':
                text=flowable.getPlainText();self.heading_number+=1;key='section_'+str(self.heading_number)
                self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,0,False)
                if text in toc_titles and text not in self.toc_seen:
                    self.toc_seen.add(text);self.notify('TOCEntry',(0,text,self.page,key))
    doc=TransportDoc(str(results/'Informe_comercial_transporte.pdf'),pagesize=A4,
                          leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=54,
                          title='Palma - Calidad de la información del transporte',author='Transit Data Lab')
    doc.multiBuild(story,onFirstPage=footer,onLaterPages=footer)


def generate(package, source, output, catalogue, qgis_python):
    package, source, output, catalogue = map(Path, (package, source, output, catalogue))
    if output.exists(): raise ValueError('Output must be new; historical deliveries are immutable')
    if output.resolve().is_relative_to(package.resolve()): raise ValueError('Output cannot be inside source package')
    verified_count=verify_package(package)
    source_manifest_sha=digest(package/'02_EVIDENCIAS/PACKAGE_MANIFEST.json')
    model=read(package/'02_EVIDENCIAS/PRESENTATION_MODEL.json')
    expected={'PAL-G03-COLOR','PAL-G04-PARENT','PAL-G04-SHAPE','PAL-G06-FREQUENCY','PAL-G07-DUP','PAL-G07-EQUAL'}
    if {c['case_id'] for c in model['cases']}!=expected or model['coverage']['unclassified_record_count']:
        raise ValueError('This reviewed editorial template requires the six R3 cases with complete classification')
    if digest(source) != model['identity']['source_sha256']: raise ValueError('Wrong source ZIP')
    compliance=read(package/'03_SOURCE_DELIVERY/compliance.json')
    source_matrix=read(package/'03_SOURCE_DELIVERY/report/client_report.json')['validation_matrix']
    checks=validation_matrix(model,compliance,source_matrix)
    requirements=load_catalogue(catalogue)
    project_root=Path(__file__).resolve().parents[3]
    legal_context_path=project_root/'03_Compliance/reports/legal_update_20261008/source_registry.json'
    legal_context=load_legal_context(legal_context_path,project_root)
    atlas=prepare_atlas(model,load_tables(source))
    evidence=output/'02_EVIDENCIAS';results=output/'01_RESULTADOS'
    results.mkdir(parents=True);evidence.mkdir()
    write(evidence/'ATLAS_MODEL.json',atlas)
    write(evidence/'VALIDATIONS.json',checks)
    write(evidence/'REGULATORY_REVIEW.json',dict(as_of='2026-10-08', legal_conclusion_allowed=False, entries=LEGAL, catalogue=requirements))
    write(evidence/'LEGAL_CONTEXT_REGISTRY.json',legal_context)
    legal_sources=evidence/'legal_sources';legal_sources.mkdir()
    source_index=[]
    for row in legal_context['sources']+legal_context['frozen_sources']:
        relative=row.get('local_path',row.get('path'))
        target=legal_sources/Path(relative).name
        shutil.copy2(project_root/relative,target)
        source_index.append(dict(source_id=row.get('source_id',row.get('identity')),
                                 path=target.relative_to(output).as_posix(),sha256=row['sha256']))
        if 'consolidated_capture' in row:
            capture=row['consolidated_capture']
            target=legal_sources/Path(capture['local_path']).name
            shutil.copy2(project_root/capture['local_path'],target)
            source_index.append(dict(source_id=row['source_id'],version='CONSOLIDATED_INFORMATIONAL',
                                     path=target.relative_to(output).as_posix(),sha256=capture['sha256']))
    write(evidence/'LEGAL_SOURCE_INDEX.json',dict(sources=source_index))
    write(results/'gis/lineas.geojson',atlas['lines']);write(results/'gis/incidencias.geojson',atlas['points'])
    shutil.copy2(package/'01_RESULTADOS/Informe_auditoria.pdf',results/'Informe_tecnico_R3_preservado.pdf')
    shutil.copy2(package/'01_RESULTADOS/Plan_de_accion_y_hallazgos.xlsx',results/'Plan_de_accion_y_hallazgos_R3_preservado.xlsx')
    env=os.environ.copy();env['QT_QPA_PLATFORM']='offscreen';env['PYTHONIOENCODING']='utf-8'
    renderer=Path(__file__).resolve().parents[1]/'tools/qgis_audit_maps.py'
    process=subprocess.run([str(qgis_python),str(renderer),str(output)],env=env,check=False,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (evidence/'QGIS_PROCESS.log').write_text(process.stdout+'\n'+process.stderr,encoding='utf-8')
    if process.returncode: raise RuntimeError('QGIS failed; see QGIS_PROCESS.log')
    report(output,model,atlas,checks,requirements)
    if verify_package(package)!=verified_count or digest(package/'02_EVIDENCIAS/PACKAGE_MANIFEST.json')!=source_manifest_sha: raise ValueError('Source package changed')
    if digest(source)!=model['identity']['source_sha256']: raise ValueError('Source ZIP changed')
    if digest(results/'Informe_tecnico_R3_preservado.pdf')!=digest(package/'01_RESULTADOS/Informe_auditoria.pdf'): raise ValueError('Technical PDF not preserved')
    write(evidence/'GENERATION_RECEIPT.json',dict(identity=model['identity'],presentation_revision='COMMERCIAL-R4-20261008',
          source_package=str(package),source_package_verified_files=verified_count,source_manifest_sha256=source_manifest_sha,
          source_zip_sha256=digest(source),catalogue_path=str(catalogue),catalogue_sha256=digest(catalogue),
          source_client_report_sha256=digest(package/'03_SOURCE_DELIVERY/report/client_report.json'),
          route_maps=len(atlas['routes']),validation_count=len(checks),legal_catalogue_count=len(requirements),
          source_validation_matrix_rows=len(source_matrix),unassigned_shape_maps=len(atlas['unassigned_shapes']),
          source_package_unchanged=True,technical_pdf_unchanged=True,
          technical_workbook_unchanged=digest(results/'Plan_de_accion_y_hallazgos_R3_preservado.xlsx')==digest(package/'01_RESULTADOS/Plan_de_accion_y_hallazgos.xlsx'),engine_rerun=False,
          legal_conclusion_allowed=False,release_status='HUMAN_REVIEW_PENDING'))
    receipt=read(evidence/'GENERATION_RECEIPT.json')
    receipt.update(legal_context_registry_sha256=digest(legal_context_path),legal_context_verified=True,
                   legal_context_source_count=len(legal_context['sources']),
                   presentation_revision='COMMERCIAL-R4-LEGAL-UPDATE-20261008')
    write(evidence/'GENERATION_RECEIPT.json',receipt)
    seal(output)
    verify_supplement(output)
    return dict(output=str(output),maps=len(atlas['routes']),checks=len(checks),status='GENERATED_FOR_REVIEW')


def seal(output):
    output=Path(output)
    artifacts={p.relative_to(output).as_posix():dict(sha256=digest(p),size_bytes=p.stat().st_size)
               for p in sorted(output.rglob('*')) if p.is_file() and p.name not in {'SUPPLEMENT_MANIFEST.json','SUPPLEMENT_SEAL.json'}}
    write(output/'02_EVIDENCIAS/SUPPLEMENT_MANIFEST.json',dict(artifacts=artifacts))
    write(output/'02_EVIDENCIAS/SUPPLEMENT_SEAL.json',dict(manifest_sha256=digest(output/'02_EVIDENCIAS/SUPPLEMENT_MANIFEST.json')))


def verify_supplement(output):
    output=Path(output);evidence=output/'02_EVIDENCIAS'
    manifest=read(evidence/'SUPPLEMENT_MANIFEST.json')
    if digest(evidence/'SUPPLEMENT_MANIFEST.json')!=read(evidence/'SUPPLEMENT_SEAL.json')['manifest_sha256']:
        raise ValueError('Supplement seal mismatch')
    actual={p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file() and p.name not in {'SUPPLEMENT_MANIFEST.json','SUPPLEMENT_SEAL.json'}}
    if actual!=set(manifest['artifacts']):raise ValueError('Supplement inventory mismatch')
    from .professional_audit import contained
    for name,entry in manifest['artifacts'].items():
        path=contained(output,name)
        if digest(path)!=entry['sha256'] or path.stat().st_size!=entry['size_bytes']:raise ValueError('Supplement artifact mismatch: '+name)
    if read(evidence/'REGULATORY_REVIEW.json')['legal_conclusion_allowed'] is not False:
        raise ValueError('Unsupported legal conclusion')
    return len(actual)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('package','source','output','catalogue','qgis-python'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args()
    print(json.dumps(generate(args.package,args.source,args.output,args.catalogue,args.qgis_python),ensure_ascii=False))


if __name__=='__main__':main()
