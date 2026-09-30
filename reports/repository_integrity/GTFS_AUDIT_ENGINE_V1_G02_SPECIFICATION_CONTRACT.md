# GTFS Audit Engine V1 — G02 Rule Registry + Specification Contract

Fecha: 2026-09-30. Estado: `IMPLEMENTED_NOT_MERGED` sujeto a revisión. Base: `d7f4c76ce5c13844ea49303f0434f83d31d95a4c`. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Alcance y titularidad

`gtfs_lab.rule_registry` es propietario del conjunto tipado de reglas declarado para una ejecución nueva. G02 define arquitectura ejecutable, pero no conecta este registro con `validation.py`, `pipeline.py` ni hallazgos productivos. No añade findings de operadores ni cambia los resultados GTFS_Lab V1. La especificación describe el contrato; el registro entrega las definiciones concretas.

Cada `RuleDefinition` contiene ID estable, versión semántica independiente, categoría, autoridad, severidad, tipo de requisito, archivos aplicables, referencia de especificación, expresión de applicability, identidad del evaluator y cobertura declarada. IDs vacíos/duplicados, SemVer inválido y valores no soportados se rechazan. No existe configuración específica por operador.

## Identidad y versión

`RuleRegistry.identity_map()` produce un mapa ordenado `{"rule_versions": {"GTFS-...": "1.0.0"}}` con todas las reglas registradas, incluso sin findings y aunque su disposición sea `NOT_APPLICABLE` o `NOT_EVALUABLE`. Antes de ejecutar se llama `freeze()`; desde entonces `register()` falla y la identidad describe el conjunto exacto congelado. ChangeAttribution 1.1.0 recibe este mapa como `identity.rules.rule_versions`; compara cambios por ID, incluso para reglas no aplicables. Un mapa vacío es válido para representar la eliminación de la última regla.

La revisión de la especificación GTFS `2026-04-27` es identidad de referencia y no es la versión semántica de una regla. Cambiar una regla requiere incrementar el SemVer de esa regla; no se deriva del número de revisión GTFS ni de la implementación del evaluator.

## Applicability

Las expresiones soportan `SIGNAL_PRESENT`, `SIGNAL_EQUALS`, `ALL`, `ANY` y `NOT`. Las señales faltantes o nulas producen `UNKNOWN`; la evaluación devuelve TRUE/FALSE/UNKNOWN junto con una traza determinista con condición, señal observada y motivo de decisión. TRUE autoriza evaluar el evaluator; FALSE produce `NOT_APPLICABLE`; UNKNOWN produce `NOT_EVALUABLE`. Ninguno de estos dos últimos estados equivale a parser error, función no soportada o inspección fallida.

`NOT_APPLICABLE` significa que la regla es válida y soportada, pero su precondición es falsa para este dataset. Si translations no está presente, una regla condicional a translations no aplica; si está presente y falta `feed_info`, la regla aplicable puede fallar. Ausencia de señal necesaria para decidir es `NOT_EVALUABLE`, nunca una certeza fabricada.

## Resultado, severidad y compatibilidad legacy

El contrato nativo `EngineRuleResult 2.0.0` acepta exclusivamente `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `NOT_APPLICABLE` e `INSPECTION_ERROR`. Severidad es un eje independiente: `ERROR`, `WARNING` o `INFO`. `WARNING` deja de ser estado solo en el contrato nuevo.

El normalizador legacy conserva `WARNING` como estado y los valores históricos de severidad. La compatibilidad es explícita por rutas distintas: no se transforma un payload histórico ni se normaliza implícitamente legacy `WARNING` a un estado nuevo. El contrato de resultado engine-native se versiona como `2.0.0`; `MANIFEST_VERSION = 1.1.2` no cambia y sus semánticas persistidas siguen intactas. Los artefactos G02 pueden añadir `identity.rules.rule_versions` cuando persistencia recibe el parámetro optativo autoritativo `rule_identity_map`; la ruta V1 sin ese parámetro conserva su serialización.

## Autoridad, requisito y cobertura

`authority` identifica la base de autoridad (`GTFS_SPECIFICATION` o `TDL_CONTRACT`); `requirement` expresa `REQUIRED`, `RECOMMENDED` o `CONDITIONAL`. No se confunden severidad ni autoridad con resultado.

`RuleCoverage` representa presencia del feature y soporte de auditoría aparte de RuleResult: `FEATURE_NOT_PRESENT`, `FEATURE_PRESENT_FULLY_AUDITED`, `FEATURE_PRESENT_PARTIALLY_AUDITED` y `FEATURE_PRESENT_DEFERRED`. Combinaciones contradictorias se rechazan. Un feature presente diferido (`presence=PRESENT`, `audit_support=DEFERRED`) es metadato de cobertura y no genera finding ni `FAIL_TECHNICAL` por sí solo.

## Persistencia y ChangeAttribution

Persistencia acepta `rule_identity_map` explícito y persiste el mismo mapa en `identity.rules.rule_versions`, `executed_rule_versions` e IDs ejecutados. Este origen incluye reglas PASS sin hallazgos, NOT_APPLICABLE, NOT_EVALUABLE y cualquier regla registrada sin finding. No reconstruye el mapa desde `validation.rules` cuando se suministra identidad; sin ella, se mantiene la derivación legacy actual. ChangeAttribution 1.1.0 compara mapa sin cambios, cambio semántico, alta, baja y cambios de versión con estado no aplicable. Los snapshots ChangeAttribution 1.0.0 siguen en su comparador original; mezclar contratos continúa `NOT_COMPARABLE`, sin inferir identidad histórica ausente.

## Frontera de migración

La validación legacy y sus siete salidas permanecen intactas en G02. No se conectan todavía reglas productivas al registry, no se reescribe evidencia histórica y no se declara equivalencia de resultados GTFS. Una migración posterior deberá comparar explícitamente salidas legacy/nuevas antes de adopción.

## Evidencia y estado

Verificación local sobre esta rama/base:

| Comprobación | Resultado |
| --- | --- |
| `python -m unittest tests.test_g02_rule_registry -v` | 8 tests PASS; cubre registro, expresiones, estados, cobertura, ChangeAttribution y persistencia explícita. |
| `python -m unittest tests.test_change_attribution_contract -v` | 16 tests PASS (ChangeAttribution 1.0.0). |
| `python -m unittest tests.test_audit_comparison -v` | 23 tests PASS; incluye pipeline GTFS con fixtures sintéticos y comparación/persistencia. |
| `python -m unittest tests.test_engine_preconditions -v` | 10 tests PASS (ChangeAttribution 1.1.0 y precondiciones sintéticas). |
| `python -m gtfs_lab.trust_persistence_gate --output <directorio-temporal-nuevo>` | PASS, 21 comprobaciones M02. |
| `python -m compileall -q tools 02_Data_Engineering/GTFS_Lab/gtfs_lab 02_Data_Engineering/GTFS_Lab/tests` | PASS. |
| `git diff --check d7f4c76ce5c13844ea49303f0434f83d31d95a4c` | PASS. |

No se ejecutaron gates ni pruebas del split/lineage que consultan inventarios HOLDOUT. No se accedió a datasets HOLDOUT. El total focalizado es 57 tests PASS, más 21 comprobaciones del gate M02. Este estado no es un PASS de gate humano ni un merge: `G02 = IMPLEMENTED_NOT_MERGED` queda sujeto a revisión de código y Draft PR.
