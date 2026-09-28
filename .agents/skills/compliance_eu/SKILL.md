---
name: compliance_eu
description: Continuar investigación, modelado y validación de Compliance UE en Transit Data Lab con trazabilidad de fuentes, fases protegidas y gates humanos. Usar en tareas de 03_Compliance; no para auditar automáticamente operadores ni para modificar el producto Desktop.
---

# Compliance UE — método operativo

## Arranque y alcance

Trabaja desde la raíz de Transit Data Lab. Lee `AGENTS.md`, `README.md`, `PROJECT_STATUS.md` y `03_Compliance/TEST_BASELINE_POLICY.md`; comprueba `git status`, rama y cambios locales. Abre solo el milestone, SQL, validator y fuentes directamente relacionados con la tarea. El estado mutable se determina en `PROJECT_STATUS.md` y se contrasta con la evidencia más reciente del milestone; un documento local más reciente puede demostrar trabajo en progreso, pero no reemplaza por sí solo `PROJECT_STATUS.md` ni una decisión humana. No hagas recorridos de datasets, backups o repos independientes por defecto. El historial metodológico y los fallos concretos están en [FAILURE_PATTERNS.md](references/FAILURE_PATTERNS.md); léelo cuando se diseñe una regla, se triage un resultado sorprendente o se trabaje con freeze/gates.

Define objetivo, lote autorizado, estado inicial, límite de escritura y criterio de cierre antes de actuar. Si la tarea es solo documental o de investigación, mantén DB y corpus en solo lectura. Consulta DuckDB con `-readonly` y SQL dirigido; no uses orquestadores que migren o materialicen por accidente. Preserva los cambios preexistentes y comprueba el diff final.

## Cadena de autoridad y evidencia

Separa: fuente legal y su versión → provision localizada → `source_fact_text` literal → candidato interpretado y revisión humana → requirement materializado → contexto de norma/perfil → capacidad técnica o funcional → mapping y revisión semántica → decisión de cobertura → representabilidad → evidencia observada → automatizabilidad → regla/resultado de auditoría. No saltes de una capa a otra mediante semejanza verbal. Comprueba tabla, PK, estado y relaciones reales en SQL antes de escribir; el modelo está explicado en `03_Compliance/PHASE_3_M02_FRAMEWORK.md` y el esquema vigente en `sql/00_setup`.

Clasifica la fuente antes de inferir obligaciones: legislación UE/BOE, política NAP, guía, especificación/perfil o regla de validador son autoridades distintas. Busca primero corpus y manifests locales; si falta un hecho actual o un vínculo preciso, formula una pregunta de investigación acotada y consulta fuentes oficiales primarias. Conserva URL, fecha de consulta, versión/consolidación, cita exacta, ámbito y límites. Una derogación o norma sucesora aporta contexto, pero no reescribe el hecho literal congelado. Si una guía interpreta una referencia, anota su carácter vinculante o informativo. Usa `UNKNOWN`/`NEEDS_REVIEW` si no se demuestra el puente.

Para GTFS, GTFS-RT, NeTEx, SIRI y DATEX II, distingue familia, versión, perfil, ámbito modal, concepto/elemento y periodo de vigencia. `registry_status = IDENTITY_ONLY` no prueba capacidad. Propón un mapping solo si requirement, concepto, estándar/perfil y fuente coinciden; registra condición, alcance parcial y evidencia. No fuerces una capacidad de formato para deberes institucionales, temporales o procedimentales: evalúa `phase3_exceptions` y rutas híbridas. La familia es metadato de planificación, no interpretación jurídica.

Revisa por separado cada mapping en `phase3_mapping_reviews` y la cobertura del requirement en `phase3_requirement_coverage`. `ESTABLISHED` describe cobertura semántica en el alcance revisado, no cumplimiento legal. La ausencia de mapping no prueba incumplimiento. `phase3_representability` expresa posibilidad técnica según perfil; `phase3_observed_evidence` requiere observación identificable de implementación/dataset, fecha y locator. No registres como ausencia de datos que aún no se hayan inspeccionado. `phase3_automatability` valora condiciones de una futura prueba; no es una regla ejecutada. No inventes vocabulario ni resultados para `audit.rules` hasta que exista un contrato aprobado para ese milestone. Una `audit.rules` solo procede con requisito, semántica, evidencia y contrato de validación revisados, falso positivo evaluado y autorización de su milestone; nunca emite por sí sola una conclusión jurídica.

## Fases protegidas y verificación

Phase 1 y Phase 2 están `FROZEN`. Lee sus tablas, fuente y evidencia en modo read-only. No cambies requirements, source facts, deadlines, corpus, manifests, hashes o informes históricos para hacer pasar Phase 3. Una corrección requiere propuesta nueva, impacto, gate humano y procedimiento de baseline explícito; la evidencia anterior se conserva y se anota su validez actual. Si falta un estado histórico, no lo reconstruyas a partir de agregados o del estado presente: `M01_NOT_RECOVERABLE` permanece así hasta que aparezca evidencia histórica auténtica. `project_baseline.json` y `PROJECT_CURRENT_STATE.md` son snapshots, no ficheros de estado cotidiano.

Selecciona validators de la fase y lote actuales según `TEST_BASELINE_POLICY.md`; captura comando, exit code, conteos y evidencia. Verifica invariantes y delta de escritura, idempotencia cuando corresponda y estado protegido. No ejecutes masters Phase 1 o pre-materialización como gate de la DB posterior ni alteres expected counts para obtener verde. Un PASS técnico, documental o de fixture no aprueba aceptación humana, implantación observada ni cumplimiento jurídico. Detente si hash protegido difiere, falla un invariante, un validator no corresponde a la fase o no puede explicarse el delta.

## Autoconfianza limitada y parada

Desconfía también de las reglas y conclusiones de Transit Data Lab. Ante un finding masivo, extremo o inesperado: detén la atribución; contrasta especificación y versión, interpretación, contrato/implementación del validador, integridad de ejecución y exportación, y finalmente datos originales y provenance. Solo después clasifica si el defecto pertenece a la herramienta, al dataset o sigue abierto. Conserva runs invalidados con addendum; no los reinterpretes como correcciones del operador. La historia Bizkaibus enum es el caso de referencia.

Detente en `BLOCKED` o `PARTIAL` cuando falte fuente, correspondencia de perfil, evidencia observada, estado reproducible o decisión humana. La investigación dirigida puede producir candidatos; no convierte propuestas en aprobaciones. No hagas commit, push, merge, tag, publicación, contacto con terceros ni cambios de repos independientes sin autorización expresa. Para cerrar, registra lote/IDs, fuente y versión, decisiones frente a propuestas, tablas/archivos tocados, conteos antes/después, validators y salida, limitaciones, estado del gate humano, cambios locales preservados y siguiente acción. Actualiza `PROJECT_STATUS.md` solo si el estado operativo ha cambiado materialmente.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
