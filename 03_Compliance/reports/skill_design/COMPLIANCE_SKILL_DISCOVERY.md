# Discovery para la Skill de Compliance UE

Fecha: 2026-09-28. Alcance: reconstrucción metodológica desde el repositorio, sin reejecutar imports, migraciones, materializaciones, auditorías de operadores ni gates históricos. Estado de entrada: `main` en `258fad1`; dos informes M06-B02 locales no versionados, preservados. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## 1. Historia relevante

La línea GTFS Explorer Desktop pasó por `0.1.0-rc1` (producto local GTFS Schedule y límites explícitos), `0.1.0-rc2` (round-trip y E2E), `0.1.0` (aceptación estable), `0.2.1` (volumen, paginación, integridad de exportación y migraciones 8→11) y `0.2.2` (contrato enum corregido y release protegido). `CHANGELOG.md`, `REPRODUCIBILITY.md` y `docs/CURRENT_STATE.md` gobiernan esta reconstrucción; los informes de Engineering documentan los incidentes sin modificar el producto. La variante `0.2.0` aparece en arquitectura y acceptance, pero el changelog consultado no la presenta como release estable autónomo.

Transit Data Lab separó luego el laboratorio de datos, el producto independiente y Compliance. La baseline raíz conserva investigación y fuentes capturadas. `01_Research_Standards` es estructura planificada, no una implementación completada. Compliance Phase 1 congeló el corpus de 92 provisions; Phase 2 separó source facts de interpretación, pasó por dos gates humanos, materializó 48 requisitos y 10 deadlines y estableció un freeze formal. Phase 3 creó infraestructura M02, amplió el registro de estándares M02A, incorporó evidencia de estándares M03, un piloto M04, separación entre review de mapping y cobertura M04B, taxonomía familiar M05B y B01 revisado en M06. `M01_NOT_RECOVERABLE`: no reconstruirlo imaginariamente. M05 solo conservaba agregados de clasificación; la baseline M05B documenta los IDs actuales sin atribuir falsamente movimientos históricos.

`PROJECT_STATUS.md` (2026-09-27) señala B02 como no iniciado. Al abrir este trabajo ya existían dos archivos B02 no versionados: research R1/R2/R3 y paquete de candidatos. Son posteriores a ese estado publicado, no equivalen a revisión humana ni a DB actualizada. El paquete declara 8 candidatos y tres conceptos P02 sin resolver; termina en `HUMAN_REVIEW_READY = PARTIAL`.

## 2. Lecciones y fallos reales

* En Bizkaibus se detectaron 1.040.852 incidencias históricas, 100.000 persistidas y 940.852 omitidas. El contrato enum compartido entre normalización y validación era erróneo. GTFS-023 invalidó esos hallazgos como `FALSE_POSITIVE_ENUM_CONTRACT`; el resultado aceptado posterior fue 0/0/0, sin afirmar que el operador corrigiese un millón de defectos. Una `TransactionException` no se reprodujo, sin que ello demuestre causalidad. Fuentes: Desktop `CHANGELOG.md`, `docs/CURRENT_STATE.md`; Engineering `GTFS-023_BIZKAIBUS_EXTERNAL_ACCEPTANCE.md`.
* Una prueba de fase histórica aplicada a una base posterior produjo 27 PASS / 1 FAIL por expectativas de staging anteriores a la materialización. `TEST_BASELINE_POLICY.md` clasifica la diferencia como `EXPECTED_HISTORICAL_STATE_MISMATCH`, conserva la evidencia y señala el gate posterior apropiado. No parchear expected counts ni pintar verde el fallo histórico.
* Gate 2 separó expresiones de tiempo funcional de fechas, conservó siete dependencias PARTIAL y requirió un source fact 9(3) antes de materializar. Un actor no especificado no se inventa. La materialización y freeze tenían hashes y reconciliaciones; un desajuste detuvo la promoción y se conservó el intento.
* B01 mostró que un deber institucional no exige un mapping de formato. La expresión histórica «servicios de localización» se investigó hasta distinguir búsqueda de datos mediante metadatos de geolocalización. `NAP_DATA_DISCOVERY` se aprobó con `standard_id = NULL`, cobertura PARTIAL y ruta manual simultánea, sin inferir implantación ni cumplimiento.
* B02 muestra riesgo de sucesión normativa: el requisito congelado cita literalmente 2015/962, derogado; R3 documenta la guía interpretativa de la Comisión sobre referencias dinámicas a 2022/670. La guía se declara informativa y no modifica el texto histórico. Los perfiles DATEX II/SIRI se proponen por concepto, con categorías aún no resueltas, sin dataset observado.

## 3. Modelo mental comprobado

La consulta DuckDB `-readonly` encontró `source.documents` (identidad, autoridad, versión, URL, hash), `source.provisions` (fragmento localizado), `compliance.source_facts` (hecho literal y versión), `compliance.requirement_candidates` (interpretación y estado de revisión), `compliance.requirements` (universo materializado) y `compliance.deadlines`. La jerarquía de Phase 3 comprende `mapping.phase3_standards` (identidad, versión/perfil, vigencia y estado), `phase3_capabilities`, `phase3_source_references`, `phase3_requirement_capabilities`, `phase3_mapping_reviews`, `phase3_requirement_coverage`, `phase3_representability`, `phase3_observed_evidence`, `phase3_automatability`, `phase3_families`, `phase3_requirement_families` y `phase3_exceptions`. `audit.rules` existe, con 0 filas.

Los IDs de `source_fact_id`, `requirement_id`, `standard_id`, `capability_id`, `mapping_id` y `coverage_id` identifican entidades diferentes. La DB contiene 48 requirements, 36 source facts, 6 mappings, 8 coverage decisions, 0 observed evidence y 0 audit rules. El SQL actual impone estados mediante `CHECK`; `validate_phase_3_level_a.sql` y validators específicos verifican además referencias lógicas. El modelo permite capacidad funcional sin estándar y exception más mapping para el mismo requisito. No equiparar cobertura semántica con cumplimiento jurídico, representabilidad con presencia en un dataset, potencial de automatización con auditoría ejecutada ni ausencia de mapping con incumplimiento.

## 4. Autoridad y protección

`AGENTS.md`, `README.md` y `PROJECT_STATUS.md` orientan el estado operativo. `PHASE_2_REQUIREMENTS_ENGINE.md` y los informes de Gates 1/2 explican extracción y decisiones; `PHASE_2_FORMAL_FREEZE.md`/JSON y `TEST_BASELINE_POLICY.md` delimitan el estado congelado y las pruebas autoritativas. `PHASE_3_M02_FRAMEWORK.md`, SQL/migraciones actuales, `PHASE3_FAMILY_BASELINE_V1.md`, `M06_B01_HUMAN_REVIEW.md` y validators definen Phase 3. `PROJECT_CURRENT_STATE.md`, `project_baseline.json`, snapshots e informes anteriores son evidencia de su momento, no estado vivo. La DB se consulta read-only; solo una intervención autorizada y trazable puede escribir.

`_Sources/SOURCE_MANIFEST.txt` distingue legislación UE (EUR-Lex), España (BOE) y políticas/guías NAP. `NAP_POLICY` o regla de validador no se convierte en ley. Conservar URL oficial, versión/fecha, referencia exacta, archivo/hash cuando proceda, y relación entre hecho literal e interpretación. Las fuentes de perfiles GTFS, GTFS-RT, NeTEx, SIRI y DATEX II requieren versión y ámbito concretos; identidad de estándar no implica cobertura. Consultar fuentes externas solo ante una pregunta acotada que no resuelva la evidencia local.

## 5. Antipatrones

Abrir una fase posterior editando Phase 1/2; ejecutar masters antiguos contra base acumulativa; sustituir el `PARTIAL` por `PASS`; inventar actor, fecha, perfil, mapping o cobertura; usar un resultado masivo de herramienta como prueba de defecto del operador; confundir un capability de descubrimiento con designación NAP; tratar un perfil como evidencia de publicación; convertir una norma sucesora en enmienda literal sin fuente; reescribir un run invalidado; mezclar GTFS raw y Compliance; recorrer backups/datasets o repos anidados por defecto; reintentar un fallo sin hipótesis nueva; pisar archivos B02 locales.

## 6. Revisión del candidato V0

El borrador llegó durante el discovery en `skills/compliance_eu/SKILL.md`; `CODEX_RUN_PROMPT.md` acompaña al borrador, pero la misión actual exige reconstrucción, no copiarlo literalmente. El árbol `skills/` era preexistente y no se editó. Matriz de decisiones:

| Regla V0 | Evidencia | Acción |
|---|---|---|
| Leer AGENTS/README/estado, comprobar Git y preservar cambios | Gobierno raíz, dos archivos B02 locales, `AGENTS.md` | KEEP; leer evidencia posterior del milestone cuando el estado se haya quedado atrás |
| Phase 1/2 protegidas; no cambiar hashes/expected | Formal freeze y `TEST_BASELINE_POLICY.md` | KEEP; distinguir propuesta de corrección y permiso efectivo |
| Separación coverage, mapping, representability, observed evidence, automatability y legal compliance | `PHASE_3_M02_FRAMEWORK.md`, M04B SQL, DB real | KEEP; añadir source/provision/source fact/candidate y review semántica explícitas |
| Research dirigido, fuentes oficiales, versión/perfil | M03/B01/B02 research y `_Sources/SOURCE_MANIFEST.txt` | REFINE; clasificar autoridad jurídica, política NAP y especificación; registrar carácter informativo de guías y fecha de contexto |
| Familia como planificación y rutas no técnicas | `PHASE3_FAMILY_BASELINE_V1.md` y B01 | KEEP; permitir mapping funcional sin standard_id y coexistencia de exception |
| Bloque B02 inicial y conteos M04 «pendientes» | Estado publicado y artefactos posteriores; M04B reviews/coverage ya persistidos | UPDATE; eliminar estado fijo de la Skill y consultar estado/candidatos locales cada vez |
| «Permitido» crear seeds, reglas y assertions en cualquier tarea explícita Compliance | Los milestones separan generación, revisión humana y persistencia | REFINE; autorizar según lote y gate concreto, no por mera pertenencia al área |
| `BLOCKED` para cualquier perfil faltante, fuente ausente o commit no autorizado | B02 es `PARTIAL` y admite candidatos de conceptos apoyados; un commit puede omitirse | GENERALIZE; reservar BLOCKED a dependencia material, documentar incertidumbre local y parar en gate humano |
| Vocabularios de resultados técnicos y Definition of Done extensa | `audit.rules` vacío; no hay vocabulario de resultados ejecutados validado para Phase 3 | REMOVE como prescripción actual; exigir diseñar regla/estado desde contrato vigente cuando exista milestone |
| Primera misión tras instalar, plantilla larga de salida | Estado mutable, instrucción actual y economía de contexto | REMOVE; el arranque y checkpoint breves bastan |
| Defensa frente a falsos positivos propios e integridad de ejecución/exportación | GTFS-023, aceptación Bizkaibus y `REPRODUCIBILITY.md` | ADD; parada y comprobación de herramienta antes de atribuir finding |
| Test histórico incompatible y evidencia invalidada | `TEST_BASELINE_POLICY.md` y runs Desktop | ADD; no reutilizar gate antiguo, conservar bytes y añadir conclusión actual separada |

## 7. Diseño propuesto

Crear `.agents/skills/compliance_eu/SKILL.md` como entrada corta: bootstrap por estado actual, ruta según tarea, cadena de evidencia, protección de fases, método de mapping/cobertura, verificación específica, autoconfianza limitada y parada/human gate. Añadir solo una referencia estable de fallos y pruebas históricas para que la guía cotidiana no cargue incidentes largos. No duplicar el esquema entero ni crear plantillas vacías: el SQL y los informes son autoridad. El discovery presente conserva la reconstrucción extensa. La Skill debe apuntar a `PROJECT_STATUS.md` para el hito vigente; ningún M06 fijo en su frontmatter.

## 8. Preguntas abiertas y piloto

1. B02 requiere revisión semántica humana de ocho candidatos y tres conceptos irresueltos. El informe local es `PARTIAL`, no autoriza persistir nuevas capacidades, mapping, cobertura o representabilidad.
2. La concordancia jurídica detallada de algunos conceptos P02 con elementos/perfiles y versiones sigue sin demostrar; no rellenarla por analogía.
3. La misión no aporta una decisión humana sobre las propuestas B02. La Skill puede guiar el examen y detener la persistencia en ese gate.

El piloto posible ahora es aplicar la Skill al paquete B02 en modo read-only, comprobar su trazabilidad, conteos y límite de autoridad, y detenerse en el gate humano. No se realizará una revisión humana simulada como si fuera aprobación real.
