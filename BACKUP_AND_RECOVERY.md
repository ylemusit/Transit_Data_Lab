# Backup y recuperación

Política revisada el 2026-10-07 tras la auditoría del entorno canónico. La raíz operativa es `P:\TransitDataLab`; los documentos de migración/reconciliación enlazados en `PROJECT_STATUS.md` conservan la historia de sus snapshots. Los paths de esta política son relativos a la raíz indicada, salvo cuando se especifica otra cosa.

## Estado actual

No hay backup físico externo integral acreditado ni restauración integral probada. Git remoto protege solo los blobs versionados de los repos correspondientes; no protege bases DuckDB, ZIP originales, artefactos excluidos, datos/evidencia no regenerables, material privado ni cambios sin commit de repos independientes. Un bundle en el mismo disco tampoco cubre fallo del disco.

La prueba controlada de octubre valida una ejecución sintética, no la recuperación ante pérdida. No se afirma capacidad de recuperación hasta restaurar desde un destino físico separado y verificar hashes/manifests.

## Contrato mínimo de backup

| Grupo | Autoridad actual | Tratamiento de backup |
|---|---|---|
| Checkout TDL | `01_Project/Transit Data Lab`, Git `main` y remoto | Preservar commit/tag y restauración en workspace nuevo; incluir cambios nuevos revisados en Git según el flujo autorizado. |
| Repositorios GTFS Explorer | `01_Project/Transit Data Lab/06_Products/GTFS Explorer/{GTFS Explorer Artifacts,GTFS Explorer Desktop,GTFS Explorer Engineering}` | Respaldar cada repo de forma independiente, incluidos historial y cambios locales sin commit; no asumir cobertura desde Git padre. |
| DB GTFS | `02_Data/External/Databases/GTFS` (DuckDB actual; SHA observado `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`) | Copia consistente con DB cerrada o procedimiento DuckDB compatible; verificar SHA tras restaurar. |
| DB Compliance | `02_Data/External/Databases/Compliance` (DuckDB actual; SHA observado `4db39fa5494c525f339f68bf0b96087b5ff2e1e0cb830eea882336174bc8048b`) | Igual que GTFS; preservar baseline actual y metadata. |
| Development / TestBank / Holdout / External | Bajo `02_Data`, según manifests/contratos | Preservar ZIP exactos y fuentes no regenerables; aplicar acceso restringido. No leer ni hashear HOLDOUT para crear el backup. |
| Evidencia histórica y aceptada | `03_Evidence`, incluidos assets canonizados bajo `Historical/CanonicalAssets` | Respaldar bytes y manifests como evidencia; no regenerar ni reescribir para que coincidan con el estado actual. |
| Cliente aceptado | `05_Client`; EXE aceptado SHA-256 `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266` | Mantener copia separada e identidad/hash. No implica release pública. |
| Material privado de firma | `Private/Signing` | Destino cifrado/restringido separado, ACL comprobada; nunca copiar a remoto público ni manifiesto público. No abrir PFX para esta política. |
| Runtime y outputs regenerables | `04_Runtime` | No respaldar por defecto; conservar recetas, versiones y outputs cuya retención/evidencia esté aprobada. |

## Procedimiento para declarar restauración probada

1. Acordar destino físico fuera de P: con capacidad, cifrado/ACL y retención definidos.
2. Inventariar el snapshot y las identidades esperadas desde manifests existentes; no seguir junctions accidentalmente ni introducir contenido HOLDOUT en logs.
3. Capturar consistentemente DBs cerradas y respaldar fuentes/evidencia necesarias junto con repos independientes y sus cambios no confirmados.
4. Restaurar en un workspace separado; verificar commit/tag, hashes dirigidos, manifests y apertura de DBs en solo lectura.
5. Ejecutar gates mínimos de reconstrucción y registrar fecha, destino, versiones, diferencias y responsable. No promover ni publicar datos restaurados automáticamente.

## No regenerable y decisiones pendientes

ZIP de fuentes exactos, bases autoritativas, capturas/fuentes únicas, evidencia excluida de Git, outputs aceptados y cambios sin commit pueden ser irremplazables. Un feed descargado de nuevo no sustituye la versión histórica. Distinguir outputs regenerables de evidencia antes de excluirlos.

No se creó backup en esta auditoría. G-01 de [análisis de gaps](reports/PROJECT_GAP_ANALYSIS_V1.md) sigue siendo requisito antes de un piloto externo. Los registros de migración permanecen históricos y se conservan íntegros; la ruta actual del repositorio de restore de prueba es `03_Evidence/Historical/CanonicalAssets/06_Products/GTFS Explorer/GTFS Explorer Backups/restore_test_v0.2.2_20260924T161533Z_02`. Su remote local aún referencia un bundle C: ausente; el bundle P: asociado se verificó, pero no se reconfiguró ni se considera backup integral.

El acceso externo a datos/clientes requiere autorización explícita por separado. Mantener el cliente interno como herramienta operacional; ningún backup, gate técnico ni prueba sintética constituye aprobación comercial o jurídica.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

Los expedientes completos excluidos por la publicación sanitizada de 2026-10-10 deben incluirse en el backup separado de P:. La copia preintegración conserva los originales de los documentos sanitizados; el repositorio público contiene método y ejemplos sintéticos, no esos expedientes.
