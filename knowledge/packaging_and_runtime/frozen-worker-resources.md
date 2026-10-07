# Resolver recursos dentro del runtime empaquetado

- **CONTEXT:** El cliente usa GUI y worker separados en PyInstaller onedir.
- **PROBLEM / ROOT_CAUSE:** Las rutas del checkout y la codificación implícita no sirven como contrato de un ejecutable congelado.
- **DECISION_OR_SOLUTION:** Incluir recursos y DuckDB; resolver desde _MEIPASS/runtime_assets y forzar UTF-8 en el JSON que consume la GUI.
- **EVIDENCE / RELATED_COMMITS_OR_REPORTS:** [Fuente autoritativa](https://github.com/ylemusit/Transit_Data_Lab/blob/cf4e0a30f6837b077e6994305f51fbf2cca8282c/reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_P_PACKAGED_SHELL_INTEGRATION.md).
- **IMPACT:** El worker completó auditoría sintética con cwd externo, PATH reducido y sin PYTHONPATH/PYTHONHOME.
- **REUSABLE_LESSON:** Verificar paquete con dependencias del desarrollador ocultas; distinguir harness, GUI real y máquina limpia. Preservar hash/metadata del RC aceptado, regenerar el entorno de build cuando haga falta.
- **STATUS:** Retenido; alcance y límites de la fuente, sin nueva certificación.
