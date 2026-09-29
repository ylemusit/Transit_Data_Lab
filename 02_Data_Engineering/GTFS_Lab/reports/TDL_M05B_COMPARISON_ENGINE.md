# TDL Trust Foundation M05-B — Productive Comparison Engine

**Estado:** `M05B_COMPARISON_ENGINE_READY_FOR_REVIEW` (sujeto a regresiones y revisión del cambio)
**Base:** `1d10dddae53e282ed5dcc001a6722a4401c99eb7`
**Entrada:** snapshots leídos de runs persistidos; comparación de solo lectura.
**Contratos:** `AuditComparisonSnapshot 1.0.0` y `ChangeAttribution 1.0.0` son contratos distintos.

## Snapshot de entrada

`gtfs_lab.audit_comparison.build_audit_snapshot(run_directory)` produce un objeto JSON serializable a partir de `audit/audit_manifest.json`, `run.json`, `validation.json` y `audit/findings.normalized.json`. Solo acepta un manifest M01 válido y evidencia aceptada. Los paths de artifacts se resuelven dentro del directorio del run. La versión del snapshot se asigna explícitamente como `AuditComparisonSnapshot 1.0.0`; no se reutiliza la versión del manifest.

El snapshot contiene `audit_id`, identidad por grupos `dataset`, `engine`, `rules`, `compliance` y `configuration`, `result.rules`, `findings` y `missing_identity`. Las reglas y findings se ordenan por identidad estable. El productor comprueba IDs únicos de regla, IDs de finding M01, integridad estructural, hash del dataset y la reconciliación entre findings normalizados y resultados por regla. No usa timestamps, orden de filas, paths locales ni hashes recalculados como identidad semántica.

Las identidades salen de artifacts existentes: hash/ID del dataset y versiones de motor/parser/validator/ruleset del manifest; resultados del `validation.json`; findings normalizados M02; y versiones/hashes de Compliance presentes en `run.json`. No se persisten actualmente `lineage_id`, commit de Git ni hash de configuración; esos valores quedan `null` y se enumeran explícitamente. `rule_version` solo se expone como identidad común cuando todas las reglas ejecutadas declaran la misma versión. No se sintetizan hashes de paquete o referencia que no estén en los artifacts.

**Límite del contrato M05-A observado:** `ChangeAttribution 1.0.0` atribuye la semántica mediante un único `rules.rule_version`. Los manifests reales también guardan un mapa por regla; si ese mapa cambia y no existe una versión escalar común, M05-B devuelve `NOT_COMPARABLE` con `RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0`. Así evita etiquetar el cambio como `NO_CHANGE` o redefinir silenciosamente M05-A. La prueba PB-006 valida el caso que el contrato escalar representa; el caso multiversión queda cubierto como fail-closed.

## API y CLI

- `build_audit_snapshot(run_directory) -> dict`
- `compare_audits(baseline, candidate) -> dict`
- `compare_audit_directories(baseline_directory, candidate_directory) -> dict`
- `python -m gtfs_lab.audit_comparison <baseline-run-dir> <candidate-run-dir>`

El comparador comprueba compatibilidad antes de llamar a `change_attribution.compare()`. El JSON de salida incluye `comparison_id`, ambas versiones de contrato, audit IDs, estado y razones de comparabilidad, diferencias de identidad/resultados/findings, atribución, causas respaldadas, estado de evidencia, referencias y razones no resueltas. La CLI imprime JSON canónico y termina con código 2 cuando el par no es comparable o la entrada es inválida.

## Comparabilidad y errores

- `COMPARABLE`: contratos compatibles y las identidades obligatorias están presentes.
- `PARTIALLY_COMPARABLE`: las identidades obligatorias existen, pero faltan identidades opcionales; el resultado incluye cuáles faltan.
- `NOT_COMPARABLE`: falta hash de fuente, parser/validator/motor, ruleset o resultado estructurado; o las versiones de snapshot no coinciden/no están soportadas. No se fuerza atribución.

Los errores de construcción usan `SNAPSHOT_INVALID`, `FINDING_IDENTITY_INVALID`, `DUPLICATE_RULE_ID` o `NOT_COMPARABLE`. La comparación incompatible se devuelve con `attribution=NOT_COMPARABLE`. No se capturan fallos para convertirlos en `NO_CHANGE`.

## Matriz productiva

La suite `tests/test_audit_comparison.py` prepara artefactos representativos M01/M02 y cubre PB-001…PB-012: repetición idéntica, solo IDs de run, cambio de SHA de dataset, parser, evaluador, regla semántica, finding nuevo/resuelto, causas múltiples, resultado no atribuido, identidad obligatoria ausente y versión incompatible. Añade lifecycle/evidencia de finding, identidad opcional parcial, regla duplicada y JSON corrupto. Se conserva intacta la suite M05-A `test_change_attribution_contract.py`.

## Límites y evidencia protegida

La comparación no ejecuta validadores, Compliance ni ingesta, y no escribe en DB, auditoría, findings o lifecycle. No usa evidencia M04 histórica para pruebas ni ejecuta HOLDOUT; PB se demuestra con artifacts sintéticos aislados. Los manifests M01 no declaran hashes de cada artifact; el productor valida estructura y concordancias disponibles, pero no puede probar que un JSON estructuralmente válido no haya sido alterado. La falta de lineage/commit/configuración mantiene comparaciones en `PARTIALLY_COMPARABLE` y limita causalidad. La salida es atribución técnica según identidades declaradas, no conclusión jurídica ni causalidad externa.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
