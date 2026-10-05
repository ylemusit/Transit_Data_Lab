# Transit Data Lab — estado vigente

**Mapa visual resumido:** [PROJECT_STATUS_TREE.md](PROJECT_STATUS_TREE.md). Actualizar ambos documentos en la misma tarea cuando un paso cambie el estado del proyecto; `PROJECT_STATUS.md` conserva el detalle y la evidencia.

## Windows Self-Service Client V1 — W02–W08 cerrados con limitaciones documentadas

**Estado (2026-10-05):** campaña `W02–W08 = PASS_WITH_LIMITATIONS` en `feat/windows-client-v1-w02-w08`, desde base `cbba86480ce6743ab57bf32f094ba95b6778bead`. PR [#51](https://github.com/ylemusit/Transit_Data_Lab/pull/51) abierta para revisión, sin merge; creada desde `e37999831d732ff8fb293e890e50caa3fa203c03`. CI de PR completa en verde en el HEAD `d8ad7123837421d8a1c2b4271b8ecd3d2a362da1` (workflow `synthetic`, run `37271159392`); su ajuste de test refleja el PDF opcional no bloqueante. El RC `1.0.0-rc.1` se construyó en onedir desde el commit limpio `d050f536c29fb58106d6924055015e75ab621eb7`; metadata externa: `C:\TDL\windows-client-v1-w08-build-final-rc1\build-metadata.json` (SHA-256 `441259F22C34F82674C833E2D98032A13C932971D425E91B99FEF806D43BE805`). Regresión GTFS_Lab: 311 tests OK, 3 skips; suite client con worker final: 25/25 PASS; `py_compile`, `git diff --check`, instalación/desinstalación de ensayo: PASS. Clean-machine `PARTIAL / BLOCKED_BY_ENVIRONMENT`, aceptación visual/manual GUI pendiente. No se accedió a HOLDOUT; sin lógica específica de operador ni cambios semánticos al motor/compliance/interpretación. Detalle W08: [informe](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W08_PACKAGING_RELEASE.md).

`W03_AUDIT_EXECUTION = PASS_WITH_LIMITATIONS`; `W04_RESULTS = PASS_WITH_LIMITATIONS`; `W05_GIS_QGIS = PASS_WITH_LIMITATIONS`; `W06_REPORTING_EXPORT = PASS_WITH_LIMITATIONS`; `W07_RELIABILITY = PASS_WITH_LIMITATIONS`; `W08_PACKAGING_RELEASE = PASS_WITH_LIMITATIONS`. Build RC limpio y regresión final completados. No hay VM externa/Sandbox; clean-machine permanece parcial. La GUI RC requiere aceptación visual/manual humana. No se accedió a HOLDOUT y no hay cambios semánticos al motor ni a los contratos de interpretación/compliance.

Informes: [W03 ejecución](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W03_AUDIT_EXECUTION.md), [W04 resultados](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W04_RESULTS.md), [W05 GIS/QGIS](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W05_GIS_QGIS_BRIDGE.md), [W06 informes/exportación](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W06_REPORTING_EXPORT.md), [W07 fiabilidad](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W07_RELIABILITY.md), [W08 packaging/release](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W08_PACKAGING_RELEASE.md).

### W01 — Application Shell — CLOSED_WITH_NONBLOCKING_LIMITATIONS

**Estado (2026-10-05):** `W00 = CLOSED_WITH_RESOURCE_LIMITATION`; `W00_PUBLICATION = COMPLETE`; PR #49 fusionada en `6271a75399732dfafcaef06ec5fd63ff5835a86b`; post-merge CI run `37256036471 = SUCCESS` sobre ese SHA. `W01_APPLICATION_SHELL = CLOSED_WITH_NONBLOCKING_LIMITATIONS`; `W01 acceptance = PASS`; aceptación humana `W01-F = W01F_PASS_READY_FOR_W01_CLOSURE`. La GUI compilada superó interacción real, éxito, cancelación, apertura de entrega, exclusión de segunda instancia, salida y reinicio; tests automatizados 7/7 PASS. `PACKAGED_ONEDIR = PASS`; `DUCKDB_BUNDLED = YES`. `CLEAN_MACHINE_VALIDATION = PENDING` para fase posterior de packaging/release. `W02 = NEXT / NOT_STARTED`. Decisión humana W00: `W00-P = W00P_PASS_WITH_RESOURCE_LIMITATION`. `W00-R = diagnostic infrastructure complete`; `W00-O = root cause initially unknown`; `W00-M = synthetic root cause probable`; `W00-P = PASS_WITH_RESOURCE_LIMITATION`.

`gtfs_lab.core.write_json` usa el serializer W00-P validado: `JSONEncoder.iterencode`, lotes de 65.536 caracteres y salto final conservado. La comparación determinista S4 da igualdad byte a byte; la equivalencia semántica cubre identidad, referencias de evidencia, findings, accounting, interpretación, semántica de informes y versiones de contrato. El replay sintético pasa. La medición diagnóstica por escritura se retiró del camino normal; los marcadores opcionales de etapa permanecen disponibles para el harness de benchmark.

Con muestreo a 100 ms, el pico privado del proceso árbol baja de 67.112.960 a 45.068.288 B en S1 (−32,85 %), de 321.392.640 a 86.949.888 B en S4 (−72,95 %) y de 4.662.751.232 a 866.676.736 B en S64 (−81,41 %). La etapa del pico observado cambia de serialización/escritura a `AUDIT`. El tiempo total cambia entre −0,47 % y +15,03 % según escala; en S64 aumenta 4,14 %. Estos son picos muestreados, no high-water marks del sistema. La causa de memoria queda `CONFIRMED` para la reproducción sintética, sin extrapolar a dataset 019.

Dataset 019 queda `DEFERRED_FOR_HIGH_MEMORY_ENVIRONMENT`; HOLDOUT no se accedió. El onedir reconstruido en la máquina de desarrollo arrancó, completó S1 y contiene DuckDB CLI 1.5.5; `CLEAN_MACHINE_VALIDATION = PENDING`. No se establece hardware mínimo ni recomendado, ni se certifica soporte extremo para feeds grandes. QGIS sigue siendo un banco externo de evidencia GIS; la integración no está implementada. No se afirma preparación de instalador de producción, compatibilidad en máquina limpia, preparación comercial, validación de mercado, soporte universal de feeds ni requisitos mínimos de RAM.

Regresión completa del cambio consolidado: **291 tests, 290 PASS, 0 FAIL y 1 SKIP documentado** por la base de Compliance V1 respaldada fuera del checkout. Resultado: [resumen de regresión](reports/evidence/windows_client_v1/w00/regression_summary.json).

Informes W00: [R — medición y subprocesos](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_RUNTIME_RESOURCE_READINESS.md), [M — aislamiento de causa raíz](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_M_MEMORY_ROOT_CAUSE_ISOLATION.md), [P — optimización JSON](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_P_JSON_SERIALIZATION_OPTIMIZATION_PROOF.md), [inventario y política de publicación](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_CONSOLIDATION_INVENTORY.md). Evidencia compacta: [manifiesto before/after](reports/evidence/windows_client_v1/w00/json_streaming_optimization/w00p_before_after_manifest.json), [comparación semántica](reports/evidence/windows_client_v1/w00/json_streaming_optimization/semantic_comparison_final.json), [inventario de runtime](reports/evidence/windows_client_v1/w00/runtime_inventory.json), [evaluación de empaquetado](reports/evidence/windows_client_v1/w00/packaging_pyinstaller_onedir.json) y [manifiesto de limpieza propuesto](reports/evidence/windows_client_v1/w00/proposed_cleanup_manifest.json). Las salidas completas permanecen locales y fuera de Git.

### W01 — Application Shell — CLOSED_WITH_NONBLOCKING_LIMITATIONS

La primera entrega añade una interfaz local con `tkinter`: seleccionar un ZIP y una carpeta de destino, iniciar una auditoría inicial, cancelar el proceso y abrir la carpeta de entrega. La interfaz lanza `gtfs_lab.client_workflow` como subproceso en modo fuente y `tdl-worker.exe` en el onedir; no importa ni duplica el motor dentro del proceso de la GUI. Cada ejecución recibe un identificador interno nuevo y un workspace dedicado. Los registros técnicos se guardan junto a la carpeta elegida; no se borran automáticamente.

`QGIS = EXTERNAL`; la GUI no lo inicia ni lo configura. No se modifican Interpretation, HOLDOUT ni la semántica del motor. La aceptación manual final confirmó diálogo real, éxito E2E compilado, entrega, cancelación antes de éxito normal y parada de ficheros, rerun, mutex entre EXE, continuidad de la primera instancia, salida/reinicio; procesos huérfanos finales = 0. Tests automatizados = 7/7 PASS, `py_compile = PASS`, `git diff --check = PASS`. `CLEAN_MACHINE_VALIDATION = PENDING` y se reserva a packaging/release posterior. Permanecen: feeds extremos sin certificación; hardware mínimo/recomendado no establecido; instalador de producción no declarado listo; presentación PDF/informes en W06; ingeniería de releases posterior. W01 está cerrado con esas limitaciones; W02 es siguiente y no iniciado.

Diseño, cierre y aceptación: [W01 Application Shell](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_APPLICATION_SHELL.md), [W01-P](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_P_PACKAGED_SHELL_INTEGRATION.md) y [W01-F](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_F_FINAL_PACKAGED_GUI_ACCEPTANCE.md). Punto de entrada actual: `02_Data_Engineering/GTFS_Lab/gtfs_lab/client_app.py`.

## Audit Interpretation & Consolidation V1 — VALIDATED WITH DOCUMENTED LIMITATIONS

**Estado (2026-10-04):** Yeison aprobó el resultado técnico de generalización de HOLDOUT. `FINAL_HUMAN_GENERALIZATION_DECISION = APPROVED`; `GENERALIZATION_RESULT = GENERALIZATION_PASS_WITH_LIMITATIONS`; `AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = VALIDATED_WITH_DOCUMENTED_LIMITATIONS`. `INTERPRETATION_HARDENING_V2 = NOT_REQUIRED_NOW`; G04 specialized interpretation queda como `BACKLOG_CANDIDATE`.

`HOLDOUT_EVIDENCE_PUBLICATION = PUBLISHED`; PR #47 está fusionada en `69567c4a82d65e3017ee74ce64695a6a8334aa46` y su CI post-merge terminó PASS (run `37230388650`). `GENERALIZATION_PUBLICATION = COMPLETE`.

La validación completó 6/6 datasets (casos 00025–00030): 5 interpretados, 1 parcialmente interpretado, 0 no soportados y 0 fallos de pipeline. Se registraron 530 findings raw y 3 familias consolidadas; accounting gaps = 0; replay = 6 PASS / 0 FAIL; falsas consolidaciones candidatas = 0. ENGINE_CHANGED = NO; código específico de operador = 0. G04 REFERENCE-EXISTENCE continúa en consolidación genérica. G07 EXACT_DUPLICATE_GEOMETRY se observó en HOLDOUT. En el dataset 017 (caso 00029), los 529 tránsitos G07 iguales se desglosaron en 6 geometrías duplicadas exactas y 523 compatibles con cuantización.

El historial de protocolo se conserva sin reescribir la declaración anterior al freeze: `HOLDOUT_METADATA_PRE_FREEZE_EXPOSURE = YES`; `HOLDOUT_CONTENT_PRE_FREEZE_EXPOSURE = NO`; `HOLDOUT_CONTENT_ACCESSED_AFTER_FREEZE = YES`; `PRISTINE_BLIND_HOLDOUT = NO`; `CONTENT_BLIND_HOLDOUT = YES`. Los ficheros funcionales versionados no cambiaron durante HOLDOUT: freeze merge `3fba5cbabee000267a511c65b9bc8d90a78b8880`; base funcional `9cafe0703abf47e80f67f80a6b423c938e1979aa`.

La regresión final registró 280 tests, 279 PASS, 0 FAIL y 1 SKIP documentado; `git diff --check = PASS`. Se preservan estas limitaciones: G04 especializado no implementado; un dataset HOLDOUT parcialmente interpretado; tres datasets DEVELOPMENT parcialmente interpretados; optimización de memoria para feeds grandes pendiente; sin claims de preparación comercial, validación de mercado, cumplimiento legal o cobertura GTFS completa. `WINDOWS_SELF_SERVICE_CLIENT_V1 = NEXT`; `W00_RUNTIME_RESOURCE_READINESS = NOT_STARTED`. No se inicia V2.

Resultados y protocolo: [informe HOLDOUT](reports/TDL_AUDIT_INTERPRETATION_V1_HOLDOUT_CONTENT_BLIND_20261004.md), [resumen JSON](reports/evidence/audit_interpretation_v1/holdout_content_blind_summary.json) y [manifiesto de evidencia por caso](reports/evidence/audit_interpretation_v1/holdout_content_blind_manifest.json). Los seis paquetes publicables están preservados con artefactos de entrega generados y replay, sin registros que expongan `original_filename` ni fuentes raw. La reconciliación por caso reproduce 530 findings, 3 familias, 6/6 replay PASS y cero gaps; el caso 00026 es el único parcialmente interpretado por G04 en consolidación genérica.

## Audit Interpretation & Consolidation V1 — FROZEN WITH DOCUMENTED LIMITATIONS

**Estado (2026-10-04):** Yeison aprobó el freeze después de la campaña DEVELOPMENT. `DEVELOPMENT_CORPUS_CAMPAIGN = PASS_WITH_PROTOCOL_DEVIATION`; `INTERPRETATION_V1_FREEZE_DECISION = APPROVED`; `AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = FROZEN_WITH_DOCUMENTED_LIMITATIONS`. La implementación queda fijada en `ENGINE_FREEZE_BASE = 9cafe0703abf47e80f67f80a6b423c938e1979aa`; este SHA no incluye la documentación de freeze.

La campaña completó 14/14 datasets, 14/14 replays PASS, 92 findings raw, 7 familias, cero fallos de pipeline y cero gaps de accounting. 11 datasets quedaron interpretados y 3 parcialmente interpretados: 010 por un hallazgo G03 en consolidación genérica; 011 por dos familias G04 en consolidación genérica; 016 por tres recomendaciones informativas G08 en consolidación genérica. No se añadió interpretación ausente. No hubo fixes genéricos, tests nuevos requeridos por la campaña ni código específico de operador. No se autoriza tuning conductual antes de una validación HOLDOUT controlada.

Durante el reconocimiento inicial se listaron por error directorios por familia, exponiendo nombres/IDs de carpetas asignadas a HOLDOUT. `HOLDOUT_ACCESSED = YES`; `HOLDOUT_ACCESS_LEVEL = METADATA_ONLY`; `HOLDOUT_DIRECTORY_NAMES_EXPOSED = YES`. No se leyó contenido, abrieron fuentes, calcularon hashes ni ejecutó el pipeline; HOLDOUT tampoco se usó para tuning, fixes o diseño de tests. `PRISTINE_BLIND_HOLDOUT = NO`; `CONTENT_BLIND_HOLDOUT = YES`. Los seis datasets permanecen protegidos de acceso a contenido hasta autorización separada.

Dataset 019 terminó `OK`, replay `PASS` y cero findings: runtime observado ≈12m43s y pico observado de memoria privada ≈18.89 GiB. `LARGE_DATASET_FUNCTIONALITY = PASS`; `LARGE_DATASET_PERFORMANCE_OPTIMIZATION = REQUIRED`; no se establece SLA ni se modifica runtime en este freeze. La regresión registrada sigue siendo 280 tests, 279 PASS, 0 FAIL y 1 SKIP documentado.

Hallazgos y evidencia por caso: [informe de campaña](reports/TDL_AUDIT_INTERPRETATION_V1_DEVELOPMENT_CORPUS_20261004.md) y [resumen JSON](reports/evidence/audit_interpretation_v1/development_corpus_summary.json). No se inició Windows Self-Service Client V1.

## Audit Interpretation & Consolidation V1 — PASS; cierre humano aprobado

**Estado vigente (2026-10-04):** Yeison aprobó el cierre técnico humano de I01–I08. La rama `feat/audit-interpretation-i02-i08` parte de `62224c13246bb0cda5cb4fc48b1409789abfcc1f`; esta aprobación no declara aceptación comercial, jurídica ni de mercado.

```ini
WORKSPACE_RECONCILIATION_R0 = CLOSED
FINAL_HUMAN_CLOSURE_DECISION = APPROVED
I01 = CLOSED
I02 = CLOSED
I03 = CLOSED
I04 = CLOSED
I05 = CLOSED
I06 = CLOSED
I07 = CLOSED
I08 = PASS / CLOSED
AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = PASS
AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1_CLOSED = YES
I01_SCHEMA_SHA256 = 9AE821BA963849D341F509A74956DEF76C5739BD8175150198EA6A5F99CA7BD4
GENERIC_CONSOLIDATION = PASS
DETERMINISTIC_FAMILY_ID = PASS; INJECTIVE_CANONICAL_BASE64URL
RAW_CARDINALITY_PRESERVED = PASS; ACCOUNTING_GAP = 0
GENERIC_IMPACT_GRAPH = PASS; DIRECT_VS_PROPAGATED = PASS
G07_GEOMETRY_INTERPRETER = PASS; SYNTHETIC_BUCKETS = 6_OF_6
JSON_MARKDOWN_REPORTING = PASS; I01_SCHEMA_UNCHANGED = YES
CLIENT_WORKFLOW_AND_TEST_BANK = PASS; INTERPRETATION_REPLAY = PASS
TESTS = 280
PASS = 279
FAIL = 0
SKIP = 1 DOCUMENTED
WINDOWS_SELF_SERVICE_CLIENT_V1 = DEFERRED
HOLDOUT_ACCESSED = NO
DEVELOPMENT_CORPUS_EXECUTED = NO
COMMERCIAL_VALIDATION = NOT_ESTABLISHED
MARKET_VALIDATION = NOT_ESTABLISHED
LEGAL_COMPLIANCE = NOT_CLAIMED
FULL_GTFS_COVERAGE = NOT_CLAIMED
OPERATOR_SPECIFIC_CODE = 0
```

Implementación, resultados, límites y registro de esta decisión: [revisión de cierre](reports/TDL_AUDIT_INTERPRETATION_CONSOLIDATION_V1_I08_CLOSURE_REVIEW.md). El contrato I01 y su fixture históricos se conservan sin cambios. El intérprete especializado es genérico para G07; el resto de reglas se agrupa sin inventar semántica específica. Se preservan los 279 PASS, 0 FAIL y el único SKIP documentado (prueba que requiere la base Compliance V1 protegida). No se accedió a HOLDOUT ni se ejecutó el corpus DEVELOPMENT de 14 datasets. La validación comercial y de mercado no está establecida; no se reclama cumplimiento legal ni cobertura GTFS completa.

## Real Dataset Test Bank V1 — CLOSED; cierre humano aprobado

Capa genérica aditiva sobre Client Audit Workflow V1: captura de identidad, Case IDs no reutilizables, workspace corto configurable, SOURCE inmutable por hash, preflight, auditoría, replay, entrega y clasificación procedural. OK significa procedimiento completo, incluso con findings; NOT_OK significa contrato incompleto. El expediente real EMT Palma permanece LOCAL / CONTROLLED, intacto y fuera de Git. Solo se publica capacidad genérica y evidencia sintética.

REAL_DATASET_VALIDATION_V1 = EMT PALMA LOCAL CASE COMPLETED.
REAL_DATASET_TEST_BANK_V1 = CLOSED.
REAL_DATASET_TEST_BANK_V1_CLOSED = YES.
REAL_DATASET_TEST_BANK_V1_HUMAN_CLOSURE_DECISION = APPROVED.
REAL_DATASET_TEST_BANK_V1_TECHNICAL_REVIEW = PASS.
SELF_SERVICE_READINESS = NOT_READY.
COMMERCIAL_VALIDATION = NOT_ESTABLISHED.
MARKET_VALIDATION = NOT_ESTABLISHED.
HOLDOUT = NOT_ACCESSED.
OPERATOR_SPECIFIC_CODE = NO.

Aceptación verificada en GitHub: PR [#40](https://github.com/ylemusit/Transit_Data_Lab/pull/40) MERGED; HEAD 202eb5997e2383defc916626a2be2bbd4df848e7; merge 3cd14d55003671f1a8926018a05fdc22044e99f6. CI PR [37023905768](https://github.com/ylemusit/Transit_Data_Lab/actions/runs/37023905768) PASS y CI post-merge [37024096727](https://github.com/ylemusit/Transit_Data_Lab/actions/runs/37024096727) PASS. Ambos ejecutaron las 18 pruebas del banco, 3 del workflow y el E2E sintético OK/NOT_OK con DuckDB PASS, replay, registros persistidos y hashes/sellos después de clasificación. Artefactos remotos descargados y comprobados; sin datos reales. [Evidencia remota](02_Data_Engineering/GTFS_Lab/reports/evidence/test_bank_v1/remote_acceptance_20261002.json) y [revisión técnica](02_Data_Engineering/GTFS_Lab/reports/TDL_TEST_BANK_V1_TECHNICAL_REVIEW_20261002.md).

Cierre humano final aprobado explícitamente por Yeison el 2026-10-02, tras verificar directamente en GitHub PR #40 y #41, los cuatro runs PASS y main 378c75aa29e3d5d8e292fbfdc1c68f77e7b23ecb. [Registro de aprobación y alcance](02_Data_Engineering/GTFS_Lab/reports/evidence/test_bank_v1/human_closure_20261002.json). Queda cerrado el banco en el alcance demostrado, con aceptación procedural independiente de la cantidad de findings. Las incidencias históricas Windows/DuckDB resueltas permanecen como conocimiento operacional, sin convertirse en fallos nuevos del caso final.

Límites preservados: SERIAL_EXECUTION = CURRENT_LIMITATION; CRASH_RECOVERY = MANUAL; FORMAT_SCOPE = GTFS_SCHEDULE. No se declara autoservicio listo ni validación comercial o de mercado.

Al cierre original del Test Bank, el siguiente bloque seleccionado fue WINDOWS SELF-SERVICE CLIENT V1 (`NEXT`; implementación `NOT_STARTED`). El estado vigente de W00 se registra al inicio de este documento. Objetivo del cliente: doble clic → seleccionar GTFS.zip → introducir datos mínimos → analizar → ver progreso → recibir resultado comprensible → abrir informe o carpeta de entrega. El usuario final debe poder operar sin terminal, Python, Git, VS Code, rutas manuales, JSON, DuckDB ni comandos. Este bloque encapsulará el flujo cerrado; no abre nuevos datasets, formatos ni cambios de motor. No se abrirá otro dataset durante el desarrollo inicial del cliente Windows. Contrato y operación: [TEST_BANK_V1.md](02_Data_Engineering/GTFS_Lab/TEST_BANK_V1.md). CI incluye tests específicos, E2E sintético OK/NOT_OK, hashes y sellos después de la clasificación. Trust Foundation, GTFS Audit Engine V1, Compliance V1, Remediation Engine V1, Client Audit Workflow V1 y NeTEx Audit Engine V1 se conservan.

## REAL DATA HARDENING CAMPAIGN V1 — PASS; CLOSED

**Cierre documental (2026-10-02):** PASS dentro del alcance controlado de GTFS Schedule y snapshots públicos históricos. Los conteos de datasets, intentos, resultados y findings proceden del resumen local de campaña y sus registros bajo `C:\TDL\BANK`; esos artefactos no forman parte de este clean worktree. Por tanto, se registran como resultados de la campaña local controlada y no como verificación local desde el repositorio. No se publican artefactos reales de operadores ni se fabrica evidencia Git sustitutiva.

`00007_NOT_OK` se conserva como evidencia histórica. El mismo SHA terminó posteriormente en `00008_OK` tras una corrección general de memoria; la recuperación no borra ni reclasifica el intento histórico.

```ini
REAL_DATA_HARDENING_CAMPAIGN_V1 = PASS
REAL_DATA_HARDENING_CAMPAIGN_V1_CLOSED = YES
UNIQUE_REAL_DATASETS_FINAL_OK = 7
TOTAL_CASE_ATTEMPTS = 9
TOTAL_OK_ATTEMPTS = 8
HISTORICAL_NOT_OK_PRESERVED = YES
OPEN_GENERAL_FAILURES = 0
ALL_REQUIRED_REPLAYS = PASS
OPERATOR_SPECIFIC_CODE = 0
HOLDOUT_ACCESSED = NO
PR43 = MERGED
PR43_HEAD = 822438151bb1bf21ff54ea1f20519d2e19ae83c5
PR43_MERGE = fe7fc77d0d65be439845468da937325279f5aeec
CI_PR43 = PASS; RUN 37033717647
CI_POST_MERGE_PR43 = PASS; RUN 37033908847
```

El merge de PR #43 es `origin/main` en la base de este cierre. El resultado respeta estos límites: solo GTFS Schedule; snapshots públicos históricos; procedencia/licencia incompleta para varios snapshots; ejecución serial; recuperación manual ante crashes; optimización de rendimiento en feeds grandes pendiente. La suite fue `262 PASS` y `1 documented SKIP`; no se declara 100 % ejecutada. En Compliance, los tests pasaron, el hash gate de la base protegida no se volvió a ejecutar durante esta campaña y la base no se modificó. No queda establecida validación comercial ni de mercado.

```ini
WINDOWS_SELF_SERVICE_CLIENT_V1 = NEXT
NEXT_PROJECT_OBJECTIVE = WINDOWS_SELF_SERVICE_CLIENT_V1
WINDOWS_SELF_SERVICE_CLIENT_V1_STATUS = NOT_STARTED
```

Este siguiente objetivo queda seleccionado, sin iniciar implementación.

## GTFS Productization / Client Audit Workflow V1 — CLOSED

**Estado verificado (2026-10-02):** PR #34 se fusionó mediante merge normal. Head `20da5f0e45b597c58074eb444035dce22bd57e34`; merge commit y `origin/main` `b28959c52aca5c0aeb60c0483267dab12ba6a139`. CI de PR #34 pasó en el run `36962646709`; CI post-merge pasó en el run `36962713037`. Ambos ejecutaron `test_client_workflow.py` y el E2E sintético de Client Audit Workflow V1. No se modificaron contratos ni código de Trust Foundation, Audit Engine V1, Compliance V1 o Remediation Engine V1.

El flujo recibe un ZIP, copia y verifica SOURCE, registra identidad cliente/dataset, ejecuta el pipeline existente, mantiene findings por origen (`AUDIT_ENGINE`, `AUDIT_ENGINE_RECOMMENDATION`, `COMPLIANCE`, `LEGACY`), genera decisión de remediación, soporta comparación con baseline, genera informe cliente y entrega manifest + seal. Los artefactos de DELIVERY se hashean; las rutas locales Windows y POSIX se redactan y comprueban. No hay uploads externos.

E2E DEVELOPMENT sintético reproducible: [evidencia local](02_Data_Engineering/GTFS_Lab/reports/evidence/client_audit_workflow_v1/e2e_synthetic_20261002_r7.json) y ejecución remota registrada en los logs de los runs CI indicados. El E2E comprobó SOURCE inmutable, igualdad byte a byte de `engine_report.json` con la misma entrada, hashes de artefactos, manifest y seal generados, ausencia de rutas locales, ningún upload externo y ningún acceso a HOLDOUT o feeds de cliente. La ejecución recurrente conserva `PARTIALLY_COMPARABLE / RUNTIME_ONLY_CHANGE`; no se elevó a `FULLY_COMPARABLE`. Los runs sintéticos terminaron `COMPLETED_WITH_LIMITATIONS`, manteniendo los gaps del motor.

```ini
PR34 = MERGED_NORMAL
PR34_HEAD = 20da5f0e45b597c58074eb444035dce22bd57e34
PR34_MERGE_COMMIT = b28959c52aca5c0aeb60c0483267dab12ba6a139
ORIGIN_MAIN = b28959c52aca5c0aeb60c0483267dab12ba6a139
PR34_CI = PASS; RUN 36962646709
POST_MERGE_CI = PASS; RUN 36962713037
CLIENT_WORKFLOW_TESTS_REMOTE = PASS (3/3)
CLIENT_WORKFLOW_E2E_REMOTE = PASS
BASELINES = PASS
CI = PASS
P01 = CLOSED
P02 = CLOSED
P03 = CLOSED
P04 = CLOSED
P05 = CLOSED
P06 = CLOSED
P07 = CLOSED_WITH_DOCUMENTED_LIMITATION
P08 = CLOSED
P09 = CLOSED
P09_TECHNICAL_REVIEW = PASS
P09_FINAL_CLOSURE_DECISION = APPROVED
GTFS_CLIENT_AUDIT_WORKFLOW_V1_HUMAN_CLOSURE_DECISION = APPROVED
GTFS_CLIENT_AUDIT_WORKFLOW_V1 = CLOSED
GTFS_CLIENT_AUDIT_WORKFLOW_V1_CLOSED = YES
CLIENT_REAL_FEED_TESTED = NO
COMMERCIAL_READINESS = NOT_ESTABLISHED
MARKET_VALIDATION = NOT_ESTABLISHED
HOLDOUT = NOT_ACCESSED
OPERATOR_SPECIFIC_CODE = NO
NETEX_WORK = CLOSED; DOCUMENTED_V1_SCOPE_ONLY
```

La decisión humana final aprueba P09 y el cierre técnico formal de V1 dentro del alcance documentado. P07 conserva `PARTIALLY_COMPARABLE / RUNTIME_ONLY_CHANGE`; no se declara comparabilidad recurrente completa. La Remediation V1 existente solo permite una propuesta de caso exacto DEVELOPMENT 010; el workflow no inventa safe fixes genéricos. Findings con posibles acciones quedan `HUMAN_REVIEW` hasta que haya evidencia y autorización caso por caso. Este cierre no acredita feeds reales de operadores, readiness comercial, validación de mercado, demanda, certificación, cumplimiento jurídico total, remediación universal ni calidad de clientes. Código, contrato, pruebas y procedimiento están en `02_Data_Engineering/GTFS_Lab/gtfs_lab/client_workflow.py`, `spec/client_audit_contract_v1.schema.json`, `reports/TDL_GTFS_CLIENT_AUDIT_WORKFLOW_V1_DESIGN_AND_CONTRACT.md`, `tests/test_client_workflow.py` y `tools/client_workflow_e2e.py`.

## GTFS Audit Engine V1 — cierre técnico V1 publicado

**Estado vigente (2026-10-01):** PR #29 se fusionó mediante merge normal en `d5c770d5015faa856963a363e14da24124da5a12`; CI post-merge PASS, run `36809106494`. Yeison aprobó expresamente el cierre humano final G11. Este estado acredita el cierre técnico del alcance documentado de GTFS Audit Engine V1.

```ini
PR29 = MERGED_NORMAL
PR29_HEAD = 44e92012b1ab8a27b232b69154abc043c55d21e8
PR29_MERGE_COMMIT = d5c770d5015faa856963a363e14da24124da5a12
MAIN = d5c770d5015faa856963a363e14da24124da5a12
PR29_CI = PASS; RUN 36808289990
POST_MERGE_CI = PASS; RUN 36809106494
G08 = PASS / CLOSED
G08_CLOSED = YES
G09 = PASS / CLOSED
G09_CLOSED = YES
G10 = PASS / CLOSED
G10_CLOSED = YES
G11_TECHNICAL_REVIEW = PASS
G11 = PASS
G11_CLOSED = YES
FINAL_HUMAN_G11_CLOSURE_DECISION = APPROVED
GTFS_AUDIT_ENGINE_V1 = PASS
GTFS_AUDIT_ENGINE_V1_CLOSED = YES
GTFS_AUDIT_ENGINE_V1_CLOSURE_DATE = 2026-10-01
HOLDOUT = NOT_ACCESSED
M02_CHANGED = NO
OPERATOR_SPECIFIC_CODE = NO
GTFS_COMPLETE_COVERAGE = NOT_CLAIMED
LEGAL_COMPLIANCE = NOT_CLAIMED
COMMERCIAL_VALIDATION = NOT_CLAIMED
```

### DEVELOPMENT y evaluabilidad G03–G08

G10 recuperó y verificó por SHA-256 los 14 feeds DEVELOPMENT del split aprobado; los 14 pipelines terminaron, hubo cero errores y la repetición de estabilidad pasó. HOLDOUT no se abrió ni se leyó. No se aplicaron umbrales agregados inventados: la cobertura se expresa como conteos de estados por regla.

- **G03:** 106 campos ejecutables, 11 parcialmente ejecutables y 15 condiciones sin resolver. En el replay persistieron `CONDITION_UNKNOWN` (1.682.207), `UNRESOLVED_CONDITION` (168), `UNRESOLVED_EXTENSION_POLICY` (11), `UNRESOLVED_TYPE_FORMAT` (23) y `UNSUPPORTED_LEXICAL_VALIDATOR` (39). Política de extensiones no resuelta; semánticas de vacíos no especificadas y evidencia insuficiente permanecen sin evaluación.
- **G04:** identidad de dominio, 32.002 evaluaciones (13 feeds PASS y un finding técnico); unicidad, 102 evaluaciones y 80 no aplicables; existencia de referencias, 1.168.910 evaluaciones, 83 no evaluables y 158 no aplicables. Las 83 no evaluables se atribuyen a cabeceras opcionales/condicionales ausentes. El inventario de identidad continúa `CREATED_LOCAL_UNPUBLISHED` como deuda contractual conocida.
- **G05:** 417 rangos de calendario; 13 feeds evaluables para conjunto de fechas y uno no evaluable por dependencia de identidad G04 en `011`. Rango de feed: 6 PASS, 7 no aplicables y uno no evaluable (`016`, valor de fecha ausente). Frecuencias y ventanas pickup/drop-off no aplicaron al corpus.
- **G06:** secuencia de paradas evaluada en 558.810 filas y PASS en 14/14. Orden temporal entre paradas queda `NOT_EVALUABLE` / `DEFERRED_BY_SCOPE`, porque la referencia fijada no establece un MUST de monotonía. Frecuencias no aplicaron.
- **G07:** nueve PASS, cuatro no aplicables y un finding técnico de progresión de distancia en `014`.
- **G08:** tres recomendaciones informativas de presencia de `feed_start_date`, `feed_end_date` y `feed_version`; siete PASS y siete no aplicables. No evalúa valores ni calidad integral del servicio.

Se mantiene el finding técnico de `010 / agency.txt / agency_url` (URL sin esquema) y el de `011` para referencias `service_id` sin resolver; no se añadieron excepciones por operador. Ningún cambio introdujo código específico por operador o dataset.

### Gaps, features diferidas y límites

G03 mantiene las condiciones sin resolver, gaps de tipos/formato, política de extensiones abierta y semánticas de valores vacíos no definidas; los casos sin evidencia suficiente siguen `NOT_EVALUABLE`. G04 mantiene su inventario local no publicado y findings que no forman parte de `validation.findings`. No se declara equivalencia total entre el engine y el validador legacy.

Los 18 archivos diferidos por G01, sin auditoría completa, son `fare_attributes.txt`, `fare_rules.txt`, `timeframes.txt`, `rider_categories.txt`, `fare_media.txt`, `fare_products.txt`, `fare_leg_rules.txt`, `fare_leg_join_rules.txt`, `fare_transfer_rules.txt`, `areas.txt`, `stop_areas.txt`, `networks.txt`, `route_networks.txt`, `location_groups.txt`, `location_group_stops.txt`, `locations.geojson`, `booking_rules.txt` y `attributions.txt`. GTFS-RT, SIRI y NeTEx también quedan fuera del producto V1 de GTFS Schedule.

`M02_CHANGED = NO`: M02 no normaliza los findings G03–G09, no registra el informe G09 y no se cambió su contrato. El validador legacy continúa generando su salida independiente. No se declara cumplimiento GTFS completo, cumplimiento jurídico, certificación, readiness comercial, demanda ni equivalencia con legacy.

### Decisión humana registrada

La decisión humana final G11 está aprobada. El cierre no constituye certificación, cumplimiento jurídico/completo ni aprobación comercial. El registro de decisión está en [g11_closure_candidate.json](02_Data_Engineering/GTFS_Lab/reports/evidence/g11_closure_candidate.json) y la evidencia detallada en el [review G11](02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_V1_G11_CLOSURE_REVIEW_20261001.md).

## Remediation Engine V1 — cierre técnico aprobado

**Estado vigente (2026-10-02):** decisión humana final aprobada; se cierra el alcance técnico documentado de Remediation Engine V1. PR #31 se fusionó mediante merge normal (`c7d3c820fab470b2796fe1384324052a53bad825` → `80d14e8d08250bcef617dfc95145d8e160a99fe4`); CI pre-merge PASS (run `36959598923`) y post-merge PASS (run `36959638138`). PR #32 registró la evidencia de publicación y se fusionó (`297a4cb1b31754a055c04e881ba68b276303a6eb` → `9bb905647bdda95244e43756a9bacb19a09a7b6f`); su workflow post-merge terminó `success` (run `36959780975`). `origin/main` queda en `9bb905647bdda95244e43756a9bacb19a09a7b6f`. El cierre cubre un caso DEVELOPMENT real acotado y no implica autocorrección general ni cobertura integral.

```ini
REMEDIATION_ENGINE_V1_HUMAN_CLOSURE_DECISION = APPROVED
REMEDIATION_ENGINE_V1 = PASS
REMEDIATION_ENGINE_V1_CLOSED = YES
FIRST_REAL_REMEDIATION_CASE = PASS
REMEDIATION_SCOPE = TECHNICAL_CLOSURE_OF_DOCUMENTED_V1_SCOPE
ORIGINAL_DATASET_UNCHANGED = YES
SOURCE_SHA256_VERIFIED = YES
DERIVED_DATASET_CREATED = YES
ONLY_AUTHORIZED_VALUE_CHANGED = YES
CHANGE_ATTRIBUTION_COMPLETE = YES
ORIGINAL_FINDING_RESOLVED = YES
NEW_UNRELATED_FINDINGS = 0
REAUDIT_REPRODUCIBLE = YES
HOLDOUT_ACCESSED = NO
GTFS_AUDIT_ENGINE_V1 = CLOSED / UNCHANGED
COMPLIANCE_V1 = CLOSED_WITH_DEFERRALS
M02_CHANGED = NO
OPERATOR_SPECIFIC_CODE = NO
ORIGINAL_DATASETS = IMMUTABLE
```

Caso `010` (DEVELOPMENT), source SHA-256 `3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf`; derivado SHA-256 `ce78c804770250165daeace125cd01c4649122c7cfc1843bb0b0fd8a1b2d2691`. El único cambio fue `agency.txt / ROW:1 / agency_url`, `empresarodil.es` → `https://empresarodil.es`. La atribución vincula el finding `GTFS-G03-FIELD-TYPE` con `RESOLVED`; el replay produjo las mismas proyecciones y cero findings nuevos. El original permanece inmutable. Evidencia completa: [informe del caso](02_Data_Engineering/GTFS_Lab/reports/TDL_REMEDIATION_ENGINE_V1_FIRST_CASE_20261002.md), [registro machine-readable](02_Data_Engineering/GTFS_Lab/reports/evidence/remediation_v1/dataset_010_case_20261002.json) y [contrato/caso](02_Data_Engineering/GTFS_Lab/reports/TDL_REMEDIATION_ENGINE_V1_FIRST_CASE_20261001.md).

```makefile
REAUDIT_CORE_G03_G07 = PASS / REPRODUCIBLE
G08_REMEDIATION_REAUDIT = NOT_EVALUABLE / NOT_INTEGRATED_IN_REMEDIATION_PIPELINE_V1
G08_INTEGRATION = KNOWN_V1_LIMITATION
```

G08 se ejecutó como módulo opcional aislado y quedó `NOT_EVALUABLE` en A/B y replay porque G03 no estableció estructura fiable de `feed_info.txt`. No se declara PASS completo G03–G08 del pipeline de re-audit. G08 recomienda sobre campos de `feed_info.txt`; no es causal para el cambio probado en `agency_url`. Remediation Engine V1 no se amplía para integrarlo.

```java
010 agency_url = SAFE_DETERMINISTIC / HUMAN_APPROVED_CASE_SPECIFIC
011 unresolved references = HUMAN_REVIEW_REQUIRED / NOT_SAFE_AUTOMATICALLY
014 shape distance progression = HUMAN_REVIEW_REQUIRED / NOT_SAFE_AUTOMATICALLY
```

No automatizar `011` ni `014` por falta de evidencia suficiente es comportamiento esperado del safety model. Los gaps restantes son la cobertura de un único caso probado, la falta de re-audit G08 integrado y los casos ambiguos/no autorizados que requieren revisión humana; tampoco se afirma cobertura de todos los findings, enriquecimiento inventado, remediación jurídica, tuning por operador ni autocorrección universal GTFS. No se accedió a HOLDOUT ni se inició ningún track posterior.

## Dirección estratégica — primer año

**Prioridad del núcleo del producto:** España + GTFS + NeTEx. GTFS Productization / Client Audit Workflow fue el objetivo de la fase de productización ya completada y cerrada en V1; no es el siguiente objetivo futuro. El flujo entregable fue ZIP GTFS → freeze e identidad → Audit Engine → Compliance → findings → remediación segura → re-audit → evidencia GIS cuando proceda → informe para el cliente.

El alcance de la fase incluyó workflow de auditoría de cliente, empaquetado de evidencias, informes entregables, comparación before/after, mantenimiento recurrente y operación reproducible. El cierre técnico del workflow no equivale a readiness comercial ni a validación con clientes.

NeTEx fue la prioridad técnica del año 1 junto con la productización GTFS; ambos alcances V1 están cerrados. SIRI, GTFS-RT y Colombia quedan deliberadamente en backlog posterior y no se inician como consecuencia de este cierre.

```ini
YEAR_1_PRODUCT_CORE = SPAIN + GTFS + NeTEx
HISTORICAL_PHASE_OBJECTIVE = GTFS_PRODUCTIZATION / CLIENT_AUDIT_WORKFLOW
HISTORICAL_PHASE_OBJECTIVE_STATUS = COMPLETED; GTFS_CLIENT_AUDIT_WORKFLOW_V1_CLOSED
CURRENT_NEXT_PROJECT_OBJECTIVE = WINDOWS_SELF_SERVICE_CLIENT_V1_W01_AFTER_W00_PUBLICATION
WINDOWS_SELF_SERVICE_CLIENT_V1_W01 = NOT_STARTED
SIRI = POST_COMMERCIALIZATION_BACKLOG
GTFS_RT = POST_COMMERCIALIZATION_BACKLOG
COLOMBIA = POST_COMMERCIALIZATION_BACKLOG
COMMERCIAL_VALIDATION = NOT_ESTABLISHED
```

## GTFS Audit Engine V1 — G02 y G03 cerrados

`G02 = PASS`, `GTFS_AUDIT_ENGINE_V1_RULE_REGISTRY = CLOSED` y `G02_DOCUMENTATION = DURABLE`. PR #23 se fusionó mediante merge normal el 2026-09-30: base `8e2b1cac53e96f4000f8be0d9c03da4350edfbee`, head revisado `6b01198d089100e425d5e1bc165a7be34adda888` y merge commit `36259cdbbc42cc6d2958ce4bd21e5279e7c1657c`, que es el `main` remoto verificado. El check `synthetic` verde corresponde al head de PR, no se afirma CI post-merge para el merge documental. Véase el [informe de cierre G02](reports/repository_integrity/TDL_GTFS_AUDIT_ENGINE_G02_CLOSURE.md).

```ini
G03 = PASS
G03_CLOSED = YES
G03_STATUS = CLOSED
G03_BASE = 36259cdbbc42cc6d2958ce4bd21e5279e7c1657c
G03_MERGE_COMMIT = 7047a9cf8408446f47bcb2325207e9923adb1d9e
G03_FILE_CATALOG = IMPLEMENTED_TESTED_MERGED
G03_CSV_STRUCTURE = IMPLEMENTED_TESTED_MERGED
G03_FIELD_CAPABILITY_MAP = IMPLEMENTED_TESTED_MERGED
G03_PRESENCE_CONDITIONS = 16_RUNTIME_RESOLVED; 15_OUTSTANDING
G03_FIELD_TYPE_FORMAT = IMPLEMENTED_PARTIAL_TESTED_MERGED
G03_FIELD_CONTRACT = PRESENT_MERGED
G03_FIELD_CONTRACT_VALIDATION = VALIDATED_WITH_METADATA_GAPS
G03_SPEC_METADATA_GAP = OPEN
G03_MAIN_VERIFICATION = PASS
G03_FIELD_CAPABILITY_MAP_COUNTS = 106_EXECUTABLE_G03; 11_PARTIALLY_EXECUTABLE_G03; 15_UNRESOLVED_CONDITION
G03_HEADER_SCHEMA = CONDITION_RUNTIME_CONNECTED_TESTED_MERGED
G03_EXTENSION_POLICY = NOT_NORMATIVELY_RESOLVED
G03_TARGETED_REGRESSION = PASS_REMOTE
G03_FULL_TEST_DISCOVERY = 164_TESTS; 163_PASS; 1_SKIP_EXTERNAL_DB (PRE-MERGE)
G03_REMOTE_REVIEW = PASS_SECOND_REVIEW
G03_REMOTE_REVIEW_FINDINGS = REMEDIATED_LOCAL_AND_PUBLISHED
G03_LOCAL_POST_REVIEW_VERIFICATION = PASS
G03_REMOTE_HEAD = 79a235be7109120c8a96aeea4b65c43e3f77a7e0
G03_REMOTE_ACTIONS_RUN = 36758403975; SUCCESS (POST-MERGE)
G03_REMOTE_G03_TESTS = 49/49_PASS
G03_REMOTE_HISTORICAL_SUITES = PASS
G03_REMOTE_WHITESPACE_GATE = PASS
G03_MERGE = PASS
G03_REMOTE_REVIEW = PASS
G03_DOCUMENTATION_ALIGNMENT = PASS
G03_KNOWN_GAPS = PRESERVED
G03_G04_AT_G03_MERGE = NOT_STARTED
G03_PUBLICATION = MERGED
```

G03 se desarrolló en un worktree dedicado desde `main`, en la rama `feat/gtfs-engine-g03-structure-schema-types`; el checkout original con modificaciones locales se conserva intacto. El resultado G03 es aditivo y separado de `validation` legacy. La revisión remota pidió cambios en semántica de cobertura parcial, validación léxica de `LANGUAGE_CODE`/`TIMEZONE` y CI G03. La remediación se publicó en commits `52f2e6403806445f59f12c56b8f39e819762c5cd` y `59633a04413404e23d8c6c3eca0b3f8ada1c9bd8`, conservando el commit original `c64c2309aba81764b046509f205de9a6f8916390`. La segunda revisión remota sobre `79a235be7109120c8a96aeea4b65c43e3f77a7e0` fue PASS. La PR #24 se fusionó el 2026-09-30 a las 18:24:56 UTC; `main` remoto apunta al merge commit `7047a9cf8408446f47bcb2325207e9923adb1d9e`, cuyos padres son la base `36259cdbbc42cc6d2958ce4bd21e5279e7c1657c` y el head revisado indicado. El workflow post-merge Actions `36758403975` terminó en `success`, incluyendo compilación, fuentes legales portables, suites sintéticas de confianza/comparación/corpus/precondiciones y whitespace. En el head de PR, G03 obtuvo 49/49 PASS, las cinco suites históricas y `Repository whitespace integrity` PASS sobre el merge ref. El capability map en `main` cuenta 106 `EXECUTABLE_G03`, 11 `PARTIALLY_EXECUTABLE_G03` y 15 `UNRESOLVED_CONDITION`. La reducción de 113 a 106 ejecutables refleja una clasificación más conservadora al excluir tipos sin validador léxico implementado. `G03 = PASS / CLOSED` corresponde al alcance estructural implementado y verificado; las brechas de metadatos normativos y la política de extensiones permanecen explícitas y no se declaran resueltas. Identidad y referencialidad quedaban para G04 en ese checkpoint; el trabajo de G04–G07 se documenta en la sección vigente superior y en el paquete de revisión local fechado 2026-10-01. Este cierre no equivale a cumplimiento GTFS completo ni acredita cumplimiento jurídico. A fecha del merge G03, no se ejecutó HOLDOUT ni se había iniciado G04.

El burn-down normativo G03 del 2026-09-30 conserva las brechas identificadas: de 31 condiciones, 16 se normalizaron y ejecutan; 10 dependen de otras etapas/multirregistro, 1 de una feature diferida y 4 siguen declaradas sin regla machine-executable en el contrato actual. Permanecen 4 gaps de tipo/formato. La revisión de ownership de las dos condiciones de ventanas mantiene las reglas de presencia condicional en G03 y las comparaciones entre valores horarios en G05, sin normalizarlas ni ampliar el runtime. La revisión formal inicial registró tres hallazgos, resueltos en la remediación documentada en el [paquete de revisión formal G03](02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G03_FORMAL_REVIEW_BUNDLE_20260930.md). La verificación pre-merge obtuvo 164 tests: 163 PASS y un `SKIP` explícito porque falta la DB Compliance protegida. Estas limitaciones permanecen registradas y no reabren el alcance G03 cerrado. El registro `G03_G04_AT_G03_MERGE` describe ese punto histórico; el estado vigente G04–G07 figura al inicio del documento.

## Desarrollo posterior a la base del GTFS Audit Engine

PR #21 está cerrada y fusionada. Su merge commit fue `d7f4c76ce5c13844ea49303f0434f83d31d95a4c`, con padres `4bb2275d9792942d5c879ca22d01fa250413457f` y `dc486d37a681975d18d4e9914f0a59cfcad59641`, `merged_at = 2026-09-30T01:19:27Z`; cerró `G01 = PASS` y `GTFS_AUDIT_ENGINE_V1_SCOPE = CLOSED`. Main avanzó posteriormente con PR #22, registrada arriba. La evidencia de precondiciones de G01 queda en [el pack de cierre](reports/repository_integrity/TDL_GTFS_ENGINE_PRECONDITIONS_PACK_CLOSURE.md).

G02 incorporó el registro de reglas tipado, applicability trazable, cobertura, estado nativo versionado e identidad registrada separada de la ejecución. Su cierre y regresión están documentados en el [informe G02](reports/repository_integrity/TDL_GTFS_AUDIT_ENGINE_G02_CLOSURE.md). El registro sigue sin gobernar la validación productiva; GTFS_Lab V1 conserva sus resultados. ChangeAttribution 1.0.0 y `MANIFEST_VERSION = 1.1.2` permanecen intactos; ChangeAttribution 1.1.0 recibe identidad por regla.

Actualizado: 2026-10-01. Sustituye únicamente las afirmaciones operativas obsoletas de las instantáneas anteriores; no promueve ni modifica sus baselines. Evidencia y límites en [la revisión](reports/repository_integrity/PROJECT_ALIGNMENT_REVIEW.md).

## Identidad y repositorios

| Elemento | Estado comprobado |
| --- | --- |
| Proyecto global | Transit Data Lab, siete áreas conceptuales incluyendo Business. |
| Raíz local | Rama main; el estado operativo se comprueba en Git y no se fija aquí un SHA de HEAD que quedaría obsoleto al publicar. Baseline validada antes del checkpoint M05B: `8358cfa7974c5b65e193dcba0f1da544ae786211`. |
| Baseline raíz | `tdl-baseline-v0.1` apunta a la baseline histórica `3c122f48ce4425c2e34313a2a65dcb9218bc77f5`; no representa el HEAD actual ni la versión del producto Desktop. |
| Remoto raíz | `https://github.com/ylemusit/Transit_Data_Lab.git`; el HEAD remoto de `main` se verifica al publicar cada checkpoint. |
| Remoto Desktop | `https://github.com/ylemusit/GTFS-Explorer-Desktop.git`; historia independiente del contenedor. |
| Baseline Desktop | `v0.2.2` → `85c700587ffec06d73d84825e1951fb73259b62c`, local y remota. |
| HEAD Desktop | `07e2c2a64766144dba4c4b6136157d5bb8291226` observado el 2026-09-30; posterior a la etiqueta `v0.2.2`, con historia independiente. |
| Visibilidad | Ambos repositorios públicos según consulta GitHub actual. Las declaraciones anteriores de privacidad son históricas. |

Los informes `REMOTE_GITHUB_ALIGNMENT.md`, `REMOTE_HISTORY_REVIEW.md` y `LEGACY_REPOSITORY_RENAME_READINESS.md` documentan el estado anterior a la separación efectiva de los remotos. El bloqueo UNRELATED_HISTORIES de esos informes no describe la relación actual entre HEAD raíz y su origin/main. No se deben fusionar historias para resolver un bloqueo ya superado.

El working tree de Desktop figura limpio en la comprobación del 2026-09-30, en HEAD `07e2c2a…`; esto no lo convierte en un checkout de la etiqueta `v0.2.2` ni valida funcionalmente los commits posteriores. Engineering, Artifacts y el restore requieren comprobación propia antes de afirmar su estado actual. Las 20 entradas locales de Desktop registradas en la revisión anterior son una observación histórica.

## NeTEx Audit Engine V1 — cierre técnico del alcance documentado

**Estado vigente (2026-10-02):** decisión humana final aprobada. PR #36–#38 están fusionadas; PR #36 merge `01689e8dd8b326c758f1df68433a03e87bc8c177`, PR #37 merge `4601886b426b3295a5e726bbc25da9cd20c06263` y PR #38 merge `accb3834e95e65675ac6bb148073b3a69930f7ac`. `origin/main` verificado en `accb3834e95e65675ac6bb148073b3a69930f7ac`. CI PR #36 run `36970572860` PASS; post-merge run `36970665306` PASS; CI final post-merge run `36971109479` PASS. N01 queda `CLOSED_WITH_LIMITATIONS`; N02–N09 quedan `CLOSED`.

El motor inspecciona XML/ZIP estáticos contra NeTEx v2.0.0 desde el root `NeTEx_publication.xsd`, fijado al commit upstream `a94e5e1752bcc13aabb8a1f3d018dc08e6978f42` y 458 hashes de XSD. El repositorio contiene el manifiesto, no redistribuye XSD ni avisos/licencias upstream; CI obtiene la fuente fijada temporalmente. El corpus es sintético. HOLDOUT y feeds públicos o de operadores no fueron accedidos; no hay código por operador.

La evaluación EPIP/CEN completa permanece `HUMAN_REVIEW_REQUIRED` por falta del texto controlado completo y de perfil español/NAP verificable. La aplicabilidad normativa de autobús por carretera queda sin concluir: el mapeo distingue el artículo 4(1)(a) del Reglamento 2024/490, su referencia a 2015/962 y la derogación de este por 2022/670; no infiere obligación NeTEx desde 4(1)(b). No se acredita conformidad jurídica, certificación, aceptación NAP, cobertura completa, validación de mercado ni preparación comercial.

```ini
NETEX_AUDIT_ENGINE_V1_HUMAN_CLOSURE_DECISION = APPROVED
N01 = CLOSED_WITH_LIMITATIONS
N02 = CLOSED
N03 = CLOSED
N04 = CLOSED
N05 = CLOSED
N06 = CLOSED
N07 = CLOSED
N08 = CLOSED
N09 = CLOSED
NETEX_AUDIT_ENGINE_V1 = PASS
NETEX_AUDIT_ENGINE_V1_CLOSED = YES
TECHNICAL_CLOSURE_OF_DOCUMENTED_NETEX_V1_SCOPE = YES
TARGET_MARKET = SPAIN
TARGET_MODE = REGULAR_SCHEDULED_BUS
DATA_DOMAIN = STATIC_SCHEDULED_PASSENGER_INFORMATION
PR36 = MERGED; MERGE = 01689e8dd8b326c758f1df68433a03e87bc8c177
PR36_CI = 36970572860; PASS
PR36_POST_MERGE_CI = 36970665306; PASS
PR37 = MERGED; MERGE = 4601886b426b3295a5e726bbc25da9cd20c06263
PR38 = MERGED; MERGE = accb3834e95e65675ac6bb148073b3a69930f7ac
FINAL_MAIN = accb3834e95e65675ac6bb148073b3a69930f7ac
FINAL_POST_MERGE_CI = 36971109479; PASS
NETEX_SCHEMA_BASELINE = v2.0.0
NETEX_SCHEMA_BASELINE_STATUS = APPROVED_WITH_LIMITATIONS
PROFILE_NORMATIVE_BASELINE = CEN/TS 16614-4:2026 / EPIP
EPIP_NETEX_V2_COMPATIBILITY = PARTIAL
FULL_EPIP_2026_CONFORMANCE = NOT_ESTABLISHED
SPANISH_ADDITIONAL_NATIONAL_PROFILE = NOT_IDENTIFIED_IN_PUBLIC_SOURCES_REVIEWED
NAP_PUBLIC_ACCEPTANCE_CONTRACT = NOT_IDENTIFIED
LEGAL_APPLICABILITY_TO_REGULAR_BUS = UNRESOLVED
LEGAL_CERTIFICATION = NO
FULL_NETEX_COVERAGE = NO
COMMERCIAL_READINESS = NOT_ESTABLISHED
MARKET_VALIDATION = NOT_ESTABLISHED
HOLDOUT = NOT_ACCESSED
PUBLIC_FEEDS_TESTED = NO
OPERATOR_FEEDS_TESTED = NO
OPERATOR_SPECIFIC_CODE = NO
NETEX_SCHEMA = V2.0.0; PINNED_COMMIT; 458_DEPENDENCY_HASHES
NETEX_CORPUS = SYNTHETIC_ONLY
NETEX_HOLDOUT_ACCESSED = NO
NETEX_PUBLIC_OR_OPERATOR_FEEDS_ACCESSED = NO
NETEX_CI = PASS; PR_RUN 36970572860; POST_MERGE_RUN 36970665306; FINAL_POST_MERGE_RUN 36971109479
```

Baselines protegidas confirmadas sin cambios por este cierre:

```ini
TRUST_FOUNDATION = CLOSED / UNCHANGED
GTFS_AUDIT_ENGINE_V1 = CLOSED / UNCHANGED
COMPLIANCE_V1 = CLOSED_WITH_DEFERRALS / UNCHANGED
REMEDIATION_ENGINE_V1 = CLOSED / UNCHANGED
GTFS_CLIENT_AUDIT_WORKFLOW_V1 = CLOSED / UNCHANGED
```

## Estado por área

| Área | Estado y límites |
| --- | --- |
| 01_Research_Standards | Estructura planificada, sin implementación observada en la baseline. |
| 02_Data_Engineering | GTFS_Lab V1 `STABLE / CHECKPOINTED` en el checkpoint de `main`. M04-A4 `M04A_SPLIT_APPROVED_FROZEN_AND_RECONCILED`: `CorpusSplit 1.0.0`, 14 DEVELOPMENT y 6 HOLDOUT (`006, 008, 013, 015, 017, 018`), equivalentes a cinco unidades lineage porque 013/015 son una sola. M04-B1 conserva su evidencia histórica inmutable. M04-B3 HOLDOUT V2 completado sobre los seis datasets y cinco unidades lineage; cierre humano aprobado como `M04_GENERALIZATION_HOLDOUT_CLOSED`. Se acepta la limitación `HOLDOUT_V2_HASH_ACCESS_TIMESTAMP_NOT_CAPTURED`; los timestamps nulos permanecen intactos. Véase el [informe B3](reports/GTFS_LAB_M04B3_HOLDOUT_REPLAY_V2.md) y el [registro de cierre](02_Data_Engineering/GTFS_Lab/reports/evidence/holdout_evaluation_v2/human_closure.json). M05-A/B/C/D están fusionados y verificados. El [cierre técnico M05](02_Data_Engineering/GTFS_Lab/reports/TDL_M05_CLOSURE.md) documenta `M05_CHANGE_ATTRIBUTION = PASS`. Tras la revisión, el merge de la PR #17 (`b6a27438417ff79c61a737690ea5f6b0c5e3c537`) y la regresión posterior, `M01 = PASS`, `M02 = PASS`, `M03 = PASS`, `M04 = PASS`, `M05 = PASS` y `TDL_TRUST_FOUNDATION = PASS` como gate técnico. Este PASS no acredita que el GTFS Audit Engine esté completo, ni cumplimiento jurídico, preparación NeTEx, preparación comercial o validación de mercado. [Aprobación M04-A4](02_Data_Engineering/GTFS_Lab/reports/GTFS_LAB_M04A4_SPLIT_APPROVAL.md). Gate, E2E sintético y py_compile PASS; el dry run Asturias completó ingestión, reglas locales, análisis, GIS y DuckDB sin findings. El resultado Compliance V1 de B1 para los feeds a escala fue `INSPECTION_ERROR`, no un finding ni una conclusión sobre operadores; en B3 Compliance V2 completó PASS en los seis datasets. Integración Compliance sintética PASS. ZIP original, base raw congelada y Compliance permanecen intactos. [Estado V1](02_Data_Engineering/GTFS_Lab/GTFS_LAB_V1_CURRENT_STATE.md) · [Informe](02_Data_Engineering/GTFS_Lab/reports/GTFS_LAB_V1_STABILIZATION_REPORT.md). GTFS-RT y SIRI siguen fuera de alcance. |
| 03_Compliance | **COMPLIANCE_V1_IMPLEMENTATION_V2_APPROVED_AND_FROZEN**; Compliance V1 continúa CLOSED_WITH_DEFERRALS; Phase 1/2 FROZEN (92 provisions, 36 source facts, 48 requirements, 10 deadlines); Phase 3 CLOSED_WITH_DEFERRALS bajo alcance GTFS/NeTEx V1. GTFS y NeTEx READY / OPERATIONAL_COMPLIANCE_TRACK exclusivamente en dos scopes técnicos reproducibles con fixtures sintéticos; SIRI y GTFS-RT STANDBY. B02 CLOSED_WITH_DEFERRALS intacto. 15 mappings y 10 coverage sin cambios (9 PARTIAL, 1 UNRESOLVED); 2 assertions PARTIAL, 28 observaciones sintéticas, 2 reglas técnicas sin conclusión jurídica. Gate vigente PASS; +44 filas en una transacción, cero migraciones. Regla `V1-RULE-GTFS / compliance-v1/1`, evaluator actual `compliance-v1/2` SHA `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; paquete SHA `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`; DB hash `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`. [Vista vigente](03_Compliance/COMPLIANCE_V1_CURRENT_STATE.md) · [Informe maestro](03_Compliance/reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md) · [Transición M04-B2D](reports/GTFS_LAB_M04B2A_COMPLIANCE_PACKAGE_TRANSITION.md). |
| 04_Interoperability | Mappings pendientes; no se presupone conversión 1:1. |
| 05_Audits | Estructura planificada; evidencia de 20 operadores ubicada en GTFS_Lab. |
| 06_Products | Desktop, Engineering, Artifacts y backups separados del índice raíz. Desktop baseline 0.2.2 protegida. |
| 07_Business | V1 FROZEN; Business Phase 3 IN_PROGRESS. Stage 1 COMPLETE / APPROVED (15/15). Stage 2A COMPLETE; autorización explícita del usuario del 2026-09-27 completó Stage 2B documental: auditoría, simulaciones sintéticas, seis objetivos y canales públicos, borrador y paquete. `CONTACT_GATE_READINESS = READY_FOR_CONTACT_GATE`; contacto externo NOT_AUTHORIZED hasta decisión humana. Sin entrevistas. |

Antecedentes preservados: M06-B02 cerró C01/C07 y dos decisiones coverage PARTIAL como CLOSED_WITH_DEFERRALS. El pack operacional posterior mantuvo Phase 3 IN_PROGRESS porque los pilotos ET/SX no demostraron constraints de perfil; ese resultado permanece histórico. La misión Compliance V1 del 2026-09-28 cambia el alcance operacional a GTFS/NeTEx y deja SIRI/GTFS-RT en standby, sin reabrir B02 ni reinterpretar requirements. Demostró referencias fixed-stop GTFS y un fragmento Line contra EPIP XSD basado en NeTEx 1.3.1, con 28 fixtures, observaciones y dos reglas técnicas. Los 48 requisitos y nueve familias quedan dispuestos; no se afirma cobertura completa ni auditoría de operadores. El cierre vigente es CLOSED_WITH_DEFERRALS; véase el [informe maestro](03_Compliance/reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md).

Los PASS previos de market evidence y validation readiness son documentales. El approval de Stage 1 tampoco valida el mercado: MARKET_VALIDATED = NO, DEMAND_VALIDATED = NO, WILLINGNESS_TO_PAY = NO, DIFFERENTIATION = UNPROVEN.

## Integridad y pendientes

La base GTFS raw coincide con su hash registrado. La base Compliance se amplió con el esquema y las decisiones reproducibles de M04B. Se conservan el hash del snapshot de Phase 2, la captura local previa a M04B y el hash actual:

- GTFS raw: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Compliance Phase 2 snapshot: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`.
- Compliance local antes de M04B: `6e944fcb3e7bffd220963854dee3d753bf9377fb8b84d2525228253fcbfc1577`.
- Compliance local tras M04B: `2c9c54a3fd261b30b3c468cf3f182a354c6ea02a80df1685fa82e545517c70b5`.
- Compliance tras M06-B01: `DD5256494A682618F8F10C46396F96806FDE90B79E88BBFCA9DFABEABB68F1E4`.
- Compliance tras migración de esquema requirement concepts M06-B02: `E1CA1603D2300B90726F50C65092DB1E923B76F1F35A70E9F57CBB05E35A7BDE`.
- Compliance tras persistencia M06-B02A (sin escrituras en este gate): `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`.
- Compliance previo al pack M06-B02 orquestado (schema B02C): `0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F`.
- Compliance tras persistencia C01+C07 y post-validation del pack (2026-09-28): `657A48BF6472F958980646193F8CBAA81C01F316D2385D0F4E81F7EF13BAA791`.
- Compliance tras M06-B02 FINAL CLOSURE, +2 coverage PARTIAL y post-validation (2026-09-28): `6C7A944FB9EB7983A912AF42C2F5C69C0F29D268F6139D3B5566BF7140788E0F`.
- Compliance V1 CLOSED_WITH_DEFERRALS, +44 filas aditivas verificadas (2026-09-28): `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`.

La concordancia de bytes no certifica semántica GTFS, fidelidad textual o cumplimiento jurídico. Se mantienen las anomalías Annex 1.3 B-I/D-I, siete dependencias PARTIAL y mappings/reglas pendientes. El SQL del gate posterior a materialización incluye rutas absolutas y `read_blob`; no es un gate portable para un nuevo checkout. Los tests históricos de Phase 1, pre-materialización y el test 23 del master inicial de Phase 2 no deben aplicarse como expectativas del estado materializado. La revisión obtiene 27 PASS / 1 FAIL en ese master antiguo y 377/377 PASS en las comprobaciones de filas del gate final, excluyendo diez hashes jurídicos. Ver [la política de tests](03_Compliance/TEST_BASELINE_POLICY.md).

La [revisión global de preparación técnica](reports/repository_integrity/TDL_GLOBAL_TECHNICAL_READINESS_REVIEW.md) clasifica dependencias operativas y precondiciones para GTFS Audit Engine V1. Su veredicto es técnico y no altera los cierres humanos, contractuales o jurídicos anteriores.

Los tres KML históricos se conservan como referencia; GTFS_Lab V1 añade exportación KML/GeoJSON reproducible por run. `main.stops` sigue siendo un duplicado documentado cuyo propósito está pendiente de aclaración. Git conserva fuentes y evidencia seleccionada; bases, feeds, repositorios anidados y grandes generados requieren backup separado. La publicación del Git raíz no acredita ese backup integral.

La documentación piloto histórica contiene referencias a 0.2.1 y al alcance previo del producto. No se sustituyen las versiones de runs ya generados por 0.2.2. La guía vigente del laboratorio diferencia esos resultados del proyecto global.

El [mapa de capacidades de campos G03](02_Data_Engineering/GTFS_Lab/spec/gtfs_schedule_field_capability_map_2026_04_27.json) deriva 132 evaluaciones primarias: 106 `EXECUTABLE_G03`, 11 `PARTIALLY_EXECUTABLE_G03` y 15 `UNRESOLVED_CONDITION`. Sus categorías secundarias se cuentan por campo y pueden solaparse: 98 `EMPTY_SEMANTICS_NOT_SPECIFIED`, 24 `DEFERRED_G04`, 11 `DEFERRED_G05`, 4 `DEFERRED_G07`; el contrato no asigna restricciones a G06 ni G08. La capacidad ejecutable se limita a validadores implementados; los tipos sin validador léxico quedan clasificados como parciales. La política de extensiones permanece sin resolver.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
