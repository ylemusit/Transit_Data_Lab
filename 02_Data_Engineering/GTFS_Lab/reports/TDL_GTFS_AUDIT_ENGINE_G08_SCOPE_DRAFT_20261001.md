# GTFS Audit Engine V1 — G08: capa de calidad y recomendaciones

**Estado:** alcance y allowlist aprobados; integración G08 local en progreso; G08 no cerrado ni publicado.
**Especificación base:** GTFS Schedule `2026-04-27`.
**Dependencias:** G01–G07 cerrados técnicamente; G02 RuleRegistry y contrato de resultados.

## Propósito

Añadir una capa opcional de recomendaciones y calidad que no altere ni rebautice los resultados de conformidad normativa. G08 no cierra el reporting integrado de G09 ni habilita evaluación de corpus de G10.

## Contrato

- Cada regla declara `authority`, `category`, `severity`, `requirement`, versión semántica, referencia o fundamento y contexto de evaluación en el registro tipado.
- Mantener canales distintos para `GTFS_REQUIRED`, `GTFS_CONDITIONAL`, `GTFS_RECOMMENDED` y `TDL_QUALITY`. Una recomendación o heurística no puede producir un finding presentado como incumplimiento normativo.
- Las reglas recomendadas oficiales se vinculan a una sección concreta de la revisión fijada de GTFS. Las heurísticas TDL llevan identificador y explicación propios, sin atribuirles autoridad externa.
- La evaluación es optativa y determinista. Regla desactivada o fuera de perfil: `NOT_EVALUABLE` o `NOT_APPLICABLE` según el contrato; ausencia de recomendaciones no cambia un PASS normativo.
- Cada resultado incluye alcance observado, prerequisites, valores/evidencia usados, limitaciones y versión. No emitir puntuación agregada ni probabilidad de confianza sin método calibrado aprobado.
- G08 no modifica G03–G07, no cambia severidades normativas existentes, no convierte recomendaciones en errores y no escribe sobre los datos fuente.

## Decisiones de alcance resueltas

1. Aprobar que el alcance V1 cubra únicamente recomendaciones oficiales GTFS expresamente codificadas y heurísticas TDL incluidas en una allowlist revisada; no intentar codificar todas las recomendaciones de la especificación.
2. Aprobar que la primera entrega no incluya score, ranking agregado ni confidence numérica; cada recomendación explicará criterio, evidencia y contexto.
3. Aprobar una allowlist inicial por separado antes de implementación. El candidato mínimo sería recomendaciones con evidencia objetiva y cálculo reproducible sobre datos ya evaluados por G03–G07. Cada fila necesitará ID/versión, fuente exacta, datos requeridos, algoritmo, límites, fixtures positivos/negativos/frontera y clasificación de autoridad.
4. Confirmar si el canal G08 se limita a `WARNING`/`INFO` y si la ausencia de datos requeridos da `NOT_EVALUABLE`, sin degradar el resultado de conformidad.

## Decisión de alcance y allowlist inicial (2026-10-01)

Yeison Arbey Carrillo Lemus aprueba los puntos 1, 2 y 4: G08 V1 es una capa separada y optativa; no emite score, ranking agregado ni confidence numérica; sus recomendaciones usan severidad `INFO` (o `WARNING` en una futura regla aprobada) y la evidencia insuficiente produce `NOT_EVALUABLE`, sin alterar conformidad.

La allowlist inicial queda aprobada solo para presencia de cabecera de estos campos recomendados de `feed_info.txt`:

| ID | Campo | Autoridad / fuente | Criterio y límites |
| --- | --- | --- | --- |
| `GTFS-G08-FEED-START-DATE-DECLARED` | `feed_start_date` | `GTFS_RECOMMENDED`; GTFS Schedule Reference 2026-04-27, `feed_info.txt`, Field Definitions row 5 | Informar si la cabecera declara el campo; sin inferir semántica de valor vacío ni revisar rangos/relaciones temporales (G05). |
| `GTFS-G08-FEED-END-DATE-DECLARED` | `feed_end_date` | `GTFS_RECOMMENDED`; GTFS Schedule Reference 2026-04-27, `feed_info.txt`, Field Definitions row 6 | Informar si la cabecera declara el campo; sin inferir semántica de valor vacío ni revisar rangos/relaciones temporales (G05). |
| `GTFS-G08-FEED-VERSION-DECLARED` | `feed_version` | `GTFS_RECOMMENDED`; GTFS Schedule Reference 2026-04-27, `feed_info.txt`, Field Definitions row 7 | Informar si la cabecera declara el campo; no evaluar contenido, formato ni semántica de valor vacío. |

La validación del candidato confirmó que G03 marca estos tres campos `EXECUTABLE_G03` y `RECOMMENDED`; los dos campos de fecha tienen semántica temporal delegada a G05. Por eso la regla aprobada observa exclusivamente declaración de cabecera, después de que G03 declare fiable la estructura. Archivo ausente es `NOT_APPLICABLE`; estructura G03 no fiable o regla desactivada es `NOT_EVALUABLE`. La ausencia de cabecera genera solo finding informativo con autoridad `GTFS_RECOMMENDED`, estado de regla `PASS` y sin efecto en G03–G07. No se infiere que toda feed deba aportar valores.

## Implementación e integración local (2026-10-01)

`gtfs_lab.g08_quality` implementa el registro tipado G02, registro congelado y evaluación opcional. `pipeline.run` ejecuta G08 después de G07 y escribe `g08.json`; G08 permanece fuera de `validation` legacy y no cambia M02. El resultado separa `recommendation_met`, estado técnico y cobertura específica de G08. La estructura desconocida queda como `UNKNOWN` sin ampliar el enum estable de cobertura G02.

## Revisión técnica local (2026-10-01)

La revisión detectó y corrigió el caso en que `feed_info_headers=None` se trataba como ausencia del archivo aunque G03 no confirmase `NOT_APPLICABLE`. La ausencia ahora requiere evidencia G03 explícita; sin ella, el resultado es `NOT_EVALUABLE`. Once pruebas focalizadas cubren registro/identidad, determinismo, cobertura, resultados de recomendación, ausencia y presencia, estructura no fiable, regla desactivada, regla desconocida, serialización, pipeline y frontera M02. Resultado local: 11 PASS; compilación y `git diff --check` PASS. Falta regresión completa del motor, CI remoto, publicación, post-merge y cierre.

Durante G10, los feeds 019 y 020 demostraron presión de memoria no acotada: G03 retenía evidencia condicional por cada fila y G04 almacenaba en caché todas las tablas parseadas. G03 mantiene ahora un máximo de 1.000 ejemplos de evidencia, añade recuentos completos y los marca explícitamente como muestra; los estados/findings técnicos no se truncan. G04 usa una caché LRU de hasta dos tablas. La evaluación DEVELOPMENT posterior completó los 14 feeds, y el replay de estabilidad pasó. El cambio G03 conserva sus campos existentes y añade metadata de muestreo; tests G03 y G04 pasan localmente. El pico G03 standalone observado para 019 fue aproximadamente 3,6 GB; el pico pipeline integrado sigue siendo un riesgo operativo a revisar en equipos con memoria limitada.

## Gates pendientes para cierre G08

- Contrato tipado y registro congelado rechazan mezcla de autoridad/severidad y duplicados; todos los resultados mantienen identidad semántica.
- Reglas aprobadas tienen fixtures positivos, negativos, límites, datos insuficientes y desactivación; los findings son deterministas y citan evidencia reproducible.
- Regresión confirma que recomendaciones no cambian resultados G03–G07 ni producen un estado de incumplimiento normativo.
- Verificación focalizada, compilación, whitespace y CI se registran como gates distintos; ningún PASS local/CI cierra G08 automáticamente.

El alcance y allowlist ya tienen aprobación de Yeison. Restan regresiones G03–G07, E2E ampliado, CI remoto, revisión/publicación y verificación post-merge. El merge que formalice cierre G08 requiere la decisión humana correspondiente. G08 no autoriza HOLDOUT; G10 se limita a DEVELOPMENT.

Un resultado G08 describe recomendaciones técnicas, no cumplimiento jurídico ni calidad real del servicio.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
