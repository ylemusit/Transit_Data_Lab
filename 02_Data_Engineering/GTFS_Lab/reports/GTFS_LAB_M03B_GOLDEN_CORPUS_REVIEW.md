# GTFS_Lab M03-B1 — Golden Corpus V1 para revisión humana

Fecha: 2026-09-29. Estado: `M03B1_CORPUS_READY_FOR_HUMAN_REVIEW`. Ningún candidato está aprobado. La propuesta no es una aprobación técnica ni humana.

## A. Inventario y decisión de candidatos

La tabla registra el propósito de cada candidato, regla/status/finding propuestos, base de autoridad, ambigüedad y decisión. `Expected` es una propuesta previa a la observación del motor. Los casos `ORPHAN_ROUTE` y `BAD_SERVICE_REFERENCE` usan inputs Golden propios; no alteran ni fijan hashes de fixtures de gates.

| Fixture | Propiedad / regla esperada | Status / findings esperados | Authority basis | Ambigüedad | Decisión |
|---|---|---|---|---|---|
| `VALID_MINIMAL` | feed mínimo admitido por el scope de validación V1 | `PASS`; 0 findings de regla | `TDL_CONTRACT` si se limita al subconjunto | El nombre sugiere validez GTFS completa; no cubre semántica condicional/opcional | `KEEP_DRAFT` |
| `ORPHAN_TRIP` | `stop_times.trip_id` sin trip padre; adapter Compliance `V1-RULE-GTFS` | `FAIL_TECHNICAL`; un finding agregado esperado | GTFS Specification para la relación, pero el adapter emite regla agregada | No aísla qué lado de la referencia fija causó el finding | `KEEP_DRAFT` |
| `ORPHAN_STOP` | `stop_times.stop_id` sin stop padre; adapter Compliance `V1-RULE-GTFS` | `FAIL_TECHNICAL`; un finding agregado esperado | GTFS Specification para la relación, pero el adapter emite regla agregada | Regla agregada compartida con trip reference | `KEEP_DRAFT` |
| `ORPHAN_ROUTE` | `trips.route_id` sin ruta padre; `GTFS-REF-TRIP-ROUTE` | `FAIL_TECHNICAL`; 1 finding | `GTFS_SPECIFICATION` | Baja: un viaje y una ruta inexistente deliberada | `APPROVE` recomendado, pendiente de Yeison |
| `BAD_SERVICE_REFERENCE` | `trips.service_id` sin service en calendar/calendar_dates; `GTFS-REF-SERVICE` | `FAIL_TECHNICAL`; 1 finding | `GTFS_SPECIFICATION` | Baja: una fila de calendario válida y un service ausente deliberado | `APPROVE` recomendado, pendiente de Yeison |
| `BAD_SHAPE_REFERENCE` | `trips.shape_id` suministrado sin shape padre; `GTFS-REF-SHAPE` | `FAIL_TECHNICAL`; 1 finding propuesto | `GTFS_SPECIFICATION` | La tabla shapes es condicional y el scope de la regla depende de que exista | `KEEP_DRAFT` |
| Compliance `gtfs-valid` | referencias fixed-stop aceptadas por Compliance V1 | `PASS`; 0 findings | `COMPLIANCE_FROZEN_SCOPE` | No afirma validación completa GTFS ni sustituye GTFS_Lab V1 | `REJECT_FOR_GOLDEN_V1` |
| Compliance `gtfs-broken-stop` | referencia fija a stop incorrecta | `FAIL_TECHNICAL`; finding de Compliance V1 | `COMPLIANCE_FROZEN_SCOPE` | Ownership y scope pertenecen al adapter Compliance; se conserva su límite y no es expectativa del validator GTFS_Lab | `REJECT_FOR_GOLDEN_V1` |
| Compliance `gtfs-broken-trip` | referencia fija a trip incorrecta | `FAIL_TECHNICAL`; finding de Compliance V1 | `COMPLIANCE_FROZEN_SCOPE` | Mismo límite de ownership y regla agregada | `REJECT_FOR_GOLDEN_V1` |
| Compliance `gtfs-missing-value` | caso GTFS de valor ausente | El manifest histórico marca `INSPECTION_ERROR`; no se convierte en finding | `COMPLIANCE_FROZEN_SCOPE` | Error de inspección no es una expectation normativa estable | `REJECT_FOR_GOLDEN_V1` |
| Compliance `gtfs-boundary` | comportamiento en el límite del scope congelado | resultado de frontera del evaluador | `COMPLIANCE_FROZEN_SCOPE` | El límite del evaluador no representa una regla GTFS | `REJECT_FOR_GOLDEN_V1` |

La etiqueta `APPROVE recomendado` es una recomendación técnica del asset. Los dos `case.json` permanecen `UNDER_REVIEW`, con `review: {}`. Para el resto, “expected” describe la hipótesis candidateada en M03-A; el resultado del evaluador Compliance no se promueve a Golden.

## B. Propuesta seleccionada

Ambos inputs son ZIP sintéticos independientes bajo `golden/cases/`; se eligió ownership propio para que un cambio legítimo en fixtures de test no altere la referencia revisable. Los dos contienen una sola referencia ausente intencional y relaciones de soporte válidas.

### `gtfs-orphan-route-v1` — versión 1.0.0

- Propósito: verificar que el `route_id` del viaje existe en `routes.txt`.
- Input: `golden/cases/gtfs-orphan-route-v1/input.zip`.
- SHA-256: `28e24901f5cec87b900d1d7de510e2a97b3007158c0775012bf6210ad73eab81`.
- Expectativas: `STATUS validation.rules[rule_id=GTFS-REF-TRIP-ROUTE].status = FAIL_TECHNICAL`; `COUNT ...finding_count = 1`.
- Authority: GTFS Schedule Reference, `trips.txt`, campo `route_id`, “Foreign ID referencing routes.route_id”, Required. Interpretación: el único trip declara una ruta que no está en el conjunto de `routes.route_id`.
- Comparación observada: `FAIL_TECHNICAL`, `FAIL_TECHNICAL`, 1 finding; coincidencia en ambas expectativas.
- Recomendación: `APPROVE`, pendiente de aprobación del usuario.

### `gtfs-bad-service-reference-v1` — versión 1.0.0

- Propósito: verificar que el `service_id` del viaje está definido en `calendar.txt` o `calendar_dates.txt`.
- Input: `golden/cases/gtfs-bad-service-reference-v1/input.zip`.
- SHA-256: `21714ca7c02f99a8e77257ea25eb90aac964b774fc7fcfd5ace0455d4d55ee51`.
- Expectativas: `STATUS validation.rules[rule_id=GTFS-REF-SERVICE].status = FAIL_TECHNICAL`; `COUNT ...finding_count = 1`.
- Authority: GTFS Schedule Reference, `trips.txt`, campo `service_id`, referencia a `calendar.service_id` o `calendar_dates.service_id`, Required. Interpretación: ambas tablas de calendario están correctamente formadas y solo declaran `weekday`; el trip declara `missing-service`.
- Comparación observada: `FAIL_TECHNICAL`, `FAIL_TECHNICAL`, 1 finding; coincidencia en ambas expectativas.
- Recomendación: `APPROVE`, pendiente de aprobación del usuario.

## C. Candidatos diferidos/rechazados

Los dos casos de referencias son focales, pero los fixtures `ORPHAN_TRIP` y `ORPHAN_STOP` actuales atraviesan una regla agregada del adapter Compliance. Permanecen `KEEP_DRAFT` hasta que puedan vincular expectativa y predicado sin atribución ambigua. `VALID_MINIMAL` no debe interpretarse como validez completa del estándar. `BAD_SHAPE_REFERENCE` requiere fijar mejor el scope condicional de la tabla. Los cinco fixtures Compliance V1 quedan fuera del Golden corpus de GTFS_Lab: no se transforman outputs del motor Compliance congelado en authority del validator GTFS_Lab.

## D. Corpus y evaluator

`golden/corpus_v1.json` declara dos casos `UNDER_REVIEW`, versión de contrato `1.0.0`, timestamp de creación UTC y `corpus_sha256` determinista. La identidad se calcula sobre la lista ordenada por `case_id`, `case_version`, con esos identificadores más `case.json SHA-256` e input SHA-256; JSON canónico UTF-8, claves ordenadas, separadores compactos. No entran timestamps ni paths.

Identidad actual del corpus: `9bbd133a54c0cd6029789a6cb7ce2bd6206aace604a71cc97981ed9459edcae0`.

`golden_evaluator.py` implementa `STATUS`, `COUNT`, `PRESENCE` y `ABSENCE`, y los targets limitados `validation.status` y `validation.rules[rule_id=ID].{status,finding_count,findings}`. COUNT exige `int` exacto; no convierte strings. El tipo `GoldenCaseResult` define caso/versión, run, dataset, engine context, status, resultados por expectation y diferencias inesperadas. No hay scoring.

Los estados generales son `PASS`, `FAIL_EXPECTATION`, `NOT_EVALUABLE` y `EXECUTION_ERROR`. Solo un caso que pase `is_executable_authority(...)` se evalúa. El gate del evaluator usa casos temporales sintéticos APPROVED que no se guardan en el corpus. Los casos candidatos `UNDER_REVIEW` no se ejecutan como autoridad.

## E. Límites y autoridad humana

El corpus no está aprobado ni es operativo. No se registra nombre, fecha ni firma de reviewer. Los outputs observados se incluyen únicamente como contraste posterior de expectativas definidas primero. La especificación GTFS es normativa técnica para estas referencias y no equivale a conclusión jurídica sobre un operador.

## F. Regresión M03-B1

| Comprobación | Resultado |
|---|---|
| M01 `TDL_TRUST_CONTRACT_GATE` | PASS, 12/12 |
| M02 `TDL_TRUST_PERSISTENCE_GATE` | PASS, 21/21; protected hashes before/after coinciden |
| M03-A `TDL_GOLDEN_CASE_CONTRACT_GATE` | PASS, 18/18 |
| GTFS_Lab V1 current gate | PASS; fixtures, E2E sintético y GIS direccional PASS |
| Compliance V1 current gate | PASS; hash inicial/final `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`; mantiene el test histórico `UNCHANGED_COUNT_audit.rules` (386 PASS, una aserción histórica FAIL admitida por el gate) |
| Golden Corpus Review Gate | PASS, 9/9; 2 casos y 0 APPROVED |
| Golden Evaluator Gate | PASS, 11/11 |
| `py_compile` | PASS para evaluator y ambos gates nuevos |
| `git diff --check` | PASS |

El Compliance gate leyó las bases locales existentes a través de junctions temporales desde el worktree aislado; las referencias se retiraron tras el gate. No se modificaron las bases protegidas. Evidencias de ejecución fuera del checkout: `C:\Users\yeiso\AppData\Local\Temp\tdl_m03b_gate_outputs\`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
