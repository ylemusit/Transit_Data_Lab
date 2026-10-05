# Windows Self-Service Client V1 — W06 Reporting / Export

**Decisión:** `W06 = PASS_WITH_LIMITATIONS` (2026-10-05).

## SCOPE

Añadir un informe PDF profesional, derivado y trazable dentro del paquete local de entrega, manteniendo JSON/manifest como evidencia autoritativa.

## IMPLEMENTATION

- `report/client_report.pdf` resume identidad, hash, fecha de ingesta, estado, accounting, familias, entidades afectadas, patrón, primera recomendación disponible, GIS y límites técnico-legales.
- ReportLab 5.0.1 queda fijado en `packaging/client-pdf-requirements.txt`; la spec onedir empaqueta el módulo y sus fuentes Unicode Vera.
- `pdf_generation_status.json` registra `GENERATED` o `FAILED_NONBLOCKING`. Un fallo del renderer no transforma un audit completo en error ni elimina las evidencias JSON/Markdown.
- PDF y estado del renderer entran en `delivery_artifacts` antes de calcular SHA-256 y el seal existente. La GUI habilita abrir el PDF solo cuando se generó.
- El Markdown y los demás artefactos de máquina permanecen intactos; el PDF se declara expresamente una capa de presentación.

## TESTS

- `python -m unittest discover -s tests -p 'test_client_*.py'`: 24 tests, OK; 2 skips documentados.
- E2E verifica PDF presente, `GENERATED`, inclusión en el manifest y fallo inyectado `FAILED_NONBLOCKING` conservando el resultado y sus hashes.
- `py_compile`: PASS.
- `git diff --check`: PASS.
- QA PDF: muestra sintética de 1 página y matriz de 80 familias/5 páginas renderizadas con Poppler; inspección visual de primera, intermedia y última páginas PASS. Texto español y caracteres Unicode revisados.

## EVIDENCE

Los artefactos JSON/manifest preexistentes son el input del PDF. El PDF y `pdf_generation_status.json` se hashean como delivery artifacts; el seal raíz conserva su forma existente.

## LIMITATIONS

- Se listan hasta 250 familias; el documento explicita el truncamiento y remite al JSON completo.
- La tabla usa la primera recomendación disponible por familia; para todos los findings y referencias consulte los JSON fuente.
- No se construyó aún el onedir que use la nueva dependencia. Ese build y la validación aislada se reservan a W08.

## DECISION

`PASS_WITH_LIMITATIONS`; PDF reproducible, legible y no autoritativo, con fallo no bloqueante.

## NEXT PHASE

W07 matriz de fallos y recuperación; W08 hará el build onedir con las dependencias fijadas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
