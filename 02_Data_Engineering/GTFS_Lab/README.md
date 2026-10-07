# GTFS_Lab — Transit Data Lab

Banco de pruebas con entrada controlada: [TEST_BANK_V1.md](TEST_BANK_V1.md). `python -m gtfs_lab.test_bank <zip> --bank P:/TransitDataLab/02_Data/TestBank --metadata <json>` captura identidad, usa nombres internos numéricos, ejecuta auditoría/replay y clasifica el procedimiento como OK/NOT_OK; un OK puede contener findings. Banco operativo fuera de Git; CLI técnico, autoservicio pendiente.

Para un gate de CI sobre un ZIP, ejecutar `python -m gtfs_lab.ci_gate <zip> --output <directorio-nuevo>` desde este directorio. Devuelve JSON y salidas 0 (política satisfecha), 2 (fallo técnico/de inspección/recurso) o 3 (configuración inválida); el CLI V1 de ejecución conserva su contrato. Las nuevas auditorías persistidas marcan ChangeAttribution 1.1.0 y versiones semánticas por regla. Véase el [pack de precondiciones](../../reports/repository_integrity/TDL_GTFS_ENGINE_PRECONDITIONS_PACK_CLOSURE.md).

Laboratorio de datos GTFS del proyecto global Transit Data Lab. Es distinto del producto GTFS Explorer Desktop, cuya baseline protegida es 0.2.2.

## Estado implementado

- GTFS Productization / Client Audit Workflow V1 está en implementación aislada. Contrato, design review, entrypoint local `python -m gtfs_lab.client_workflow` y gates/evidencia sintética se describen en el [diseño y contrato](reports/TDL_GTFS_CLIENT_AUDIT_WORKFLOW_V1_DESIGN_AND_CONTRACT.md); el estado vigente y límites están en [PROJECT_STATUS](../../PROJECT_STATUS.md). No declara readiness comercial.

- GTFS Audit Engine V1 está `PASS / CLOSED` desde el 2026-10-01 para el alcance técnico documentado. G08–G11 están cerrados; PR #29 y CI post-merge PASS constan en [PROJECT_STATUS.md](../../PROJECT_STATUS.md). La decisión humana final y sus límites se detallan en el [cierre G11](reports/TDL_GTFS_AUDIT_ENGINE_V1_G11_CLOSURE_REVIEW_20261001.md) y el [registro machine-readable](reports/evidence/g11_closure_candidate.json). HOLDOUT no se accedió, M02 no cambió y no se inició ningún track posterior.
- G08 es aditivo después de G07 y queda fuera de `validation` legacy y de la normalización M02. G09 escribe informes JSON/Markdown suplementarios que M02 no registra. G10 verifica hashes y usa exclusivamente el split DEVELOPMENT.

- GTFS_Lab V1 tiene pipeline local reproducible de ZIP a informe; gate sintético PASS y reglas GTFS_Lab PASS en Asturias con cero hallazgos. El resultado Compliance V1 del primer checkpoint M04-B1 fue `INSPECTION_ERROR` por límites del evaluador histórico. La implementación actual `compliance-v1/2` completó la evaluación técnica del HOLDOUT V2; véase el [estado vigente](../../PROJECT_STATUS.md). Ninguno de estos resultados acredita una auditoría jurídica del operador.
- El dry run crea DuckDB aislado por ejecución y no modifica `databases/gtfs_lab.duckdb`, el ZIP original ni Compliance.
- Core, integridad, reglas iniciales, análisis con calendario, consultas SQL y exportaciones KML/GeoJSON están en el pack V1. Ver [estado V1](GTFS_LAB_V1_CURRENT_STATE.md) y [informe de estabilización](reports/GTFS_LAB_V1_STABILIZATION_REPORT.md).
- El import SQL/runner anterior y los tres KML históricos se conservan; el nuevo flujo no depende de ellos.
- Persistencia dual de confianza M02: las ejecuciones completas escriben `audit/audit_manifest.json` y `audit/findings.normalized.json` sin cambiar los outputs V1. Se valida con `python -m gtfs_lab.trust_persistence_gate --output runs/trust_persistence_gate`; el estado y los límites están en [estado V1](GTFS_LAB_V1_CURRENT_STATE.md).
- M03-A define `GoldenCase 1.0.0` y M03-B aprueba dos casos sintéticos en `TDL_GOLDEN_CORPUS_V1`. `python -m gtfs_lab.golden_corpus_gate` valida el corpus aprobado; `python -m gtfs_lab.golden_regression_gate --output <directorio>` ejecuta ambos casos aprobados y genera evidencia fuera de `golden/`. `APPROVED` solo es autoridad ejecutable tras validar el contrato completo. La detección de mutaciones históricas sigue `NOT_ENFORCED_IN_M03A`; los hashes aprobados quedan ligados al corpus V1. Ver [contrato M03](GTFS_LAB_M03_GOLDEN_CASE_CONTRACT.md) y [review M03-B](reports/GTFS_LAB_M03B_GOLDEN_CORPUS_REVIEW.md).
- M04-A4 aprobó y congeló `CorpusSplit 1.0.0`: 14 DEVELOPMENT y 6 HOLDOUT (`006, 008, 013, 015, 017, 018`), que representan cinco unidades de lineage porque 013/015 forman una. M04-B3 completó la evaluación HOLDOUT V2 y obtuvo cierre humano aprobado; sus límites y evidencia constan en el [informe B3](../../reports/GTFS_LAB_M04B3_HOLDOUT_REPLAY_V2.md) y en el [estado vigente](../../PROJECT_STATUS.md). Aprobación, gate y política de freeze: [M04-A4](reports/GTFS_LAB_M04A4_SPLIT_APPROVAL.md). El análisis de sensibilidad está en [M04-A3b](reports/GTFS_LAB_M04A3B_SPLIT_SENSITIVITY_REVIEW.md); la evidencia de lineage M04-A2 se conserva en [M04-A2](reports/GTFS_LAB_M04A2_LINEAGE_EVIDENCE_REVIEW.md).
- Evidencia piloto de 20 operadores en [20_clientes_reales](20_clientes_reales/CURRENT_DOCUMENTATION.md). Son datasets de investigación, no clientes comerciales, y quedan fuera del run V1.

En M02, `findings.normalized.json` describe solo la normalización: `NORMALIZED` no significa que la auditoría esté aceptada. Solo la existencia de `audit_manifest.json` validado contra M01 1.1.2 representa aceptación Trust. Cada `finding.evidence.source_sha256` debe coincidir con el SHA-256 del dataset; los hashes extranjeros se rechazan como `REJECTED_FINDING_SOURCE_MISMATCH` y el pipeline falla cerrado. Si falta ese campo, se completa con el hash del dataset actual.

GTFS-RT y SIRI quedan fuera de GTFS_Lab V1; NeTEx pertenece al laboratorio Compliance separado. El resultado técnico V1 no acredita cumplimiento jurídico ni auditoría de operadores.

## Inspección segura

Desde este directorio, una consulta de inventario se puede ejecutar así:

```powershell
duckdb -readonly databases/gtfs_lab.duckdb -c "SHOW ALL TABLES;"
```

La base está excluida de Git. Un checkout no incluye bases ni feeds; requiere recuperar los bytes exactos conforme a [BACKUP_AND_RECOVERY.md](../../BACKUP_AND_RECOVERY.md).

El runner `sql/01_import/run_import_consorcio_asturias.ps1` ejecuta SQL con CREATE OR REPLACE TABLE y modifica la base. No ejecutarlo para comprobar una baseline congelada. Su existencia no acredita replay end-to-end del laboratorio. Tampoco se deben regenerar KML ni runs piloto para actualizar documentación.

`main.stops` duplica raw.stops según la auditoría congelada; su propósito sigue sin documentar. No borrarlo sin una tarea específica.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
