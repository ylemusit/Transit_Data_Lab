# Entrega profesional V1: reproducción y límites

Esta capa utiliza una ejecución ya terminada y sellada. No ejecuta el motor, no cambia RAW, Compliance ni interpretación V1 y no modifica una entrega anterior. Un único modelo produce los dos PDF, el libro y el KMZ.

## Entradas y contrato

- `--delivery`: entrega existente con manifest, sello, interpretación, reporte del motor y Compliance.
- `--source-zip`: fuente exacta de esa ejecución, comprobada por SHA-256; solo se utiliza para el mapa.
- `--decisions`: entrada opcional explícita según `spec/reviewed_decisions_v1.schema.json`: `case_contract` V1, procedencia/versiones de criterios, perfiles de cierre y secuencia justificada. El contenido específico permanece fuera de Git.
- `--revision`: identidad de presentación distinta de la ejecución del motor.
- `--output`: carpeta nueva; se rechaza sobrescribir carpetas existentes.

`TDL_AUDIT_CASES_V1 1.0.0` no cambia. La envoltura `TDL_PROFESSIONAL_PRESENTATION 1.0.0` valida esquema completo, identidad, proyecciones, cobertura, localizadores, versiones, orígenes y relaciones. Los constructores privados anteriores se conservan como antecedentes y no son necesarios en esta ruta. Una decisión anterior sin envoltura debe aportar explícitamente procedencia, secuencia y perfiles; no se inventan al migrar.

Los registros sin decisión aparecen completos como revisión pendiente en modelo/libro. No reciben tratamiento de otro operador. Una entrada sin hallazgos no obtiene automáticamente aptitud para un destino no declarado. Matriz y evidencia conservan cobertura no evaluable y capacidades diferidas.

## Runtime y comando

Desde `02_Data_Engineering/GTFS_Lab`, utilizar el entorno Python del proyecto con `packaging/professional-audit-requirements.txt`: `jsonschema 4.25.1`, `reportlab 5.0.1`, `XlsxWriter 3.2.9` y `pypdf 6.20.0`. El generador 1.1.0 utiliza por defecto el renderer Python portátil; produce el paquete completo sin dependencia privada de Codex. El preflight exige esas versiones antes de crear salidas. QA visual utiliza `packaging/professional-audit-qa-requirements.txt` (PyMuPDF 1.28.2), separado de las dependencias de generación.

El renderer Node anterior permanece disponible cuando se proporcionan conjuntamente `--node` y `--workbook-script`. Esa ruta necesita su runtime `@oai/artifact-tool 2.8.59`; es una selección explícita, no un fallback automático. No distribuir ni modificar el paquete privado. Ejemplo PowerShell con rutas del encargo como parámetros:

```powershell
$pythonTdl = Join-Path $env:TDL_RUNTIME_ROOT 'Current/TDL/Scripts/python.exe'
& $pythonTdl -m pip install -r packaging/professional-audit-requirements.txt
& $pythonTdl -m gtfs_lab.client_workflow present --delivery $sealedDelivery `
  --source-zip $auditedZip --decisions $reviewedDecisions --revision $presentationRevision `
  --output $newDirectory
```

Sin decisiones, omitir `--decisions`; los resultados conservan revisión pendiente. «Abrir revisión profesional» en la aplicación selecciona una carpeta separada, verifica sello/inventario/modelo, muestra conclusión/siguiente paso y permite abrir informe, libro y mapa. No altera la ejecución anterior ni aprueba emisión. No se afirma aceptación manual de la interfaz nativa.

## Cierre y verificación

Cada caso exige condición, evidencia, comprobación y límite. Colores: vacío real o seis dígitos hexadecimales. Referencias: resolución, obligatoriedad y relación pretendida. Frecuencias: ambas cotas estrictas para salidas a horario fijo, horario deseado y tramos adyacentes. Distancias: progresión estricta, cálculo trazable y conservación de geometría y relaciones.

`technical_condition` comprueba condiciones acotadas, no intención ni conservación de servicio. `closure_verified` valida suficiencia declarada de comprobaciones del auditor, versión, correspondencia y evidencia. No ejecuta reauditoría ni sustituye la inspección de esos documentos. `RESOLVED` requiere evidencia y enlace concordantes de otra ejecución, excluidas ambas identidades actuales. Una respuesta del productor o ejecución enlazada por sí sola no basta. La aceptación de riesgo no elimina una infracción obligatoria. No se verificaron correcciones reales del productor.

La nueva carpeta contiene resultados, decisiones/modelo, controles GIS/protocolo, recibo y copia íntegra del delivery fuente. La generación se realiza en una carpeta `.partial`; solo se renombra al destino final después del escaneo de contenido y la verificación completa. Un fallo conserva material parcial sin habilitarlo como entrega. El recibo identifica versiones y hashes de generadores. `PACKAGE_MANIFEST.json` inventaría todos los archivos, incluidos los añadidos después del motor; `PACKAGE_SEAL.json` sella ese manifest. Solo se excluyen esos dos archivos en sus rutas propias. Se rechazan inventarios vacíos, archivos adicionales o ausentes, cambios de tamaño/hash, referencias que escapan de la raíz y reparse points.

`DELIVERY_CONTENT_SCAN.json` inspecciona texto UTF-8, texto/metadatos/anotaciones PDF y contenido XML/KML de XLSX/KMZ. Contenido opaco, adjuntos PDF o necesidad de OCR dejan cobertura parcial y bloquean la generación profesional. El alcance es detección de patrones de rutas locales; no equivale a auditoría universal de datos personales o secretos. El motor conserva su base DuckDB en el espacio privado; las nuevas entregas cliente omiten esa copia redundante y preservan los bytes de los archivos de entrada proyectados.

```powershell
& $pythonTdl -c "from pathlib import Path; from gtfs_lab.professional_audit import verify_package; print(verify_package(Path(r'$newDirectory')))"
& $pythonTdl -m unittest tests.test_professional_audit tests.test_audit_case_contract `
  tests.test_audit_interpretation_contract tests.test_client_report tests.test_client_workflow tests.test_client_app
& $pythonTdl -m tools.professional_audit_synthetic --output $newSyntheticDirectory
git diff --check
```

Los fixtures generan evidencia sintética sellada de estructura diferente, una entrada sin hallazgos y otra con familia no cubierta. No son auditorías reales del motor. `verify_package` reconstruye el modelo esperado desde fuente/decisiones, verifica bytes/tamaños y rechaza archivos fuera del inventario. Las seis hojas son Resumen, Casos, Ocurrencias, Seguimiento, Matriz y Evidencias. Matriz presenta las columnas principales; los controles técnicos completos también se conservan en Ocurrencias, identificados por tipo de registro, y en `PRESENTATION_MODEL.json`. Los campos largos se dividen en partes reconstruibles sin truncamiento. Las cadenas externas son literales, los recuentos son numéricos y el seguimiento editable no cierra casos.

En el cierre de CS Autobuses del 2026-10-10 se abrieron en Excel 16.0, en lectura y sin guardar, la entrega R14 y el fixture revisado: seis hojas por libro, sin fórmulas ni conexiones inesperadas. Se inspeccionaron 40 páginas renderizadas entre informes y rangos iniciales de las hojas; esta comprobación acotada no acredita todas las funciones de Excel ni aceptación del cliente. Evidencia y límites en [el cierre de correcciones](CS_AUTOBUSES_REMEDIATION_20261010.md).

GIS: coordenadas finitas WGS84, secuencia no ambigua y anclajes en filas fuente. Los casos no localizables no reciben puntos inventados; contexto no equivale a ausencia de defectos. `LookAt` codifica la extensión de datos, sin demostrar el zoom del visor. La aceptación visual exige el protocolo local suministrado y queda pendiente cuando las herramientas no permiten operar el visor.
