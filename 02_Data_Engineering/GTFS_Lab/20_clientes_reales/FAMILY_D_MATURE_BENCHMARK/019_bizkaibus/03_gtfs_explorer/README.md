# Recepción GTFS Explorer 0.2.1 — Bizkaibus

GTFS Explorer Desktop se ejecuta externamente; sus outputs se copian aquí como
evidencia. No se ejecuta ni se replica desde el piloto.

## Runs preservados

- `run_001`: **HISTORICAL NON-CANONICAL `validation-100k`**. Evidencia original
  de investigación; no debe borrarse ni reinterpretarse como RC-002.
- `run_002_rc002`: **PROVENANCE MISMATCH — NOT ACCEPTED AS RC-002**. Aunque el
  nombre lo presenta como RC-002, su `data.duckdb` es schema 9 y conserva
  100.000 de 1.040.852 incidencias, con 940.852 omitidas. RC-002 exige schema
  11 y ejecutable SHA-256 `d154fe2131922765ad464852866b95268cbc92020b525cdda5a9affeadbde2e7`.
  No contiene informe HTML ni evidencia que vincule el proceso a ese hash.

Hasta disponer de un run con procedencia canónica demostrada, las conclusiones
actuales del Pilot no deben sustituirse por `run_002_rc002`.

## run_004_gtfs023_candidate001

- `run_004` es `CURRENT_ACCEPTED_BIZKAIBUS_RESULT` y `GTFS023_ACCEPTED`.
  La reevaluación forense independiente confirma
  `RUN004_CANDIDATE_PROVENANCE_CONFIRMED`: UserAssist acredita la ruta exacta
  de `GTFS-023-CANDIDATE-001` / `ATTEMPT-002` antes de crear el workspace y
  antes de la importación persistida. El EXE SHA-256 es
  `8ea4a367baeef61381380f42edb44619c9d8bb97c1961754775c289bf588a357`.
- Es un proyecto fresco schema 11 con fuente original Bizkaibus confirmada,
  importación completa y validación `VALID` con cero incidencias persistidas.
- La nota RC-002 se conserva como `STALE_INCORRECT_PROVENANCE_NOTE`; el
  addendum de lanzamiento posterior no se emplea para acreditar el run.
- `FALSE_ENUM_NORMALIZATION_BLOCKER` y `CANONICAL_BIZKAIBUS_IMPORT_BLOCKER`
  están `CLOSED`. La `duckdb.TransactionException` histórica es
  `NOT_REPRODUCED`; no se afirma causalidad completa ni se requiere rerun.
- Los 1.040.852 hallazgos de `run_001`/`run_002_rc002` siguen siendo
  `INVALIDATED_PRODUCT_FINDING` / `FALSE_POSITIVE_ENUM_CONTRACT`; nunca deben
  utilizarse como indicador de calidad de Bizkaibus.
