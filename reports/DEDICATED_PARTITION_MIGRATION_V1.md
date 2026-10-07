# Dedicated Partition Migration V1

Fecha: 2026-10-07. **DEDICATED_PARTITION_MIGRATION_V1 = CLOSED_WITH_TEMPORARY_COMPATIBILITY_LINKS**. **FINAL_C_DRIVE_TDL_STATE = CLEAN**, para las raíces TDL inventariadas y las ubicaciones de almacenamiento auditadas.

## Raíces canónicas y contratos

| Área | Raíz física |
| --- | --- |
| Fuente y cuatro repositorios independientes | `P:\TransitDataLab\01_Project\Transit Data Lab` |
| Development, TestBank, Holdout, External y bases autoritativas | `P:\TransitDataLab\02_Data` |
| Evidencia física Accepted/Historical/Manual y checkpoints | `P:\TransitDataLab\03_Evidence` |
| Entornos reconstruidos, cachés, temporales y outputs nuevos | `P:\TransitDataLab\04_Runtime` |
| RC interno aceptado, paquetes e identidades históricas | `P:\TransitDataLab\05_Client` |
| Firma restringida | `P:\TransitDataLab\Private\Signing` |

`config/tdl_paths.json` centraliza las seis variables TDL. `tools/activate_tdl.ps1` activa las rutas solo para el proceso; permite `-Root` o `TDL_ROOT`. Test Bank usa `TDL_DATA_ROOT/TestBank` y conserva `--bank`. Las bases recuperadas desde el checkout histórico coinciden con los hashes aprobados; se conservan en `02_Data/External/Databases` y abren read-only. Los cuatro worktrees protegidos registrados se repararon a P:, conservando HEAD/branches; los repositorios de producto siguen independientes y sus cambios locales previos están preservados.

## Clasificación y retirada verificadas

La resolución se hizo por archivo/unidad, conservando la descomposición original y registrando overrides de layout/duplicidad. **REVIEW_REQUIRED_BYTES_FINAL = 0**; cuarentena y ambigüedades protegidas fuera de P: cero. No se borraron padres mixtos por nombre.

| Operación de esta resolución | Archivos | Bytes lógicos |
| --- | ---: | ---: |
| DELETE_REGENERABLE | 244.584 | 227.943.369.017 |
| Copias de C: verificadas por SHA-256 antes de retirar el origen | 87.175 | 108.239.546.474 |
| DELETE_DUPLICATE en P:, con identidad retenida y mapa de recuperación | 3.426 | 12.503.583.020 |

Las dos primeras cifras son operaciones distintas; los duplicados de P: estaban incluidos en la transferencia y no se cuentan nuevamente como regenerables. La pasada previa de reparación ya había retirado 489 archivos / 635.338.932 bytes; no están incluidos en esta tabla. PFX y copia portable de DuckDB se contabilizan separadamente de las raíces del plan.

Se retiraron **11 raíces C:**, incluidos el checkout canónico, `C:\TDL`, `C:\TDL_DATA`, `C:\t14`, `C:\t14-evidence`, `C:\t11v`, `C:\t-m03a`, los tres checkouts protegidos del directorio de proyectos y el worktree m04b2 de Temp. Directorios regenerables retirados en esta resolución: **130.099**; directorios de origen retirados en total: **155.979**. No quedan enlaces de compatibilidad en C:.

El checkpoint pre-0.2.2 conserva el snapshot completo, incluidos directorios vacíos: **22.868 archivos coinciden con su manifiesto congelado**. No se redujo su runtime ni se reescribieron manifests históricos. En los paquetes históricos se eliminaron únicamente archivos de identidad SHA-256 duplicada; `05_Client/ARTIFACT_LOCATIONS.json` permite recuperar cada ruta omitida desde el archivo retenido. Los paquetes operacionales actuales siguen completos. Clasificación de 70 unidades de paquete: 2 ACCEPTED_CURRENT (cliente interno y release Desktop 0.2.2), 1 ACCEPTED_HISTORICAL (P1-32, requerido por el contrato de upgrade vigente) y 67 SUPERSEDED. Se conservan las identidades únicas requeridas por el ledger de recuperación; las copias idénticas se omiten. Las extracciones temporales idénticas son REGENERABLE. 166 manifests/checksums de Git se copian al cliente porque forman parte de la recuperación/entrega, sin duplicar informes versionados. Las capturas, scripts de diagnóstico y binarios únicos que apoyan evidencia de defectos siguen en Historical como FAILED_EVIDENCE cuando corresponda; no se ha inferido aceptación por el nombre de una carpeta.

HOLDOUT mantiene contenido: solo transferencia/verificación criptográfica, sin inspección GTFS ni nueva evaluación. Los seis originales físicos están en `02_Data/Holdout`, con el contrato relativo original resuelto mediante junctions. Test Bank conserva casos, SOURCE, registros y manifiestos sellados byte a byte; no se reconstruyó el registro real ni se repitieron auditorías reales.

## Junctions: todas dentro de P:

34 junctions verificadas; ningún target está en C:. El registro local contiene OLD_PATH, TARGET, REASON, DEPENDENCY y REMOVAL_CONDITION para cada una.

| Contrato | Cantidad | Condición de retirada |
| --- | ---: | --- |
| Fuentes corpus DEVELOPMENT, HOLDOUT y schema NeTEx | 21 | Resolver recursos externos en una nueva versión del contrato, preservando manifests congelados. |
| `GTFS_Lab/feeds` y runs históricos | 2 | Actualizar consumidores y referencias relativas de evidencia. |
| Fixtures y ejemplo generado de Desktop | 2 | Configurar explícitamente el directorio de assets externos en los tests/ejemplo. |
| Bases GTFS y Compliance | 2 | Sustituir defaults relativos de los consumidores por configuración externa. |
| `.venv`, basetemp, scratch y recursos npm de Desktop | 5 | Adaptar las recetas a `TDL_RUNTIME_ROOT` directamente. |
| Configuración privada del editor | 2 | Integración nativa del editor con configuración externa. |

Los manifests/reportes históricos conservan rutas antiguas como procedencia. No son dependencias ejecutables nuevas. El inventario no sigue ni cuenta reparse points.

## Verificación operacional

- Repositorio canónico abre en P:, `main == origin/main` antes de la rama de publicación; `git fsck --no-dangling` PASS en siete repositorios. Cuatro worktrees registrados apuntan a P:.
- 50 tests focales PASS: almacenamiento 3, banco 18, NeTEx 10 y Desktop 19. Lint PASS; typecheck Desktop PASS, 142 archivos.
- E2E sintético del Test Bank PASS (dos casos); gate Compliance V1 portátil PASS, con hashes DB inicial/final idénticos. Única adaptación del gate: CRLF/LF del JSON de metadata en memoria, manteniendo estrictos los bytes y hashes de fixtures.
- Recursos web reconstruidos desde package-lock: cuatro assets byte-idénticos. Desktop usa Python nuevo en P:, sin transportar virtualenvs. El spike WebEngine mostró intermitencia también en C:; el gate final pasa con flags de renderer sin throttling para ejecución offscreen, sin modificar código del producto.
- 51 links de documentación actual y 20 referencias de corpus resuelven. Snapshot XSD capturado: 458 dependencias coinciden con el manifest fijado; se comprueban sus bytes canónicos, sin exigir `.git` al snapshot. Ningún HOLDOUT fue usado por estos gates.
- EXE operacional único: SHA-256 **3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266**. Se valida identidad, no una nueva aceptación humana o clean-machine.
- Private/Signing y PFX mantienen ACL restringida a Yeison/SYSTEM/Administradores; no hay material de firma en Git. La configuración privada nueva hereda únicamente esos principales.

La publicación de este cierre se realiza mediante PR; CI se verifica sobre el SHA efectivo de main y se registra en el expediente local de publicación. No se publica una release ni se elevan los gates comerciales/jurídicos.

## Huella y capacidad

Snapshot local `2026-10-07T05:34:52.456686+00:00`: **98,363 archivos**, **23,579 directorios**, **97,777,191,020 bytes lógicos / 91.062105279 GiB**. Se recalcula después de cleanup sin doble conteo por junctions. La actividad Git/CI y sus registros posteriores pueden cambiar la medición; el inventario final entregado usa un snapshot posterior a la publicación.

| Área | Archivos | Directorios | GiB lógicos |
| --- | ---: | ---: | ---: |
| 01_Project | 13,084 | 1,781 | 0.515392 |
| 02_Data | 22,842 | 1,638 | 48.734438 |
| 03_Evidence | 44,130 | 17,369 | 32.165223 |
| 04_Runtime | 14,469 | 1,507 | 1.031882 |
| 05_Client | 3,740 | 1,246 | 8.550159 |
| 06_Knowledge | 0 | 1 | 0.000000 |
| 07_Tools | 1 | 2 | 0.034531 |
| Private | 97 | 33 | 0.030481 |
| 99_Quarantine | 0 | 1 | 0.000000 |

Espacio libre comprobado tras cutover: **208.586 GiB**; cubre 10 GiB de reconstrucción y 30 GiB de reserva. El runtime nuevo está incluido en la huella física de P:. Los números son longitudes lógicas, no una certificación de espacio asignado.

## Pendiente independiente y límites

`npm audit` identifica una vulnerabilidad crítica en MapLibre GL 6.3.0, confirmada por el [advisory oficial GHSA-jrc7-96c5-q579](https://github.com/maplibre/maplibre-gl-js/security/advisories/GHSA-jrc7-96c5-q579). Afecta versiones hasta 6.4.0; la corrección se publica desde 6.4.1. La migración preserva la baseline 0.2.2; evaluar alcance y actualización del producto requiere una tarea separada. No se declara certificación de seguridad.

El audit de C: cubre raíces del inventario, registros worktree y candidatos por nombre en C:, proyectos, Temp, workspace/tmp/temp, Documentos y Descargas. Aplicaciones compartidas, cachés generales, historial Codex y material ajeno no son raíces TDL y no se retiraron. Los inventarios por archivo, hashes privados, originales de documentos locales y logs permanecen locales en `03_Evidence/Historical/migration_v1`; no se versionan.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
