# Business Master Roadmap

Fecha: 2026-09-27. Fuente: secuencia definida por el usuario.

Este roadmap fija el recorrido desde la preparación de customer discovery hasta el objetivo del primer cliente. Su adopción no autoriza iniciar etapas, ejecutar entrevistas/pilotos ni superar gates humanos.

| Stage | Etapa | Condición explícita | Transición |
| --- | --- | --- | --- |
| 1 | DESK MARKET DISCOVERY / EVIDENCE BASELINE | Investigación documental verificable; criterios obligatorios definidos abajo | HUMAN GATE antes de Stage 2 |
| 2 | Customer Discovery Evidence | Requiere entrevistas reales; el diseño documental no sustituye la evidencia | HUMAN GATE antes de Stage 3 |
| 3 | Problem / Solution Fit Assessment | Evaluación basada en evidencia de discovery | HUMAN GATE antes de Stage 4 |
| 4 | Pilot Design | Diseño del piloto, separado de su ejecución | HUMAN GATE antes de Stage 5 |
| 5 | Pilot Evidence | Requiere piloto real; un diseño o demo interna no sustituye la evidencia | HUMAN GATE antes de Stage 6 |
| 6 | Commercial Validation | Evaluación de evidencia comercial, sin inferirla de interés informal | HUMAN GATE antes de Stage 7 |
| 7 | Offer & Pricing | Oferta y precios solo después de superar el gate anterior | HUMAN GATE antes de Stage 8 |
| 8 | Go-to-Market | Ejecución dentro del alcance autorizado | Objetivo: PRIMER CLIENTE |

Cada HUMAN GATE exige una decisión humana explícita para continuar y su registro en DECISION_LOG. La preparación de documentación, un resultado PASS o el transcurso del tiempo no equivalen a esa decisión. Si el gate no se supera, no se avanza automáticamente.

## Situación actual

Hay preparación documental relevante para **Stage 1** en [MARKET_VALIDATION_PLAN.md](../03_Market/MARKET_VALIDATION_PLAN.md), [CUSTOMER_DISCOVERY_INTERVIEW_GUIDE.md](../03_Market/CUSTOMER_DISCOVERY_INTERVIEW_GUIDE.md) y [COMMERCIAL_VALIDATION_EVIDENCE_MODEL.md](../03_Market/COMMERCIAL_VALIDATION_EVIDENCE_MODEL.md). La revisión de readiness está documentada en [BUSINESS_PHASE_3_VALIDATION_GATE.md](../03_Market/BUSINESS_PHASE_3_VALIDATION_GATE.md).

Esto no declara Stage 1 completado ni su HUMAN GATE aprobado. **Stage 2 no autorizado:** no entrevistas reales ejecutadas ni customer validation disponible. El diseño preliminar de experimentos existente tampoco declara completado Stage 4 ni autoriza Stage 5.

Siguiente decisión humana: revisar la [reevaluación contra los criterios aprobados](../03_Market/STAGE_1_CRITERIA_REEVALUATION.md) y, si hay carencias, el [STAGE_1_EVIDENCE_GAP_PLAN](../03_Market/STAGE_1_EVIDENCE_GAP_PLAN.md). Stage 2 no autorizado. No outreach por la mera adopción o modificación del roadmap.

## Amendment aprobado — Stage 1 (2026-09-27)

Autoridad: autorización explícita del usuario «AUTORIZADO — BUSINESS MASTER ROADMAP AMENDMENT — STAGE 1 ENTRY / EXIT / EVIDENCE CRITERIA», registrada como BUS-DEC-024 en [DECISION_LOG.md](DECISION_LOG.md). Revisa el nombre y definición de Stage 1 de BUS-DEC-022; no cambia Stages 2–8 ni aprueba ningún gate.

Los criterios se incorporan después de detectar la ausencia de criterios verificables durante la primera ejecución. Se conserva íntegra la [primera revisión INCOMPLETE](../03_Market/STAGE_1_GATE_REVIEW.md) y su evidencia histórica; no se presenta como una ejecución completada retroactivamente.

### Definición

**STAGE 1 — DESK MARKET DISCOVERY / EVIDENCE BASELINE**.

Objetivo: establecer mediante investigación documental verificable que existe un contexto suficientemente relevante de problemas, sujetos afectados, contratación, regulación, alternativas y posibles gaps como para justificar investigación primaria mediante entrevistas.

Stage 1 NO valida demanda comercial, willingness to pay, intención de compra, product-market fit, pricing, aceptación del servicio, satisfacción ni buyer real.

### Entry criteria — todos obligatorios

| CRITERION | Requisito |
| --- | --- |
| S1-ENTRY-01 | BUSINESS_CAPABILITY_BASELINE_V1 debe estar FROZEN. |
| S1-ENTRY-02 | Business Phase 3 — Market Evidence debe estar iniciada. |
| S1-ENTRY-03 | Debe existir metodología documentada para clasificación, trazabilidad y calidad de evidencia externa. |

### Exit criteria — todos obligatorios para READY_FOR_HUMAN_GATE

| CRITERION | Requisito |
| --- | --- |
| S1-EXIT-01 | Identificar al menos 3 segmentos potenciales de cliente/actor respaldados por evidencia. |
| S1-EXIT-02 | Documentar al menos 5 problemas o necesidades diferentes relacionados con datos de transporte. |
| S1-EXIT-03 | Documentar al menos 3 evidencias independientes de contratación o gasto real relacionado. |
| S1-EXIT-04 | Al menos una contratación debe disponer de importe económico verificable mediante fuente fiable. |
| S1-EXIT-05 | Identificar al menos 3 proveedores o alternativas existentes relevantes. |
| S1-EXIT-06 | Identificar al menos una alternativa gratuita u open-source relevante. |
| S1-EXIT-07 | Documentar al menos 3 obligaciones, requisitos regulatorios o requisitos formales relevantes y trazables. Distinguir obligatoriamente LEGAL OBLIGATION, FORMAL REQUIREMENT, STANDARD, RECOMMENDATION y BEST PRACTICE. |
| S1-EXIT-08 | Relacionar al menos 5 capabilities EXISTING del BUSINESS_CAPABILITY_BASELINE_V1 con problemas/necesidades observados externamente. La relación NO convierte automáticamente la capability en servicio. |
| S1-EXIT-09 | Identificar al menos 3 gaps potenciales entre necesidades observadas y soluciones/alternativas existentes. Etiquetarlos como POTENTIAL GAP. No afirmar oportunidad comercial validada. |
| S1-EXIT-10 | Revisar las hipótesis Business afectadas y mantener explícitamente sin validar aquellas que requieran evidencia primaria. |
| S1-EXIT-11 | Generar las preguntas y objetivos de investigación que Stage 2 deberá contrastar mediante entrevistas reales. |
| S1-EXIT-12 | No debe existir afirmación de product-market fit, demanda validada, willingness to pay validado, buyer validado o pricing validado basada únicamente en Stage 1. |

### Suficiencia, calidad e independencia

Los umbrales numéricos representan mínimos de cobertura, NO prueba automática de suficiencia. La evidencia utilizada debe ser identificable, trazable, relevante, verificable y suficientemente independiente. No contar como evidencias independientes páginas que reproducen el mismo hecho, copias del mismo expediente, artículos derivados de una única fuente primaria o múltiples URLs de una misma contratación.

Prioridad de fuentes: (1) legislación oficial; (2) contratación pública oficial; (3) organismos públicos; (4) documentación oficial de estándares; (5) documentación directa de proveedores; (6) literatura académica; (7) fuentes secundarias fiables.

Cuando un criterio use múltiples evidencias, evitar que todas procedan innecesariamente de una única organización, expediente, geografía o fuente secundaria. La diversidad debe ser razonable para el criterio evaluado.

S1-EXIT-07 no exige tres leyes diferentes: pueden ser distintos requisitos verificables del marco aplicable, pero cada requisito debe tener trazabilidad independiente hasta su fuente primaria. La clasificación no convierte estándares, recomendaciones o buenas prácticas en obligaciones legales universales.

### Reevaluación, gaps y gate humano

La primera reevaluación utilizará las 36 fichas existentes y la evidencia actualmente recopilada, sin investigación externa adicional. Para cada criterio: PASS, FAIL, INSUFFICIENT_EVIDENCE o NOT_APPLICABLE. NOT_APPLICABLE requiere justificación y no puede evitar un criterio obligatorio.

Si existe FAIL o INSUFFICIENT_EVIDENCE, no iniciar Stage 2 y crear STAGE_1_EVIDENCE_GAP_PLAN con exclusivamente: criterio afectado, evidencia existente, evidencia faltante, tipo de fuente necesaria y pregunta que debe resolverse. No inventar evidencia faltante. Resultado: STAGE_1_EXECUTION = INCOMPLETE; GATE_READINESS = NOT_READY_FOR_HUMAN_GATE; STAGE_1_GATE = NOT_REACHED.

Solo si todos los ENTRY y EXIT pasan: STAGE_1_EXECUTION = COMPLETE; GATE_READINESS = READY_FOR_HUMAN_GATE; STAGE_1_GATE = PENDING_HUMAN_DECISION. El agente NO puede aprobarlo. Esperar decisión humana; esta modificación NO autoriza Stage 2.

Restricciones: no modificar BUSINESS_CAPABILITY_BASELINE_V1 ni producto técnico; no iniciar Stage 2, contactar terceros, realizar entrevistas, fijar pricing, afirmar validación comercial ni hacer commit.

## Relación con el gobierno existente

Los **Stages 1–8** de este roadmap son etapas del recorrido comercial; sus números no equivalen a las **Business Phases 1–7** históricas. La secuencia histórica y sus autorizaciones se conservan. No se renumeran fases, se crean directorios futuros ni se cierra Business Phase 3.

Business Phase 3 permanece IN_PROGRESS; BUSINESS_CAPABILITY_BASELINE_V1 permanece FROZEN. Sin cambios de capacidades, supuestos o afirmaciones de mercado validado. Cualquier trabajo futuro continúa limitado por evidencia técnica, permisos, recursos y autorización de su alcance. Primer cliente es un objetivo, sin garantía de resultado.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
