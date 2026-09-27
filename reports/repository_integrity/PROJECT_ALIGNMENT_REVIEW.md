# Transit Data Lab — revisión de coherencia del proyecto

Fecha: 2026-09-27. Resultado: **alineación documental completada; pendientes técnicos y de recuperación explícitos**. Esta revisión no certifica el producto, el corpus jurídico, la seguridad del contenido publicado ni un backup integral.

## Alcance y fuentes

Revisión estructural de los 136 Markdown inicialmente elegibles del Git padre (902.862 bytes), navegación local, codificación y contratos de estado; lectura dirigida de gobierno, fases, baselines, informes de migración, scripts y tests. No es una revisión jurídica de todos los textos. Los repositorios independientes de Products se inspeccionaron mediante metadatos Git, sin recorrer ni modificar sus árboles. No se ejecutó Desktop ni se auditó funcionalmente su código.

Se consultaron directamente las referencias anunciadas por los dos remotos y su visibilidad mediante Git/gh. Se verificaron los hashes de las dos bases y documentos congelados concretos; no se realizó hash global ni recorrido de datasets, entornos, backups o binarios. Las fuentes actuales prevalecen sobre informes antiguos para describir el estado operativo.

## Hallazgos y resolución

| ID | Impacto | Hallazgo comprobado | Resolución o pendiente |
| --- | --- | --- | --- |
| ALIGN-01 | Alto | Documentos que dicen «sin commits/remoto» o snapshot BLOCKED pese a existir baseline local/remota. | Nueva entrada README y PROJECT_STATUS; política, estructura y recuperación actualizadas. Instantáneas y fallos originales conservados. |
| ALIGN-02 | Alto | Informes anteriores describen UNRELATED_HISTORIES contra el remoto que entonces contenía Desktop. | Comprobación actual: raíz y origin/main/tdl-baseline-v0.1 coinciden; Desktop tiene otro remoto. El bloqueo es histórico. No merge/rebase/push. |
| ALIGN-03 | Alto | Ambos repositorios son públicos; documentación previa habla de repositorio privado. | Estado actual registrado. No cambio de visibilidad ni nueva publicación. No se certifica que todo el contenido publicado pueda compartirse ni ausencia de secretos. |
| ALIGN-04 | Alto | Desktop tiene 20 entradas locales, incluyendo código/tests; no es working tree limpio de 0.2.2. | Etiqueta 0.2.2 y HEAD comprobados; cambios previos conservados. Revisión funcional de esos cambios requiere una tarea específica del producto. |
| ALIGN-05 | Medio | Business AGENTS/README dicen Phase 1; decisiones/estado indican Phase 3. | Gobierno vigente alineado con V1 FROZEN, Phase 3 IN_PROGRESS, Stage 1 INCOMPLETE y Stage 2 no autorizado. Sin avanzar fases/gates. |
| ALIGN-06 | Medio | GTFS_Lab README vacío; confusión de laboratorio/producto y ausencia de guía segura del import. | Guía operativa añadida, capas pendientes y escritura del import explícitas. No ejecución de imports. |
| ALIGN-07 | Medio | 19 README de operadores con placeholders literales y NUL; otras guías con codificación dañada. | 26 documentos reparados de forma dirigida; ID/familia tomados de metadata existente. Fuentes, metadata y manifests preservados. |
| ALIGN-08 | Medio | Catálogo de operadores: 12 cabeceras y 11 celdas, desplazando SIRI y columnas posteriores. | Tabla de 20 filas reconstruida desde el manifest preservado; presencia inventariada, no afirmación sobre servicio real. |
| ALIGN-09 | Medio | README piloto con hash en Business V1 contiene corrupción y descripción de privacidad inicial. | Bytes conservados; CURRENT_DOCUMENTATION explica el registro histórico y da navegación vigente. CHANGELOG histórico tampoco se reescribe. |
| ALIGN-10 | Alto | Master Phase 2 test 23 exige trazabilidad al staging inicial para 45 requisitos materializados después por universo aprobado. | Ejecución actual: 27 PASS / 1 FAIL, actual=45. Clasificado como incompatibilidad del contrato histórico; política de tests actualizada. No «PASS» artificial ni cambio de SQL/base congelados. |
| ALIGN-11 | Medio | Gate final tiene 13 rutas absolutas: tres valores de metadata esperada y diez read_blob jurídicos. | Portabilidad pendiente documentada. Se contrastaron 377 assertions de filas excluyendo diez hashes jurídicos; no se ejecutó el gate completo ni se modificaron sus bytes. |
| ALIGN-12 | Medio | Baselines y Git no cubren bases, originales, grandes generados ni repos anidados; GIS sin generador. | Recuperación y límites actualizados. Backup integral y replay portable no acreditados por esta revisión. |

Las menciones históricas a GTFS Explorer Desktop 0.2.1, RC-002 y candidate001 se conservan como procedencia de resultados. No son instrucciones para renombrar el proyecto global ni para cambiar la versión del release protegido. La baseline raíz tdl-baseline-v0.1 y el release de producto v0.2.2 son identidades distintas.

## Evidencia y comprobaciones

Artefactos bajo `alignment_20260927/`:

- `before.json` y `after.json`: inventario Markdown, enlaces locales, sintaxis Python, metadatos Git y hashes concretos antes/después.
- `remote_observation.json`: stdout/stderr y exit codes de consultas remotas y de visibilidad, sin operaciones de publicación.
- `documentation_repairs.json`: rutas y hashes antes/después de las 26 reparaciones documentales.
- `powershell_syntax.json`: análisis sintáctico de 14 scripts, sin ejecutarlos.
- `compliance_phase_2.stdout.json`, `.stderr.txt`, `.exit_code.txt`, `.summary.json`: resultado íntegro del master inicial; 27/28 PASS y un FAIL histórico explícito.
- `compliance_frozen_rows.sql`, `.stdout.json`, `.stderr.txt`, `.exit_code.txt`, `.summary.json`: 377/377 PASS de assertions del estado congelado actual; diez checks jurídicos excluidos. La primera invocación por -c excedió el límite Windows antes de iniciar DuckDB; el mismo SQL se ejecutó por stdin y se conserva íntegro.
- `document_validation.json`: tabla 20×12, concordancia de IDs/familias con metadata, controles de caracteres y huellas de documentos congelados comparadas con el commit.

Las dos bases coinciden con los hashes registrados GTFS `f4186d60…` y Compliance `823999a9…`; el detalle completo figura en PROJECT_STATUS y los JSON. La comparación final verifica que bases, documentos protegidos, HEAD/tag raíz y HEAD/tag/estado de repositorios anidados se conservan respecto del inicio.

Las referencias locales ausentes detectadas inicialmente son 23 enlaces de dos README externos capturados como evidencia, a archivos de sus repositorios originales. Se preservan; no se presentan como navegación local del proyecto. La comprobación de enlaces no valida URLs externas, anchors ni enlaces por referencia. La codificación dañada restante en el README piloto/CHANGELOG es histórica y está documentada.

## Cambios y pendientes

Documentos vigentes nuevos: README.md, AGENTS.md, PROJECT_STATUS.md, guía CURRENT_DOCUMENTATION del piloto y este informe. Actualizados: PROJECT_STRUCTURE, REPOSITORY_POLICY, BACKUP_AND_RECOVERY, gobierno/estado Business, política de tests Compliance y README GTFS_Lab. Reparadas 26 guías piloto. Añadido `tools/audit_project_alignment.py` para repetir controles documentales acotados.

No se modificaron bases, corpus, SQL/scripts originales, manifests, baseline Business, registros congelados ni repositorios del producto. Los tres informes untracked preexistentes permanecen conservados. No commit, staging, push, merge, rebase, cambio de permisos/visibilidad ni contacto con terceros.

Pendientes: revisar cambios locales de Desktop en una tarea del producto; decidir si la visibilidad pública es la deseada; acreditar backup independiente de datos/repositorios; resolver portabilidad del gate mediante un procedimiento que respete el freeze. Core/validation/analysis, replay GIS, mappings, reglas y gates empresariales siguen en los estados existentes. No se han implementado para ampliar esta revisión.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
