# Base de auditoría V1

Contrato de encargo, gate de categorías de conclusión, inventario de controles y correspondencia entre controles, casos y referencias. Los ejemplos públicos GTFS y NeTEx son sintéticos; sus hashes ilustrativos no acreditan una ejecución.

Esta es la documentación pública sanitizada. Los informes aplicados, resultados de operadores, paquetes privados y recibos completos se conservan localmente, fuera de Git. El checkout público permite comprobar los contratos y casos sintéticos; no reproduce por sí solo los expedientes históricos.

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m unittest tools.test_audit_foundation_v1 -v
```
