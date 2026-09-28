# Prueba estática y piloto read-only de compliance_eu

Fecha: 2026-09-28. Basado en `.agents/skills/compliance_eu/SKILL.md`. Sin aprobación semántica simulada, cambios de DB, ejecución de seeds o contacto externo. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Cuatro escenarios

| Caso | Evidencia real | Decisión guiada por la Skill |
|---|---|---|
| A. Mapping técnico claro | B02 `A05-P01-002` y tiempos de viaje medidos en enlaces de carretera; perfil MMTIS Level 2 y capacidad `CAP-DATEXII-RRP-ROAD-TRAVEL` | Candidate técnico acotado, con versión de modelo no establecida y puente jurídico informativo expresos. Revisión humana antes de persistir. No se infiere dataset publicado. |
| B. Deber procedimental | B01 `A03-P01-001` establece el NAP | Ruta `LEGAL_PROCESS`, sin forzar estándar ni capability de formato; cobertura PARTIAL no es cumplimiento. |
| C. Ambigüedad parcial | B02 `A05-P02-001` y tarifas, vehículos compartidos o aparcamiento del Annex 2.2 | Tres conceptos `UNRESOLVED`, investigación concreta del perfil/elemento; no se fabrica DATEX II, SIRI ni un mapping global. |
| D. Posible falso positivo propio | Bizkaibus histórico y contrato enum GTFS-023 | Se detiene la atribución; se comprueban especificación, enum, normalizador, validador, persistencia/exportación y fuente original. Los 1.040.852 hallazgos quedan invalidados como error de producto, sin reescribir el run ni atribuir corrección al operador. |

## Ejecución piloto: M06-B02

`PROJECT_STATUS.md` del 2026-09-27 decía `M06-B02_PLANNING`; al inicio ya existían `M06_B02_TARGETED_RESEARCH.md` y `M06_B02_CANDIDATES.md` como cambios locales no versionados. No se editaron. El primero registra R3 `PASS` para el puente interpretativo y límites de su fuerza jurídica; el segundo concluye `COMPLIANCE_PHASE3_M06_B02_CANDIDATE_GENERATION = PARTIAL` y `HUMAN_REVIEW_READY = PARTIAL`.

Una consulta DuckDB `-readonly` comprobó ambos IDs en `compliance.requirements`; P01 es `FORMAT` no condicional y P02 es `FORMAT` condicional con referencia a Annex 2.1/2.2. Para P02 se documentan rutas candidatas SIRI/DATEX II, sujetas a revisión por concepto. Lectura dirigida de la tabla de candidatos: P01 tiene tres, P02 cinco; DATEX II seis y SIRI dos, total ocho. Tres conceptos P02 permanecen `UNRESOLVED`. La DB aún tiene 48 requirements, 36 source facts, seis mappings y ocho coverage decisions de hitos previos, cero observed evidence y cero audit rules. Ningún candidato B02 se ha persistido según el paquete y no se ejecutaron escrituras en este piloto.

El caso de tiempos futuros merece atención humana específica: el propio paquete reconoce que no hay categoría discreta Annex 2.1/2.2 establecida y propone `PARTIAL`. La Skill impide convertir esa propuesta en cobertura plena. Para facility status SIRI falta correspondencia precisa Annex-elemento. Las recomendaciones `ACCEPT_WITH_LIMITATIONS` del paquete siguen siendo recomendaciones, no decisiones humanas.

**Resultado:** checkpoint de revisión documental read-only completado; B02 `PARTIAL`, detenido en `M06_B02_HUMAN_REVIEW`. La decisión humana debe resolver cada candidato, el alcance de las tres capacidades propuestas y el destino de los tres conceptos irresueltos antes de diseñar seeds o validators de persistencia. No se atribuye incumplimiento a ningún NAP u operador.

## Verificación y límite

`quick_validate = NOT_EXECUTED`; `reason = missing yaml dependency`. En esta revisión se intentó `py -3.12 C:\Users\yeiso\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/compliance_eu` (exit code 1): el script terminó en `ModuleNotFoundError: No module named 'yaml'` antes de validar la skill. Los Python 3.12 y 3.14 disponibles carecen de `yaml`; no se instaló ninguna dependencia ni se modificó el entorno. La validación local de frontmatter, nombre, enlace a la referencia y ausencia de placeholders pasó en el piloto anterior; no equivale a un PASS de `quick_validate.py`. La inspección de espacios finales pasó para los cuatro archivos nuevos. `git diff --check` devolvió 0, aunque por sí solo no cubre archivos no versionados. Una consulta adicional `-readonly` encontró 0 mappings persistidos para los dos requisitos B02. Los archivos de Phase 1/2 y datos no se modificaron. `PROJECT_STATUS.md` se preserva: el piloto no ha completado B02 y los dos informes B02 son trabajo local aún no integrado.
