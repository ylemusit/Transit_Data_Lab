# TDL-AUD-06 — conclusión técnica y prioridad de actuación

Fecha: 2026-10-08. Rúbrica inicial propia de TDL. Es una propuesta de decisión para un destino documentado, no una clasificación atribuida a ISO, IIA o a la especificación del formato.

## Cuatro dimensiones independientes

1. **Estado técnico:** resultado del criterio implantado en una versión concreta.
2. **Exposición:** cantidad de unidades afectadas sobre población elegible, con su unidad. No equivale a viajeros, gravedad ni probabilidad de daño.
3. **Evidencia:** hecho técnico vinculado a fuente; criterio documentado; consecuencias del servicio verificadas o pendientes. No calificar como independencia externa una interpretación interna.
4. **Prioridad y bloqueo de destino:** requieren uso, criterios de aceptación, plazo y consecuencias documentadas. UNASSESSED y NOT_DETERMINED son resultados válidos cuando falta contexto.

## Rúbrica de prioridad propuesta

Antes de asignar nivel se exigen: destino, referencia de criterios de aceptación, fecha objetivo ISO y referencia de evidencia de consecuencias. Las referencias requieren revisión humana: un texto con nombre de fichero no autentica su contenido.

| Evidencia de consecuencia para el destino | Prioridad propuesta | Condición adicional |
|---|---|---|
| Servicio no disponible dentro del uso auditado, con urgencia y ausencia de alternativa documentadas | CRITICAL | Evidencia específica de urgencia y falta de alternativa; no se deduce solo de una fecha próxima. |
| Servicio no disponible o función necesaria que falla | HIGH | Reproducción o constatación verificable de la consecuencia. |
| Degradación comprobada del resultado utilizado | MEDIUM | Evidencia de la degradación; no basta una advertencia del validador. |
| Defecto comprobado de presentación | LOW | Evidencia en el consumidor identificado. No implica conformidad del resto de datos. |
| Destino, plazo o consecuencia no verificados | UNASSESSED | Obtener contexto o medición antes de clasificar. No convertirlo en LOW. |

Ejemplos: un millón de anotaciones sin impacto verificado permanece UNASSESSED; dos valores que provocan un fallo funcional reproducido pueden ser HIGH; un XML mal formado confirma el defecto técnico, pero su prioridad depende del destino y del uso. Son ejemplos metodológicos, no valoraciones de un operador real.

La prioridad no decide automáticamente si un destino acepta la entrega. El bloqueo se documenta aparte con criterio del consumidor y evidencia de aceptación/rechazo. El orden de trabajo puede responder a dependencias de corrección sin atribuir niveles de riesgo.

## Conclusión técnica

La función `conclusion()` recibe controles únicos, no filas duplicadas. Conserva por separado fallos técnicos, límites de cobertura, no aplicables y errores de inspección. No calcula una nota ni porcentaje global de PASS.

* Fallos y límites: NONCONFORMITIES_DETECTED_WITH_COVERAGE_LIMITS.
* Fallos sin límites declarados: NONCONFORMITIES_DETECTED_IN_DEFINED_SCOPE.
* Sin fallos detectados y con límites: NO_NONCONFORMITY_DETECTED_WITH_COVERAGE_LIMITS.
* Sin fallos detectados ni límites declarados y con controles PASS: NO_NONCONFORMITY_DETECTED_IN_DEFINED_SCOPE.
* Sin resultados aplicables: NO_APPLICABLE_CONTROL_RESULT.

Ninguna etiqueta equivale a cobertura universal, veracidad del servicio, certificación, aceptación NAP o cumplimiento jurídico integral. La ausencia de límites declarados no demuestra por sí sola que se hayan identificado todas las brechas del formato.

La prioridad y el bloqueo de destino requieren contexto probado; una cifra de hallazgos no proporciona ese contexto.
