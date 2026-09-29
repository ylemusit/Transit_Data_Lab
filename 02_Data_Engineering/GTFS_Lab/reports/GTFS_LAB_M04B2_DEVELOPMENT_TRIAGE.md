# GTFS_Lab M04-B2 — triage de desarrollo sintético

Fecha: 2026-09-29

Base y rama: `8d4f2ad7fa0545b76dd5d5ec5503890ed0c396d9` · `feat/tdl-trust-foundation-m04b2-triage`
Evidencia ejecutable: `reports/evidence/m04b2_development_triage_20260929/`

## A. Observaciones M04-B1 investigadas

El checkpoint V1 registró `008 → DATA_AMBIGUITY` tras detener la ingestión ante un registro CSV de cero campos en `shapes.txt`. También registró `013`, `015`, `017` y `018 → SCALE_LIMIT` en el evaluador Compliance V1. Este triage solo usa esas observaciones ya persistidas; no vuelve a derivar datos de los feeds.

## B. Declaración de no acceso a HOLDOUT

No se abrió, leyó, extrajo, ejecutó ni hasheó ningún ZIP HOLDOUT. Tampoco se inspeccionaron filas ni se tomaron decisiones de implementación a partir de ellas. La evaluación se limitó al código versionado, documentación y JSON de evidencia M04-B1 ya persistida, además de fixtures sintéticos nuevos. No se ejecutó HOLDOUT V2.

## C. Reproducción sintética de filas vacías

La reproducción directa con `csv.reader(..., strict=True)` obtuvo:

| Entrada | Registro emitido |
| --- | --- |
| Línea física vacía | `[]` |
| Línea con espacios | Una celda que contiene espacios |
| Línea `,,,` | Cuatro celdas vacías; fila no vacía y con estructura propia |
| CSV entrecomillado escapado válido | Una fila ordinaria con las comillas decodificadas |

El parser anterior rechazaba cualquier fila cuyo número de celdas no coincidiese con la cabecera, incluida `[]`. No había una regla documentada de normalización de líneas vacías. Una fila de comas no es una línea física vacía y sigue sujeta a validación estructural.

## D. Decisión de contrato del parser

Se adopta `IGNORE_PHYSICALLY_EMPTY_RECORD` solo para líneas del cuerpo que estén vacías o contengan exclusivamente espacios en blanco. La cabecera debe seguir siendo el primer registro y una fila entrecomillada con un valor de espacios no se ignora. El validador de ingestión emite `EMPTY_CSV_RECORD_IGNORED` con tabla, hasta las primeras 20 líneas físicas y el conteo total; es una observación de ingestión, no un finding de operador.

La referencia GTFS define records como valores de campos, exige los nombres de campo en la primera línea y recomienda no publicar filas vacías. RFC 4180 también describe cada record como campos delimitados. Una línea física sin contenido no representa una entidad GTFS; omitirla no cambia datos de tabla. La advertencia preserva evidencia de que se normalizó una entrada que la guía recomienda corregir. Una línea vacía antes de la cabecera, una celda entrecomillada con espacios y filas con delimitadores no se normalizan. Referencias consultadas: [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/) y [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180).

## E. Cambios del parser

`ingestion.py` ignora líneas vacías/solo espacios en el cuerpo, informa su conteo y posiciones, conserva los bytes de entrada y mantiene los errores de filas con dos o cinco columnas frente a una cabecera de cuatro. CSV entrecomillado válido permanece aceptado. El parser se identifica ahora como `gtfs-lab-csv/2`.

Se añadieron guardas de 4 MiB por registro lógico, 128 KiB por campo y 256 columnas. Se conservan los topes ZIP existentes de 512 MiB por miembro y 2 GiB descomprimidos en total. Los límites de registro no cambian los bytes archivados ni el hash del feed.

## F. Reproducción de escala Compliance

El motor de la base produjo `PASS` a 9.999 y 10.000 filas, `INSPECTION_ERROR: EMPTY_OR_ROW_LIMIT` a 10.001; `PASS` a 1 MiB−1 y 1 MiB; `INSPECTION_ERROR: SIZE_OR_NUL` a 1 MiB+1. La reproducción empleó únicamente datos sintéticos.

La implementación B2 pasa pruebas en 9.999, 10.000, 10.001, 25.000 y 100.000 filas; también en 1 MiB−1, 1 MiB, 1 MiB+1, y un caso combinado de 100.001 filas y 1.900.054 bytes de `stop_times.txt`. El fixture integrado de 100.001 filas produce cero findings y ningún resultado de tamaño se convierte en finding de operador.

## G. Causa de los límites anteriores

Los topes estaban como constantes (`MAX_BYTES = 1 MiB`, `MAX_ROWS = 10.000`). El código leía el archivo completo como bytes, convertía todas las filas en listas y después construía diccionarios, por lo que el coste de memoria crecía con el feed. El commit que incorporó el motor lo describió como inspector técnico acotado; no documentó por qué se eligieron esas cifras ni las definió como umbrales contractuales. La evidencia disponible indica guardas de recursos/prototipo deliberadas alrededor de una implementación en memoria. No son supuestos algorítmicos de la regla ni semántica de cumplimiento. La regla fija-stop puede verificar claves con lectura incremental.

## H. Decisión de arquitectura de escala

Se implementó lectura incremental CSV y acceso específico a `trips.txt`, `stops.txt` y `stop_times.txt`, que son las únicas tablas necesarias para la regla actual. El motor conserva sets/mapa de IDs de referencia y procesa `stop_times` fila a fila; la API adaptadora opera sobre rutas de archivo y el CLI no carga los ficheros GTFS completos en memoria.

Esta opción mantiene el orden, códigos y determinismo de la regla sin depender del esquema intermedio DuckDB ni alterar su importación. El coste en memoria queda acotado por los IDs retenidos y el tamaño de la fila; no es constante respecto al número de IDs. El modo DuckDB o procesamiento externo por particiones se pospone hasta que una medición muestre que las cotas de V1 resultan insuficientes. Los límites actuales son 512 MiB por fichero GTFS, 1.000.000 de filas, 4 MiB por registro lógico, 128 KiB por campo y 256 columnas. No se añadió timeout porque la arquitectura actual no tiene cancelación segura por deadline.

## I. Cambios Compliance

`tools/compliance_v1_engine.py` usa `csv.reader` incremental, valida anchuras y límites durante el recorrido, conserva hashing reproducible de archivos y deja `MAX_BYTES = 1 MiB` para el inspector NeTEx. GTFS usa las cotas anteriores. El evaluador mantiene los estados `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE` e `INSPECTION_ERROR`; no convierte errores de recursos en findings.

La regla mantiene `rule_version = compliance-v1/1`. La identidad de implementación pasa a `evaluator_version = compliance-v1/2` con SHA-256 `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`. No se modificaron la base histórica, reglas jurídicas ni evidencias congeladas. El gate estricto Compliance V1 termina en `PACKAGE_GENERATOR_REPLAY`: el paquete persistido contiene la identidad v1, mientras que la implementación actual informa v2. El gate no se relajó ni se reescribió el paquete histórico. La comparación en memoria de `compliance_identity_comparison.json`, tras normalizar solo identidad de implementación (versión/hash/evaluator), coincide con el paquete congelado; el gate estricto sigue detectando que el identificador persistido aún es v1 y requiere revisión/aprobación antes del replay.

## J. Pruebas sintéticas

`tests/test_m04b2_synthetic_triage.py`: 10 pruebas unitarias PASS. Incluyen CSV ordinario, líneas vacías múltiples/al inicio del cuerpo/al final, línea de espacios, CSV escapado, fila malformada de anchura corta/larga, celda citada con espacios, bytes del ZIP de origen inmutables, límites previos, 25k/100k, 100.001 filas combinadas con >1 MiB, resultado repetible y límites de fichero/fila/campo/columna/registro.

El registro de escala observa 100.003 filas fuente (1 trip, 1 stop, 100.001 stop-times), 1.900.118 bytes totales y PASS; el evaluador vuelve a leer una fila de trips y una de stops para validar unicidad. `performance_100k_final.json` registra 60.294 bytes de pico de asignaciones Python observado y 0,916419 s diagnósticos en esta máquina. No son umbrales contractuales ni miden toda la memoria nativa/OS.

## K. Pruebas DEVELOPMENT

No se usó ningún dataset real de DEVELOPMENT. Los fixtures sintéticos bastaron para distinguir parser y evaluador y ejercitar los límites nuevos.

## L. Identidad de motor y versión

Parser: `gtfs-lab-csv/2`. Compliance evaluator: `compliance-v1/2`, hash registrado arriba. Identidad semántica de `V1-RULE-GTFS`: `compliance-v1/1`, sin cambio. Las identidades y resultados históricos M04-B1 permanecen intactos.

## M. Regresión Trust

| Gate | Resultado |
| --- | --- |
| M01 Trust contract | PASS |
| M02 Trust persistence | PASS |
| M03-A Golden contract | PASS |
| Golden Corpus / Evaluator / Regression | PASS; dos casos aprobados ejecutados |
| Split + lineage | PASS |
| GTFS_Lab synthetic/current | PASS |
| Compliance V1 current gate | FAIL: `PACKAGE_GENERATOR_REPLAY` por identidad de evaluador persistida v1 frente a implementación v2 |
| unittest focalizado | 10/10 PASS; descubrimiento GTFS_Lab completo 49/49 PASS |
| `compileall` y `git diff --check` | PASS |

La comprobación Compliance confirma un delta real de identidad de motor contra el snapshot congelado; la comparación tras normalizar únicamente identidad de implementación coincide, pero el gate estricto sigue sin pasar y no se ha presentado como PASS. La base Compliance copiada al worktree antes del gate conservó el SHA-256 `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`; el gate la abrió con `-readonly`.

## N. Integridad Golden, split y evidencia B1

Golden Corpus SHA-256: `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3` (sin cambios). Split SHA-256: `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d` (sin cambios). Ningún caso Golden fue promovido.

Los tres JSON de `reports/evidence/holdout_evaluation_v1/` se compararon byte a byte con la base B2; hashes iguales. No se escribió ninguna base histórica.

## O. Veredicto de replay

`M04B2_BLOCKED`. Los cambios sintéticos y la regresión Trust pasan, pero el gate estricto Compliance V1 detecta la transición de identidad v1→v2 frente al paquete congelado. Aunque los resultados coinciden al normalizar solo identidad, se requiere revisar y aprobar esa transición antes del replay controlado. HOLDOUT permanece cerrado.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
