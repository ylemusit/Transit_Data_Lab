# Pilot 01 — baseline matrix

Valores NAP: `NAP snapshot` + `manual_verified`. Valores físicos: censados desde `02_sources/gtfs_schedule/extracted/`. Valores GTFS Explorer: evidencia de `run_001/informe-validacion.html`.

| Operador | Rutas NAP/GTFS | Paradas NAP/GTFS | Viajes NAP/GTFS | Fechas | Geometría | Tarifas | Accesibilidad | GTE status | GTE detectadas | GTE persistidas | Detalle completo |
|---|---:|---:|---:|---|---|---|---|---|---:|---:|---|
| Ancebus | 2/2 | 26/26 | 6/6 | MATCH | CONSISTENT_WITH_NAP | NO_FARE_DATA_DECLARED | NO_ACCESSIBILITY_DATA_IN_GTFS | INVALID | 12 | 12 | true |
| Viagón | 11/11 | 62/62 | 22/22 | MATCH | CONSISTENT_WITH_NAP | NO_FARE_DATA_DECLARED | NO_ACCESSIBILITY_DATA_IN_GTFS | INVALID | 56 | 56 | true |
| Gilsanz | 144/144 | 1244/1244 | 788/788 | MATCH | CONSISTENT_WITH_NAP | FARE_DATA_IN_GTFS | NO_ACCESSIBILITY_DATA_IN_GTFS | INVALID | 1 | 1 | true |
| Kbus | 4/4 | 88/88 | 278/278 | PARTIAL_MATCH | CONSISTENT_WITH_NAP | FARE_DATA_IN_GTFS | ACCESSIBILITY_DATA_PRESENT_IN_GTFS | INVALID | 644 | 644 | true |
| Bizkaibus | 99/99 | 2334/2334 | 22151/22151 | PARTIAL_MATCH | CONSISTENT_WITH_NAP | FARE_DATA_IN_GTFS | ACCESSIBILITY_DATA_PRESENT_IN_GTFS | INVALID | 1040852 | 100000 | false |

Las cifras GTE se conservan separadas entre ocurrencias detectadas, ocurrencias persistidas y filas de detalle persistidas.
