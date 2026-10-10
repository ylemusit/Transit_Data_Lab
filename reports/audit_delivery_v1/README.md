# Entrega para dos audiencias V1

Modelo común y vistas para dirección y técnicos, inventario, referencias, sellos y comprobación de traslado. Los adaptadores existentes tienen alcance limitado; un paquete íntegro no aprueba emisión humana ni conformidad de destino.

Esta es la documentación pública sanitizada. Los informes aplicados, resultados de operadores, paquetes privados y recibos completos se conservan localmente, fuera de Git. El checkout público permite comprobar los contratos y casos sintéticos; no reproduce por sí solo los expedientes históricos.

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m unittest tools.test_audit_delivery_v1 -v
```
