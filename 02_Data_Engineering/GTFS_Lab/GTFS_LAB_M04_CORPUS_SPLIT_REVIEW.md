# GTFS Lab M04-A — Corpus split review

**Estado:** `M04A_BLOCKED_BY_CORPUS_PROVENANCE`
**Baseline:** `b363079e5b8c8131f484917098d06b3a12a13eeb`
**Split:** no propuesto; no existe `split_sha256` ni asignación `DEVELOPMENT` / `HOLDOUT`.
**Golden Corpus V1:** independiente e intacto.

## A. Por qué existe holdout

Un holdout reservado permite estimar si un motor generaliza a feeds que no se usaron para diseñar reglas, heurísticas o umbrales. La north star es que un feed de un operador desconocido produzca una auditoría reproducible y trazable sin cambios de código específicos para ese operador.

## B. Golden, development y holdout

- **Golden cases:** casos pequeños y conocidos que fijan invariantes y regresiones deterministas. Pueden ser visibles durante el desarrollo.
- **Development corpus:** feeds cuyos inputs y outputs pueden usarse para desarrollar, depurar y mejorar el motor.
- **Holdout corpus:** feeds asignados y congelados que no se usan para adaptar reglas. Solo se abren en checkpoints registrados.

El inventario de esta revisión es metadata-visible: inspecciona identidad declarada, bytes y estructura de entrada. No ejecuta reglas ni utiliza findings para asignar casos.

## C. Inventario del corpus

`corpus/inventory_v1.json` registra los 20 datasets de `20_clientes_reales/benchmark_manifest.csv`: siete de `FAMILY_A_SMALL_BASIC`, cinco de `FAMILY_B_SME_OPERATIONAL`, tres de `FAMILY_C_COMPLEX_REGIONAL` y cinco de `FAMILY_D_MATURE_BENCHMARK`.

El inventario conserva SHA-256 medido, tamaño ZIP, número de ficheros, tablas GTFS, rutas, paradas, viajes, modelo de calendario y presencia de shapes. Los campos no documentados aparecen como `UNKNOWN`. Los hashes medidos coinciden con los hashes declarados en los metadatos de los 20 ZIP.

Generación reproducible (solo lectura de los ZIP; salida en el worktree):

```powershell
python 02_Data_Engineering/GTFS_Lab/gtfs_lab/corpus_inventory.py `
  --corpus-root <ruta-local-a-20_clientes_reales> `
  --output 02_Data_Engineering/GTFS_Lab/corpus/inventory_v1.json
```

La ruta local de entrada puede apuntar a un directorio fuera del checkout porque los ZIP están excluidos de Git. No se persiste ninguna ruta absoluta en el inventario.

## D. Procedencia y lineages

Los 20 registros declaran NAP España como plataforma y ES como país. El nombre de operador está presente, pero `source_dataset_id`, `source_url` y `capture_date` son desconocidos en los metadatos. Los nombres de familia describen cohortes del benchmark; no prueban independencia de operador ni lineage.

## E. Duplicados y relaciones

- No se detectó ningún SHA-256 de ZIP duplicado entre los 20 casos.
- Se detectaron 28 pares con al menos un `agency_id`, `route_id` o `stop_id` compartido. Son señales estructurales, no prueba por sí solas de que los feeds compartan origen.
- Hay solapamientos destacados entre 016–019 en IDs de paradas y entre 017–018 en IDs de rutas/paradas. El inventario conserva los conteos por par para revisión.
- La fuente no documenta si esos IDs compartidos son identificadores de red reutilizados, feeds relacionados o coincidencias. No se fuerza su interpretación.

## F. Unidad de split

No se ha elegido una unidad final. `DATASET` sería demasiado fino si dos ZIP pertenecen a una misma lineage. `FAMILY` tampoco está justificada: las familias parecen estratos de benchmark y no linajes de fuente. `OPERATOR` y `SOURCE_LINEAGE` requieren aclarar los cruces observados y completar provenance.

## G. Split propuesto

Ninguno. No asignar ahora grupos ni usar un 80/20 aleatorio. La tabla de asignaciones queda pendiente de evidencia de procedencia suficiente y decisión humana.

## H. Riesgos de leakage

Separar feeds con relaciones 016–019 podría filtrar IDs y estructura entre lados. Los nombres distintos no bastan para declarar independencia. Las categorías de familia no deben utilizarse como sustituto de provenance. No se ha consultado el número de findings por feed para estratificar.

## I. Política de acceso al holdout

Una futura apertura se limita a milestone validation, release candidate, Trust checkpoint o investigación de un fallo registrada previamente. El registro debe incluir `access_id`, timestamp UTC, motivo, versiones del motor y ruleset, identidades de datasets, resumen de resultado y decisión. Antes de aprobar la asignación, solo se permite verificar existencia, parseabilidad del archivo y hash; no se consumen resultados para desarrollar.

## J. Gestión de fallos

Registrar primero el resultado del checkpoint y clasificar el defecto. Reproducir el problema en un caso separado de development, corregir con ese caso y reservar el holdout original. No reabrirlo repetidamente ni reclasificarlo como development. Una promoción a Golden requiere reproducción mínima, revisión de autoridad y aprobación independiente.

## K. Versionado y expansión

El contrato futuro será `CorpusSplit 1.0.0`, con `split_id`, versión, timestamp UTC, método, base de selección y entradas con `dataset_id`, `source_sha256`, `family_or_lineage`, assignment y justificación. Su SHA se calculará determinísticamente sobre identidades, hash, lineage y assignment; excluirá timestamps, paths absolutos, findings y run IDs.

Tras la aprobación, mover una entrada requerirá nueva versión y razón (`PROVENANCE_CORRECTION`, `DUPLICATE_DISCOVERED`, `LINEAGE_CORRECTION`, `DATASET_RETIRED` o `CORPUS_EXPANSION`). Los datasets 021+ no modificarán V1 automáticamente: se asignarán mediante una nueva versión del contrato.

## L. Limitaciones

Los resultados describen los ZIP locales inspeccionados, no la independencia comercial o jurídica de operadores. La calidad de metadatos existente incluye campos de provenance vacíos y texto con problemas de codificación; no se ha corregido la fuente. Los solapamientos de identificadores necesitan interpretación del custodio del corpus. Esta revisión no ejecutó validación GTFS ni usó resultados previos del motor.

## M. Decisión humana requerida

El custodio del corpus debe aclarar:

1. si cada `benchmark_id` representa una captura independiente y su fecha/fuente canónica;
2. por qué hay identificadores agency/route/stop compartidos, especialmente en los grupos citados;
3. si algún conjunto debe mantenerse agrupado por proveedor, feed derivado o linaje;
4. qué entradas, si las hay, pueden considerarse holdout después de resolver esas relaciones.

Hasta resolverlo, el gate de split no puede emitir `UNDER_REVIEW` para una asignación completa y M04-A queda bloqueado. No se ha abierto el holdout, ejecutado una evaluación comparativa ni iniciado M04-B.

## N. Gate del split

`gtfs_lab/corpus_split_gate.py` implementa `TDL_CORPUS_SPLIT_GATE`: contrato y versión, cobertura única del inventario, hashes medidos, asignaciones permitidas, separación de lineage y relaciones estructurales, identidad SHA determinista, ausencia de resultados/rutas absolutas, `UNDER_REVIEW` y revisión vacía. No se ejecuta contra un split real porque la propuesta está detenida; el corpus de entrada no se fuerza a un contrato artificial.

## O. Pruebas negativas de leakage

`tests/test_corpus_split_gate.py` usa únicamente fixtures sintéticos para comprobar rechazo de hash duplicado entre lados, lineage dividida, campos de resultados, dataset ausente, dataset duplicado y relación estructural separada. También comprueba aceptación de un fixture limpio `UNDER_REVIEW`. Resultado: 7/7 PASS.

## P. Regresión

En el worktree aislado: M01 12/12 PASS; M02 PASS; M03-A Contract PASS; Golden Corpus PASS con dos casos y el SHA esperado; Golden Evaluator PASS 11/11; Golden Regression PASS para los dos casos; GTFS_Lab V1 PASS; py_compile y `git diff --check` PASS. Compliance V1 se ejecutó en solo lectura desde el checkout local vigente porque su base protegida no está en Git; PASS con hash idéntico antes/después `4DB39FA5…BC8048B`. La salida de esa ejecución quedó en una carpeta temporal, fuera del repositorio.

No se declara un PASS del `TDL_CORPUS_SPLIT_GATE` para los 20 datasets, ni `TDL_TRUST_FOUNDATION = PASS`.
