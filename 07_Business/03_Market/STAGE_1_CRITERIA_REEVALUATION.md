# Stage 1 — reevaluación de criterios aprobados

Fecha: 2026-09-27. Autoridad: [amendment del roadmap](../01_Governance/BUSINESS_MASTER_ROADMAP.md), BUS-DEC-024. Primera reevaluación exclusivamente del corpus existente; NEW_EXTERNAL_RESEARCH = NO; NEW_EXTERNAL_EVIDENCE = 0.

STAGE_1_EXECUTION = INCOMPLETE

GATE_READINESS = NOT_READY_FOR_HUMAN_GATE

STAGE_1_GATE = NOT_REACHED

Stage 2 = NOT AUTHORIZED. Business Phase 3 = IN_PROGRESS. BUSINESS_CAPABILITY_BASELINE_V1 = FROZEN. No gate aprobado por el agente. Se espera decisión humana sobre la carencia documentada, sin ejecutar investigación adicional.

## Método y trazabilidad

FACT — Reutilizadas las [36 fichas](STAGE_1_EVIDENCE_REUSE.md) MKT-EVD-001–036, su [registro](MARKET_EVIDENCE_REGISTER.md) y documentos derivados. Las 36 fichas no son 36 hechos independientes: 001–005 pertenecen a TUVISA; 006–007 a ATTG; original/consolidado BOE 011–012 a la misma ley; avisos sucesivos de Nantes a una contratación. No se actualizan fechas de consulta ni se certifica vigencia externa actual.

Los PASS siguientes evalúan requisitos documentales concretos y suficiencia para desk discovery; no son resultado automático del conteo ni del PASS histórico de Phase 3/readiness. Las fuentes oficiales conservadas soportan las afirmaciones acotadas; claims de proveedores solo acreditan oferta descrita. Fuentes sin copia íntegra, cobertura UE parcial, muestra histórica vasca y cifras dinámicas francesas conservan sus límites. No se infiere pago ejecutado de adjudicación, incidencia de requisito ni aplicabilidad jurídica individual.

## Matriz completa

| CRITERION | STATUS | EVIDENCE | GAP |
| --- | --- | --- | --- |
| S1-ENTRY-01 | PASS | [V1](../02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md): estado FROZEN; BUS-DEC-013/015 y BUSINESS_STATUS lo mantienen. | Ninguno para estado documental; no nueva certificación técnica ni hashes de V1. |
| S1-ENTRY-02 | PASS | BUS-DEC-016 autoriza inicio; [BUSINESS_STATUS](../BUSINESS_STATUS.md): PHASE 3 IN_PROGRESS. | Ninguno; Phase 3 no cerrada. |
| S1-ENTRY-03 | PASS | Registro: fuente/localizador/fechas/fiabilidad/límites/conservación; [modelo](COMMERCIAL_VALIDATION_EVIDENCE_MODEL.md): tipos y calidad; roadmap: independencia y diversidad. | Ninguno para metodología; no todos los originales están íntegramente conservados. |
| S1-EXIT-01 | PASS | [Segmentos](CUSTOMER_SEGMENTS.md): SEG-001 operador bus (001–005), SEG-004 autoridad (006/031), SEG-005 gestor municipal/metropolitano (030). También productor ferroviario SEG-002 (018). | Ninguno; actores respaldados por entidades distintas en España/Francia/Italia. Buyer TDL sin validar. |
| S1-EXIT-02 | PASS | [Problemas](PROBLEM_REGISTER.md): PROB-001 hallazgos (017/018); 002 mantenimiento (002/007); 003 coherencia estático/RT (002/007); 004 interoperabilidad (009/030); 006 adquisición/integración (008/031); 008 suministro/corrección (011/012). | Ninguno para ≥5 necesidades distintas; no prevalencia española, coste o incumplimiento individual medidos. |
| S1-EXIT-03 | PASS | [Contratación](PROCUREMENT_EVIDENCE.md): PROC-001 TUVISA (001/005), PROC-002 ATTG (006), PROC-006 Nantes (030), PROC-007 Roma (031). Cuatro expedientes, cuatro compradores, tres países. | Ninguno: adjudicación/contrato real relacionado; no pagos ejecutados ni compra separada a TDL. CTM/Puglia/Alicante no cuentan aquí. |
| S1-EXIT-04 | PASS | MKT-EVD-005, contrato TUVISA cláusula 3, pp. 2–3: 31.866,25 EUR sin IVA; [texto conservado](evidence/tuvisa_contract.txt). 006/030/031 aportan otros importes oficiales. | Ninguno; fechas divergentes TUVISA no invalidan el importe concordante. No pricing TDL. |
| S1-EXIT-05 | PASS | [Alternativas](COMPETITOR_LANDSCAPE.md): Datik (001–005), Ingartek (006/007), Okina (030), BIGO (031); también enRoute (025). | Ninguno: proveedores relacionados y diferenciados; no rendimiento auditado ni ranking. |
| S1-EXIT-06 | PASS | TOOL-001 MobilityData Canonical GTFS Schedule Validator, MKT-EVD-020/021/022; [README conservado](evidence/mobilitydata_readme.txt), Apache-2.0, reportes HTML/JSON. | Ninguno para alternativa documentada; sin ejecución/benchmark ni superioridad TDL. |
| S1-EXIT-07 | PASS | [Regulación](REGULATORY_DEMAND.md): OBL-001 art. 85.1/5; OBL-003 art. 86.1; OBL-004 anexo I.1.f. MKT-EVD-011/012, BOE conservado, tres localizadores distintos. Clasificación de cinco categorías debajo. | Ninguno para tres requisitos trazables; no exige tres leyes. No dictamen de vigencia/aplicabilidad ni uso de extractos UE incompletos como soporte único. |
| S1-EXIT-08 | PASS | [Matriz](MARKET_GAPS.md): TDL-CAP-001→PROB-006 (008/031); 002→005/007 (002/005/030); 003→001/003 (007/018/020); 004→001/006 (008/031); 011→007/008 (002/013). Los cinco figuran EXISTING en V1; matriz contiene once. | Ninguno para vínculo conceptual documentado; límites Asturias, revisión humana y SQL conservados. No servicios ni encaje demostrados. |
| S1-EXIT-09 | INSUFFICIENT_EVIDENCE | [Gaps existentes](MARKET_GAPS.md): GAP-001 y GAP-002 son POTENTIAL GAP externos con alternativas identificadas. GAP-003 es principalmente interno; GAP-004 no delimita una parte posiblemente no resuelta por alternativas multiformato. | Solo dos contrastes externos suficientemente delimitados. Falta un tercero; cuatro etiquetas no acreditan cobertura del criterio. [Plan](STAGE_1_EVIDENCE_GAP_PLAN.md). |
| S1-EXIT-10 | PASS | [ASM](../01_Governance/ASSUMPTIONS_REGISTER.md) y §6 de [revisión inicial](STAGE_1_GATE_REVIEW.md): 001–003 PARTIALLY_SUPPORTED; 004–008 UNTESTED. Revisión explícita debajo. | Ninguno para revisión; demanda/WTP/buyer/pricing siguen sin validar y requieren evidencia primaria o fases posteriores. |
| S1-EXIT-11 | PASS | [Guía](CUSTOMER_DISCOVERY_INTERVIEW_GUIDE.md), [plan](MARKET_VALIDATION_PLAN.md), §14 de revisión inicial y objetivos/preguntas debajo. | Ninguno para diseño de investigación; entrevistas reales ausentes y no autorizadas. |
| S1-EXIT-12 | PASS | Límites del corpus revisado, matriz, ASM y revisión inicial: ninguna conclusión positiva de PMF/demanda/WTP/buyer/pricing validados por Stage 1. | Ninguno para este control; términos de validación figuran como exclusiones o diseño futuro, sin validación comercial. |

Resultado: 14 PASS / 0 FAIL / 1 INSUFFICIENT_EVIDENCE / 0 NOT_APPLICABLE. Todos los criterios son obligatorios; no se usa NOT_APPLICABLE para omitir ninguno.

## Suficiencia por familia y clasificación regulatoria

SUPPORTED INTERPRETATION — Segmentación y necesidades tienen soporte en compras de varias entidades, hallazgos públicos y obligaciones específicas. Los seis problemas citados no son seis URLs del mismo hecho: mantenimiento, coherencia de identificadores, conversión, adquisición, hallazgos y suministro legal describen tareas diferentes. España aporta contexto contractual; Francia/Italia diversifican soluciones y necesidades, sin extrapolar su prevalencia.

FACT — Contratación se cuenta por expediente: TUVISA 2022; ATTG E3/2019/01; Nantes 22MB4/262, TED 272975-2023; Roma CIG 9072480F53, TED 560078-2022. [Nantes](evidence/ted_nantes_award.txt) distingue 660.810 EUR firmes de 795.310 EUR totales con opciones/máximo. [Roma](evidence/ted_rome_award.txt) publica 188.873,75 EUR sin IVA; [ATTG](evidence/attg_notice.txt), 60.000 EUR sin IVA. No sumarlos como mercado o pagos. Documentos sucesivos TUVISA/Nantes no incrementan el conteo.

| Clasificación obligatoria | Evidencia y alcance |
| --- | --- |
| LEGAL OBLIGATION | OBL-001: Ley 9/2025 art. 85.1/5, disponibilidad digital gratuita/no discriminatoria/actualizada; OBL-003: art. 86.1, datos de infraestructuras digitalizados; OBL-004: anexo I.1.f, actualizar cambios/corregir inexactos. Cada requisito remite a pasaje propio del [BOE original](evidence/boe_original.txt), contrastado en el corpus con [consolidado](evidence/ley9_consolidated.txt). Misma ley, tres requisitos, no tres fuentes legales independientes. |
| FORMAL REQUIREMENT | TUVISA PPT §§1–6 (002), envío semanal/informes/SLA de ese contrato; no obligación universal. |
| STANDARD | NeTEx/SIRI y perfiles (033/034/035); documentación técnica, sin obligatoriedad automática para cualquier actor. |
| RECOMMENDATION | Considerando 12 de 2024/490 según registro regulatorio: cooperación contextual; cobertura UE parcial, no contado para satisfacer los tres requisitos. |
| BEST PRACTICE | Reglas de buenas prácticas MobilityData (020/021); warning técnico no acredita infracción legal. |

## Evaluación de gaps sin inventar evidencia

| Gap del corpus | Tratamiento en S1-EXIT-09 | Necesidad frente a alternativa / límite |
| --- | --- | --- |
| GAP-001 | POTENTIAL GAP — contado | PROB-007/008 exige informes/justificantes (002/011/013). Hipótesis: revisión independiente con cadena fuente→regla→resultado. enRoute tiene historial (025), Ito control humano (029), Nantes indicadores (030). Podrían cubrirlo; separación/insuficiencia y compra no demostradas. |
| GAP-002 | POTENTIAL GAP — contado | PROB-001 hallazgos publicados (017/018) y contratos de corrección (002/007). Hipótesis: interpretación de hallazgos específicos fuera del reporte gratuito. MobilityData/PAN y proveedores son alternativas (019–023/025/029). Utilidad incremental y tarea residual no demostradas. |
| GAP-003 | No contado como gap externo | Corpus/engine/mapping incompletos de TDL describen carencia propia. Necesidad normativa sí observada, pero no se delimita una carencia potencial distinta de alternativas externas. |
| GAP-004 | POTENTIAL GAP — no contado por evidencia insuficiente | Coherencia estático/RT/multiconsumidor requerida (002/007/030), ya ofrecida por plataformas multiformato. El corpus no delimita un problema residual o diferencia de cobertura para construir un tercer contraste externo suficiente. TDL no acredita RT/NeTEx/SIRI. |

ASSUMPTION — Los dos gaps contados son preguntas de discovery, no déficits demostrados de competidores ni oportunidades validadas. UNKNOWN — Un tercer gap externo suficientemente delimitado. No se exige validación primaria del gap para Stage 1; falta su delimitación documental, no una entrevista para certificar oportunidad comercial.

## Hipótesis afectadas: revisión sin cambios

PROPOSED_STATUS_CHANGE = NONE. Registro ASM intacto.

| Hipótesis | Estado conservado | Resultado de reevaluación / validación pendiente |
| --- | --- | --- |
| BUS-ASM-001 | PARTIALLY_SUPPORTED | Problemas/compras relacionados; demanda suficiente específica por TDL sin validar. |
| BUS-ASM-002 | PARTIALLY_SUPPORTED | Compras ajenas no prueban WTP TDL; decisor, gasto separado y compromiso siguen sin validar. |
| BUS-ASM-003 | PARTIALLY_SUPPORTED | Segmentos exploratorios; prioridad definitiva requiere casos y roles reales. |
| BUS-ASM-004 | UNTESTED | Flujo/modelo de prestación adecuado sin validar; alternativas pueden bastar. |
| BUS-ASM-005 | UNTESTED | Pricing viable sin validar; fuera de Stage 1 y entrevistas diseñadas actuales. |
| BUS-ASM-006 | UNTESTED | Costes/viabilidad sin medir; ningún margen inferido de contratos. |
| BUS-ASM-007 | UNTESTED | Estructura jurídica/fiscal sin evaluar; no derivada de regulación de datos. |
| BUS-ASM-008 | UNTESTED | Producto repetible y transferible sin validar; software ajeno no lo demuestra. |

## Stage 2: objetivos y preguntas preparados, sin ejecución

| Objetivo de investigación primaria | Pregunta neutral / evidencia buscada |
| --- | --- |
| Confirmar problema y contexto propios | ¿Cuál fue el último hallazgo estático revisado y qué ocurrió? Caso/fecha/material autorizado; no extrapolar SNCF. |
| Reconstruir flujo, roles y aceptación | ¿Quién detectó, interpretó, corrigió y aceptó? Fuente, versión, regla y registro del cierre; usuario no equivale a buyer. |
| Contrastar GAP-001 y alternativas | ¿Cómo justifican discrepancias entre reportes y conservan versiones? ¿Qué resuelve el historial/control humano actual y qué, si algo, queda pendiente? |
| Contrastar GAP-002 y señales negativas | ¿Qué herramienta/proveedor resolvió el caso? ¿Qué parte, si alguna, fue difícil? Registrar también casos resueltos sin dificultad. |
| Distinguir frecuencia/esfuerzo declarado de medido | ¿Dónde registran casos similares y tiempo empleado? Sin convertir estimación en coste medido. |
| Identificar decisión y contratación observada | ¿Quién decide cambios y autoriza gasto? ¿Han contratado ayuda para esta tarea y qué incluía? Sin cantidades confidenciales, compra hipotética ni WTP validado. |
| Explorar utilidad incremental acotada | Después del caso: ¿qué duplicaría o aportaría una revisión estática limitada? ¿Qué resultado observable permitiría evaluarla? No prometer corrección, RT, compliance integral o servicio. |

La [guía existente](CUSTOMER_DISCOVERY_INTERVIEW_GUIDE.md) establece neutralidad, permisos y corrección de notas. Diseño no sustituye entrevistas; Stage 2 tampoco valida automáticamente PMF/WTP/pricing, que pertenecen a etapas posteriores. No ampliar entrevistas a GAP-004 ni ofrecer capacidades ausentes por esta reevaluación.

## Historia, restricciones y verificación

FACT — Primera ejecución: [STAGE_1_GATE_REVIEW](STAGE_1_GATE_REVIEW.md), INCOMPLETE por ausencia de criterios; verificación histórica conservada en stage_1_review. Amendment resuelve esa ausencia y esta reevaluación identifica una carencia distinta en S1-EXIT-09. No borra ni recalifica el intento anterior.

Escrituras exclusivamente Business: roadmap, DECISION_LOG, BUSINESS_STATUS, este informe, plan de gaps y paquete de verificación. Sin investigación externa nueva, producto técnico, baseline, ASM, contactos, entrevistas, pilotos, pricing o commit. [Verificación acotada](stage_1_amendment/verification.json) y [exit code](stage_1_amendment/exit_code.txt): estructura, IDs, referencias y coherencia; no aprobación humana ni nueva certificación global. Git agrupa untracked y diff vacío no demuestra inmutabilidad global. No hash global ni rerun histórico.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
