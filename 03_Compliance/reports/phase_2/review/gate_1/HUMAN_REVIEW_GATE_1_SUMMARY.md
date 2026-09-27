# HUMAN REVIEW GATE 1 — EU-REG-2017-1926

Propuesta documental de decisiones para revisión humana. Estos reports no son datos normativos definitivos. La base se consultó en modo read-only; no se materializaron requirements, deadlines, mappings ni audit rules.

## Baseline

- Candidates: 34 (esperado 34)
- Estados actuales: 3 APPROVED, 31 NEEDS_REVIEW, 0 REJECTED (coincide)
- Decisions propuestas: {"APPROVE_AS_IS": 13, "SPLIT": 5, "HOLD_EXTERNAL": 7, "APPROVE_WITH_CHANGES": 9}

## Simulación atómica

- Requirements atómicos propuestos: 43
- Children de candidatos SPLIT: 14
- Candidatos SPLIT: 5
- Status READY / WAITING_EXTERNAL / WAITING_HUMAN / REJECTED: {'READY': 22, 'WAITING_HUMAN': 14, 'WAITING_EXTERNAL': 7}

## Condiciones

- Candidates is_conditional=TRUE: 13
- Con condition_text propuesto: 13
- Nota: condiciones derivadas de SOURCE FACT; las condiciones de artículo 4, apartado 3 conservan sus excepciones textuales y ámbitos.

## Dependencias externas detectadas

- Registros: 7
- Documentos distintos: 5
- Blocking: {'PARTIAL': 7}
- Todas se clasifican PARTIAL porque la obligación principal es reconocible pero su alcance técnico, definición o marco temporal requiere la fuente externa. No se han consultado ni interpretado esas normas.

## Fechas y referencias temporales

- Reconciliación temporal: 12 = conteo inicial del dossier; 13 = conteo reconciliado tras Gate 1 (10 con fecha explícita y 3 con expresiones funcionales). Se añade A08-P01-001 porque su SOURCE FACT también contiene «en un plazo que permita la reutilización fiable y efectiva». Las 5 expresiones funcionales están en 3 candidatos; no se convierten en DATE. Referencia externa de calendario: 1 en A10-P02-001 (Directiva 2010/40/UE, artículo 17, apartado 3), categoría separada.
- Fechas explícitas: 10
- Expresiones temporales funcionales: 5 en 3 candidatos ("sin demora"; en A06, "plazo que permita su utilización fiable y efectiva", "con antelación" y "oportunamente"; en A08, "plazo que permita la reutilización fiable y efectiva").
- Referencias a calendario externo: 1 (Directiva 2010/40/UE, artículo 17, apartado 3; periodicidad no interpretada).
- Las fechas están documentadas con scope, referencia de anexo cuando consta, ámbito geográfico, excepciones y provision fuente. No se transformaron expresiones funcionales en fechas.

## Artículo 9

Se propone registrar por separado la potestad de las autoridades de solicitar documentos del apartado 2. El verbo de potestad no se convierte en obligación general de titulares/proveedores. Candidate no creado en la base.

## Conflictos y anomalías

- HUMAN_DECISION_CONFLICTS: 0 tras reconciliación. A04-P01-004 conserva HOLD_EXTERNAL y dependency_blocking_level=PARTIAL; su remisión al artículo 7 de la Directiva 2007/2/CE requiere contexto externo y no contradice la decisión humana. Se elimina únicamente el flag documental HUMAN_DECISION_CONFLICT.
- Anomalías Annex 1.3 B-I y D-I: se mantienen sin corregir, renumerar ni usar como fundamento interpretativo.
- SQL de materialización, mappings y audit rules: no creados.

## Integridad / estado

- Base SHA-256 before/after observado: ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668
- DB unchanged respecto a la lectura inicial: YES (huella antes y después idéntica). project_baseline.json contiene 52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5, correspondiente a Phase 1. No es un fallo de integridad de DB; no actualizar el baseline hasta el cierre formal de Phase 2.
- Git antes: raíz ya presentaba archivos no rastreados; el detalle estaba compuesto por `.gitignore`, `02_Data_Engineering/`, `03_Compliance/`, `PROJECT_CURRENT_STATE.md`, `project_baseline.json`, `reports/`.
- Git tras generación: el estado raíz mantiene los mismos elementos no rastreados de entrada; los ocho reportes nuevos quedan dentro de `03_Compliance/`, ya no rastreado por Git. No se hizo git add, commit ni push.

## Reconciliación y estado de Gate 1

- Propuestas pendientes documentales Article 9: 2 (9(2) PROCEDURAL_POWER, potestad de solicitar documentos; 9(3) VERIFICATION, comprobaciones aleatorias obligatorias sobre declaraciones de 9(2)(c)). Se detallan en MISSING_CANDIDATES_V2.csv; no se insertaron filas en DuckDB. MISSING_CANDIDATES_V1.csv se conserva intacto como evidencia histórica.
- 9(2) conserva las cuatro categorías documentales a)–d) del texto consolidado a 04/03/2024. 9(3) no se amplía a frecuencia, porcentaje, método, sanciones ni documentación adicional. No se crearon audit.rules.
- Reconciliación documental: GATE_1_RECONCILIATION.md y GATE_1_RECONCILIATION.csv.
- GATE_1_RECONCILIATION = PASS
- HUMAN_REVIEW_GATE_1 = CLOSED
- READY_FOR_HUMAN_REVIEW_GATE_2 = YES

Esto no congela Phase 2, no materializa requirements ni deadlines, no evalúa cumplimiento legal ni realiza mappings.

## Validaciones de propuesta

- 34 candidatos únicos representados una vez: PASS
- Todas las decisiones declaradas aparecen en la matriz: PASS
- Todos los SPLIT tienen hijos: PASS
- Todos los conditionals tienen condición propuesta: PASS
- Dependencias externas inventariadas: PASS
- Requisitos con source traceability: PASS
- Fundamentos B-I/D-I: ninguno
- DuckDB: solo consultas read-only

## Autoría

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
