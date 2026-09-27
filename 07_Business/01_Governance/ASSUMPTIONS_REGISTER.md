# Assumptions register

Registro de hipótesis, no de hechos comprobados. Los identificadores son estables y no se reutilizan. Las ideas siguientes se registran para futura validación; no autorizan investigaciones ni decisiones comerciales en Fase 1.

Estado inicial histórico: **PENDING VALIDATION** para todas las entradas; fecha de registro **2026-09-27** y fuente **cuestiones señaladas por el usuario en la autorización de Fase 1**. La revisión Phase 3 siguiente conserva las hipótesis originales y registra evidencia/limitaciones antes de cambiar estados; no asigna precios ni valida viabilidad.

| ID | Hipótesis o cuestión pendiente | Validación futura requerida |
| --- | --- | --- |
| BUS-ASM-001 | Podría existir demanda suficiente para la futura oferta. | Comprobar la demanda en la fase de mercado autorizada. |
| BUS-ASM-002 | Operadores, autoridades o consultoras podrían estar dispuestos a pagar. | Verificar disposición a pagar sin presumirla por interés declarado. |
| BUS-ASM-003 | Podrían identificarse segmentos de cliente prioritarios. | Evaluar segmentos con evidencia antes de priorizarlos. |
| BUS-ASM-004 | Podría identificarse un modelo de prestación adecuado. | Contrastar alternativas con necesidades y capacidades demostradas. |
| BUS-ASM-005 | Podría definirse un pricing viable. | Validar el pricing en su fase autorizada; no hay precios establecidos. |
| BUS-ASM-006 | Los costes de operación podrían permitir una prestación viable. | Identificar y verificar costes; no hay estimaciones ni valores asignados. |
| BUS-ASM-007 | Podría determinarse una estructura jurídica/fiscal adecuada. | Evaluación formal futura en la fase correspondiente; no hay estructura elegida. |
| BUS-ASM-008 | Podría ser posible convertir partes del servicio en producto/software. | Verificar factibilidad técnica y empresarial antes de concluir o comprometer un producto. |

## Revisión Business Phase 3 — 2026-09-27

Estados autorizados: UNTESTED, PARTIALLY_SUPPORTED, SUPPORTED, CONTRADICTED. AGENTS.md no fija un enum de hipótesis ni exige modificación para introducirlos; se conserva intacto. Ninguna entrada VALIDATED. SUPPORTED exigiría evidencia sobre la hipótesis completa, no un contrato ajeno aislado.

| ID | Estado actual | Evidencia / conclusión | Qué falta |
| --- | --- | --- | --- |
| BUS-ASM-001 | PARTIALLY_SUPPORTED | Problemas y compras relacionados existen: MKT-EVD-001/006/018/030/031. | Demanda suficiente por V1, volumen recurrente y diferenciación. |
| BUS-ASM-002 | PARTIALLY_SUPPORTED | Operador y autoridades compran generación/mantenimiento/plataformas: PROC-001/002/006/007. | Pago por TDL, auditoría separada o consultoras como compradoras. |
| BUS-ASM-003 | PARTIALLY_SUPPORTED | 15 segmentos; compra más directa en operador municipal/autoridad. | Muestra española histórica/concentrada; prioridad comercial definitiva no establecida. |
| BUS-ASM-004 | UNTESTED | Contratos/SaaS/suscripción son alternativas observadas (MKT-EVD-025/028). | Adecuación de un modelo a TDL sin contrastar; no diseñar oferta Phase 3. |
| BUS-ASM-005 | UNTESTED | Valores contractuales no son pricing viable TDL. | Fase Economics autorizada y costes/alcance/compra verificados. |
| BUS-ASM-006 | UNTESTED | Costes TDL no medidos. | Costes completos y viabilidad sin inferir márgenes de contratos ajenos. |
| BUS-ASM-007 | UNTESTED | Normas de datos no eligen estructura jurídica/fiscal. | Evaluación formal en fase autorizada. |
| BUS-ASM-008 | UNTESTED | Alternativas software no verifican convertir TDL en producto. | Factibilidad/operación/derechos/viabilidad específicos. |

Apoyadas parcialmente: 001/002/003. SUPPORTED y CONTRADICTED: ninguna de las ocho hipótesis originales. La existencia de herramientas gratuitas descarta considerar diferenciación demostrada la mera ejecución de un validador; no sustituir una hipótesis original por esa proposición.

Fuentes: [registro](../03_Market/MARKET_EVIDENCE_REGISTER.md), [gaps y límites](../03_Market/MARKET_GAPS.md). Sin PMF, precios o cambios V1.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Revisión de readiness — 2026-09-27 (sin cambios de estado)

PROPOSED_STATUS_CHANGE = NONE. Sin error determinista de clasificación detectado. Contradicciones/límites siguientes describen obstáculos a interpretaciones amplias; no declaran CONTRADICTED la hipótesis original.

| ID | current_status | supporting_evidence | contradicting_evidence / límites | missing_evidence | next_validation_action |
| --- | --- | --- | --- | --- | --- |
| BUS-ASM-001 | PARTIALLY_SUPPORTED | 017/018 hallazgos; 001/006/030/031 compras | 020/019 alternativas gratuitas; 025/029 control humano/historial; contratos integrales no demanda TDL | Utilidad incremental, volumen/repetición | Entrevista PROB-001 tras autorización |
| BUS-ASM-002 | PARTIALLY_SUPPORTED | PROC-001/002/006/007 adjudicaciones ajenas | No compra separada de audit; gratuidad no demuestra rechazo a pagar | Comprador/relevancia TDL y compromiso específico | Identificar decisor después del caso; WTP posterior, sin precio ahora |
| BUS-ASM-003 | PARTIALLY_SUPPORTED | SEG-001/004 compras; SEG-002/008 hallazgos/flujo | Muestra histórica vasca/francesa; cobertura interna posible | Necesidad por rol y alternativas | Comparar relatos en organizaciones independientes |
| BUS-ASM-004 | UNTESTED | 025/028 modelos ajenos, sin soporte TDL | SaaS/mantenimiento exceden V1 | Formato útil y aceptación del trabajo acotado | Entrevista de flujo; no oferta Phase 4 |
| BUS-ASM-005 | UNTESTED | Ninguna evidencia de pricing viable TDL | Valores integrales incomparables con audit | Alcance/comprador/costes/compromiso | Diferir a fase autorizada, sin precio |
| BUS-ASM-006 | UNTESTED | Ninguna medición de costes TDL | Manualidad impide inferir eficiencia; sin refutación cuantificada | Costes completos/repetibilidad | Medición futura autorizada; sin estimación ahora |
| BUS-ASM-007 | UNTESTED | Sin estructura jurídica/fiscal elegida | Normas de datos no determinan estructura | Evaluación formal específica | Mantener pendiente de fase autorizada |
| BUS-ASM-008 | UNTESTED | Once EXISTING acotadas; software ajeno contextual | Core/engine/analítica/findings PLANNED; mapping/audit sin resultados | Transferencia/derechos/operación/viabilidad | Entrevista aclara tarea repetible, sin desarrollar/inferir producto |

Números abreviados = MKT-EVD. [Gate](../03_Market/BUSINESS_PHASE_3_VALIDATION_GATE.md), [plan](../03_Market/MARKET_VALIDATION_PLAN.md). Acciones propuestas, sin ejecución/aprobación comercial.
