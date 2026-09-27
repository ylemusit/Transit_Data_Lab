# Piloto de 20 operadores — guía vigente

El piloto pertenece a GTFS_Lab dentro del proyecto global Transit Data Lab. `20_clientes_reales` identifica 20 datasets de investigación; no acredita clientes comerciales. La baseline protegida del producto GTFS Explorer Desktop sigue en 0.2.2, con repositorio independiente.

## Procedencia y estado

El [README inicial](README.md) forma parte de la evidencia con hash registrada en Business V1. Conserva errores históricos de codificación, un carácter NUL en la ruta 05_working_copy y la descripción inicial de repositorio privado. No se reescribe para evitar invalidar esa evidencia. El repositorio Git padre actual es público según la consulta de esta revisión; esa frase histórica no constituye una garantía de privacidad.

Las versiones 0.2.1, RC-002 y candidate001 de runs anteriores se conservan como procedencia. No sustituirlas por 0.2.2 ni presentar un resultado anterior como validación vigente del producto. Las guías iniciales que dicen NOT_STARTED o «ejecución posterior» describen la preparación histórica, no la ausencia de resultados ya conservados.

| Documento | Uso |
| --- | --- |
| [benchmark_manifest.csv](benchmark_manifest.csv) | Inventario histórico de 20 datasets; metadatos preservados. |
| [OPERATOR_CATALOG.md](docs/OPERATOR_CATALOG.md) | Vista legible, con columnas alineadas con el manifest. |
| [DATA_GOVERNANCE.md](docs/DATA_GOVERNANCE.md) | Inmutabilidad de originales y separación de copias. |
| [PILOT_01.md](docs/PILOT_01.md) | Alcance y etapas históricas del piloto. |
| [final_report.md](04_audit/pilot_01/final_report.md) | Resultados de la auditoría piloto conservada. |
| [README Bizkaibus](FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/README.md) | Clasificación de RC-002 y candidato posterior. |

Se han reparado caracteres de control, acentos y placeholders en documentación no integrante del baseline Business, usando sus metadatos existentes. La tabla inicial omitía una celda y desplazaba SIRI y las columnas posteriores; ahora deriva sus indicadores del manifest, sin volver a inspeccionar feeds. Los nombres y hechos registrados en manifests, metadata y runs no se han modificado.

No se han ejecutado nuevos runs ni validado derechos de reutilización/publicación de datasets. Bases, ZIP originales y grandes generados permanecen fuera del Git padre según su política de exclusión; su recuperación requiere backup independiente.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
