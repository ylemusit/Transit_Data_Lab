# TDL Trust Foundation — cierre técnico M05

**Base de `main`:** `03d4283ccb6e774241bf77e7c8039c518b0d07af`.
**Decisión en esta rama:** `M05_CHANGE_ATTRIBUTION = PASS`; `M05_CLOSURE_READY_FOR_REVIEW`.
**Trust Foundation:** `TDL_TRUST_FOUNDATION_READY_FOR_PASS`. El PASS técnico propuesto en este documento será estado vigente de `main` tras revisar y fusionar la PR de cierre.

## Pregunta de cierre

**Sí, dentro de las identidades y la evidencia persistidas.** Dos auditorías M01/M02 se reconstruyen como snapshots M05-B sin volver a ejecutar sus datasets. M05-A separa diferencias de resultados y findings de las causas respaldadas por identidad, conserva `UNATTRIBUTED_CHANGE` o `NOT_COMPARABLE` cuando falta soporte, y M05-D guarda el resultado, sus referencias y hashes en un registro reproducible. La prueba productiva `CA-20dd6212be68afda` y la prueba histórica `M05C-HISTORICAL-PROOF-V1` verifican las dos rutas.

## Cadena contractual y evidencia

| Hito | Contrato o adaptador | Evidencia vigente |
| --- | --- | --- |
| M05-A | `ChangeAttribution 1.0.0` | [Contrato y matriz CA](TDL_M05A_CHANGE_ATTRIBUTION_CONTRACT.md); `tests/test_change_attribution_contract.py`; merge `1d10dddae53e282ed5dcc001a6722a4401c99eb7` |
| M05-B | `AuditComparisonSnapshot 1.0.0` → M05-A | [Motor y matriz PB](TDL_M05B_COMPARISON_ENGINE.md); `gtfs_lab/audit_comparison.py`; merge `00ccb10` |
| M05-C | Adaptador de resúmenes M04 B1/B3 → M05-A | [Prueba histórica](TDL_M05C_HISTORICAL_PROOF.md); `reports/evidence/m05c_historical_proof/summary.json`; merge `9a54144f51c16cfaa4d5dc8cecbdfe2149cb1c65` |
| M05-D | `AuditComparisonRecord 1.0.0` envuelve resultado y versión del snapshot | [Persistencia](TDL_M05D_PERSISTENCE_REPORTING.md); dos pares canónicos JSON/Markdown; merge `03d4283ccb6e774241bf77e7c8039c518b0d07af` |

La ruta histórica usa explícitamente `M05CHistoricalSourceSnapshot 1.0.0`, no se hace pasar por un `AuditComparisonSnapshot` productivo. Ambos resultados declaran `ChangeAttribution 1.0.0`; el registro conserva la versión real del snapshot. M05-B y M05-C rechazan el cambio de versiones de regla por regla que no cabe en la identidad escalar de M05-A con `RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0`. No hay normalización oculta ni semántica duplicada. La clasificación M04-B3 `NO_CHANGE` de 006 describe el estado del resultado; M05-C registra aparte los cambios de identidad de parser y evaluator como `MULTIPLE_CAUSES`, con resultado `UNCHANGED_STATUS`.

## Capacidades comprobadas

| Capacidad | Comprobación |
| --- | --- |
| Dataset; parser, validator y evaluator; ruleset y regla semántica; paquete, referencia y configuración; solo runtime; múltiples causas; cambio no atribuido | Matrices CA y PB en la suite completa. Solo una diferencia de SHA de fuente sustenta `DATASET_CHANGE`; un commit no prueba cambio semántico. |
| `NEW_FINDING`, `RESOLVED_FINDING`, `FINDING_STATUS_CHANGE`, `FINDING_EVIDENCE_CHANGE` | Tests CA/PB de identidad estable y lifecycle; el cambio del conjunto de findings también consta en `CA-20dd6212be68afda`. |
| Identidad ausente, evidencia parcial, incompatibilidad y lagunas históricas | Tests de rechazo/`NOT_COMPARABLE`; M05-C mantiene 008 no comparable y los otros cinco como parciales. |
| Registro canónico, cuatro SHA-256, idempotencia, conflicto, informe determinista y referencias duraderas | Tests PD; lectura y verificación directas de ambos registros; repetición productiva sin cambiar bytes ni fechas de escritura. |

## Pruebas persistidas

**Histórica M04 B1 → B3.** `M05C-HISTORICAL-PROOF-V1` conserva seis datasets y cinco unidades lineage; 013 y 015 comparten `LINEAGE-013-015`. 006: `PARTIAL / MULTIPLE_CAUSES`, con resultados sin cambio. 008: `NOT_COMPARABLE`, porque B1 no guardó resultados de reglas. 013, 015, 017 y 018: `PARTIAL / MULTIPLE_CAUSES`. Las tres referencias del registro resuelven; los punteros JSON de cada fila señalan el dataset correcto; coinciden los SHA de los resúmenes M04, los cuatro hashes del registro y el Markdown renderizado. Esto verifica el adaptador sobre resúmenes ya guardados, sin revalidar el análisis original.

**Productiva.** `CA-20dd6212be68afda` se reconstruye de los ocho JSON productivos M01/M02. Las cuatro referencias resuelven, `compare_audits` reproduce exactamente el payload, `DATASET_CHANGE` está respaldado por la identidad de fuente y cambia el conjunto de findings. Coinciden los cuatro hashes y el informe. La segunda persistencia conservó bytes y fechas de escritura de JSON y Markdown.

## Límites preservados

- `RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0` produce `NOT_COMPARABLE` cuando corresponde.
- B1 no persistió listas de warnings; en 008 tampoco hay resultados de reglas B1.
- B3 no persistió la versión global GTFS_Lab; la identidad de paquete Compliance B1 no está disponible.
- Los snapshots productivos no prueban la integridad criptográfica individual de cada JSON fuente M01/M02; se verifican las concordancias disponibles y los hashes del registro M05-D.
- El resultado técnico no prueba causalidad externa, cumplimiento jurídico, validación comercial, auditoría GTFS completa ni preparación NeTEx completa.

## Principios de confianza

`NO FABRICATED CAUSALITY`: una diferencia de findings no se convierte por sí sola en causa; existe `UNATTRIBUTED_CHANGE`. `NO SILENT HISTORICAL NORMALIZATION`: identidades y warnings ausentes permanecen explícitos. `NO HOLDOUT TUNING`: esta operación no ejecutó HOLDOUT ni modificó código o umbrales. `NO RESULT OVERWRITE` y `NO EVIDENCE OVERWRITE`: los resultados M04 y registros M05 anteriores permanecen intactos; la persistencia repetida es idempotente. `FAIL CLOSED ON CONFLICT`: payload o hash alterado se rechaza. `PERSIST MINIMAL EVIDENCE`: los registros refieren artifacts y guardan solo ocho JSON productivos, sin copiar runs completos. `REPRODUCIBLE WITHOUT SOURCE RERUN`: ambos registros se verificaron desde artifacts persistidos.

## Regresión y estado protegido

En checkout aislado desde la base indicada: suite GTFS_Lab **97/97 PASS** (incluye M05-A/B/C/D); M01 **12/12 PASS**; M02 **21/21 PASS**; M03-A **18/18 PASS**; Golden Corpus y Golden Evaluator **PASS**; Golden Regression **2 casos PASS**; split y lineage **PASS**; GTFS_Lab V1 gate **PASS**; Compliance strict **PASS**; `compileall` y `git diff --check` **PASS**. Compliance strict conserva su fallo histórico identificado `UNCHANGED_COUNT_audit.rules`, separado de los 386 checks actuales que pasan. Los outputs de regresión se guardaron fuera del repositorio y no forman parte de esta PR.

SHA-256 protegidos: GTFS DB `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`; Compliance DB `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` antes y después del gate; checkpoint M04 V2 `CEEEC24A72211DD0F0B59A663C3AF34C3697820FEACA015384DFDF534392C978`. Split, resúmenes M04 y [cierre humano M04](evidence/holdout_evaluation_v2/human_closure.json) no se modificaron respecto de la base. La decisión humana M04 `APPROVE` del `2026-09-29T18:03:08Z` mantiene aceptada la limitación `HOLDOUT_V2_HASH_ACCESS_TIMESTAMP_NOT_CAPTURED`. No se abrieron ZIP de fuentes HOLDOUT; solo se leyeron resúmenes históricos persistidos. Golden Regression utilizó fixtures sintéticos aprobados.

## Decisión técnica

M01 **PASS**, M02 **PASS**, M03 **PASS** dentro de la autoridad de sus dos Golden Cases aprobados, M04 **PASS** con su cierre humano y limitación aceptada, y M05 **PASS** para la pregunta de cierre definida arriba. Se propone `TDL_TRUST_FOUNDATION = PASS` como gate **técnico** tras la revisión y fusión de esta PR. Hasta entonces, el estado publicable de `main` es `TDL_TRUST_FOUNDATION_READY_FOR_PASS`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
