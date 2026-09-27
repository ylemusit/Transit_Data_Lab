# Bizkaibus

- Benchmark ID: `019`; familia: `FAMILY_D_MATURE_BENCHMARK`.
- Fuentes físicas preservadas: GTFS Schedule original, GTFS Schedule extraído y snapshot NAP.
- GTFS original: `02_sources/gtfs_schedule/original/20260910_060014_Euskadi_Bizkaibus.zip`.
- GTFS extraído: `02_sources/gtfs_schedule/extracted/`; snapshot NAP: `01_nap_snapshot/bizkaibus.png`.
- El original permanece trazado por SHA-256; no se han alterado fuentes, raw evidence ni Working Copy.

## Resultado actual GTFS Explorer

`CURRENT_ACCEPTED_BIZKAIBUS_RESULT=run_004_gtfs023_candidate001` y
`GTFS023_ACCEPTED`; en v0.2.2, `GTFS-023=CLOSED_IN_V0.2.2`. La procedencia de
`GTFS-023-CANDIDATE-001` / `ATTEMPT-002` está confirmada por evidencia
independiente de UserAssist anterior al workspace y a la operación. El run es
fresco, schema 11, de importación completa y validación `VALID` de cero
incidencias bajo las reglas y alcance actuales de validación de GTFS Explorer;
no prueba calidad universal perfecta del feed.

Los 1.040.852 hallazgos de `run_001` y `run_002_rc002` permanecen separados
como `HISTORICAL_INVALIDATED_PRODUCT_FINDINGS`,
`INVALIDATED_PRODUCT_FINDING` y `FALSE_POSITIVE_ENUM_CONTRACT`. No son una
medida de calidad de Bizkaibus. La `duckdb.TransactionException` histórica no
se reprodujo en `run_004`; no se deduce una causalidad completa.
