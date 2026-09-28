# Phase 3 — Operational Closure Report

Fecha: 2026-09-28. **PHASE3 = IN_PROGRESS; CLOSURE_READINESS = BLOCKED.**

Se completan conciliación, selección y dos intentos de representabilidad, contrato de almacenamiento observado probado, revisión de automatizabilidad y disposición de los 48 requisitos. Falta un contrato representable demostrable para el piloto y, por dependencia, fixtures de perfil, parser, primera regla validada y demo completa. No se declara cierre por volumen de documentación. B02 permanece CLOSED_WITH_DEFERRALS y no se reabre.

## Autoridad, alcance y preestado

Autoridad: misión «PHASE 3 COMPLIANCE FULL OPERATIONAL CLOSURE PACK», `.agents/skills/compliance_eu/SKILL.md`, `references/FAILURE_PATTERNS.md`, `PROJECT_STATUS.md`, `TEST_BASELINE_POLICY.md`, framework M02, family baseline M05B y cierre B02. La autorización actual permite trabajo técnico de este pack; no convierte las limitaciones semánticas previas en afirmaciones aprobadas ni autoriza nuevas interpretaciones jurídicas.

La búsqueda acotada no localizó un roadmap independiente de Compliance. El roadmap operativo disponible es la secuencia M02–M06 del framework y PHASE3_NEXT_CRITICAL_PATH del cierre B02, reconciliados con el estado vigente y los criterios A–O de esta misión. El roadmap Business no gobierna Compliance. No se declara que falte un archivo que pueda existir fuera del conjunto inspeccionado.

Preestado verificado con DuckDB read-only: 48 requirements, 92 provisions, 36 source facts, 10 deadlines; 9 familias/48 membresías; 15 mappings (6 legacy + 9 B02); 9 scope units INCLUDED; 10 coverage; 6 automatability PARTIAL; 0 representability, 0 observed evidence, 0 audit.rules. Rama main y cambios locales anteriores conservados. No se accedió a repositorios de productos, no hubo commit/push ni contacto con terceros.

## Master stages

Writes distingue documentos/artefactos de filas autoritativas. Ninguna etapa escribió la DB autoritativa.

| Stage | Status | Blocking | Writes | Result | Follow-up |
|---|---|---:|---|---|---|
| A Scope reconciliation | PASS | No | Inventarios | PHASE3_SCOPE_RECONCILED=YES; 48 requisitos y 9 familias | Mantener alcance |
| B Pilot selection | PASS | No | Informe | PRIMARY ET; ALTERNATE SX | Máximo dos intentos, cumplido |
| C Representability | DEFERRED | Sí | Fuentes y análisis | Ambos contratos incompletos; 0 assertions | Obtener restricciones normativas acotadas |
| D Observed contract | PASS | No | Código, pruebas; 5 filas solo en copia | Esquema actual suficiente; roundtrip y rollback | Integrar escritor validado cuando exista parser |
| E Controlled profile fixtures | SKIPPED_BY_DEPENDENCY | Sí | 0 fixtures de perfil | C no demuestra contrato esperado | Crear positive/negative/boundary/invalid/failure tras C |
| F Observation pipeline | SKIPPED_BY_DEPENDENCY | Sí | 0 | Sin parser ni observaciones de dataset | C+E |
| G First audit rule | SKIPPED_BY_DEPENDENCY | Sí | 0 | audit.rules=0 | C+D+E y pipeline válidos |
| H False-positive defence | SKIPPED_BY_DEPENDENCY | Sí | Matriz de aceptación documental | No hay regla promovible | Ejecutar matriz contra regla real |
| I Automatability | PASS | No | Inventario documental | 15 mappings revisados; 6 potenciales parciales, 9 diferidos | Sin promoción automática |
| J Coverage reconciliation | PASS | No | Inventario | 9 PARTIAL + 1 UNRESOLVED; 38 sin decisión | No reabrir P01/P02 |
| K Remaining families | PASS | No | Disposición por 48 IDs | 10 PARTIAL, 38 DEFERRED; razones/impacto/reapertura | Trabajo residual formal |
| L Closure criteria | PASS | Sí | Checklist | Criterios evaluados; mínimo operativo no satisfecho | No confundir revisión PASS con cierre |
| M End-to-end demonstration | SKIPPED_BY_DEPENDENCY | Sí | 0 | Cadena completa no ejecutada | C→E→F→G→H |
| N Final validation | PASS | No | Logs completos | Gates vigentes y protección exacta PASS | Gates históricos separados |
| O Closure decision | PASS | Sí | Informe/estado | IN_PROGRESS por cadena operativa ausente | Resolver C antes de promoción |

## Inventario comprometido

| Deliverable | Disposición | Evidencia/límite |
|---|---|---|
| Infraestructura M02, catálogo inicial M03, baseline familiar | DONE | Verificación estructural y filas protegidas |
| Mappings/reviews B01 y B02 aprobados | DONE | Estabilidad row-exact; semántica PARTIAL preservada |
| Cobertura global | PARTIAL | 10 decisiones; no prueba ejecución ni todos los requisitos |
| Representabilidad de un scope persistido | DEFERRED | ET y SX: constraints normativos no demostrados |
| Contrato observado | DONE | Contrato v1 probado en copia, sin migración |
| Fixtures SIRI y observación de implementación | NOT_STARTED | Dependencia de contrato normativo; tests de storage no sustituyen fixtures |
| Regla operativa y demo completa | NOT_STARTED | No autorizable sin los prerrequisitos demostrados |
| Revisión de automatizabilidad | DONE | Revisión documental completa del conjunto persistido; cero automatización operativa probada |
| Residuales por familia | DEFERRED | Disposición por ID, sin investigación indefinida |
| VM, C02/C03/C05/C06 en este scope; score global; todos los perfiles/operadores | OUT_OF_SCOPE | No se cambia el rechazo humano ni se expande arquitectura |

## Representability: selección y dos intentos

ET y SX tienen identidad EPIP-RT CEN/TS 15531-7:2025 y base SIRI 2.1, con scopes INCLUDED aprobados. ET ofrece un caso más acotado de journey delay/cancellation; SX requiere interpretar ámbito y consecuencias de avisos. DATEX 4-SN-A tiene buen foco técnico pero el registro aprobado no fija release individual; los otros legacy no tienen scope_unit persistido equivalente y exigirían ampliar modelado. La selección responde a calidad/versionado/ambigüedad, no a atractivo comercial.

**PRIMARY:** `M06-B02-SCOPE-C07-ET-JOURNEY-DELAY-CANCELLATION` → `M06-B02-MAP-A05-P02-001-SIRI-ET` → `CAP-SIRI-EPIPRT-ET` → EPIP-RT 2025/SIRI 2.1 → EstimatedTimetableDelivery, EstimatedVehicleJourney y calls. Evidencia permite identificar el servicio; no se ha obtenido el contenido completo de §8 (páginas normativas 69 y siguientes) para constraints y condiciones del scope. La vista disponible tiene 15 páginas físicas y contiene el índice, no ese capítulo. Resultado: **DEFERRED**. No se sustituye delay/cancellation por mera existencia de un tag.

**ALTERNATE:** `M06-B02-SCOPE-C07-SX-PASSENGER-DISRUPTION-NOTICE` → `M06-B02-MAP-A05-P02-001-SIRI-SX` → `CAP-SIRI-EPIPRT-SX` → mismo perfil/base → SituationExchangeDelivery, PtSituationElement y consecuencias. El índice identifica §7 (páginas normativas 25 y siguientes), pero no permite verificar reglas de alcance, validez y representación textual/estructurada. Resultado: **DEFERRED**. No se infiere el concepto entero desde un aviso.

La [vista oficial](https://normy.normoff.gov.sk/norma/141185/nahlad/) prueba identidad y ubicación de los capítulos, no sus constraints. El [repositorio oficial SIRI](https://github.com/TransmodelEcosystem/SIRI) distingue releases/base schemas; la descripción de su contenido enumera partes 1–6. Eso no prueba por sí solo restricciones de Part 7. Búsqueda adicional de docs v2.1: HTTP 404 conservado, sin atribuirlo a ausencia universal del perfil. No se afirma que el texto completo sea imposible de conseguir; no se localizó en la investigación acotada ejecutada.

El [perfil DATEX 4-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-a-road-closures/) sí documenta una ruta de gestión de cierres y enumera tipos. La página remite al generador para obtener schemas; no fija por sí sola el artefacto/versionado del scope aprobado. No se hizo un tercer intento de representabilidad.

Fuentes recuperadas el 2026-09-28 y SHA-256 en [source_manifest.json](evidence/phase3_operational_closure_20260928/source_manifest.json). Son capturas nuevas de investigación, separadas del corpus protegido. La equivalencia semántica general aprobada sigue siendo parcial; la pieza pendiente es demostración técnica de constraints del scope, no un permiso mecánico genérico. Assertions persistidas: **0**. Reapertura: disponer de extracto autorizado/versionado de §8 o §7 y artefacto técnico verificable; revisar únicamente cualquier semántica nueva que aparezca.

## Observed evidence y fixtures

[Contrato v1](PHASE3_OBSERVED_EVIDENCE_CONTRACT.md): utiliza columnas existentes y una envolvente JSON en notes. Distingue inspection_status de observed_result, incluye identidad/hash/run/evaluador/locator/scope/limitaciones. Cinco roundtrips, diez rechazos y rollback PASS. Cero migraciones, cero observaciones autoritativas; cinco filas sintéticas solo en copia local.

No existen todavía fixtures positivos/negativos/boundary normativos del piloto ni casos de parser real. Las cinco envolventes son pruebas del contrato de almacenamiento, no resultados observados. E/F permanecen SKIPPED_BY_DEPENDENCY: inventar un mini-perfil local para conseguir PASS introduciría semántica sin evidencia. No se creó motor nuevo ni jerarquía bajo scope_unit.

## Regla y defensa de falsos positivos

Creada: NO. Validada: NO. Promoción: bloqueada por C/E/F. El contrato futuro de la regla deberá fijar scope, perfil/version/artefacto, locator y expected structure, y devolver solo PASS, FAIL_TECHNICAL, NOT_EVALUABLE o INSPECTION_ERROR. No existe autorización derivada para LEGAL_NON_COMPLIANCE u OPERATOR_NON_COMPLIANT.

| Caso futuro obligatorio | Resultado técnico esperado / límite |
|---|---|
| Fixture válido y scope aplicable | PASS dentro de estructura verificada |
| Violación demostrada de constraint | FAIL_TECHNICAL, sin atribución jurídica |
| Missing pero NOT_INSPECTED | NOT_EVALUABLE |
| Malformed/parser failure | INSPECTION_ERROR; nunca fallo de operador |
| Versión distinta | NOT_EVALUABLE; nunca aplicar silenciosamente otra versión |
| Enum inesperado | Separar versión/contrato/parser; FAIL_TECHNICAL solo si la especificación fijada lo demuestra |

Lección Bizkaibus aplicada: antes de atribuir un finding verificar specification → interpretation → implementation → validator → input → version → execution → persistence/export. Las pruebas de D ejercitan colisiones de estados, versión de contrato, hash, scope y roundtrip; **no constituyen H para una regla que aún no existe**. Toda regla que confunda esos estados tendrá FAIL_BLOCKING de promoción.

## Automatability, coverage y familias

[Inventario completo por ID](evidence/phase3_operational_closure_20260928/reconciliation_02/requirements.md), [automatability](evidence/phase3_operational_closure_20260928/reconciliation_02/automatability.json), [coverage exacta](evidence/phase3_operational_closure_20260928/reconciliation_02/coverage.json).

Los 15 mappings se revisaron: seis evaluaciones PARTIAL existentes se expresan documentalmente como PARTIALLY_AUTOMATABLE, con sus prerequisites intactos; nueve mappings/scopes B02 DEFERRED hasta prueba técnica. AUTOMATABLE probado=0. No se persiste DEFERRED en un enum que no lo admite; tampoco se convierte esta revisión documental en nueva aprobación humana. Para rutas institucionales/temporales subsiste HUMAN_REVIEW_REQUIRED; no se declara NOT_AUTOMATABLE para siempre por falta de evidencia actual.

Coverage global: diez decisiones completas conservadas (nueve PARTIAL, una UNRESOLVED), 38 requisitos sin decisión. P01/P02 PARTIAL sin cambios. No se calculan porcentajes. Disposición operativa por requisito: diez PARTIAL (incluye el trabajo existente de cobertura UNRESOLVED), 38 DEFERRED. La disposición no altera el coverage_state.

| Familia | Requisitos | Disposición familiar | Razón / impacto / reapertura |
|---|---:|---|---|
| F01 NAP | 8 | PARTIAL | Rutas parciales; falta operación/contexto NAP; reabrir con evidencia identificable |
| F02 formatos | 8 | PARTIAL | Mappings acotados; no contrato completo de perfil; reabrir con constraints versionados |
| F03 temporal | 9 | PARTIAL | Ruta manual de piloto; falta evidencia fechada; reabrir con registros de disponibilidad |
| F04 metadata | 4 | PARTIAL | Metadata técnica parcial; falta contexto de procedencia/solicitud; reabrir con trazabilidad |
| F05 actualización | 3 | DEFERRED | Sin historial de cambios; no evalúa corrección; reabrir con historial y contrato revisado |
| F06 calidad | 4 | DEFERRED | Sin criterio/evidencia acotados; no atribuye calidad; reabrir con criterios y ejecución |
| F07 reutilización | 5 | DEFERRED | Sin casos/contexto; no evalúa ranking; reabrir con decisiones documentadas |
| F08 routing | 1 | DEFERRED | Sin contrato/observación; no evalúa intercambio; reabrir con interfaz y solicitud/respuesta |
| F09 gobierno | 6 | PARTIAL | Ruta institucional piloto; requiere HUMAN_REVIEW_REQUIRED y registros de autoridad |

Los siete diferimientos B02 C04/C08/5-SN-D/CM/U01/U02/U03 y las exclusiones se heredan literalmente del [cierre final](M06_B02_FINAL_CLOSURE.md#deferred-work-and-reopen-conditions), con sus razones, impacto y condición de reapertura. No son nuevos bloqueos globales ni se reabren en esta misión. Las 38 disposiciones nuevas son planificación residual por ID, no interpretaciones jurídicas.

## Criterios L y demo M

| Criterio | Satisfecho |
|---|---|
| Scope reconciled; mappings stable; coverage reconciled | Sí |
| Representability contract demonstrated | No |
| Observed evidence contract demonstrated | Sí, almacenamiento aislado; integración pendiente |
| At least one end-to-end evaluation works | No |
| Automatability reviewed; residual limitations documented | Sí |
| Audit rule validated for committed automated scope | No |
| Protected baselines intact | Sí para DB/filas protegidas; corpus externo no rehasheado |
| Execution reproducible | Sí para inventario y contrato; no existe demo operativa completa |

La cadena requirement → concept → mapping → capability → scope existe y es estable para el piloto; se interrumpe en representability. No se presenta el roundtrip de storage como demo de requirement→rule→result. No se exige automatizar todos los requisitos ni resolver todos los diferimientos para cerrar; sí se mantiene el mínimo operativo exigido por la misión.

## Validación y reproducibilidad

Evidencia durable en [run](evidence/phase3_operational_closure_20260928/). CURRENT AUTHORITATIVE GATES: los diez validators conciliados mediante `m06_b02_validate.py --closure-coverage`, row_exact, protected_delta y readonly_hash PASS (13 grupos). Comparación bidireccional EXCEPT ALL contra backup prepack + deltas autorizados conserva todas las tablas legacy y Phase 1/2. No implica revalidación textual/jurídica de fuentes externas.

HISTORICAL INCOMPATIBLE GATES: salidas originales B02D precoverage, B02C, B02A, populated, M04, M04B, M05B, B01 conservadas con sus mismatches. No se cambiaron expected counts. No se ejecutaron masters Phase 1/pre-materialización incompatibles. Representability, observations y audit.rules autoritativos siguen vacíos: integridad estructural/ausencia de promociones PASS; capacidad operativa NO DEMOSTRADA.

Un intento local de inventario filtró `PRIMARY` en vez del enum real `PRIMARY_FAMILY`, produjo cero filas y se detuvo sin escribir. Diagnóstico read-only demostró 48 PRIMARY_FAMILY. Se preserva FAIL_LOCAL del intento y se corrigió exclusivamente la consulta; no fue drift, fallo semántico ni conciliación real fallida. El segundo intento reconcilió los 48 IDs. No se continuó ciegamente después del error.

Comandos desde raíz; usar directorios nuevos:

```powershell
python tools/m06_b02_validate.py --db 03_Compliance/databases/transit_compliance.duckdb --baseline 03_Compliance/reports/phase_3/evidence/m06_b02_orchestrated_20260928_04/authoritative_before.duckdb --closure-coverage --evidence <gate_nuevo>
python tools/phase3_scope_inventory.py --evidence <inventario_nuevo>
python tools/phase3_operational_checks.py --evidence <contrato_nuevo>
python -m py_compile tools/phase3_observation_contract.py tools/phase3_operational_checks.py tools/phase3_scope_inventory.py
git diff --check
```

El gate requiere el backup local excluido de Git. Las pruebas del contrato parten de la DB local protegida y no requieren ese backup; tampoco reconstruyen Phase 1/2 desde fuentes. Copias locales y capturas no acreditan backup remoto. Comandos, códigos de salida y comprobaciones finales: `final_checks.json` del run.

## DB y cierre

- Hash inicial y final: `6C7A944FB9EB7983A912AF42C2F5C69C0F29D268F6139D3B5566BF7140788E0F`.
- Escrituras autoritativas: 0. Migraciones: 0. Rollbacks autoritativos: 0.
- Copia aislada: cinco filas SYNTHETIC_TEST; una transacción fallida deliberadamente y rollback comprobado; resto exacto.
- FULL compliance assertions: 0. Nuevos mappings/reviews/coverage/automatability: 0.

**PHASE3 = IN_PROGRESS.** Bloqueador raíz: falta demostrar los constraints de representabilidad del scope ET o SX con fuente/perfil versionado suficiente. Dependientes reales: fixtures normativos, parser, regla y defensa de falsos positivos, demo end-to-end. Obtener esa evidencia no reabre B02 ni exige rediseñar arquitectura. Los residuales por familia quedan formalmente diferidos y no se confunden con condiciones obligatorias de automatización total.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
