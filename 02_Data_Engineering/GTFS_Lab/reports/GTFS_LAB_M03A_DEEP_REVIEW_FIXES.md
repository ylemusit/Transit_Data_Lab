# GTFS_Lab Trust Foundation M03-A — deep review fixes

Fecha: 2026-09-29. Revisión del Draft PR #5 sobre el head revisado `77c0ddb911fda969c1d2bc4c98dfe9cc0c46ec87`. Se mantiene `GoldenCase 1.0.0`; no se hace merge ni se inicia M03-B.

## A. API de autoridad

`has_approved_status(case)` expresa únicamente el lifecycle. `is_executable_authority(case, base_dir)` valida primero el GoldenCase completo, incluyendo input y SHA-256, y solo entonces devuelve `True` para `APPROVED`. Un contrato inválido produce error de validación; nunca se considera autoridad ejecutable. La validación no autentica a la persona revisora ni la base declarada.

## B. Casos de autoridad inválida

El gate llama directamente a la API de autoridad para ambos negativos:

- `APPROVED` sin review válida: PASS, no es autoridad.
- `{"status":"APPROVED"}` sin contrato: PASS, no es autoridad.

El caso completo APPROVED con review válida se reconoce como elegible; los otros lifecycle statuses no son APPROVED.

## C. Semántica del gate

M03-A aplica 18 checks contractuales; resultado `PASS = 18/18`. `approved_mutation_detection = NOT_ENFORCED_IN_M03A` se informa en `limitations` y no se contabiliza como PASS. No se implementa ledger, firma ni registro externo.

## D. Rutas

Casos negativos permanentes del gate: `absolute_windows_path`, `absolute_posix_path` y `parent_traversal_path` (todos PASS). El contrato además comprueba containment después de resolver la ruta; no se añadió caso de symlink.

## E. Alcance y documentación

Se conserva `GoldenCase 1.0.0`. M03-A valida estructura y declaración del tipo de expectation; M03-B definirá evaluación. Se actualizaron el contrato y el README de GTFS_Lab. La detección de mutación histórica consta como limitación, nunca como PASS.

## F. Regresión

- M01 Trust Contract: PASS, 12/12.
- M02 Trust Persistence: PASS, 21/21; reconciliación válida y outputs V1 preservados.
- GTFS_Lab V1: PASS; fixtures, E2E sintético y GIS direccional PASS.
- Compliance V1: PASS; 386 checks Phase 2 actuales y 22 Phase 1 actuales PASS. Se conserva por separado el FAIL histórico `UNCHANGED_COUNT_audit.rules` (esperado 0, observado 2). Hash de la base inicial/final idéntico: `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`.
- M03-A: PASS, 18/18.
- `py_compile`: PASS.
- `git diff --check`: PASS.

Los gates M01, M02, GTFS_Lab V1 y M03-A se ejecutaron desde el worktree aislado de M03. Compliance V1 se ejecutó desde el worktree M02 que contiene el DuckDB protegido con el hash vigente; su evidencia regenerada quedó bajo `%TEMP%`, fuera del PR.

## G. Archivos del cambio

Cinco archivos intencionados: contrato M03, README GTFS_Lab, `golden_contract.py`, `golden_contract_gate.py` y este informe. No se incluyen runs, `reports/evidence`, DB ni JSON regenerables de gates.

## H. Head

Se actualizará el mismo Draft PR #5; el SHA final corresponde al head publicado de esa rama.

## I. Pull request

PR #5, base `main`, sigue abierto como Draft. No merge.

## J. Veredicto

`M03A_DRAFT_PR_READY_FOR_FINAL_REVIEW`

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
