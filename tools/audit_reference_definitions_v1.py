"""Authored expectations for small synthetic reference cases, not engine output.

Cases focus one criterion: they do not predict aggregate whole-feed outcomes.
"""
from copy import deepcopy


BASE = {
 "agency.txt": [{"agency_id":"AG","agency_name":"TDL synthetic","agency_url":"https://example.org","agency_timezone":"Europe/Madrid"}],
 "stops.txt": [{"stop_id":"ST1","stop_name":"Synthetic A","stop_lat":"41","stop_lon":"2","location_type":"0","parent_station":""},
               {"stop_id":"ST2","stop_name":"Synthetic B","stop_lat":"41.01","stop_lon":"2.01","location_type":"0","parent_station":""}],
 "routes.txt": [{"route_id":"R","agency_id":"AG","route_short_name":"1","route_long_name":"","route_type":"3","route_text_color":"000000"}],
 "trips.txt": [{"route_id":"R","service_id":"S","trip_id":"T","shape_id":"SH"}],
 "stop_times.txt": [{"trip_id":"T","arrival_time":"24:00:00","departure_time":"24:00:00","stop_id":"ST1","stop_sequence":"1"},
                    {"trip_id":"T","arrival_time":"25:00:00","departure_time":"25:00:00","stop_id":"ST2","stop_sequence":"3"}],
 "calendar.txt": [{"service_id":"S","monday":"1","tuesday":"1","wednesday":"1","thursday":"1","friday":"1","saturday":"1","sunday":"1","start_date":"20261001","end_date":"20261031"}],
 "shapes.txt": [{"shape_id":"SH","shape_pt_lat":"41","shape_pt_lon":"2","shape_pt_sequence":"1","shape_dist_traveled":"0"},
                {"shape_id":"SH","shape_pt_lat":"41.01","shape_pt_lon":"2.01","shape_pt_sequence":"3","shape_dist_traveled":"100"}],
 "feed_info.txt": [{"feed_publisher_name":"TDL synthetic","feed_publisher_url":"https://example.org","feed_lang":"es","feed_start_date":"20261001","feed_end_date":"20261031","feed_version":"synthetic-v1"}]
}

# id, source locator, authority, criterion paraphrase, scenario family.
DEFINITIONS = [
 ("GTFS-G03-CSV-STRUCTURE","## File Requirements","FORMAT_REQUIRED","Ficheros CSV legibles, encabezado y escapado coherentes.","csv"),
 ("GTFS-G03-FIELD-TYPE","### Field Types","FORMAT_REQUIRED_IF_SUPPLIED","Un color informado debe tener seis dígitos hexadecimales; vacío y espacio son diferentes.","color"),
 ("GTFS-G03-FILE-CATALOG","## Dataset Files","TDL_DIAGNOSTIC","Distinguir archivos del formato y extensiones; un archivo desconocido no prueba por sí solo una infracción.","catalog"),
 ("GTFS-G03-FILE-PRESENCE","## Dataset Files","FORMAT_CONDITIONAL","calendar.txt es necesario si falta calendar_dates.txt.","calendar_presence"),
 ("GTFS-G03-FILE-RESTRICTIONS","networks.txt","FORMAT_CONDITIONAL","No combinar networks.txt con network_id en routes.txt.","networks"),
 ("GTFS-G03-HEADER-SCHEMA","### routes.txt","FORMAT_CONDITIONAL","route_id es requerido; agency_id depende de si hay una o varias agencias.","header"),
 ("GTFS-G04-CONTEXTUAL-REFERENCE","### translations.txt","FORMAT_CONDITIONAL","record_id en una traducción de nombre de parada identifica un registro del archivo indicado.","translation"),
 ("GTFS-G04-IDENTITY-DOMAIN","### trips.txt","FORMAT_REQUIRED","service_id de un viaje identifica servicio en calendar o calendar_dates.","service_ref"),
 ("GTFS-G04-PRIMARY-KEY-UNIQUENESS","Primary key","FORMAT_REQUIRED","Una clave primaria de parada no puede repetirse.","unique"),
 ("GTFS-G04-REFERENCE-EXISTENCE","### stops.txt","FORMAT_REQUIRED_IF_SUPPLIED","parent_station opcional para tipo 0; una referencia informada debe existir y ser adecuada.","parent"),
 ("GTFS-G05-CALENDAR-RANGE","### calendar.txt","FORMAT_REQUIRED","La fecha final de calendar no precede a la inicial.","calendar_range"),
 ("GTFS-G05-FEED-RANGE","### feed_info.txt","FORMAT_REQUIRED_IF_SUPPLIED","Si se informan ambas fechas de feed_info, la final no precede a la inicial; no equivale a comprobar servicio real.","feed_range"),
 ("GTFS-G05-FREQUENCY-TIME-RANGE","### frequencies.txt","FORMAT_REQUIRED","Un intervalo de frecuencia tiene comienzo y fin ordenados; las horas extendidas conservan su significado.","frequency_range"),
 ("GTFS-G05-SERVICE-DATE-SET","### calendar_dates.txt","TDL_DIAGNOSTIC","El conjunto efectivo combina calendario y excepciones; un conjunto vacío requiere contexto antes de atribuir incumplimiento.","service_dates"),
 ("TDL-G05-PICKUP-WINDOW-ORDER-REVIEW","start_pickup_drop_off_window","TDL_REVIEW_MARKER","Conservar diagnóstico de ventanas sin inventar una aserción obligatoria revisada para este control.","window_review"),
 ("GTFS-G06-FREQUENCY-OPERATIONS","### frequencies.txt","FORMAT_CONDITIONAL","Con exact_times=1, el fin es posterior a la última salida deseada e inferior a esa salida más headway.","frequency_end"),
 ("GTFS-G06-STOP-SEQUENCE","stop_sequence","FORMAT_REQUIRED","La secuencia de paradas aumenta por viaje; puede tener saltos.","stop_sequence"),
 ("TDL-G06-TRIP-TIME-ORDER-REVIEW","### stop_times.txt","TDL_REVIEW_MARKER","Diagnóstico temporal pendiente de criterio aprobado; nunca convertir su no evaluación en PASS.","time_review"),
 ("GTFS-G07-COORDINATE-BOUNDS","### shapes.txt","FORMAT_REQUIRED","Latitud y longitud de puntos están dentro de sus dominios numéricos.","coordinate"),
 ("GTFS-G07-DISTANCE-PROGRESSION","shape_dist_traveled","FORMAT_REQUIRED_IF_SUPPLIED","Las distancias informadas aumentan con la secuencia; puntos coincidentes no autorizan distancias iguales.","distance"),
 ("GTFS-G07-SHAPE-SEQUENCE","shape_pt_sequence","FORMAT_REQUIRED","La secuencia de puntos de un trazado aumenta; puede tener saltos.","shape_sequence"),
 ("GTFS-G08-FEED-END-DATE-DECLARED","feed_end_date","RECOMMENDATION","Declaración del encabezado recomendado; no valida el valor ni convierte omisión en fallo técnico.","recommend_end"),
 ("GTFS-G08-FEED-START-DATE-DECLARED","feed_start_date","RECOMMENDATION","Declaración del encabezado recomendado; valor vacío no es encabezado ausente.","recommend_start"),
 ("GTFS-G08-FEED-VERSION-DECLARED","feed_version","RECOMMENDATION","Declaración del encabezado recomendado de versión; no verifica exactitud de la versión.","recommend_version"),
 ("V1-RULE-GTFS","### stop_times.txt","BOUNDED_TECHNICAL_PARTIAL_COMPLIANCE","Referencia de stop_id en horario fijo a una parada/plataforma válida; alcance parcial sin conclusión jurídica.","stop_ref"),
 ("GTFS-COORDINATE-RANGE","### stops.txt","FORMAT_REQUIRED","Coordenadas de parada dentro de los dominios latitud/longitud.","stop_coordinate"),
 ("GTFS-REF-SERVICE","### trips.txt","FORMAT_REQUIRED","Referencia de servicio existente; control legacy separado sin duplicar eventos.","service_ref"),
 ("GTFS-REF-SHAPE","shape_id","FORMAT_REQUIRED_IF_SUPPLIED","La referencia de trazado informada identifica un trazado existente.","shape_ref"),
 ("GTFS-REF-TRIP-ROUTE","route_id","FORMAT_REQUIRED","El viaje referencia una línea existente.","route_ref"),
 ("GTFS-STRUCT-REQUIRED","## Dataset Files","FORMAT_REQUIRED","Un horario fijo requiere los archivos base aplicables, incluida agencia.","agency_presence"),
 ("GTFS-STRUCT-SERVICE-CALENDAR","## Dataset Files","FORMAT_CONDITIONAL","Servicio definido mediante calendar o calendar_dates; no es obligatorio disponer de ambos.","calendar_presence"),
 ("GTFS-UNIQUE-PRIMARY-ID","Primary key","FORMAT_REQUIRED","Un identificador primario de parada es único.","unique"),
]


def case_data(kind, variant):
    """Authored mutations; expected results below are not evaluated from them."""
    data = deepcopy(BASE); context = {}; raw = {}
    negative = variant == "negative"; edge = variant == "boundary"
    def put(file, field, value, index=0): data[file][index][field] = value
    if kind == "csv":
        if negative: raw["routes.txt"] = 'route_id,route_short_name,route_type\nR,"unterminated,3\n'
        if edge: put("routes.txt","route_long_name",'Línea con "comillas", coma y ñ')
    elif kind == "color": put("routes.txt","route_text_color"," " if negative else "" if edge else "00aAfF")
    elif kind == "catalog":
        if negative: raw["operator_extension.txt"] = "custom_id\nX\n"
        if edge: data.pop("shapes.txt"); put("trips.txt","shape_id","")
    elif kind == "calendar_presence":
        if negative: data.pop("calendar.txt")
        if edge:
            data.pop("calendar.txt"); data["calendar_dates.txt"]=[{"service_id":"S","date":"20261009","exception_type":"1"}]
    elif kind == "networks":
        if negative: put("routes.txt","network_id","N")
        if not edge: data["networks.txt"]=[{"network_id":"N","network_name":"Synthetic network"}]
        else: put("routes.txt","network_id","N")
    elif kind == "header":
        if negative:
            data["agency.txt"].append({**data["agency.txt"][0],"agency_id":"AG2"}); data["routes.txt"][0].pop("agency_id")
        elif edge: data["routes.txt"][0].pop("agency_id")
    elif kind == "translation":
        if not edge: data["translations.txt"]=[{"table_name":"stops","field_name":"stop_name","language":"en","translation":"Synthetic stop","record_id":"MISSING" if negative else "ST1"}]
    elif kind == "service_ref":
        if negative: put("trips.txt","service_id","MISSING")
        if edge:
            data.pop("calendar.txt"); data["calendar_dates.txt"]=[{"service_id":"S","date":"20261009","exception_type":"1"}]
    elif kind == "unique":
        if negative: put("stops.txt","stop_id","ST1",1)
        if edge: put("stops.txt","stop_id","st1",1); put("stop_times.txt","stop_id","st1",1)
    elif kind == "parent":
        if negative: put("stops.txt","parent_station"," ")
        elif not edge: data["stops.txt"].append({"stop_id":"P","stop_name":"Synthetic station","stop_lat":"41","stop_lon":"2","location_type":"1","parent_station":""}); put("stops.txt","parent_station","P")
    elif kind in {"calendar_range","feed_range"}:
        f="calendar.txt" if kind=="calendar_range" else "feed_info.txt"; start="start_date" if f=="calendar.txt" else "feed_start_date"; end="end_date" if f=="calendar.txt" else "feed_end_date"
        if negative: put(f,start,"20261101")
        if edge: put(f,end,data[f][0][start])
    elif kind in {"frequency_range","frequency_end"}:
        data["frequencies.txt"]=[{"trip_id":"T","start_time":"08:00:00","end_time":"09:09:59","headway_secs":"600","exact_times":"1"}]
        if kind=="frequency_range":
            if negative: put("frequencies.txt","end_time","07:59:59")
            if edge: put("frequencies.txt","start_time","24:00:00");put("frequencies.txt","end_time","25:00:00")
        else:
            context["last_desired_departure"]="09:00:00"
            if negative: put("frequencies.txt","end_time","09:10:00")
            if edge: put("frequencies.txt","end_time","09:00:01")
    elif kind == "service_dates":
        data.pop("calendar.txt"); data["calendar_dates.txt"]=[{"service_id":"S","date":"20261009","exception_type":"2" if negative else "1"}]
        if edge: data["calendar_dates.txt"].append({"service_id":"S","date":"20261010","exception_type":"1"})
    elif kind in {"window_review","time_review"}:
        context["approved_criterion_available"] = False
        if kind=="window_review" and not edge:
            for i in range(2): put("stop_times.txt","start_pickup_drop_off_window","09:00:00",i);put("stop_times.txt","end_pickup_drop_off_window","08:00:00" if negative else "10:00:00",i)
        elif kind=="time_review" and negative: put("stop_times.txt","arrival_time","23:00:00",1)
    elif kind in {"coordinate","stop_coordinate"}:
        f="shapes.txt" if kind=="coordinate" else "stops.txt"; field="shape_pt_lat" if f=="shapes.txt" else "stop_lat"
        if negative: put(f,field,"90.0001")
        if edge: put(f,field,"90");put(f,"shape_pt_lon" if f=="shapes.txt" else "stop_lon","-180")
    elif kind == "distance":
        if negative: put("shapes.txt","shape_dist_traveled","0",1)
        if edge:
            for row in data["shapes.txt"]: row.pop("shape_dist_traveled")
    elif kind in {"stop_sequence","shape_sequence"}:
        f="stop_times.txt" if kind=="stop_sequence" else "shapes.txt"; field="stop_sequence" if kind=="stop_sequence" else "shape_pt_sequence"
        if negative: put(f,field,"1",1)
        if edge: put(f,field,"99",1)
    elif kind.startswith("recommend_"):
        field={"recommend_start":"feed_start_date","recommend_end":"feed_end_date","recommend_version":"feed_version"}[kind]
        if negative: data["feed_info.txt"][0].pop(field)
        if edge: put("feed_info.txt",field,"")
    elif kind == "stop_ref":
        if negative: put("stop_times.txt","stop_id","MISSING")
        if edge: put("stops.txt","location_type","1")
    elif kind == "shape_ref": put("trips.txt","shape_id"," " if negative else "" if edge else "SH")
    elif kind == "route_ref":
        if negative: put("trips.txt","route_id","MISSING")
        if edge: put("routes.txt","route_id","r");put("trips.txt","route_id","r")
    elif kind == "agency_presence":
        if negative: data.pop("agency.txt")
        if edge: data["agency.txt"][0].pop("agency_id")
    else: raise ValueError("Unknown case family: "+kind)
    return data, raw, context


def expectation(kind, variant):
    negative=variant=="negative"; edge=variant=="boundary"
    state="VIOLATED" if negative else "SATISFIED"; status="FAIL_TECHNICAL" if negative else "PASS"
    notes = "El caso ilustra un criterio concreto; no predice el resultado agregado de todas las reglas."
    extras={}
    if kind.startswith("recommend_"):
        state="RECOMMENDATION_UNMET" if negative else "SATISFIED"; status="PASS"; extras["recommendation_met"]=not negative
        notes="La omisión es informativa. La variante límite declara el encabezado con valor vacío; evaluar solo presencia."
    if kind=="catalog" and negative: state="REVIEW_REQUIRED";status="HUMAN_REVIEW_REQUIRED";notes="Extensión sin política acordada: no inventar una prohibición GTFS. Puede diferir de la proyección técnica del motor."
    if kind=="translation" and edge: state="NOT_APPLICABLE";status="NOT_APPLICABLE"
    if kind=="distance" and edge: state="NOT_APPLICABLE";status="NOT_APPLICABLE"
    if kind=="service_dates" and negative: state="REVIEW_REQUIRED";status="HUMAN_REVIEW_REQUIRED";notes="Solo existe una exclusión y ninguna fecha efectiva. Se conoce el conjunto vacío, pero falta criterio para atribuir obligación incumplida."
    if kind in {"window_review","time_review"}:
        state="UNKNOWN";status="NOT_EVALUABLE";notes="No hay criterio aprobado completo para este diagnóstico. Incluso datos aparentemente ordenados no autorizan PASS."
        if kind=="window_review" and edge: state="NOT_APPLICABLE";status="NOT_APPLICABLE"
    if kind=="stop_ref" and edge: state="VIOLATED";status="FAIL_TECHNICAL";notes="Una estación tipo 1 no es una parada/plataforma admisible para este horario fijo."
    return {"criterion_state":state,"criterion_status":status,"explanation":notes,"details":extras,
            "aggregate_feed_status": "NOT_PREDICTED", "engine_observed_status": None}


RATIONALES = {
 "csv": ["CSV bien escapado y con encabezado.","Comilla de apertura sin cierre: el registro no puede interpretarse como CSV válido.","Comas, comillas y caracteres UTF-8 escapados por el escritor CSV son aceptables."],
 "color": ["00aAfF tiene seis caracteres hexadecimales.","Un espacio no cumple seis dígitos y no es vacío.","Vacío en un campo opcional no exige un color informado."],
 "catalog": ["Solo archivos reconocidos.","Archivo adicional sin política de extensiones: revisión, no prohibición normativa inventada.","Sin shapes ni referencia/recogida continua; no forzar obligatoriedad."],
 "calendar_presence": ["calendar aporta servicio S.","Faltan calendar y calendar_dates: no hay fuente de fechas de servicio.","calendar_dates aporta una fecha añadida de S; calendar puede omitirse."],
 "networks": ["networks presente y network_id ausente en routes.","networks y routes.network_id coexisten, combinación prohibida.","routes.network_id presente y networks ausente, sin combinación prohibida."],
 "header": ["Una agencia y rutas con agency_id declarado.","Dos agencias y encabezado agency_id ausente en routes: condición requerida incumplida.","Una agencia y agency_id ausente en routes: condición no exige ese encabezado."],
 "translation": ["record_id ST1 existe en stops.","record_id MISSING no existe en stops.","translations ausente; no hay traducción que inspeccionar."],
 "service_ref": ["S existe en calendar.","El viaje usa MISSING y las fuentes solo contienen S.","S existe únicamente en calendar_dates; la unión del dominio lo resuelve."],
 "unique": ["ST1 y ST2 son distintos.","Dos filas usan ST1 como clave primaria.","ST1 y st1 son distintos con comparación sensible a mayúsculas."],
 "parent": ["P existe y es estación tipo 1.","El espacio informado no identifica ninguna estación.","Campo vacío en parada tipo 0: relación opcional."],
 "calendar_range": ["1 de octubre precede a 31 de octubre.","1 de noviembre sigue a 31 de octubre.","Fechas iguales describen un rango de un día."],
 "feed_range": ["Las fechas informadas están ordenadas.","La fecha inicial informada es posterior a la final.","Fechas iguales no implican inversión del rango."],
 "frequency_range": ["08:00 precede a 09:09:59.","07:59:59 precede al comienzo 08:00.","24:00 y 25:00 son horas extendidas ordenadas, no un cambio de día que se reinicia a cero."],
 "frequency_end": ["09:00 < 09:09:59 < 09:10 para última salida deseada 09:00 y headway 600.","Fin igual a última salida más headway incumple la cota estricta.","Fin un segundo después de la última salida cumple ambas cotas; no es una receta de corrección para operadores."],
 "service_dates": ["Excepción tipo 1 añade 9 de octubre a S.","Solo una exclusión tipo 2 deja conjunto vacío; revisar alcance y uso antes de declarar infracción.","Dos adiciones forman un conjunto efectivo de dos fechas."],
 "window_review": ["Ventana ordenada pero criterio de este diagnóstico aún no aprobado.","Ventana invertida; registrar revisión sin inventar autoridad normativa del marcador.","Campos de ventana ausentes: feature no presente."],
 "time_review": ["Horas extendidas ordenadas, pero el marcador carece de decisión de autoridad aprobada.","La llegada posterior retrocede; problema candidato con criterio pendiente, no nuevo fallo normativo automático.","No convertir datos aparentemente correctos en PASS de un control no implementado."],
 "coordinate": ["41 y 2 dentro de los dominios de latitud/longitud.","90.0001 excede la latitud máxima 90.","90 y -180 coinciden con límites admitidos."],
 "stop_coordinate": ["Coordenadas de parada dentro de sus dominios.","Latitud de parada 90.0001 fuera de dominio.","Latitud 90 y longitud -180 en límites admitidos."],
 "distance": ["Distancias 0 y 100 aumentan con la secuencia.","Distancias 0 y 0 entre puntos diferentes no aumentan.","Sin encabezado de distancia opcional: no comparar valores inexistentes."],
 "stop_sequence": ["Secuencia 1 y 3 aumenta.","Secuencia 1 y 1 repite una clave por viaje.","Secuencia 1 y 99 aumenta; los valores no necesitan ser consecutivos."],
 "shape_sequence": ["Secuencia de puntos 1 y 3 aumenta.","Secuencia 1 y 1 repite clave por trazado.","Secuencia 1 y 99 aumenta; los saltos son aceptables."],
 "recommend_start": ["Encabezado recomendado presente.","Encabezado recomendado ausente: información, no fallo técnico.","Encabezado presente con valor vacío; G08 solo declara presencia."],
 "recommend_end": ["Encabezado recomendado presente.","Encabezado recomendado ausente: información, no fallo técnico.","Encabezado presente con valor vacío; el valor es otro ámbito de evaluación."],
 "recommend_version": ["Encabezado recomendado presente.","Encabezado recomendado ausente: información, no fallo técnico.","Encabezado presente con valor vacío; no acredita la exactitud de una versión."],
 "stop_ref": ["Horario referencia ST1/ST2 de tipo 0.","Horario referencia un identificador inexistente.","Horario fijo referencia ST1 cambiado a estación tipo 1, no parada/plataforma."],
 "shape_ref": ["SH existe en shapes.","Un espacio no identifica SH ni ningún otro trazado.","Referencia vacía, sin recogida/bajada continua: no inventar relación obligatoria."],
 "route_ref": ["R existe en routes.","MISSING no existe en routes.","r coincide exactamente entre viaje y routes; no normalizar identidades."],
 "agency_presence": ["agency presente.","agency ausente: archivo requerido para este horario fijo.","Una agencia puede omitir agency_id; la prueba de presencia de archivo no juzga otras referencias."],
}
