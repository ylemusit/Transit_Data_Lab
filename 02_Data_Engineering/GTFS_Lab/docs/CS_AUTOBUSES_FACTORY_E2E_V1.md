# E2E sintético de fábrica a auditoría de cliente: CS Autobuses

Este recorrido copia el generador y sus archivos directos de `origenes/` desde `P:\Frabica_GTFS` a un espacio aislado de runtime, produce allí un ZIP nuevo y lo entrega al flujo cliente de GTFS Lab. Conserva Frabica_GTFS como proyecto independiente y trata su salida exclusivamente como datos sintéticos.

## Qué ejecuta

`tools/factory_client_e2e.py` copia únicamente el generador y los archivos regulares de origen, rechaza reparse points y conserva hashes antes/después. Ejecuta `--generar-gtfs` y `--empaquetar-gtfs` sobre esa copia. Comprueba que el ZIP resultante tenga 32 archivos en la raíz, nombres únicos, archivos base esperados y CRC válido. A continuación ejecuta `run_client_audit` con procedencia `SYNTHETIC` y metadatos de la entidad ficticia CS Autobuses. Guarda las fuentes copiadas, el ZIP, la auditoría y su recibo en una carpeta nueva bajo `P:\TransitDataLab\04_Runtime\AuditQuality\FactoryE2E`.

El runner 1.7.0 relaciona el hash binario del ZIP con un manifest canónico de hashes por fichero y verifica inventario exacto, tamaños, hashes y sello. El workflow conserva en privado una copia con SHA-256 de los módulos Python de GTFS Lab cargados durante la ejecución; una referencia Git con cambios locales no basta para reconstruirlos. Preserva los bytes del input del productor y sus URL; la redacción se limita a metadatos de ejecución y texto de informes. La base DuckDB original permanece privada y se omite de la proyección cliente.

Un escaneo independiente inspecciona texto, PDF y, en la presentación completa, XLSX/KMZ. Si quedan formatos sin inspeccionar no se declara cobertura completa; la generación profesional exige `PASS`. El recibo E2E es interno. Las pasadas R1–R4 incluyen rutas locales y no deben compartirse; los ensayos parciales tampoco son entregas finales. Los artefactos y recibos históricos se conservan separados de la nueva ejecución.

## Ejecución

Desde `02_Data_Engineering\GTFS_Lab`:

```powershell
$pythonTdl = Join-Path $env:TDL_RUNTIME_ROOT 'Current\TDL\Scripts\python.exe'
& $pythonTdl -m tools.factory_client_e2e `
  --factory-root examples/cs_autobuses_factory `
  --output 'P:\TransitDataLab\04_Runtime\AuditQuality\FactoryE2E\CS_AUTOBUSES_NUEVA_EJECUCION' `
  --professional
```

La carpeta de salida debe ser nueva. Cada repetición debe utilizar un nombre distinto. Frabica_GTFS se lee sin cambios; regeneración y empaquetado ocurren en la copia del recibo. Instalar previamente `packaging/professional-audit-requirements.txt` en el runtime del proyecto. `--professional` incorpora informe PDF, LEEME PDF, libro de seis hojas y KMZ, junto con modelo, evidencias e inventario sellado; sin esa opción el recibo declara presentación no ejecutada.

## Interpretación y límites

`E2E_RECEIPT.json` acredita la ejecución de esta versión concreta del ZIP por el flujo cliente interno. Su estado de auditoría puede ser `COMPLETED_WITH_FINDINGS` o `COMPLETED_WITH_LIMITATIONS` y aun así completar el E2E. No equivale a un feed sin problemas.

La demostración se identifica como `DEMO`: no prueba cobertura universal, veracidad del servicio, licencias, titularidad, cumplimiento legal o aceptación/publicación por el NAP. La presentación profesional que incorpora decisiones por caso requiere revisión humana explícita; los casos pendientes no deben convertirse en decisiones implícitas. Con un cliente se parte del ZIP consolidado recibido y autorizado, sin regenerarlo en la fábrica, y se acuerdan alcance, perfil y destino. La aceptación NAP es posterior e independiente de la emisión de una auditoría previa a publicación. El registro de riesgos está en [CS_AUTOBUSES_E2E_RISK_REGISTER_V1.md](CS_AUTOBUSES_E2E_RISK_REGISTER_V1.md).

## Resultado observado el 10 de octubre de 2026

La ejecución final `CS_AUTOBUSES_20261010_REMEDIATED_FINAL_R14` terminó `E2E_PASS`, con 20/20 comprobaciones y auditoría `COMPLETED_WITH_LIMITATIONS`: cero hallazgos detectados en el alcance ejecutado, con capacidades no evaluables aún declaradas. El ZIP de 32 miembros queda ligado al SHA-256 `aff91b6018b8b8ef86a7cff23ed710c2960b7d1fba4f73874c510624f4c386fc`; el manifest canónico de contenido es `2f9e0073ec4c05c8f6a989f26c0ee0ef6d765a67b57beea132657dc7b8aa2918`. El SHA-256 de su recibo es `90c12405dfcc9596b5f39a79f6a10fa90ddad98cc64a47348a6ab917bbc53cb6`.

G03 FIELD-TYPE 1.1.0 corrige los dominios enumerados y resuelve los dominios referenciados del calendario. La comparación sobre el mismo ZIP R14 devuelve tres alertas con 1.0.0 y cero con 1.1.0; el contrato original permanece intacto y se puede reproducir con `inspect_g03_archive(..., type_revision="1.0.0")` o `pipeline.run(..., g03_type_revision="1.0.0")`. Las regresiones incluyen valores válidos, vecinos inválidos y los siete días. La corrección es del auditor, no una corrección del productor. Dominios contrastados con la [referencia GTFS](https://gtfs.org/documentation/schedule/reference/).

La presentación profesional está `GENERATED_FOR_HUMAN_REVIEW`: 74 artefactos inventariados y verificados, tres PDF inspeccionados (incluida la copia fuente), XLSX y KMZ, sin contenido opaco ni patrones de rutas locales detectados en el escaneo aplicado. Los 29 ficheros de input proyectados coinciden byte a byte con sus miembros del ZIP; la ejecución privada conserva 40 módulos con hash. Dos libros abren en Excel 16.0 y se revisaron 40 páginas renderizadas de informes y rangos de QA. Detalle reproducible en [el cierre de correcciones](CS_AUTOBUSES_REMEDIATION_20261010.md).

El estado de demo es `INTERNAL_DEMO_READY_WITH_LIMITATIONS`; la emisión real sigue `BLOCKED_FOR_CLIENT_ISSUANCE` por la fuente sintética y la revisión humana pendiente. Publicación NAP y aceptación visual GIS permanecen sin acreditar. La entrega R7 sigue verificando su sello/inventario. Su recibo actual tiene SHA-256 `243e8ce9c6fe1894404ffb9fbb691416b417a5572acecc0fa9d7fcc689e253c9`, distinto del hash escrito en la documentación anterior; se registra esa discrepancia sin atribuir su causa ni modificar el recibo histórico.

Para reproducir desde un checkout público, las fuentes sintéticas están versionadas en `examples/cs_autobuses_factory`, con manifest de integridad. Los recibos históricos citados describen la ejecución local y permanecen fuera de Git.
