# Local Workspace Reconciliation R1 — resumen de cierre

## Propósito

Cerrar la reconciliación local R1 preservando los datos reales y los límites de protección, y registrar una política controlada para el material externo futuro.

## Método

Se aplicó limpieza segura de espacio temporal y artefactos locales prescindibles. Después se verificaron la integridad de Git y la conservación de la fuente versionada del proyecto. La documentación pública de cierre se limita a resultados sanitizados; el inventario operativo detallado permanece local.

## Resultado

- Espacio recuperado: **6,395,371,423 bytes** (aproximadamente 6,40 GB).
- Integridad del proyecto: la fuente versionada no fue afectada; integridad de Git verificada.
- Datos reales: preservados.
- Contenido protegido y HOLDOUT: no accedidos.
- Política de datos externos: el material externo permanente nuevo se restringe a `C:\TDL_DATA`.
- Residuos históricos: se conservan intencionadamente en su ubicación; las raíces históricas retenidas no recibirán trabajo nuevo. Una investigación o limpieza forense adicional no resulta coste-efectiva.

## Clasificación final

`WORKSPACE_RECONCILIATION_R1 = CLOSED_WITH_PROTECTED_LEGACY_RESIDUALS`
