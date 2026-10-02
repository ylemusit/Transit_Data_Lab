# NeTEx N04 — representabilidad

**Estado:** `MATRIX_COMPLETE_FOR_APPROVED_SCOPE_AND_ACCESSIBLE_REQUIREMENTS`; el inventario de assertions EPIP completas permanece `UNKNOWN` por falta de texto controlado.

La matriz machine-readable está en `N04_REPRESENTABILITY_20261002.json`. Cada concepto separa clase de evaluación (`DIRECT_XSD`, `PROFILE_CONSTRAINT`, `CROSS_REFERENCE`, `SEMANTIC`, `QUALITY`, `REGULATORY_ALIGNMENT`), representabilidad, locator XML/XSD, evidencia y certeza. Las locators estructurales son candidatos de extracción; solo la validación XSD es ejecutable en esta entrega.

- `MACHINE_EVALUABLE`: la propiedad estructural está en la raíz XSD fijada.
- `HUMAN_REVIEW_REQUIRED`: interpretación de perfil/contexto no se deduce del schema.
- `NOT_REPRESENTABLE`: solo se usa si hay evidencia afirmativa de límite del modelo; no se observó caso probado en los conceptos cubiertos.
- `OUT_OF_SCOPE`: incluye datos dinámicos, modos distintos y aceptación NAP.
- `UNKNOWN`: requisito/perfil sin texto o mapping suficiente; no se convierte en `FAIL`.

`N04_UNKNOWN` y `N04_HUMAN_REVIEW` son explícitos. No se afirma completitud semántica ni EPIP; el runtime marca el perfil como `HUMAN_REVIEW_REQUIRED`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
