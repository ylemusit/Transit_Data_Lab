# NAP vs source — Kbus (020)

Todos los datos NAP de esta tabla proceden de `NAP snapshot`; los datos GTFS proceden del directorio físico `extracted/`.

| Campo | NAP declarado | Fuente física | Resultado |
|---|---:|---:|---|
| routes | 4 | 4 | MATCH |
| stops | 88 | 88 | MATCH |
| trips | 278 | 278 | MATCH |
| valid dates | 2023-12-31 → 2026-12-30 | 2024-01-01 → 2026-12-31 | PARTIAL_MATCH |
| route geometry | true | shapes.txt=true, trips con shape_id=6 | CONSISTENT_WITH_NAP |
| fares | true | fare_attributes.txt, fare_rules.txt | FARE_DATA_IN_GTFS |
| accessibility | false | true | ACCESSIBILITY_DATA_PRESENT_IN_GTFS |
