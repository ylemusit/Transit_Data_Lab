# Criterios previos del gate de Stage 2

Fijados antes de las entrevistas. El gate evalúa suficiencia de evidencia para decidir el paso siguiente; no exige confirmar todas las hipótesis y no mide product-market fit. El agente/investigador prepara el dossier, pero no aprueba el gate. Hace falta decisión humana explícita registrada en DECISION_LOG para continuar.

## Estados

- **APPROVE:** evidencia primaria suficientemente diversa, trazable y contradictoria para justificar Stage 3 Problem / Solution Fit Assessment. No equivale a demanda validada ni autoriza Stage 3 hasta decisión humana.
- **REWORK:** defectos corregibles de calidad/cobertura/codificación; completar o revisar investigación solo tras autorización correspondiente.
- **HOLD:** evidencia incompleta o acceso insuficiente; preservar estado, aclarar dependencias y esperar decisión.
- **STOP:** evidencia consistente indica que el problema/relación investigada es irrelevante, está resuelta o no merece continuar dentro del alcance; requiere decisión humana y no se convierte en conclusión universal.

## Requisitos medibles de entrada a decisión

| Dimensión | Umbral para que APPROVE sea elegible | Regla de fallo |
|---|---|---|
| Muestra | ≥12 entrevistas válidas; ≥2 de cada cohorte A–F; ≥8 organizaciones independientes; ≥4 familias de rol y ≥3 contextos geográficos/regulatorios. | Por debajo: REWORK si subsanable; HOLD si no se autoriza/no se puede completar. |
| RQ | Cada RQ-01–20 con ≥4 entrevistas directas aplicables, en ≥2 cohortes, o `NOT_APPLICABLE` justificado con rol/alcance; al menos 16/20 con evidencia directa. | RQ crítico sin cobertura: REWORK/HOLD. No rellenar con fuentes secundarias. |
| Casos | ≥6 casos concretos PRIMARY-BEHAVIOR/PROBLEM de ≥4 organizaciones; incluir al menos 2 casos donde proceso funciona, problema está ausente, automatizado o alternativa basta. | Si solo hay relatos hipotéticos/opiniones, no elegible. |
| Procurement | Para cada afirmación de gasto: ≥3 organizaciones con evidencia PRIMARY-SPEND sobre tarea comparable, diferenciando contrato, servicio y pago. Si no se observa, registrar «no demostrado»; esto no bloquea por sí solo APPROVE. | No inferir compra de TDL ni bloquear por ausencia de gasto si la pregunta de Stage 3 puede resolverse con evidencia problema. |
| Segmentos | A–F cubiertos con participante de conocimiento directo y al menos una comparación de proceso entre tres cohortes. | No presentar ranking comercial a partir del tamaño de muestra. |
| Contradicciones | Matriz favorable/adversa completa para ASM-001/002/003/004/008 y GAP-001/002/005; revisión explícita de casos negativos; no omitir resultados que debiliten. | Hallazgos adversos omitidos o no resueltos: REWORK. |
| Calidad/consentimiento | 100% de fichas con metadatos mínimos, clase de evidencia, fuente/atribución, permisos y límites; cero grabaciones sin consentimiento explícito. | Incumplimiento material de consentimiento: HOLD y aplicar borrado/revisión; no usar la evidencia afectada. |
| Trazabilidad | Cada conclusión material enlaza a IDs de entrevista/claim; doble revisión interna de la síntesis y registro de disensos. | Conclusión sin trazabilidad: REWORK. |

Los umbrales son mínimos de revisión, no significación estadística. No hay requisito de que BUS-ASM quede SUPPORTED ni de que GAP se confirme. ASM-005/006/007 quedan fuera de decisión probatoria en Stage 2; no hacer pricing, modelo económico ni asesoramiento legal/fiscal.

## Reglas de decisión

1. **APPROVE elegible** si se cumplen muestra, cobertura, casos, consentimiento, contradicciones y trazabilidad, y el dossier formula una pregunta de decisión concreta para Stage 3. La decisión humana puede aun así elegir REWORK/HOLD/STOP.
2. **REWORK** cuando las carencias sean corregibles en el diseño/codificación o con una muestra adicional autorizada.
3. **HOLD** cuando existan lagunas materiales, restricciones de acceso/consentimiento o incertidumbre que impida elegir con rigor.
4. **STOP** solo si patrones independientes muestran que continuar la línea investigada no se justifica; incluir evidencia contraria y el alcance exacto. No generalizar más allá de la muestra.
5. Ningún resultado cambia Stage 2 a validado, autoriza contacto adicional o mueve a Stage 3 automáticamente. Registrar decisión humana y autorización siguiente por separado.

## Salida exigida al gate

Resumen de muestra real y desviaciones frente al diseño; cobertura RQ/cohortes/roles; casos independientes; tabla de evidencia favorable, adversa y neutra; estado propuesto (sin aplicar) de cada ASM/gap; consentimiento/retención; limitaciones/sesgos; pregunta de Stage 3 o razón para rework/hold/stop; decisión humana pendiente. Hasta entonces `HUMAN_GATE_DECISION = PENDING`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
