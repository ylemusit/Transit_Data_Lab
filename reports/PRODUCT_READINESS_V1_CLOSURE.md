# Transit Data Lab Product Readiness V1 — cierre técnico

**Fecha:** 2026-10-06
**Resultado:** `READY_FOR_CONTROLLED_PILOT_WITH_LIMITATIONS`
**Distribución:** `INTERNAL_USE_ONLY`

## Alcance

Se cerró la preparación técnica de un piloto controlado del workflow local interno GTFS. No se habilita distribución a clientes, instalador público, ejecución local por clientes, SaaS, firma de código, reputación SmartScreen ni soporte de hardware declarado. SaaS queda como opción futura fuera del scope. GTFS-RT, SIRI, Colombia, pricing, CRM y validación comercial permanecen fuera de alcance.

Windows Client V1 se clasifica como herramienta operacional interna `CLOSED_WITH_LIMITATIONS`; el estado documentado de W02–W08 es `PASS_WITH_LIMITATIONS`. PR #51 se fusionó el 2026-10-05 en `37bd5c5459c2f9ebad5f5cf4364ba209963cf6cd`; el CI post-merge run `37360863986` terminó SUCCESS sobre ese SHA. No se publicó release.

## Gap analysis y contrato de informe

El gap de presentación confirmado era la pérdida/ambigüedad de la matriz por regla, aplicabilidad, evaluabilidad, estado, fuentes y enlaces a findings al pasar de los artefactos G09/Compliance al informe cliente. El análisis completo está en [COMPLIANCE_REPORT_GAP_ANALYSIS_V1](COMPLIANCE_REPORT_GAP_ANALYSIS_V1.md). No hay base para generar un dictamen jurídico por requisito o declarar fuentes normativas vigentes a partir de la salida actual; tales atributos permanecen desconocidos o se explican como ausentes.

Se añadió `TDL_CLIENT_REPORT_V1` con 29 secciones en español, salida JSON/Markdown/PDF, matriz por regla, links a evidencia, visualización explícita de estados, conclusión de publication readiness derivada con brecha contable cero, y disclaimer. Severity sólo aparece si el contrato fuente ya la define. G09 preserva metadata disponible de regla/fuente de manera aditiva; el renderer no modifica Compliance, findings RAW ni artefactos autoritativos.

## E2E y gates

La auditoría E2E se ejecutó sobre `SYNTHETIC_UNKNOWN_GTFS`, no un operador real. Tres runs completaron con limitaciones: dos ejecuciones idénticas y una recurrente; misma salida del motor en replay; 34 artefactos por entrega; fuente inmutable; hashes, manifest y seal válidos; informe de 29 secciones, matriz de 33 reglas, PDF y JSON generados; sin rutas locales, upload, datos de cliente ni acceso nuevo a HOLDOUT. El accounting gap de interpretación fue 0. Para ese fixture el propio informe devuelve `NO ES POSIBLE EMITIR CONCLUSIÓN`, porque la aplicabilidad de varias reglas no está disponible en los artefactos y persisten gaps evaluativos; no se fuerza un PASS de publicación.

Evidencia persistida:

- [Resumen machine-readable de gates, tests y E2E](evidence/product_readiness_v1/validation_summary.json).
- [Detalle E2E sintético final](../02_Data_Engineering/GTFS_Lab/reports/evidence/product_readiness_v1/e2e_synthetic_r5.json), con hashes del PDF/Markdown/JSON, manifest y seal.
- [Salida segura del gate Compliance V1](evidence/product_readiness_v1/compliance_current_gate/summary.json): PASS. Phase 1 22/22 PASS; Phase 2 376 checks PASS y un FAIL histórico `UNCHANGED_COUNT_audit.rules` esperado y conservado (esperaba 0, observa 2); no se cambió la base y su hash inicial/final coincide.
- Gates Trust y Golden: Trust contract 12 checks PASS, Trust persistence PASS; GoldenCase 18/18, corpus 2/2 aprobado, evaluator PASS y golden regression 2/2 casos y 3/3 comprobaciones PASS.

Se ejecutaron los 15 grupos de tests del workflow sintético actual más `test_client_report.py`: **232 tests PASS**, cero FAIL. `compileall` y `git diff --check` PASS. No se ejecutaron pruebas de lectura de HOLDOUT ni nuevas campañas con operadores.

## Estado y limitaciones

```ini
COMPLIANCE_REPORT_GAP_ANALYSIS = PASS
REPORT_CONTRACT_V1 = PASS
ENGINE_REPORT_BRIDGE = PASS
FULL_VALIDATION_MATRIX = PASS
SPANISH_CLIENT_REPORT = PASS
END_TO_END_AUDIT = PASS (synthetic only)
ACCOUNTING_GAP = 0
TRUST_GATE = PASS
GTFS_LAB_GATE = PASS
COMPLIANCE_GATE = PASS_WITH_DOCUMENTED_HISTORICAL_EXCEPTION
TRANSIT_DATA_LAB_PRODUCT_READINESS_V1 = READY_FOR_CONTROLLED_PILOT_WITH_LIMITATIONS
WINDOWS_CLIENT_ROLE = INTERNAL_OPERATIONAL_TOOL
WINDOWS_CLIENT_V1 = CLOSED_WITH_LIMITATIONS (PR #51 merged; no product release)
SUPPORTED_OPERATING_ENVELOPE_V1 = DEFERRED_NOT_REQUIRED_FOR_CURRENT_PRODUCT_SCOPE
PUBLIC_WINDOWS_DISTRIBUTION = DEFERRED
CODE_SIGNING = DEFERRED
SMARTSCREEN_REPUTATION = DEFERRED
FUTURE_SAAS = FUTURE_OPTION_NOT_CURRENT_SCOPE
MARKET_VALIDATED = NO
DEMAND = NO
WTP = NO
DIFFERENTIATION = UNPROVEN
HOLDOUT_CONTENT_NEWLY_ACCESSED = NO
```

**Clean-machine qualification:** El pack indicó tratar Clean Machine Validation V1 como fundación cerrada y prohibió repetir la validación. La fuente vigente de W08 en este repositorio, sin embargo, registra `PARTIAL / BLOCKED_BY_ENVIRONMENT`; no se encontró evidencia autoritativa que permita elevar ese estado a PASS. Se conserva la clasificación documentada y no se repite la campaña. El límite no bloquea el scope actual de herramienta interna.

No se afirma certificación oficial, evaluación por autoridad competente, garantía NAP, cumplimiento legal integral, cobertura universal GTFS, validación de mercado ni willingness to pay. El próximo paso recomendado es un piloto real controlado sujeto a su autorización y a la aceptación de estos límites; no se contactó a terceros.

## Referencias Git

Base revisada: `origin/main` en `9734d800f3f2efeba8d910d23f565133ec7da402`. La PR y los SHA/resultados de CI asociados a esta implementación se añadirán a los metadatos finales al cerrar la revisión remota.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
