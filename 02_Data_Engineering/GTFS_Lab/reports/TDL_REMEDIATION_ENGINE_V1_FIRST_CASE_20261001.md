# Remediation Engine V1 — primer caso DEVELOPMENT

**Estado (2026-10-01):** contrato y aplicador local implementados; aceptación del primer caso pendiente de recuperar y verificar el ZIP original DEVELOPMENT `010`. No se declara el caso exitoso ni `READY_FOR_FINAL_HUMAN_CLOSURE_DECISION`.

## Flujo y contrato

```text
finding G03 → propuesta exacta → clasificación y autorización por instancia
→ copia de trabajo ZIP → aplicación → diff del miembro → atribución
→ re-audit G03–G08 → comparación de findings → evidencia JSON persistida
```

El contrato ejecutable está en `gtfs_lab/remediation.py`. Solo admite en esta revisión `dataset_id=010`, `agency.txt`, `agency_url`, `empresarodil.es` → `https://empresarodil.es`, regla `GTFS-G03-FIELD-TYPE` y la identidad estable que resulta de regla/archivo/localizador/campo/valor observado. Rechaza escrituras sobre la fuente, salida existente, valor ambiguo, autorización ausente, locator distinto y propuestas de otros dominios. No existe regla genérica `missing_scheme → prepend https://`.

La evidencia registra valor original/propuesto, ruta y SHA-256 de entrada/salida, archivo, locator, regla y finding de origen, fuente externa, clasificación `SAFE_DETERMINISTIC`, diff interno exacto, autorización `HUMAN_APPROVED_CASE_SPECIFIC` y resultados de re-audit/comparación. La fuente original permanece read-only por contrato; el resultado derivado usa otra ruta. `persist_evidence()` crea un JSON nuevo y rehúsa reemplazar evidencia existente.

## Evidencia externa del caso

Observación web: `2026-10-01T04:02:00Z`, [https://empresarodil.es](https://empresarodil.es). La página se cargó bajo HTTPS y se identifica como Empresa Rodil (título “Inicio - Empresa rodil”; contenido de Empresa Rodil/RODIL S.L.). Esta evidencia queda acotada a este dominio y caso, junto con la autorización humana explícita de Yeison del 2026-10-01. No se generaliza a otros valores.

## Revisión de otros findings DEVELOPMENT

La documentación del replay G10 identifica, además, el finding de referencias `service_id` sin resolver en `011` y progresión de distancia en `014`. No hay en los artefactos locales revisados evidencia suficiente por instancia para proponer transformaciones seguras: resolver referencias requiere evidencia del dominio del feed y la progresión requiere evaluación de los datos/semántica afectada. Los estados `NOT_EVALUABLE`, los gaps G03 y las recomendaciones G08 tampoco constituyen por sí mismos fixes. **No se encontró otro candidato demostrablemente seguro**; no se fuerza un segundo cambio.

## Bloqueo de aceptación reproducible

El artefacto de inventario declara para `010`:

```ini
EXPECTED_SOURCE_PATH = FAMILY_B_SME_OPERATIONAL/010_rodil/02_sources/gtfs_schedule/original/20260309_110029_BUS_RODIL.zip
EXPECTED_SOURCE_SHA256 = 3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf
EXPECTED_SIZE_BYTES = 13888
```

Esa ruta no existe en este checkout. No se ha reconstruido ni sustituido el dataset desde `provenance_v1.json`; sus metadatos no reemplazan los bytes originales. En consecuencia, no se pudo crear el derivado real, ejecutar el pipeline G03–G08 pre/post, demostrar resolución del finding ni comprobar findings nuevos. La suite unitaria usa un ZIP sintético solo para verificar el contrato y **no** satisface aceptación del feed 010.

```ini
ORIGINAL_DATASET_UNCHANGED = NOT_VERIFIABLE_WITH_SOURCE_ABSENT
DERIVED_DATASET_CREATED = NO (real case)
CHANGE_ATTRIBUTION_COMPLETE = CONTRACT_IMPLEMENTED; CASE_PENDING
ORIGINAL_FINDING_RESOLVED = NOT_VERIFIED
NEW_UNRELATED_FINDINGS = NOT_VERIFIED
REAUDIT_REPRODUCIBLE = NOT_VERIFIED
REMEDIATION_ENGINE_V1 = IMPLEMENTED_LOCAL; FIRST_CASE_ACCEPTANCE_PENDING_SOURCE
HOLDOUT = NOT_ACCESSED
GTFS_AUDIT_ENGINE_V1 = UNCHANGED
M02 = UNCHANGED
```

Para cerrar este caso hace falta restaurar el ZIP exacto en su ruta original o aportar una copia de trabajo cuyos bytes coincidan con el SHA-256 anterior. Después se podrá aplicar el contrato en un directorio derivado y ejecutar/repetir el audit pipeline exclusivamente sobre ese DEVELOPMENT.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
