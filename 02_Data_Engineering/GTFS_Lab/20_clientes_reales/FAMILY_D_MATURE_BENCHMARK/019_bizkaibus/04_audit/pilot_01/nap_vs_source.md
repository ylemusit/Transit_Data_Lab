# NAP vs source — Bizkaibus (019)

Todos los datos NAP de esta tabla proceden de `NAP snapshot`; los datos GTFS proceden del directorio físico `extracted/`.

| Campo | NAP declarado | Fuente física | Resultado |
|---|---:|---:|---|
| routes | 99 | 99 | MATCH |
| stops | 2334 | 2334 | MATCH |
| trips | 22151 | 22151 | MATCH |
| valid dates | 2017-01-06 → 2026-12-23 | 2016-06-30 → 2026-12-23 | PARTIAL_MATCH |
| route geometry | true | shapes.txt=true, trips con shape_id=433 | CONSISTENT_WITH_NAP |
| fares | true | fare_attributes.txt, fare_rules.txt | FARE_DATA_IN_GTFS |
| accessibility | true | true | ACCESSIBILITY_DATA_PRESENT_IN_GTFS |
