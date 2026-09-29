# Backup y recuperación

Política documentada el 2026-09-27; la afirmación de que HEAD coincidía con `tdl-baseline-v0.1` describe solo aquel snapshot. El estado Git actual se consulta en [PROJECT_STATUS.md](PROJECT_STATUS.md) y en el remoto. No se acredita copia física integral, restauración probada ni backup de datos excluidos. El bloqueo inicial por evidencia HTML corresponde a un intento histórico conservado.

## VERSIONED IN GIT — snapshot local y remoto existentes

El commit raíz conserva fuentes SQL/Python/PowerShell, Markdown, CSV/JSON de evidencia seleccionada, manifests, informes de gates (incluidos fallos), registros de freeze, gobierno Business y PDF jurídicos. Los documentos nuevos y cambios sin commit posteriores no quedan cubiertos por ese snapshot. FIRST_FORMAL_COMMIT_MANIFEST.csv y su audit son registros del intento previo, no un inventario actualizado del índice.

Reconstruir el contenido versionado de la baseline mediante checkout de tdl-baseline-v0.1 en un destino independiente. Verificar el commit y tag sin modificar informes históricos. Una copia o git bundle adicional y una restauración acotada siguen siendo operaciones separadas; no se han ejecutado en esta revisión. Un Git local en el mismo disco no protege de avería/ransomware.

## NOT VERSIONED / REGENERABLE

Entornos, cachés, builds y temporales, siempre que sus fuentes/dependencias estén disponibles. Las extracciones de feeds se pueden regenerar solo a partir del ZIP exacto conservado; descargar una versión nueva no reconstruye la historia. No se regeneran en esta tarea.

## NOT VERSIONED / MUST BE BACKED UP SEPARATELY

| Ruta o categoría | Propósito / requisito |
| --- | --- |
| 02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb | Base raw autoritativa; conservar copia consistente y SHA del baseline |
| 03_Compliance/databases/transit_compliance.duckdb | Base Compliance V1 actual, con Phase 1/2 congeladas y capas posteriores aprobadas; copia consistente y SHA del estado vigente, sin modificar metadata |
| 03_Compliance/reports/phase_2/materialization/PRE_WRITE_DATABASE_BACKUP.duckdb | Copia previa a escritura; histórica, no presumir que equivale a Phase 2 actual |
| GTFS_Lab/feeds/raw y feeds/extracted | Snapshot Asturias; ZIP exacto necesario |
| 20_clientes_reales/**/02_sources/gtfs_schedule/original y extracted | Snapshots piloto históricos; manifests en Git no sustituyen sus bytes |
| 20_clientes_reales/**/data.duckdb y *.duckdb.editor-pre-migration.bak | Resultados y recuperación de runs del piloto; conservar por procedencia |
| Bizkaibus run_001 JSON/ZIP/informe-validacion.html y run_002_rc002 ZIP | Generados grandes excluidos; evidencia histórica cuya reproducción exacta no se presupone |
| 07_Business/03_Market/evidence/scope_before.json | Inventario histórico de 70.195.962 bytes, excluido; no regenerar/hash global |
| Exportaciones GIS/KML | Los KML pequeños están versionados; proteger los originales porque no hay generador reproducible |
| Evidencia que contenga credenciales | Conservar en un destino restringido hasta resolución; no publicar ni incluir en backup compartido indiscriminadamente |

- GTFS raw: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Compliance Phase 1 histórico: `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`.
- Compliance Phase 2 actual: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`.
- Business V1 agregado: `5e0635956f40c6fbf27d6c6b16fcac8d4762f3fc1c93793d628c7df24dea30c2`.

GTFS ZIP Asturias SHA persistido: f3093ab85d728ee824ba45cd3f247d1d9ea68a4685aaf25b27a8de98ea50b549. No se han rehasheado bases, feeds ni PDF en esta tarea.

## NESTED REPOSITORY

- `06_Products/GTFS Explorer/GTFS Explorer Artifacts`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Backups/restore_test_v0.2.2_20260924T161533Z_02`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Desktop`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Engineering`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.

Los commits del padre no incluyen commits ni cambios sin commit de estos repositorios. Respaldarlos independientemente con su historial, fuentes locales no confirmadas y manifests; no asumir que un bundle cubre cambios sin commit. Hay directorios de checkpoint y auxiliary_repositories en Products/Backups. Solo se comprobó su presencia superficial: no se certifica integridad ni cobertura del backup actual.

## Procedimiento controlado propuesto

1. Consultar el estado vigente y conservar el registro de sanitización de la fuente histórica; no copiar originales sensibles excluidos a destinos públicos/compartidos.
2. Verificar el commit/tag y el destino remoto actual; preservar por separado los repos anidados y los cambios locales sin commit. No repetir una publicación ya realizada para corregir un informe antiguo.
3. Copiar bases cerradas de forma consistente, el ZIP fuente y evidencia no regenerable a un destino separado y restringido. No copiar un DuckDB abierto o descartar WAL pendientes.
4. Restaurar en un workspace independiente. Comprobar hashes autoritativos dirigidos y manifests existentes; respetar directorios de ejecución de scripts. El replay Compliance requiere decisiones humanas; el GIS no tiene replay completo.
5. No lanzar masters antiguos ni materializaciones automáticamente: contienen expectativas históricas y rutas locales. Los tres local_file absolutos y read_blob absolutos requieren un procedimiento futuro de recuperación compatible con el freeze.

Fuentes: project_baseline.json; PROJECT_CURRENT_STATE.md; Compliance PHASE_1_MANIFEST.csv, PHASE_2_FORMAL_FREEZE.json y manifests de promotion_resume; benchmark_manifest.csv/json; Business baseline V1 y source_manifest*.json. No hay un mecanismo de backup integral automatizado acreditado por esta inspección.


Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
