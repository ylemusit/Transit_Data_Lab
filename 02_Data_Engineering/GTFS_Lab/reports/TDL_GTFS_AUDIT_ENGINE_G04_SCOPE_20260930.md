# GTFS Audit Engine V1 — G04: identidad e integridad referencial

**Fase:** definición de alcance solamente\
**Base:** `137ff4ed38da65fb3fb61f9804d729a1cee51feb`\
**Especificación fijada:** GTFS Schedule `2026-04-27`\
**Dictamen técnico revisado:** `G04_SCOPE_READY_FOR_IMPLEMENTATION_REVIEW` (no autoriza ni inicia implementación)

## Objetivo

Definir un contrato trazable para comprobar unicidad de identificadores y existencia de referencias pobladas en GTFS Schedule V1. El inventario máquina-legible deriva sus candidatos de los contratos G01/G03 congelados, conserva incertidumbres y registra los hashes de entrada.

## No objetivos

- Implementar evaluadores, reglas productivas, findings, remediación, migraciones o integración de pipeline.
- Cambiar G03, la revisión fijada de la especificación, `validation.py` legacy o evidencia histórica.
- Validar semántica de valores vacíos, requisitos/presencia, secuencias G05/G06, grafos o reglas no expresadas por el contrato.
- Inferir un destino a partir de nombres parecidos, contenido de feeds, referencias externas o reglas legacy.
- Consultar HOLDOUT, iniciar G05+, publicar, hacer commit o abrir PR.

## Límites de arquitectura

G03 sigue siendo propietario de presencia, condición y validez estructural/de tipos. G04 consume valores ya interpretables y evidencia disponible de los ficheros padre. El registro G02 proporciona identidad estable por regla, applicability de tres valores, cobertura separada del status y vocabulario nativo. La validación legacy sigue productiva hasta una prueba de equivalencia y una decisión posterior; este documento no la modifica.

La cobertura del destino debe declarar por entidad si la evidencia está disponible, diferida o sin resolver. `NOT_EVALUABLE` es el resultado cuando falta evidencia autoritativa. Una entidad diferida no constituye error del operador. Un fallo de lectura produce `INSPECTION_ERROR`.

## Composite Identity

La especificación fijada define claves primarias como un campo o combinación de campos que identifica de forma única una fila. G04 inventaría esas declaraciones explícitas para todos los ficheros `FULL_V1_TECHNICAL`; no deriva claves a partir de `UNIQUE_ID` ni de nombres de campos. La unicidad de la tupla completa corresponde a G04. La semántica del componente sigue en la etapa propietaria: `stop_times.stop_sequence` conserva secuencia operativa en G06; `shapes.shape_pt_sequence` conserva semántica espacial en G07; `calendar_dates.date` y `frequencies.start_time` conservan semántica temporal en G05. Esta separación permite que G04 compruebe unicidad sin duplicar reglas de orden o tiempo.

El inventario contiene 7 claves de un solo campo y 6 compuestas. También registra `feed_info.txt` como `NONE` (la fuente permite una fila) y representa claves `ALL_FIELDS` si una declaración así aparece en el conjunto soportado. El catálogo resumía la clave de `transfers.txt` como todos los campos; la declaración primaria explícita de la referencia fijada enumera seis campos y se transcribe como clave compuesta. El localizador enlaza cada clave con el atributo Primary key.

Los 31 registros actuales se conservan como `FIELD_LEVEL_IDENTITY_REFERENCE_CANDIDATES`: 7 `UNIQUE_ID` y 24 `FOREIGN_ID`. Son candidatos a nivel de campo; no representan el alcance total de identidad. Los IDs de campo no autorizan inferir claves compuestas.

## Identity Domains

No se presume que cualquier campo llamado `id` sea único. Además de referencias físicas fichero/campo, G04 modela dominios lógicos: un mismo identificador puede contribuirse desde más de una fuente y ser consumido sin que cada fichero sea un padre obligatorio.

Se conserva el modelo aprobado `SERVICE_ID`: `calendar.service_id` contribuye al dominio; `calendar_dates.service_id` contribuye condicionalmente o puede referir al calendario; `trips.service_id` consume el dominio. Si `calendar.txt` está presente, `calendar_dates.service_id` puede referir a sus servicios. Si está ausente, los valores poblados de `calendar_dates.service_id` pueden establecer identidades. No se exige `calendar_dates.txt` como segundo padre independiente.

## Contextual References

`translations.table_name` selecciona el dominio y la clave primaria destino. La política relaciona el selector con `record_id` (primer o único componente de la clave) y, cuando corresponde, `record_sub_id` (componente secundario). Para `stop_times`, el par es `trip_id` + `stop_sequence` y el secundario es requerido cuando se usa `record_id`. Para claves simples el secundario no aplica. `feed_info` prohíbe ambos IDs; la alternativa `field_value` también los excluye, y su interpretación queda fuera de matching G04 en esta fase.

Se normalizan sólo los selectores documentados en la referencia: mappings explícitos y mappings recomendados aparecen diferenciados en `contextual_reference_policies`. Destinos FULL quedan ejecutables en principio cuando exista runtime; `attributions`, `fare_attributes` y `fare_rules` están diferidos y quedan `NOT_EVALUABLE / DEFERRED_TARGET`, sin fallo del operador. Selectores o semánticas no oficiales/no resueltos quedan `NOT_EVALUABLE / CONTEXTUAL_TARGET_UNRESOLVED`. No se incorporan valores de feeds ni reglas específicas de operadores.

## Coverage

La cobertura de G04 incluye candidatos de campo, claves primarias explícitas de las 14 tablas FULL, el dominio `SERVICE_ID`, referencias ordinarias y las políticas contextuales descritas. Las referencias a targets diferidos siguen sin evaluación, no en PASS/FAIL. `locations.geojson#Feature.id` permanece diferido y fuera del catálogo CSV; los campos de Flex y los targets `booking_rules.txt`/`location_groups.txt` siguen diferidos. Los selectores contextuales no oficiales permanecen sin resolver. La fase no crea runtime ni findings.

## Modelo referencial

Una referencia simple apunta a un campo padre concreto. Ejemplo: `trips.route_id → routes.route_id`. Las referencias pobladas se evalúan de forma independiente de si la presencia del campo era obligatoria. G04 no reinterpreta un vacío ni produce una infracción de presencia.

`trips.service_id` apunta conceptualmente al dominio lógico `SERVICE_ID`. Los ficheros físicos contribuyentes se conservan como procedencia, pero la existencia se resolverá contra el dominio construido según la presencia de sus contribuyentes, no como un OR ingenuo de padres independientes. Esto evita exigir a `calendar_dates.txt` que actúe siempre como padre separado.

Las referencias dentro de la misma familia, como `stops.parent_station → stops.stop_id`, distinguen padre válido de padre ausente. No se prohíbe una autorreferencia ni se inventa semántica de grafo salvo que la especificación lo haga explícito.

Los detalles de selector, mapeo y evaluabilidad contextual se definen en `## Contextual References`; este inventario es metadato de alcance y no ejecuta matching.

## Status y cobertura

Se reutiliza exclusivamente el vocabulario G02:

| Evidencia y aplicabilidad | Status propuesto |
| --- | --- |
| Referencia poblada, padre autoritativo disponible y coincidencia | `PASS` |
| Referencia poblada, padre autoritativo disponible y sin coincidencia | `FAIL_TECHNICAL` |
| Padre ausente, diferido o target unresolved | `NOT_EVALUABLE` |
| Sin referencia poblada aplicable | `NOT_APPLICABLE` |
| Fallo de inspección | `INSPECTION_ERROR` |

La falta de padre nunca equivale a `PASS`. Un target diferido nunca genera fallo del operador por sí solo. Cobertura describe soporte/evidencia; status describe el resultado de una regla.

## Frontera de valores vacíos

G04 verifica existencia sólo para referencias pobladas. No determina si un campo vacío era válido, requerido, opcional, prohibido o significativo. Ese criterio corresponde a G03 o al propietario declarado, salvo regla de identidad explícita en la revisión fijada. Valores ausentes no se fabrican como referencias vacías ni se convierten en huérfanos.

## Inventario derivado

El artefacto [gtfs_schedule_g04_identity_references_2026_04_27.json](../spec/gtfs_schedule_g04_identity_references_2026_04_27.json) contiene cada candidato `UNIQUE_ID`, cada `FOREIGN_ID` y todo campo cuyo ownership normalizado sea G04. Cada registro diferencia identidad fuente, identidad y ficheros físicos destino, dominio lógico, rol, condición, evaluabilidad, estado/candidatos deferred, ownership entre etapas y localizador trazable. Incluye SHA-256 de las tres entradas G01/G03. Se regenera mediante `python tools/generate_g04_identity_inventory.py`; `--check` compara bytes con la derivación determinista.

Los conteos independientes (`counts` del JSON) son:

| Familia | Conteo |
| --- | ---: |
| A. Candidatos de campo `FIELD_LEVEL_IDENTITY_REFERENCE_CANDIDATES` | 31 |
| B. Campos `UNIQUE_ID` | 7 |
| C. Campos `FOREIGN_ID` | 24 |
| D. Claves primarias de un campo | 7 |
| E. Claves primarias compuestas | 6 |
| F. Dominios de identidad | 1 |
| G. Referencias foráneas ordinarias | 20 |
| H. Políticas contextuales | 17 |
| I. Políticas contextuales a destino diferido | 3 |
| J. Políticas contextuales unresolved | 1 |

El inventario también contiene una fila `NONE` (`feed_info.txt`); no hay `ALL_FIELDS` entre las declaraciones FULL tras normalizar la clave explícita de transfers. Las políticas contextuales se dividen en 12 ejecutables en principio, 3 deferred, 1 unresolved y 1 prohibida/no aplicable (`feed_info`). Esas categorías no se suman a referencias ordinarias. Los conteos se derivan durante la generación.

## Constraints entre etapas

- G03 provee presencia de cabeceras, reglas léxicas/de tipo y semántica de requisitos/vacíos; G04 consume sus entradas sin tomar ownership de esas reglas.
- G04 es propietario de unicidad, construcción de dominios de identidad y existencia de referencias pobladas.
- G05 conserva interpretación temporal, incluida la semántica de `calendar_dates.date`; la unicidad de `(service_id, date)` sigue siendo G04.
- G06 conserva secuencia/orden de `stop_times` y `frequencies`; la unicidad de sus claves compuestas sigue siendo G04.
- G07 conserva semántica espacial/secuencia de `shapes`; la unicidad de `(shape_id, shape_pt_sequence)` sigue siendo G04.
- G02 provee los status y el contrato de applicability/cobertura.
- Ninguna etapa posterior asume propiedad de la unicidad de una clave primaria declarada: G04 la conserva, mientras G05/G06/G07 mantienen la semántica temporal, operativa o espacial de componentes.
- Los targets `booking_rules.txt` y `location_groups.txt` quedan `NOT_EVALUABLE` por estar deferred en G01. `locations.geojson#Feature.id` no es una tabla FULL del catálogo CSV G01 y queda sin evaluación hasta definir una evidencia compatible.
- `translations` ya tiene metadatos normalizados de selector y componente; evaluación/matching sigue fuera de alcance. `field_value` y precedencia requieren tratamiento en una fase posterior.

## Solapamiento con validación legacy

La inspección es de `gtfs_lab/validation.py`; no se cambió el comportamiento.

| Regla | Comportamiento y alcance observado | Riesgos | Relación propuesta | ¿Legacy sigue productiva? |
| --- | --- | --- | --- | --- |
| `GTFS-REF-TRIP-ROUTE` | Recorre `trips.route_id`; consulta IDs de `routes.route_id` sólo si `routes.txt` pudo cargarse. Valor poblado o vacío se compara cuando el set existe. | Si falta el padre, omite comprobación y puede acabar en `PASS`; con padre disponible, vacío puede reportarse huérfano aunque es cuestión de presencia G03. | `PARTIAL_OVERLAP`; no hay evidencia nueva de equivalencia. | Sí |
| `GTFS-REF-SERVICE` | Forma una unión de IDs poblados de `calendar.service_id` y `calendar_dates.service_id`; la regla requiere al menos un calendario para marcar cobertura disponible. | Un vacío con calendario disponible puede reportarse como huérfano; ausencia de calendario se detecta también como regla estructural. No formaliza aquí completeness de evidence por tabla. | `PARTIAL_OVERLAP`; candidata a equivalencia tras prueba de status/coverage y vacíos. | Sí |
| `GTFS-REF-SHAPE` | Sólo comprueba `trips.shape_id` poblado cuando `shapes.txt` está presente; carga `shapes.shape_id`. Si shapes no está, omite y la regla puede resultar `PASS`. | `PASS` con target ausente produce falsa cobertura; valor vacío se ignora. El soporte FULL/deferred debe gobernar G04. | `PARTIAL_OVERLAP`; preservar hasta implementar y probar `NOT_EVALUABLE` correctamente. | Sí |
| `GTFS-UNIQUE-PRIMARY-ID` | Comprueba duplicados no vacíos en `routes.route_id`, `trips.trip_id`, `stops.stop_id`, `agency.agency_id`; aplica una regla agregada y omite otros UNIQUE_ID del contrato. | Cobertura incompleta para `calendar`, `pathways`, `levels`; el nombre “primary” no modela semántica por campo. La rutina ejecuta dentro de la validación legacy. | `PARTIAL_OVERLAP`; ninguna equivalencia total antes de demostrar mismos dominios y estados. | Sí |

No se clasifican reglas legacy como `SUPERSEDED_BY_G04` en scope: no existe aún evaluador G04 ni prueba de paridad. Reglas legacy fuera de esta tabla permanecen fuera de G04 salvo análisis futuro.

## Criterios de aceptación para esta fase

- Worktree y rama G04 preexistentes reutilizados; HEAD permanece exactamente en la base indicada, con G03 presente. Los borradores locales preexistentes se preservan y se actualizan en alcance.
- Cada registro del inventario traza a G03/G01, sin IDs duplicados ni targets desconocidos inferidos.
- Hashes de entrada incluidos y regeneración byte-determinista.
- G03 field contract y capability map sin cambios (SHA-256 conservados).
- Regeneración determinista `--check`, `py_compile`, 49 pruebas G03 y `git diff --check` PASS.
- Sin acceso a HOLDOUT, sin runtime G04, publicación, commit, PR o inicio de G05+.
- Revisión formal humana del alcance pendiente.

## Arquitectura de implementación propuesta

Un evaluador G04 puro y aislado, alimentado por campos G03 y una capa explícita de disponibilidad de entidades G01. Un registro de restricciones tipadas representará unicidad, dominios lógicos multi-source, referencia condicional, referencia simple, referencia padre y unresolved/deferred. Antes de iterar valores, se resolverá cobertura del target; sólo la cobertura completa habilitará existencia. Salidas por regla usarán status G02 y coverage separada, con trazabilidad al campo y valor fuente. La integración legacy/productiva queda para una fase posterior tras fixtures sintéticos de casos presentes, ausentes, duplicados, dominios multi-source, self-reference, deferred, vacíos y errores de inspección, revisión de paridad y autorización de alcance.

## Evidencia de esta remediación

- Worktree: `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g04`; rama `feat/gtfs-engine-g04-identity-referential`; HEAD `137ff4ed38da65fb3fb61f9804d729a1cee51feb`, descendiente de la base requerida. Había borradores locales G04 sin commit al iniciar; se conservaron y actualizaron.
- Inventario: 31 registros (`UNIQUE_ID=7`, `FOREIGN_ID=24`); SHA-256 de bytes `1691125CC2DECD90E2A011B2F86EB52512187CD72E60EF534D7E58AFD8CC1165`.
- Entradas: field contract `B583CA329D4E034C5553A0EE6E1BCECF7BDB8C6736FE2CEDAD822302F5B9B4D6`; capability map `0B4CCAEC009E983E2C96D707D0D93C92735AD3AEE4AC70EDE9C52C32DA6D452D`; catálogo G01 `366A9CADDE04E3E2E5980FD02ACD3C9FBDA49766CC9C8E0AD7AD696F1EC712F8`.
- `python tools/generate_g04_identity_inventory.py --check`: PASS. Generación repetida byte-determinista.
- `python -m unittest discover -s tests -p "test_g03_*.py"`: 49 tests, PASS.
- `python -m py_compile tools/generate_g04_identity_inventory.py`: PASS. `git diff --check`: PASS.
- Los SHA-256 del field contract y capability map coinciden con los hashes de entrada; `git diff` confirma ambos sin cambios.
- Las cuatro reglas legacy (`GTFS-REF-TRIP-ROUTE`, `GTFS-REF-SERVICE`, `GTFS-REF-SHAPE`, `GTFS-UNIQUE-PRIMARY-ID`) siguen en `PARTIAL_OVERLAP` y productivas.
- No se accedió a HOLDOUT. No se inició G05+, no se implementó runtime y no se hizo commit, push ni PR.

**Dictamen técnico revisado:** `G04_SCOPE_READY_FOR_IMPLEMENTATION_REVIEW`. Confirma que la definición puede pasar a revisión para autorizar posteriormente la implementación; no inicia runtime ni sustituye la revisión/aprobación humana.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
