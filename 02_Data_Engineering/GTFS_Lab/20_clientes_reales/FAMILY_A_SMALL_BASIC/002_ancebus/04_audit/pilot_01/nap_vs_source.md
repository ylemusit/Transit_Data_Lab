# NAP vs source — Ancebus (002)

Todos los datos NAP de esta tabla proceden de `NAP snapshot`; los datos GTFS proceden del directorio físico `extracted/`.

| Campo | NAP declarado | Fuente física | Resultado |
|---|---:|---:|---|
| routes | 2 | 2 | MATCH |
| stops | 26 | 26 | MATCH |
| trips | 6 | 6 | MATCH |
| valid dates | 2025-01-01 → 2026-12-31 | 2025-01-01 → 2026-12-31 | MATCH |
| route geometry | false | shapes.txt=false, trips con shape_id=0 | CONSISTENT_WITH_NAP |
| fares | false | sin ficheros tarifarios | NO_FARE_DATA_DECLARED |
| accessibility | false | false | NO_ACCESSIBILITY_DATA_IN_GTFS |
