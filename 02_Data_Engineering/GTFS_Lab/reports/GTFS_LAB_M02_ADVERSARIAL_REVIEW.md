# GTFS_Lab Trust Foundation M02 — revisión adversarial

Fecha: 2026-09-29. Revisión del branch `feat/tdl-trust-foundation-m02` frente a `origin/main` en `0134408021c335007cfde88137ca2fb599c72ee5`. No se inicia M03 ni se hace merge.

## A. Atomicidad de auditoría

Orden observado en `pipeline.run()`:

1. extrae y valida el ZIP; construye Compliance, validación, análisis, GIS y DuckDB;
2. escribe `run.json`, `analysis.json`, `validation.json` y `report.md`, en ese orden;
3. crea `audit/`, verifica el SHA-256 de entrada, normaliza y reconcilia findings;
4. escribe `findings.normalized.json`;
5. si integridad o duplicados no son aceptables, no crea manifest y `run()` termina con excepción;
6. si son aceptables, construye y valida `audit_manifest.json`, comprueba que todas las rutas declaradas existen, escribe el manifest en un temporal del mismo directorio, lo vuelve a validar desde disco y lo mueve con `os.replace`.

El manifest se compromete después de validar sus campos y la existencia de los artefactos declarados. `os.replace` evita que un fallo durante la escritura publique un archivo final parcial. Se inyectó un fallo en el reemplazo: no hubo `audit_manifest.json`, el temporal se limpió y quedaron únicamente los otros outputs y `findings.normalized.json`.

Si fallan normalización o deduplicación por excepción, quedan los outputs V1 y puede quedar `audit/` vacío. Un conflicto produce `findings.normalized.json` con `REJECTED_CONFLICTING_DUPLICATES`; si falla validación del manifest, integridad o su escritura, puede quedar `findings.normalized.json` aceptado, pero sin manifest. Este último caso se clasifica `EXPECTED_INCOMPLETE_AUDIT_ARTIFACT`: la presencia de findings normalizados no acepta la auditoría. El manifest solo aparece tras el reemplazo final.

## B. Fail-closed

Se inyectaron dos representaciones del mismo finding en un pipeline sintético completo: dos ocurrencias, un finding único y un conflicto. `run()` lanzó `RuntimeError` (`Trust audit persistence was not accepted`); no devolvió resultado; `run.json` conserva el resumen V1 (PASS porque el fixture GTFS era válido), los demás outputs V1 permanecen, `findings.normalized.json` marca `REJECTED_CONFLICTING_DUPLICATES` y no existe `audit_manifest.json`.

También se forzó una discrepancia de SHA-256: `run()` lanzó la misma clase de error, el normalizado quedó `REJECTED_INPUT_INTEGRITY` y no hubo manifest. El resumen PASS de `run.json` es solo el resultado V1 previo a persistencia, no una aceptación de Trust. **Un run fallido de Trust no puede presentarse como auditoría aceptada:** no existe manifest válido y el llamador recibe excepción.

## C. Artefactos

| Entrada del manifest | Clasificación | Procedencia y mutabilidad |
| --- | --- | --- |
| `run` (`../run.json`) | `RUN_OWNED_ARTIFACT` | Emitido por el pipeline en la carpeta única del run; incluye el resultado V1. |
| `validation` (`../validation.json`) | `RUN_OWNED_ARTIFACT` | Resultado de validación del run. |
| `analysis` (`../analysis.json`) | `RUN_OWNED_ARTIFACT` | Análisis del run. |
| `report` (`../report.md`) | `RUN_DERIVED_ARTIFACT` | Informe renderizado de sus outputs. |
| `findings_normalized` | `RUN_DERIVED_ARTIFACT` | Producido por la reconciliación M02. |
| `gis_export_*` | `RUN_OWNED_ARTIFACT` | Exportaciones GIS bajo el `work_dir` del run. |
| `database` (`../dataset.duckdb`), si existe | `RUN_OWNED_ARTIFACT` | `build_duckdb()` lo crea en `ctx.work_dir/dataset.duckdb`; cada run obtiene carpeta y base propias. No es `databases/gtfs_lab.duckdb` ni otro activo compartido. |

Un run posterior no reusa estas rutas porque su `run_id` crea un directorio distinto. Los archivos siguen siendo editables manualmente y el manifest guarda rutas, no hashes de outputs. No se encontró `SHARED_REFERENCE` ni `EXTERNAL_PROTECTED_ASSET` entre las entradas declaradas. El contrato M01 1.1.2 no expresa tipo/propiedad ni digest por artefacto; no se amplió el contrato: `CONTRACT_MODEL_LIMITATION` para futuras necesidades de procedencia más fuerte.

## D. Ruleset identity

`ruleset_id` es el literal `gtfs-lab-v1`. `ruleset_version` es la lista ordenada de versiones únicas de las entradas de `validation.rules`, concatenada con comas. `executed_rule_ids` es la lista ordenada de `rule_id` no vacíos de esas entradas; `executed_rule_versions` es el mapa ID→versión. Los scopes son la lista ordenada de scopes declarados.

El orden de entrada no afecta a las listas ni a la versión; por tanto, el mismo conjunto de IDs/versions produce esos mismos campos. Los IDs incluyen la regla Compliance adjunta porque forma parte de `validation.rules`. También incluyen reglas con `NOT_EVALUABLE` o `INSPECTION_ERROR` si esas entradas tienen `rule_id`; el código no filtra por estado. En consecuencia, “executed” describe los resultados de regla enumerados por el pipeline, no prueba que cada predicado pudiera ejecutarse o completarse. `ruleset_id` no es un hash del conjunto de reglas. No se introduce una semántica distinta en esta revisión.

## E. Regresión de outputs V1

Se generó `ORPHAN_TRIP.zip` en el checkout base y se reutilizaron los mismos bytes en ejecuciones separadas de base `0134408021c335007cfde88137ca2fb599c72ee5` y M02. SHA-256 del ZIP: `26baf9a07d4b6e3b2155bfaa4e82bb7a6bf45550218fc2f711e8cbc425ed0af8`. Se compararon JSON parseados de forma canónica y texto tras sustituir run IDs, timestamps y rutas locales; también se compararon hashes de bytes sin normalizar.

`validation.json`, `analysis.json`, `stops.geojson`, `stops.kml`, `routes.geojson` y KML de rutas fueron idénticos byte a byte. `run.json` y `report.md` difieren en IDs, timestamps y rutas absolutas esperadas; ambos son iguales semánticamente tras normalizarlas. No hay diferencias semánticas introducidas por M02: `M02_V1_SEMANTIC_REGRESSION = NO` para este fixture representativo.

## F. Input integrity

`INPUT_INTEGRITY_VERIFIED` significa únicamente que el SHA-256 asociado a la identidad del dataset coincide con el SHA-256 comprobado al terminar el pipeline y antes de aceptar el manifest. No prueba archivo permanente, WORM, custodia externa, retención ni que el archivo no cambiase y volviese a su contenido entre observaciones.

## G. Reconciliación

Gate reproducido: `source_finding_occurrences=2`, `normalized_unique_findings=1`, `identical_duplicates_collapsed=1`, `conflicting_duplicates=0`. La relación observada es `ocurrencias fuente = únicos + ocurrencias idénticas colapsadas + ocurrencias conflictivas`. “Colapsados” cuenta ocurrencias redundantes adicionales, no grupos ni IDs. Para duplicados conflictivos el contador representa ocurrencias conflictivas adicionales respecto a la primera representación retenida, no grupos de IDs.

## H. Ingestion error

`MALFORMED_CSV → INGESTION_ERROR`: el directorio contiene `run.json` y `report.md`; no existe directorio `audit/`, `findings.normalized.json` ni `audit_manifest.json`. No queda contenido parcial que pueda confundirse con auditoría aceptada.

## I. Defectos y cambios

Se encontraron y corrigieron dos defectos materiales de M02:

- `persist_audit()` podía devolver `NOT_ACCEPTED` sin que `pipeline.run()` lo propagase; ahora el caller recibe excepción.
- Una escritura directa podía dejar un manifest parcial; ahora se valida un temporal completo y se publica mediante reemplazo atómico. La validación desde disco precede al reemplazo.
- El payload de findings se podía marcar `ACCEPTED` con hash de fuente discrepante; ahora se marca `REJECTED_INPUT_INTEGRITY`.

Los outputs V1 ya generados se conservan ante errores Trust para diagnóstico. No se modificó `audit_contract.py` ni el contrato M01. `CONTRACT_MODEL_LIMITATION` sobre metadatos/hash por artefacto queda como limitación futura, no como bloqueo del contrato actual.

## J. Gates finales

- Trust Contract M01: PASS, 12/12.
- Trust Persistence M02: PASS, 16/16; reconciliación 2/1/1/0.
- GTFS_Lab V1: PASS.
- Compliance V1: PASS; 386 comprobaciones Phase 2 actuales PASS. Se informa aparte un control histórico `UNCHANGED_COUNT_audit.rules` (2 frente a 0), excluido del resultado vigente.
- `py_compile`: PASS.
- `git diff --check`: PASS.
- Pruebas adversariales nuevas: conflicto, mismatch de SHA-256 y fallo inyectado de reemplazo del manifest; comportamiento fail-closed confirmado.

## K. Estado Git

El branch partía de `cab3eee97db65ed16bb91c468ba17732a30d4449`, dos commits por delante de `origin/main` en `0134408021c335007cfde88137ca2fb599c72ee5`. SHA final y estadísticas se completan al preparar el Draft PR.

## L. Draft PR

Título: `feat(gtfs-lab): persist Trust Foundation audit evidence M02`

Body propuesto:

### Purpose

Persistir AuditManifest 1.1.2 y findings normalizados de forma aditiva.

### Scope

- Persistencia de auditoría, findings normalizados, reconciliación y gate de persistencia.
- Propagación de fallos Trust al caller.
- Escritura atómica del manifest con validación del temporal y existencia de artefactos.
- Documentación e informe adversarial M02.

### Compatibility

Outputs V1 (`run.json`, `validation.json`, `analysis.json`, `report.md`, GIS y DuckDB) permanecen contractualmente disponibles. En fallo Trust se conservan como evidencia V1.

### Ingestion errors

No generan AuditManifest aceptado ni directorio `audit/`.

### Preservation

`INPUT_INTEGRITY_VERIFIED` solo compara el SHA-256 de la identidad del dataset con el verificado al finalizar el pipeline. No implica archivado, WORM, custodia ni retención.

### Gates

- Trust Contract M01: PASS 12/12.
- Trust Persistence M02: PASS 16/16.
- Compliance V1: PASS; se conserva anotado el control histórico no bloqueante `UNCHANGED_COUNT_audit.rules`.
- GTFS_Lab V1: PASS.
- `py_compile` y `git diff --check`: PASS.

### Known limitations

- No se demuestra preservación archivística.
- Cross-platform Linux y golden corpus no se validaron.
- No se validaron conjuntos development/holdout.
- La prueba V1 comparativa usa un fixture representativo, no un corpus amplio.
- M01 1.1.2 no tipa propiedad ni digest de artefactos.
- No se declara `TDL_TRUST_FOUNDATION = PASS`.

Draft PR hacia `main`; no merge.

## M. Veredicto

`M02_DRAFT_PR_READY_FOR_DEEP_REVIEW`
