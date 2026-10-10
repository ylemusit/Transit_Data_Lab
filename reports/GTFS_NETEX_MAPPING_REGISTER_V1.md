# Registro de correspondencias GTFS Schedule ↔ NeTEx — borrador V1

Fecha: 2026-10-09. Estado: **BORRADOR INTERNO, pendiente de datos y decisiones de un operador**.

Este registro prepara el diseño de una conversión estática GTFS Schedule ↔ NeTEx. No es un perfil NeTEx, una especificación de generación, una declaración de cobertura ni una aceptación de destino. Ninguna correspondencia de abajo debe codificarse como definitiva hasta fijar el modelo fuente, el perfil de destino y las reglas del operador.

## Registro inicial de dominios

| ID | Dominio | GTFS Schedule de origen | Conceptos NeTEx candidatos | Riesgo o decisión que falta | Evidencia mínima para aprobar el mapping |
|---|---|---|---|---|---|
| MAP-01 | Operador y metadatos | `agency.txt`, `feed_info.txt` | Organización, autoridad/operador y metadatos de publicación | `agency_id`, autoridad competente, identidad del publicador y versión de feed no son necesariamente una entidad uno-a-uno. | Propietario del dato, namespace de IDs, identificación de productor/publicador y periodo/versionado acordados. |
| MAP-02 | Paradas y jerarquía | `stops.txt`, `levels.txt`, `pathways.txt` | `ScheduledStopPoint`, `StopPlace`, `Quay` y relaciones de acceso/parada | `location_type` y `parent_station` requieren interpretación; edificios, andenes, accesos y áreas de embarque pueden tener granularidad distinta. | Tabla de tipos y relaciones validada por el operador, catálogo de paradas/IDs y casos de parada simples y jerárquicas. |
| MAP-03 | Líneas y modos | `routes.txt` | `Line` y conceptos de modo/transporte del perfil | `route_type`, códigos extendidos, agencia y presentación pueden requerir listas controladas del destino. | Versión del perfil, tabla de códigos autorizados y decisión por cada extensión/código sin equivalente. |
| MAP-04 | Viajes y paradas programadas | `trips.txt`, `stop_times.txt` | `ServiceJourney`, patrón de viaje y tiempos de paso programados | Identidades, orden, visitas repetidas, tiempos omitidos/interpolados y datos opcionales pueden cambiar la semántica. | Ejemplos aprobados de ida/vuelta, parada repetida, primer/último horario y política de IDs estables. |
| MAP-05 | Calendario y excepciones | `calendar.txt`, `calendar_dates.txt` | Tipos de día, periodos operativos y asignaciones | Fechas efectivas, excepciones y periodo de publicación deben coincidir; una fecha vacía no prueba que no haya servicio real. | Periodo de servicio acordado, zona horaria y casos de alta/baja de servicio contrastados por el operador. |
| MAP-06 | Geometría y recorridos | `shapes.txt` y coordenadas de `stops.txt` | Geometría, enlaces de recorrido y secuencias espaciales del perfil | CRS, orden de ejes, unidades, distancia acumulada y diferencias entre forma y recorrido operacional. | CRS/axis declarados, referencia espacial y ejemplos con geometría validada por responsable del dato. |
| MAP-07 | Frecuencias | `frequencies.txt` | Servicio/frecuencia según las construcciones admitidas por el perfil | `start_time`, `end_time`, `headway_secs` y `exact_times` no garantizan una conversión uno-a-uno a horarios explícitos. | Decisión de representación y prueba de ida/vuelta con hora de inicio, fin y salida exacta cuando aplique. |
| MAP-08 | Transbordos y accesibilidad | `transfers.txt`, campos de accesibilidad en `stops.txt`/`trips.txt` | Reglas de intercambio, conexiones y accesibilidad | Reglas condicionadas, duraciones y valores desconocidos no deben convertirse en valores por defecto. | Tabla de códigos/perfil, semántica de desconocido y casos de conexión y accesibilidad aprobados. |
| MAP-09 | Tarifas | `fare_attributes.txt`, `fare_rules.txt` y extensiones admitidas | Productos, zonas y reglas de tarifa del perfil | Estructuras de tarifas pueden no ser expresables de forma equivalente; las extensiones y métodos de pago dependen del destino. | Decidir explícitamente si está en alcance, mapping soportado o pérdida aceptada; ejemplos validados. |
| MAP-10 | Extensiones y campos no representables | Campos GTFS extendidos, traducciones y atribuciones | Extensiones y referencias definidos por el perfil del operador | No existe correspondencia genérica segura para todo campo opcional o extensión. | Registro campo a campo: transformar, conservar como extensión, omitir con aprobación o bloquear la generación. |

Todos los conceptos de la columna NeTEx son **candidatos de diseño**, no rutas XML aprobadas por el perfil. La tabla no prueba que los elementos puedan combinarse en cualquier versión o destino.

## Decisiones que debe aportar el operador

Completar antes de construir un generador o publicar una salida:

| Dato requerido | Valor acordado / evidencia |
|---|---|
| Operador, productor y propietario de cada fuente | `PENDIENTE` |
| Feed/modelo de entrada autorizado, licencia, versión y periodo | `PENDIENTE` |
| Versión y extensiones GTFS Schedule que deben aceptarse | `PENDIENTE` |
| XSD NeTEx exacto, versión y SHA-256 de dependencias | `PENDIENTE` |
| Perfil NeTEx, NAP/destino y versión de criterios controlados | `PENDIENTE` |
| Catálogo externo y política de referencias/IDs/alias | `PENDIENTE` |
| CRS, eje, unidades y zona horaria | `PENDIENTE` |
| Decisión campo a campo en `MAP-01` a `MAP-10`, pérdidas y transformaciones | `PENDIENTE` |
| Validador y versión de referencia que usará el destinatario | `PENDIENTE` |
| Canal, titularidad, permisos, entorno, cadencia y formato de entrega | `PENDIENTE` |
| Prueba de aceptación, responsable del resultado, rollback y monitorización | `PENDIENTE` |

No registrar credenciales en este documento; el mecanismo de acceso se acuerda aparte y los secretos permanecen fuera del repositorio.

## Puertas de aprobación y prueba

1. **Identidad y derechos:** fuente identificada, autorizada y reproducible; cada versión conserva procedencia.
2. **Perfil y destino:** versión de esquema, perfil, catálogo y destinatario fijados. Un XSD PASS no aprueba perfil o destino.
3. **Mapping:** cada fila tiene responsable, decisión, conversión, tratamiento de ausencias/desconocidos y pérdidas explícitas. `PENDIENTE` bloquea generar para ese alcance.
4. **Pruebas:** fixtures positivos, negativos, condicionales y límite por cada fila aprobada; comparación con validador independiente cuando aplique; preservación de IDs, calendarios, tiempos y geometría según criterios acordados.
5. **Entrega:** paquete de prueba separado de producción, validación local y de destino, versión identificada, evidencia de recepción, monitorización y recuperación comprobadas.
6. **Aceptación:** decisión real del destinatario registrada aparte del resultado técnico; respuesta del productor seguida de una nueva versión y una ejecución distinta de reauditoría.

## Estado de partida

El repositorio mantiene líneas de auditoría estática, pero no integra generadores GTFS/NeTEx, conversión, ni publicación remota. La recepción del operador y el flujo de correcciones existentes son internos/sintéticos. El [mapa de brechas de capacidad](TDL_STATIC_GTFS_NETEX_CAPABILITY_GAP_20261009.md) documenta las dependencias; el [blueprint del servicio](audit_service_v1/SERVICE_BLUEPRINT.md) contiene las etapas de recepción, alcance, revisión, entrega, reauditoría y aceptación.
