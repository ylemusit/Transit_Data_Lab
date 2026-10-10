# Guía de documentación de los archivos GTFS Schedule

**Propósito:** servir como especificación de trabajo para construir y revisar un GTFS ficticio de transporte terrestre. Describe los 32 archivos definidos por la referencia GTFS Schedule vigente consultada el 9 de octubre de 2026: qué representa cada uno, formato y presencia, relaciones, origen operativo habitual y controles de calidad.

**Límite importante:** “cumplir GTFS” significa respetar la estructura y las reglas técnicas publicadas por GTFS. No demuestra por sí solo que un operador tenga autorización para prestar un servicio, que los datos sean ciertos, que la tarifa sea legal ni que una Administración o el Punto de Acceso Nacional (NAP) haya aceptado la publicación. En una simulación, los datos deben etiquetarse claramente como ficticios y no atribuirse a un operador, concesión o localidad real como si fueran datos oficiales.

## 1. Cómo leer esta guía

- **Obligatorio:** el archivo o campo debe estar presente en las condiciones indicadas por GTFS.
- **Condicional:** se exige solo cuando se da una circunstancia concreta; se explica en cada caso.
- **Opcional:** GTFS permite omitirlo. “Opcional” no quiere decir irrelevante cuando la red o el servicio sí usa esa función.
- **Prohibido condicionalmente:** no debe aparecer junto a determinada alternativa del esquema.
- **Origen habitual** describe prácticas comunes de las empresas; GTFS no obliga a usar un sistema informático o departamento específico. Para un feed ficticio, la fuente debe anotarse como dato sintético, con método y supuestos.

La referencia técnica manda para el encabezado exacto, los valores enumerados, la presencia por campo y las excepciones. Esta guía resume esos requisitos y ofrece contexto de producción; no sustituye la tabla de campos de la referencia.

## 2. Reglas comunes del paquete

1. El ZIP contiene los archivos directamente en su raíz, con los nombres oficiales exactos. No se añade una carpeta envolvente ni archivos de trabajo como Excel. Evita columnas propias dentro de las tablas normalizadas: los consumidores pueden ignorarlas o interpretarlas de forma incompatible.
2. Los archivos tabulares son texto CSV UTF-8, separados por comas, con una primera fila de encabezados exactos y sensibles a mayúsculas/minúsculas. Cada fila debe tener el número correcto de columnas; los valores con comas, comillas o saltos de línea se escapan conforme a CSV. Las celdas vacías se dejan vacías, no se rellenan con textos como “N/A” salvo que lo indique la definición del campo.
3. locations.geojson es GeoJSON según el subconjunto GTFS y RFC 7946. No es CSV.
4. Los identificadores son claves internas estables: deben ser únicos donde corresponda, no reutilizarse para otra entidad y conservarse entre publicaciones mientras la entidad siga siendo la misma. No se deben usar como texto visible para viajeros.
5. Las fechas usan AAAAMMDD. Las horas de horarios usan HH:MM:SS y pueden superar las 24:00:00 para viajes que continúan después de medianoche dentro del mismo día de servicio. No se deben convertir sin más a la fecha civil siguiente. Las coordenadas GTFS tabulares son latitud/longitud WGS84 en grados decimales.
6. Mantener un registro de procedencia separado del ZIP: archivo/campo, fuente documental o sistema, responsable, fecha de extracción, transformación aplicada, unidad, licencia, aprobación y si el dato es real o sintético. Los archivos GTFS no tienen una columna estándar de procedencia por fila; añadir columnas propias puede romper consumidores.
7. Antes de publicar, comprobar relaciones entre identificadores, continuidad de horarios, coherencia espacial, fechas vigentes, validez CSV/GeoJSON y ausencia de información de prueba que pueda confundirse con datos reales. Como práctica de publicación, la referencia recomienda mantener el feed vigente al menos los próximos siete días, idealmente más tiempo y, si es posible, treinta días; retirar calendarios caducados. Validar técnicamente no es una aprobación jurídica.

## 3. Archivos, uno por uno

### 1. agency.txt — operadores o agencias

**Función y formato:** identifica a las agencias responsables de los servicios descritos. CSV. Es obligatorio. Campos obligatorios: agency_name, agency_url y agency_timezone. agency_id es obligatorio cuando hay varias agencias; con una sola, puede omitirse aunque se recomienda. Si hay varias agencias, todas deben tener el mismo agency_timezone. Los demás datos de contacto, idioma, moneda, colores, atributos tarifarios o accesibilidad se incluyen solo si aplican y según la referencia vigente.

**Origen habitual:** registro maestro de operadores, contrato o concesión, web oficial y configuración del sistema de planificación/publicación. El nombre y la URL visibles deberían coincidir con la identidad pública autorizada; la zona horaria debe ser una zona IANA válida del servicio. En un ejercicio ficticio, usar una entidad inventada y un dominio reservado o claramente no operativo.

**Documentación y controles:** registrar quién es el operador del dato frente a quién produce el feed; no confundir autoridad de transporte, concesionario y proveedor tecnológico. Verificar que todas las rutas apuntan a una agencia existente si se usan varias, URL completa y zona horaria consistente con el servicio.

### 2. stops.txt — paradas, estaciones y puntos de acceso

**Función y formato:** catálogo de ubicaciones de embarque y desembarque, estaciones, entradas, nodos interiores y áreas de embarque. CSV. Condicionalmente obligatorio: se exige normalmente; puede omitirse si el servicio bajo demanda está descrito mediante zonas GeoJSON. stop_id es obligatorio y único incluso frente a los IDs de locations.geojson y location_groups.txt. stop_name, stop_lat y stop_lon son obligatorios para paradas/plataformas, estaciones y entradas; son opcionales para nodos genéricos y zonas de embarque. location_type, parent_station, códigos, zona, accesibilidad, nivel y propiedades para demanda se añaden cuando corresponda.

**Origen habitual:** inventario de paradas del operador/autoridad, GIS corporativo, catastro o cartografía oficial, inspección de campo y sistema de activos de estaciones. Las coordenadas suelen salir de levantamiento GPS/GNSS, GIS o cartografía revisada; los nombres, de nomenclátor oficial y señalización. La cartografía no confirma por sí sola que una parada exista u opere.

**Documentación y controles:** guardar evidencia de nombre oficial, ubicación, fecha de comprobación, tipo de punto y fuente de accesibilidad. Verificar IDs únicos, relaciones padre-hijo válidas, coordenadas plausibles, jerarquía de estación coherente y que una estación no se use como si fuera plataforma cuando el modelo requiere paradas hijas. No inferir que una estación es accesible por tener ascensor en otro punto.

### 3. routes.txt — líneas o servicios comerciales

**Función y formato:** agrupa viajes que se presentan al público como una misma línea o servicio. CSV. Obligatorio: route_id único, route_type y al menos route_short_name o route_long_name. agency_id es condicionalmente obligatorio cuando hay varias agencias y recomendado en caso contrario. Colores, texto, descripción, URL y atributos de pago/accesibilidad solo si están sustentados.

**Origen habitual:** catálogo de líneas comerciales aprobado por operador o autoridad, sistema de planificación de oferta y material oficial para pasajeros. route_type debe representar el modo real (por ejemplo, autobús urbano/interurbano según la clasificación aplicable), no el nombre comercial.

**Documentación y controles:** enlazar cada ruta a una ficha de servicio y a su autoridad/operador; conservar la fuente de nombre, modo, colores y vigencia. Comprobar que toda ruta tiene viajes en trips.txt, que los nombres son legibles y que no se crean líneas para representar cada salida individual.

### 4. trips.txt — viajes programados

**Función y formato:** cada registro representa un viaje concreto de una ruta en uno o varios días de servicio. CSV. Obligatorios: route_id, service_id y trip_id. shape_id es obligatorio si el viaje hereda comportamiento de parada continua en ruta; en caso contrario es opcional en la tabla, aunque las formas deben estar disponibles para los servicios basados en rutas. El resto (destino mostrado, dirección, bloque, accesibilidad, bicicletas, calendario ampliado, servicio flexible, etc.) es opcional o condicional según el modelo usado.

**Origen habitual:** sistema de planificación de horarios (HASTUS, Trapeze u otro), tablas de marcha, programación de vehículos o exportación del sistema corporativo de gestión de oferta. A menudo el proveedor GTFS transforma esos datos a IDs y registros normalizados.

**Documentación y controles:** conservar el documento/versión de horario que autoriza cada viaje y la regla con que se asignó service_id. Validar referencias a rutas, calendarios y shapes; evitar trip_id duplicados; distinguir viajes diferentes aunque compartan ruta y recorrido; revisar orientación/destino y atributos especiales contra la ficha oficial.

### 5. stop_times.txt — secuencia y horario por parada

**Función y formato:** indica el paso de cada viaje por sus ubicaciones, en orden. CSV. Obligatorios por fila: trip_id y stop_sequence; además, se indica exactamente la ubicación aplicable mediante stop_id, location_group_id o location_id. arrival_time es obligatorio en la primera y última parada y cuando timepoint=1; departure_time es obligatorio cuando timepoint=1. Ambos tiempos están prohibidos si se define una ventana start_pickup_drop_off_window/end_pickup_drop_off_window y son opcionales en los demás casos. stop_sequence debe aumentar dentro del viaje; no tiene que ser consecutivo. Los campos de recogida, bajada, ventana, reserva y timepoint son condicionales según la modalidad.

**Origen habitual:** cuadro horario publicado, tablas de marcha de explotación, tiempos de recorrido planificados y, como contraste, históricos de AVL/GPS o mediciones de campo. Los datos históricos pueden ayudar a estimar tiempos, pero no sustituyen el horario aprobado.

**Documentación y controles:** dejar constancia de la versión de horario y método de estimación de cada tiempo. Comprobar que stop_sequence aumenta, las horas no retroceden sin justificación, los tiempos respetan el sentido del viaje, las paradas existen y el primer/último punto tienen tiempos compatibles con las reglas. Usar >24:00:00 para continuidad nocturna del día de servicio.

### 6. calendar.txt — calendario semanal de servicios

**Función y formato:** define días de la semana activos y el rango de vigencia de un service_id. CSV. Condicionalmente obligatorio: debe estar presente salvo que calendar_dates.txt enumere todas las fechas de servicio. Los campos de servicio incluyen service_id, los siete indicadores de día y start_date/end_date.

**Origen habitual:** calendario oficial de explotación, calendario escolar/laboral, programación de temporada y acuerdos de días festivos del operador o autoridad.

**Documentación y controles:** conservar el calendario que aprueba cada patrón; revisar el rango de fechas, los días activos, festivos y cambios de temporada. Todo service_id de trips.txt debe resolverse en calendar.txt o calendar_dates.txt y producir el conjunto de fechas esperado.

### 7. calendar_dates.txt — excepciones de calendario

**Función y formato:** añade o elimina una fecha concreta de un patrón de servicio. CSV. Condicionalmente obligatorio si no existe calendar.txt; en tal caso debe enumerar todas las fechas en que opera cada servicio. Si coexisten ambos archivos, contiene excepciones y requiere service_id, date y exception_type válidos.

**Origen habitual:** calendario de festivos, avisos de servicio especial, calendarios escolares, resoluciones de la autoridad y programación de eventos.

**Documentación y controles:** guardar referencia y motivo de cada excepción; detectar duplicados de servicio/fecha, tipo de excepción incorrecto, fechas fuera del horizonte, servicios sin viajes y festivos no reflejados. Las excepciones deben seguir la regla de precedencia de la especificación.

### 8. fare_attributes.txt — tarifas GTFS Fares V1

**Función y formato:** describe productos tarifarios del modelo antiguo Fares V1. CSV, opcional. Incluye fare_id, precio, moneda ISO 4217, método de pago y política de transbordos; agencia y duración son condicionales o complementarias. Se relaciona con fare_rules.txt.

**Origen habitual:** tablas oficiales de tarifas, ordenanzas o resoluciones, sistema de venta y validación, y fichas comerciales vigentes.

**Documentación y controles:** cada precio y condición debe enlazarse a su disposición o tarifario oficial y a su fecha de validez. Verificar códigos de moneda, importes decimales y lógica de transbordos. No mezclar tarifas inventadas con reales ni presentar una tarifa ficticia como vigente. GTFS permite el modelo, no valida la legalidad del precio.

### 9. fare_rules.txt — aplicación de tarifas V1

**Función y formato:** relaciona un fare_id con rutas, zonas de origen/destino o zonas atravesadas. CSV, opcional; fare_id es obligatorio. route_id, origin_id, destination_id y contains_id son selectores opcionales y pueden dejarse vacíos cuando no correspondan. Depende de fare_attributes.txt y de las zonas configuradas.

**Origen habitual:** matriz tarifaria por zonas, reglas de venta, definición de coronas tarifarias y condiciones publicadas de los títulos.

**Documentación y controles:** documentar qué regla comercial implementa cada combinación; asegurar que IDs de tarifa, rutas y zonas existen y que las reglas no se contradicen. Si la estructura requiere más precisión (productos, medios de pago, categorías, tramos y transbordos), valorar Fares V2; no duplicar modelos incompatibles sin probar qué interpreta el consumidor.

### 10. timeframes.txt — franjas de vigencia horaria

**Función y formato:** define grupos de franjas horarias y días en los que se aplican, sobre todo para reglas tarifarias que cambian por hora/día. CSV, opcional. Obligatorios: timeframe_group_id y service_id; start_time/end_time son un par condicional y expresan el intervalo local, con inicio incluido y fin excluido.

**Origen habitual:** tarifario aprobado con horas punta/valle, calendario de fin de semana o reglas horarias del sistema de venta.

**Documentación y controles:** anotar zona horaria que gobierna el evento y la fuente normativa/comercial. Evitar huecos y solapes involuntarios, horas mayores de 24:00 y referencias a servicios inexistentes. La semántica de días se calcula según la hora local correspondiente al evento tarifario.

### 11. rider_categories.txt — categorías de viajeros

**Función y formato:** define categorías aplicables a productos, como tarifa general, joven o sénior. CSV, opcional. Obligatorios: rider_category_id, rider_category_name e is_default_fare_category. La elegibilidad no se especifica por completo aquí: se relaciona con productos de tarifa y sus condiciones.

**Origen habitual:** catálogo de títulos y perfiles tarifarios, condiciones de venta y documentación de descuentos aprobados. La empresa suele normalizar nombres de producto del sistema de ticketing.

**Documentación y controles:** usar nombres entendibles y respaldados por condiciones publicadas; identificar de forma consistente cuál es la categoría general. Si un producto admite varias categorías de viajeros, exactamente una de ellas debe marcarse como predeterminada. No incorporar datos personales, números de tarjetas ni criterios de elegibilidad que el esquema no pide. Verificar referencias desde productos.

### 12. fare_media.txt — medio de pago o validación

**Función y formato:** describe el soporte utilizado para adquirir/validar un producto: efectivo sin soporte, billete papel, tarjeta física, cEMV o aplicación móvil, según los valores permitidos por la referencia. CSV, opcional. fare_media_id y fare_media_type son obligatorios; fare_media_name es obligatorio para tarjeta de transporte física o app móvil.

**Origen habitual:** inventario de canales de venta y validación, documentación de ticketing, proveedores de pago y catálogo comercial.

**Documentación y controles:** reflejar medios disponibles para ese producto y operador, no solo medios técnicamente posibles. Confirmar etiquetas oficiales y relación con fare_products.txt. La presencia del medio no demuestra que el canal acepte una tarjeta concreta ni que funcione en toda la red.

### 13. fare_products.txt — títulos o productos tarifarios V2

**Función y formato:** modela los productos que compra o utiliza el pasajero y el precio por medio/categoría. CSV, opcional. fare_product_id, amount y currency son obligatorios; rider_category_id y fare_media_id son opcionales y, si se usan, deben existir en sus tablas. Puede haber varias filas con el mismo fare_product_id si cambia el medio o la categoría. Se enlaza a las reglas que determinan en qué viaje se aplica.

**Origen habitual:** maestro de títulos del sistema de venta, tarifas publicadas, configuración del sistema central de ticketing y resoluciones vigentes.

**Documentación y controles:** registrar nombre/composición, periodo de venta y viaje, precio y moneda en un inventario de apoyo; GTFS no contiene toda la ficha comercial/legal del título. Verificar formato decimal monetario, IDs referenciados, productos gratuitos/descuentos y consistencia con condiciones oficiales.

### 14. fare_leg_rules.txt — reglas para cobrar cada tramo

**Función y formato:** asigna productos a un tramo según red, área de origen/destino y franjas horarias. CSV, opcional. fare_product_id es obligatorio y apunta a fare_products.txt. network_id, from_area_id, to_area_id, from_timeframe_group_id y to_timeframe_group_id son selectores opcionales; su semántica cambia si se usa rule_priority. leg_group_id y rule_priority se emplean cuando hacen falta grupos de transferencia o prioridades.

**Origen habitual:** motor de tarifas, matriz de origen-destino, zonas y reglas de validación del sistema de ticketing.

**Documentación y controles:** mantener una matriz de decisión revisable, incluidos valores vacíos y prioridades; demostrar para ejemplos de viaje qué regla aplica y qué precio resulta. Comprobar IDs de red, área, franjas y producto. Es fácil producir reglas técnicamente válidas pero con ambigüedad tarifaria.

### 15. fare_leg_join_rules.txt — combinación de tramos

**Función y formato:** especifica cuándo dos tramos consecutivos se tratan como un solo tramo tarifario efectivo para buscar reglas de fare_leg_rules.txt. CSV, opcional. from_network_id y to_network_id son obligatorios y deben indicar respectivamente la red del tramo anterior y posterior. from_stop_id y to_stop_id son condicionales: si se indica uno, debe indicarse el otro; ambos deben identificar la estación/parada del intercambio. Las reglas de coincidencia de la especificación determinan el alcance de los campos vacíos.

**Origen habitual:** reglas de integración tarifaria entre operadores, productos que cubren varias etapas y lógica del motor de tarifas.

**Documentación y controles:** vincular cada combinación con la condición comercial de transbordo o continuidad que la autoriza. Comprobar que los grupos y redes referenciados existen y probar viajes con uno y varios tramos, en ambos sentidos cuando las reglas sean direccionales.

### 16. fare_transfer_rules.txt — tarifa de los transbordos

**Función y formato:** define las consecuencias de tarifa al cambiar entre grupos de tramos: producto adicional, coste, número de transbordos o límites aplicables. CSV, opcional. fare_transfer_type es obligatorio. from_leg_group_id y to_leg_group_id seleccionan los grupos y fare_product_id es opcional. transfer_count es obligatorio cuando ambos grupos son iguales y está prohibido si son distintos; duration_limit_type es obligatorio si se define duration_limit. Se apoya en fare_leg_rules.txt y fare_products.txt; una regla de A a B no implica automáticamente la regla inversa.

**Origen habitual:** condiciones de integración y transbordo, sistema central de ticketing, acuerdos entre operadores y reglas de compensación.

**Documentación y controles:** conservar el acuerdo/fuente, ventana temporal y trayectos cubiertos. Verificar direccionalidad, contadores, productos y comportamiento del motor para cadenas de más de dos tramos. Contrastar el coste calculado con ejemplos publicados.

### 17. areas.txt — zonas para tarifas

**Función y formato:** declara las áreas tarifarias usadas por Fares V2. CSV, opcional. area_id es obligatorio y único; area_name es opcional. La pertenencia de paradas se establece en stop_areas.txt.

**Origen habitual:** zonificación oficial, planos tarifarios y tablas de la autoridad de transporte.

**Documentación y controles:** adjuntar mapa/tabla que define cada zona y fecha de validez; comprobar nombres, IDs y que la zona no se confunda con un límite municipal o geográfico distinto. Las áreas de tarifa no son automáticamente polígonos: se asignan a paradas.

### 18. stop_areas.txt — asignación de paradas a zonas

**Función y formato:** asigna ubicaciones de stops.txt a las áreas de areas.txt. CSV, opcional. Cada fila requiere area_id y stop_id; la misma parada puede pertenecer a varias áreas según el modelo.

**Origen habitual:** cruce entre inventario de paradas georreferenciado y zonificación tarifaria aprobado por la autoridad/operador.

**Documentación y controles:** conservar la regla de asignación, mapa y versión; verificar referencias existentes y estaciones con plataformas. Revisar paradas fronterizas y cambios de zona para que el resultado coincida con la regla de cobro real.

### 19. networks.txt — redes tarifarias

**Función y formato:** declara redes empleadas por reglas de tramo tarifario. CSV, condicionalmente prohibido: no se incluye si routes.txt tiene network_id ni si se usan route_networks.txt/networks.txt junto a ese campo. Si se utiliza esta tabla, network_id es obligatorio y único; network_name es opcional. El campo routes.network_id y las tablas networks.txt/route_networks.txt son alternativas excluyentes según la referencia.

**Origen habitual:** definición de operadores/redes dentro de una integración tarifaria y del sistema de venta.

**Documentación y controles:** describir qué líneas y servicios pertenecen a cada red y quién lo aprobó. Escoger un único patrón de asociación: network_id en routes.txt o asociación mediante route_networks.txt; nunca mezclar la tabla networks con el campo network_id en routes, según la prohibición del estándar.

### 20. route_networks.txt — asignación de rutas a redes

**Función y formato:** asigna cada route_id a network_id. CSV, opcional salvo que el modelo tarifario necesite redes; condicionalmente prohibido si routes.txt contiene network_id. Ambos campos son obligatorios y forman la asociación. network_id debe existir en networks.txt y route_id en routes.txt.

**Origen habitual:** catálogo de rutas y pertenencia a redes tarifarias u operadores dentro de un sistema integrado.

**Documentación y controles:** comprobar que ruta y red existen, que cada ruta pertenece a la red prevista y que no se intenta representar en esta tabla más de una red por ruta cuando el esquema lo prohíbe. Registrar excepciones intermodales en el sistema maestro.

### 21. shapes.txt — trazado geográfico de los recorridos

**Función y formato:** secuencia ordenada de puntos que representa el itinerario del vehículo. CSV. La referencia lista el archivo como opcional, pero indica que debe incluirse para servicios basados en rutas; no aplica a servicios a demanda basados en zonas. Obligatorios por punto: shape_id, shape_pt_lat, shape_pt_lon y shape_pt_sequence. Los viajes la enlazan mediante shape_id.

**Origen habitual:** GIS de red vial, CAD, cartografía de rutas, trazas GPS de vehículos y edición manual validada contra el recorrido aprobado. Un GPS histórico debe depurarse de desvíos y ruido.

**Documentación y controles:** guardar fuente cartográfica, fecha, método de digitalización y CRS de origen. Revisar visualmente el sentido, continuidad, desvíos, puentes y proximidad entre línea y paradas; convertir con cuidado a WGS84. Los shape_id usados en trips deben existir y la secuencia debe ser creciente.

### 22. frequencies.txt — servicios definidos por intervalo

**Función y formato:** representa salidas cada intervalo dentro de una ventana o comprime horarios repetitivos. CSV, opcional. Requiere trip_id, start_time, end_time y headway_secs; exact_times indica el tratamiento del horario conforme a los valores del esquema. No es una lista de salidas individuales cuando la oferta es frecuencia aproximada.

**Origen habitual:** plan de oferta por frecuencia, despacho, planificación de flota y horario comercial.

**Documentación y controles:** conservar la ventana y el intervalo aprobados; comprobar start < end, intervalo positivo, viaje de referencia y coherencia con stop_times y calendario. No duplicar frecuencias y salidas explícitas de manera que se generen viajes dobles.

### 23. transfers.txt — reglas de conexión entre viajes/paradas

**Función y formato:** expresa restricciones o tiempos mínimos de conexión entre paradas, viajes o rutas. CSV, opcional. transfer_type es obligatorio. Para los tipos 0–3, from_stop_id y to_stop_id son obligatorios; para los tipos 4–5, from_trip_id y to_trip_id son obligatorios y las paradas son opcionales. Los IDs de ruta/viaje adicionales afinan la regla; min_transfer_time es opcional y se expresa en segundos. Los tipos 4–5 enlazan viajes operados por el mismo vehículo.

**Origen habitual:** estudios de intercambio, planificación de estaciones, tiempos medidos, reglas de conexión garantizada y acuerdos de enlace entre servicios.

**Documentación y controles:** distinguir conexión posible de conexión garantizada; registrar fuente y método del tiempo mínimo. Comprobar IDs, sentido, tipos enumerados y que no se prometa una conexión imposible por recorrido peatonal o margen operativo. No usarlo para describir el camino interior completo de una estación.

### 24. pathways.txt — recorridos interiores de estaciones

**Función y formato:** conecta nodos dentro de una estación con aristas como pasillos, puertas, escaleras, escaleras mecánicas o ascensores. CSV, opcional. Cuando se usa, pathway_id, from_stop_id, to_stop_id, pathway_mode e is_bidirectional son obligatorios. Los extremos deben ser nodos interiores válidos de stops.txt, no la estación principal. Otros detalles de tiempo, longitud, anchura, pendiente o señalización se añaden según el modo y la información disponible. Una puerta de salida (pathway_mode=7) no puede ser bidireccional.

**Origen habitual:** planos de estación/BIM, GIS interior, inventario de activos, levantamiento de campo y auditorías de accesibilidad.

**Documentación y controles:** mantener plano y nivel de detalle, método/fecha de inspección y evidencias de accesibilidad. Verificar extremos existentes, conexión dirigida o bidireccional correcta y completitud del grafo. Si se modelan caminos de una estación, se espera una representación completa de las conexiones relevantes; evitar nodos colgantes. La existencia de un ascensor no demuestra que toda la ruta sea accesible.

### 25. levels.txt — niveles o plantas

**Función y formato:** nombra y ordena niveles dentro de estaciones para interpretar caminos verticales. CSV. Condicionalmente obligatorio si pathways.txt describe ascensores (pathway_mode=5); opcional en otros casos. level_id y level_index son obligatorios; level_name es opcional. El suelo debe llevar índice 0, los niveles superiores índices positivos y los inferiores negativos.

**Origen habitual:** planos arquitectónicos, inventario de estación, BIM y datos de ascensores/escaleras.

**Documentación y controles:** acordar un origen de alturas coherente (por ejemplo, planta calle como cero) y documentar la convención; revisar niveles referenciados en stops/pathways, signos y orden. No calcular accesibilidad solo a partir de level_index.

### 26. location_groups.txt — grupos de puntos de demanda

**Función y formato:** agrupa paradas que representan conjuntamente dónde puede solicitarse recogida o bajada en un servicio flexible. CSV, opcional. location_group_id es obligatorio y único; debe ser único a escala del conjunto combinado de IDs stops.stop_id, features de locations.geojson y location_groups.location_group_id.

**Origen habitual:** diseño operativo de zona a demanda, catálogo de puntos virtuales de encuentro y reglas de reserva.

**Documentación y controles:** conservar plano de servicio y criterio de agrupación; verificar que los grupos tienen paradas asignadas mediante location_group_stops.txt y que el pasajero puede identificar razonablemente los puntos. No crear un grupo como sustituto de una zona poligonal cuando el servicio promete recogida en cualquier punto dentro de un área.

### 27. location_group_stops.txt — miembros de grupos de demanda

**Función y formato:** relación muchos-a-muchos entre grupo y parada. CSV, opcional. Cada fila requiere location_group_id y stop_id existentes. Un mismo stop puede aparecer en más de un grupo.

**Origen habitual:** exportación del planificador de demanda bajo demanda o tabla maestra de puntos habilitados por zona/horario.

**Documentación y controles:** mantener evidencia de qué paradas están disponibles para cada grupo y en qué vigencia (la vigencia operativa puede requerir otros campos o feeds complementarios); detectar referencias huérfanas y duplicados. Confirmar que el conjunto coincide con las condiciones de reserva publicadas.

### 28. locations.geojson — polígonos de servicio a demanda

**Función y formato:** representa zonas donde el usuario puede pedir recogida o bajada. GeoJSON FeatureCollection, opcional, con geometría Polygon o MultiPolygon válida; cada Feature tiene id, properties y geometry. El id debe ser único frente a stop_id y location_group_id. Las coordenadas siguen el orden GeoJSON RFC 7946: longitud, latitud.

**Origen habitual:** GIS municipal/operador, delimitación contractual del servicio, análisis de cobertura y digitalización de zonas aprobadas.

**Documentación y controles:** guardar capa fuente, sistema de referencia, fecha, proceso de transformación, licencia y documento que aprueba los límites. Validar geometría, anillos, orden lon/lat, cobertura y ausencia de huecos o solapes no deseados. Esta geometría no sustituye stops.txt para otros servicios; la omisión de stops solo se permite bajo la condición de zonas a demanda descrita por GTFS.

### 29. booking_rules.txt — condiciones de reserva

**Función y formato:** indica antelación y modalidad con que el pasajero debe reservar un servicio flexible. CSV, opcional. booking_rule_id y booking_type son obligatorios. Para booking_type=1 se exige prior_notice_duration_min; para booking_type=2 se exige prior_notice_last_day y, si se indica ese día, prior_notice_last_time. prior_notice_duration_max solo puede usarse con tipo 1; los campos prior_notice_start_day/start_time dependen de las condiciones de la referencia. Debe enlazarse desde stop_times mediante los campos de reserva correspondientes.

**Origen habitual:** reglamento y proceso de reserva, centro de llamadas, aplicación, portal de reservas y parámetros del planificador de demanda.

**Documentación y controles:** publicar de forma congruente canal, plazo, horario de atención, zona horaria y condiciones de modificación/cancelación. Verificar que los valores GTFS representan literalmente los plazos ofrecidos y que cada regla se usa por un servicio flexible válido.

### 30. translations.txt — traducciones de campos visibles

**Función y formato:** proporciona traducciones de textos de cara al pasajero en varias lenguas. CSV, opcional. table_name, field_name y language son obligatorios. Se debe indicar el valor traducido mediante field_value o mediante record_id (y record_sub_id cuando corresponda); no se usan ambos métodos a la vez. Solo se traducen campos admitidos por la referencia y feed_info no admite referencias por registro/valor. feed_info.txt es obligatorio si se incluye este archivo.

**Origen habitual:** catálogo corporativo de topónimos y traducciones revisadas por personal lingüístico, autoridad local o proveedor autorizado.

**Documentación y controles:** registrar idioma BCP 47, traductor/revisor y versión del glosario; verificar que cada registro y campo existe y que la traducción corresponde al texto original. Para España, respetar las formas oficiales y las obligaciones lingüísticas aplicables al servicio y territorio; GTFS permite traducciones, pero no decide por sí solo qué idioma es jurídicamente exigible.

### 31. feed_info.txt — metadatos de la publicación

**Función y formato:** identifica publicador, idioma, periodo de validez y versión del conjunto. CSV. El archivo es recomendado y pasa a ser obligatorio si se usan traducciones. Si se incluye, feed_publisher_name, feed_publisher_url y feed_lang son obligatorios. También conviene mantener fechas de inicio/fin, feed_version y contacto técnico cuando se conozcan.

**Origen habitual:** proceso de publicación de datos, catálogo de datasets, pipeline GTFS y política de versiones del operador/autoridad.

**Documentación y controles:** registrar responsable del feed, idioma principal, calendario de actualización y versión reproducible. Alinear la vigencia declarada con los calendarios; no publicar un feed caducado como actual. El contacto aquí es técnico para consumidores de datos; el contacto de atención al viajero va en agency.txt.

### 32. attributions.txt — atribución y licencia

**Función y formato:** declara atribuciones aplicadas al conjunto o a una parte. CSV, opcional. organization_name es obligatorio. attribution_id, agency_id, route_id, trip_id, attribution_url, attribution_email y attribution_phone son opcionales. Debe indicarse al menos uno de is_producer, is_operator o is_authority con valor 1; como alcance, se elige como máximo uno entre agency_id, route_id y trip_id. Si no se especifica ninguno, la atribución se aplica a todo el feed.

**Origen habitual:** contratos y licencias de cartografía, datos abiertos, autoría de formas, proveedor de paradas, operador y autoridad que publica el conjunto.

**Documentación y controles:** conservar la licencia, texto de atribución requerido, URL y alcance; confirmar si aplica a todo el feed, a una agencia o a rutas concretas. No usar una atribución para reemplazar permisos/licencias ni omitir créditos exigidos por la fuente.

## 4. Cómo suelen producir las empresas un GTFS

La producción común parte de varios sistemas de referencia, no de una única hoja:

| Información | Fuente empresarial habitual | Equipo o responsable típico |
| --- | --- | --- |
| Operador, líneas y condiciones de servicio | Contratos/concesiones, catálogo maestro, resolución y web oficial | Autoridad de transporte y operador |
| Horarios, calendarios y viajes | Planificación de oferta y horarios, tablas de marcha, calendario operativo | Planificación de servicio |
| Paradas y estaciones | GIS, inventario de activos, cartografía y levantamiento de campo | GIS, infraestructura y operación |
| Recorridos | GIS vial, diseño de línea, trazas GPS depuradas | Planificación y GIS |
| Tarifas y medios de pago | Tarifario oficial, ticketing, ventas, validación y acuerdos de integración | Área tarifaria y sistemas de billetaje |
| Accesibilidad e interiores | Auditorías, planos, BIM/GIS interior e inventario de ascensores | Infraestructura y accesibilidad |
| Demanda y reserva | Planificador DRT, zonas, puntos de encuentro y reglas del centro de reservas | Operación de transporte a demanda |
| Publicación y versiones | Exportador GTFS propio, software de planificación o proveedor especializado | Datos abiertos/TI y propietario del dato |

Una empresa puede generar el feed con hojas controladas en una red pequeña, con software de planificación/exportación en redes medianas y grandes, con desarrollo interno, o contratando un proveedor GTFS. En todos los casos el propietario del servicio sigue teniendo que revisar la exactitud y autorizar el contenido. La guía oficial de GTFS describe estas opciones; son prácticas posibles, no requisitos del formato.

Para este proyecto ficticio conviene mantener fuera del ZIP un **registro de procedencia** con: identificador del dato, campo/archivo afectado, categoría (sintético, derivado, cartografía de referencia, fuente oficial), fuente o documento, fecha, método, supuestos, licencia, responsable y revisión. En lo que sea enteramente inventado, indicarlo explícitamente; no dar una URL, concesión o marca real que sugiera autenticidad.

## 5. Qué cubre la normativa y qué no cubre este ZIP

La referencia GTFS establece esquema e interoperabilidad. En España, la Ley 9/2025 de Movilidad Sostenible regula obligaciones de información de servicios y prevé datos estáticos y dinámicos, con contenidos como rutas, paradas, horarios, características del servicio, tarifas, reserva, venta, accesibilidad e información ambiental, además de incidencias, tiempos reales y datos históricos. La normativa europea MMTIS regula disponibilidad e intercambio de información de transporte multimodal y contempla estándares y formatos interoperables. En el NAP español se admite GTFS o NeTEx; el propio NAP recomienda NeTEx por su mayor riqueza y alineación como estándar europeo.

Por tanto, un GTFS Schedule estático puede ser una parte útil del intercambio, pero no contiene por sí solo todo el ciclo de datos dinámicos, históricos, legales, ambientales, comerciales o de reserva que pueda ser exigible a un servicio concreto. GTFS Realtime es una especificación aparte. Antes de afirmar cumplimiento jurídico hay que identificar entidad obligada, tipo de servicio, autoridad competente, ámbito territorial, versión normativa aplicable, formato aceptado y procedimiento de publicación. Para este proyecto, “ficticio” impide afirmar cumplimiento operativo o legal de un servicio real.

## 6. Fuentes de referencia

- [Referencia oficial de GTFS Schedule (español)](https://gtfs.org/es/documentation/schedule/reference/) — esquema, campos, condiciones y formatos; revisada el 27 de abril de 2026.
- [Cómo producir/crear un feed GTFS](https://gtfs.org/es/getting-started/create/) y [cómo validarlo](https://gtfs.org/es/getting-started/validate/) — prácticas de producción y validación.
- [Ley 9/2025, de Movilidad Sostenible, texto consolidado del BOE](https://boe.es/buscar/act.php?id=BOE-A-2025-24545&p=20260321&tn=1) — consultar especialmente artículo 85 y anexo I, además de las disposiciones y desarrollos aplicables.
- [Preguntas frecuentes del Punto de Acceso Nacional (NAP)](https://nap.transportes.gob.es/faqs) — formatos y publicación en el contexto español.
- [Reglamento Delegado (UE) 2024/490](https://www.boe.es/buscar/doc.php?id=DOUE-L-2024-80207) — modificación del marco MMTIS.
- [RFC 7946 — GeoJSON](https://www.rfc-editor.org/rfc/rfc7946) — formato geográfico de locations.geojson.

**Mantenimiento:** revisar esta guía antes de generar cada versión del ZIP, porque la referencia GTFS y las normas de datos de transporte pueden cambiar. Cualquier afirmación de obligación legal debe volver a contrastarse con el BOE/DOUE consolidado y con las instrucciones vigentes del NAP.
