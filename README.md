# Transit Data Lab

Transit Data Lab es el proyecto global de investigación, ingeniería de datos, compliance, interoperabilidad, auditoría y exploración empresarial del transporte público. GTFS Explorer Desktop es un producto independiente dentro de ese proyecto; su baseline protegida permanece en **0.2.2**.

## Estado y navegación

La entrada vigente es [PROJECT_STATUS.md](PROJECT_STATUS.md). Describe el estado comprobado y separa los documentos actuales de las instantáneas congeladas.

| Documento o área | Finalidad |
| --- | --- |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Estado vigente, baselines, Git y pendientes. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Componentes, flujo y límites. |
| [Conocimiento de ingeniería](knowledge/README.md) | Lecciones curadas con fuentes. |
| [Reconciliación local V2](reports/LOCAL_ENVIRONMENT_RECONCILIATION_V2.md) | Cierre comprobado y residuos protegidos. |
| [Revisión de integridad y salud V1](reports/PROJECT_INTEGRITY_AND_HEALTH_REVIEW_V1.md) | Estado canónico, integridad, repos, datos, junctions y límites. |
| [Matriz de validación V1](reports/PROJECT_VALIDATION_MATRIX_V1.md) | Suites/gates ejecutados, resultados y cobertura no ejecutada. |
| [Análisis de gaps V1](reports/PROJECT_GAP_ANALYSIS_V1.md) | Prioridades antes de piloto externo y distribución. |
| [REPOSITORY_POLICY.md](REPOSITORY_POLICY.md) | Separación de repositorios y preservación de evidencia. |
| [BACKUP_AND_RECOVERY.md](BACKUP_AND_RECOVERY.md) | Cobertura Git y recuperación de datos excluidos. |
| [GTFS_Lab](02_Data_Engineering/GTFS_Lab/README.md) | Operación y límites del laboratorio GTFS. |
| [Precondiciones del GTFS Audit Engine](reports/repository_integrity/TDL_GTFS_ENGINE_PRECONDITIONS_PACK_CLOSURE.md) | Pack P1, comandos portables, evidencia local y límites de CI. |
| [G02 Rule Registry + Specification Contract](reports/repository_integrity/GTFS_AUDIT_ENGINE_V1_G02_SPECIFICATION_CONTRACT.md) | Contrato tipado inicial de reglas, applicability, cobertura e identidad por regla. |
| [Business](07_Business/README.md) | Capacidades, evidencia y gates empresariales. |
| [Revisión de alineación](reports/repository_integrity/PROJECT_ALIGNMENT_REVIEW.md) | Hallazgos, cambios y verificación de esta revisión. |

`PROJECT_CURRENT_STATE.md`, `project_baseline.json`, `PROJECT_SNAPSHOT_V0.1.md` y los informes de ejecuciones anteriores son registros históricos. Sus afirmaciones sobre commits, remotos o fases se interpretan en el momento de su creación. Se conservan sus bytes y no deben utilizarse aisladamente como estado vigente.

## Operación en la partición dedicada

Raíz Git canónica: `P:\TransitDataLab\01_Project\Transit Data Lab`. Datos, evidencia física, runtime y cliente se conservan en áreas separadas de `P:\TransitDataLab`; los binarios y entornos antiguos no forman parte del checkout. [Cierre y límites de la migración](reports/DEDICATED_PARTITION_MIGRATION_V1.md).

```powershell
. .\tools\activate_tdl.ps1
Set-Location (Join-Path $env:TDL_PROJECT_ROOT '02_Data_Engineering\GTFS_Lab')
& "$env:TDL_RUNTIME_ROOT\Current\TDL\Scripts\python.exe" -m gtfs_lab.test_bank --help
```

La activación usa [config/tdl_paths.json](config/tdl_paths.json) y admite `-Root` o `TDL_ROOT` para otra ubicación. Solo configura el proceso actual. El banco predeterminado es `TDL_DATA_ROOT/TestBank`; `--bank` conserva su override. Los resultados nuevos van a `04_Runtime`, y los datos originales/evidencia congelada se preservan.

## Identidad

El nombre del proyecto global es Transit Data Lab. Los nombres GTFS Explorer Desktop, GTFS_Lab y las versiones históricas de sus resultados se mantienen para conservar la identidad y procedencia de cada componente. El nombre empresarial sigue siendo provisional según el gobierno Business; no implica disponibilidad jurídica de marca.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
