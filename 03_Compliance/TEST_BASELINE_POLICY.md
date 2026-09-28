# Política de baseline de tests

## Gate vigente Compliance V1 (2026-09-28)

CURRENT AUTHORITATIVE: `tools/compliance_v1_current_gate.py --evidence <directorio_nuevo>`.
Compliance V1 y Phase 3 están CLOSED_WITH_DEFERRALS en los scopes de
[COMPLIANCE_V1_SCOPE](COMPLIANCE_V1_SCOPE.md). El gate verifica el delta aditivo
exacto de 44 filas, fuentes, fixtures, representability, observaciones, reglas,
coverage/disposiciones, standby, reproducción y protección de todas las tablas.

Phase 1 invariants: 22/22 PASS. Phase 2 post-materialization: 386 PASS y un
FAIL original histórico `UNCHANGED_COUNT_audit.rules` (0 esperado frente a 2
reglas autorizadas). El gate V1 exige ese único mismatch exacto y valida ambas
reglas completas; no modifica el SQL histórico. Los diez hashes legales sí se
comprueban. El preestado anterior a V1 pasó 387/387.

El gate B02 `--closure-coverage` conserva su utilidad HISTORICAL para su
preestado; como gate global tras V1 queda DEPRECATED_FOR_CURRENT_STATE debido
a las nuevas capas. Su contenido protegido permanece cubierto por igualdad
exacta contra baseline más paquete V1, no por relajar contadores. Los validators
históricos y sus FAIL se conservan.

Evidencia vigente: `reports/evidence/compliance_v1_20260928/current_gate_04/`.
Los apartados siguientes documentan contratos anteriores a V1. No deben
interpretarse como la decisión de cierre actual.

## Selección histórica tras materialización y freeze de Phase 2

La entrada operativa global es [PROJECT_STATUS.md](../PROJECT_STATUS.md). Phase 2 está FROZEN; su base contiene 48 requirements. Los masters iniciales y la política de conciliación que sigue conservan el contexto de sus etapas de preparación.

`test_phase_2_master.sql` no es un gate de cierre compatible con la base materializada: su test 23 une requirements con el staging original `requirement_candidates` por requirement_id y exige APPROVED allí. La materialización posterior aprobó un universo atómico de 48 mediante Gate 2, reutilizando tres requisitos e insertando 45, sin sustituir aquel staging. La revisión actual observa 27 PASS / 1 FAIL (45 en test 23), con hash DB idéntico al freeze. Ese resultado se clasifica EXPECTED_HISTORICAL_STATE_MISMATCH para este contrato antiguo; no se convierte en PASS ni se modifica la evidencia original.

El contrato del estado final es `sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql`, junto con `reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.json` y la materialización aprobada. El gate incluye diez comprobaciones read_blob de fuentes y trece rutas absolutas en total (tres son valores esperados de metadata histórica); no es portable fuera del workspace original. No relativizar sus expectativas ni metadatos congelados silenciosamente.

En esta revisión se contrastaron 377 comprobaciones de filas/estado extraídas de ese gate, excluyendo explícitamente las diez comprobaciones de hashes jurídicos para no rehashear el corpus. Resultado completo, SQL ejecutado y exit code en `../reports/repository_integrity/alignment_20260927/`. No es un nuevo gate jurídico completo ni una promoción de baseline.

### Contrato de cierre final M06-B02 (2026-09-28)

La misión FINAL CLOSURE autoriza dos decisiones PARTIAL para A05-P01-002 y
A05-P02-001, sin modificar los mappings aprobados ni el esquema. El gate vigente
se ejecuta con `tools/m06_b02_validate.py --closure-coverage`: conserva los SQL y
sus resultados originales, añade las dos filas completas esperadas a row-exact y
al delta EXCEPT ALL contra backup + S1, y mantiene las restantes comprobaciones.
B02D `B02_COVERAGE_UNCHANGED`, B02C `B02_COVERAGE`/`COVERAGE_GLOBAL`, populated
`B02_COVERAGE` y M04B `NON_PILOT_COVERAGE` son expectativas pre-coverage
históricas incompatibles exclusivamente con este delta. B01 TOTALS y B02A
PROTECTED_COUNTERS ya eran históricos; su contenido protegido sigue cubierto
por igualdad de todas las tablas. Sin el flag se conserva el gate pre-cierre.
No se relajan vocabularios, referencias, límites, revisiones ni protección legacy.

Pruebas aisladas fresh/NO-OP/conflict/rollback PASS; posterior autoritativo PASS.
Evidencia y FAIL históricos: `reports/phase_3/M06_B02_FINAL_CLOSURE.md` y
`reports/phase_3/evidence/m06_b02_final_closure_20260928_03/`.
El cierre es CLOSED_WITH_DEFERRALS; Phase 3 sigue IN_PROGRESS.

### Pack operacional Phase 3 (2026-09-28)

No modifica el estado autoritativo; sigue aplicando el gate B02 con
`--closure-coverage`. `tools/phase3_operational_checks.py --evidence <nuevo>`
prueba exclusivamente el contrato de observación en una copia local: cinco
roundtrips, diez rechazos, relaciones scope/mapping/capability, delta exacto y
rollback. Ese PASS no equivale a representabilidad, fixtures de perfil, regla
de auditoría ni demo operativa. El inventario reproducible está en
`tools/phase3_scope_inventory.py`; no persiste disposiciones documentales.
La decisión vigente es Phase 3 IN_PROGRESS, con dos pilotos DEFERRED y etapas
dependientes SKIPPED_BY_DEPENDENCY. Véase
`reports/phase_3/PHASE3_OPERATIONAL_CLOSURE_REPORT.md`.

## Contexto histórico y conciliación de fases

### Contrato posterior a M06-B02D-S1 (2026-09-28)

El pack orquestado autoriza nueve mappings C01/C07 PARTIAL y sus siete grupos
de filas, más la identidad SIRI prerequisito. No autoriza cambiar las filas
protegidas. `tools/m06_b02_validate.py` ejecuta y conserva las salidas originales
de diez validators, y separa las expectativas históricas incompatibles con ese
delta mediante una lista explícita `HISTORICAL`. M04/M05B esperaban ausencia de
mappings fuera de sus lotes; B01 fijaba totales anteriores; B02A/populated/B02C
esperaban B02 sin mappings, bridges o scopes. Sus FAIL originales siguen siendo
FAIL históricos, no se reetiquetan como PASS de los SQL originales.

El gate vigente combina los restantes checks, B02D (21 checks), comparación
NULL-safe de todas las columnas del paquete y comparación bidireccional
`EXCEPT ALL` de cada tabla contra la copia previa más exclusivamente el delta
aprobado. Esta última comprobación también protege los componentes invariantes
de los checks históricos compuestos. Cualquier otra diferencia bloquea.
No se cambian expected counts en los validators históricos ni se reconstruye
una baseline de Phase 1/2. El informe maestro y la evidencia conservan los
errores iniciales del validator B02D y las repeticiones aisladas corregidas.

`test_phase_1_master.sql` es PHASE_1_FROZEN_STATE_TEST: valida la instantánea histórica de Phase 1. PHASE_1_FROZEN_REQUIREMENTS_COUNT = 0 permanece cierto para esa instantánea. El master y su evidencia nunca se reescriben para ajustarlos a datos actuales.

Los tests 01–21 y las condiciones estructurales del agregado son invariantes del corpus protegido: documentos, referencias, unicidad, relaciones y estructura 2017/1926. `test_phase_1_invariants.sql` conserva esas comprobaciones y manifiestos. Los tests 22–24 y las tres condiciones de tablas vacías del agregado son PHASE_STATE_TESTS: requirements, format_coverage y audit.rules pueden evolucionar. Se excluyen los tres de la suite de invariantes, aunque los dos últimos aún pasen en Phase 2.

Los masters estructural y de anexos son invariantes del corpus protegido. En el master Phase 2, 01–13 y 24–28 son contratos de integridad/trazabilidad; 17–20 protegen el corpus Phase 1; 14–16, 21–23 son condiciones del alcance y estado de Phase 2. No se presupone que estas últimas sean invariantes de fases posteriores.

Los tests de gate actual validan la fase activa. `test_phase_2_pre_materialization_gate.sql` exige 36 facts, 3 requirements, 1 deadline, universo propuesto de 48, cola y bloqueos vacíos, traza de fuentes, hashes y siete dependencias PARTIAL. Se ejecuta desde la raíz con DuckDB `-readonly`. La condición interpretativa verifica la decisión humana documentada, no produce una nueva interpretación jurídica. Las guardas de formatos inspeccionan propuestas y sus condiciones/alternativas; no certifican cumplimiento jurídico.

Una base acumulativa posterior no debe satisfacer condiciones históricas mutables ya superadas. Ejecutar el master Phase 1 contra Phase 2 produce EXPECTED_HISTORICAL_STATE_MISMATCH, incluido el FAIL agregado causado por requirements=0; no CURRENT_DATABASE_INTEGRITY_FAILURE. Un fallo adicional de invariantes sí bloquea el cierre.

Cada cambio de base exige verificación de delta específica de fase. Esta conciliación es exclusivamente read-only y compara todas las tablas con DATABASE_AFTER.json; revalida el delta anterior de +1 source_fact contra DATABASE_BEFORE.json. La transacción anterior es SOURCE_FACT_TRANSACTION=PASS; el FAIL global original se clasifica POST_WRITE_TEST_GATE_FAIL por HISTORICAL_PHASE_STATE_ASSERTION_APPLIED_TO_LATER_PHASE_DB. Los informes originales se conservan.

project_baseline.json solo se promueve en una congelación formal; no con cada escritura controlada. Cerrar Gate 2 permite iniciar una futura materialización autorizada: no congela ni cierra Phase 2, no evalúa cumplimiento, no completa mappings/reglas y no habilita Phase 3.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
