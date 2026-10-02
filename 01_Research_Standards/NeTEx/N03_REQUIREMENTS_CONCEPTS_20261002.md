# NeTEx N03 — requisitos y catálogo de conceptos

**Estado:** `TRACEABLE_WITH_EXPLICIT_UNKNOWN_PROFILE_REQUIREMENTS`
**Ámbito:** exclusivamente datos estáticos de autobús regular programado en España conforme al scope N01 aprobado.

Los identificadores machine-readable y sus relaciones están en `N03_REQUIREMENTS_20261002.json` y `N03_CONCEPTS_20261002.json`. Cada requisito separa fuerza normativa, fuente, cita, aplicabilidad e interpretación técnica. El extracto público incompleto de CEN/TS 16614-4:2026 no se trata como texto completo: los requisitos EPIP no visibles están representados por gaps `UNKNOWN`, sin assertions ejecutables.

## Esquema de extracción

`SOURCE → PROVISION → REQUIREMENT → CONCEPT → SCOPE`.

- **R-REG-01 — MUST textual, applicability sin resolver:** el artículo 4(1)(a) del Reglamento Delegado (UE) 2017/1926, modificado por 2024/490, asigna formato de carretera mediante referencia a 2015/962. EUR-Lex registra que 2015/962 fue derogado desde 2025-01-01 por 2022/670. No inferimos que NeTEx sea obligación para autobús regular desde el artículo 4(1)(b), que trata otros modos. Hay que revisar jurídicamente las categorías de datos de carretera y la remisión temporal antes de formular reglas regulatorias.
- **R-REG-02 — MUST, condicional y no ejecutable:** el artículo 4(2) exige perfiles mínimos UE o nacionales para categorías del Anexo 1 en que NeTEx/DATEX II sean aplicables. No afirma que EPIP 2026 sea automáticamente el perfil de autobús español. Categorías aplicables, modo jurídico y perfil están sujetos a revisión humana.
- **R-REG-03 — MUST textual, OUT_OF_SCOPE:** el artículo 4(1)(b) lista NeTEx CEN/TS 16614 y versiones posteriores para otros modos. No se traslada a autobús por inferencia.
- **R-SCHEMA-01 — expectativa técnica:** un documento declarado conforme a la línea base implementada debe validar frente al XSD NeTEx v2.0.0 fijado. Esta es una afirmación sobre el contrato técnico del audit, no un requisito legal autónomo ni prueba de EPIP.
- **R-EPIP-UNKNOWN — UNKNOWN:** requisitos, fuerza, condiciones y assertions completos de CEN/TS 16614-4:2026 requieren texto controlado. La preview pública solo sirve como pista de conceptos, no como fuente suficiente para un MUST exhaustivo.
- **R-NAP-UNKNOWN — UNKNOWN:** criterios machine-readable de aceptación del NAP español no identificados públicamente.

## Catálogo de conceptos

El catálogo incluye PublicationDelivery, frames, organisations/operators, StopPlace, Quay, ScheduledStopPoint, Line, Route, RoutePoint, JourneyPattern, ServiceJourney, PassingTime, DayType, OperatingPeriod/calendar, destination, mode/submode, identifiers, references, version/frame relationships, geometry and tariff zones. La existencia de un elemento en XSD prueba representabilidad estructural, no obligatoriedad EPIP. Las relaciones y estado `MACHINE_EVALUABLE`, `HUMAN_REVIEW_REQUIRED` o `UNKNOWN` constan concepto a concepto en N03/N04 JSON.

`N03_REQUIREMENTS = TRACEABLE` para las fuentes accesibles y el baseline aprobado; `N03_CONCEPTS = NORMALIZED`; `FABRICATED_REQUIREMENTS = 0`. El mapeo regulatorio de bus/road permanece `HUMAN_REVIEW_REQUIRED`, y el gap de texto controlado bloquea afirmaciones de cobertura completa del perfil.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
