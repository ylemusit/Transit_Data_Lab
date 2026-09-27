# Política de baseline de tests

`test_phase_1_master.sql` es PHASE_1_FROZEN_STATE_TEST: valida la instantánea histórica de Phase 1. PHASE_1_FROZEN_REQUIREMENTS_COUNT = 0 permanece cierto para esa instantánea. El master y su evidencia nunca se reescriben para ajustarlos a datos actuales.

Los tests 01–21 y las condiciones estructurales del agregado son invariantes del corpus protegido: documentos, referencias, unicidad, relaciones y estructura 2017/1926. `test_phase_1_invariants.sql` conserva esas comprobaciones y manifiestos. Los tests 22–24 y las tres condiciones de tablas vacías del agregado son PHASE_STATE_TESTS: requirements, format_coverage y audit.rules pueden evolucionar. Se excluyen los tres de la suite de invariantes, aunque los dos últimos aún pasen en Phase 2.

Los masters estructural y de anexos son invariantes del corpus protegido. En el master Phase 2, 01–13 y 24–28 son contratos de integridad/trazabilidad; 17–20 protegen el corpus Phase 1; 14–16, 21–23 son condiciones del alcance y estado de Phase 2. No se presupone que estas últimas sean invariantes de fases posteriores.

Los tests de gate actual validan la fase activa. `test_phase_2_pre_materialization_gate.sql` exige 36 facts, 3 requirements, 1 deadline, universo propuesto de 48, cola y bloqueos vacíos, traza de fuentes, hashes y siete dependencias PARTIAL. Se ejecuta desde la raíz con DuckDB `-readonly`. La condición interpretativa verifica la decisión humana documentada, no produce una nueva interpretación jurídica. Las guardas de formatos inspeccionan propuestas y sus condiciones/alternativas; no certifican cumplimiento jurídico.

Una base acumulativa posterior no debe satisfacer condiciones históricas mutables ya superadas. Ejecutar el master Phase 1 contra Phase 2 produce EXPECTED_HISTORICAL_STATE_MISMATCH, incluido el FAIL agregado causado por requirements=0; no CURRENT_DATABASE_INTEGRITY_FAILURE. Un fallo adicional de invariantes sí bloquea el cierre.

Cada cambio de base exige verificación de delta específica de fase. Esta conciliación es exclusivamente read-only y compara todas las tablas con DATABASE_AFTER.json; revalida el delta anterior de +1 source_fact contra DATABASE_BEFORE.json. La transacción anterior es SOURCE_FACT_TRANSACTION=PASS; el FAIL global original se clasifica POST_WRITE_TEST_GATE_FAIL por HISTORICAL_PHASE_STATE_ASSERTION_APPLIED_TO_LATER_PHASE_DB. Los informes originales se conservan.

project_baseline.json solo se promueve en una congelación formal; no con cada escritura controlada. Cerrar Gate 2 permite iniciar una futura materialización autorizada: no congela ni cierra Phase 2, no evalúa cumplimiento, no completa mappings/reglas y no habilita Phase 3.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
