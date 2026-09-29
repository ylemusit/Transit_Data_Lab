# GTFS_Lab M03-A — Golden Case Contract

Estado: contrato y gate implementados para revisión; no existe corpus aprobado ni Golden Regression Gate. Versión del contrato: `GoldenCase 1.0.0`.

## Objetivo y distinción

Un `Test fixture` es una entrada sintética para comprobar una propiedad del software y puede cambiar con la prueba. Un `Golden Case` fija una entrada identificada por hash y expectativas revisadas, justificadas y aceptadas para detectar regresiones dentro de un scope explícito. No describe automáticamente el output actual. Los fixtures inventariados abajo son candidatos, nunca golden por el mero hecho de pasar un gate.

| fixture | purpose_actual | candidate_golden | reason | ambiguity | external_authority_needed |
|---|---|---|---|---|---|
| GTFS_Lab `VALID_MINIMAL` | Smoke test de pipeline y Compliance adapter | REQUIRES_REVIEW | ZIP sintético y reproducible | Scope de reglas que debe fijarse | No para invariantes; sí para claims normativos |
| GTFS_Lab `ORPHAN_TRIP`, `ORPHAN_STOP`, `ORPHAN_ROUTE` | Referencias rotas | REQUIRES_REVIEW | Casos negativos focales | Expected rule/status nace de implementación actual | GTFS specification y revisión humana |
| GTFS_Lab `BAD_SERVICE_REFERENCE`, `BAD_SHAPE_REFERENCE` | Integridad de referencias | REQUIRES_REVIEW | Prueban relaciones concretas | Scope/calendar y semántica shape | GTFS specification |
| GTFS_Lab `MALFORMED_CSV`, `MISSING_HEADER`, `MISSING_FILE`, `PARTIAL_FEED`, `UNSUPPORTED_TABLE` | Límites de ingesta/esquema | NOT_SUITABLE | Fixtures de infraestructura y errores del adaptador | Resultados muy ligados a límites del motor | No; para referencia estable exigiría rediseño de propósito |
| GTFS_Lab `ZIP_PATH_TRAVERSAL`, `ZIP_DUPLICATE_MEMBER` | Seguridad de ingesta ZIP | NOT_SUITABLE | Casos defensivos del gate | No expresan expectativa funcional de feed | No |
| Compliance V1 `gtfs-valid`, `gtfs-broken-stop`, `gtfs-broken-trip`, `gtfs-missing-value`, `gtfs-boundary` | Casos sintéticos de regla GTFS congelada | REQUIRES_REVIEW | Inputs documentados en manifest y hashes por archivo | Expectativas `PASS/FAIL_TECHNICAL` requieren confirmar predicado y scope | GTFS specification + revisión humana |
| Compliance V1 otros fixtures GTFS: `gtfs-schema-mismatch`, `gtfs-ragged`, `gtfs-duplicate-parent`, `gtfs-empty-target`, `gtfs-duplicate-header`, `gtfs-parser-failure`, `gtfs-malformed`, `gtfs-missing-file`, `gtfs-wrong-version`, `gtfs-partial-inspection`, `gtfs-flex`, `gtfs-station-reference`, `gtfs-unexpected-enum` | Límites, errores, versiones y valores GTFS | NOT_SUITABLE | Son pruebas de robustez/alcance del motor | Estados informativos del evaluador no equivalen a verdad normativa | Sí para interpretación de especificación |
| Compliance V1 NeTEx: `netex-valid`, `netex-missing-name`, `netex-boundary`, `netex-unknown-enum`, `netex-malformed`, `netex-unknown-profile`, `netex-partial-inspection`, `netex-namespace`, `netex-external-entity`, `netex-missing-id` | Pruebas de fragmento EPIP/XSD | NOT_SUITABLE | Pertenece a Compliance, y el fragmento no constituye feed GTFS | Alcance XSD/perfil | Sí; fuera de M03-A GTFS Golden Cases |
| `golden/cases/contract-smoke/input.zip` | Ejemplo de forma/hash del contrato | NOT_SUITABLE | Solo ejercita metadatos del contrato | No afirma comportamiento del motor | No |

`PUBLIC_DATASET`/`OPERATOR_PROVIDED` solo se usarán con procedencia comprobable. Los fixtures existentes se referencian mediante path relativo estable y SHA; no se copian. El ejemplo M03-A sí guarda un ZIP mínimo propio para que sea autocontenido. Todos los casos siguen DRAFT.

## Contrato

Cada `case.json` contiene `case_id`, `case_version`, `contract_version`, `status`, `purpose`, `created_at_utc`, `input` (`filename`, `sha256`, `format`, `provenance`), `scope`, `expected`, `excluded_expectations`, `authority`, `review` y `engine_context`. `GTFS_STATIC_ZIP` es el formato de ZIP GTFS. `filename` se resuelve desde el directorio del caso, debe existir dentro de ese directorio y su SHA-256 debe coincidir. Se rechazan paths absolutos Windows/POSIX y traversal (`..`), incluido escape al resolver symlinks: `PATH_CONTAINMENT_ENFORCED`.

`case_id` y `case_version` deben ser strings no vacíos tras `strip`; no hay gramática de formato adicional y no se interpretan como rutas. El gate rechaza `case_id` whitespace-only.

Las expectativas son objetos `{type, target, value, authority}`. Tipos aceptados por el código: `EXACT`, `SEMANTIC`, `STATUS`, `COUNT`, `PRESENCE`, `ABSENCE`, `RELATION`, `HASH`. El contrato separa igualdad byte a byte (`EXACT`/`HASH`) de significado (`SEMANTIC`, `STATUS`, `COUNT`, `PRESENCE`, `ABSENCE`, `RELATION`). M03-A valida su estructura, no implementa la evaluación de esos tipos. El ejemplo vincula su expectativa a `SYNTHETIC_INVARIANT`; no incluye output observado del motor ni usa el motor como autoridad.

No se convierten automáticamente en expectativas `run_id`, timestamps de ejecución, paths absolutos/locales, temporales ni metadatos de máquina. No se eliminan de outputs productivos. `GoldenCaseResult` queda especificado conceptualmente con `case_id`, `case_version`, `run_id`, `dataset_id`, `engine_context`, `status`, `expectation_results` y `unexpected_differences`; estados `PASS`, `FAIL_EXPECTATION`, `NOT_EVALUABLE`, `EXECUTION_ERROR`. No hay scoring ni porcentajes.

## Lifecycle, autoridad y revisión

Estados: `DRAFT → UNDER_REVIEW → APPROVED → SUPERSEDED` o `RETIRED` (y retiro desde estados no aprobados). `is_executable_authority(case)` solo considera elegible el estado `APPROVED`; la elegibilidad no ejecuta expectativas ni acredita la veracidad de la revisión declarada. PASS/FAIL pertenece a `GoldenCaseResult`, nunca al status del caso. `DRAFT` no entra en gate regresivo.

Bases permitidas: `TDL_CONTRACT`, `GTFS_SPECIFICATION`, `COMPLIANCE_FROZEN_SCOPE`, `HUMAN_REVIEW`, `SYNTHETIC_INVARIANT`. La base se declara por expectativa; una regla técnica congelada no se presenta como obligación legal. `APPROVED` requiere `reviewed_by`, `reviewed_at_utc` en UTC explícito y `review_basis`; no se inventan revisores.

`engine_context` exige `gtfs_lab_version`, `validator_version`, `ruleset_id`, `ruleset_version` como provenance, no como pin de validez: una versión nueva puede satisfacer la misma expectativa. Se registran identidades de dataset/ruleset/engine en resultados futuros, pero no se atribuye causalidad automáticamente.

## Cambios y límites

Una expectativa aprobada no se edita silenciosamente: crear nueva `case_version`, conservar la anterior y documentar razón entre `DATASET_CORRECTION`, `SPEC_INTERPRETATION_CHANGED`, `RULESET_CHANGED`, `ENGINE_DEFECT_CORRECTED`, `GOLDEN_CASE_DEFECT`, `SCOPE_CHANGED`; opcionalmente marcarla `SUPERSEDED`. El gate M03-A no detecta mutaciones históricas sin un registro externo firmado/versionado. Ese enforcement se aplaza; Git history por sí sola no se trata como mecanismo contractual.

Protección contra “approve current behavior”: se rechazan marcadores `CURRENT_OUTPUT`, `AUTO_GENERATED`, `AUTO_ACCEPTED`; el gate no captura outputs del motor para generar expectations. La aprobación exige revisión declarada. El gate comprueba metadatos, no autoridad real del revisor ni validez normativa. El ZIP mínimo es DRAFT y no demuestra que el validador devuelva PASS.

## Gate y siguiente fase

`python -m gtfs_lab.golden_contract_gate` valida el contrato y casos negativos: SHA ausente/incorrecto, input ausente, status desconocido, APPROVED sin revisor, timestamp naïve, expectation sin tipo/authority, path absoluto Windows, ID vacío, versión desconocida y expectation derivada de output. También demuestra que mutaciones de caso aprobado requieren mecanismo posterior.

M03-B podrá seleccionar casos tras review explícita, definir evaluación de expectations y resultados GoldenCaseResult y decidir mecanismo durable de cambios. No comenzar M03-B como parte de este cambio.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
