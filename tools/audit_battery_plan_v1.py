"""Source-bound test design, not a new GTFS/NeTEx audit implementation."""
import argparse
from collections import Counter
from pathlib import Path
import json
from tools.audit_corpus_v1 import ROOT, read, write, sha
from tools.audit_precision_v1 import REFERENCE


GTFS_PROPOSALS = [
 ('G-PLAN-01','P1','agency.txt','agency_id','Cardinality-dependent agency identity',
  'Require agency_id when multiple agencies are present; a single agency may omit it. Unknown cardinality stays NOT_EVALUABLE.',
  'Two agencies with distinct IDs: SATISFIED','Two agencies with missing agency_id: VIOLATED','One agency without agency_id: SATISFIED; unavailable agency evidence: UNKNOWN'),
 ('G-PLAN-02','P1','routes.txt','agency_id','Resolve conditional header and reference separately',
  'Require agency_id with multiple agencies; a supplied value references agency.agency_id. Do not replace value presence by header presence.',
  'Two agencies, route bound to one: SATISFIED','Two agencies, agency_id absent: VIOLATED','One agency without route agency_id: SATISFIED; supplied orphan: VIOLATED'),
 ('G-PLAN-03','P1','stops.txt','parent_station','Stop hierarchy and forbidden values',
  'Types 2/3 require station parent; type 4 requires platform parent; type 1 forbids parent. Type 0 parent is optional, if supplied it is station.',
  'Entrance referencing station: SATISFIED','Entrance missing parent, or station with parent: VIOLATED','Platform with no parent: SATISFIED; boarding area referencing station: VIOLATED'),
 ('G-PLAN-04','P1','stop_times.txt','arrival_time','Time requirement by ordered trip and timepoint',
  'Arrival required at first/last stop and exact timepoint; forbidden with pickup/drop-off windows. Determine endpoints by numeric sequence, not row order.',
  'First/last times declared, middle interpolated: SATISFIED','First arrival missing with no windows: VIOLATED','Unsorted physical rows and 25:00:00: SATISFIED; mixed windows/time: VIOLATED'),
 ('G-PLAN-05','P1','stop_times.txt','stop_sequence','Composite identity versus physical order',
  'Non-negative sequence orders the trip; values need not be consecutive. Duplicate (trip_id,stop_sequence) belongs to identity rule, not CSV ordering.',
  'Sequence 1,23,40: SATISFIED','Duplicate sequence within trip: VIOLATED identity','Shuffled rows and same sequence in distinct trips: SATISFIED'),
 ('G-PLAN-06','P1','shapes.txt','shape_pt_sequence','Shape identity and physical row permutation',
  'Non-negative sequence orders points per shape; duplicate composite key is checked in G04. Physical CSV order is not a separate failure criterion.',
  'Sequence 0,6,11: SATISFIED','Duplicate (shape_id,shape_pt_sequence): VIOLATED identity','Shuffle same point set: SATISFIED; negative sequence: VIOLATED type'),
 ('G-PLAN-07','P2','calendar_dates.txt','date','Calendar exceptions and real dates',
  'Use YYYYMMDD actual calendar dates and explicit exception semantics; empty effective service set is a diagnostic, not proof of wrong real service.',
  'Leap day 20280229 with addition: SATISFIED','Impossible date 20260229: VIOLATED type','Only removals yields empty set: REVIEW_REQUIRED operational context'),
 ('G-PLAN-08','P2','frequencies.txt','headway_secs','Frequency intervals and exact departure context',
  'Positive seconds; compare intervals of same trip according to frozen specification. Last desired departure is separate context, never guessed from end_time.',
  'Positive headway and disjoint same-trip intervals: SATISFIED','Zero headway: VIOLATED type','Adjacent intervals: inspect interval semantics; missing last desired departure: UNKNOWN for last-departure test'),
 ('G-PLAN-09','P2','shapes.txt','shape_dist_traveled','Distance progression and units',
  'Supplied distance is non-negative and increases in numeric sequence order; units agree with stop_times. Do not infer metres without evidence.',
  '0 then 100 with shared declared units: SATISFIED','Repeated supplied distance: VIOLATED progression','Omitted optional column: NOT_APPLICABLE; unit agreement without context: UNKNOWN'),
]

NETEX_PROPOSALS = [
 ('N-PLAN-01','P1','XML','TDL_SECURE_XML_POLICY','Secure XML and encoding',
  'TDL intake rejects unsafe DTD/entities and malformed XML; this is a security policy, not CEN profile conformance.',
  'Well-formed UTF-8/UTF-16 document: XML PASS','Unbalanced tag or external entity: intake FAIL','BOM or whitespace: PASS; rejected XML means XSD NOT_EVALUABLE'),
 ('N-PLAN-02','P1','XSD','PINNED_XSD_ARTIFACT','Pinned schema and dependency errors',
  'Validate only against exact v2.0.0 schema and 458 named dependency hashes; missing schema is inspection failure, not invalid operator XML.',
  'Existing valid_minimal.xml: XSD PASS','Existing xsd_invalid.xml: XSD FAIL','Missing/changed dependency in isolated copy: INSPECTION_ERROR; do not alter original schema'),
 ('N-PLAN-03','P1','IDENTITY','TDL_DIAGNOSTIC','Typed versioned object identity',
  'Diagnostic groups type,id,version and document context. Equal IDs across versions require review, not unconditional EPIP failure.',
  'Distinct scoped identities: diagnostic satisfied','Same type/id/version conflict: REVIEW_REQUIRED','Same ID different versions or frame context: REVIEW_REQUIRED'),
 ('N-PLAN-04','P1','REFERENCES','TDL_DIAGNOSTIC','Reference context and resolution',
  'Resolve type/id/version only in supplied scope; external unresolved references remain UNKNOWN until scope/completeness and target catalogue are identified.',
  'Local exact typed/versioned target: SATISFIED','Missing target in explicitly closed graph: REVIEW_REQUIRED diagnostic','External target or unknown version policy: UNKNOWN; JSON witness is not NeTEx PublicationDelivery'),
 ('N-PLAN-05','P2','NETWORK_STOPS','TDL_DIAGNOSTIC','Journey pattern and stop associations',
  'Inspect graph links between journey-pattern points, scheduled stop points and supplied stop assignments. No equivalence with GTFS stops is assumed.',
  'Complete local target associations: diagnostic satisfied','Unresolved local link in closed graph: REVIEW_REQUIRED','Partial external frame: UNKNOWN; exact profile obligations unavailable'),
 ('N-PLAN-06','P2','CALENDAR','TDL_DIAGNOSTIC','Day types and operating dates',
  'Build diagnostic effective dates only when day types, assignments and operating periods are supplied and interpreted. Service reality needs independent reference.',
  'Supplied coherent assignments: diagnostic satisfied','Conflicting local assignment: REVIEW_REQUIRED','No effective dates or missing referenced frame: UNKNOWN operational meaning'),
 ('N-PLAN-07','P2','TIMETABLE','TDL_DIAGNOSTIC','Passing times and day offsets',
  'Interpret passing times with day offset and supplied timezone; compare service journeys in their context. No new MUST asserted without controlled profile criterion.',
  'Cross-midnight time with explicit day offset: diagnostic satisfied','Contradictory offset/time in known context: REVIEW_REQUIRED','Missing timezone/day-offset interpretation: UNKNOWN'),
 ('N-PLAN-08','P2','SPATIAL','TDL_DIAGNOSTIC','Coordinate reference system',
  'Evaluate spatial bounds only with declared CRS/axis convention; do not apply WGS84 ranges to arbitrary projected coordinates.',
  'Known WGS84 axes and in-range coordinate: diagnostic satisfied','Known WGS84 out-of-range: REVIEW_REQUIRED','Projected or undeclared CRS: UNKNOWN until identified'),
 ('N-PLAN-09','P1','PROFILE','CONTROLLED_PROFILE_NOT_AVAILABLE','EPIP 2026 requirement mapping',
  'Full controlled CEN/TS 16614-4:2026 text is absent. No exact assertions or fixtures can be approved from public overview or XSD.',
  'XSD-valid example: profile HUMAN_REVIEW_REQUIRED','XSD-invalid example: not a complete EPIP decision','Malformed XML: profile NOT_EVALUABLE'),
 ('N-PLAN-10','P2','DESTINATION','DESTINATION_CONTRACT_NOT_AVAILABLE','National and destination requirements',
  'No selected destination profile/acceptance contract. Obtain version and exact requirements before mapping technical assertions.',
  'Contract provided: new controlled mapping required','Contract absent: UNKNOWN','XSD PASS never implies destination acceptance'),
]


def source_row(spec,file,field):
    lines=spec.splitlines();start=lines.index('### '+file)
    stop=next((i for i in range(start+1,len(lines)) if lines[i].startswith('### ')),len(lines))
    matches=[(i+1,lines[i]) for i in range(start,stop) if lines[i].startswith('|') and '`'+field+'`' in lines[i].split('|')[1]]
    if len(matches)!=1:raise ValueError('Source field selector ambiguous: '+file+':'+field)
    line,text=matches[0]
    import hashlib
    return {'source_id':'GTFS-FIXED','section':'### '+file,'field':field,'line':line,'row_sha256':hashlib.sha256(text.encode()).hexdigest()}


def build(output):
    output=Path(output)
    if output.exists():raise ValueError('Use new plan directory')
    inventory_path=ROOT/'reports/audit_foundation_v1/accepted_reference_20261008/CONTROL_INVENTORY.json'
    inventory=read(inventory_path);bank=read(REFERENCE/'REFERENCE_BANK.json');criteria=read(REFERENCE/'CRITERIA.json')
    spec_path=ROOT/'03_Compliance/reports/evidence/compliance_v1_20260928/sources/gtfs_reference.md'
    spec=spec_path.read_text(encoding='utf8');rules=[]
    criterion_items=criteria['criteria'] if isinstance(criteria,dict) else criteria
    source_criteria={c['criterion_id']:c for c in criterion_items}
    for rid in bank['current_rule_ids']:
        cases=[c for c in bank['cases'] if c['criterion_id']==rid]
        rules.append({'rule_id':rid,'criterion':source_criteria[rid],
            'fixtures':[{'case_id':c['case_id'],'variant':c['variant'],'fixture':c['fixture'],'sha256':c['sha256'],'expected':c['expected']} for c in cases],
            'coverage':'THREE_CURRENT_WITNESSES_NOT_EXHAUSTIVE','next':'Expand field/condition branches and follow discrepancy review.'})
    proposed=[]
    for rows,fmt in ((GTFS_PROPOSALS,'GTFS_SCHEDULE'),(NETEX_PROPOSALS,'NETEX')):
        for row in rows:
            pid,priority,area,field,title,assertion,positive,negative,boundary=row
            entry={'proposal_id':pid,'format':fmt,'priority':priority,'area':area,'title':title,'criterion':assertion,
                'application_condition':'Apply only to supplied, interpretable data and explicitly identified scope; unknown prerequisites never PASS.',
                'authority':field if fmt=='NETEX' else 'GTFS_FIXED_FIELD_DEFINITION',
                'fixtures':{'positive':positive,'negative':negative,'boundary':boundary},
                'implementation_status':'DESIGNED_NOT_IMPLEMENTED','fixture_status':'SPECIFIED_NOT_MATERIALIZED',
                'expected_review':'Authored design, requires implementation acceptance; not independent human review.'}
            if fmt=='GTFS_SCHEDULE':entry['source_selector']=source_row(spec,area,field)
            else:
                entry['source_ids']=['NETEX-XSD-MANIFEST'] if area=='XSD' else ['NETEX-EPIP-2026'] if area=='PROFILE' else ['NETEX-REGISTRY']
                entry['exact_normative_assertion_available']=area=='XSD'
                entry['blocking_reason']='Full controlled profile absent' if area=='PROFILE' else 'Destination contract absent' if area=='DESTINATION' else None
            proposed.append(entry)
    fields=[{**f,'next_fixture_dimensions':['supplied valid','supplied invalid','absent header versus empty value','conditional true/false/unknown'],
             'boundary_expected':'NOT_APPROVED_GENERIC_MATRIX; select values and semantic empty rules from exact field criterion before materialization.',
             'scope':'132-field frozen inventory, not all GTFS fields/extensions'} for f in inventory['GTFS_field_capability']['fields']]
    result={'contract':'TDL_BATTERY_DESIGN/1','revision':'TDL-BATTERY-20261009-V1','tasks':['TDL-AUD-10','TDL-AUD-11'],
        'inputs':{'inventory_sha256':sha(inventory_path),'bank_sha256':sha(REFERENCE/'REFERENCE_BANK.json'),'gtfs_spec_sha256':sha(spec_path)},
        'current_rule_design':rules,'proposals':proposed,'gtfs_file_scope':inventory['GTFS_file_catalog']['files'],'gtfs_field_branch_matrix':fields,
        'netex_schema':{'version':'2.0.0','commit':'a94e5e1752bcc13aabb8a1f3d018dc08e6978f42','profile':'EPIP 2026 REQUESTED_NOT_EVALUABLE',
                        'root_sha256':'965bc6d92efb49a8ce6fa8fac3f4ef6a172d57c3d54aa9d49799ffcc14a17175'},
        'selection_for_next_increment':{'GTFS':['G-PLAN-01','G-PLAN-02'],'NETEX':['N-PLAN-03','N-PLAN-04'],
            'condition':'Tasks 12/13 approve bounded selection, materialize fixtures and run regression. Diagnostic graph tests do not establish XML or EPIP conformance.'},
        'out_of_scope':['GTFS-RT','SIRI','Actual service truth without independent reference','Unimplemented GTFS file extensions listed by inventory','Full NeTEx/EPIP or national profile conformance'],
        'engine_modified':False,'holdout_accessed':False,'full_coverage_claim':False}
    validate(result)
    write(output/'BATTERY_PLAN.json',result)
    text=['# Baterías de auditoría GTFS y NeTEx — diseño V1','',
          'TDL-AUD-10/11: diseño delimitado, no implementación ni cobertura completa. Fuente GTFS fijada 2026-04-27; XSD NeTEx 2.0.0 identificado. EPIP 2026 completo y contrato del destino no disponibles.','',
          f"Se enlazan {len(rules)} controles y 108 fixtures actuales; {len(proposed)} propuestas tienen escenarios positivo, negativo y de límite especificados. Matriz de ramas para {len(fields)} campos y disposición de 32 archivos. Los escenarios propuestos aún no están materializados.",'',
          'Orden: primero discrepancias de ejecución/estado y condiciones de agencia; después referencias NeTEx con identidad contextual; después calendario, tiempos y espacial. Nunca modificar el banco para conseguir coincidencia con el motor.','']
    for p in proposed:
        text.extend([f"## {p['proposal_id']} · {p['priority']} · {p['title']}",'',p['criterion'],'',
                     f"Aplicación: {p['application_condition']}",'',
                     f"Fuente: `{p.get('source_selector',p.get('source_ids'))}`. Autoridad: {p['authority']}.",'',
                     '* Positivo: '+p['fixtures']['positive'], '* Negativo: '+p['fixtures']['negative'], '* Límite/contexto: '+p['fixtures']['boundary'],''])
    text.extend(['## Criterios de aceptación de las implementaciones','',
       'Cada incremento identifica regla y versión nuevas, fuente/hash/localizador, precondiciones, autoridad y localizador de hallazgo. Materializar los tres escenarios y sus variantes de contexto; verificar hechos sin copiar salidas del auditor. Comparar baseline e incremento, explicar diferencias y conservar RAW. Casos metamórficos: permutar filas, renombrar IDs preservando referencias y variar orden de archivos conserva resultados semánticos donde proceda.','',
       'GTFS: agrupar por clave, ordenar secuencias numéricamente, aceptar horas extendidas; separar recomendación, dato opcional vacío, condición desconocida y valor inválido. NeTEx: XML, XSD, perfil y diagnóstico son capas distintas; ausencia de resultados no implica PASS. Dependencias faltantes son defecto de entorno; no del productor.','',
       'El detalle de campos mantiene las brechas del inventario; no convierte sus 132 entradas en cobertura total. Fares/Flex y archivos diferidos requieren incremento específico. NeTEx calendarios/horarios/CRS están diseñados como diagnósticos pendientes de contexto, no como requisitos CEN inventados.',''])
    (output/'DESIGN.md').write_text('\n'.join(text),encoding='utf8')
    return {'rules':len(rules),'proposals':len(proposed),'fields':len(fields),'files':len(result['gtfs_file_scope'])}


def validate(plan):
    ids=[p['proposal_id'] for p in plan['proposals']]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate proposal')
    for p in plan['proposals']:
        if set(p['fixtures'])!={'positive','negative','boundary'} or not all(p['fixtures'].values()):raise ValueError('Incomplete fixture design')
        if p['implementation_status']!='DESIGNED_NOT_IMPLEMENTED':raise ValueError('Design promoted to implementation')
        if p['format']=='NETEX' and p['area']=='PROFILE' and not p['blocking_reason']:raise ValueError('Profile gap suppressed')
    if plan['engine_modified'] or plan['holdout_accessed'] or plan['full_coverage_claim']:raise ValueError('Invalid scope claim')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(build(args.output)))
