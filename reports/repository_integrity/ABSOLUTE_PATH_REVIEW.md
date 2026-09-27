# Revisión de rutas absolutas — Blocker Resolution 03

Fecha: 2026-09-27. Revisión analítica; no se ejecutan SQL, gates ni pipelines.

ABSOLUTE_PATH_REVIEW = PASS
EXISTING_FINDINGS_RECONSTRUCTED = YES
EXPECTED_FINDINGS = 23
CLASSIFIED_FINDINGS = 23
UNCLASSIFIED_FINDINGS = 0
ABSOLUTE_PATH_COMMIT_BLOCKERS = 0

## Fuente y reconstrucción

Conjunto exacto: las 23 filas con category=EXECUTABLE_PORTABILITY_RISK del histórico FIRST_FORMAL_COMMIT_FINDINGS.csv, en su orden original. Identificadores AP-001 a AP-023 asignados aquí, sin alterar el CSV original. No se confunden con las 155 referencias totales de la auditoría ni con el inventario de migración. Cada pareja archivo/línea existe y contiene read_blob con ruta absoluta Windows. El registro tiene una clasificación primaria por hallazgo.

## Clasificación

| Clasificación | Total |
|---|---:|
| INTENTIONAL_HISTORICAL_METADATA | 0 |
| DOCUMENTATION_REFERENCE | 0 |
| LOCAL_CONFIGURATION_REFERENCE | 0 |
| EXECUTABLE_PORTABILITY_RISK | 10 |
| FROZEN_EVIDENCE_REFERENCE | 13 |
| STALE_OR_DEAD_REFERENCE | 0 |
| UNKNOWN | 0 |

## Contexto y actividad

- AP-001–AP-010: CONTROLLED_TRANSACTION.sql, líneas 811–829. FROZEN_EVIDENCE_REFERENCE: transacción histórica de materialización, con BEGIN/COMMIT y validación de diez PDF. materialize_requirements.py:220–238 muestra su generación y ejecución originales. La matriz PHASE_2_REPRODUCIBILITY_MATRIX.csv exige estado previo y replay aislado, nunca sobre la base actual. No es un workflow activo sobre la baseline vigente. Sigue teniendo riesgo técnico si se intenta replay en otra ubicación.
- AP-011–AP-020: test_phase_2_post_materialization_gate.sql, líneas 758–776. EXECUTABLE_PORTABILITY_RISK: gate read-only vigente para validar el estado congelado; cada read_blob depende del directorio de la máquina original. La matriz lo conserva como validación reproducible y materialize_requirements.py:265 lo incluye como suite. Activo significa función vigente, no proceso ejecutándose ni rerun en esta revisión.
- AP-021–AP-023: test_phase_2_pre_materialization_gate.sql, líneas 81–83. FROZEN_EVIDENCE_REFERENCE: gate de una etapa anterior, con assertions mutables de 3 requirements/1 deadline. PHASE_2_FORMAL_FREEZE.md documenta su mismatch esperado frente al estado posterior de 48/10; review_phase_2_freeze.py:237 lo identifica como histórico. TEST_BASELINE_POLICY.md conserva la descripción de aquella etapa; el freeze posterior determina su vigencia actual. Puede ejecutarse en un replay histórico autorizado; no se clasifica como código muerto.

Los 23 son SQL ejecutable por sintaxis, pero solo diez pertenecen al gate vigente. Trece son referencias de etapas históricas congeladas. Los diez riesgos activos también están protegidos como inputs del freeze: clasificación primaria D, indicador frozen_or_historical=YES. No hay referencias documentales, configuración local, stale/dead ni UNKNOWN dentro del conjunto exacto de 23.

## Riesgos activos por hallazgo

Fuente común: `03_Compliance/sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql`.
Propósito: verificar el SHA-256 esperado del PDF jurídico indicado. Actividad: gate posterior vigente según la matriz de reproducibilidad y la suite de finalize; invocación read-only desde la raíz. Fallaría al relocalizar si la ruta original no existe. No se ha accedido a los PDF ni calculado hashes.

| finding_id | Línea | Documento | Corrección futura | Commit blocker |
|---|---:|---|---|---|
| AP-011 | 758 | EU-DIR-2010-40 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-012 | 760 | EU-DIR-2023-2661 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-013 | 762 | EU-REG-2017-1926 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-014 | 764 | EU-REG-2024-490 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-015 | 766 | ES-LAW-9-2025 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-016 | 768 | EU-REG-2024-1679 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-017 | 770 | EU-REG-IMPL-2026-1554 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-018 | 772 | EU-REG-IMPL-2026-253 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-019 | 774 | EU-REG-2011-454 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |
| AP-020 | 776 | EU-REG-2014-1305 | Variante separada con raíz configurable, mismos hashes, SQL congelado intacto | NO |

## Excepción Compliance y decisión de commit

Los tres local_file retenidos (EU-REG-2024-1679, EU-REG-IMPL-2026-1554 y EU-REG-IMPL-2026-253) son INTENTIONAL_HISTORICAL_METADATA fuera del conjunto de 23. Contrastados exclusivamente en PHASE_1_SOURCE_DOCUMENTS.csv y las comparaciones UNCHANGED_ROW de los dos SQL. No se modifica ni abre la DuckDB. Su presencia en las lecturas read_blob revisadas es una dependencia ejecutable distinta de la conservación de metadatos.

Commit blockers = 0. El commit puede establecer fielmente la baseline histórica con su limitación de ubicación documentada. No implica validación portable en cualquier máquina. Modificar ahora transacción, tests o local_file alteraría artefactos del freeze; no es requisito del primer commit. En una tarea futura, conservar originales y diseñar una variante de replay/validación con resolución de rutas configurable, sin mutar metadatos históricos ni resultados. Esto no autoriza replay ni corrección.

## Verificación y límites

Verificación dirigida del registro: 23 filas únicas, correspondencia exacta con archivo/línea del CSV histórico, clasificaciones válidas, 10 activos, 13 históricos primarios, 0 UNKNOWN, 0 blockers. Los tres SQL se comparan byte a byte antes/después de generar los informes, sin hash. La auditoría conserva su prefijo previo byte a byte; solo se añade esta resolución. Índice real ausente y sin entradas antes/después. No nueva certificación de bytes del corpus o de la base; seguridad por alcance de escrituras limitado a los tres informes.

Compliance known retained paths preserved = YES
FROZEN_EVIDENCE_MODIFIED = NO
PATHS_REWRITTEN = NO
REAL_GIT_INDEX_CHANGED = NO
STAGING/COMMIT/TAG/PUSH = NO
REPOSITORY_WIDE_CONTENT_SEARCH = NO
REPOSITORY_WIDE_SEARCH_PERFORMED = YES (consulta inicial recursiva de nombres con rg --files antes de leer las restricciones; no repetida)
REPOSITORY_WIDE_HASH_PERFORMED = NO
RECURSIVE_DATASET_TRAVERSAL = NO
RESOURCE_GUARD_TRIGGERED = YES (desviación inicial de nombres declarada; estrategia corregida)

No fallback de búsqueda para reconstruir hallazgos. Reconstrucción realizada exclusivamente desde evidencia existente. Sin investigación web, datasets, hashes ni descubrimiento amplio de dependencias.

## Archivos y pendiente

Creados: ABSOLUTE_PATH_REGISTER.csv y ABSOLUTE_PATH_REVIEW.md en reports/repository_integrity.
Modificado: FIRST_FORMAL_COMMIT_AUDIT.md, únicamente adenda del resultado.

JWT_BLOCKER_RESOLUTION y LINE_ENDING_REVIEW conservan su PASS registrado. PROJECT_CONSOLIDATION = BLOCKED. FIRST_FORMAL_COMMIT = STILL_PENDING. Queda la verificación final pre-commit acotada; no se ejecuta en esta resolución. No se detectan blockers materiales por rutas dentro del conjunto revisado.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
