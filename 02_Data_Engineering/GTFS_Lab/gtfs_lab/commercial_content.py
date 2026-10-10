"""Reviewed editorial content for the additive transport report, 2026-10-08.

Legal entries are bounded review questions, never automated legal verdicts.
They do not modify the frozen Compliance catalogue or engine decisions.
"""

RULES = {
    'CSV-STRUCTURE': ('Lectura de los ficheros', 'Organización de filas y columnas para que la información pueda leerse de forma consistente.'),
    'FIELD-TYPE': ('Formato de los valores', 'Compatibilidad de los valores con el formato previsto en cada campo; las incidencias corresponden al color del texto de dos líneas.'),
    'FILE-CATALOG': ('Inventario de ficheros', 'Reconocimiento de los ficheros incluidos en el conjunto entregado.'),
    'FILE-PRESENCE': ('Información necesaria', 'Presencia de ficheros según las condiciones que comprueba el motor.'),
    'FILE-RESTRICTIONS': ('Combinaciones de ficheros', 'Restricciones entre ficheros según las condiciones implantadas.'),
    'HEADER-SCHEMA': ('Nombres de las columnas', 'Correspondencia de las cabeceras con el esquema admitido. La ejecución no permite emitir una conclusión.'),
    'CONTEXTUAL-REFERENCE': ('Relaciones condicionadas por el servicio', 'Relaciones exigibles solo cuando aparecen las condiciones previstas por esta comprobación.'),
    'IDENTITY-DOMAIN': ('Identificación de entidades', 'Coherencia de los identificadores en los dominios comprobados.'),
    'PRIMARY-KEY-UNIQUENESS': ('Identificadores sin duplicados', 'Unicidad de las claves en las tablas inspeccionadas.'),
    'REFERENCE-EXISTENCE': ('Enlaces entre paradas, viajes y trazados', 'Existencia de los destinos de las referencias informadas. Hay incidencias y cinco comprobaciones no evaluables.'),
    'CALENDAR-RANGE': ('Periodos de servicio', 'Orden y consistencia de las fechas de los calendarios declarados.'),
    'FEED-RANGE': ('Periodo global de la publicación', 'Comprobación del periodo general cuando está declarado.'),
    'FREQUENCY-TIME-RANGE': ('Inicio y fin de las franjas horarias', 'Orden temporal de los intervalos publicados. Este resultado no resuelve la distinta comprobación sobre su última salida.'),
    'SERVICE-DATE-SET': ('Fechas de circulación', 'Comprobación del conjunto de fechas definido por calendario y excepciones.'),
    'PICKUP-WINDOW-ORDER-REVIEW': ('Ventanas de recogida', 'Revisión de ventanas de recogida cuando se declaran.'),
    'FREQUENCY-OPERATIONS': ('Salidas en servicios por intervalo', 'Coherencia de la programación por intervalos, incluido el límite de la última salida.'),
    'STOP-SEQUENCE': ('Orden de paso por paradas', 'Secuencia declarada de las paradas de cada viaje.'),
    'TRIP-TIME-ORDER-REVIEW': ('Orden de las horas de paso', 'Revisión temporal del viaje; no se obtuvo una evaluación en esta ejecución.'),
    'COORDINATE-BOUNDS': ('Coordenadas dentro de rango', 'Rangos numéricos admisibles de las coordenadas. No acredita que el punto coincida con una parada o calzada real.'),
    'DISTANCE-PROGRESSION': ('Distancia acumulada del itinerario', 'Progresión de la distancia declarada entre puntos consecutivos de cada trazado.'),
    'SHAPE-SEQUENCE': ('Orden de los puntos del trazado', 'Secuencia de puntos que forma el itinerario publicado.'),
    'FEED-END-DATE-DECLARED': ('Fecha final de la publicación', 'Declaración de la fecha final recomendada; el campo no está presente.'),
    'FEED-START-DATE-DECLARED': ('Fecha inicial de la publicación', 'Declaración de la fecha inicial recomendada; el campo no está presente.'),
    'FEED-VERSION-DECLARED': ('Versión de la publicación', 'Declaración de una versión identificable; el campo no está presente.'),
}

LEGAL = [
    dict(id='UE-01', level='Unión Europea', title='Acceso a datos de información multimodal',
         source='Reglamento Delegado (UE) 2017/1926, art. 4.1; versión consolidada de 04/03/2024, modificada por 2024/490',
         url='https://eur-lex.europa.eu/eli/reg_del/2017/1926/2024-03-04',
         analysis='Marco de disponibilidad de datos. El catálogo interno vincula V1-RULE-GTFS a una descomposición parcial del requisito A04-P01-001.',
         check='Se inspeccionaron referencias de paradas fijas a viajes y paradas/plataformas. No se inspeccionó el acceso público nacional ni el conjunto de obligaciones del artículo.',
         validation='Sin incidencias en esa prueba técnica acotada. La evidencia fuente declara expresamente que no permite concluir sobre cumplimiento legal.',
         assessment='Cumplimiento legal no determinado. La correspondencia técnica documentada es parcial.',
         solution='Responsable de publicación: aportar perfil exigible, ámbito y sujeto obligado, plazos aplicables, registro y acceso al Punto de Acceso Nacional; verificar cada obligación y documentar las evidencias.',
         mapping='DOCUMENTED_PARTIAL', rules=['V1-RULE-GTFS']),
    dict(id='ES-01', level='España', title='Disponibilidad y actualización de datos de movilidad',
         source='Ley 9/2025 de Movilidad Sostenible, arts. 85 y 90 y anexo I',
         url='https://www.boe.es/buscar/act.php?id=BOE-A-2025-24545',
         analysis='Se identifican deberes relativos a datos de movilidad y al Punto de Acceso Nacional. Su aplicación requiere concretar operador, datos y servicio.',
         check='El expediente contiene un fichero local. Faltan evidencias de acceso, actualización, condiciones de incorporación e idioma de la información comunicada.',
         validation='No existe en esta ejecución una validación específica de estos artículos.',
         assessment='Pendiente de determinar; los controles de estructura, horarios y referencias solo pueden contribuir como evidencia técnica.',
         solution='Responsable de publicación: identificar obligaciones y fechas aplicables, aportar publicación y actualizaciones, contrastar el anexo I y documentar requisitos de incorporación e idioma. Cerrar con evidencia fechada de cada punto.',
         mapping='CONTEXT_ONLY', rules=[]),
    dict(id='ES-02', level='España', title='Marco de sistemas de transporte inteligentes',
         source='Real Decreto 450/2026, arts. 1 y 5 y disposición derogatoria única; vigente desde 06/06/2026',
         url='https://www.boe.es/buscar/act.php?id=BOE-A-2026-12035',
         analysis='Marco estatal vigente de los sistemas inteligentes de transporte y del Punto de Acceso Nacional de Transporte Multimodal. Deroga expresamente el Real Decreto 662/2012, que solo se conserva como antecedente histórico.',
         check='No se ha aportado el sistema receptor ni el perfil de intercambio contratado.',
         validation='Revisión documental de la fuente normativa; sin prueba automatizada específica en RUN02.',
         assessment='No determina por sí solo el formato exigible a este fichero.',
         solution='Responsable del servicio: documentar destino, especificaciones y condiciones de intercambio; contrastarlas antes de concluir sobre interoperabilidad.',
         mapping='CONTEXT_ONLY', rules=[]),
    dict(id='IB-01', level='Illes Balears', title='Información de horarios y frecuencias en las paradas',
         source='Ley 4/2014 de transportes terrestres y movilidad sostenible, art. 37.6',
         url='https://www.boe.es/buscar/act.php?id=BOE-A-2014-7536#a3-9',
         analysis='Las administraciones deben garantizar información suficiente sobre precios, horarios y frecuencias en las paradas urbanas e interurbanas.',
         check='Se detectaron intervalos que necesitan corrección técnica. No se compararon con la información efectivamente ofrecida al viajero.',
         validation='No hay verificación de campo ni documental del cumplimiento de este artículo.',
         assessment='La incidencia del fichero no prueba un incumplimiento de la información en parada.',
         solution='Administración competente y operador: aportar información vigente en parada y horario autorizado, contrastar una muestra justificada y corregir discrepancias. Registrar alcance, fecha y evidencias antes de cerrar.',
         mapping='CONTEXT_ONLY', rules=[]),
    dict(id='LOCAL-01', level='Contrato y ámbito local', title='Condiciones particulares del servicio',
         source='Pliegos, acuerdos de publicación y normativa local: no aportados', url='',
         analysis='El destino y las condiciones particulares pueden añadir exigencias a los datos.',
         check='No constan documentos que permitan establecer esos requisitos.',
         validation='Sin evaluación; no se inventa una obligación a partir de una recomendación técnica.',
         assessment='Ámbito contractual y local pendiente de delimitar.',
         solution='Responsable del contrato: aportar pliegos, acuerdos y normativa aplicable; identificar obligación, prueba, responsable y criterio de aceptación para cada requisito.',
         mapping='UNDETERMINED', rules=[]),
]

LEGAL.extend([
    dict(id='PRIV-01', level='Datos personales', title='Frontera de privacidad para publicación',
         source='Reglamento (UE) 2016/679, arts. 4.1 y 5; Reglamento 2017/1926, art. 4.6',
         url='https://www.boe.es/buscar/doc.php?id=DOUE-L-2016-80807',
         analysis='La publicación a través del NAP no debe incluir datos personales. La identificación de una persona exige contexto; un email funcional no prueba por sí solo presencia de datos personales.',
         check='Los controles técnicos de RUN02 no constituyen una revisión de privacidad de todos los campos, extensiones y archivos adicionales.',
         validation='Revisión de las fuentes y sus correcciones; sin detector jurídico automatizado ni declaración de ausencia de datos personales.',
         assessment='No determinado para la publicación: falta revisión contextual documentada del conjunto completo.',
         solution='Antes de publicación, registrar los campos revisados, finalidad, personas identificables y decisión de exclusión o anonimización.',
         mapping='CONTEXT_ONLY', rules=[]),
    dict(id='SPAT-01', level='Información espacial', title='Ámbito e interoperabilidad espacial',
         source='Directiva 2007/2/CE, arts. 4 y 7; Ley 14/2010; modificaciones 2019/1010 y 2024/2829',
         url='https://www.boe.es/buscar/doc.php?id=DOUE-L-2007-80587',
         analysis='INSPIRE delimita conjuntos, titulares y servicios espaciales. Su referencia en el Reglamento multimodal no convierte shapes.txt en una prueba de conformidad.',
         check='Coordenadas y trazados comprobados técnicamente; no se evaluó un perfil INSPIRE ni los servicios de una infraestructura pública.',
         validation='Fuentes originales, corrección y modificación capturadas; sin validador INSPIRE.',
         assessment='Aplicabilidad no determinada: falta identificar titular, conjunto de referencia y perfil o normas de ejecución exigibles.',
         solution='Documentar titular, ámbito, perfil de red espacial y evidencia de interoperabilidad antes de emitir una conclusión.',
         mapping='CONTEXT_ONLY', rules=[]),
    dict(id='REUSE-01', level='Reutilización', title='Derechos y condiciones de reutilización',
         source='Ley 37/2007, arts. 2, 3 y 8; Ley 18/2015; Directiva 2019/1024; RDL 24/2021, libro tercero',
         url='https://www.boe.es/buscar/act.php?id=BOE-A-2007-19814',
         analysis='El régimen de reutilización depende del sujeto, el documento y las exclusiones aplicables. No se presume que todo dato de un operador privado sea información del sector público.',
         check='No constan en esta presentación documentos que acrediten la licencia concreta, la autorización del titular o las condiciones aceptadas.',
         validation='Revisión contextual del régimen y de su transposición; sin verificación contractual del operador.',
         assessment='No determinado para publicación o reutilización externa.',
         solution='Aportar titularidad o autorización, licencia, atribución y condiciones del conjunto concreto; registrar su revisión.',
         mapping='UNDETERMINED', rules=[]),
    dict(id='NAP-01', level='Punto de Acceso Nacional', title='Acuerdo del proveedor y orientación administrativa',
         source='Política de contribución, licencia de datos y FAQ del NAP; documentos de distinta autoridad',
         url='https://nap.transportes.gob.es/Provider/PoliticaContribucion',
         analysis='El acuerdo del proveedor regula autorización, calidad, actualización y retirada. La FAQ orienta sobre GTFS y NeTEx y conserva una referencia al RD derogado; no sustituye la legislación vigente.',
         check='No se acredita aceptación del acuerdo ni publicación real de este conjunto en el NAP.',
         validation='Contexto documental; sin prueba del vínculo contractual ni del servicio receptor.',
         assessment='No determinado: la aceptación técnica GTFS no acredita cumplimiento jurídico ni equivalencia con NeTEx.',
         solution='Aportar acuerdo y licencia aplicables y evidencia de acceso, metadatos y actualización del conjunto publicado.',
         mapping='UNDETERMINED', rules=[]),
])

# Authority belongs to each source, not to the technical result of an audit.
for _entry in LEGAL:
    _entry['as_of'] = '2026-10-08'
    _entry['applicability'] = 'UNDETERMINED'
    _entry['legal_conclusion_allowed'] = False
    _entry['context_review_status'] = 'REVIEWED_WITH_LIMITS'
    _entry['authority_types'] = {
        'UE-01': ['EU_REGULATION'], 'ES-01': ['NATIONAL_LEGISLATION'],
        'ES-02': ['NATIONAL_LEGISLATION'], 'IB-01': ['REGIONAL_LEGISLATION'],
        'LOCAL-01': ['CONTRACT_OR_LOCAL_RULE_UNIDENTIFIED'],
        'PRIV-01': ['EU_REGULATION'],
        'SPAT-01': ['EU_DIRECTIVE', 'NATIONAL_LEGISLATION', 'EU_DECISION'],
        'REUSE-01': ['NATIONAL_LEGISLATION', 'EU_DIRECTIVE'],
        'NAP-01': ['NAP_PROVIDER_CONTRACT', 'NAP_LICENCE', 'ADMINISTRATIVE_GUIDANCE'],
    }[_entry['id']]
del _entry


STATUS = {'PASS': 'Sin incidencias detectadas en el alcance comprobado',
          'FAIL_TECHNICAL': 'Requiere actuación', 'NOT_EVALUABLE': 'No se pudo evaluar',
          'NOT_APPLICABLE': 'No aplicó en esta ejecución'}
DISPOSITIONS = {'PARTIAL': 'Cobertura parcial', 'HUMAN_REVIEW_REQUIRED': 'Requiere revisión documental',
                'DEFERRED': 'Comprobación aplazada', 'OUT_OF_SCOPE_V1': 'Fuera del alcance de V1'}

LEGACY_RULES = {
    'GTFS-COORDINATE-RANGE': ('Coordenadas: comprobador anterior', 'Rangos numéricos de las coordenadas inspeccionadas; no contrasta la ubicación física del servicio.'),
    'GTFS-REF-SERVICE': ('Correspondencia con el calendario', 'Referencias de los viajes al servicio declarado.'),
    'GTFS-REF-SHAPE': ('Correspondencia con el trazado', 'Referencias de los viajes a trazados existentes. Los doce hallazgos son los mismos eventos reconciliados en PAL-G04-SHAPE.'),
    'GTFS-REF-TRIP-ROUTE': ('Correspondencia de viaje y línea', 'Referencias de los viajes a las líneas declaradas.'),
    'GTFS-STRUCT-REQUIRED': ('Estructura necesaria: comprobador anterior', 'Elementos estructurales requeridos por este comprobador.'),
    'GTFS-STRUCT-SERVICE-CALENDAR': ('Disponibilidad de calendario de servicio', 'Estructura de calendario utilizada para declarar los servicios.'),
    'GTFS-UNIQUE-PRIMARY-ID': ('Identificadores únicos: comprobador anterior', 'Unicidad de identificadores según el alcance del comprobador anterior.'),
}

CATALOGUE_TRANSLATIONS = {
    'DEFERRED_BY_PRODUCT_SCOPE: realtime, road format or spatial-network track outside committed GTFS/NeTEx pilots.': 'El producto V1 no incorpora esta comprobación sobre tiempo real, formato de carretera o red espacial. Esto no excluye la obligación legal.',
    'Two operational technical subscopes demonstrated; broad NAP/static/historical/observed obligation not demonstrated.': 'Se demostraron dos comprobaciones técnicas acotadas. No se acreditó la obligación amplia sobre acceso nacional y datos estáticos, históricos y observados.',
    'Historical obligation, mapping, review and coverage remain unchanged; no operational V1 claim.': 'Se conserva la obligación y su evaluación histórica. El producto V1 no aporta una comprobación operativa de este requisito.',
    'No claim that the full legal requirement is delivered.': 'No se acredita el cumplimiento completo del requisito legal.',
    'Additional reviewed scopes and contextual NAP evidence.': 'Añadir comprobaciones revisadas y evidencia del acceso a los datos en el Punto de Acceso Nacional.',
    'GTFS + NeTEx V1 stable AND the relevant future track explicitly opened.': 'Requiere abrir y validar expresamente la capacidad correspondiente del producto, con el alcance y las evidencias acordados.',
    'Perfil, constraints o aplicabilidad incompletos.': 'Faltan especificaciones, restricciones o justificación de aplicación al servicio.',
    'Perfil versionado y crosswalk revisado por scope.': 'Aportar las especificaciones identificadas por versión y una correspondencia revisada de requisitos y datos para este alcance.',
    'No acredita operación NAP.': 'No demuestra la disponibilidad y acceso a los datos a través del Punto de Acceso Nacional.',
    'Evidencia NAP identificable y contrato de inspección acotado.': 'Aportar evidencia identificable del Punto de Acceso Nacional y acordar qué acceso y datos se inspeccionarán.',
    'No evalúa neutralidad ni ranking.': 'No se ha comprobado la neutralidad ni el orden de presentación de las alternativas de viaje.',
}
