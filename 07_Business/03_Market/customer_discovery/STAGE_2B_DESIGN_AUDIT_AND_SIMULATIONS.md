# Stage 2B — auditoría del diseño y simulaciones sintéticas

**Estado:** auditoría documental y fixtures sintéticos; ninguna entrevista real. **V1:** FROZEN. **Contacto externo:** NOT_AUTHORIZED.

## Resultado de auditoría

| DESIGN-CHECK-ID | Resultado | Evidencia | Riesgo | Corrección requerida / aplicada |
|---|---|---|---|---|
| DC-01 Cobertura RQ-01–20 | PASS | INTERVIEW_GUIDE contiene 20 IDs explícitos y la plantilla permite anotar cobertura por RQ. | Cobertura formal podía confundirse con preguntar cada inciso literal. | Se aclaró la lista de cobertura y el uso semiestructurado en INTERVIEW_GUIDE. |
| DC-02 BUS-ASM relevantes | PASS | HYPOTHESIS_TEST_MATRIX mapea ASM-001/002/003/004/008 a RQ/cohortes, evidencia favorable y adversa. ASM-005/006/007 quedan fuera por alcance. | Preguntas de gasto pueden obtener conocimiento indirecto. | Mantener marca directa/parcial/indirecta y no cambiar estados por recuento. |
| DC-03 GAP-001/002/005 falsables | PASS | La matriz especifica resultados que confirman, limitan o contradicen; GAP-005 exige comparación real y conserva MEDIUM. | Preguntas podrían presuponer que existe gap. | Preguntar por flujo/último caso sin nombrar gaps; buscar caso completo resuelto o irrelevante. |
| DC-04 Neutralidad | PASS | Preguntas sobre casos recientes y alternativas; no revelar gaps antes del bloque neutral. | La revelación opcional al final puede primar opiniones posteriores. | Mantenerla solo después del discovery y etiquetar toda respuesta posterior como opinión/hipotética. |
| DC-05 Conducta frente a hipotético | PASS | Se priorizan último ciclo, última incidencia, compra ejecutada, recursos y workaround. | Algunos participantes no tienen conocimiento directo de compra. | Preguntar solo si conocen el caso; marcar no sabe/no aplica. |
| DC-06 Evidencia negativa | PASS | Guía pregunta por avisos inocuos, alternativa suficiente y problemas no resueltos; plantilla exige contraevidencia. | Sesgo del entrevistador al sondear casos positivos. | La simulación SIM-04 comprueba explícitamente salida negativa sin persuasión. |
| DC-07 Clases de evidencia | PASS | DISCOVERY_SCORING_RULES separa PRIMARY-BEHAVIOR/SPEND/PROBLEM/WORKAROUND/PROCESS/OPINION/HYPOTHETICAL y FACT/OPINION/INTERPRETATION/HYPOTHESIS. | Tabla de captura tiene `FACT` sin subcampo para observed frente a reported. | La procedencia/atribución se conserva en columnas de evidencia y se reitera en simulaciones; no elevar relato a observado. |
| DC-08 Duración | WARNING → CORREGIDO | La suma anterior permitía 33–42 min antes de transiciones; duración declarada 25–40. | Sesgo por cortar procurement, alternativas o contraevidencia. | Agenda revisada: 33 min nominales / 38 min de topes agregados; guía indica omitir repeticiones, respetar límite y marcar RQ fuera de competencia. Probar con personas reales solo tras autorización. |
| DC-09 Consentimiento y privacidad | WARNING / BLOQUEO PREVIO A CAMPO | Plan requería definir retención “antes” de entrevistas pero no daba aviso, responsable/base ni campo de aceptación de notas. | Recoger datos sin información completa o conservar notas indefinidamente. | Guía/plan ahora exigen aviso aprobado, plazo, responsable/base/derechos y aceptación separada antes de recoger datos. Pendiente revisión de privacidad y completar aviso/plazo antes de cualquier campo. |
| DC-10 Gate definido antes de entrevistas | PASS | STAGE_2_GATE_CRITERIA establece umbrales, resultados, límites y decisión humana antes de campo. | Umbrales altos podrían confundirse con representatividad estadística. | El documento advierte que no estima prevalencia; mantenerlo como elegibilidad para decidir, no validación de mercado. |
| DC-11 Muestra alcanzable en solitario | WARNING | Plan exige mínimo 12 (dos por seis cohortes), 8 organizaciones y 3 contextos; objetivo 18, tres olas. | 12 entrevistas y tres contextos pueden ser una carga elevada para una persona; la expansión geográfica puede ralentizar calibración. | Wave 1 se trata como pool de 6 organizaciones y no como 6 entrevistas completadas. Revaluar metas tras calibración con autorización; no relajar gate por conveniencia. |
| DC-12 Criterio no circular | PASS | Ningún umbral requiere confirmar hipótesis; se aceptan negativos y se separa gate de aprobación. | Un gate exigente puede seleccionar solo entrevistables favorables. | Registrar rechazos, no-respuesta y limitaciones de acceso, sin contarlos como evidencia de problema. |
| DC-13 Registro sin CRM | PASS | INTERVIEW_REGISTER vacío; captura sin nombre de entidad por defecto. | Confundir target research con leads. | Mantener roles/organizaciones para selección de aprendizaje; excluir score de venta, ingresos y pipeline. |
| DC-14 DIVULGACIÓN | PASS_WITH_WARNING | Guía contiene un mensaje factual sobre demostraciones acotadas. | Detalles prematuros alteran respuestas o pueden exagerar capacidades. | Disclosure por niveles queda separado en invitación y gate; revelar nivel B únicamente si preguntan y después del discovery. |
| DC-15 Seguridad de baseline/alcance | PASS | No se tocó producto, V1, registros de mercado, entrevistas, datos técnicos ni fase comercial distinta. | Cambios colaterales en documentos congelados. | Archivos nuevos/ajustes se limitan a customer_discovery; no commit. |

**Síntesis:** `DESIGN_AUDIT = PASS_WITH_WARNINGS`. Sin FAIL bloqueante de diseño para pasar a decisión humana, con dos pendientes materiales antes de cualquier trabajo de campo: validar privacidad/aviso/retención y probar duración con calibración autorizada.

## Simulaciones sintéticas (fixtures; no son evidencia)

Se redactaron cuatro perfiles contrafactuales para probar la guía. No representan entidades/personas reales y no deben copiarse a MARKET_EVIDENCE_REGISTER, INTERVIEW_REGISTER ni estados de hipótesis.

| ID | Fixture y respuestas sintéticas | Prueba y resultado | Ajuste/nota |
|---|---|---|---|
| SIM-01 | Operador público maduro: producción con sistema central y proveedor; validación automática, incidencias recientes trazadas; no recuerda gasto individual porque compra centralizada; aporta un caso de alerta inocua y proceso rutinario sin intervención. | RQ-01–09/13–19 contestables; procurement parcialmente fuera de competencia; evidencia directa separable de estimación. **Usable con enrutamiento por rol.** | No insistir en importes ni interpretar madurez como ausencia de trabajo. |
| SIM-02 | Operador pequeño/mediano externalizado: proveedor prepara/publica feeds; operador revisa cambios puntuales, desconoce reglas internas y precio; un retraso reciente corregido por proveedor, sin artefacto compartible. | Caso y ownership reconstruibles, pero validación/esfuerzo parcialmente conocidos. **Usable; marca límites y ofrece “no sabe”.** | Preguntar qué hizo personalmente, cuándo recibió resultado y qué observó; no atribuir labores del proveedor al operador. |
| SIM-03 | Autoridad/administración: fija obligaciones y consume entregables; usa validador de portal para controles de aceptación; no conoce el trabajo diario ni pagos de operador; conserva actas agregadas. | RQ-10–12 y operación de terceros no aplicables salvo experiencia directa. **Usable con `NOT_APPLICABLE` motivado.** | No exigir acceso a expediente o nombres; separar práctica, contrato y obligación legal referida. |
| SIM-04 | Proveedor ITS: relata flujo automatizado; indica que su validador y soporte actuales bastan, el problema no ocurre en cartera actual, carga adicional negligible, no asignaría recursos ni contrataría revisión adicional. No ofrece artefactos. | Evidencia adversa/opinión distinguible; no aparece pregunta que invite a refutarle ni réplica persuasiva. **Negativo capturable correctamente**; opinión de recursos no equivale a conducta de mercado. | Registrar como fixture únicamente; en campo pedir caso más reciente, confirmar alcance de “no ocurre” y parar si no hay caso. |

### Chequeos transversales

- Duración estimada por bloques: 33 min nominales; hasta 38 min en el guion revisado. Preguntas redundantes pueden omitirse; preguntas fuera de rol se marcan sin cobertura.
- Ambigüedad residual: `problema`, `validación` y `evidencia` varían por actor; comenzar pidiendo definición desde un ejemplo suyo y conservar su vocabulario, sin imponer el de TDL.
- Disclosure: no abrir con TDL ni afirmar certificación, universalidad, empresa establecida o solución validada.
- Clasificación: distinguir FACT reportado/observado, opinión, inferencia e hipotético; ningún fixture aporta evidencia.
- Privacidad: no cargar nombres, citas identificables, correos, teléfonos ni organización del supuesto participante; no generar grabaciones/transcripciones.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
