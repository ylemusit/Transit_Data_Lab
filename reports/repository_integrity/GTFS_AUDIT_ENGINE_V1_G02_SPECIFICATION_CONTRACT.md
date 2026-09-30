# GTFS Audit Engine V1 — G02 Rule Registry + Specification Contract

Fecha: 2026-09-30. Estado: `CONTRACT_ALIGNED_PENDING_FINAL_REVIEW`. Base: `d7f4c76ce5c13844ea49303f0434f83d31d95a4c`. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Alcance

G02 establece contratos tipados para el registro de reglas, aplicabilidad, resultados y cobertura. No conecta el registro con `validation.py` ni `pipeline.py`, no cambia reglas productivas ni findings, y no implementa G03. `GTFS_AUDIT_ENGINE_V1_G01_SPECIFICATION_BASELINE` es la fuente normativa de las categorías, autoridades, clases de requisito y condiciones. El catálogo normalizado GTFS es referencia técnica y no una afirmación de autoridad jurídica.

## Dimensiones de regla

`category` conserva exactamente la taxonomía G01: `STRUCTURE`, `SCHEMA`, `TYPE_FORMAT`, `IDENTITY`, `REFERENTIAL`, `TEMPORAL`, `SEQUENCE`, `SPATIAL`, `DATA_CONSISTENCY`, `QUALITY`. No se sustituye por agrupaciones de alcance como conformidad técnica, calidad de datos o revisión geoespacial.

`authority` acepta `GTFS_REQUIRED`, `GTFS_CONDITIONAL`, `GTFS_RECOMMENDED`, `TDL_QUALITY`. `requirement` acepta `REQUIRED`, `CONDITIONALLY_REQUIRED`, `OPTIONAL`, `RECOMMENDED`, `PROHIBITED_WHEN`. `severity` (`ERROR`, `WARNING`, `INFO`) es independiente de autoridad y requisito. En consecuencia: **authority != severity** y **requirement != category**.

## Identidad, aplicabilidad y ejecución

`RuleRegistry.freeze()` cierra el conjunto ordenado de definiciones. `identity_map()` devuelve `{"rule_versions": {rule_id: semantic_version}}`, que incluye todas las reglas registradas aunque sean no aplicables, no evaluables, produzcan cero findings o no lleguen a evaluación. Este mapa completo se persiste como `identity.rules.rule_versions`; `registered_rule_ids` y `registered_rule_versions` son conveniencias equivalentes.

La identidad de regla no prueba que su evaluator se haya ejecutado: **rule identity != rule execution**. La persistencia explícita solo incluye en `executed_rule_ids` y `executed_rule_versions` reglas con evidencia `evaluator_executed: true` en el resultado y excluye siempre `NOT_APPLICABLE`. `NOT_EVALUABLE` puede estar marcado como ejecutado únicamente si la evidencia indica que el evaluator sí se invocó; una precondición no satisfecha no lo está. **rule applicability evaluation != evaluator execution**. Un PASS con cero findings sigue figurando como ejecución si lleva esa marca.

La evaluación de applicability produce TRUE, FALSE o UNKNOWN. FALSE da `NOT_APPLICABLE`; UNKNOWN da `NOT_EVALUABLE`; TRUE habilita la ejecución, pero no la afirma. **coverage != status**: la cobertura describe la presencia del feature y el soporte declarado por el motor, no el resultado de una regla. Un feature presente diferido no produce por sí solo finding ni `FAIL_TECHNICAL`.

## Traducción del vocabulario G01 (opción B)

G01 mantiene su vocabulario semántico: `FILE_PRESENT`, `FILE_ABSENT`, `FIELD_PRESENT`, `FIELD_VALUE_EQUALS`, `FIELD_VALUE_IN`, `ENTITY_EXISTS`, `PARENT_ENTITY_EXISTS`, `RELATED_FILE_PRESENT`, `ONE_OF_FILES_PRESENT`, `DEPENDENT_FIELDS`, `ALL`, `ANY`, `NOT` y `ALL_SERVICE_DATES_DEFINED`. `SpecificationCondition` conserva esos operadores en el contrato de entrada. `compile_specification_condition()` los traduce sin pérdida semántica a señales runtime tipadas y `SIGNAL_PRESENT`, `SIGNAL_EQUALS`, `ALL`, `ANY`, `NOT`:

- Predicados de presencia (archivo, campo, entidad, entidad padre o fichero relacionado) usan una señal booleana cuyo valor representa exactamente ese predicado.
- `FILE_ABSENT` niega la señal de presencia del archivo. `FIELD_VALUE_EQUALS` compara el valor inspeccionado con el literal. `FIELD_VALUE_IN` conserva el conjunto G01 en el comparador de señales y comprueba el valor inspeccionado contra ese conjunto.
- `ONE_OF_FILES_PRESENT`, `DEPENDENT_FIELDS` y `ALL_SERVICE_DATES_DEFINED` usan señales booleanas calculadas conforme a su predicado G01, no inferidas de una mera presencia genérica.
- `ALL`, `ANY`, `NOT` conservan estructura y lógica de tres valores. Señal ausente o nula es UNKNOWN, no FALSE.

La construcción de señales es responsabilidad de la capa inspectora futura; este contrato no la conecta al validador productivo. No se permite mapear un predicado a una señal con significado distinto.

## Resultados, cobertura y compatibilidad

`EngineRuleResult 2.0.0` admite `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `NOT_APPLICABLE`, `INSPECTION_ERROR`; severidad permanece separada. La ruta legacy conserva `WARNING` como estado y sus bytes/semántica actuales. `MANIFEST_VERSION = 1.1.2` no cambia.

Cobertura admite `FEATURE_NOT_PRESENT`, `FEATURE_PRESENT_FULLY_AUDITED`, `FEATURE_PRESENT_PARTIALLY_AUDITED`, `FEATURE_PRESENT_DEFERRED` con presencia y soporte coherentes. La cobertura no modifica el estado de resultado.

Sin `rule_identity_map`, persistencia conserva exactamente el comportamiento legacy y no reescribe campos históricos. Con mapa, añade identidad completa y separa evidencia ejecutada mediante el marcador explícito. Los campos legados `executed_rule_ids` y `executed_rule_versions` no se renombran ni se les atribuye la identidad de todo el registry. Los snapshots ChangeAttribution 1.0 permanecen en su comparador; no se infiere identidad ausente.

## ChangeAttribution

ChangeAttribution 1.1 usa `identity.rules.rule_versions` como identidad semántica de regla: mapa sin cambios, cambio semántico, alta, baja y cambio aun con status `NOT_APPLICABLE`. Cada ID y versión individual mantiene la validación vigente. El mapa vacío representa de forma válida el registry vacío (incluida la eliminación de la última regla).

## Frontera de migración

G02 no conecta el registry a la validación productiva, no añade hallazgos GTFS, no accede a datasets HOLDOUT ni ejecuta G03. Cualquier adopción productiva posterior requiere su alcance y revisión propios.

## Verificación

| Comprobación | Resultado local |
| --- | --- |
| G02 focalizado | 10 tests PASS; taxonomía, traducción G01, identidad/ejecución, persistencia y ruta legacy. |
| ChangeAttribution 1.0 | 16 tests PASS. |
| ChangeAttribution 1.1 / precondiciones | 10 tests PASS. |
| Comparación y pipeline sintético | 23 tests PASS. |
| Tests corpus split / lineage review | 23 + 6 tests PASS; metadatos solamente. |
| Persistencia M02 | PASS, 21 checks. |
| Flujo sintético del workflow PR | PASS: fuentes Compliance portables, trust, Golden contract/corpus/evaluator y split/lineage metadata gates. |
| `compileall` | PASS. |
| `git diff --check <base>` | PASS. |

No se leyeron bytes ni se reprodujeron feeds HOLDOUT. Los gates split/lineage anteriores inspeccionan sus metadatos de acuerdo con el workflow; no son validación del dataset. PR #22 continúa OPEN en su HEAD de entrada hasta que estos cambios se publiquen. El check remoto `synthetic` en SUCCESS corresponde a `0cb074d4b4c1e011bd2cc384b61f1c7ee91b7811`, no a esta edición local pendiente.
