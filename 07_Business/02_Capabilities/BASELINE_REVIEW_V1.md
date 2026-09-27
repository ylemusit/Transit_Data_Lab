# Business Phase 2 — revisión final V1

Fecha: 2026-09-27. Resultado: **BUSINESS_PHASE_2_BASELINE_REVIEW = PASS**.

Revisión autorizada condicionalmente para congelar V1; no inicia Phase 3. Scope de escritura: 07_Business. Sin commit, producto técnico, investigación externa, precios, servicios o contenido comercial.

## Revisión individual A–H de las 11 EXISTING

A: evidencia identificada. B: disponible y hash correcto. C: demuestra la descripción exacta. D: no exclusivamente declarativa. E: limitaciones documentadas. F: afirmación permitida acotada. G: prohibiciones suficientes. H: EXISTING justificado. Cada PASS se refiere al alcance del registro, no a un producto terminado ni a un servicio disponible.

| Capability | Evidencias TDL-EVD | A | B | C | D | E | F | G | H | Fundamento de C/D | Límite revisado para E/F/G/H |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TDL-CAP-001 | 001–005/008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | raw VARCHAR, siete tablas y conteos del sentinel; SQL de importación concordante | Feed Asturias único; importación no replayada; no ingestión universal |
| TDL-CAP-002 | 001–003/008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | SHA base y ZIP; 7/7 entradas ZIP/extracción iguales | Identidad binaria; sin calidad, autenticidad jurídica o licencia garantizadas |
| TDL-CAP-003 | 002/006–008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | sentinel SELECT ejecutado read-only: 46 checks, 42 PASS / 4 FAIL | WARNING; cobertura estructural parcial, sin validador GTFS completo |
| TDL-CAP-004 | 002/006–008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | SELECT read-only; ruta 440: 1 ruta, 2 viajes, 2 shapes, 814 puntos | Consultas puntuales; sin motor analítico general |
| TDL-CAP-009 | 010–012/015/017 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DB: 10 documents, 6 relationships, 92 provisions; 10/10 hashes y 22 invariantes | Fidelidad textual no acreditada; anomalías, paths absolutos; sin exhaustividad |
| TDL-CAP-010 | 010/011/013–015/018/019/028 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | DB y CSV: 48 requirements, 36 facts, 10 deadlines; 387 checks completos | Fuente 2024-03-04; siete PARTIAL, decisiones humanas; sin cumplimiento |
| TDL-CAP-011 | 011/016/018/019 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | matrices CSV de decisiones y universo atómico; materialización efectiva, gates CLOSED | Registros operativos de revisión, no solo narrativa; sin aprobación jurídica externa o automática |
| TDL-CAP-012 | 010/011/015/017 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | diez resultados completos JSON, exit codes 0 y hashes SQL; 22+22+63+387 PASS | Resultados de estados identificados; sin rerun ni prueba jurídica |
| TDL-CAP-016 | 021–023 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | JSON de cinco datasets, código de censo y cinco ZIP con hashes concordantes | Censo histórico; no veinte clientes ni evaluación semántica |
| TDL-CAP-018 | 024–026 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | JSON estructurado 0.2.1 y manifiesto SHA/tamaño concordantes | Export recibido histórico; AH/H/L2 en routes frente a selección con L3; sin completitud, replay ni findings |
| TDL-CAP-019 | 022–024/027 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | CSV computado de cinco datasets y código; UNKNOWN/NOT_COMPARABLE; aceptación posterior distingue histórico | Comparación descriptiva; sin equivalencia de reglas, superioridad ni enum findings históricos válidos |

B se apoya en los checks de rutas individuales de checks.json y los resultados completos; A usa las referencias exactas del CAPABILITY_REGISTER. En 011, las matrices de decisiones son registros estructurados de acciones y su resultado materializado, corroborados por base/CSV/gates; no se toma una mera declaración de revisión como prueba de auditoría normativa. En 018 se acredita el artefacto conservado y su identidad, sin afirmar completitud de selección. En 019 el resultado descriptivo computado conserva desconocidos y la rectificación de procedencia; no transforma hallazgos invalidados en hechos.

## Coherencia de las 20 capacidades

001 ingestión, 002 identidad binaria, 003 controles y 004 consulta tienen objetos diferentes aunque compartan fuente/base; reutilización probatoria legítima, sin extrapolar a otros feeds. 009 corpus, 010 requisitos materializados, 011 decisiones y 012 regresión distinguen persistencia, revisión y comprobación técnica. No se fusionan en capacidad jurídica. 016 censo, 018 export conservado y 019 comparación descriptiva separan datos originales, salida recibida y contraste histórico. Las descripciones compuestas contienen actividades de un mismo resultado acotado; no mezclan capacidades normativas, comerciales o universales demostradas.

| Capacidades restantes | Estado confirmado | Motivo |
| --- | --- | --- |
| 005 | PENDING_VERIFICATION | Tres KML; generador GIS reproducible no identificado. |
| 006 | PLANNED | Sin core tipado en catálogo GTFS. |
| 007 | PLANNED | Sin motor propio ni validation.results; sentinel no lo sustituye. |
| 008 | PLANNED | Sin analysis persistido en GTFS; SELECT ad hoc no lo sustituye. |
| 013 | PENDING_VERIFICATION | Replay integral no demostrado, execution_performed=NO y decisiones humanas. |
| 014 | IN_DEVELOPMENT | Solo DDL/infraestructura; coverage/equivalences=0, sin mapping consolidado. |
| 015 | IN_DEVELOPMENT | Solo infraestructura audit; rules/runs/results=0, sin motor normativo operativo. |
| 017 | PENDING_VERIFICATION | Outputs históricos y aceptación declarada, sin cadena independiente de build vigente revisada. |
| 020 | PLANNED | Modelo conceptual Audit/Quality; sin contrato operativo demostrado. |

No hay duplicados, contradicciones de estado ni dependencias que invaliden los alcances EXISTING. Las dependencias pendientes sí impiden ampliarlos. Ninguna degradación adicional de las 11 EXISTING; las degradaciones del inventario previo siguen vigentes. Distribución: EXISTING 11, IN_DEVELOPMENT 2, PLANNED 4, PENDING_VERIFICATION 3; total 20.

## Clasificación de las 28 evidencias

Los tipos siguientes distinguen implementación y resultado. Un script, hash, baseline declarada o aceptación registrada no prueba por sí solo que toda la capacidad se haya ejecutado.

| Evidence ID | Naturaleza comprobada | Uso y límite |
| --- | --- | --- |
| TDL-EVD-001 | Declarativa: JSON/estado | Baselines y contexto; corroborados por bases y resultados |
| TDL-EVD-002 | Resultado persistido: DuckDB | raw disponible, identidad y SELECT verificables |
| TDL-EVD-003 | Input binario: ZIP | Fuente y procedencia; no resultado de validación |
| TDL-EVD-004 | Ejecutable: SQL | Implementación import; sin replay nuevo |
| TDL-EVD-005 | Ejecutable: PowerShell | Runner; sin adquisición o replay demostrado |
| TDL-EVD-006 | Ejecutable: SQL SELECT | Sentinel acotado; ejecución guardada en review_v1 |
| TDL-EVD-007 | Resultado persistido: TXT | Salida histórica completa con FAIL explícitos |
| TDL-EVD-008 | Declarativa: informes | Límites y observaciones, corroboración sin suficiencia aislada |
| TDL-EVD-009 | Resultado persistido: KML | Artefactos GIS; sin generador/replay |
| TDL-EVD-010 | Resultado persistido: DuckDB | Corpus/requisitos y DDL vacío de mapping/audit |
| TDL-EVD-011 | Declarativa: freeze JSON/MD | Estado aprobado y hashes, corroborados físicamente |
| TDL-EVD-012 | Resultado persistido: CSV de hashes | 10/10 fuentes actuales concordantes |
| TDL-EVD-013 | Resultado persistido: CSV | 48 requisitos, 36 facts, 10 deadlines; concordancia DB |
| TDL-EVD-014 | Mixta: informe y Python ejecutable | Materialización histórica; sin escritura/replay nuevo |
| TDL-EVD-015 | Mixta: JSON/exit codes persistidos y SQL | Diez suites completas ligadas a estado y hashes |
| TDL-EVD-016 | Declarativa: matriz CSV de replay | Execution_performed=NO; no replay demostrado |
| TDL-EVD-017 | Declarativa: política tests | Atribución histórica, no evidencia de PASS por sí sola |
| TDL-EVD-018 | Registro operativo: CSV decisiones y MD | Decisiones Gate 1; corroboradas por resultado final, no auditoría jurídica |
| TDL-EVD-019 | Registro operativo: universo CSV y MD | Resolución Gate 2 y materialización; no generador independiente |
| TDL-EVD-020 | Ejecutable: SQL DDL | Infraestructura solamente; cero evaluación |
| TDL-EVD-021 | Inventario declarativo: CSV/README | 20 entradas de investigación; no clientes comerciales |
| TDL-EVD-022 | Resultado persistido: JSON/MD | Censo cinco datasets; ZIP actuales concordantes |
| TDL-EVD-023 | Ejecutable: Python | Implementación censo/comparación; no generadores ejecutados ahora |
| TDL-EVD-024 | Mixta: CSV computado y informes/diseño | Comparación descriptiva; histórico Bizkaibus superado |
| TDL-EVD-025 | Resultado persistido: HTML/manifiesto | Output recibido 0.2.1; hash y tamaño correctos, no runtime actual |
| TDL-EVD-026 | Resultado persistido: JSON/manifiesto | Datos recibidos; sin completitud, replay ni round-trip |
| TDL-EVD-027 | Mixta: aceptación declarativa y project JSON | Registro run_004; no forense/build vigente independiente |
| TDL-EVD-028 | Declarativa: diseño técnico | Estado inicial superado por freeze; sin prueba de mapping/audit |

76/76 rutas únicas disponibles y hashes correctamente asociados. Correspondencia bidireccional de referencias en las 20 fichas comprobada. No referencias rotas en los enlaces del registro/índice/gaps. Las rutas históricas absolutas y baselines superadas se identifican como límites de portabilidad/procedencia; no se presentan como entradas actuales universales. Artefactos Business de revisión adicionales no incrementan 28 Evidence IDs / 76 rutas técnicas.

## Sentinel GTFS y Compliance

Sentinel: **42 PASS / 4 FAIL**; exit 0, global **WARNING**. Los cuatro FAIL son analysis, core, validation y validation.results ausentes. Demuestra únicamente conteos, catálogo/tipos seleccionados, referencias y propiedades estructurales comprobadas, tiempos >=24h conservados y subconjunto ruta 440 de Asturias. La prueba de monotonía ordena numéricamente secuencias: no demuestra el orden original de las filas. No demuestra toda la especificación, validez semántica universal, completitud, otras fuentes, GIS ni motor propio. No es un validador GTFS completo.

Compliance: 48 requisitos revisados, 36 facts, 10 deadlines, 10 fuentes y gates conservados. Siete dependencias PARTIAL, anomalías Annex 1.3 B-I/D-I, textual_fidelity_certified=false, legal_compliance_assessed=false; tres paths absolutos, decisiones humanas y generadores Gate 1/2 no independientes. Replay integral no demostrado; mappings sin resultado consolidado (cero coverage/equivalences) y audit limitado a infraestructura (cero rules/runs/results). No es auditoría normativa completa. GIS permanece PENDING_VERIFICATION. Licencias/reutilización, readiness comercial y mercado no evaluados.

## Evidencia durable de esta revisión

[checks.json](review_v1/checks.json) conserva 221 controles iniciales: 216 PASS y cinco FAIL de comparación textual case-sensitive del hexadecimal del censo. [summary.json](review_v1/summary.json) conserva ese FAIL inicial. [final_summary.json](review_v1/final_summary.json) resuelve los cinco mediante hash binario recomputado y normalización hexadecimal: 221 controles satisfechos, sin discrepancia de bytes. No se reinterpreta ningún FAIL técnico del sentinel: siguen siendo cuatro. review.py conserva el comparador inicial y no debe utilizarse para certificar los cinco hashes sin esa corrección documentada.

Consultas read-only, stdout completo, stderr y exit_code.txt persistidos en review_v1 para sentinel, raw_columns, compliance_catalog y compliance_counts. Diez suites Compliance verificadas desde resultados guardados, sin rerun. Inventarios technical_before.json/technical_after.json: 899 archivos técnicos concordantes; sin escritura técnica. Solo se ejecutaron SELECT y verificadores de lectura.

La congelación se describe en [BUSINESS_CAPABILITY_BASELINE_V1.md](BUSINESS_CAPABILITY_BASELINE_V1.md). PASS acredita consistencia y respaldo del inventario acotado; no declara éxito técnico completo ni cierra los gaps.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
