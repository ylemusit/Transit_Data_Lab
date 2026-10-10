# TDL-AUD-23 — validación de necesidad, compra y beneficio

Fecha: 2026-10-09. **PARCIAL: diseño listo; validación sin ejecutar.** Alcance exclusivo GTFS Schedule y NeTEx. Propietarios funcionales propuestos: Business e investigación de usuarios; sin personas ni plazos de ejecución asignados. Phase 3 IN_PROGRESS, baseline V1 FROZEN, contacto externo NOT_AUTHORIZED. Offering/Economics no iniciados.

Este protocolo complementa el [diseño de discovery](customer_discovery/README.md), su [matriz de hipótesis](customer_discovery/HYPOTHESIS_TEST_MATRIX.md) y las [reglas de evidencia](customer_discovery/DISCOVERY_SCORING_RULES.md). No reemplaza sus gates, cohortes o estados. Las audiencias del [registro de afirmaciones](TDL_GTFS_NETEX_CLAIMS_REGISTER_20261009.md) son hipótesis de destinatario. El [test de comprensión](../../reports/audit_quality_gate_v1/USER_STUDY_PROTOCOL.md) mide comprensión, no demanda o compra.

## Preguntas y decisiones que la evidencia debe permitir

| Dimensión | Pregunta neutral sobre un caso real | Evidencia requerida | Criterio de revisión / contraevidencia |
|---|---|---|---|
| Problema | «Describa la última publicación/corrección del fichero: qué ocurrió, quién actuó y qué consecuencia tuvo.» | Incidente fechado, formato/versión, tarea y procedencia; alerta separada de defecto confirmado | Investigar recurrencia con seis casos directos en al menos cuatro organizaciones y tres cohortes, según matriz vigente. Es indicio; no prueba demanda suficiente. Problema raro/sin consecuencia o ya resuelto debilita la necesidad. |
| Comprador | «¿Quién decidió, autorizó y pagó la última solución comparable?» | Roles de usuario, presupuesto, aprobación y contratación; distinguir relato, contrato y pago | Buscar tres organizaciones con contratación comparable y dos perspectivas de procurement, según matriz vigente. No convierte gasto ajeno en compra de TDL. Usuario sin poder de compra no es buyer confirmado. |
| Alternativa | «¿Cómo resuelven hoy esa tarea? ¿Qué funciona y qué queda pendiente?» | Validador gratuito/interno, proveedor, proceso manual, coste/tiempo observado y limitaciones | Comparar tarea/alcance equivalentes; registrar alternativas suficientes, no solo favorables a TDL. Una herramienta gratuita puede cubrir toda la necesidad del caso. |
| Compra y disposición a pagar | «¿Qué evidencia necesitó la última compra y qué restricciones impidieron externalizar?» | Comportamiento pasado y proceso decisorio verificable; no interés hipotético | En Phase 3 registrar contexto, sin preguntar precio ni ofrecer servicio. Una futura prueba de compromiso/precio necesita fase y autorización propias. No cambiar ASM-002/005 por opiniones positivas. |
| Beneficio | «¿Cómo miden hoy el esfuerzo y el resultado de corregir/publicar?» | Observación comparable antes/después, unidades y denominadores, recursos completos | Diseñar medición futura de tiempo, reintentos, defectos confirmados y aceptación de destinatario. Sin observación autorizada no publicar ahorro/ROI. Menor tiempo con mayor error no acredita mejora. |

## Ejecución y puertas

1. Antes del contacto: gate de privacidad y autorización, canal/aviso, consentimiento apropiado, materiales y versión, alcance y roles; grabación desactivada por defecto. Conservar el esquema de cohortes del discovery existente. No reclutar ni enviar desde esta tarea.
2. Recoger relatos de conducta pasada con guion neutral. Registrar cada organización/caso una vez; distinguir OBSERVED, REPORTED, OPINION e INTERPRETATION. Registrar evidencia negativa, permisos, recencia y límites. No pedir secretos ni documentos confidenciales.
3. Revisar cada dimensión por separado: SIN_EVIDENCIA / PARCIAL / APOYO / CONTRAEVIDENCIA; documentar soporte y huecos. Ningún recuento aprueba demanda, WTP o viabilidad automáticamente. Proponer revisión humana de hipótesis sin alterar ASM vigente.
4. Solo tras autorización posterior: diseñar piloto/prueba de compra con decisor, alcance, presupuesto, criterio de aceptación y compromiso real registrados. Un email de interés o uso gratuito no prueba pago. Pricing y condiciones no se fijan aquí.
5. Medir beneficio solo sobre tareas comparables y dentro de permisos/derechos acordados. Revisar resultados y problemas de interpretación; repetir tareas afectadas después de cambios de informe. El umbral UX 4/5 no sustituye evidencia de compra.

## Medición futura de beneficio

Unidad: un caso de publicación/corrección de una versión identificada, por formato y ámbito. Registrar esfuerzo inicial y con intervención en minutos-persona, reintentos, defectos confirmados, errores nuevos, completitud y aceptación real del destino. Documentar experiencia del equipo, tamaño/complejidad del fichero y cambios de alcance. Contrabalancear el orden o utilizar casos equivalentes para limitar aprendizaje; no repetir el mismo caso aprendido y atribuir toda mejora a TDL.

Diferencia de tiempo = esfuerzo de referencia − esfuerzo con intervención, incluyendo análisis, revisión, coordinación, corrección y reauditoría. Informar datos individuales y dispersión; una estimación declarada se conserva como estimación, no como tiempo observado. Coste evitado requiere coste unitario/recursos acreditados y costes completos de prestación. ROI exige beneficio atribuible y coste total medidos y fórmula explícita. Si falta una entrada, el resultado es **NO_MEDIDO**, nunca cero ni porcentaje inventado. No extrapolar una muestra pequeña a empresas o formatos no observados.

## Registro y salida

Registro de evidencias (evidencia local no publicada), actualmente vacío. Una entrada futura debe contener: ID estable, organización codificada/caso independiente, perfil/rol, formato, versión/fecha, dimensión, clase de evidencia, observado/declarado, soporte permitido, limitaciones, evidencia negativa, datos/unidades/denominadores, revisor y decisión. Datos personales y claves de identidad fuera del registro técnico, con acceso/retención acordados. Conservar versiones y correcciones; no sobrescribir la evidencia inicial.

Salida: matriz por dimensión y segmento, casos a favor/en contra, incertidumbre, próxima acción y decisión humana. Este cierre no tiene entrevistas, buyer confirmado, compra TDL, disposición a pagar, ahorro o ROI medidos. TDL-AUD-23 permanece PARCIAL hasta obtener evidencia primaria autorizada y completar su revisión.
