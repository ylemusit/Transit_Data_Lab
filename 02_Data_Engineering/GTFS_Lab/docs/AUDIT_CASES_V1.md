# Contrato lateral de casos de auditoría V1

## Propósito y compatibilidad

`TDL_AUDIT_CASES_V1` representa casos, decisiones, seguimiento y relaciones con la evidencia. Es un contrato lateral: `AUDIT_CONSOLIDATED.json` V1 conserva su esquema, significado y autoridad técnica. El modelo de casos referencia el SHA-256 canónico del JSON V1, la fuente y la ejecución exacta.

El esquema está en `spec/audit_case_contract_v1.schema.json`. `gtfs_lab.interpretation.cases.validate_cases()` valida el esquema completo cuando `jsonschema` está disponible. En instalaciones mínimas aplica validaciones estructurales y contables principales; esta ruta no sustituye la validación completa contra JSON Schema.

## Contabilidad

- `source_record_count`: findings de procedencia conservados.
- `classified_record_count`: registros cubiertos por la interpretación V1.
- `reconciled_event_count`: eventos tras reconciliar referencias duplicadas con evidencia.
- `duplicate_source_reference_count`: registros adicionales que apuntan a eventos ya representados; no se deducen solo por similitud.
- `unclassified_record_count` y `accounting_gap`: mantienen las definiciones de cobertura contable V1.

La suma de eventos y referencias duplicadas debe coincidir con los registros clasificados. La brecha contable se calcula respecto a los registros fuente, no respecto a eventos deduplicados.

Cada ocurrencia conserva `origin`, regla, fichero, localizador nativo, localizador normalizado y `source_record_id`. `assignment=PRIMARY` incluye la referencia en la cobertura de ocurrencias del caso; `RELATED` permite enlazar evidencia adicional sin contarla dos veces. Las referencias primarias deben pertenecer a V1 y, junto a `unclassified_source_record_ids`, cubrir exactamente sus registros de procedencia. La normalización añade una clave de comparación y nunca reemplaza el localizador original.

## Decisiones y estados

El contrato separa aplicabilidad, evaluabilidad, disposición, prioridad, impacto conocido/potencial, estado comunicado por productor y verificación de reauditoría. `UNASSESSED` es el valor explícito por defecto de prioridad sin fundamento. El estado `REPORTED_CORRECTED` no equivale a `RESOLVED`; `RESOLVED`, `PERSISTENT` y `REAPPEARED` requieren evidencia enlazada. `RESOLVED` además exige una ejecución distinta de la actual. El validador exige que la referencia de ejecución enlazada tenga evidencia asociada. Relaciones entre ejecuciones admiten correspondencias uno a uno, divisiones, fusiones, nuevo, persistente, resuelto, reaparecido, no reevaluado y no comparable.

La aptitud para uso (`use_readiness`) es independiente de la evaluación técnica y puede quedar `NOT_DETERMINED` si no se declara un destino.

## Comprobación

Desde `02_Data_Engineering/GTFS_Lab`, ejecutar las pruebas focalizadas del contrato, interpretación y workflow con el runtime Python TDL. La prueba `tests/test_audit_case_contract.py` cubre contabilidad por registros frente a eventos, identidad, localizadores, aceptación del productor sin borrar el resultado técnico y corrección pendiente de reauditoría.
