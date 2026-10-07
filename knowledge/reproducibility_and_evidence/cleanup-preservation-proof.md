# Un checkout limpio no prueba que sus datos sean prescindibles

- **CONTEXT:** Los checkouts históricos mezclan fuentes Git con datos, evidencia e ignorados.
- **PROBLEM / ROOT_CAUSE:** Git solo representa el contenido versionado; un HEAD remoto o un status limpio no conserva los archivos ignorados/no rastreados.
- **DECISION_OR_SOLUTION:** Verificar hojas, fuente canónica, diferencias locales, dependencias y protección antes de borrar. Si no hay prueba, conservar y describir la ambigüedad.
- **EVIDENCE / RELATED_COMMITS_OR_REPORTS:** [Fuente autoritativa](../../reports/LOCAL_ENVIRONMENT_RECONCILIATION_V2.md).
- **IMPACT:** V2 retiró únicamente cachés/builds con receta comprobada; dejó los árboles ambiguos intactos.
- **REUSABLE_LESSON:** Clasificar desconocido como REVIEW_REQUIRED; no convertir antigüedad, nombre o reproducibilidad supuesta en autorización. No abrir HOLDOUT para intentar justificar una limpieza.
- **STATUS:** Retenido; alcance y límites de la fuente, sin nueva certificación.
