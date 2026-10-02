# NeTEx N06 — reglas técnicas

El registry versionado está en `02_Data_Engineering/NeTEx_Lab/spec/netex_rule_registry_v1.json`; su contrato es `netex_rule_registry_v1.schema.json`. `RuleSpec` exige identidad/versionado, autoridad, requisito, scope, applicability, evaluation type, familia, severidad, vocabulario nativo y contrato de evidencia.

| Regla | Familia | Autoridad | Evaluación y límites |
|---|---|---|---|
| `NETEX-XML-001` | XSD/intake | L4 técnico TDL | Well-formedness y rechazo DTD/entity. |
| `NETEX-XSD-001` | XSD | L4 artefacto pinned | Valida únicamente contra root y dependencias de v2.0.0. |
| `NETEX-PROFILE-001` | PROFILE | L3 EPIP 2026 | Devuelve `HUMAN_REVIEW_REQUIRED`; asserts exhaustivas no implementadas. |
| `NETEX-IDENTITY-001` | IDENTITY | L4 recomendación TDL | IDs repetidos se elevan a revisión; nunca a obligación normativa/EPIP. |

Las reglas en runtime y catálogo JSON se contrastan en pruebas. Referencias, temporalidad, geografía, semántica y alineación regulatoria no tienen reglas que inventen resultados; se inventarían y quedan `NOT_EVALUABLE`/`UNKNOWN` cuando no hay contract/cobertura. `WARNING` no es estado nativo.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
