# GTFS_Lab V1 — informe de estabilización

Fecha: 2026-09-28. Decisión: **`GTFS_LAB_V1 = READY_FOR_CHECKPOINT`**. No hay commit ni push.

## Resumen ejecutivo

- Estado inicial comprobado: ZIP/raw y sentinel existentes; DuckDB con siete tablas; GIS con tres KML route 440 sin generador; core, validation y analysis no implementados.
- Estado final: paquete V1 reproducible con gate sintético PASS, salida DuckDB aislada, análisis y GIS reproducibles, informe e invocación directa del evaluador Compliance V1. En Asturias las reglas locales dieron PASS y cero findings, pero la regla Compliance devolvió `INSPECTION_ERROR` por el límite contractual de filas; el resultado combinado del run lo conserva como `INSPECTION_ERROR`.
- Alcance técnico: ZIP Schedule estático. No es una auditoría legal ni concluye cumplimiento del operador.
- Compliance V1 no se reabrió y sus documentos/base no se modificaron. No se incorporaron realtime, SIRI, UI, servicio web ni dependencias Python nuevas.

## Inventario Stage 0

| Artefacto | Clase | Decisión de conservación |
|---|---|---|
| ZIP Asturias, extracción local y `databases/gtfs_lab.duckdb` | ACTIVE | Input/base de referencia protegidos; el nuevo flujo trabaja por run. |
| `gtfs_lab/` (core, ingestión, database, validation, analysis, GIS, pipeline, gate) | ACTIVE | Implementación V1. |
| `sql/07_tests/test_gtfs_lab_integrity.sql` | ACTIVE | Sentinel read-only alineado con la base congelada. |
| `sql/08_analysis/gtfs_lab_v1_query_pack.sql` | ACTIVE | Consultas de análisis reproducibles sobre la base de un run. |
| SQL/PowerShell de importación antigua en `sql/01_import` | LEGACY | Conservado; modifica la base congelada y no forma parte del camino V1. |
| `exports/route_440*.kml` (3 XML KML válidos) | USEFUL_EXPERIMENT | Conservados como referencia histórica; ya existe generador reproducible. |
| PNG y canvases de GTFS/NeTEx | USEFUL_EXPERIMENT | Material de exploración, sin uso como dependencia runtime. |
| `20_clientes_reales/` y herramientas piloto | ACTIVE, scope independiente | Conservadas; no se ejecutaron ni se usaron como evidencia de este gate. |
| `main.stops` | DUPLICATED | El sentinel verifica igualdad exacta con `raw.stops`; no se elimina porque su propósito sigue por aclarar. |

No se clasificó ningún elemento como `DEAD` y no se borró, movió ni reescribió evidencia anterior. Recomendación de limpieza posterior: mantener paquetes V1, inputs, base protegida, sentinel y consultas; marcar el import antiguo como deprecated cuando el checkpoint V1 se adopte; conservar KML anteriores como fixtures visuales de referencia. `REMOVE_LATER` no se recomienda por ahora.

## Contrato V1 y arquitectura

Entrada: GTFS ZIP. Salidas: resultado de ingestión, identidad/hash, inventario y conteos, integridad, resultados/hallazgos técnicos, resumen analítico, export GIS, observación compatible con Compliance V1 e informe por run.

`gtfs_lab/core.py` define identidad, contexto de ejecución y resultados. El ZIP nunca se extrae sobre un destino arbitrario: se inspeccionan rutas/nombres y se copian únicamente las tablas soportadas al área aislada `runs/<run_id>/input`. Cada ejecución construye su propio `dataset.duckdb`; mantiene valores como `VARCHAR` y verifica columnas ID/tiempo. La base histórica en `databases/gtfs_lab.duckdb` no se reimporta ni escribe.

El catálogo declara 31 nombres GTFS Schedule. Asturias tiene 7 presentes (`agency`, `calendar_dates`, `routes`, `shapes`, `stop_times`, `stops`, `trips`); `calendar.txt` no está presente y no es necesario porque se suministra `calendar_dates.txt`. Las tablas opcionales ausentes se informan como `OPTIONAL`; una tabla entrante fuera del catálogo queda como `NOT_SUPPORTED` con advertencia. GTFS-RT y SIRI no se consideran.

Protecciones de ingestión: path traversal, miembros/tabla duplicados, miembros >512 MiB o total descomprimido >2 GiB, ZIP corrupto, codificación no decodificable, cabeceras ausentes/duplicadas y filas CSV irregulares. UTF-8 es preferido; fallback cp1252 queda advertido. Faltas del archivo obligatorio se convierten en resultado estructural técnico; fallo de parser/cabeceras produce `INGESTION_ERROR` y no un finding GTFS.

## Integridad, reglas y control de falsos positivos

Integridad informa por separado presencia/lectura de archivos, esquema/cabeceras, integridad referencial y validación semántica inicial. Reglas versionadas identifican scope, severidad/tipo, descripción, referencia, dataset, tabla/registro/campo, observado, esperado, mensaje técnico y evidencia con hash/parser. Estados admitidos: `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `INSPECTION_ERROR`; error de carga se mantiene como `INGESTION_ERROR`.

Reglas iniciales: archivos y calendario estructurales; unicidad de IDs principales de agency/stops/routes/trips; trips→routes, trips→calendar/calendar_dates, trips→shapes cuando se indica; coordenadas dentro de rango; y `V1-RULE-GTFS` para stop_times→trips/stops fijas. La regla de Compliance V1 omite las localizaciones flex fuera de este subconjunto. No se generan hallazgos cuando falla el parser.

Los fixtures verifican casos de referencia y errores. En un feed real, cualquier resultado futuro `FAIL_TECHNICAL` exige cotejar specification, interpretación, implementación, input/hash, versión de parser, validador y serialización antes de atribuirlo al operador. Un resultado técnico nunca equivale a `LEGAL_NON_COMPLIANT`.

## Análisis, SQL y GIS

El análisis produce recuentos, agencias, rutas, viajes por servicio, inventario de shapes, matriz ruta-parada y paradas compartidas. El calendario expande los días activos de `calendar.txt` y aplica adiciones/excepciones de `calendar_dates.txt`; rangos malformados o mayores de 50 años quedan identificados. Sobre Asturias se calcularon 108 servicios con fechas y 3.875 pares servicio-fecha. El SQL formaliza ocho consultas: agencias, rutas por agencia, paradas por ruta, viajes/direcciones, paradas compartidas, shapes, servicios y matriz ruta-parada.

Exportadores generan stops KML/GeoJSON y líneas por route/shape KML/GeoJSON, filtrables por `route_id` y `direction_id`. GeoJSON usa `[longitud, latitud]`; KML usa `longitud,latitud,altitud`. Se comprueban rangos antes de exportar.

## Compliance y reporting

`V1-RULE-GTFS` llama directamente a `tools/compliance_v1_engine.py`, sin replicar el predicado. El adaptador exige el SHA evaluador fijado `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70` y el SHA de referencia `1ff40b8001b180bd023dd6f1899907aecbcb4600c8dbcb6fc6c841a50839b147`. Conserva provenance, hash ZIP, hash del subconjunto inspeccionado, evaluador, regla y salida técnica en el run. No escribe en código, fuentes ni base de Compliance.

La regla congelada admite 1 MiB por archivo y 10.000 filas. Los fixtures V1 (dentro del límite) dan PASS para referencia válida y `FAIL_TECHNICAL` para trip/stop orphan. En el feed Asturias, `trips.txt` supera 10.000 filas (21.015); el motor devolvió `INSPECTION_ERROR: ValueError:EMPTY_OR_ROW_LIMIT`, cero findings y ninguna conclusión sobre esas referencias. La inspección fue correcta conforme al límite configurado. No se amplió el límite porque el contrato/regla de Compliance V1 está cerrado.

Cada run guarda `run.json`, `analysis.json`, `validation.json`, `report.md`, una base aislada y exportaciones. `run.json` contiene run/dataset ID, hash, parser/lab/validator, inicio/fin, inventario, resultados, errores y resumen. La ruta `runs/` está excluida de Git por contener bases y artefactos de ejecución; el informe de esta misión y la definición de estado son documentación versionable.

## Verificación ejecutada

| Comprobación | Resultado |
|---|---|
| Compilación sintáctica `python -m compileall -q gtfs_lab` | PASS |
| `GTFS_LAB_V1_CURRENT_GATE` | PASS; casos requeridos VALID_MINIMAL, ORPHAN_TRIP, ORPHAN_STOP, ORPHAN_ROUTE, BAD_SERVICE_REFERENCE, BAD_SHAPE_REFERENCE, MALFORMED_CSV, MISSING_FILE, PARTIAL_FEED; hardening adicional missing header, unsupported table, traversal, duplicate ZIP y repetición de identidad. |
| End-to-end sintético | PASS; ZIP→hash→DuckDB→integridad→reglas→análisis→KML/GeoJSON→regla Compliance→informe. |
| Integridad histórica read-only | 42 PASS, 0 FAIL en conteos, tablas, referencias, coordenadas, secuencias, horas, duplicados conocidos y route 440. |
| Query pack sobre DuckDB de ejecución | PASS; las ocho consultas ejecutan en feed Asturias. |
| GIS | PASS; GeoJSON de route 440 presenta coordenadas `[−5.63121, 43.3691]` (lon,lat); KML generado parsea como XML; direcciones 0/1 producen shapes diferenciadas. |
| Feed Asturias local (Stage 15) | FAIL_LOCAL para el subresultado de Compliance V1 por su límite fijo; ingestión, reglas GTFS_Lab, análisis, GIS y DuckDB PASS. 0 findings; resultado combinado de integridad/validación `INSPECTION_ERROR`. 41 agencias, 609 rutas, 21.015 viajes, 6.368 stops, 354.287 stop_times, 774.732 shape points y 3.875 filas calendar_dates. |
| Integración Compliance V1 | PASS con fixtures, llamando al evaluador congelado por SHA. Asturias produjo `INSPECTION_ERROR` (scope >10.000 filas), no un PASS inventado ni un finding del operador. |
| Identidad repetible | PASS; mismo ZIP → `GTFS-f3093ab85d728ee8` en las repeticiones, distinto run ID. |
| Estado protegido SHA-256 antes/después | PASS, idéntico: ZIP `f3093ab85d728ee824ba45cd3f247d1d9ea68a4685aaf25b27a8de98ea50b549`; base GTFS congelada `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`; base Compliance V1 `4db39fa5494c525f339f68bf0b96087b5ff2e1e0cb830eea882336174bc8048b`; evaluador `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70`; referencia `1ff40b8001b180bd023dd6f1899907aecbcb4600c8dbcb6fc6c841a50839b147`. |

Evidencia local completa del run: `runs/real_closure_20260928/GTFSRUN-ae0d31fdad204709/`. Evidencia JSON del gate: `runs/gtfs_lab_v1_gate_ready/gate.json`. Ambos directorios son locales e ignorados por Git; los resúmenes anteriores están capturados en este informe.

## Cierre

| Criterio V1 | Estado |
|---|---|
| Ingestión ZIP reproducible e identidad estable | PASS |
| Core y contratos comunes | PASS |
| Integridad/validación y reglas iniciales | PASS |
| Fixtures y defensa sintética de referencias | PASS |
| Análisis, calendario y SQL reproducibles | PASS |
| GIS KML/GeoJSON y direcciones | PASS |
| Adaptador Compliance V1 con provenance | PASS |
| Informe técnico y E2E | PASS con ZIP sintético de punta a punta; run real reproducible con `INSPECTION_ERROR` únicamente en la regla Compliance por el límite existente. |
| Gate actual | PASS |

Limitaciones conocidas: solo se procesa GTFS Schedule estático y el subconjunto de tablas del catálogo; el resumen de fechas está limitado a rangos de hasta 50 años; la regla Compliance V1 solo emite una conclusión en inputs de hasta 1 MiB por archivo y 10.000 filas. La salida `INSPECTION_ERROR` para el feed local queda como límite técnico conocido; no se aumenta ni reemplaza el evaluador cerrado. El gate PASS demuestra V1 con fixtures acotados, y el run real reproduce el resultado acotado sin atribuir findings al operador. No es una auditoría legal ni una declaración del operador.

**Decisión final: `GTFS_LAB_V1 = READY_FOR_CHECKPOINT`.** Sin commit, push, limpieza destructiva ni contacto con terceros.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
