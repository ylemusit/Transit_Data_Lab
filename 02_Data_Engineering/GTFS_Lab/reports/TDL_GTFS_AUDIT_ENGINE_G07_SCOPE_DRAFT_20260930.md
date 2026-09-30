# GTFS Audit Engine V1 — G07: shapes y evidencia espacial

**Estado:** alcance aprobado formalmente por Yeison Arbey Carrillo Lemus el 2026-10-01; implementación candidata en revisión técnica.\
**Especificación fijada:** GTFS Schedule `2026-04-27`.\
**Dependencias:** gates revisados de G04, G05 y G06.\
**Perfil:** `shapes.txt` opcional de GTFS Schedule V1.

## Objetivo

Evaluar estructura espacial de shapes, orden de sus puntos, coordenadas y relaciones entre distancia declarada y recorrido cuando la referencia permita afirmarlas; producir evidencia reproducible asociada a los findings.

## Incluido

- Campos/filas `shapes.txt` del catálogo congelado y su lectura compatible con G03.
- Consumo de unicidad `(shape_id, shape_pt_sequence)` y referencias de `trips.shape_id` ya cubiertas por G04, sin duplicar findings.
- Orden espacial declarado de `shape_pt_sequence` por shape y comprobaciones explícitas de `shape_pt_lat`/`shape_pt_lon`.
- Interpretación de `shape_dist_traveled` y su coherencia dentro de un shape únicamente donde la referencia fijada determine la semántica con suficiente precisión.
- Secuencia de puntos creciente, sin exigir números consecutivos; distancia declarada creciente al aumentar la secuencia, sin inferir dirección inversa.
- Evidencia espacial determinista: coordenadas fuente, orden/fila, unidades/fuente y transformación aplicada; la salida no cambia el dataset ni atribuye errores por estimaciones cartográficas.
- Cobertura por rule/feature, con estados G02 y localizadores a especificación.

## Exclusiones y ownership

- G03 conserva estructura CSV y validez léxica de números; G04 conserva identidad, unicidad y referencias; G06 conserva tiempo y secuencia operacional de `stop_times`.
- Distancia geodésica calculada, tolerancias geométricas, detección de desvío de ruta, matching con calles y juicios de plausibilidad son heurísticas/calidad y quedan fuera de G07 salvo aprobación específica posterior.
- No se puede demostrar igualdad de unidades entre `shapes.shape_dist_traveled` y `stop_times.shape_dist_traveled` si el feed no las declara; registrar esa limitación y no inferirlas de las magnitudes.
- No se convierte CRS, no se supone proyección distinta de la definida por el contrato, no se usa información externa de mapas.
- La unicidad de los puntos permanece en G04; G07 evalúa semántica de orden espacial sin reclamar propiedad de la clave.
- Sin `shapes.txt`, las reglas espaciales son `NOT_APPLICABLE`; con tabla incompleta o valores no interpretables, cobertura `NOT_EVALUABLE`/`INSPECTION_ERROR`, no `PASS`.

## Aceptación propuesta

- Matriz normativa campo por campo para shape ID, secuencia, latitud, longitud y distancia, con owner y gaps explícitos.
- Fixtures para shape ausente/presente, secuencias no negativas/no únicas, límites de coordenada, coordenada no parseable, distancia ausente/parcial/monótona y fallos de lectura. Las distancias se ordenan por `shape_pt_sequence`, no por el orden de filas físicas.
- Distinción comprobada entre defecto de identidad G04, defecto espacial G07 y heurística excluida.
- Evidencia determinista y localizable; regresión G02–G06 y CI específico.
- Revisión formal de alcance/implementación antes del cierre técnico G07.

## Límites

Un finding técnico de coordenadas o secuencia no es una conclusión jurídica ni acredita que una ruta coincida con el servicio real. G07 no cierra el engine V1 completo: calidad (G08), reporting/evidence integration (G09), evaluación autorizada de corpus (G10) y gate de cierre V1 (G11) permanecen posteriores.

La [referencia GTFS Schedule fijada al 2026-04-27](https://gtfs.org/documentation/schedule/reference/) define coordenadas WGS84, límites de latitud/longitud, orden creciente no necesariamente consecutivo para `shape_pt_sequence` y crecimiento de `shape_dist_traveled` a lo largo de la secuencia. Describe la cercanía de paradas a la forma como recomendación sin umbral numérico; no se convierte en fallo automatizado.

## Candidato local implementado

`gtfs_lab.g07_spatial` comprueba secuencias no negativas y únicas (unicidad delegada a G04), límites inclusivos de latitud/longitud WGS84 y crecimiento estricto de `shape_dist_traveled` al ordenar por `shape_pt_sequence`, independientemente del orden físico de filas CSV. La ausencia de `shapes.txt` es `NOT_APPLICABLE`; las brechas estructurales/tipológicas detectadas por G03 dejan G07 `NOT_EVALUABLE`. No calcula distancias geodésicas ni decide plausibilidad cartográfica. La comparación de unidades de distancias shapes/stops sigue expresamente sin evaluarse.

Referencias oficiales: [shapes.txt](https://gtfs.org/documentation/schedule/reference/#shapestxt). Casos sintéticos compartidos en `tests/test_g05_g07_runtimes.py`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Aprobación formal de alcance y reglas

El 2026-10-01, Yeison Arbey Carrillo Lemus aprobó el alcance congelado y las reglas propuestas de G07 para continuar con el registro tipado y la revisión del candidato. `RULE_SPECS` y `build_phase_registry` producen definiciones `RuleDefinition` tipadas en un `RuleRegistry` congelado; la regresión de G05–G07 comprueba IDs, versiones, metadatos, evaluator identities y revisión normativa. Esta aprobación no declara G07 cerrado ni autoriza HOLDOUT, commit o publicación.
