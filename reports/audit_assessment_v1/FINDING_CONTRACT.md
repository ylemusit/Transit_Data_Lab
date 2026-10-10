# TDL-AUD-04 — contrato de hallazgo valorado

Contrato `TDL_ASSESSED_FINDING/1`. Fecha: 2026-10-08. Capa aditiva sobre casos y resultados existentes. No sustituye el contrato de casos V1 ni modifica el motor congelado.

| Campo | Significado y condición de aceptación |
|---|---|
| case_id / format / condition | Identidad estable, GTFS_SCHEDULE o NETEX, y hecho observado sin atribuir causa. |
| criterion | Texto exacto del criterio, referencia identificada y condición de presencia/aplicación. Campo opcional y valor informado inválido son situaciones diferentes. |
| exposure | Unidades afectadas, población elegible, total de filas cuando proceda, definición y origen del denominador. Si falta, razón explícita; no sustituirlo por cero. |
| evidence | Fichero/identidad, localizador o referencia a las ocurrencias originales y registros de procedencia. Los localizadores GTFS son filas de datos desde 1; se mantienen los originales. |
| observed_impact | VERIFIED exige evidencia; NOT_VERIFIED conserva la falta de medición. Un incumplimiento técnico no demuestra daño al servicio. |
| potential_impact | Consecuencia posible separada del impacto demostrado. No convertirla en coste, viajeros afectados o gravedad confirmada. |
| cause | UNKNOWN, HYPOTHESIS o CONFIRMED. CONFIRMED exige evidencia; correlación espacial o frecuencia de errores no demuestra causa. |
| action / closure | Acción practicable y qué demostraría su cierre mediante fuente nueva y comprobación comparable. |
| priority | UNASSESSED o prioridad propuesta según rúbrica, con evidencia de consecuencias. |
| destination_blocking | NOT_DETERMINED, CONFIRMED o NOT_BLOCKING; las dos últimas requieren evidencia del destino. |
| disposition / producer_status / reaudit | Conservar la decisión técnica y distinguir respuesta, corrección comunicada y re-auditoría. |

Validación invocable: `validate_finding()` en [audit_assessment_v1.py](../../tools/audit_assessment_v1.py). Rechaza unidades afectadas mayores que la población, denominadores desconocidos sin explicación, causas o impactos confirmados sin evidencia y prioridades sin impacto verificado.

Las aplicaciones a fuentes concretas permanecen en el expediente privado; los tests públicos comprueban el contrato con datos sintéticos.

Ejemplo NeTEx (evidencia local no publicada): representa el resultado de un fixture de XML mal formado en la evidencia sintética histórica. Misma estructura, unidades de fichero, criterio XML y cierre sin afirmar conformidad XSD/perfil. Es un ejemplo interno, no una auditoría de operador.

Los `source_ref` de los casos son referencias lógicas: `PRESENTATION_MODEL.json` se resuelve al input `model` del recibo de generación, y sus fragmentos son índices JSON desde cero. No son enlaces a un fichero copiado al directorio de salida. Su materialización portable pertenece a TDL-AUD-08.
