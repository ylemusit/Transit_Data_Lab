# NAP vs source — Viagón (005)

Todos los datos NAP de esta tabla proceden de `NAP snapshot`; los datos GTFS proceden del directorio físico `extracted/`.

| Campo | NAP declarado | Fuente física | Resultado |
|---|---:|---:|---|
| routes | 11 | 11 | MATCH |
| stops | 62 | 62 | MATCH |
| trips | 22 | 22 | MATCH |
| valid dates | 2025-01-01 → 2026-12-31 | 2025-01-01 → 2026-12-31 | MATCH |
| route geometry | false | shapes.txt=false, trips con shape_id=0 | CONSISTENT_WITH_NAP |
| fares | false | sin ficheros tarifarios | NO_FARE_DATA_DECLARED |
| accessibility | false | false | NO_ACCESSIBILITY_DATA_IN_GTFS |
