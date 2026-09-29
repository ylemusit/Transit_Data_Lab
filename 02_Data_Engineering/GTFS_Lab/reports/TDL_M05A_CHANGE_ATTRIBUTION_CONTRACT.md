# TDL Trust Foundation M05A — Change Attribution Contract

**Estado:** `M05A_CHANGE_ATTRIBUTION_CONTRACT_READY_FOR_REVIEW`\
**Contrato:** `ChangeAttribution 1.0.0`\
**Base:** `bd00902f892462e1caa007ff99287bb986f91393` (`origin/main`, post-M04)\
**Alcance:** contrato determinista y demostración sintética; no es el comparador productivo final.

## Contrato e identidad

La API `gtfs_lab.change_attribution.compare(baseline, candidate)` consume dos snapshots que contienen `audit_id`, `identity`, `result` y `findings`; devuelve un diccionario JSON serializable. El ID de comparación se deriva de forma estable de ambos IDs de auditoría. Las diferencias se recorren por nombres de campo y `rule_id`, nunca por orden de filas.

La identidad opcional se organiza en `dataset`, `engine`, `rules`, `compliance` y `configuration`. Se comparan literalmente las identidades declaradas; los campos SHA-256 se validan como hashes de 64 caracteres y se comparan sin distinguir mayúsculas. `dataset_change` solo se activa si ambos hashes de fuente existen y difieren. Un cambio de commit se etiqueta como cambio de implementación y nunca demuestra por sí solo un cambio semántico.

Se separan parser/validator/evaluador y hashes de implementación, versión/definición semántica de regla, ruleset, paquete Compliance, referencias y configuración. Run/audit ID, timestamp y paths runtime se excluyen de la comparación semántica; si solo cambian metadatos runtime, la atribución es `RUNTIME_ONLY_CHANGE`.

## Finding y RuleResult

Las reglas se indexan por `rule_id`. Se informa `RULE_NEW`, `RULE_REMOVED`, `STATUS_CHANGED`, `FINDING_COUNT_CHANGED`, `FINDING_SET_CHANGED` o `NOT_COMPARABLE`; el orden no cuenta como cambio. Findings se emparejan por `finding_id` o por el contrato M01 `stable_finding_id`. Se reportan `NEW_FINDING`, `RESOLVED_FINDING`, `FINDING_STATUS_CHANGE` y `FINDING_EVIDENCE_CHANGE`. Metadatos de evidencia modificados con identidad estable no crean un finding nuevo.

Los cambios de findings son resultados (`finding_change`) y no causas automáticas. Por ejemplo, dataset atribuido y finding nuevo se registran en sus campos separados. Ante causas independientes, `attribution = MULTIPLE_CAUSES` y `supported_causes` enumera todas. Un cambio de resultado sin identidad causal sustentada queda `UNATTRIBUTED_CHANGE`. Identidades ausentes se declaran `MISSING_IDENTITY`; nunca se rellenan por inferencia.

## Categorías

El modelo admite `NO_CHANGE`, `DATASET_CHANGE`, `PARSER_IMPLEMENTATION_CHANGE`, `VALIDATOR_IMPLEMENTATION_CHANGE`, `ENGINE_IMPLEMENTATION_CHANGE`, `RULESET_CHANGE`, `RULE_SEMANTIC_CHANGE`, `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE`, `COMPLIANCE_PACKAGE_CHANGE`, `REFERENCE_CHANGE`, `CONFIGURATION_CHANGE`, `RUNTIME_ONLY_CHANGE`, `MULTIPLE_CAUSES` y `UNATTRIBUTED_CHANGE`. El ciclo de findings se expresa en `finding_change` con `NEW_FINDING`, `RESOLVED_FINDING`, `FINDING_STATUS_CHANGE` o `FINDING_EVIDENCE_CHANGE`.

## Matriz sintética determinista

| Caso | Cambio probado | Resultado esperado |
|---|---|---|
| CA-001 | Auditorías idénticas | `NO_CHANGE` |
| CA-002 | Identidad parser; resultados iguales | `PARSER_IMPLEMENTATION_CHANGE`, resultado sin cambio |
| CA-003 | Evaluador Compliance v1→v2; semántica igual | `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE` |
| CA-004 | SHA dataset distinto; resultado igual | `DATASET_CHANGE` |
| CA-005 | Dataset distinto y finding nuevo | `DATASET_CHANGE` + `NEW_FINDING` |
| CA-006 | Versión semántica de regla y resultado cambian | `RULE_SEMANTIC_CHANGE` + `STATUS_CHANGED` |
| CA-007 | Solo audit/run IDs y timestamp | `RUNTIME_ONLY_CHANGE` |
| CA-008 | Finding desaparece | `RESOLVED_FINDING` |
| CA-009 | Dataset y ruleset cambian | `MULTIPLE_CAUSES` con ambos motivos |
| CA-010 | Resultado cambia con identidades conocidas iguales | `UNATTRIBUTED_CHANGE` |

La prueba añade lifecycle/evidencia de findings, hash de paquete/referencia/configuración, SHA inválido, identidad de regla semántica y permutación de filas.

## Relación con M04 y límites

M04 se usó solo como referencia conceptual: actualización parser/evaluador con hashes de datos y semántica de Compliance sin cambio, además de cambios de evaluabilidad. No se cargó evidencia de M04 como fixture ni se ejecutó HOLDOUT. Este módulo compara snapshots dados; no ejecuta motores ni afirma causalidad fuera de las identidades presentes. `evidence_refs` devuelve rutas de identidad que sustentan las diferencias; cuando no hay identidad causal, se conserva la razón no atribuida.

El gate no prueba productor ni persistencia de snapshots. M05 posterior puede definir la ingestión/versionado de snapshots y enlazar evidencia persistida; este contrato no declara M05 terminado.

## Verificación

- M05A: 16 pruebas sintéticas PASS, CA-001…CA-010 y seis casos de borde.
- M01: `TDL_TRUST_CONTRACT_GATE` PASS (12/12).
- M02: `TDL_TRUST_PERSISTENCE_GATE` PASS (21/21).
- M03-A: Golden Contract PASS (18/18); Golden Corpus PASS; Golden Evaluator PASS (11/11); Golden Regression PASS (2 casos y controles negativos).
- Split/lineage persistido: PASS. Suite GTFS_Lab: 68/68 PASS.
- Compliance V1 current strict: PASS; 386 checks actuales y el FAIL histórico `UNCHANGED_COUNT_audit.rules` sigue identificado como histórico por el gate. Hash inicial/final Compliance idéntico `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`.
- `compileall` para `gtfs_lab` y `tests`: PASS. `git diff --check`: PASS.
- M04 histórico y evidencia protegida no se modificaron; HOLDOUT no se ejecutó.

Las evidencias generadas por gates se escriben en `%TEMP%`, fuera del repositorio. Para gates que requieren las bases omitidas por Git se usaron junctions temporales a los DuckDB protegidos, solo en lectura: Compliance `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` y GTFS raw `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`; ambos hashes se volvieron a comprobar sin cambios.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
