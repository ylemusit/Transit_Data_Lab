# Guía de entrevista semiestructurada

**Duración objetivo:** 30–38 minutos (bloques con tope agregado de 38). **Modo:** conversación neutral, una persona cada vez.
**No introducir Transit Data Lab durante el descubrimiento inicial. No vender ni preguntar si compraría/usaría algo.**

## Apertura y consentimiento (2 min)

«Gracias por conversar. Queremos entender cómo se producen, publican, validan y mantienen los datos de transporte en la práctica, incluidos los procesos que funcionan bien. No estamos evaluando su desempeño ni buscando venderle algo. Puede omitir preguntas o parar cuando quiera. Tomaremos notas con información mínima y la usaremos de forma agregada. No incluiremos citas identificables sin permiso separado. ¿Tiene alguna pregunta?»

Antes de tomar notas, explicar quién es responsable del tratamiento, finalidad, base y derechos/canal de contacto, destinatarios, plazo de conservación y uso agregado; entregar aviso de privacidad aprobado para la investigación y comprobar que la participación es voluntaria. Registrar aceptación para notas separadamente del consentimiento explícito y previo a cualquier grabación. Si no se ha aprobado el aviso/plazo o la persona no acepta notas, no recoger datos de entrevista. Si no hay consentimiento explícito para grabar, notas únicamente. No registrar datos confidenciales. La invitación inicial no solicitará información personal sensible ni detalles de casos identificables.

## 1. Rol y contexto (3 min)

- ¿Cuál es su función en los datos de transporte y qué parte del proceso toca personalmente?
- ¿Qué modos y formatos aparecen en su trabajo: GTFS, GTFS-RT, NeTEx, SIRI u otros?
- ¿Qué tarea reciente puede describir de primera mano?

## 2. Flujo actual (4 min)

- Recorra el último ciclo desde la fuente del dato hasta publicación/consumo. ¿Qué pasos hubo y quién se responsabilizó de cada uno?
- ¿Qué sistemas, archivos, transferencias o proveedores intervinieron?
- ¿Quién valida y en qué momento? ¿Qué se comprueba automáticamente y qué manualmente?
- ¿Qué evidencia queda guardada y quién puede recuperarla?

## 3. Último caso concreto y errores (6 min)

- ¿Cuál fue la última vez que detectaron un problema en un dataset o integración? ¿Cuándo, en qué etapa y cómo lo supo?
- ¿Qué observación concreta se hizo? ¿Era defecto confirmado, aviso de herramienta o discrepancia por resolver?
- ¿Qué pasó después, paso a paso? ¿Quién investigó, corrigió, volvió a validar y aceptó el resultado?
- ¿Qué ocurrió si el dato ya estaba publicado o consumido? ¿Hubo consecuencia medible/documentada?
- Cuénteme un caso reciente en que el validador encontró avisos que resultaron no ser problema o se resolvieron fácilmente.

Sondear recurrencia solo con periodo y denominador claros. No convertir anécdota en tasa.

## 4. Herramientas, trabajo y alternativas (5 min)

- ¿Qué herramientas y procesos usaron en ese caso? ¿Qué resolvió cada uno?
- ¿Qué parte fue automática y qué parte requirió revisión manual? ¿Cómo se mide o estima el tiempo?
- ¿Qué workaround utilizan? ¿Desde cuándo y quién lo mantiene?
- ¿Qué alternativa ya funciona suficientemente bien? ¿En qué condiciones?
- ¿Qué trabajo adicional producen los controles/reportes o qué trabajo evitan?

## 5. Responsabilidad, contratación y recursos (4 min)

- ¿Han recurrido a soporte externo para este tipo de tarea? Describa la última ocasión, alcance y motivo.
- ¿Qué se contrató realmente y qué se hizo internamente? ¿Conoce si se pagó o solo se presupuestó/procuró?
- En ese caso, ¿quién detectó la necesidad, definió requisitos, inició/tramitó la contratación, aprobó gasto y aceptó el resultado? No pedir nombres.
- Si no se externalizó, ¿qué decidió la organización y qué alternativa siguió?

No preguntar importes confidenciales ni asumir que valor adjudicado equivale a pago.

## 6. Regulación, reporting, cambios y formatos (4 min)

- ¿Qué requisito concreto genera tareas recurrentes? ¿Cómo saben que aplica a su función?
- ¿Qué reporte/evidencia conservaron la última vez y quién lo revisó?
- ¿Qué ocurre cuando cambia una fuente después de publicar? ¿Cómo se enteran y quién evalúa el impacto?
- ¿Qué pasa cuando conviven estático, tiempo real, NeTEx/SIRI u otros formatos? Cuente la última integración/discrepancia real.

No pedir opinión jurídica general; distinguir obligación conocida, requisito contractual, estándar y práctica interna.

## 7. Consecuencias y prioridad revelada (3 min)

- ¿Qué ocurrió concretamente por el último fallo o demora: retrabajo, retraso, reclamación, incumplimiento documentado u otra consecuencia?
- ¿Qué recursos dedicó realmente la organización para resolverlo: horas registradas, contrato, personal asignado o ninguno?
- ¿Qué problema parecido decidieron no resolver? ¿Por qué?

## 8. Cierre y seguimiento (2 min)

- ¿Qué he entendido mal o qué caso contradice el resumen?
- ¿Existe documentación no confidencial que usted quiera ofrecer voluntariamente, con permiso y condiciones claros? No solicitar envío automático.
- ¿Autoriza que le contactemos una vez para aclarar notas? Registrar permiso separado. No pedir presentaciones a terceros.

## Revelación neutral opcional — solo tras discovery

Si se requiere explicar el contexto: «Estamos diseñando investigación sobre métodos para revisar datos de transporte y conservar trazabilidad de hallazgos. En el proyecto existen demostraciones acotadas sobre baselines concretas; no acreditan validación universal, corrección continua ni cumplimiento jurídico». Después preguntar qué parte duplica o no encaja con el proceso descrito, qué evidencia la contradice y qué alternativa ya resuelve la tarea. No preguntar «¿lo compraría?», «¿lo usaría?», «¿le gusta?» ni precios. Opiniones posteriores se etiquetan PRIMARY-OPINION o HYPOTHETICAL, nunca como conducta.

## Mapeo explícito de las preguntas de investigación

| ID | Pregunta que debe quedar cubierta |
|---|---|
| RQ-01 | ¿Quién es operativamente responsable de los datos de transporte? |
| RQ-02 | ¿Cómo se producen actualmente GTFS, GTFS-RT, NeTEx, SIRI u otros datasets equivalentes? |
| RQ-03 | ¿Quién valida esos datos y en qué momento del flujo? |
| RQ-04 | ¿Qué herramientas y procesos se usan actualmente? |
| RQ-05 | ¿Qué errores o discrepancias ocurren en operaciones reales? |
| RQ-06 | ¿Cómo se descubren esos errores o discrepancias? |
| RQ-07 | ¿Qué sucede después de detectar un error? |
| RQ-08 | ¿Cuánto trabajo manual existe y cómo se mide o estima? |
| RQ-09 | ¿Qué actividades se externalizan y qué se conserva internamente? |
| RQ-10 | ¿Qué se ha comprado o contratado realmente para estas tareas? |
| RQ-11 | ¿Quién inicia o propone esa contratación? |
| RQ-12 | ¿Quién aprueba el gasto y quién acepta el resultado? |
| RQ-13 | ¿Qué requisitos regulatorios, contractuales o de reporting generan trabajo operativo? |
| RQ-14 | ¿Cómo se conserva la evidencia de validación, revisión o cumplimiento? |
| RQ-15 | ¿Cómo se detectan y gestionan cambios después de publicar? |
| RQ-16 | ¿Qué ocurre cuando coexisten varios estándares, formatos o consumidores? |
| RQ-17 | ¿Qué soluciones existentes resuelven bien el proceso? |
| RQ-18 | ¿Dónde añaden trabajo las soluciones o procesos actuales? |
| RQ-19 | ¿Qué consecuencias reales han causado fallos de calidad de datos? |
| RQ-20 | ¿Qué problemas han sido suficientemente importantes para dedicarles tiempo, dinero o personal? |

Marcar cada RQ como directa, parcial o sin evidencia y enlazarlo a afirmaciones concretas de la plantilla. «No sabe/no aplica/no hubo caso» es dato, no omisión.

## Cobertura sin alargar la sesión

La guía es semiestructurada: no se espera formular todas las viñetas literalmente. Usar la tabla RQ como lista de cobertura; pedir una respuesta breve o marcar `no sabe / no aplica / no ocurrió` cuando el relato ya cubra un RQ. No forzar una entrevista a cubrir RQ fuera del conocimiento del participante. Respetar el tope de 38 minutos; si un caso requiere más detalle, pedir permiso para una sesión posterior solo si existe autorización aplicable. Reservar al menos un sondeo explícito para cada RQ-05–08 y RQ-17–20, incluyendo alternativa suficiente, ausencia de trabajo/coste y decisión de no actuar.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
