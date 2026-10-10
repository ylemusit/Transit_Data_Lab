# Replay aislado V1

Preparación y ejecución offline con manifiesto de entradas, guard de red, comparación semántica y módulos cargados. La preparación operacional usa el runtime autorizado de Windows; las pruebas públicas del cierre de imports usan temporales. No se acredita clean-machine ni otro SO por esas pruebas.

Esta es la documentación pública sanitizada. Los informes aplicados, resultados de operadores, paquetes privados y recibos completos se conservan localmente, fuera de Git. El checkout público permite comprobar los contratos y casos sintéticos; no reproduce por sí solo los expedientes históricos.

Desde la raíz del repositorio, con Python 3.12:

```powershell
python -m unittest tools.test_audit_replay_v1 -v
```
