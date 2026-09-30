# GTFS Audit Engine V1 — G05: calendario de servicio y coherencia temporal

**Estado:** alcance aprobado formalmente por Yeison Arbey Carrillo Lemus el 2026-10-01; implementación candidata en revisión técnica.\
**Especificación fijada:** GTFS Schedule `2026-04-27`.\
**Dependencia:** gate formal de G04 y base candidata revisada.\
**Autoridad:** continuación solicitada por Yeison hasta G07; sin publicación ni acceso HOLDOUT.

## Objetivo

Evaluar relaciones de fechas, calendarios y ventanas temporales explícitamente descritas en la referencia fijada, usando valores que G03 haya podido interpretar. Mantener la identidad/unicidad en G04 y las relaciones operativas entre filas en G06.

## Entradas candidatas del capability map

La instantánea de G03 asigna a G05 once campos: `calendar.start_date`, `calendar.end_date`, `calendar_dates.date`, `feed_info.feed_start_date`, `feed_info.feed_end_date`, `frequencies.start_time`, `frequencies.end_time`, `stop_times.arrival_time`, `stop_times.departure_time`, `stop_times.start_pickup_drop_off_window` y `stop_times.end_pickup_drop_off_window`. Esa asignación identifica ownership temporal; no significa que todas las reglas de estos campos sean G05.

## Incluido

- Semántica de alternativas `calendar.txt` y `calendar_dates.txt`, incluida la evaluación dates-only según el contrato de la referencia.
- Coherencia de rangos `calendar.start_date`/`end_date` inclusivos y `feed_info.feed_end_date >= feed_start_date` cuando ambas fechas estén informadas. Los límites feed que exceden los días activos no generan automáticamente un finding: la referencia describe ese tramo como afirmación explícita de ausencia de servicio.
- Aplicación de días semanales y excepciones de `calendar_dates.txt` al conjunto de servicios/días, consumiendo de G04 el resultado de la referencia condicional de `calendar_dates.service_id` si coexiste con `calendar.txt` y la identidad dates-only en otro caso. G05 no duplica identidad ni existencia. En modalidad dates-only, la tabla define el conjunto de días de servicio; su completitud respecto al servicio real externo no se puede verificar desde el feed.
- Comparación del inicio y final de una ventana de recogida/devolución cuando ambos valores sean evaluables.
- Parseo temporal sólo como precondición de comparación; G03 conserva la propiedad de validación léxica. Los tipos `Time` son horas del día de servicio y pueden exceder `24:00:00`; no se tratan como hora civil local. Si G03 no ofrece una interpretación suficiente, G05 devuelve `NOT_EVALUABLE` con cobertura parcial y causa trazable.
- `frequencies.start_time`/`end_time`: coherencia temporal intrafila; G06 conserva headway, referencias, aplicabilidad de frecuencias y relación operacional con los viajes.

## Exclusiones y ownership

- G04 conserva unicidad de claves, incluida `(service_id, date)`, y existencia de referencias/identificadores.
- G03 conserva presencia, condiciones de cabecera, semántica normativa de vacíos y validación léxica cuando está implementada.
- G06 conserva la agrupación por trip, secuencia de paradas, campos alternativos y funcionamiento de `frequencies.txt`; G05 conserva la interpretación y comparación temporal.
- G07 conserva `shapes.shape_pt_sequence`, coordenadas, geometría y evidencia espacial.
- No se derivan nuevas reglas de rangos, precedencia o timezone a partir de prácticas habituales. Toda regla necesita localizador de la referencia y estado claro de autoridad.
- No se amplía soporte a SIRI, GTFS-RT, Flex ni entradas ausentes del perfil congelado.

## Evidencia normativa consultada

La [referencia GTFS Schedule fijada al 2026-04-27](https://gtfs.org/documentation/schedule/reference/) define el rango `calendar.txt` como inclusivo, la semántica de excepciones y el modo `calendar_dates.txt` sin calendario, la hora mayor de 24 como hora del día de servicio y la relación ordenada de intervalos `frequencies`. `feed_info.feed_end_date` no debe preceder a `feed_start_date` cuando ambas están informadas. Los valores que G03 no pueda interpretar siguen sin evaluación en G05.

## Contrato de resultados

La referencia define `Time` como tiempo del día de servicio medido desde el inicio de ese día (incluidos valores posteriores a 24 horas), no como conversión de la parada a su timezone local. `feed_end_date` no precede a `feed_start_date` cuando ambas están informadas. Véanse [definición de Time](https://gtfs.org/documentation/schedule/reference/#field-types) y [feed_info](https://gtfs.org/documentation/schedule/reference/#feed_infotxt) en la revisión fijada.

Reutilizar RuleRegistry y los estados/cobertura G02. Distinguir `FAIL_TECHNICAL` de `NOT_EVALUABLE`, `NOT_APPLICABLE` e `INSPECTION_ERROR`. Las ausencias de datos que G03 aún no pueda interpretar no se convertirán en fallos del operador. Cada finding debe localizar tabla, fila y campos, incluir versión de regla y referencia normativa exacta.

## Matriz preliminar de reglas

| ID propuesto | Comprobación | Evidencia/condición | Límite de evaluación |
| --- | --- | --- | --- |
| `GTFS-G05-CALENDAR-RANGE` | `calendar.start_date <= calendar.end_date`; extremos inclusivos | G03 interpreta ambas fechas. | Fecha no interpretable → `NOT_EVALUABLE`; G04 conserva PK `service_id`. |
| `GTFS-G05-FEED-RANGE` | `feed_end_date` no precede `feed_start_date` cuando ambas existen | Sólo `feed_info` con ambos valores. | Ambos pueden quedar vacíos; fechas feed fuera del calendario no son por sí solas defecto. |
| `GTFS-G05-SERVICE-DATE-SET` | Fechas semanales activas y excepciones (`1` añade; `2` elimina) | Fechas/enum interpretables; IDs resueltos por G04. | Dates-only declara el conjunto; completitud frente al servicio real no se puede comprobar desde el feed. |
| `GTFS-G05-STOP-TIME-CHRONOLOGY` | Comparar tiempos del viaje en orden de secuencia | G06 aporta agrupación/orden; G03 tiempos parseables. | `Time` es tiempo del día de servicio; puede exceder 24h y no se convierte a timezone local por parada. |
| `GTFS-G05-PICKUP-WINDOW` | Candidato para inicio/fin de ventana | Ambos valores presentes y parseables. | Relación/severidad permanece `NEEDS_REVIEW` si el ancla no la expresa; nombres de campos no bastan para declarar un MUST. |
| `GTFS-G05-FREQUENCY-TIME-DOMAIN` | Interpretar `frequencies.start_time` y `end_time` | G03 ofrece valores parseables. | G06 aplica solapamiento, headway y `exact_times`; G04 conserva PK `(trip_id,start_time)`. |

Las IDs son identificadores internos del candidato y no contratos públicos. `RULE_SPECS` y `build_phase_registry` las incorporan a un `RuleRegistry` tipado, congelado y versionado `1.0.0`; una regresión comprueba que todos los IDs, metadatos, evaluator identities y referencias están registrados. Su estabilidad pública requeriría otro gate.

## Aceptación propuesta

- Matriz de reglas con campo, owner, precondiciones G03, referencia, condición, casos deferred y status/coverage esperado.
- Fixtures sintéticos positivos, negativos, frontera, condicional/no aplicable, metadata inválida y fallo de inspección.
- Pruebas específicas de calendario alternativo, dates-only, excepciones añadidas/eliminadas, intervalos invertidos, ventanas temporales y límites de día de servicio que la referencia admita.
- Diferencias con legacy tratadas como solapamiento hasta demostrar equivalencia; legacy permanece productivo.
- Inventario y hashes de entradas congeladas; regresiones G02–G04 y workflow CI enfocado.
- Revisión formal del alcance antes de iniciar runtime; revisión de implementación antes de declarar G05 cerrado.

## Decisión técnica de frontera G05/G06

La roadmap global asigna a G06 secuencias, `stop_times` y `frequencies`, mientras el capability map y la revisión de ownership asignan a G05 ciertas comparaciones temporales de esos mismos campos. La frontera propuesta separa la interpretación/comparación temporal local (G05) de la estructura y coherencia operacional entre filas (G06). Así, G05 puede proporcionar parseo y orden de intervalos como dependencia sin apropiarse de secuencias, referencias, headway ni sustitución de horarios. Si una regla concreta no permite esa separación con base normativa, se mantiene `NOT_EVALUABLE` hasta revisión; no se cambia el ownership por inferencia.

## Candidato local implementado

`gtfs_lab.g05_temporal` implementa rangos inclusivos `calendar`/`feed_info`, días semanales modificados por excepciones `1` (añade) y `2` (elimina), modo dates-only y orden intrafila de `frequencies`. Expone `service_dates_by_service_id` como intervalos semanales compactos más un mapa de excepciones, evitando expandir calendarios grandes en memoria; no entrega materialización parcial si alguna fila deja incompleto el conjunto. Usa horas del día de servicio y admite valores superiores a 24:00. El orden start/end de ventanas de recogida/devolución queda como revisión `TDL_QUALITY / NOT_EVALUABLE`: la referencia define ambos campos y condiciones de presencia, pero no formula esa comparación como MUST. Si G03 o las identidades/referencias G04 no demuestran cobertura suficiente, la regla queda `NOT_EVALUABLE`. La integridad frente al servicio real externo sigue fuera del feed y no se infiere.

Verificación sintética vigente: `tests/test_g05_g07_runtimes.py`, 28 casos compartidos entre G05–G07. `service_dates_by_service_id` conserva periodos semanales (`weekdays` de lunes=0 a domingo=6) y overrides booleanos sin expandir las fechas. Referencias oficiales fijadas: [calendar.txt](https://gtfs.org/documentation/schedule/reference/#calendartxt), [feed_info.txt](https://gtfs.org/documentation/schedule/reference/#feed_infotxt), [frequencies.txt](https://gtfs.org/documentation/schedule/reference/#frequenciestxt) y [field types](https://gtfs.org/documentation/schedule/reference/#field-types).

### Revisión técnica de ownership, 2026-10-01

Los tiempos start/end de ventanas pickup/drop-off no tienen una comparación MUST explícita en la referencia fijada. La rule local anterior `GTFS-G05-PICKUP-WINDOW-RANGE` podía producir un fallo técnico por orden invertido y dar por validada la relación si el orden coincidía. Se reemplazó por `TDL-G05-PICKUP-WINDOW-ORDER-REVIEW` (`QUALITY`, `TDL_QUALITY`, `INFO`, `NOT_EVALUABLE`) hasta recibir autoridad humana sobre esa relación. Hay cobertura sintética para ventanas ordenadas e invertidas sin findings técnicos.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Aprobación formal de alcance y reglas

El 2026-10-01, Yeison Arbey Carrillo Lemus aprobó el alcance congelado y las reglas propuestas de G05 para continuar con el registro tipado y la revisión del candidato. Esta aprobación no declara G05 cerrado ni autoriza HOLDOUT, commit o publicación.
