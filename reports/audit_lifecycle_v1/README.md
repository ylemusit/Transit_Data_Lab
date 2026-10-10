# Seguimiento de correcciones V1

Registro lateral versionado de respuesta, nueva ejecución, resolución y aceptación. REPORTED_CORRECTED no equivale a RESOLVED. Las pruebas usan evidencia sintética temporal y no amplían las raíces autorizadas de producción.

Esta es la documentación pública sanitizada. Los informes aplicados, resultados de operadores, paquetes privados y recibos completos se conservan localmente, fuera de Git. El checkout público permite comprobar los contratos y casos sintéticos; no reproduce por sí solo los expedientes históricos.

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m unittest tools.test_audit_lifecycle_v1 -v
```
