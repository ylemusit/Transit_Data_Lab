# Diseño de baterías — TDL-AUD-10 y TDL-AUD-11

Fecha: 2026-10-09. **COMPLETADAS en alcance de diseño delimitado**, no implementación de nuevas reglas.

Diseño legible (referencia local no publicada) · Contrato y matriz de ramas (referencia local no publicada).

Se enlazan los 36 controles actuales con sus 108 fixtures, y se especifican 19 propuestas: nueve GTFS y diez NeTEx. Cada propuesta identifica prioridad, condición de aplicación, autoridad y escenarios positivo, negativo y de límite. Se conserva la disposición de los 32 archivos del catálogo y la matriz de 132 campos del inventario congelado; no representan todos los campos del formato ni una cobertura exhaustiva de sus ramas. Los fixtures propuestos están especificados, aún no materializados.

GTFS utiliza la captura fijada 2026-04-27 y localizadores por sección/campo/línea con huella de la fila fuente. Prioridad: condiciones de agencia, identidad/referencias y distinción entre orden lógico y orden físico; después calendario, horarios, frecuencias, geometría y unidades. Las recomendaciones se separan de los errores obligatorios. Las ramas de campos sin criterio suficientemente normalizado siguen pendientes de revisión, sin expectativas genéricas inventadas.

NeTEx conserva XML seguro, XSD 2.0.0 fijado, identidad, referencias, red/paradas, calendario, horarios y CRS como capas separadas. Las propuestas semánticas son diagnósticos TDL con contexto, no obligaciones CEN inventadas. EPIP 2026 completo y el contrato del destino están ausentes: sus aserciones normativas no pueden aprobarse. El esquema XSD y el perfil no son equivalentes. Un grafo JSON de referencia no es una publicación NeTEx.

Selección propuesta para 12/13: condiciones `agency_id` y referencias NeTEx con tipo/id/versión y ámbito. Antes de implementar: delimitar las reglas, materializar fixtures, revisar expectativas y comparar con baseline. La anomalía de diagnóstico CSV observada en 15 necesita priorización expresa en el incremento GTFS; no se ha reparado el motor congelado.

Reproducción desde la raíz, usando una carpeta nueva:

```powershell
& 'P:\TransitDataLab\04_Runtime\Current\TDL\Scripts\python.exe' -m tools.audit_battery_plan_v1 --output '<directorio nuevo de diseño>'
```

[Medición y discrepancias](../audit_precision_v1/README.md). No se amplía readiness, distribución, conformidad de perfil ni cobertura jurídica.
