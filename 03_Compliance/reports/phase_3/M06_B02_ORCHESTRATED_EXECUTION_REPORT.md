# M06-B02 — Orchestrated execution & closure pack

Fecha: 2026-09-28. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Executive status

**Persistencia C01+C07 completada y validada. B02 está preparado para cierre documental con diferimientos; Phase 3 continúa IN_PROGRESS.** No se declara cobertura FULL, representabilidad establecida, observación de operadores ni cumplimiento jurídico.

La misión de este pack autoriza ejecutar el subconjunto de S1 y sustituye sus prohibiciones históricas de ejecución. Se preservan los siete seeds originales y su semántica aprobada. Solo se han insertado las 63 filas del paquete (9 por cada una de siete entidades) y una identidad SIRI prerequisito ya descrita en S1. Ningún UPDATE, DELETE ni cambio de esquema en la DB autoritativa.

Autoridad consultada: misión adjunta, skill `compliance_eu` y `FAILURE_PATTERNS.md`, S1, `PROJECT_STATUS.md`, esquema/constraints reales, validators y revisiones B02 vinculadas abajo. No se localizó un archivo identificado como «análisis Astra más reciente» en las búsquedas acotadas de documentación; se solicitó su ruta. No se afirma haberlo leído. Esta carencia documental limita la conciliación final de autoridades, pero no sustituye ni contradice el subconjunto explícitamente autorizado por la misión.

Evidencia final: [run 04](evidence/m06_b02_orchestrated_20260928_04/). Los runs 01–03 conservan los intentos y diagnósticos previos. No se sobrescribió evidencia de errores. Las copias DuckDB y el backup son locales/excluidos de Git; no se afirma backup remoto.

## Stage table

| Stage | Result | Blocking | DB write | Key output | Next action |
|---|---|---:|---:|---|---|
| 0 Baseline/inventory | PASS | No | No | Hash S1 coincidente; 48 requirements; 1 P01 + 6 P02 | Baseline preservada |
| 1 Idempotence | PASS | No | No autoritativa | Comparación de todas las columnas, NULL-safe, PK/natural keys/FK | Usar ejecutor acotado |
| 2 Isolated tests | PASS | No | Solo copias | A–H PASS en runs 03 y 04 | Requisito de persistencia satisfecho |
| 3 Persist C01+C07 | PASS | No | Sí, +64 filas | Una transacción; global preflight y recheck interno | No ampliar lote |
| 4 Post-validation | PASS | No | No | B02D + invariantes compatibles + delta exacto | Conservar FAIL históricos separados |
| 5 Pending dispositions | PASS | No | No | Todos los candidatos tienen disposición y reapertura | Investigación solo al cumplir condiciones |
| 6 Coverage review | PASS | No | No | P01/P02 PARTIAL como revisión documental; no decisión humana inventada | Human review antes de persistir cobertura |
| 7 Pilot selection | PASS | No | No | Primario SIRI-ET; alternativo DATEX 4-SN-A | Dos intentos acotados |
| 8 Representability | DEFERRED | Solo 10/11 | No | Ambos intentos FAIL_LOCAL; versión/crosswalk incompletos | Fijar artefacto y constraints |
| 9 Observation contract | PASS | No para diseño | No | Propuesta reutilizando `notes` y locator; sin migración | Validar con futuro piloto |
| 10 End-to-end fixture | SKIPPED_BY_DEPENDENCY | Solo 11 | No | Representability no establecida | Ejecutar cinco casos tras Stage 8 |
| 11 First audit rule | SKIPPED_BY_DEPENDENCY | No para B02 | No | Sin prerequisites; 0 reglas | Mantener gap Phase 3 |
| 12 B02 closure review | PASS | No técnico | No | READY_FOR_CLOSURE_WITH_DEFERRALS; autoridad Astra no conciliada | Conciliar documento faltante antes de cierre formal |
| 13 Phase 3 gaps | PASS | No para informe | No | Familias y capas pendientes clasificadas | Phase 3 no cerrada |

## Baseline y persistencia

- DB: `03_Compliance/databases/transit_compliance.duckdb`.
- SHA-256 inicial: `0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F`.
- SHA-256 final: `657A48BF6472F958980646193F8CBAA81C01F316D2385D0F4E81F7EF13BAA791`.
- Inventario inicial: 48 requirements, 7 conceptos B02, 6 mappings legacy; 0 mappings/scopes/coverage B02; 0 representability y observed evidence sustantivas; 0 audit.rules.
- Inventario final: 15 mappings sustantivos (6 legacy + 9 B02), 9 bridges B02, 9 INCLUDED scopes B02, 9 enlaces scope-source. Los conceptos siguen siendo 7: 1 P01 y 6 P02.
- No fue necesaria una corrección del inventario narrativo vigente: `PROJECT_STATUS.md` y S1 ya expresaban correctamente 1+6.
- Preservación exacta de todas las filas previas y tablas no objetivo, incluyendo Phase 1/2, concepts, coverage, representability, observed evidence, automatability, audit.rules y seis mappings legacy. Comparación bidireccional `EXCEPT ALL` contra backup + expected rows; no solo conteos/hash de tablas.
- Los hashes distintos de la DB completa son el resultado esperado de esta persistencia Phase 3; no se sustituyó ningún hash protegido de Phase 1/2.

| Tabla | Delta |
|---|---:|
| `mapping.phase3_standards` | +1 identidad SIRI EPIP-RT 2025, IDENTITY_ONLY |
| `mapping.phase3_capabilities` | +9 |
| `mapping.phase3_source_references` | +9 |
| `mapping.phase3_requirement_capabilities` | +9 PARTIAL / NEEDS_REVIEW |
| `mapping.phase3_mapping_reviews` | +9 ACCEPTED_WITH_LIMITATIONS |
| `mapping.phase3_concept_mappings` | +9 |
| `mapping.phase3_mapping_scope_units` | +9 INCLUDED |
| `mapping.phase3_scope_source_references` | +9 SUPPORT |
| Todas las demás tablas | 0; filas idénticas |

Los IDs exactos, valores, columnas, constraints y hashes de los seeds constan en [entities.json](evidence/m06_b02_orchestrated_20260928_04/entities.json), [tests.json](evidence/m06_b02_orchestrated_20260928_04/tests.json) y [execution.sql](evidence/m06_b02_orchestrated_20260928_04/execution.sql). DATEX: 4-SN-A/B/C/D y 5-SN-A/B/C; SIRI: ET/SX. C04, C08, 5-SN-D, CM, VM, U01–U03 y C02/C03/C05/C06 no tienen nuevas filas.

## Idempotence y seguridad transaccional

Ejecutor: [tools/m06_b02_pack.py](../../../tools/m06_b02_pack.py). Usa Python stdlib y DuckDB CLI disponible; no instala dependencias. El módulo Python `duckdb` no está instalado; eso no impidió el aislamiento mediante CLI.

Las siete entidades y la identidad prerequisito comparten clasificación: MISSING → INSERT, MATCHING → NO-OP, CONFLICTING → ABORT. Todas las columnas almacenadas son semánticas en este paquete, incluidas fechas de revisión, notas y fixture_kind; no hay columnas generadas excluidas. Se compara con `IS NOT DISTINCT FROM`.

Se detectan colisiones de PK y UNIQUE del schema; adicionalmente se usan identidades naturales conservadoras para standard (kind/version/profile), capability (standard/domain/entity/element) y fuente (capability/kind/URL/section/version). Se rechazan duplicados esperados, padres FK inexistentes y desacuerdos concept/requirement. Ninguna colisión se resuelve actualizando o reasignando un ID.

Se cargan únicamente los INSERT VALUES revisados en tablas TEMP; no se ejecutan las guardas históricas de los seeds. Orden: identidad → capabilities → fuentes → mappings → reviews → bridges → scopes → scope-source. Todas las expected rows se comprueban antes de BEGIN y otra vez dentro; se insertan solo ausentes; se comparan todas las tablas; B02D se ejecuta como postcheck que lanza error; solo entonces COMMIT.

La CLI usa `-bail`: el primer error impide COMMIT y termina la conexión; DuckDB revierte la transacción abierta. Este mecanismo de rollback al cerrar conexión se probó con fallo real a mitad de transacción y se contrastó mediante snapshots completos. No se ejecuta un bucle que continúe SQL después del error ni se confunde una sentencia ROLLBACK no alcanzada con rollback probado.

El modo `apply` está anclado al hash inicial, rechaza WAL y cambios de seeds/ejecutor/SQL desde las pruebas, y crea backup exacto antes de escribir. La transacción es idempotente, aunque el comando autoritativo de esta misión es deliberadamente de una sola baseline y no permite reejecución indiscriminada sobre otro estado.

| Test | Resultado final | Evidencia |
|---|---|---|
| A Fresh | PASS | 64 ausentes insertadas, 0 conflictos |
| B Second | PASS | 0 ausentes; 64 matching; todas las tablas idénticas a A |
| C Partial consistent | PASS | 19 matching preservadas (identidad/capabilities/fuentes); 45 insertadas |
| D Semantic conflict | PASS | Cambio de source_metadata bajo mismo ID; aborto pre-write |
| E Mid-transaction | PASS | Error inyectado después de mappings; rollback completo |
| F Natural key collision | PASS | Misma identidad natural, ID distinto; aborto pre-write |
| G Duplicate expected | PASS | Duplicado rechazado antes de escribir |
| H FK inconsistency | PASS | Padre de capability inexistente rechazado antes de escribir |

[Clasificaciones completas](evidence/m06_b02_orchestrated_20260928_04/row_classifications.json), salidas/exit codes individuales y snapshots antes/después en el run 04. No hay conflictos autoritativos ni rollback autoritativo.

### Fallos locales encontrados y resueltos

1. Run 01 A/C: el validator B02D no ejecutado previamente contenía un `concept_id` ambiguo. Se cualificaron los JOIN y se añadió igualdad del bridge con el concepto esperado.
2. Run 02 A/C: faltaba el alias `check_name` en el primer SELECT del CTE de B02D. Se corrigió el alias, sin relajar expectativas.
3. Run 03: A–H PASS. El intento `apply` se detuvo antes de abrir para escritura por comparar bytes LF con el archivo SQL CRLF generado por Windows. Se corrigió la comparación: hash real del archivo conservado + igualdad textual normalizada. Run 04 repitió A–H con el ejecutor final; no se cambió la baseline esperada.
4. La primera adaptación del colector de checks asumía que M04/accounting tenían CTE `checks`. Se corrigió el colector y se conservó su salida inicial. Se contrastaron las demás métricas M04 contra la baseline original, y accounting debe seguir PASS íntegramente.

Estos fallos bloquearon temporalmente persistencia, no investigación independiente. La auditoría adicional de rollback de los primeros A/C está guardada: A vuelve al estado inicial; C conserva exclusivamente su preparación parcial anterior a la transacción fallida. Los fallos inyectados E y los conflictos esperados son pruebas, no incidentes de integridad de la DB autoritativa.

## Post-validation

Comandos reproducibles desde raíz (no repetir `apply` sobre el estado final):

```powershell
python tools/m06_b02_pack.py test --evidence 03_Compliance/reports/phase_3/evidence/m06_b02_orchestrated_20260928_04
python tools/m06_b02_pack.py apply --evidence 03_Compliance/reports/phase_3/evidence/m06_b02_orchestrated_20260928_04
python tools/m06_b02_validate.py --db 03_Compliance/databases/transit_compliance.duckdb --baseline 03_Compliance/reports/phase_3/evidence/m06_b02_orchestrated_20260928_04/authoritative_before.duckdb --evidence 03_Compliance/reports/phase_3/evidence/m06_b02_orchestrated_20260928_04/post_validation
```

El primer comando exige un directorio nuevo para una futura prueba aislada y la baseline previa: son los comandos históricos realmente ejecutados, no una receta para sobrescribir evidencia. Para verificar el estado final solo usar el tercer comando con una carpeta de evidencia nueva.

Resultado del gate compuesto: PASS, exit 0. [Resumen](evidence/m06_b02_orchestrated_20260928_04/post_validation/summary.json).

| Validator | Salida original tras persistencia | Tratamiento vigente |
|---|---|---|
| B02D S1 | PASS, 21 checks, 0 failures | Se exige íntegro |
| B02C | FAIL por scope vacío/totales anteriores | Invariantes estructurales + delta exacto PASS |
| B02A | FAIL por bridges/mappings cero y total anterior | Conceptos exactos + delta protegido PASS |
| Populated B02A | FAIL por mappings/bridges cero y agregado legacy | Conjunto de conceptos/estructura + legacy exacto PASS |
| Level A | PASS | Referencias/vocabularios/contexto |
| M04 | FAIL por 9 non-pilot mappings | Otras métricas idénticas; filas legacy exactas |
| M04B | PASS | Semántica/cobertura anteriores intactas |
| M05B | FAIL por 9 NONPILOT_MAPPINGS | Familia baseline intacta; resto de checks PASS |
| M06-B01 | FAIL por TOTALS de baseline previa | B01 intacto; delta exacto exclusivamente B02 |
| Accounting | PASS | 3 excepciones M04 + 3 B01 |
| Row-exact, protected delta, hash read-only | PASS | Paquete completo, tablas protegidas, hash sin cambio durante validación |

Se documenta la selección en `03_Compliance/TEST_BASELINE_POLICY.md`. No se presenta un FAIL original como PASS del archivo original ni se ajustan sus expected counts. Los componentes protegidos dentro de agregados históricos se verifican por comparación completa con el backup previo. Ningún fallo protegido actual quedó pendiente.

## Pending disposition pack

Fuentes locales vigentes para el alcance: S1; `M06_B02_POST_HUMAN_REVIEW.md`; `M06_B02B_TARGETED_CLOSURE.md`; `M06_B02B_R1_DATEX_II_TARGETED_CLOSURE.md`; `M06_B02B_R2_SIRI_TARGETED_CLOSURE.md`; `M06_B02D_PARTIAL_MAPPING_PERSISTENCE_PACKAGE.md`. Las decisiones más antiguas se interpretan según el subconjunto posterior de S1 y esta misión.

| Item | Disposición del pack | Razón / impacto | Condición de reapertura |
|---|---|---|---|
| C01, siete DATEX | RESOLVED_APPROVED | Aplicados PARTIAL; limitación de release conservada | Nueva evidencia versionada para ampliar afirmaciones |
| C07 ET/SX | RESOLVED_APPROVED | Aplicados PARTIAL; crosswalk exacto incompleto | Artefacto EPIP-RT y constraints para piloto |
| C04 | DEFERRED | Article 5(2) es condicional; no se demuestra puente específico para esta rama P02. No bloquea C01 | Evidencia explícita de applicability y revisión de interpretación; reutilizar las siete capabilities C01 sin duplicarlas |
| C08 lift operational status | DEFERRED | FM y ascensores tienen soporte de descripción de servicio; no se demuestra cadena normativa EPIP-RT → path/constraints exactos. No se amplía a todas las facilities | Fuente normativa accesible con sección, path, release y constraints del estado de ascensor |
| 5-SN-D | DEFERRED | Página oficial sigue usando «RSP» bajo catálogo RRP; release individual no fijado. Sin octavo DATEX | Artefacto/perfil inequívoco versionado o aclaración oficial; propuesta futura separada |
| U01 parking tariffs | DEFERRED / DEFERRED_RESEARCH | Catálogo y ruta técnica parcial; perfil mínimo general aplicable/elementos/version no establecidos | Perfil MMTIS/nacional y cadena de applicability para tarifas; no extrapolar truck parking |
| U02 shared vehicles | DEFERRED / NO_TECHNICAL_MAPPING_ESTABLISHED | No hay ruta común demostrada para coches/bicis/patinetes; no se inventan facets | Evidencia de perfil y elementos con ámbito modal explícito |
| U03 parking availability | DEFERRED / DEFERRED_RESEARCH | No establecido perfil exacto aplicable a ambos on/off-street; no se extrapola truck-only | Perfil mínimo general y crosswalk de ambos ámbitos |
| CM | DEFERRED | Identidad Connection Monitoring no prueba correspondencia C07/conexiones garantizadas | Evidencia del servicio y elementos exactos bajo perfil aplicable + nueva autorización |
| C02/C03/C05/C06 | RESOLVED_REJECTED | Decisión humana previa REJECT_FOR_THIS_REQUIREMENT_SCOPE; tiempos actuales/futuros no sustituyen status/disruption | Solo nuevo requisito/alcance y autorización; no por este pack |
| VM | RESOLVED_REJECTED para C07 | Posición de vehículos fuera del subconjunto de disrupción de pasajeros | Propuesta de otro scope, no extensión silenciosa |

La investigación se limitó a las preguntas indicadas y a fuentes locales ya revisadas más comprobaciones oficiales acotadas. C04 no rehace capabilities DATEX. Los diferimientos no significan que el dato no exista ni que un operador incumpla. No quedan ítems con «research forever».

### Fuentes externas comprobadas en esta ejecución

Fecha de consulta: 2026-09-28. Las páginas vivas se citan como evidencia consultada, no como artefactos normativos inmutables capturados.

- [DATEX II 5-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-d-weather-conditions-affecting-road-surface-and-visibility/): documentación técnica oficial. Mantiene «This RSP» bajo RRP y describe PoorEnvironmentConditions. La consulta no fija release individual. Sustenta el diferimiento de identidad, no una corrección local del emisor.
- [DATEX II 4-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-a-road-closures/): documentación técnica oficial. Identifica SituationPublication y RoadOrCarriagewayOrLaneManagement, con roadClosed entre los valores de cierre. Requiere concretar localización y no fija en la evidencia revisada un artefacto inmutable específico para este piloto.
- [CEN-CENELEC EPIP-RT](https://www.cencenelec.eu/news-events/news/2025/eninthespotlight/2025-08-21-siri-7/), anuncio de 2025-08-21: fuente informativa oficial, no texto normativo completo. Apoya identidad y servicios, sin cerrar constraints del piloto ni el crosswalk de FM.
- [NEN preview](https://www.nen.nl/norm/pdf/preview/document/341552/): el acceso del navegador de investigación produjo error. Se conserva la evidencia local previa de SIRI 2.1/EPIP-RT 2025 sin afirmar lectura nueva del documento normativo.
- [EUR-Lex consolidado](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R1926-20240304): el acceso de esta ejecución no devolvió texto utilizable. No se obtuvo una nueva interpretación jurídica; se mantuvo la condicionalidad y el HOLD documentados. Consultas locales dirigidas por artículo/provision textual no localizaron una fila en el formato supuesto; no se alteró ni reconstruyó el corpus.

## Coverage review

Revisión documental de Codex, no nueva aprobación humana atribuida a Yeison. Base versionada: conceptos B02A existentes, S1 de 2026-09-28, DB final de este informe, DATEX RTTI 670/2022 con release individual unresolved y SIRI EPIP-RT CEN/TS 15531-7:2025 / SIRI 2.1.

| Requirement | Evaluated scope | Supporting concepts/mappings | Gaps y deferred items | Resultado y rationale |
|---|---|---|---|---|
| P01 / A05-P01-002 | Rama road status/disruption expresamente autorizada | C01, siete mappings DATEX y siete scopes exactos | No se demuestra todo el requisito de representación de datos dinámicos de carretera; 5-SN-D diferido, release individual sin fijar; no deployment observado | PARTIAL documental: las siete categorías aportan rutas limitadas, sin demostrar exhaustividad del requisito |
| P02 / A05-P02-001 | Rama passenger real-time status/disruption | C07, SIRI-ET y SIRI-SX con dos scopes | C04 applicability, C08 ascensores, CM, U01/U02/U03; constraints exactos pendientes | PARTIAL documental: dos servicios sustentan parte de una obligación condicional más amplia, sin resolver otras ramas |

No se deriva coverage de 7/2/9 conteos ni se escribe una fila en `phase3_requirement_coverage`. Human review: la aprobación de mappings con limitaciones ya existe; la aceptación de esta decisión de cobertura como registro autoritativo sigue pendiente. El pack satisface la revisión documental del ámbito acordado, sin promoverlo a FULL/ESTABLISHED.

## End-to-end pilot

Selección primaria: `M06-B02-SCOPE-C07-ET-JOURNEY-DELAY-CANCELLATION`, por identidad de perfil/release mejor determinada y rama de pasajeros explícita. Alternativa máxima: `M06-B02-SCOPE-C01-4-SN-A`, por documentación concreta del evento roadClosed. SX se descarta para este primer piloto por mayor amplitud de avisos/impactos; FM, CM y 5-SN-D no están aprobados para persistencia.

| Contrato | Intento 1: ET | Intento 2: 4-SN-A |
|---|---|---|
| Standard/profile | SIRI 2.1 / EPIP-RT | DATEX II / RTTI 670/2022 RRP 4-SN-A |
| Release/artifact | CEN/TS 15531-7:2025 identificado; artefacto ejecutable y constraints exactos no obtenidos | Página RRP identificada; release individual/artefacto XSD inmutable no fijado |
| Elements | Servicio ET acotado a delay/cancellation; path y cardinalidades exactas no establecidos en evidencia disponible | SituationPublication → SituationRecord de tipo RoadOrCarriagewayOrLaneManagement → roadOrCarriagewayOrLaneManagementType=roadClosed |
| Constraints/conditions | Necesarios identificación de viaje/llamada, tiempo y reglas de estado; no se infieren cardinalidades | Localización y validez temporal necesarias; método de localización debe fijarse con artefacto; no generar XSD por analogía |
| Limitations | Preview previo no cierra crosswalk ejecutable; ninguna inspección de dataset | Documentación de concepto no sustituye release/schema ni demuestra cumplimiento |
| Evidence | S1, R2 local y anuncio CEN; acceso nuevo NEN falló | Página oficial de road closures consultada |
| Result | FAIL_LOCAL: representability no establecida | FAIL_LOCAL: artefacto/version/constraints no suficientemente fijados |

Resultado Stage 8: DEFERRED tras dos intentos, sin tercero. Reapertura: artefacto técnico autorizado e identificable, hash/version, elementos, cardinalidades y restricciones relevantes revisados. No se registran estados AVAILABLE/MISSING ni se diseña una regla contra un esquema inventado.

## Observed evidence contract

Schema real inspeccionado: `phase3_observed_evidence` contiene evidence_id, capability_id, mapping_id, evidence_type, locator, observed_value, observed_on, notes, fixture_kind. No tiene columnas tipadas independientes para run, evaluator, scope_unit ni inspection status. Puede transportar un contrato acotado sin migración mediante `notes` como JSON versionado y `locator` apuntando a evidencia inmutable; esto es una **propuesta de contrato**, no una constraint de DB existente.

| Dato requerido | Propuesta de representación |
|---|---|
| Dataset identity | `notes.dataset_id`, `notes.dataset_sha256`; ID local sintético para fixture |
| Run/evaluator version | `notes.run_id`, `notes.evaluator_id`, `notes.evaluator_version` |
| Locator | columna `locator`: fichero/registro/path preciso; evidencia conservada |
| Inspection status | `notes.inspection_status`: COMPLETED, NOT_RUN, ERROR |
| Observed result | `notes.observed_result`: SATISFIES, DOES_NOT_SATISFY, UNKNOWN; `observed_value` guarda el valor encontrado |
| Scope relation | `mapping_id` + `notes.scope_unit_id`; verificar que scope pertenece al mapping |
| Limits/errors | `notes.inspection_limits`, `notes.errors`; lista vacía solo cuando se verificó que no hubo errores |
| Provenance | `notes.contract_version = M06-B02-OBS-v1-proposal`, `observed_on`, fixture_kind=SYNTHETIC_TEST para fixtures |

Reglas del contrato propuesto: NOT_RUN/ERROR ⇒ observed_result=UNKNOWN; DOES_NOT_SATISFY exige inspección COMPLETED y criterio aplicable; dato no inspeccionado nunca se registra como ausencia. El futuro evaluator debe validar el JSON y la relación con scope antes de devolver un resultado. La DB no impone esas reglas hoy. No se requiere ni se ejecutó una nueva tabla/migración para preparar este piloto; la aprobación y prueba del contrato operativo quedan vinculadas a un Stage 8 válido.

Stages 10/11 no se ejecutan porque falta representability. El futuro fixture deberá cubrir positivo, negativo, boundary, invalid input e inspection failure, con resultados técnicos separados PASS / FAIL_TECHNICAL / NOT_EVALUABLE / INSPECTION_ERROR. Esto es el criterio de reapertura, no un test ejecutado. `audit.rules = 0`; no hay resultado atribuido a un operador real.

## B02 closure review

| Criterio del pack | Resultado |
|---|---|
| Inventory reconciled | Sí, 1 P01 + 6 P02 |
| Approved mappings applied or infrastructure block | Aplicados los nueve; sin bloqueo activo |
| All candidates have disposition | Sí, incluidos rechazos previos y diferimientos |
| Coverage reviewed for agreed scope | Sí, documental PARTIAL en P01/P02; aceptación autoritativa pendiente |
| Limitations/deferred items documented | Sí |
| Reopen conditions defined | Sí, por ítem y piloto |
| Decisions reproducible | SQL, scripts, hashes, snapshots, logs y fuentes identificadas; falta conciliar referencia Astra no localizada |

`B02_CLOSURE_READINESS = READY_FOR_CLOSURE_WITH_DEFERRALS`, con salvedad de autoridad Astra pendiente. La revisión de cierre del pack está completada; no se declara cierre formal sin esa conciliación documental ni se equipara a Phase 3 completa. Los HOLD técnicos no bloquean por sí mismos el cierre documental permitido por la misión.

## Phase 3 gap analysis

Roadmap disponible consultado: `PROJECT_STATUS.md`, `PHASE_3_M02_FRAMEWORK.md` (M03 evidencia, M04 mappings, M05 observación, M06 automatizabilidad/reglas), `PHASE3_FAMILY_BASELINE_V1.md`. No se encontró un roadmap separado con criterios exhaustivos de cierre Phase 3; la clasificación siguiente es propuesta de planificación explícita, no un nuevo gate humano aprobado.

Inventario actual reproducible en [family_gaps.json](evidence/m06_b02_orchestrated_20260928_04/family_gaps.json). Mapped/reviewed no significa coverage suficiente ni que cada requisito deba tener mapping técnico.

| Familia | Requirements | Requirements con mapping | Con coverage review persistida |
|---|---:|---:|---:|
| F01 NAP access/discovery | 8 | 2 | 4 |
| F02 Availability/format | 8 | 3 | 1 |
| F03 Temporal/deadlines | 9 | 0 | 1 |
| F04 Metadata/provenance | 4 | 1 | 1 |
| F05 Update/correction | 3 | 0 | 0 |
| F06 Quality/notification | 4 | 0 | 0 |
| F07 Reuse/presentation | 5 | 0 | 0 |
| F08 Routing exchange | 1 | 0 | 0 |
| F09 Governance/process | 6 | 0 | 1 |

| Pendiente | Clasificación propuesta | Razón/condición |
|---|---|---|
| Definir cierre Phase 3 y revisar restantes familias/requirements | MUST_DO_FOR_PHASE3_CLOSE | 48 requisitos; solo 8 coverage reviews persistidas; rutas manuales válidas, no forzar mappings |
| Completar decisiones autoritativas de mapping o ruta no técnica para el scope Phase 3 acordado | MUST_DO_FOR_PHASE3_CLOSE | Hay 15 mappings en 6 requisitos; las otras filas no se consideran incumplidas |
| Revisar/persistir coverage cuando exista aprobación humana | MUST_DO_FOR_PHASE3_CLOSE | P01/P02 solo revisión documental; resto según alcance acordado |
| Al menos un piloto de representability con artefacto/version/constraints | MUST_DO_FOR_PHASE3_CLOSE | 0 assertions sustantivas; Stage 8 diferido |
| Validar contrato observado y fixtures con provenance | MUST_DO_FOR_PHASE3_CLOSE | 0 observed evidence sustantiva; no observación inventada |
| Evaluar automatizabilidad del piloto y cerrar primera regla estrecha | MUST_DO_FOR_PHASE3_CLOSE | 6 valoraciones legacy; 0 nuevas B02; audit.rules=0 |
| Resolver C04/C08/5-SN-D/CM/U01–U03 para ampliar cobertura | DEFER_TO_NEXT_PHASE | Compatible con cierre B02 limitado; no si se exige cubrir esos scopes en Phase 3 |
| Inspeccionar operador/dataset real y ampliar evaluación | DEFER_TO_NEXT_PHASE | Este pack no autoriza atribución jurídica ni requiere operador real para fixture |
| Normalizar JSON observado en columnas tipadas / crear framework general | OPTIONAL | No demostrado necesario; no rediseño por defecto |
| Ampliar a nuevos perfiles/modos/categorías | OPTIONAL | Requiere objetivo y autorización propios |

`PHASE3_CLOSURE_READINESS = NOT_READY`. No hay bloqueo de integridad; faltan decisiones/evidencia/contratos operativos. No se confunde avance técnico con aceptación jurídica o comercial.

## Human decisions required

Ninguna para completar las operaciones mecánicas ya autorizadas: se han completado. Para trabajo futuro material:

1. Aprobar la revisión P01/P02 si se quiere convertir en cobertura autoritativa persistida; no atribuir esta aprobación al review previo de mappings.
2. Acordar criterios y ámbito del cierre Phase 3 antes de convertir la clasificación de gaps propuesta en un gate formal.

Resolver interpretación de C04 o autorizar mappings adicionales solo será necesario cuando haya evidencia nueva y se reabran esos ítems; no se solicita aprobación prematura ahora. La ruta del análisis Astra es información faltante, no un permiso adicional de ejecución.

## Archivos y verificación final

- Nuevo ejecutor acotado y colector de validación en `tools/m06_b02_pack.py` y `tools/m06_b02_validate.py`.
- Corrección mínima del validator B02D; seeds originales sin cambio.
- Política de selección de tests y `PROJECT_STATUS.md` actualizados; informe maestro único y evidencia técnica por ejecución.
- Cambios locales preexistentes preservados; sin commit/push/publicación ni cambios en repositorios de productos.
- `git diff --check` ejecutado; la validación de whitespace y compilación de los scripts se registra en `final_checks.json` junto con el hash final revalidado.
