# CS Autobuses — fábrica sintética DEMO

Fuentes copiadas de la fábrica independiente y verificadas byte a byte. `SOURCE_MANIFEST.json` fija los 37 archivos originales. Los atributos Git preservan esos bytes. El ejemplo es sintético: no acredita servicio real, conformidad jurídica ni aceptación NAP.

Desde GTFS_Lab, la ejecución local autorizada utiliza:

```powershell
python -m tools.factory_client_e2e --factory-root examples/cs_autobuses_factory --output "$env:TDL_RUNTIME_ROOT/AuditQuality/FactoryE2E/NUEVA_EJECUCION" --professional
```

La carpeta de salida debe ser nueva. El runner copia las fuentes y genera en runtime; no cambia el ejemplo ni la fábrica independiente. Instalar previamente las dependencias fijadas en `packaging/professional-audit-requirements.txt` y disponer del CLI DuckDB del proyecto. No ejecutar `--crear-origenes` sobre esta captura.
