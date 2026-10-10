# Medición delimitada V1

Comparación por criterio, abstenciones, discrepancias y contraste externo. El código conserva diferencias y no infiere precisión universal ni conformidad de perfil de una muestra limitada.

Esta es la documentación pública sanitizada. Los informes aplicados, resultados de operadores, paquetes privados y recibos completos se conservan localmente, fuera de Git. El checkout público permite comprobar los contratos y casos sintéticos; no reproduce por sí solo los expedientes históricos.

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m unittest tools.test_audit_precision_v1 tools.test_audit_external_review_v1 -v
```
