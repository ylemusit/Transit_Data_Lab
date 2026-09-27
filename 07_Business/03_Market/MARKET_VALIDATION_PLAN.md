# Plan de validación comercial — diseño, sin ejecución

## 1. Objective

Determinar si interpretar hallazgos GTFS estáticos aporta utilidad adicional al proceso existente de un actor real. Phase 3 sigue IN_PROGRESS; V1 FROZEN. Esta revisión permite diseño documental, sin entrevistas, pilotos, contactos, precios ni Phase 4.

## 2. Current evidence

36 MKT-EVD aceptadas conservadas; diez PROB; ocho PROC; once EXISTING; cuatro GAP; ocho ASM. [Matriz](COMMERCIAL_VALIDATION_READINESS.csv), [registro canónico](MARKET_PROBLEM_REGISTER.csv) y [gate con trazabilidad](BUSINESS_PHASE_3_VALIDATION_GATE.md). Sin investigación externa nueva. Niveles 5/6 ausentes; nivel 4 tampoco se asigna por falta de evidencia de encaje operativo transferible.

## 3. What documentary research established

Hallazgos públicos en Francia; compras de generación/mantenimiento/control/integración; actores identificables; presión normativa documentada; alternativas gratuitas y proveedores existentes. Avisos públicos no son ground truth ni tasas españolas. Seguimiento contractual es un requisito, no prueba de dolor insatisfecho.

## 4. What documentary research did NOT establish

Demanda suficiente por TDL, compra separada de diagnóstico, disposición a pagar, formato preferido, precio aceptable, repetición, ventaja competitiva, mercado escalable, coste del error o aplicabilidad jurídica por operador. No prueba de incumplimiento individual. Contratos nominales no son TAM/SAM/SOM ni ingresos TDL.

## 5. Candidate problems for validation

Solo **PROB-001**, limitado a interpretación de hallazgos de **GTFS Schedule**. RT/SIRI/NeTEx quedan fuera del concepto y del piloto V1. Selección no implica que un comprador francés o español quiera TDL.

- WHAT_WE_KNOW: MKT-EVD-017/018 muestran hallazgos; 020/021/022 y 019 ofrecen reportes gratuitos; 002/007 exigen controles e informes dentro de contratos mayores. CAP-003/004/019 acreditan controles específicos, consulta manual y comparación histórica.
- WHAT_WE_DO_NOT_KNOW: qué hallazgos requieren ayuda externa, quién los interpreta, coste/impacto, falsos positivos, cobertura interna, comprador ni transferencia a otra muestra sin desarrollo.
- WHAT_MUST_BE_TESTED: último hallazgo estático y consecuencias, pasos/responsables, suficiencia de herramientas actuales y utilidad incremental de explicar fuente/regla/resultado con incertidumbre.
- WHO_CAN_VALIDATE_IT: responsable de datos/calidad de operador, autoridad, integrador o consultora; equipo NAP como validador de flujo, sin presumir comprador. Identificar después al decisor presupuestario.
- WHAT_EVIDENCE_WOULD_CHANGE_OUR_DECISION: GO si casos documentados muestran dificultad pendiente y un responsable solicita evaluar ayuda acotada; HOLD si falta material o requiere funciones fuera V1; STOP si reportes/proveedor y equipo actual resuelven el problema sin dificultad material o utilidad adicional.

HOLD: PROB-002/005/006/007/008/009, sin incidencia específica observada suficiente. NO: PROB-003/004/010, fuera de cobertura funcional V1. Son hipótesis conservadas, sin experimentos independientes autorizados. Los cuatro gaps se revisan en el gate; no se declaran oportunidades.

## 6. Target validator/customer types

SEG-001 operadores bus; SEG-002 productores ferroviarios con GTFS estático; SEG-004 autoridades; SEG-008 equipos NAP/PAN; SEG-011 consultoras de datos; SEG-013 integradores. SEG-010/014 proveedores pueden validar flujos o resolverlos internamente; no asumir compra/colaboración. Roles, sin leads ni contactos. Usuario, corrector, aceptante y comprador pueden ser distintos.

## 7. Interview hypotheses

PROBLEM_INTERVIEW + WORKFLOW_INTERVIEW: hipótesis de que algunos avisos estáticos necesiten interpretación contextual adicional. Pedir último caso antes de mostrar TDL. Diseño pequeño propuesto: 3–5 entrevistas de 30–45 minutos en al menos dos organizaciones distintas con casos conocidos. Muestra exploratoria, sin estimar prevalencia ni mercado. [Guía neutral](CUSTOMER_DISCOVERY_INTERVIEW_GUIDE.md).

## 8. Pilot hypotheses

DOCUMENT_REVIEW: tras entrevista, revisar con permiso un reporte estático y descripción del proceso, preferentemente anonimizados. Sin ejecutar nuevos validadores ni cargar datos externos por defecto.

PILOT_AUDIT: solo tras demostrar relevancia, permiso escrito y comprobación previa read-only de que la muestra es compatible con EXISTING sin desarrollo, importación o alteración técnica no autorizados. Un caso estático, hallazgos acordados y explicación manual con procedencia/límites, contrastada con el reporte gratuito existente. Si exige funciones nuevas, detener y mantener HOLD. No SLA, corrección continua, auditoría jurídica completa ni RT.

Medir responsables, pasos/tiempo declarados y contrastables, discrepancias explicadas y falsas alarmas confirmadas por responsable. Utilidad no significa cumplimiento ni WTP. Acceso permitido, alcance aprobado y resultado aceptado son evidencias separadas.

WILLINGNESS_TO_PAY_INTERVIEW: posterior a problema/relevancia demostrados, comprador identificado y nueva autorización. No guion de precio ni cantidades ahora.

## 9. Evidence required

ID, fecha, organización/rol, permiso, caso/material, notas confirmadas, fuentes/reglas/versiones, impacto, alternativa vigente, objeciones, límites, resultado y revisión humana. [Modelo](COMMERCIAL_VALIDATION_EVIDENCE_MODEL.md). Conservar señales negativas igual que positivas.

## 10. Stop/go criteria

GO a revisión documental, con autorización, si al menos dos organizaciones independientes describen casos concretos y responsables confirman una tarea pendiente. Criterio exploratorio de diseño, no umbral estadístico ni demanda validada.

GO a piloto: permiso escrito, compatibilidad y utilidad adicional observable frente al proceso vigente. HOLD: falta caso/permiso/responsable o transferencia técnica. STOP: función ya resuelta sin dificultad material, incompatibilidad V1 o ausencia repetida de utilidad. Revisar cada experimento; no elevar automáticamente ASM/niveles.

## 11. Risks

Falsos positivos; sesgo francés/ferroviario e histórico vasco; entrevistados sin poder de compra; alternativas suficientes; corpus histórico; esfuerzo/costes manuales no medidos; datos sin permiso/licencia; confundir interés/piloto gratis con compra. Asturias WARNING 42 PASS/4 FAIL, export Kbus discrepante y mapping/audit sin resultados permanecen.

## 12. Next authorization required

Autorizar una primera ronda limitada de customer discovery: categorías/roles, número/canal de entrevistas, tratamiento/retención de notas y permiso de contacto. Nada ejecutado. Material real/piloto requieren alcance, datos y permiso explícitos más comprobación de capacidad. Precios, oferta, costes y Phase 4 siguen sin iniciar.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
