# Decision log

Registro de decisiones aprobadas. Los identificadores son estables y no se reutilizan. Cualquier cambio posterior se documentará mediante una nueva decisión que referencie la afectada, conservando su trazabilidad.

Todas las entradas siguientes tienen estado **APPROVED**, fecha **2026-09-27** y fuente **autorización explícita del usuario: BUSINESS PHASE 1 — DOCUMENT GOVERNANCE**. Su aprobación no constituye evidencia de capacidades técnicas ni de hipótesis comerciales.

| ID | Decisión aprobada |
| --- | --- |
| BUS-DEC-001 | El área Business queda físicamente aislada dentro de `07_Business`. |
| BUS-DEC-002 | Compliance y GTFS_Lab son las fuentes técnicas de verdad. Business no puede modificar ni sustituir esas fuentes. |
| BUS-DEC-003 | Ninguna capacidad podrá presentarse comercialmente como existente sin evidencia técnica verificable. |
| BUS-DEC-004 | Deben distinguirse explícitamente capacidades existentes, en desarrollo y planificadas, además de la condición pendiente de verificación. Esta condición no acredita existencia ni demostración técnica. |
| BUS-DEC-005 | La construcción empresarial se realizará progresivamente: governance → capabilities → market → offering → economics → legal/commercial → go-to-market. Cada fase requiere inicio formal autorizado; sus directorios no se crean anticipadamente. |
| BUS-DEC-006 | Transit Data Lab se adopta actualmente como WORKING NAME. No se registra como marca registrada, nombre societario definitivo ni denominación jurídicamente disponible. Su disponibilidad deberá verificarse formalmente antes de una decisión definitiva de marca. |
| BUS-DEC-007 | El desarrollo comercial no debe condicionar ni alterar resultados, requisitos, evidencias o conclusiones técnicas de Compliance o GTFS_Lab. |
| BUS-DEC-008 | El objetivo empresarial inicial es explorar la futura comercialización de servicios/productos relacionados con calidad, validación, auditoría y compliance de datos de transporte público, sujeto siempre a capacidades técnicamente demostradas. |

## Autorización de Business Phase 2

Las entradas siguientes tienen estado **APPROVED**, fecha **2026-09-27** y fuente **autorización explícita del usuario: AUTORIZADO — BUSINESS PHASE 2: CAPABILITY BASELINE**. Conservan las decisiones iniciales; no suponen aprobación del inventario resultante ni de sus afirmaciones por parte del usuario.

| ID | Decisión aprobada |
| --- | --- |
| BUS-DEC-009 | Business Phase 1 se considera completada según declaración del usuario y se autoriza iniciar Business Phase 2 — Capability Baseline. Revisa el límite temporal de BUS-DEC-005: se habilita 02_Capabilities, sin habilitar ninguna fase posterior. |
| BUS-DEC-010 | Se autoriza lectura read-only de GTFS_Lab, Compliance y documentación técnica relacionada. Toda escritura queda exclusivamente en 07_Business: crear los tres documentos de capacidades y actualizar BUSINESS_STATUS, DECISION_LOG y ASSUMPTIONS_REGISTER únicamente cuando corresponda. No corregir hallazgos técnicos ni ejecutar herramientas que alteren fuentes o artefactos. |
| BUS-DEC-011 | Clasificar capacidades exclusivamente como EXISTING, IN_DEVELOPMENT, PLANNED o PENDING_VERIFICATION, vinculadas a evidencia exacta y limitaciones. No inferir capacidad por intención, documentación, código aislado, datasets o infraestructura. Las afirmaciones defendibles deben ser conservadoras y no convertir Compliance en certificación o garantía jurídica. |
| BUS-DEC-012 | Mantener PHASE: BUSINESS PHASE 2 — CAPABILITY BASELINE y STATUS: IN PROGRESS. Entregar inventario, índice y gaps, verificar alcance con git status/diff, no hacer commit ni iniciar Business Phase 3; esperar autorización. |

## Congelación de Business Phase 2 — V1

Fecha: **2026-09-27**. Fuente: **petición explícita del usuario BUSINESS PHASE 2 — BASELINE REVIEW AND FREEZE**, autorización de congelación condicionada a revisión satisfactoria. Condición verificada: **BUSINESS_PHASE_2_BASELINE_REVIEW = PASS** en [BASELINE_REVIEW_V1.md](../02_Capabilities/BASELINE_REVIEW_V1.md), con resultados completos y resolución del comparador hexadecimal conservados en review_v1. No se registra aprobación jurídica o comercial externa.

| ID | Estado | Decisión |
| --- | --- | --- |
| BUS-DEC-013 | APPROVED — condición verificada | Congelar [BUSINESS_CAPABILITY_BASELINE_V1](../02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md): 20 capacidades, distribución 11 EXISTING / 2 IN_DEVELOPMENT / 4 PLANNED / 3 PENDING_VERIFICATION, 28 evidencias y 76 rutas. Describe evidencia disponible a 2026-09-27; NO constituye certificación, homologación ni garantía de cumplimiento normativo. No acredita catálogo comercial, producto terminado o readiness comercial. |
| BUS-DEC-014 | APPROVED | Revisa exclusivamente el estado temporal de BUS-DEC-012: BUSINESS_STATUS pasa de IN PROGRESS a FROZEN tras revisión satisfactoria. BUSINESS_CAPABILITY_BASELINE_V1 = FROZEN; Business Phase 3 = NOT STARTED. Continúan las restricciones de escritura Business, sin producto técnico, mercado, pricing, servicios, contenido comercial o commit. Esperar autorización. |
| BUS-DEC-015 | APPROVED | V1 y sus documentos integrantes no se modificarán silenciosamente. Cambios requieren nueva revisión documentada o V2 según magnitud, conservando V1 y sus huellas. La evolución técnica no actualiza automáticamente capacidades o afirmaciones comerciales: exige nueva verificación Business. Permanecen los cuatro FAIL del sentinel y las limitaciones Compliance/GIS/piloto. |

## Autorización Business Phase 3 — Market Evidence

Fecha: **2026-09-27**. Fuente: autorización adjunta explícita del usuario **AUTORIZADO — BUSINESS PHASE 3: MARKET EVIDENCE**. Registra alcance autorizado, no aprobación del dossier resultante. Revisa límites temporales BUS-DEC-012/014; mantiene BUS-DEC-002/003/007/015. Prevalece sobre texto temporal inicial de AGENTS.md, conservado sin cambios.

| ID | Estado | Decisión |
| --- | --- | --- |
| BUS-DEC-016 | APPROVED | Iniciar Phase 3; Internet e investigación autorizados, escritura exclusivamente Business, habilitar 03_Market y siete documentos. V1 FROZEN; sin producto técnico. |
| BUS-DEC-017 | APPROVED | Priorizar España y TUVISA; diferenciar compra/presupuesto/adjudicación/pagos y contratos mixtos. Fuentes primarias y límites; importe individual no precio de mercado. |
| BUS-DEC-018 | APPROVED | Revisar ASM-001–008 con UNTESTED/PARTIALLY_SUPPORTED/SUPPORTED/CONTRADICTED. AGENTS.md no enumera estados: no cambiar gobierno. Matriz solo 11 EXISTING con límites V1. |
| BUS-DEC-019 | APPROVED | PHASE 3 y STATUS IN PROGRESS; entregar PASS/INSUFFICIENT y esperar revisión/autorización. Sin precios/paquetes/oferta/landing/pitch/CRM/contacto/emails/PMF/commit/Phase 4. |

Resultado del agente (**no decisión adicional aprobada**): BUSINESS_PHASE_3_MARKET_EVIDENCE = PASS para evaluación A–G; 36 entradas, ocho PROC, 15 segmentos, diez problemas, 11 proveedores/actores y cinco alternativas gratuitas. Gaps potenciales no validados; opciones/contratos mixtos separados. [Dossier](../03_Market/MARKET_GAPS.md) y [verificación](../03_Market/evidence/verification.json). No aprobación comercial/jurídica del usuario ni cierre Phase 3 inferidos.

## Autorización de commercial validation readiness review — 2026-09-27

Fuente: petición explícita adjunta del usuario BUSINESS PHASE 3 — MARKET EVIDENCE / COMMERCIAL VALIDATION READINESS REVIEW. Revisa siguiente paso BUS-DEC-019; conserva V1 y BUS-DEC-002/003/007/015. No autoriza experimentos/Phase 4.

| ID | Estado | Decisión autorizada |
| --- | --- | --- |
| BUS-DEC-020 | APPROVED (alcance de trabajo) | Revisar diez PROB, ocho PROC, 36 evidencias, once EXISTING, cuatro gaps y ocho ASM; siete artefactos y gobierno necesario, solo Business; sin repetir investigación/verificación global. |
| BUS-DEC-021 | APPROVED (restricción) | Prohibir hash global por defecto y detener antes de umbrales según RESOURCE_USAGE_POLICY.md. Phase 3 IN_PROGRESS, V1 FROZEN; sin precios/código/outreach/leads/pilotos ejecutados/commit/Phase 4. |

Resultado del agente, no aprobación de experimentos/cierre: BUSINESS_PHASE_3_VALIDATION_READINESS = PASS según evidencia íntegra en readiness_review. Un candidato PROB-001, seis HOLD, tres NO; diferenciación UNPROVEN, customer validation/WTP ausentes, ASM sin cambios. [Gate](../03_Market/BUSINESS_PHASE_3_VALIDATION_GATE.md). Próxima autorización de ronda limitada según plan, no concedida aquí.

## Business Master Roadmap — 2026-09-27

Fuente: secuencia BUSINESS MASTER ROADMAP definida explícitamente por el usuario. Conserva los límites de BUS-DEC-019/020/021; adopta el recorrido, sin autorización de ejecución ni aprobación de gates.

| ID | Estado | Decisión |
| --- | --- | --- |
| BUS-DEC-022 | APPROVED (roadmap) | Adoptar [BUSINESS_MASTER_ROADMAP.md](BUSINESS_MASTER_ROADMAP.md): Stage 1 Customer Discovery Preparation → Stage 2 Customer Discovery Evidence → Stage 3 Problem / Solution Fit Assessment → Stage 4 Pilot Design → Stage 5 Pilot Evidence → Stage 6 Commercial Validation → Stage 7 Offer & Pricing → Stage 8 Go-to-Market → objetivo PRIMER CLIENTE. HUMAN GATE entre etapas; Stage 2 requiere entrevistas reales y Stage 5 piloto real. |

Los Stages no renumeran las Business Phases históricas ni autorizan su inicio/cierre. Preparación de Stage 1 disponible, aprobación humana pendiente; Stage 2 sin autorizar. V1 FROZEN, Phase 3 IN_PROGRESS; sin entrevistas, pilotos, oferta, precios ni outreach ejecutados por esta decisión.

## Autorización exclusiva de Stage 1 — 2026-09-27

Fuente: petición explícita del usuario «AUTORIZADO — BUSINESS MASTER ROADMAP — STAGE 1 ONLY». Revisa exclusivamente la falta de autorización de ejecución de Stage 1 tras BUS-DEC-022; conserva prohibiciones y baseline.

| ID | Estado | Decisión autorizada |
| --- | --- | --- |
| BUS-DEC-023 | APPROVED (alcance de trabajo, no gate) | Preparación y ejecución documental exclusivamente de Stage 1 conforme al roadmap aprobado; preparar STAGE_1_GATE_REVIEW para decisión humana APPROVE / REWORK / HOLD / STOP. Sin reinterpretar el roadmap, sin modificar V1/producto, validar mercado, contactar terceros, entrevistas, leads, pilotos, pricing o commit. Stage 2 NOT AUTHORIZED; Phase 3 IN_PROGRESS y V1 FROZEN; no renumerar Business Phases. |

Resultado del agente, no decisión humana: STAGE_1_EXECUTION = INCOMPLETE; GATE_READINESS = NOT_READY_FOR_HUMAN_GATE. [Review](../03_Market/STAGE_1_GATE_REVIEW.md) documenta carencia de criterios de entrada/salida y evidencia requerida específica en roadmap. No contradicción directa identificada; no se completa la carencia por interpretación. Preparación documental reutilizada, ASM sin cambios y ninguna evidencia externa nueva. HUMAN_GATE_DECISION = PENDING. Solicitar decisión humana sobre criterios; no registrar APPROVE/REWORK/HOLD/STOP sin recibirla.

## Amendment aprobado — criterios Stage 1, 2026-09-27

Fuente: autorización explícita del usuario «AUTORIZADO — BUSINESS MASTER ROADMAP AMENDMENT — STAGE 1 ENTRY / EXIT / EVIDENCE CRITERIA». Revisa exclusivamente Stage 1 de BUS-DEC-022 y resuelve la carencia detectada al ejecutar BUS-DEC-023. La primera ejecución INCOMPLETE y su review/verificación permanecen conservados. Criterios incorporados después de detectar ausencia de requisitos verificables; no aprobación retroactiva de ejecución ni gate.

| ID | Estado | Decisión aprobada |
| --- | --- | --- |
| BUS-DEC-024 | APPROVED (amendment y reevaluación, no gate) | Denominar Stage 1 DESK MARKET DISCOVERY / EVIDENCE BASELINE e incorporar al roadmap S1-ENTRY-01–03 y S1-EXIT-01–12 obligatorios, calidad/independencia/diversidad, prioridad de fuentes y trazabilidad regulatoria. Reevaluar primero las 36 fichas y corpus existente sin investigación externa adicional; usar PASS/FAIL/INSUFFICIENT_EVIDENCE/NOT_APPLICABLE justificado sin omitir obligatorios. Si hay carencias, crear STAGE_1_EVIDENCE_GAP_PLAN con los cinco campos autorizados; solo si todos pasan declarar COMPLETE/READY_FOR_HUMAN_GATE con gate PENDING_HUMAN_DECISION, nunca aprobado por el agente. No modificar V1/producto, iniciar Stage 2, contactar terceros, entrevistar, fijar pricing, afirmar validación comercial o hacer commit. |

Resultado del agente, no decisión aprobada: [reevaluación](../03_Market/STAGE_1_CRITERIA_REEVALUATION.md) = 14 PASS / 1 INSUFFICIENT_EVIDENCE (S1-EXIT-09). STAGE_1_EXECUTION = INCOMPLETE; GATE_READINESS = NOT_READY_FOR_HUMAN_GATE; STAGE_1_GATE = NOT_REACHED. [Plan de gaps](../03_Market/STAGE_1_EVIDENCE_GAP_PLAN.md). Ausencia de criterios resuelta; tercer gap externo insuficientemente delimitado. No investigación nueva ni cambios ASM. Esperar decisión humana, Stage 2 NOT AUTHORIZED; Phase 3 IN_PROGRESS y V1 FROZEN. Verificación documental en stage_1_amendment, separada de los resultados históricos.
