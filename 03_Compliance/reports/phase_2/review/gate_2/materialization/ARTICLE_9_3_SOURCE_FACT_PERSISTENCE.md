# Article 9(3): persistencia controlada

- SOURCE_FACT_PERSISTENCE: `FAIL`
- source_fact_persisted: `YES`
- source_fact_id: `EU-2017-1926-SF-A09-P03`
- source_provision_id: `EU-2017-1926-ART09`
- source_document_id: `EU-REG-2017-1926`
- transaction_committed: `YES`
- PRE_WRITE_SHA: `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`
- POST_WRITE_SHA: `0c119b4a75e6a0e7954480675cc625659fe65a1878f46dae1e496e0790d8ffec`
- SHA_changed: `YES`
- source_fact_count_before: `35`
- source_fact_count_after: `36`
- article_9_source_facts_before: `2`
- article_9_source_facts_after: `3`
- requirements_before: `3`
- requirements_after: `3`
- deadlines_before: `1`
- deadlines_after: `1`
- protected_tables_unchanged: `YES`
- semantic_DB_delta: `+1 compliance.source_facts row: EU-2017-1926-SF-A09-P03`
- source_fact_traceability: `PASS`
- UTF8_roundtrip: `PASS`
- Phase_1_tests: `FAIL`
- Phase_2_tests: `PASS`
- final_atomic_universe: `48`
- final_exception_queue: `0`
- interpretive_issues: `0`
- mechanical_blockers: `0`
- materialization_prerequisites: `PASS`
- HUMAN_REVIEW_GATE_2: `OPEN`
- READY_FOR_PHASE_2_REQUIREMENTS_MATERIALIZATION: `NO`
- compliance.requirements_hash_before: `f17abec6a633fe0407ae49732db41a398aff3554fbcf98d9a73b3168ea0e0a5e`
- compliance.requirements_hash_after: `f17abec6a633fe0407ae49732db41a398aff3554fbcf98d9a73b3168ea0e0a5e`
- compliance.deadlines_hash_before: `2edd7d93608d71ef2196ecf88860522562035e4a811e2cff26f8959313f75a1d`
- compliance.deadlines_hash_after: `2edd7d93608d71ef2196ecf88860522562035e4a811e2cff26f8959313f75a1d`

## Tests
- test_phase_1_master: 22_REQUIREMENTS_NOT_DERIVED_YET = FAIL; expected=0, actual=3
- test_phase_1_master: PHASE_1_CORPUS_INTEGRITY = FAIL; expected=None, actual=None
El test histórico Phase 1 mantiene la expectativa requirements=0. Se ejecutó intacto: hay 3 requisitos preexistentes, conservados exactamente. El fallo histórico no es un delta introducido, pero el criterio estricto solicitado impide declarar PASS y cerrar Gate 2. No se alteran tests ni se revierte la inserción autorizada que superó sus verificaciones transaccionales.

La referencia aprobada es «Artículo 9, apartado 3» (Article 9(3)); la provision general Article 9 tiene paragraph=NULL. La traza del apartado 3 queda acreditada por referencia, texto literal, versión, URI y página 10 del corpus consolidado, no por una provision de párrafo inventada.

Solo se ha reevaluado SOURCE_FACT_NOT_PERSISTED. G2-045.source_fact_id y elegibilidad quedan documentados en el nuevo CSV de universo; los informes históricos y project_baseline.json conservan sus hashes.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Verificación específica final

Source fact tests: 8/8 PASS (SOURCE_FACT_TESTS.json). Phase 2: 28/28 PASS. Master estructural 2017/1926: 21/21 PASS y agregado PASS. Siete tests de anexos: 63/63 PASS. Phase 1 master: 23/24 comprobaciones PASS; falla 22_REQUIREMENTS_NOT_DERIVED_YET (0 esperado, 3 existentes) y por ello falla PHASE_1_CORPUS_INTEGRITY. Los diez hashes jurídicos coinciden. UTF-8 y la comparación de todas las filas existentes pasan.

Inventario completo de archivos nuevos y hashes: FILES_CREATED.csv. Estado Git conservado: GIT_STATUS_BEFORE.txt / GIT_STATUS_AFTER.txt.
