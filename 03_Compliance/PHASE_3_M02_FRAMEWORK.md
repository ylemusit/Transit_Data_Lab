# Phase 3 M02 — marco de mappings

## Alcance y ejecución

M02 añade infraestructura reproducible, sin investigar estándares ni asociar capacidades reales a los 48 requisitos. Ejecutar desde cualquier directorio:

```powershell
& '<repo>\03_Compliance\sql\00_setup\run_phase_3_m02.ps1'
```

La migración `sql/00_setup/005_phase_3_m02_mapping_framework.sql` es aditiva e idempotente. `-ValidateOnly` ejecuta únicamente los conteos protegidos y Level A. La validación tarda una consulta DuckDB y comprueba integridad referencial lógica, estados, razones, duplicados y contexto; no realiza revisión semántica. No crea objetos de auditoría.

## Modelo

Los objetos nuevos `mapping.phase3_*` separan registro de estándares/versiones/perfiles, catálogo reusable de capacidades, relación N:M con `compliance.requirements`, representabilidad, evidencia observada, potencial de automatización, clasificación familiar, excepciones y referencias fuente. Los registros de estándar empiezan vacíos: `GTFS_SCHEDULE`, `GTFS_REALTIME`, `NETEX` y `SIRI` son vocabulario de identidad, no afirmaciones de cobertura.

`phase3_representability` describe si una capacidad puede expresar un concepto dentro del contexto registrado; no prueba presencia en un dataset. `phase3_observed_evidence` registra observaciones futuras. `phase3_automatability` describe posibilidad de auditoría futura; no ejecuta reglas. `PARTIAL`, `MISSING`, `UNKNOWN` y `NOT_APPLICABLE` requieren explicación.

La excepción declara una ruta de evaluación fuera del mapping de formato con tipo, razón, justificación, expectativas de evidencia y revisión. Una ausencia de mapping no se interpreta como incumplimiento. Las familias son taxonomía provisional, no clasificación jurídica.

## Vocabularios y compatibilidad

`mapping.phase3_vocabularies` conserva los términos de mapping, representabilidad, evidencia, automatización, revisión, relación familiar y excepción. Las tablas aplican `CHECK` para estados críticos. Los objetos heredados `mapping.format_coverage` y `mapping.format_equivalences` se preservan sin cambios por compatibilidad; Phase 3 no depende de ellos. La existencia y referencias hacia requisitos se validan en Level A porque DuckDB no ofrece FK entre esquemas.

M03 podrá incorporar referencias oficiales revisadas al catálogo; M04 podrá clasificar requisitos por familia y construir mappings; M05 podrá añadir observaciones de datasets; M06 podrá evaluar automatizabilidad y diseñar reglas/resultados en su propio alcance. M02 no habilita ni crea reglas de auditoría.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
