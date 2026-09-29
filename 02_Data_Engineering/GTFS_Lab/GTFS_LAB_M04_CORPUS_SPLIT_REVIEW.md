# GTFS Lab M04-A — Corpus split review

**Registro histórico:** Estado tras M04-A1 `M04A_PROVENANCE_PARTIALLY_RECOVERED` (detalle y límites en Q–W). **Estado vigente tras M04-A3:** `M04A_SPLIT_READY_FOR_HUMAN_REVIEW`; split `UNDER_REVIEW` sin aprobación en [`reports/GTFS_LAB_M04A3_SPLIT_DESIGN_REVIEW.md`](reports/GTFS_LAB_M04A3_SPLIT_DESIGN_REVIEW.md).
**Baseline de entrada A2 (histórica):** `b363079e5b8c8131f484917098d06b3a12a13eeb`
**Split al cierre A2 (histórico):** no propuesto entonces. **Split vigente A3:** [`corpus/split_v1.json`](corpus/split_v1.json), SHA `b30b1de464984b8c61f41e51279005cf3a32f9a11509e9996803c8f18be261e2`.
**Golden Corpus V1:** independiente e intacto.

> **Actualización M04-A2:** la matriz anterior de las secciones R–V conservaba `POSSIBLY_RELATED` para coincidencias de IDs. Esa clasificación queda reemplazada para la decisión de split por [la revisión M04-A2](reports/GTFS_LAB_M04A2_LINEAGE_EVIDENCE_REVIEW.md) y [`lineage_review_m04a2.json`](corpus/lineage_review_m04a2.json). M04-A2 concluyó `M04A_LINEAGE_MATRIX_READY_FOR_SPLIT_DESIGN`. **Actualización M04-A3:** la propuesta reproducible está registrada en [`corpus/split_v1.json`](corpus/split_v1.json); sigue `UNDER_REVIEW`, no abre holdout ni inicia M04-B.

> Las secciones de análisis originales que describen la ausencia de split y el bloqueo de A1/A2 son registros de su momento; M04-A3 los supersede para el estado actual.

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

## Q. Provenance recovery

La recuperación M04-A1 está registrada de forma reproducible en `corpus/provenance_v1.json`; el proceso es `gtfs_lab/corpus_provenance.py`. Leyó los 20 `source_metadata.json`, los 20 ZIP originales locales y las tablas GTFS disponibles. Los hashes SHA-256 de todos los ZIP coinciden con el hash declarado en metadata. El ZIP no se copia ni modifica. Los archivos originales son excluidos de Git; el proceso recibe `--corpus-root` local y no persiste rutas absolutas.

Por dataset se conserva familia de benchmark, operador declarado, agencia, `feed_info`, fechas de feed, plataforma, IDs/URL de origen, hash y fuentes de evidencia. Los timestamps `YYYYMMDD_HHMMSS` en los nombres se registran como `filename_timestamp_candidate`; `timestamp_semantics=UNKNOWN` y `capture_date=UNKNOWN` mientras no haya prueba local que les asigne significado. Las fechas de `feed_info` son fechas de vigencia del feed, no fechas de captura.

Los metadatos dejan `source_dataset_id`, `source_url`, `capture_date`, `download_date` y `nap_last_update` nulos o vacíos en los 20 casos. Revisé los 20 snapshots PNG preservados: muestran la página NAP del operador, fechas visibles de actualización y rangos de servicio, pero no un ID/URL de recurso recuperable en la vista capturada. Por tanto: `NAP_SOURCE_ID_NOT_RECOVERED_LOCALLY`. Las fechas/rangos transcritos figuran por separado en `provenance_v1.json`; no se tratan como captura del ZIP. Los cuatro snapshots 016–019 se resumen en S.

`agency.txt` apoya identidad operacional, no lineage por sí solo. `feed_info` falta en parte de los ZIP y sus campos vacíos se conservan como `UNKNOWN`. Los feeds 016–019 muestran publishers, URLs, versiones y rangos distintos o no declarados, lo que no prueba independencia de su estructura compartida.

La vista `normalization` separa `raw_value`, `normalized_display_value` y método de visualización. El fallback CP1252 solo se usa al decodificar tablas GTFS para comparar texto; los bytes fuente no se reescriben. La reparación reversible de mojibake de los nombres del manifest tampoco sustituye los valores originales.

## R. Relationship analysis

`corpus/relationships_v1.json` reproduce los 28 pares de `inventory_v1.json` con IDs compartidos y agrega el sexto par prioritario 016–017, que no tenía coincidencias estructurales. Registra IDs y nombres compartidos de agencia/ruta/parada, IDs de viajes, solapamientos de rutas/paradas/viajes, ambos `feed_info`, relación temporal, clasificación, confianza, razón y la decisión de independencia. Se incluyen explícitamente las seis combinaciones 016–019.

No se calcula la independencia con thresholds numéricos. Los ZIP exactos duplicados podrían clasificarse `SAME_SOURCE_LINEAGE`; no hay ninguno. Los pares con solo solapamientos estructurales se mantienen `POSSIBLY_RELATED`/`LOW`; no hay base para `INDEPENDENT` o `LIKELY_INDEPENDENT`. Los casos sin señal decisiva continúan `UNRESOLVED`. Los valores de solapamiento son descriptores, no reglas automáticas.

La matriz resultante no autoriza lados opuestos: `NO` solo para lineage exacta, `UNRESOLVED` para relaciones posibles o no resueltas. Ningún par recibe `YES`. Estos datos apoyan revisión de unidad de split, no una asignación.

## S. 016–019 deep review

Comparación directa de bytes/tablas de entrada; no se consultaron findings ni resultados del validator. No hay IDs de agencia compartidos ni IDs de viajes compartidos entre las seis combinaciones. Los nombres de rutas y paradas tampoco coinciden como cadenas, aunque varios feeds comparten IDs de paradas.

| Par | Agency IDs | Route IDs | Stop IDs | Feed/identidad observada | Clasificación |
| --- | ---: | ---: | ---: | --- | --- |
| 016–017 | 0 | 0 | 0 | La Unión vs Tuvisa; publishers y URLs diferentes. Sin feed dates/version en 016; 017 `20260920–20261021`, v1.0. | UNRESOLVED |
| 016–018 | 0 | 0 | 84 | La Unión vs Bilbobus; publishers/URLs distintos. 016 sin fechas/version; 018 `20260901–20270630`, version `1789938057086`. | POSSIBLY_RELATED |
| 016–019 | 0 | 0 | 72 | La Unión vs publisher Lantik; URLs distintas. 019 `20260907–20261107`, version `20260908`. | POSSIBLY_RELATED |
| 017–018 | 0 | 6 | 15 | Tuvisa vs Bilbobus; publishers/URLs/versiones y rangos distintos. | POSSIBLY_RELATED |
| 017–019 | 0 | 0 | 262 | Tuvisa vs Lantik; publishers/URLs/versiones y rangos distintos. | POSSIBLY_RELATED |
| 018–019 | 0 | 0 | 336 | Bilbobus vs Lantik; publishers/URLs/versiones y rangos distintos. | POSSIBLY_RELATED |

Agency identity: `launion` / Autobuses La Unión, S.A.; `320` / Tuvisa; `Bilbobus` / Bilbobus; `200` / Bizkaibus. Los cuatro snapshots NAP muestran operadores y ámbitos diferenciados. Las imágenes muestran “Actualizado el 22/9/2026” para 016, 017 y 018, y “10/9/2026” para 019; rangos NAP 21/9/2026–21/9/2027, 20/9/2026–21/10/2026, 1/9/2026–30/6/2027 y 6/1/2017–23/12/2026, respectivamente. Estas fechas son evidencia visible del snapshot, no `capture_date` del ZIP. Evidencia: `20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/016_alu/01_nap_snapshot/La Union.png`, `017_tuvisa/01_nap_snapshot/TUVISA.png`, `018_bilbobus/01_nap_snapshot/Bilbobus.png`, `019_bizkaibus/01_nap_snapshot/bizkaibus.png`.

El solapamiento de 016 con 018/019 y de 017/018/019 en IDs de paradas no viene acompañado de identidad de agencia, nombre de parada idéntico, trips compartidos ni publisher común. Es insuficiente para inferir el origen del ID o separar los feeds en lados opuestos.

## T. Source lineage candidates

`source_lineage_candidates=[]`. No hay duplicados exactos ni evidencia local de un ID de fuente que permita agrupar feeds por lineage. Las familias A–D siguen siendo cohortes del benchmark, nunca lineage. Los grupos 016–019 quedan como relaciones potenciales por resolver, no como lineage asignada.

## U. Independence matrix

La matriz completa está embebida en `relationships_v1.json` mediante `independence_decision` y `can_be_opposite_split_sides`. Hay 28 pares del inventario y la comparación auxiliar 016–017: ningún `YES`, `NO` solo para SHA idéntico (cero pares), y el resto `UNRESOLVED`. El estado del conjunto es por tanto insuficiente para diseñar un split defendible.

## V. Remaining custodian questions

1. Para los 20 IDs de benchmark, ¿qué ID y URL de recurso NAP corresponden a cada ZIP, y qué registro local/fecha de descarga los relaciona? La búsqueda local encontró campos nulos en metadata y screenshots sin identificador de recurso visible.
2. Para los pares con IDs de paradas compartidos (en especial 016–019), ¿los IDs provienen de un registro común, de una red de transbordo o de reutilización independiente? ¿Debe mantenerse alguno agrupado por lineage/proveedor?
3. ¿Qué evidencia primaria documenta los timestamps de nombre de ZIP: descarga, publicación, captura u otra operación? Hasta responder, no son fechas semánticas.

No se pregunta por agency/feed fields ni por solapamientos: ya están extraídos del input local.

## W. Veredicto M04-A1 (histórico, supersedido por M04-A2)

**Estado a cierre de M04-A1:** `M04A_PROVENANCE_PARTIALLY_RECOVERED`. Se recuperó identidad de agencias, metadata `feed_info`, fechas de feed y análisis estructural para los 20 inputs; no se recuperaron los IDs/URLs NAP ni significado de timestamps, y quedaron relaciones de lineage sin resolver. La clasificación y preguntas de custodia de A1 son históricas; M04-A2 establece el estado vigente en la revisión enlazada al principio. No proponer split ni holdout; no iniciar M04-B/M05; Golden Corpus V1 sigue intacto; `TDL_TRUST_FOUNDATION != PASS`.

Gate reproducible: `python gtfs_lab/corpus_provenance.py --corpus-root <corpus-local> --provenance corpus/provenance_v1.json --relationships corpus/relationships_v1.json --check`. Rechaza cobertura incompleta, ausencia de fuentes, confianza/enum inválida, fecha de captura derivada únicamente del nombre, campos de validator, rutas absolutas, relaciones independientes sin razón y relaciones unresolved ocultas. Los tests negativos están en `tests/test_corpus_provenance.py`.
