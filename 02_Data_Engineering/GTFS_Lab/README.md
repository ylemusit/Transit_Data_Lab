# GTFS_Lab — Transit Data Lab

Laboratorio de datos GTFS del proyecto global Transit Data Lab. Es distinto del producto GTFS Explorer Desktop, cuya baseline protegida es 0.2.2.

## Estado implementado

- GTFS_Lab V1 tiene pipeline local reproducible de ZIP a informe; gate sintético PASS y reglas GTFS_Lab PASS en Asturias con cero hallazgos. La regla Compliance V1 del checkpoint base reportaba `INSPECTION_ERROR` al superar sus límites de 10.000 filas/1 MiB. M04-B2 desarrolla lectura incremental sintética en una rama aislada; su replay sigue cerrado hasta reconciliar la identidad del motor con el gate Compliance V1.
- El dry run crea DuckDB aislado por ejecución y no modifica `databases/gtfs_lab.duckdb`, el ZIP original ni Compliance.
- Core, integridad, reglas iniciales, análisis con calendario, consultas SQL y exportaciones KML/GeoJSON están en el pack V1. Ver [estado V1](GTFS_LAB_V1_CURRENT_STATE.md) y [informe de estabilización](reports/GTFS_LAB_V1_STABILIZATION_REPORT.md).
- El import SQL/runner anterior y los tres KML históricos se conservan; el nuevo flujo no depende de ellos.
- Persistencia dual de confianza M02: las ejecuciones completas escriben `audit/audit_manifest.json` y `audit/findings.normalized.json` sin cambiar los outputs V1. Se valida con `python -m gtfs_lab.trust_persistence_gate --output runs/trust_persistence_gate`; el estado y los límites están en [estado V1](GTFS_LAB_V1_CURRENT_STATE.md).
- M03-A define `GoldenCase 1.0.0` y M03-B aprueba dos casos sintéticos en `TDL_GOLDEN_CORPUS_V1`. `python -m gtfs_lab.golden_corpus_gate` valida el corpus aprobado; `python -m gtfs_lab.golden_regression_gate --output <directorio>` ejecuta ambos casos aprobados y genera evidencia fuera de `golden/`. `APPROVED` solo es autoridad ejecutable tras validar el contrato completo. La detección de mutaciones históricas sigue `NOT_ENFORCED_IN_M03A`; los hashes aprobados quedan ligados al corpus V1. Ver [contrato M03](GTFS_LAB_M03_GOLDEN_CASE_CONTRACT.md) y [review M03-B](reports/GTFS_LAB_M03B_GOLDEN_CORPUS_REVIEW.md).
- M04-A4 aprobó y congeló `CorpusSplit 1.0.0`: 14 DEVELOPMENT y 6 HOLDOUT (`006, 008, 013, 015, 017, 018`), que representan cinco unidades de lineage porque 013/015 forman una. HOLDOUT no se ha abierto ni ejecutado y M04-B no ha comenzado. Aprobación, gate y política de freeze: [M04-A4](reports/GTFS_LAB_M04A4_SPLIT_APPROVAL.md). El análisis de sensibilidad está en [M04-A3b](reports/GTFS_LAB_M04A3B_SPLIT_SENSITIVITY_REVIEW.md); la evidencia de lineage M04-A2 se conserva en [M04-A2](reports/GTFS_LAB_M04A2_LINEAGE_EVIDENCE_REVIEW.md).
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
