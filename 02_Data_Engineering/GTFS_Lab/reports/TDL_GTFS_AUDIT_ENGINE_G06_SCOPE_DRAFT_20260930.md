# GTFS Audit Engine V1 — G06: `stop_times`, secuencia y coherencia operacional

**Estado:** alcance aprobado formalmente por Yeison Arbey Carrillo Lemus el 2026-10-01; implementación candidata en revisión técnica.\
**Especificación fijada:** GTFS Schedule `2026-04-27`.\
**Dependencias:** gates revisados de G04 y G05.\
**Ámbito:** perfil fixed-stop V1; Flex permanece deferred salvo evidencia evaluable ya soportada.

## Objetivo

Evaluar la integridad operacional de las filas `stop_times.txt`, su secuencia por viaje y las reglas explícitas de `frequencies.txt`, usando catálogo/presencia y lectura estructural de G01/G03, referencias G04 y valores temporales G05.

## Incluido

- Agrupación de dos o más filas por viaje y monotonía de `stop_sequence`; G04 sigue informando duplicados de clave.
- Consumo del resultado temporal G05 junto al orden de secuencia. G05 conserva semántica y comparación de tiempo; G06 aporta agrupación/secuencia operacional sin duplicar el finding temporal.
- Reglas de presencia de primera/última parada y campos dependientes de `timepoint` sólo cuando el contrato G03 pueda resolver su expresión; las expresiones `NEEDS_REVIEW` siguen `NOT_EVALUABLE`.
- Condiciones de campos de parada fija frente a los selectores Flex, únicamente si G03 entrega una expresión de outcomes ejecutable. Una condición `NEEDS_REVIEW` no se reconstruye en G06.
- Reglas de `frequencies.txt` para `headway_secs`, `exact_times`, intervalos no solapados por viaje y relación operacional. G05 proporciona el dominio de `start_time`/`end_time`; G04 mantiene clave y referencia del viaje. Intervalos contiguos pueden compartir el instante de frontera.
- Ubicación de findings por fichero, fila, viaje y campo, con estado y cobertura G02.

## Exclusiones y ownership

- G03 conserva validez CSV, tipos léxicos, cabeceras y presencia/condiciones que ya sean ejecutables.
- G04 conserva unicidad `(trip_id, stop_sequence)` y `(trip_id, start_time)`, identidad y existencia de referencias.
- G05 conserva el parseo/precondición temporal y las comparaciones de ventanas/date-time que le atribuye el contrato.
- G06 no implementa grafo de estaciones, geometría, semántica de shapes ni comportamiento de reservas Flex.
- No completar campos requeridos mediante inferencias locales cuando su expression/outcome siga sin resolver; el estado será `NOT_EVALUABLE`.
- No se rebajan reglas existentes de legacy ni se etiqueta paridad sin matriz y evidencia por status/coverage.

## Aceptación propuesta

- Matriz normativa de secuencia, alternativas fixed-stop, campos horarios y frecuencias con localizadores y propietario único.
- Fixtures positivos, negativos, límites, no aplicables, targets ausentes, input no evaluable y errores de inspección.
- `stop_sequence` es el valor que declara el orden de paradas; G06 valida su dominio no negativo y ordena tiempos por dicho valor. Las filas físicas CSV no se presumen ordenadas; duplicados quedan en G04.
- Casos de hora inválida consumen el resultado de G05; G06 no emite falsa infracción de viaje cuando el tiempo es `NOT_EVALUABLE`.
- Casos de `frequencies.txt` ausente/presente, intervalos, headway, `exact_times`, asociación a viaje y tablas vacías; cada regla comprueba applicability y cobertura.
- Regresión G02–G05, workflow CI y documentación de gaps; ninguna lectura HOLDOUT.
- Revisión formal de alcance/implementación antes de marcar G06 cerrado.

## Frontera operacional

La roadmap V1 incluye en G06 `stop_times`, secuencia, horas y frecuencias. El capability map asigna a G05 el ownership temporal de las horas y algunas comparaciones. Este borrador conserva esa separación: G05 interpreta fechas/horas y ventanas; G06 agrupa por viaje usando la secuencia declarada y evalúa headway/frecuencias. La referencia dice que `stop_sequence` aumenta a lo largo del viaje sin ser consecutiva y permite intervalos de frecuencia contiguos. No establece un requisito MUST explícito de monotonía entre horas de distintas filas; por ello G06 no produce findings técnicos de cronología y conserva esa regla como `TDL_QUALITY/NOT_EVALUABLE` para decisión humana. Fuente: [GTFS Schedule Reference, revisión 2026-04-27](https://gtfs.org/documentation/schedule/reference/).

## Candidato local implementado

`gtfs_lab.g06_operations` valida secuencias no negativas (G04 conserva unicidad y cada valor declara el orden), `headway_secs > 0`, `exact_times=1` y no solapamiento por viaje; intervalos contiguos se admiten. Para `exact_times=1`, un intervalo de longitud cero falla la regla explícita de que end_time supere el último inicio deseado. Con `exact_times` vacío/0, la longitud cero queda `NOT_EVALUABLE` y deferred `TDL_QUALITY`, sin convertir una relación start<end no anclada como MUST en finding GTFS. Orden temporal entre paradas queda como regla informativa `TDL_QUALITY` `NOT_EVALUABLE`: la referencia fijada describe horas por parada, pero no declara explícitamente una relación cross-row MUST. Los errores léxicos/estructurales G03 y tiempos G05 no evaluables producen `NOT_EVALUABLE`. La asociación completa de frecuencias con viajes y reglas condicionales de `stop_times` que dependen de expresiones G03 sin resolver quedan fuera del candidato.

Referencias oficiales: [stop_times.txt](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) y [frequencies.txt](https://gtfs.org/documentation/schedule/reference/#frequenciestxt). Casos sintéticos compartidos en `tests/test_g05_g07_runtimes.py`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Aprobación formal de alcance y reglas

El 2026-10-01, Yeison Arbey Carrillo Lemus aprobó el alcance congelado y las reglas propuestas de G06 para continuar con el registro tipado y la revisión del candidato. `RULE_SPECS` y `build_phase_registry` producen definiciones `RuleDefinition` tipadas en un `RuleRegistry` congelado; la regresión de G05–G07 comprueba IDs, versiones, metadatos, evaluator identities y revisión normativa. Esta aprobación no declara G06 cerrado ni autoriza HOLDOUT, commit o publicación.
