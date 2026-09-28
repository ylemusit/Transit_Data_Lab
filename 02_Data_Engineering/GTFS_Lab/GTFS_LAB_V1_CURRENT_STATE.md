# GTFS_Lab V1 — estado actual

Actualizado: 2026-09-28. Este documento describe el estado técnico local de V1; no reabre ni modifica Compliance V1 y no acredita cumplimiento jurídico de ningún operador.

## Arquitectura

`gtfs_lab` implementa contratos comunes mínimos en `core.py` y módulos separados para ingestión, DuckDB, validación, análisis, GIS, orquestación e informe. La entrada es un ZIP GTFS. Cada ejecución crea su carpeta bajo `runs/<run_id>/`, conserva una copia únicamente de las tablas soportadas y genera una base DuckDB propia; no escribe en `databases/gtfs_lab.duckdb` ni en el ZIP de entrada.

Flujo: ZIP → comprobaciones y hash → tablas de ejecución → DuckDB `raw.*` → integridad → reglas → análisis → GIS → regla técnica Compliance V1 → `run.json` e informe.

## Entrada, identidad e inventario

Identidad: nombre fuente, SHA-256 completo, ID derivado del hash, hora UTC de ingesta, versión del parser y de GTFS_Lab, archivos, codificación, cabeceras y filas. Los valores GTFS se importan a DuckDB como `VARCHAR`.

El catálogo en `gtfs_lab/ingestion.py` enumera las tablas Schedule reconocidas. Las cinco tablas base (`agency`, `stops`, `routes`, `trips`, `stop_times`) se esperan en un feed fijo estándar; `calendar` y `calendar_dates` pueden aparecer individual o conjuntamente. Las otras tablas catalogadas son opcionales. Entradas no catalogadas se notifican como no soportadas. Se rechazan traversal, colisiones de nombres, límites de tamaño, archivos comprimidos corruptos, cabeceras inválidas y filas CSV irregulares. UTF-8 es preferido; cp1252 se admite con advertencia explícita.

## Integridad y reglas V1

La integridad de archivo/CSV ocurre antes de crear hallazgos. La integridad de esquema comprueba presencia de cabeceras base. La validación técnica incluye archivos requeridos y al menos una tabla de calendario; identificadores primarios repetidos para agency/stop/route/trip; referencias trip→route, service→calendar/calendar_dates, trip→shape si se proporciona; y la regla aceptada `V1-RULE-GTFS` para stop_times→trips/stops fijas. Las coordenadas de stops/shapes se validan en rangos y se exportan como lon,lat.

Los resultados técnicos son `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE` e `INSPECTION_ERROR`; `INGESTION_ERROR` se devuelve por separado antes de validar. No existe resultado jurídico.

## Compliance V1

El adaptador invoca directamente el motor congelado `tools/compliance_v1_engine.py`; comprueba el hash del evaluador (`efa87d…afa3b70`) y de la referencia GTFS (`1ff40b…b147`), sin copiar su predicado ni modificar Compliance V1. Su scope fijo es `stop_times.trip_id → trips.trip_id`, `stop_times.stop_id → stops.stop_id`, limitado a paradas (`location_type` vacío o `0`), máximo 1 MiB por archivo y 10.000 filas. Conserva hashes de ZIP/dataset/inspector y provenance en el run. No importa ni modifica la base de Compliance. En Asturias el motor devolvió `INSPECTION_ERROR: ValueError:EMPTY_OR_ROW_LIMIT` para `trips.txt` (21.015 filas); no es un finding GTFS. La inspección Compliance V1 pasa con fixtures sintéticos dentro de su límite. Cualquier `FAIL_TECHNICAL` exige defensa de falsos positivos y revisión de specification, interpretación, implementación, input/hash, versión/parser, validador y serialización antes de atribuirlo al operador.

## Análisis y GIS

`analysis.json` contiene recuentos, rutas, servicios por viajes, shapes, matriz ruta-parada, paradas compartidas y fechas activas por servicio. Expande los días semanales de `calendar.txt` y aplica las altas/bajas de `calendar_dates.txt`; limita cada rango a 50 años y reporta filas malformadas. No interpreta legalmente los datos. El query pack SQL contiene agencias, rutas por agencia, paradas por ruta, direcciones, paradas compartidas, shapes, servicios y matriz ruta-parada.

Se generan `stops.geojson`, `stops.kml`, `routes*.geojson` y KML por shape/ruta. `--route` y `--direction` limitan y diferencian la exportación. No hay edición manual. GeoJSON sigue `[longitude, latitude]`; KML usa `longitude,latitude,altitude`. Los puntos fuera de rango no se exportan y ya son findings técnicos.

## Uso

Desde este directorio:

```powershell
python -m gtfs_lab.cli "feeds/raw/feed.zip" --output runs --route 440 --direction 0
python -m gtfs_lab.gate --output runs/current_gate `
  --protect feeds/raw/20260924_020003_Consorcio_Asturias.zip `
  --protect databases/gtfs_lab.duckdb `
  --protect ../../tools/compliance_v1_engine.py `
  --protect ../../03_Compliance/reports/evidence/compliance_v1_20260928/sources/gtfs_reference.md `
  --protect ../../03_Compliance/databases/transit_compliance.duckdb
```

Se necesita Python 3.10+ y DuckDB CLI en PATH para crear la base local por ejecución. El gate usa fixtures sintéticos deterministas; genera sus ZIP y evidencia bajo la ruta de salida indicada.

## Límites y estado

No incluye GTFS-RT, SIRI, interfaz, plugin QGIS o parser completo de todas las tablas. Dry run local Asturias: ingestión, reglas GTFS_Lab, análisis, DuckDB y GIS PASS; cero hallazgos locales. La regla Compliance V1 devolvió `INSPECTION_ERROR` por su límite fijo de 10.000 filas, con cero hallazgos y sin modificar ZIP ni bases protegidas. Gate sintético con la regla Compliance dentro de scope: PASS. Esto es una limitación de tamaño del evaluador existente, no un incumplimiento del feed. Estado de cierre y alcance en `reports/GTFS_LAB_V1_STABILIZATION_REPORT.md`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
