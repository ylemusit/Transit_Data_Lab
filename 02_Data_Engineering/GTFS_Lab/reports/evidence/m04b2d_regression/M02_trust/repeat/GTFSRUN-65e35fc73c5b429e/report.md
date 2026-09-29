# Informe técnico GTFS_Lab

- Run: `GTFSRUN-65e35fc73c5b429e`
- Dataset: `GTFS-26baf9a07d4b6e3b`
- Fuente: `ORPHAN_TRIP.zip`
- SHA-256: `26baf9a07d4b6e3b2155bfaa4e82bb7a6bf45550218fc2f711e8cbc425ed0af8`
- Ingesta UTC: `2026-09-29T16:24:34.756921+00:00`
- GTFS_Lab: `1.0.0-dev`; parser: `gtfs-lab-csv/2`; reglas: `1.0.0`

## Tablas y filas

| Tabla | Estado | Filas |
|---|---:|---:|
| agency.txt | PRESENT | 1 |
| stops.txt | PRESENT | 2 |
| routes.txt | PRESENT | 1 |
| trips.txt | PRESENT | 2 |
| stop_times.txt | PRESENT | 2 |
| calendar.txt | OPTIONAL | 0 |
| calendar_dates.txt | PRESENT | 1 |
| shapes.txt | PRESENT | 4 |
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
- Referencial: PASS

## Validación

Estado: **FAIL_TECHNICAL**; hallazgos técnicos: 1

| Regla | Estado | Hallazgos |
|---|---|---:|
| GTFS-STRUCT-REQUIRED | PASS | 0 |
| GTFS-STRUCT-SERVICE-CALENDAR | PASS | 0 |
| GTFS-REF-TRIP-ROUTE | PASS | 0 |
| GTFS-REF-SERVICE | PASS | 0 |
| GTFS-REF-SHAPE | PASS | 0 |
| GTFS-UNIQUE-PRIMARY-ID | PASS | 0 |
| GTFS-COORDINATE-RANGE | PASS | 0 |
| V1-RULE-GTFS | FAIL_TECHNICAL | 1 |

Hallazgos:
- `V1-RULE-GTFS` stop_times.txt stop_times.txt#csv-record=2;trip_id=ghost;stop_id=s1 / trip_id/stop_id: observado `ABSENCE_CONFIRMED`; esperado trip_id references trips.trip_id; stop_id references fixed stops.txt platform. BROKEN_FOREIGN_REFERENCE

## Análisis

```json
{
  "agency": 1,
  "routes": 1,
  "trips": 2,
  "stops": 2,
  "stop_times": 2,
  "shapes": 4,
  "calendar": 0,
  "calendar_dates": 1
}
```
- Rutas: 1; paradas compartidas: 0
- Calendario: PASS; servicios con fechas: 1; pares servicio-fecha: 1

## GIS y DuckDB

- GeoJSON/KML paradas: PASS (2 entidades)
- GIS rutas/formas: PASS (3 archivos)
- Base DuckDB aislada: PASS

## Compliance V1

- Regla: `V1-RULE-GTFS` → `FAIL_TECHNICAL` (BROKEN_FOREIGN_REFERENCE)
- Evaluador: `compliance-v1/2` / `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`.
- Procedencia: Invocación del motor Compliance V1 v2 sobre archivos de ingestión; regla semántica sin cambios.

## Límites

- Resultado exclusivamente técnico; no concluye cumplimiento jurídico ni incumplimiento de operador.
- SIRI y GTFS-RT no se procesan; tablas GTFS adicionales solo se inventariarían si están en el catálogo soportado.
- Revisión de falsos positivos debe conservar specification, interpretation, implementation, input/hash, versión/parser, validador y serialización antes de atribuirlos al operador.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
