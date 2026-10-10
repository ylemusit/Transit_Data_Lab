"""Notice-to-criterion attribution; no PASS inferred from missing notices."""
from pathlib import Path
import argparse
import json
from collections import Counter
from tools.audit_corpus_v1 import ROOT, read, write, sha

MAP = {
 'GTFS-G03-CSV-STRUCTURE':('invalid_row_length','routes.txt',None),
 'GTFS-G03-FIELD-TYPE':('invalid_color','routes.txt','route_text_color'),
 'GTFS-G03-FILE-CATALOG':('unknown_file','operator_extension.txt',None),
 'GTFS-G03-FILE-PRESENCE':('missing_calendar_and_calendar_date_files',None,None),
 'GTFS-G03-FILE-RESTRICTIONS':('route_networks_specified_in_more_than_one_file',None,'network_id'),
 'GTFS-G03-HEADER-SCHEMA':('missing_required_agency_id','routes.txt',None),
 'GTFS-G04-CONTEXTUAL-REFERENCE':('translation_foreign_key_violation',None,None),
 'GTFS-G04-IDENTITY-DOMAIN':('foreign_key_violation','trips.txt','service_id'),
 'GTFS-G04-PRIMARY-KEY-UNIQUENESS':('duplicate_key','stops.txt',None),
 'GTFS-G04-REFERENCE-EXISTENCE':('foreign_key_violation','stops.txt','parent_station'),
 'GTFS-G05-CALENDAR-RANGE':('start_and_end_range_out_of_order','calendar.txt',None),
 'GTFS-G05-FEED-RANGE':('start_and_end_range_out_of_order','feed_info.txt',None),
 'GTFS-G05-FREQUENCY-TIME-RANGE':('start_and_end_range_out_of_order','frequencies.txt',None),
 'TDL-G05-PICKUP-WINDOW-ORDER-REVIEW':('invalid_pickup_drop_off_window',None,None),
 'GTFS-G06-STOP-SEQUENCE':('duplicate_key','stop_times.txt',None),
 'TDL-G06-TRIP-TIME-ORDER-REVIEW':('stop_time_with_arrival_before_previous_departure_time',None,None),
 'GTFS-G07-COORDINATE-BOUNDS':('number_out_of_range','shapes.txt','shape_pt_lat'),
 'GTFS-G07-DISTANCE-PROGRESSION':('equal_shape_distance_diff_coordinates',None,None),
 'GTFS-G07-SHAPE-SEQUENCE':('duplicate_key','shapes.txt',None),
 'GTFS-G08-FEED-END-DATE-DECLARED':('missing_recommended_field','feed_info.txt','feed_end_date'),
 'GTFS-G08-FEED-START-DATE-DECLARED':('missing_recommended_field','feed_info.txt','feed_start_date'),
 'GTFS-G08-FEED-VERSION-DECLARED':('missing_recommended_field','feed_info.txt','feed_version'),
 'V1-RULE-GTFS':('foreign_key_violation','stop_times.txt','stop_id'),
 'GTFS-COORDINATE-RANGE':('number_out_of_range','stops.txt','stop_lat'),
 'GTFS-REF-SERVICE':('foreign_key_violation','trips.txt','service_id'),
 'GTFS-REF-SHAPE':('foreign_key_violation','trips.txt','shape_id'),
 'GTFS-REF-TRIP-ROUTE':('foreign_key_violation','trips.txt','route_id'),
 'GTFS-STRUCT-REQUIRED':('missing_required_file','agency.txt',None),
 'GTFS-STRUCT-SERVICE-CALENDAR':('missing_calendar_and_calendar_date_files',None,None),
 'GTFS-UNIQUE-PRIMARY-ID':('duplicate_key','stops.txt',None),
}


def focal_notices(row):
    target=MAP.get(row['criterion_id'])
    if target is None:return []
    code,table,field=target;found=[]
    for notice in row['notices']:
        if notice['code']!=code:continue
        samples=[]
        for s in notice['sampleNotices']:
            file=s.get('filename',s.get('childFilename'))
            name=s.get('fieldName',s.get('childFieldName'))
            if (table is None or file==table) and (field is None or name==field):samples.append(s)
        if samples:found.append({**notice,'focal_sampleNotices':samples})
    return found


def review_row(row,internal):
    focal=focal_notices(row);rid=row['criterion_id'];state=row['expected_state']
    outcome='FOCAL_NOTICE_PRESENT' if focal else 'NO_FOCAL_NOTICE_NOT_PASS'
    reason='Notice attributed by code and focal table/field; no whole-feed status comparison.'
    if rid in {'GTFS-G03-FIELD-TYPE','GTFS-G04-REFERENCE-EXISTENCE','GTFS-REF-SHAPE'} and row['case_id'].endswith('--negative'):
        outcome='NORMALIZATION_DIFFERENCE_REVIEW'
        reason='Fixture has a single space in optional color/reference. TDL preserves literal nonempty value; external has no focal error notice. Frozen File Requirements recommends removing extra spaces, not automatic equivalence to empty. No universal FP/FN asserted.'
    if rid=='GTFS-G06-FREQUENCY-OPERATIONS':
        outcome='CONTEXT_NOT_SHARED'
        reason='TDL witness supplies last_desired_departure separately; external CLI receives ZIP only. Absence of notice cannot judge that provider intention.'
    if rid=='GTFS-G05-SERVICE-DATE-SET':
        outcome='SCOPE_NOT_EQUIVALENT'
        reason='TDL criterion is calculation and context review of effective dates, not generic feed usability; no exact external focal assertion mapped.'
    if rid.startswith('TDL-G0'):
        outcome='AUTHORITY_DIFFERENCE_REVIEW'
        reason='External temporal/window notice is retained. TDL criterion is explicitly deferred pending approved source authority; external ERROR alone does not approve a mandatory TDL rule.'
    if rid.startswith('GTFS-G08-'):
        outcome='RECOMMENDATION_SCOPE_REVIEW'
        reason='TDL checks header declaration; external notice can check empty row value. Boundary empty value and absent header are separate; not a technical FP/FN.'
    if rid=='GTFS-G03-FILE-CATALOG':
        outcome='INFORMATIONAL_SCOPE_REVIEW'
        reason='External unknown_file is informational and TDL inventory classifies it while returning PASS for inventory execution. Neither proves feed nonconformance.'
    if row['system_notices']:
        reason+=' External system notices indicate partial validator execution; exit 0 is not proof that all validators succeeded.'
    return {'case_id':row['case_id'],'criterion_id':rid,'expected_state':state,'internal_classification':internal['classification'],
            'internal_native_status':internal['observed']['status'],'external_review':outcome,'focal_notices':focal,
            'system_notices':row['system_notices'],'reason':reason,'external_report_sha256':row['report_sha256'],
            'external_report_path':row['report_path'],'source_of_criterion':'Authored reference bank linked to fixed GTFS source; external output is comparison evidence only.'}


def review(external_path,measurement_path,output):
    output=Path(output)
    if output.exists():raise ValueError('Use new reviewed receipt')
    ext=read(external_path);internal={r['case_id']:r for r in read(measurement_path)['rows']}
    if ext['scenarios']!=96 or len(ext['rows'])!=96:raise ValueError('Incomplete external execution')
    rows=[review_row(r,internal[r['case_id']]) for r in ext['rows']]
    result={'contract':'TDL_EXTERNAL_REVIEW/1','reviewer':'Codex authoring agent','independent_human_review':False,
            'external_receipt_sha256':sha(external_path),'internal_measurement_sha256':sha(measurement_path),
            'review_code_sha256':sha(Path(__file__)),'notice_attribution_map':{k:list(v) for k,v in MAP.items()},'rows':rows,
            'counts':dict(Counter(r['external_review'] for r in rows)),
            'external_system_error_cases':[r['case_id'] for r in rows if r['system_notices']],
            'task_15_state':'COMPLETADA_BOUNDED_INTERNAL_MEASUREMENT_WITH_EXTERNAL_GTFS_CONTRAST',
            'unresolved_improvement_items':['Improve CSV diagnostic in next version','Resolve agency and translation conditions',
                'Review whitespace normalization without editing sealed expectations','Review temporal authority before implementing MUST',
                'No independent NeTEx semantic/profile comparator in this scope; profile criteria unavailable'],
            'global_accuracy':None,'neTEx_external_comparator_applicable':False}
    write(output,result)
    text=['# Contraste externo GTFS — revision delimitada','',
          'MobilityData 8.0.1, 96 escenarios GTFS, fecha fija 2026-10-09, un hilo por JVM, -svu y solo entrada local. La version fue descargada de la release oficial y su SHA-256 coincide con el digest publicado. No se interpreta ausencia de aviso como PASS. NeTEx no es entrada admisible para este validador; lxml no se presenta como comparador independiente.','',
          '| Caso | Comparacion TDL | Resultado externo revisado | Avisos focales | Errores internos externos |','|---|---|---|---|---|']
    for r in rows:
        text.append(f"| {r['case_id']} | {r['internal_classification']} | {r['external_review']} | {', '.join(n['code'] for n in r['focal_notices']) or 'Sin aviso focal; no PASS'} | {'SI' if r['system_notices'] else 'No'} |")
    text.extend(['','## Diferencias investigadas','',
       '1. CSV no cerrado: TDL rechaza con INSPECTION_ERROR sin diagnostico focal; externo emite invalid_row_length. Mejora de diagnostico para incremento nuevo.',
       '2. Agencia multiple sin agency_id y traduccion huerfana: TDL abstiene por cobertura/condiciones; externo emite missing_required_agency_id y translation_foreign_key_violation. Brechas confirmadas de evaluabilidad, no PASS correcto.',
       '3. Claves de secuencia duplicadas: externo duplicate_key y TDL G04 coinciden en la deteccion. No atribuir omision al auditor entero por PASS focal en G06/G07.',
       '4. Coordenada fuera de dominio: externo number_out_of_range, TDL G03 la detecta y G07 abstiene. Conservar atribucion y cobertura.',
       '5. Espacio en color/parent_station/shape_id: ausencia de aviso externo frente a fallo literal TDL. Diferencia de normalizacion; la recomendacion de retirar espacios no acredita que todos los productores/consumidores los traten como vacio. Revisar politica y expectativas antes de declarar falso positivo.',
       '6. Frecuencia y ultima salida deseada: contexto autoral no suministrado al CLI externo. No comparar el mismo criterio por ausencia de notice.',
       '7. Calendario invertido: externo emite aviso correcto de rango y dos excepciones de validadores secundarios. Registrar ejecucion parcial; exit 0 no basta.',
       '8. Ventanas y tiempos: externo emite ERROR donde TDL conserva criterio temporal no aprobado. Revisar norma/fuente exacta en un incremento; no convertir severidad externa en autoridad obligatoria.',
       '9. Recomendaciones: externo puede avisar sobre valor vacio y TDL sobre encabezado. No confundir omision de campo con vacio.',
       '10. Catalogo desconocido y conjunto de fechas vacio: el significado de inventario/calculo no es conformidad ni verdad del servicio.','',
       'Estas diferencias quedan clasificadas, no reparadas en motores congelados. La medicion 15 se cierra en este corpus sintetico, sin certificar precision universal ni comparacion semantica NeTEx independiente. Expectativas y revision del agente autor; revision humana corresponde a 18.',''])
    (output.parent/'EXTERNAL_REVIEW.md').write_text('\n'.join(text)+'\n',encoding='utf8')
    return result['counts']


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--external',type=Path,required=True);parser.add_argument('--measurement',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(review(args.external,args.measurement,args.output)))
