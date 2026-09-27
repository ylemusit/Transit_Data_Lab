# GTFS_Lab — Transit Data Lab

Laboratorio de datos GTFS del proyecto global Transit Data Lab. Es distinto del producto GTFS Explorer Desktop, cuya baseline protegida es 0.2.2.

## Estado implementado

- Snapshot Asturias: `feeds/raw/20260924_020003_Consorcio_Asturias.zip` y extracción con siete tablas GTFS; usa calendar_dates y no calendar.
- Base local: `databases/gtfs_lab.duckdb`; esquema raw con columnas VARCHAR. Conteos y hash en [PROJECT_STATUS.md](../../PROJECT_STATUS.md) y en la instantánea congelada raíz.
- SQL de importación en `sql/01_import`; runner PowerShell que fija el directorio del laboratorio.
- Sentinel de integridad en `sql/07_tests/test_gtfs_lab_integrity.sql`. Las capas ausentes producen advertencias/fallos explícitos; no es un validador GTFS completo.
- Tres KML en exports para route_id 440; no existe un pipeline GIS reproducible acreditado.
- Evidencia piloto de 20 operadores en [20_clientes_reales](20_clientes_reales/CURRENT_DOCUMENTATION.md). Son datasets de investigación, no clientes comerciales.

Core, validation y analysis siguen pendientes. GTFS-RT, NeTEx y SIRI son laboratorios futuros separados. No se infiere soporte de estándares o auditoría jurídica a partir de los nombres de carpetas.

## Inspección segura

Desde este directorio, una consulta de inventario se puede ejecutar así:

```powershell
duckdb -readonly databases/gtfs_lab.duckdb -c "SHOW ALL TABLES;"
```

La base está excluida de Git. Un checkout no incluye bases ni feeds; requiere recuperar los bytes exactos conforme a [BACKUP_AND_RECOVERY.md](../../BACKUP_AND_RECOVERY.md).

El runner `sql/01_import/run_import_consorcio_asturias.ps1` ejecuta SQL con CREATE OR REPLACE TABLE y modifica la base. No ejecutarlo para comprobar una baseline congelada. Su existencia no acredita replay end-to-end del laboratorio. Tampoco se deben regenerar KML ni runs piloto para actualizar documentación.

`main.stops` duplica raw.stops según la auditoría congelada; su propósito sigue sin documentar. No borrarlo sin una tarea específica.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
