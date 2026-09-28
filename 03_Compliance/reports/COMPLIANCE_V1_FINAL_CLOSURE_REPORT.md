# Compliance V1 Final Closure

## Executive summary

**COMPLIANCE_V1_FINAL_CLOSURE = PASS. COMPLIANCE_V1 = CLOSED_WITH_DEFERRALS.**

Misión autorizada el 2026-09-28. Cierre engine/lab para GTFS fixed-stop references y NeTEx EPIP Line fragment. No equivale a cumplimiento íntegro de formatos, requisitos ni operadores. Phase 1/2 siguen FROZEN; Phase 3 cierra con diferimientos bajo el nuevo alcance. B02 no se reabre.

Baseline real: rama main; DB `03_Compliance/databases/transit_compliance.duckdb`, hash `6C7A944FB9EB7983A912AF42C2F5C69C0F29D268F6139D3B5566BF7140788E0F`. Cambios locales previos en PROJECT_STATUS, política de tests, herramientas, seeds, skills y evidencia B02 conservados. Sin acceso a árboles de productos, commit, push ni contacto externo.

Preestado contrastado: 92 provisions, 36 source facts, 48 requirements, 10 deadlines; nueve familias/48 membresías; 15 mappings, siete conceptos, nueve bridges/scopes, diez coverage, seis automatability PARTIAL, cero representability/observaciones/reglas. [Baseline por tabla](evidence/compliance_v1_20260928/baseline.json) e [initial gate](evidence/compliance_v1_20260928/initial_gate/).

## V1 scope

[Definición de alcance](../COMPLIANCE_V1_SCOPE.md) y [vista vigente](../COMPLIANCE_V1_CURRENT_STATE.md). Dos scopes técnicos derivados de relaciones M04 aceptadas; el universo jurídico congelado no se modifica. No se exige conversor, QGIS, UI, todas las reglas ni realtime.

### Master execution table

Writes indica artefactos/documentación y filas DB solo donde se especifica. La persistencia de las distintas capas se agrupó en una única transacción después de validar ambos pilotos.

| Stage | Result | Blocking | Writes | Output | Next |
|---|---|---:|---|---|---|
| 0 Authoritative baseline | PASS | No | baseline/logs | Hash, tablas y gate B02 exactos | Preservar |
| 1 Scope formalization | PASS | No | COMPLIANCE_V1_SCOPE | GTFS/NeTEx primary | Aplicar scope |
| 2 Family reconciliation | PASS | No | dispositions.json/md | 48 requisitos/9 familias/15 mappings | Backlog |
| 3 GTFS inventory | PASS | No | gtfs_inventory.json | Siete tablas raw | Reutilizar contrato |
| 4 GTFS target | PASS | No | engine/fixtures; DB agrupada | Referencias fixed-stop, 18 casos | Gate |
| 5 NeTEx inventory | PASS | No | fuentes/XSD/manifest | Lab vacío; nuevo artefacto EPIP fijado | Scope Line |
| 6 Representability contract | PASS | No | +2 assertions | PARTIAL amplia; AVAILABLE acotada | Mantener límites |
| 7 Observed contract | PASS | No | +28 observaciones sintéticas | Dataset/hash/evaluador/locator/estado | Replay |
| 8 Audit rule contract | PASS | No | +2 reglas | Resultados técnicos, legal=false | Gate |
| 9 Automatability | PASS | No | +2 PARTIAL e inventario | Subscope automático; requisito contextual | Revisión humana residual |
| 10 Coverage | PASS | No | conciliación | Diez decisiones intactas | Sin porcentajes |
| 11 GTFS E2E | PASS | No | resultados reproducibles | Fuente→requisito→scope→regla→resultado | READY |
| 12 NeTEx E2E | PASS | No | resultados reproducibles | Artefacto EPIP→Line→XSD→observación | READY |
| 13 Consistency | PASS | No | gate | Identidades, relaciones, versiones y límites | Preservar |
| 14 Legacy protection | PASS | No | delta exacto | Todas las filas antiguas intactas | Sin reabrir B02 |
| 15 Documentation | PASS | No | vista vigente/informe | Una entrada compacta actual | Consultar vista |
| 16 Validator consolidation | PASS | No | current gate | PASS; dos fallos locales corregidos y conservados | Gate único |
| 17 Reproducibility | PASS | No | fixtures/paquete/CLI replay | Mismo resultado en directorio/proceso separados | Checkpoint |
| 18 Failure recovery | PASS | No | matriz y rollback aislado | Estados controlados; sin falso finding | Mantener contrato |
| 19 Data safety | PASS | No | safety_cases.json | Límites, sin DTD/entidades externas/red | Sin ampliar security |
| 20 Requirement disposition | PASS | No | 48 filas documentales | 6 partial/12 human/20 deferred/10 fuera | Reaperturas por ID |
| 21 Family disposition | PASS | No | nueve filas documentales | Cinco parciales/cuatro diferidas | Backlog |
| 22 GTFS readiness | PASS | No | gate | READY en scope fijado | No extender claim |
| 23 NeTEx readiness | PASS | No | gate | READY en fragmento fijado | No extender claim |
| 24 Standby | PASS | No | scope/gate | SIRI y GTFS-RT STANDBY | Track futuro explícito |
| 25 Deferred backlog | PASS | No | backlog compacto | Razón, impacto y reapertura | Trabajo futuro |

## Standards

### GTFS

Inventario read-only de GTFS_Lab: `raw.agency`, `routes`, `trips`, `stops`, `stop_times`, `calendar_dates`, `shapes`: AVAILABLE. `main.stops` conserva su duplicado histórico. `calendar`, `frequencies`, `transfers`, `feed_info`, tablas tarifarias y demás entidades: NOT_AVAILABLE en esta DB; NOT_REQUIRED_FOR_CURRENT_SCOPE. No se infiere que GTFS no las soporte.

Se inspeccionó el SQL de importación existente, basado en DuckDB `read_csv(header=true, all_varchar=true)`, sin ejecutarlo contra raw. El gate compara ese contrato en memoria con el inspector acotado. No se crea otra DB ni stack de ingestión. Sentinel e infraestructura raw conservados. Los KML/GIS existentes no son necesarios; no se regeneran. La regla es nueva porque el laboratorio no aportaba este contrato de auditoría Compliance.

Referencia técnica: [GTFS oficial](https://gtfs.org/documentation/schedule/reference/), captura del repositorio oficial google/transit en `sources/gtfs_reference.md`, identificada por hash. Reglas consultadas: `stop_times.trip_id`, `stop_id` y `stops.location_type`. La captura web directa devolvió 403; se obtuvo el archivo oficial fuente sin alterar la referencia. No se atribuye al estándar una versión de calendario inferida: gobiernan los bytes fijados.

### NeTEx

Antes del trabajo, `02_Data_Engineering/NeTEx_Lab` estaba vacío. Existían registro EPIP, una capacidad general y dos mappings legacy; fuentes M03 de alcance e identidad, sin parser ni validación operacional demostrados. NAP contiene políticas/FAQ HTML, no un dataset NeTEx de este piloto. No se presupone cobertura de cualquier archivo fuera del inventario dirigido.

Artefacto fijado: [TransmodelEcosystem/NeTEx-Profile-EPIP](https://github.com/TransmodelEcosystem/NeTEx-Profile-EPIP/tree/e5eaf83f15f7fd8db7991a4a8323b6ff7905c13a), XSD Data4PT 2021 basado en NeTEx 1.3.1, actualmente no mantenido. Se compilaron el XSD con constraints y sus dependencias locales. Scope: elemento global `Line`, atributos y `Name`, según `LineStructure/LineGroup`. La identidad normativa legacy 2017 permanece histórica; no se afirma equivalencia ni perfil nacional aplicable.

Fixture positivo y frontera validados realmente contra el XSD, no contra un esquema inventado. Diez casos. Automatización técnica del fragmento disponible; semántica jurídica y conformidad integral requieren revisión separada.

### SIRI — standby

STANDBY / DEFERRED_BY_PRODUCT_SCOPE. Los dos mappings y scopes B02 persisten intactos; ninguna regla V1 los ejecuta. Los gaps ET/SX anteriores dejan de ser bloqueadores de cierre V1.

### GTFS-RT — standby

STANDBY / DEFERRED_BY_PRODUCT_SCOPE. No se afirma implementación operativa. Reapertura de ambos realtime: V1 GTFS/NeTEx estable y autorización explícita de su track.

## Phase 1

FROZEN. 22/22 invariantes PASS y filas protegidas idénticas. El gate Phase 2 revalida también hashes de las diez fuentes legales. No se cambia corpus, manifests ni snapshots.

## Phase 2

FROZEN. Antes de persistir: 387/387 PASS del post-materialization gate. Después: 386 PASS y un FAIL histórico `UNCHANGED_COUNT_audit.rules` (esperaba 0, observa 2). El gate vigente exige exactamente ese único mismatch y sustituye esa condición por igualdad exacta de las dos filas autorizadas; no modifica el SQL ni convierte su FAIL original en PASS. Requirements/deadlines/source facts íntegros.

## Phase 3

CLOSED_WITH_DEFERRALS según alcance de esta misión. B02 mantiene CLOSED_WITH_DEFERRALS y su estado exacto. Total: 15 mappings, 9 concepts, 11 concept bridges, 11 scopes, 10 coverage, 8 automatability, 2 representability, 28 observaciones sintéticas y 2 reglas. No se eliminan filas ni se amplían mappings legacy.

## Requirement disposition

[48 IDs con razón, impacto, automatizabilidad y reapertura](evidence/compliance_v1_20260928/dispositions.md). Conteos: SUPPORTED_IN_V1 íntegro=0; PARTIAL=6; HUMAN_REVIEW_REQUIRED=12; DEFERRED=20; OUT_OF_SCOPE_V1=10. Ningún UNKNOWN operativo sin disposición. OUT_OF_SCOPE es planificación, no exclusión de obligaciones jurídicas.

## Family disposition

F01/F02/F03/F04/F09: PARTIAL_WITH_ACCEPTED_LIMITS. F05/F06/F07/F08: DEFERRED. DELIVERED íntegramente=0. Las familias son planificación existente, no una nueva interpretación. Límites y reaperturas por familia en el mismo inventario.

## GTFS end-to-end

`EU-REG-2017-1926` (consolidación congelada) → `EU-2017-1926-SF-A04-P01` / ART04 → `EU-2017-1926-REQ-A04-P01-001` → `V1-CPT-GTFS` → capacidad `CAP-GTFS-SCHEDULE-TRIP-STOP-TIMES` y mapping aceptado `M04-MAP-A04P01-GTFS-TRIP-STOP` → `V1-SCOPE-GTFS` → `V1-REP-GTFS` → fixture/hash → parser CSV → locator de registro → `V1-OBS-*` → `V1-RULE-GTFS` → resultado técnico.

Se verifica la existencia de las referencias en tres archivos completos y que la parada referenciada sea plataforma. Campos ausentes de un fragmento, versión desconocida, padres ambiguos o flex dan NOT_EVALUABLE. Referencias vacías/rotas con scope completo dan FAIL_TECHNICAL. CSV malformado o error de decodificación da INSPECTION_ERROR. Horarios posteriores a medianoche se conservan sin imponerles validación fuera del scope.

## NeTEx end-to-end

Misma fuente/requisito → `V1-CPT-NETEX` → mapping aceptado `M04-MAP-A04P01-NETEX-PT` → `V1-SCOPE-NETEX` con perfil/artefacto exacto → `V1-REP-NETEX` → fragmento `Line`/hash → parser XML seguro y XSD → locator con namespace explícito → `V1-OBS-*` → `V1-RULE-NETEX` → resultado técnico reproducible.

La regla puede automatizar este fragmento; no se necesita simular HUMAN_ASSISTED. La revisión del requisito y perfil nacional sí permanece humana. No hay conversión GTFS↔NeTEx ni equivalencia entre los resultados de ambos scopes.

## Representability

Dos filas nuevas PARTIAL, ligadas a capacidades existentes. El JSON de condiciones fija scope, versión/hash/commit, path técnico, constraints, fuente y límites. AVAILABLE solo para el fragmento/relación evaluados; no para toda la capacidad. No se deduce presencia observada de la posibilidad técnica.

## Observed evidence

28 filas en `mapping.phase3_observed_evidence`, todas `SYNTHETIC_TEST`, con dataset, versión/hash, versión/hash de evaluador, run determinista, locator, scope, alcance, estados, errores y límites. Contrato existente `phase3-observation-envelope/1`; sin migración. `NOT_INSPECTED` y `FAILED` se representan con INDETERMINATE; nunca como ausencia confirmada.

Observaciones de operadores/datasets de producción=0. El resultado técnico está en la envolvente y en `pilot_results.json`, reproducido por el gate. `audit.runs/results/evidence` permanece sin filas: no se inventan auditorías de operadores para poblar esas tablas.

## Audit rules

Dos reglas activas para los scopes comprometidos, en `audit.rules`; automáticas, `legal_conclusion_allowed=false`. El contrato en `validation_expression` es JSON declarativo, nunca eval/SQL ejecutado desde un feed. Vincula scope, representación, versiones, evaluador, configuración, observación y vocabulario de resultados.

El CLI público es `python tools/compliance_v1_engine.py --standard GTFS|NETEX --dataset <directorio|XML> --version <identidad exacta> [--partial]`. Las identidades exactas figuran en `fixtures/compliance_v1/manifest.json` y los comandos ejecutados en `current_gate_04/cli_replay.json`. El CLI emite JSON técnico; no realiza escrituras DB.

## Automatability

Dos evaluaciones nuevas PARTIAL expresan automatización total del subscope y revisión humana del requisito amplio. Las seis legacy quedan intactas. Las 48 disposiciones incluyen automatizabilidad; los nueve mappings B02 son OUT_OF_SCOPE_V1 operativo. No se convierte una restricción técnica en auditoría de toda la obligación.

## Coverage

Diez decisiones sin cambios exactos: nueve PARTIAL y una UNRESOLVED. P01/P02 conservan PARTIAL. Los 38 requisitos restantes no reciben cobertura DB inventada; sí tienen disposición vigente. La UNRESOLVED no contradice los scopes técnicos demostrados: no se presenta como cobertura jurídica resuelta. Cero porcentajes.

## False-positive controls

GTFS: válido, vacío requerido, referencia rota de stop/trip, enum inesperado, estación referenciada, enum vacío válido, malformed, parser failure, schema mismatch, archivo ausente, versión desconocida, inspección parcial, flex, padre duplicado, target vacío, header duplicado y fila irregular: 18 resultados esperados.

NeTEx: válido, falta Name, Name vacío permitido por XSD, enum inválido, malformed, perfil desconocido, parcial, namespace ajeno, entidad externa y falta id: diez resultados esperados. No se inventa una restricción de texto no vacío a partir del nombre del campo.

Controles adicionales: DTD en UTF-16, XML/CSV sobredimensionado y ausencia del XSD confiable → INSPECTION_ERROR; enum erróneo en una parada no referenciada no genera finding de este scope. Lección Bizkaibus aplicada a contrato, versión, normalización y error del evaluador. No se evalúa a Bizkaibus en esta misión.

## Reproducibility

28 fixtures regenerados byte a byte en directorio temporal independiente; dos inspecciones iguales al paquete persistido; dos procesos CLI por estándar con resultado idéntico. Generador del paquete recrea exactamente sus 44 filas. Transacción reproducida en copia aislada, repetición NO-OP, conflicto de identidad rechazado y rollback deliberado comprobado.

Entorno registrado: Python 3.12.10; DuckDB 1.5.5; lxml 6.1.3/libxml2 2.11.9. No se instalaron dependencias. No se afirma portabilidad a cualquier combinación de versiones. DB y corpus legales son recursos locales excluidos de Git; el checkpoint no acredita backup remoto. Las rutas absolutas del gate histórico Phase 2 se conservan y limitan su portabilidad.

## Current validation gate

**COMPLIANCE_V1_CURRENT_GATE = PASS**, [salida completa](evidence/compliance_v1_20260928/current_gate_04/summary.json). Comprueba delta exacto de las 33 tablas, fuentes técnicas, generador, Phase 1/2, scope/standby, 48 disposiciones, coverage, replay, contrato de ingestión GTFS_Lab en memoria, observaciones/reglas, controles de seguridad y hash GTFS protegido.

```powershell
python tools/compliance_v1_current_gate.py --evidence 03_Compliance/reports/evidence/compliance_v1_recheck_unique
python -m py_compile tools/compliance_v1_engine.py tools/compliance_v1_fixtures.py tools/compliance_v1_pack.py tools/compliance_v1_reconcile.py tools/compliance_v1_current_gate.py
git diff --check
```

Usar directorio nuevo. Salidas, códigos y comprobaciones finales en `final_checks.json`. No basta el exit code de un SQL: se inspeccionan sus filas de resultado.

## Historical validators

CURRENT AUTHORITATIVE: gate V1. Phase 1 invariants y Phase 2 post-materialization integrados con clasificación explícita de la única expectativa superada `audit.rules=0`. B02 `--closure-coverage` pasó antes de V1; sus invariantes se preservan mediante delta exacto. HISTORICAL: masters antiguos, gates precoverage y B02/operacional con contadores de capas vacías; DEPRECATED_FOR_CURRENT_STATE como gates globales, no borrados ni reescritos.

Intentos locales conservados: `current_gate_01` falló al leer JSON UTF-8 con encoding Windows implícito; corregida solo la lectura documental. `current_gate_02` pasó. Al ampliar la comprobación de reutilización de GTFS_Lab, `current_gate_03` encontró que DuckDB prohíbe abrir `:memory:` en read-only; se corrigió únicamente esa conexión efímera. `current_gate_04` pasó. Ninguno fue drift de DB ni se relajaron condiciones para ocultarlo.

## Database state

- Inicial: `6C7A944FB9EB7983A912AF42C2F5C69C0F29D268F6139D3B5566BF7140788E0F`.
- Tras única escritura autoritativa y final: `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`.
- Delta: +44 filas, cero updates/deletes/migraciones: 2 conceptos, 2 bridges, 2 scopes, 2 fuentes, 2 scope-source links, 2 assertions, 2 automatability, 28 observaciones y 2 reglas.
- Transacción: preflight de identidad → BEGIN → insert aditivo → postcheck exacto de todas las tablas → COMMIT. Rollback aislado=PASS; rollback autoritativo=0.
- GTFS protegido: `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`.

SQL reproducible, resultados fresh/NO-OP/conflict/rollback, copia local previa y postchecks en [persistence](evidence/compliance_v1_20260928/persistence/). El hash no sustituye la comprobación semántica de filas completas. [Checkpoint lógico](evidence/compliance_v1_20260928/freeze.json).

## Deferred backlog

| Item | Razón / impacto | Reopen trigger |
|---|---|---|
| SIRI / GTFS-RT | Realtime fuera del alcance operacional V1 | V1 estable y track futuro explícito |
| DATEX II / red espacial | Fuera de los dos pilotos; conocimiento histórico conservado | Track específico autorizado |
| C04/C08/5-SN-D/CM/U01–U03 | Diferimientos B02 intactos; no bloquean este cierre | Condiciones del cierre B02 y track pertinente abierto |
| Más reglas GTFS / flex | No necesarias para estas referencias fixed-stop | Necesidad concreta, contrato y fixtures revisados |
| Más perfiles/frames NeTEx | Fragmento actual no prueba publicación completa ni perfil nacional | Perfil versionado, constraints y artefactos verificables |
| F05–F08 | Faltan registros de cambios/calidad/reutilización/solicitudes | Evidencia contextual y criterios acotados |
| Contexto NAP/temporal/institucional | Formato no demuestra acceso, fechas ni actuaciones | Registros y revisión humana por requisito |

## Reopen conditions

Por ID/familia en `dispositions.json/md`; por scope, una nueva versión, parser, regla, fuente o ampliación requiere nuevo gate y delta explícito. Drift protegido detiene promoción. Las decisiones históricas no se reinterpretan para acomodar un validador.

## Product claims allowed

Transit Data Lab dispone de un pipeline reproducible de análisis de compliance para los scopes GTFS y NeTEx comprometidos, demostrado con fixtures sintéticos y resultados técnicos acotados.

## Product claims prohibited

No afirmar automatización de toda la normativa UE, cumplimiento íntegro GTFS/NeTEx, conformidad jurídica de operadores, soporte operacional SIRI/GTFS-RT, datos NAP de producción, perfil mínimo nacional satisfecho ni conversión sin pérdida.

## Closure decision

**PHASE1 = FROZEN; PHASE2 = FROZEN; PHASE3 = CLOSED_WITH_DEFERRALS.**

**GTFS = READY; NeTEx = READY; SIRI = STANDBY; GTFS_RT = STANDBY.**

**COMPLIANCE_V1 = CLOSED_WITH_DEFERRALS.** Sin bloqueadores materiales para el alcance fijado. El cierre no transforma diferimientos en implementación ni PASS técnico en aceptación jurídica/comercial.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
