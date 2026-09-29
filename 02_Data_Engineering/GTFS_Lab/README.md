# GTFS_Lab — Transit Data Lab

Laboratorio de datos GTFS del proyecto global Transit Data Lab. Es distinto del producto GTFS Explorer Desktop, cuya baseline protegida es 0.2.2.

## Estado implementado

- GTFS_Lab V1 tiene pipeline local reproducible de ZIP a informe; gate sintético PASS y reglas GTFS_Lab PASS en Asturias con cero hallazgos. La regla Compliance V1 reporta `INSPECTION_ERROR` para el feed completo por su límite fijo de 10.000 filas.
- El dry run crea DuckDB aislado por ejecución y no modifica `databases/gtfs_lab.duckdb`, el ZIP original ni Compliance.
- Core, integridad, reglas iniciales, análisis con calendario, consultas SQL y exportaciones KML/GeoJSON están en el pack V1. Ver [estado V1](GTFS_LAB_V1_CURRENT_STATE.md) y [informe de estabilización](reports/GTFS_LAB_V1_STABILIZATION_REPORT.md).
- El import SQL/runner anterior y los tres KML históricos se conservan; el nuevo flujo no depende de ellos.
- Persistencia dual de confianza M02: las ejecuciones completas escriben `audit/audit_manifest.json` y `audit/findings.normalized.json` sin cambiar los outputs V1. Se valida con `python -m gtfs_lab.trust_persistence_gate --output runs/trust_persistence_gate`; el estado y los límites están en [estado V1](GTFS_LAB_V1_CURRENT_STATE.md).
- M03-A define `GoldenCase 1.0.0` y un gate de contrato (`python -m gtfs_lab.golden_contract_gate`). El ejemplo está en DRAFT; no hay corpus aprobado ni regresión Golden operativa. `APPROVED` es estado de lifecycle; la autoridad ejecutable requiere validar el contrato completo. La detección de mutaciones históricas se informa como `NOT_ENFORCED_IN_M03A`. Ver [contrato M03](GTFS_LAB_M03_GOLDEN_CASE_CONTRACT.md).
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
