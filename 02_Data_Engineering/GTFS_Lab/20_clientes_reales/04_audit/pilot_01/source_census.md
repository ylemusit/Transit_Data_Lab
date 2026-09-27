# Pilot 01 — source census

Censo físico read-only de los cinco GTFS extraídos. No es una validación semántica.

| ID | Operador | TXT | routes | stops | trips | stop_times | shapes | fares | feed_info |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| 002 | Ancebus | 6 | 2 | 26 | 6 | 52 | false | false | 0 |
| 005 | Viagón | 6 | 11 | 62 | 22 | 240 | false | false | 0 |
| 014 | Gilsanz | 10 | 144 | 1244 | 788 | 16529 | true | true | 0 |
| 020 | Kbus | 11 | 4 | 88 | 278 | 6142 | true | true | 1 |
| 019 | Bizkaibus | 12 | 99 | 2334 | 22151 | 519647 | true | true | 1 |

El detalle de bytes, filas, columnas, encoding, BOM, saltos de línea, columnas duplicadas y campos no estándar se encuentra en el `source_census.json` y `source_census.md` de cada operador.
