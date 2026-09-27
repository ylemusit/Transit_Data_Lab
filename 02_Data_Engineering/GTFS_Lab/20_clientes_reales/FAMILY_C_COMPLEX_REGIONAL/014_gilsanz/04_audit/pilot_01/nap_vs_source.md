# NAP vs source — Gilsanz (014)

Todos los datos NAP de esta tabla proceden de `NAP snapshot`; los datos GTFS proceden del directorio físico `extracted/`.

| Campo | NAP declarado | Fuente física | Resultado |
|---|---:|---:|---|
| routes | 144 | 144 | MATCH |
| stops | 1244 | 1244 | MATCH |
| trips | 788 | 788 | MATCH |
| valid dates | 2026-01-01 → 2049-12-31 | 2026-01-01 → 2049-12-31 | MATCH |
| route geometry | true | shapes.txt=true, trips con shape_id=246 | CONSISTENT_WITH_NAP |
| fares | false | fare_attributes.txt, fare_rules.txt | FARE_DATA_IN_GTFS |
| accessibility | false | false | NO_ACCESSIBILITY_DATA_IN_GTFS |
