# Windows Self-Service Client V1 — W04 Results

**Decisión:** `W04 = PASS_WITH_LIMITATIONS` (2026-10-05).

## SCOPE

Mostrar identidad, resultado de interpretación, accounting y familias consolidadas como una vista de solo lectura sobre la entrega sellada.

## IMPLEMENTATION

- La ventana de resultados lee `audit_manifest.json` y `AUDIT_CONSOLIDATED.json` de la entrega.
- Presenta identidad del dataset, hash fuente, estado, interpretation status, raw count, consolidated count, unclassified count y accounting gap.
- Lista las familias por regla, ocurrencias, entidades afectadas, patrón e impacto directo. La selección muestra la familia junto con findings fuente relacionados y referencias disponibles.
- Conserva límites técnicos/jurídicos explícitos y acceso a artefactos originales desde la entrega.

## TESTS

- `python -m unittest discover -s tests -p 'test_client_*.py'`: 24 tests, OK; 2 skips documentados.
- Tests de modelo de vista verifican los campos del resumen, brecha contable, límite jurídico, clasificación de familia, impacto, referencias y recomendaciones de findings fuente.
- `py_compile`: PASS.
- `git diff --check`: PASS.

## EVIDENCE

La interfaz consume el manifest y resultado consolidados generados por `client_workflow`; no escribe otra fuente de verdad. Se conserva la vista de artefactos técnicos para inspección avanzada.

## LIMITATIONS

- No se hizo aceptación visual humana de la nueva ventana. Los detalles avanzados se presentan como JSON formateado dentro de la GUI para mantener sus campos y referencias íntegros; su presentación puede requerir refinamiento visual.
- No se afirma que findings técnicos equivalgan a incumplimiento legal.

## DECISION

`PASS_WITH_LIMITATIONS`; un usuario puede ver resumen y familias en la aplicación, y seguir hasta la evidencia fuente sin abrir manualmente un archivo JSON.

## NEXT PHASE

W05 puente de exportación GIS y QGIS externo.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
