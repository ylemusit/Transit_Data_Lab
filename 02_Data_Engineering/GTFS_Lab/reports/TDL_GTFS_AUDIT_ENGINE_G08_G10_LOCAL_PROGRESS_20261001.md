# GTFS Audit Engine V1 — recuperación G10 y preparación G11

**Actualizado:** 2026-10-01
**Base integrada:** PR #28, merge `07bd0beaaf158718430ee53a5001e5f01655dac7`; CI post-merge PASS, run `36804060651`.

## Estado de este checkpoint

- G08: criterios técnicos PASS; implementación y suites sintéticas integradas por PR #28. Cierre técnico registrado en el candidato G11.
- G09: criterios técnicos PASS; reporte determinista y suites sintéticas integradas por PR #28. M02 permanece sin cambios y el reporte sigue suplementario.
- G10: se recuperaron los 14 ZIP DEVELOPMENT exactos; hashes de inventario/split verificados antes y después de copiar a `C:/Users/yeiso/AppData/Local/Temp/tdl-g11-development-source-20261001`, fuera de Git.
- Replay: 14/14 completados, cero errores, estabilidad PASS sobre dataset `001`; `HOLDOUT_ACCESSED = NO`.
- G11: revisión técnica preparada para decisión humana final, pendiente de publicar e integrar esta corrección y verificar CI post-merge. La decisión humana no se registra aquí como aprobada.

## Hallazgos del replay y remediación

G03 publica sus estados CSV en `csv_structure.files_inspected`, mientras G04–G07 leían `csv_structure.inspected`. El lector incorrecto ocultaba los estados de archivo y convertía evidencia disponible en incertidumbre downstream. Se corrigió la lectura con compatibilidad para el nombre anterior y se añadieron pruebas de regresión.

G05–G07 ahora contrastan los gaps de tipos G03 con los campos que cada regla consume. Antes, cualquier gap de tipo de un archivo bloqueaba reglas que dependían de otros campos del mismo archivo. No se cambió el contrato de reglas ni el scope normativo.

La evidencia G10 guarda estados de archivo, conteos agrupados por archivo/campo/razón, cobertura por regla y hasta 20 muestras acotadas por etapa. Las muestras omiten valores observados. La atribución se conserva por separado y reconcilia los 83 casos G04 de campos opcionales/condicionales ausentes.

## Cobertura observada

| Regla / etapa | Conteo DEVELOPMENT | Explicación preservada |
|---|---:|---|
| G04 identidad-domain | 32.002 evaluaciones; 13 feeds PASS, uno con finding técnico | `011` contiene referencias de `service_id` que no resuelven contra el dominio disponible de `calendar.txt`. |
| G04 primary-key uniqueness | 102 evaluaciones; 80 no aplicables | Las unidades de llave disponibles pasan; no se marca PASS para tablas no presentes. |
| G04 reference-existence | 1.168.910 evaluaciones; 83 N/E; 158 N/A | Los 83 N/E se reconcilian con cabeceras opcionales/condicionales ausentes, identificadas por feed/campo. |
| G05 calendar-range | 417 evaluaciones; 13 feeds PASS, uno N/A | Fechas comparadas sin gaps de regla evaluables. |
| G05 feed-range | 6 evaluaciones; 7 N/A; uno N/E | Siete feeds no tienen `feed_info.txt`; a `016` le falta un valor de fecha de feed. |
| G05 service-date-set | 13 PASS; `011` N/E | Depende del dominio G04 no resuelto en `011`. |
| G06 stop-sequence | 558.810 evaluaciones; 14 PASS | Secuencia evaluada en todos los feeds DEVELOPMENT. |
| G06 trip-time-order-review | 14 N/E | `DEFERRED_BY_SCOPE`: no hay requisito MUST de monotonía en la referencia fijada. |

Frecuencias no aplica a los 14 feeds. Las cabeceras de ventana pickup/drop-off no aparecen en este corpus. G07 registró nueve PASS, cuatro N/A y un finding técnico en `014`. G08 produjo siete PASS y siete N/A.

G03 conserva gaps reales: 1.682.207 `CONDITION_UNKNOWN`, 168 `UNRESOLVED_CONDITION`, 11 `UNRESOLVED_EXTENSION_POLICY`, 23 `UNRESOLVED_TYPE_FORMAT` y 39 `UNSUPPORTED_LEXICAL_VALIDATOR`. El único finding G03 observado sigue en `010 / agency.txt / agency_url`; no se introdujo excepción por operador.

## Evidencia y comprobaciones

- Replay: [G10 recovery](evidence/g10_development/g10_development_recovery_20261001.json), SHA-256 `5c1f6dc8a744fe4df44ea2e57e61e6c4e365bc402b240501a682a37cc8447479`.
- Cobertura/categorías por regla y dataset: [evaluability attribution](evidence/g10_development/g10_evaluability_attribution_20261001.json), SHA-256 `497e2694d31c96ae58ee05461bc6309b0475f483afb3acb5a766fad520a33712`.
- Pruebas dirigidas G03–G10: 114 PASS.
- HOLDOUT no abierto; M02 sin cambios; no se encontró código específico por operador/dataset.

## Límites

El resultado no declara cobertura GTFS completa, cumplimiento jurídico, certificación, readiness comercial ni equivalencia total con legacy. Se conservan los 15 gaps G03, la política de extensiones abierta, la deuda local `CREATED_LOCAL_UNPUBLISHED` del inventario G04 y las fronteras de M02/legacy. NeTEx, SIRI y GTFS-RT quedan fuera de alcance.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
