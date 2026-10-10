# Cierre de correcciones del E2E de CS Autobuses

Fecha: 2026-10-10. Resultado: problemas técnicos identificados corregidos y nueva ejecución sintética completa verificada. La entidad ficticia es **CS Autobuses**. Esta entrega sirve para demostración y revisión interna; no acredita operación real, cobertura universal ni aceptación externa.

## Cambios y alcance

| Problema | Corrección | Archivos principales |
|---|---|---|
| Dominios enum G03 mal normalizados y referencias de calendario ignoradas | Contrato nuevo 1.1.0, resolución de referencias y rechazo de dominios no resueltos. Reproducción explícita 1.0.0 conservada. | `spec/gtfs_schedule_fields_2026_04_27_revision_1_1.json`, `g03_structure.py`, `g03_field_contract.py`, `pipeline.py` |
| Redacción que podía modificar input y URL observadas | Input/CSV preservados, redacción de metadatos, protección de URL y comprobación de hashes antes de sellar. DuckDB original permanece privado. | `client_workflow.py` |
| Inventarios vacíos o archivos adicionales aceptados | Inventario exacto común, tamaños/hashes, referencias contenidas y rechazo de reparse points. | `delivery_integrity.py`, workflow, presentación y runner |
| PDF y binarios sin inspección declarados como seguros | Escaneo independiente de texto, PDF y XML/KML de XLSX/KMZ; cobertura parcial explícita y bloqueo de presentación incompleta. | `delivery_privacy.py` |
| Dependencia privada impedía generar la entrega completa | Renderer Python portátil de seis hojas, preflight con versiones fijadas, generación parcial y destino final tras verificación. Renderer Node anterior opcional explícito. | `professional_workbook.py`, `professional_audit.py`, requisitos de packaging |
| Referencia Git insuficiente con cambios locales | Snapshot privado y hashes de módulos GTFS Lab cargados; hashes de generadores, contrato y artefactos originales. | `client_workflow.py` |
| Confusión entre demo, auditoría y publicación | Rótulo DEMO en nuevas presentaciones y estados separados de uso/emisión/NAP. | `factory_client_e2e.py`, presentación, README, documentos de alcance/riesgos y ambos estados del proyecto |

Las regresiones nuevas son `tests/test_g03_enum_revision.py`, `tests/test_delivery_revision.py` y `tests/test_portable_professional_workbook.py`. `tools/professional_audit_synthetic.py` permite probar la presentación sin el runtime Node privado. No se alteraron el contrato G03 original, RAW ni entregas históricas. No se accedió a HOLDOUT, no se cambió la baseline y no hubo commit, publicación ni envío externo.

## Evidencia final

Raíz de ejecución: `P:\TransitDataLab\04_Runtime\AuditQuality\FactoryE2E\CS_AUTOBUSES_20261010_REMEDIATED_FINAL_R14`.

- Runner 1.7.0: `E2E_PASS`, 20/20 controles. Auditoría: `COMPLETED_WITH_LIMITATIONS`; 0 hallazgos detectados, manteniendo los controles no evaluables.
- ZIP exacto: SHA-256 `aff91b6018b8b8ef86a7cff23ed710c2960b7d1fba4f73874c510624f4c386fc`.
- Contenido canónico de 32 miembros: `2f9e0073ec4c05c8f6a989f26c0ee0ef6d765a67b57beea132657dc7b8aa2918`.
- `E2E_RECEIPT.json`: SHA-256 `90c12405dfcc9596b5f39a79f6a10fa90ddad98cc64a47348a6ab917bbc53cb6`.
- Presentación: `professional/01_RESULTADOS/Informe_auditoria.pdf`, `LEEME.pdf`, `Plan_de_accion_y_hallazgos.xlsx` y `Mapa_auditoria.kmz`. 74 artefactos inventariados/verificados, además de manifest y sello.
- Escaneo del paquete final: 71 archivos textuales, 3 PDF (incluida la copia fuente), XLSX y KMZ; `PASS`, sin formatos opacos o sin inspección y sin patrones de rutas locales detectados. No es un escaneo universal de secretos/datos personales, OCR ni análisis de binarios arbitrarios.
- Los 29 archivos de input que el motor proyecta coinciden byte a byte con sus miembros del ZIP. El ZIP completo y los artefactos originales se conservan en privado; no se afirma que los 32 miembros estén proyectados en input ni que todos sus campos tengan evaluador.
- Snapshot de 40 módulos GTFS Lab en `workflow/CS-AUTOBUSES-DEMO/E2E-CS-AUTOBUSES-FACTORY-V1/audit/execution_code`, comprobado contra los hashes del manifest. Permite identificar el código capturado; no sustituye la conservación del runtime completo.

Evidencia de cierre interna: `P:\TransitDataLab\04_Runtime\AuditQuality\FactoryE2E\CS_AUTOBUSES_REMEDIATION_20261010\REMEDIATION_CLOSURE_RECEIPT_FINAL.json`. Esa carpeta conserva copias/hashes anteriores, la comparación del mismo ZIP, fixtures y QA; no forma parte del paquete externo.

La comparación `G03_SAME_SOURCE_COMPARISON_FINAL_R14.json` utiliza el ZIP exacto R14: FIELD-TYPE 1.0.0 devuelve tres alertas y 1.1.0 devuelve cero. Se atribuye el cambio al auditor, sin afirmar corrección del productor. Se contrastaron los dominios con la [referencia oficial GTFS](https://gtfs.org/documentation/schedule/reference/). El hash del contrato original sigue siendo `b583ca329d4e034c5553a0ee6e1bcecf7bdb8c6736fe2cedad822302f5b9b4d6`.

La entrega histórica R7 sigue pasando verificación de sello/inventario. El hash actual de su recibo es `243e8ce9c6fe1894404ffb9fbb691416b417a5572acecc0fa9d7fcc689e253c9`; difiere de `dd67a7830b576db29b4d4892090018b627d4d024d7fe80f76e0b4fec0bfb6029`, escrito en la documentación anterior. Se registra la discrepancia y se corrige la referencia documental actual. No se deduce cuándo o por qué difirió ni se reescribe el recibo histórico.

## Verificación realizada

121 tests PASS en 13 módulos seleccionados, incluyendo regresiones nuevas y contratos G03, workflow, E2E, presentación, casos, interpretación, reporte y aplicación. `pip check` no detecta requisitos incompatibles.

Excel 16.0 abrió en modo lectura los libros R14 y del fixture revisado: 12 hojas en total, sin fórmulas ni conexiones inesperadas y sin guardar cambios. QA visual: 40 páginas renderizadas e inspeccionadas, entre todos los PDF de la demo, tres fixtures y las exportaciones de los rangos iniciales de las seis hojas de cada libro. Los rangos nativos revisados son A1:D8 y, en Resumen, A1:B22; no equivalen a inspección visual completa de todas las columnas o funciones del libro. Los datos completos y textos largos se verifican además mediante regresiones de reconstrucción. Matriz muestra campos principales y Ocurrencias conserva controles completos diferenciados de las ocurrencias de hallazgos.

Recibos: `visual_qa_release_r14/NATIVE_EXCEL_QA.json` y `PDF_RENDER_RECEIPT.json`. La aceptación visual GIS sigue pendiente conforme a `professional/02_EVIDENCIAS/MAP_MANUAL_PROTOCOL.md`; generar un KMZ válido no demuestra aceptación en un visor.

## Reproducción

Ejecutar desde `02_Data_Engineering\GTFS_Lab`, con una carpeta de salida nueva en cada pasada:

```powershell
$pythonTdl = 'P:\TransitDataLab\04_Runtime\Current\TDL\Scripts\python.exe'
& $pythonTdl -m pip install -r packaging/professional-audit-requirements.txt
& $pythonTdl -B -m unittest tests.test_g03_enum_revision tests.test_delivery_revision `
  tests.test_portable_professional_workbook tests.test_g03_field_contract `
  tests.test_g03_file_catalog tests.test_g03_aggregate_capability_map `
  tests.test_client_workflow tests.test_factory_client_e2e tests.test_professional_audit `
  tests.test_client_report tests.test_client_app tests.test_audit_case_contract `
  tests.test_audit_interpretation_contract -q
& $pythonTdl -B -m tools.factory_client_e2e --factory-root examples/cs_autobuses_factory `
  --output 'P:\TransitDataLab\04_Runtime\AuditQuality\FactoryE2E\CS_AUTOBUSES_NUEVA_EJECUCION' `
  --professional
```

Runtime de generación: jsonschema 4.25.1, reportlab 5.0.1, XlsxWriter 3.2.9 y pypdf 6.20.0. PyMuPDF 1.28.2 solo para QA local. Se instalaron las dependencias ausentes en el runtime TDL; no se modificó el directorio de dependencias de Codex.

## Uso y límites pendientes

`INTERNAL_DEMO_READY_WITH_LIMITATIONS` permite usar este recorrido sintético internamente. `GENERATED_FOR_HUMAN_REVIEW` identifica generación completa, no emisión aprobada. `BLOCKED_FOR_CLIENT_ISSUANCE` permanece por la procedencia sintética y la revisión humana. No se inventaron decisiones de cierre para conseguir un PASS.

Para un cliente real se recibe su ZIP consolidado autorizado, se conserva sin modificación, se fija alcance/perfil/destino, se ejecuta una auditoría nueva y se revisan los resultados y limitaciones antes de emitir. La aceptación de una carga en NAP es una operación posterior independiente; no impide emitir previamente un informe de errores. Fuentes operativas, decisiones humanas, cobertura pendiente y aceptación GIS/NAP requieren evidencia propia. El estado comercial y los pendientes externos 19/20/23 del backlog no se promueven por esta corrección técnica.

Para reproducir desde un checkout público, las fuentes sintéticas están versionadas en `examples/cs_autobuses_factory`, con manifest de integridad. Los recibos históricos citados describen la ejecución local y permanecen fuera de Git.
