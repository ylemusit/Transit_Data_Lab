# TDL TRUST FOUNDATION — M04-B2D Compliance V2 Approval and Freeze

Estado: `COMPLIANCE_V1_IMPLEMENTATION_V2_APPROVED_AND_FROZEN`. HOLDOUT V2 sigue cerrado.

## A. Historical package identity

- Identidad/paquete: `compliance-v1/1`; SHA-256 `2f85c9bd92ad603bab696e34c886b3f85ac22c05ba7aa0e90dc10137bb061981`.
- Evaluador: `compliance-v1/1`; SHA-256 `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70`.
- DB histórica: SHA-256 `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`. Freeze: `COMPLIANCE_V1_LOGICAL_FREEZE_20260928`; SHA-256 `3BBB6D87500608364972CFE841D6B2D3D03558FC73F1960A28579905FAEC6A3E`.
- El paquete declara `version` como `compliance-v1/1`; no separa package, evaluator y generator version. La identidad real del paquete se conserva por SHA-256.

## B. Candidate package identity

- Archivo: `03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate_final/package_candidate.json`.
- Paquete actual aprobado: `compliance-v1/2`; SHA-256 `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`.
- Lifecycle `APPROVED_CURRENT` se registra en `transition_manifest.json`; el contrato del paquete no contiene un campo lifecycle.

## C. Package lineage

El manifest acompaña al paquete candidato con `predecessor_package` igual al SHA histórico y razón `IMPLEMENTATION_CHANGE`. La estructura de paquete existente no tiene campos versionados de lineage ni generator identity; el sidecar declara ambas identidades y no altera el artefacto congelado. Generador base SHA-256 `ba9fb9367dd9b734cf957993cc3b5ff6ecb5834dd8180e2bd604c84d946846c9`; constructor de transición y SHA están registrados en el manifest.

## D. Rule semantic identity

`V1-RULE-GTFS` permanece `compliance-v1/1`. La identidad semántica no cambia.

## E. Evaluator implementation identity

El evaluador cambia de `compliance-v1/1` (`efa87d…`) a `compliance-v1/2` (`60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`). El parser del motor GTFS_Lab sigue `gtfs-lab-csv/2`.

## F. Differential semantic comparison

Se compararon los 28 fixtures sintéticos congelados de Compliance con evaluadores v1 y v2. La proyección explícita fue: `result`, `reason`, `locator`, `observed`, `legal_conclusion_allowed`, `dataset_sha256`, `dataset_id`. Resultado: 28/28 iguales, cero deltas. No se eliminaron campos ad hoc. Harness: `02_Data_Engineering/GTFS_Lab/tests/test_compliance_v1_transition.py`.

## G. Legacy-domain equivalence

Los 28 casos cubren el conjunto de fixtures existente dentro del dominio evaluable legacy (filas y archivos dentro de los límites anteriores). Todos mantienen outcome, finding/razón, locator, observado y significado de aplicabilidad.

## H. Expanded operational domain

Dos casos sintéticos superan por separado el límite antiguo de 1 MiB y el de 10.000 filas: v1 devuelve `INSPECTION_ERROR`; v2 evalúa normalmente con resultado semántico `PASS`. Esto demuestra ampliación de capacidad, no cambio de regla. Guardas del evaluador: 512 MiB por archivo GTFS, 1.000.000 filas, 4 MiB por registro lógico, 128 KiB por campo y 256 columnas. El límite de ZIP descomprimido de 2 GiB pertenece a la ingesta GTFS_Lab, no al evaluator Compliance. Son guardas de implementación, no requisitos GTFS/Compliance.

## I. Generator replay

La construcción del candidato v2 repetida dos veces produce el mismo objeto y SHA; `candidate_replay_status=PASS`. En el intento inicial de reproducir el paquete histórico, la escritura temporal en Windows convirtió LF a CRLF y cambió el SHA del código incorporado; ese intento quedó registrado como inconcluso. La sección siguiente cierra la reproducibilidad con recuperación binaria del blob y serialización explícita. No se escribió sobre el paquete histórico ni la DB original.

## I.1. Cierre de reproducibilidad histórica

- El evaluador histórico se recuperó directamente y en bytes del blob Git `efe3164ddfe33255d9ce94db0e6f410a80ec58c6`; el blob contiene 8.768 bytes LF, cero CRLF y no tiene BOM. SHA-256 esperado y actual: `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70`.
- Contrato de replay del paquete: reconstruir el objeto con el evaluador recuperado; serializar con `json.dumps(ensure_ascii=False, indent=2).encode("utf-8")`; convertir LF a CRLF para reproducir la materialización histórica de Windows; no añadir newline final.
- SHA-256 esperado y reproducido del paquete: `2f85c9bd92ad603bab696e34c886b3f85ac22c05ba7aa0e90dc10137bb061981`; identidad byte a byte: PASS. La DB protegida se copió y verificó por SHA antes de usarla en lectura; la DB original no se modificó.
- El intento anterior permanece registrado como inconcluso: la materialización temporal en modo texto convirtió el evaluador LF a CRLF y alteró el SHA del código incorporado. La recuperación binaria del blob y el contrato explícito de serialización cierran ahora esa limitación; no se elimina el registro histórico.
- Evidencia durable: `02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2a_transition_20260929/historical_package_replay.json`.

Veredicto técnico registrado antes de la revisión humana: `M04B2B_HISTORICAL_REPLAY_VERIFIED`. En esa captura la transición aún esperaba decisión; la aprobación vigente consta en la sección M.

## J. Historical package integrity

- Paquete histórico: sin cambios; SHA verificado `2f85c9bd…`.
- DB Compliance: sin cambios; SHA verificado `4DB39FA5…`.
- Freeze: sin cambios; SHA verificado `3BBB6D87…`.
- B1 `reports/evidence/holdout_evaluation_v1/*`: `git diff` frente a `8d4f2ad7fa0545b76dd5d5ec5503890ed0c396d9` vacío. No se leyeron ZIPs HOLDOUT.
- Golden Corpus `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3`; split `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d`.

## K. Regression

- 52/52 tests GTFS_Lab: PASS, incluidos parser/scale y differential transition.
- Trust M01, Trust M02, M03-A, Golden Corpus, Golden Evaluator, Golden Regression, split, lineage y GTFS_Lab sintético: PASS.
- `compileall` y `git diff --check` (incluidos los ficheros nuevos): PASS.
- Estado de entrada: el gate estricto había quedado bloqueado en `PACKAGE_GENERATOR_REPLAY`. Tras registrar esta aprobación, el gate se actualizó para ejecutar por separado el generador histórico v1 y el generador actual aprobado v2. Resultado actual: `PASS`, con DB hash de entrada/salida idéntico; salida en [evidencia M04-B2D](../03_Compliance/reports/evidence/compliance_v1_20260929/current_gate_m04b2d_final4/summary.json).
- Phase 1: 22/22 PASS. Phase 2: 386 PASS y el mismatch histórico preservado `UNCHANGED_COUNT_audit.rules` (0 esperado, 2 actual). No se debilitó ese contrato ni los checks de replay.

## L. Commit / PR head

Rama `feat/tdl-trust-foundation-m04b2-triage`; base revisada `83b6a6a522892c916272a2249f57a906023a56ed`, base PR `8d4f2ad7fa0545b76dd5d5ec5503890ed0c396d9`. Destino: el mismo Draft PR #9; no se marca Ready ni se hace merge.

## M. Human approval

- Transition: `COMPLIANCE_V1_IMPLEMENTATION_TRANSITION_V1_TO_V2`; decision `APPROVE`.
- Reviewer: Yeison Arbey Carrillo Lemus; `reviewed_at_utc=2026-09-29T16:18:55Z`.
- Basis: regla semántica sin cambios; 28/28 equivalencia legacy; 2/2 fixtures ampliados; replay v2 actual y replay v1 histórico PASS; paquete/DB/freeze históricos y B1 preservados; HOLDOUT no usado durante desarrollo.

## Approved current implementation

Pointer vigente: [compliance_v1_current_implementation_v2.json](../03_Compliance/reports/evidence/compliance_v1_current_implementation_v2.json). Rule semantic identity: `V1-RULE-GTFS / compliance-v1/1`. Evaluator actual: `compliance-v1/2`, SHA-256 `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; parser: `gtfs-lab-csv/2`; package SHA-256 `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`.

## Historical/current coexistence

Semantic scope: Compliance V1. Historical implementation: `compliance-v1/1`, package SHA-256 `2f85c9bd92ad603bab696e34c886b3f85ac22c05ba7aa0e90dc10137bb061981`. Current approved implementation: `compliance-v1/2`, package SHA-256 `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`. La DB y los artefactos históricos conservan bytes; el pointer y el sidecar de transición identifican v2 sin reescribirlos.

## Future HOLDOUT V2 engine identity preparation

Identidad preparada solo para checkpoint futuro: commit/merge SHA pendiente; parser `gtfs-lab-csv/2`; validator `1.0.0`; ruleset `gtfs-lab-v1/1`; Compliance evaluator `compliance-v1/2` y SHA anterior; package SHA aprobado anterior; split SHA `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d`. No se creó registro de acceso HOLDOUT V2.

## N. Verdict

`M04B2_COMPLIANCE_V2_APPROVED_FROZEN_AND_GATE_PASS`. M04 no se declara completo ni `TDL_TRUST_FOUNDATION = PASS`. HOLDOUT V2 no se ejecutó. PR #9 sigue Draft y sin merge.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
