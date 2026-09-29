# Informe técnico GTFS_Lab

- Run: `GTFSRUN-e3a0c3f163294e24`
- Dataset: `GTFS-28e24901f5cec87b`
- Fuente: `input.zip`
- SHA-256: `28e24901f5cec87b900d1d7de510e2a97b3007158c0775012bf6210ad73eab81`
- Ingesta UTC: `2026-09-29T16:24:34.551309+00:00`
- GTFS_Lab: `1.0.0-dev`; parser: `gtfs-lab-csv/2`; reglas: `1.0.0`

## Tablas y filas

| Tabla | Estado | Filas |
|---|---:|---:|
| agency.txt | PRESENT | 1 |
| stops.txt | PRESENT | 2 |
| routes.txt | PRESENT | 1 |
| trips.txt | PRESENT | 1 |
| stop_times.txt | PRESENT | 2 |
| calendar.txt | OPTIONAL | 0 |
| calendar_dates.txt | PRESENT | 1 |
| shapes.txt | OPTIONAL | 0 |
| frequencies.txt | OPTIONAL | 0 |
| transfers.txt | OPTIONAL | 0 |
| feed_info.txt | OPTIONAL | 0 |
| levels.txt | OPTIONAL | 0 |
| translations.txt | OPTIONAL | 0 |
| pathways.txt | OPTIONAL | 0 |
| attributions.txt | OPTIONAL | 0 |
| fare_attributes.txt | OPTIONAL | 0 |
| fare_rules.txt | OPTIONAL | 0 |
| fare_media.txt | OPTIONAL | 0 |
| fare_products.txt | OPTIONAL | 0 |
| fare_leg_rules.txt | OPTIONAL | 0 |
| fare_leg_join_rules.txt | OPTIONAL | 0 |
| fare_transfer_rules.txt | OPTIONAL | 0 |
| timeframes.txt | OPTIONAL | 0 |
| networks.txt | OPTIONAL | 0 |
| route_networks.txt | OPTIONAL | 0 |
| areas.txt | OPTIONAL | 0 |
| stop_areas.txt | OPTIONAL | 0 |
| locations.txt | OPTIONAL | 0 |
| location_groups.txt | OPTIONAL | 0 |
| booking_rules.txt | OPTIONAL | 0 |
| fare_parkings.txt | OPTIONAL | 0 |

## Integridad

- Archivos: PASS
- Esquema: PASS
- Referencial: FAIL_TECHNICAL

## Validación

Estado: **FAIL_TECHNICAL**; hallazgos técnicos: 1

| Regla | Estado | Hallazgos |
|---|---|---:|
| GTFS-STRUCT-REQUIRED | PASS | 0 |
| GTFS-STRUCT-SERVICE-CALENDAR | PASS | 0 |
| GTFS-REF-TRIP-ROUTE | FAIL_TECHNICAL | 1 |
| GTFS-REF-SERVICE | PASS | 0 |
| GTFS-REF-SHAPE | PASS | 0 |
| GTFS-UNIQUE-PRIMARY-ID | PASS | 0 |
| GTFS-COORDINATE-RANGE | PASS | 0 |
| V1-RULE-GTFS | PASS | 0 |

Hallazgos:
- `GTFS-REF-TRIP-ROUTE` trips.txt record:2 / route_id: observado `missing-route`; esperado route_id debe existir en routes.txt. Referencia técnica sin registro padre

## Análisis

```json
{
  "agency": 1,
  "routes": 1,
  "trips": 1,
  "stops": 2,
  "stop_times": 2,
  "shapes": 0,
  "calendar": 0,
  "calendar_dates": 1
}
```
- Rutas: 1; paradas compartidas: 0
- Calendario: PASS; servicios con fechas: 1; pares servicio-fecha: 1

## GIS y DuckDB

- GeoJSON/KML paradas: PASS (2 entidades)
- GIS rutas/formas: NOT_EVALUABLE (0 archivos)
- Base DuckDB aislada: PASS

## Compliance V1

- Regla: `V1-RULE-GTFS` → `PASS` (FIXED_STOP_REFERENCES_RESOLVE_TO_TRIP_AND_PLATFORM)
- Evaluador: `compliance-v1/2` / `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`.
- Procedencia: Invocación del motor Compliance V1 v2 sobre archivos de ingestión; regla semántica sin cambios.

## Límites

- Resultado exclusivamente técnico; no concluye cumplimiento jurídico ni incumplimiento de operador.
- SIRI y GTFS-RT no se procesan; tablas GTFS adicionales solo se inventariarían si están en el catálogo soportado.
- Revisión de falsos positivos debe conservar specification, interpretation, implementation, input/hash, versión/parser, validador y serialización antes de atribuirlos al operador.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
