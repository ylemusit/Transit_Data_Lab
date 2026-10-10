# Procedimiento de servicio V1

Ocho etapas con entradas, salidas, excepciones y responsables propuestos; API/CLI con historial reconstruible y versiones inmutables. Acuerdos y aceptaciones simulados no prueban una relación con un cliente real.

Esta es la documentación pública sanitizada. Los informes aplicados, resultados de operadores, paquetes privados y recibos completos se conservan localmente, fuera de Git. El checkout público permite comprobar los contratos y casos sintéticos; no reproduce por sí solo los expedientes históricos.

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m unittest tools.test_audit_service_v1 -v
```
