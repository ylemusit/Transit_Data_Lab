# Arquitectura de Transit Data Lab

Estado y gates: [PROJECT_STATUS.md](PROJECT_STATUS.md). Lecciones reutilizables: [knowledge](knowledge/README.md).

| Área | Responsabilidad y contrato |
| --- | --- |
| `01_Research_Standards` | Fuentes/perfiles y decisiones normativas; distinguir schema, perfil y aceptación NAP. |
| `02_Data_Engineering/GTFS_Lab` | Ingestión, auditoría GTFS Schedule, trust/replay, interpretación, remediation, workflow/Test Bank y cliente interno. |
| `02_Data_Engineering/NeTEx_Lab` | Auditoría NeTEx del alcance técnico aprobado; no presupone conformidad integral EPIP/NAP. |
| `03_Compliance` | Corpus y requisitos congelados, bridges técnicos y resultados con deferrals; no dictamen jurídico. |
| `06_Products` | Repositorios independientes de GTFS Explorer; Desktop baseline 0.2.2 protegida. |
| `07_Business` | Gates documentales y validación comercial separada; no contacto autorizado por un PASS técnico. |
| `reports` / `knowledge` | Evidencia de claims frente a lecciones curadas; el estado actual pertenece a PROJECT_STATUS. |

## Flujo y límites

Entrada controlada → fuente inmutable e identidad → auditoría → interpretación con accounting → informe/entrega → hashes, manifest/seal y replay. La interpretación conserva los findings RAW y distingue observación, inferencia e impacto. El cliente Windows ejecuta el workflow como worker separado y resuelve recursos del paquete onedir; es tooling interno.

Git/GitHub conserva fuente, configuración reproducible, documentación y evidencia seleccionada. Bases, feeds y outputs grandes requieren retención externa controlada: [política](REPOSITORY_POLICY.md), [recuperación](BACKUP_AND_RECOVERY.md). Para material externo permanente nuevo, raíz aprobada `C:\TDL_DATA`; los históricos retenidos no reciben nuevo trabajo. HOLDOUT tiene su propio límite protegido y queda excluido de esta limpieza.

Las instantáneas PROJECT_CURRENT_STATE, project_baseline y PROJECT_SNAPSHOT describen su fecha; no se reescriben. Interoperabilidad adicional, SIRI y GTFS-RT no se declaran implementados por este mapa. No se absorben productos anidados ni se cambian baselines.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
