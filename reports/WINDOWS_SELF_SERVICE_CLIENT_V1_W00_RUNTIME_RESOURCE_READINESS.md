# Windows Self-Service Client V1 — W00 Runtime / Resource Readiness

**Estado vigente:** `W00O_READY_FOR_HUMAN_REVIEW`
**Clasificación técnica vigente:** `W00O_BLOCKED_RESOURCE_ROOT_CAUSE_UNKNOWN`
**Base:** `f53335747562206936e5db7704dfb093844d768e` (main tras PR #48)
**Fecha:** 2026-10-05

W00-R permanece documentado abajo como resultado histórico. La actualización W00-O y sus límites se registran al final de este informe.

## W00-R — cierre de remediación de runtime

**Estado:** `W00R_READY_FOR_HUMAN_REVIEW`
**Clasificación:** `W00R_BLOCKED_REQUIRES_OPTIMIZATION`
**Base verificada:** `f53335747562206936e5db7704dfb093844d768e` (`HEAD` y `origin/main` coinciden al iniciar el trabajo).

### Resultado

- `PROCESS_TREE_TELEMETRY = PASS` en control sintético Windows: raíz y descendiente observados; 24 muestras a 50 ms; working set y memoria privada agregados por árbol. Son máximos muestreados, no high-water marks del sistema. El fin del proceso raíz y su código de salida se capturan; el fin exacto de descendientes que salen entre muestras queda `NOT_CAPTURED`.
- `STAGE_ATTRIBUTION = PASS` para los ocho marcadores y su correlación sintética timestamp → etapa → recursos. Los marcadores optativos no alteran el resultado y se activan con `TDL_RESOURCE_STAGE_FILE`. No se atribuye memoria real del motor: no se ejecutó un feed.
- `RESOURCE_SAFETY = PASS`; regla experimental solo para desarrollo: RAM disponible ≥ 1,25 × 18,89 GiB = 23,6125 GiB; disco libre ≥ 10 GiB; workspace dentro del worktree W00-R; CPU del sistema muestreada ≤ 25 %. No son mínimos de producción. En el preflight grande se observaron 18.44 GiB disponibles, 679.83 GiB libres y 6.5 % CPU: falla RAM y `DATASET_019_NEW_BENCHMARK = SKIPPED` con `BENCHMARK_BLOCKED_BY_RESOURCE_SAFETY`. No se abrió el Test Bank ni se accedió a fuentes.
- El control sintético pasó preflight reducido (≥1 GiB RAM/disco, workspace aislado y CPU ≤25 %), terminó con código 0 y confirmó descendiente, captura stdout/stderr, cambios de TEMP/salida, disco y etapas.
- `MEMORY_STAGE_ATTRIBUTION = NOT_DETERMINED`. Los candidatos estáticos siguen siendo extracción/decodificación ZIP, materialización Python en validación/análisis, acumulación de findings, estructuras de interpretación y serialización/reporting. No se atribuye el pico a DuckDB ni a Python sin perfil real.
- `SUBPROCESS_MODEL = PASS` en prueba CLI: inicio, progreso, captura stdout/stderr, código de salida, cancelación y proceso ausente del snapshot del SO tras salir. El muestreo del árbol se ejerce con el harness externo de recursos; no se midieron bytes de RAM devueltos; no hay GUI.
- `PACKAGING_FEASIBILITY = LIMITED`: PyInstaller 6.22.3 generó un onedir local y el ejecutable respondió a `--help`. DuckDB CLI no está incluido; máquina limpia, ejecución de auditoría empaquetada, rutas de recursos y firma quedan sin probar. No es instalador ni release.
- `MINIMUM_HARDWARE = NOT_YET_ESTABLISHED`; `RECOMMENDED_HARDWARE = NOT_YET_ESTABLISHED`.

### Decisión de remediación y límites

Se conserva `OPTIMIZATION_REQUIRED_BEFORE_W01` como bloqueo heredado del resultado W00: dataset 019 registró históricamente unos 18.89 GiB de memoria privada muestreada y W00 dejó pendiente optimizar el feed grande. W00-R no localiza la causa ni implementa optimizaciones porque la carga real no superó la barrera de seguridad. La próxima evidencia requiere ejecutar 019 en máquina aislada que sí cumpla el preflight, correlacionar etapas y procesos, y después revisar opciones que preserven semántica y replay. Cualquier cambio de materialización/streaming necesita revisión humana previa.

`FUNCTIONAL_ENGINE_CHANGED = YES` (instrumentación observacional optativa en workflow, pipeline e ingesta); `ENGINE_SEMANTICS_CHANGED = NO`; `HOLDOUT_ACCESSED = NO`; `W01_STARTED = NO`; GUI no iniciada; QGIS sigue siendo un workbench externo y GeoPackage permanece como formato candidato primario.

Evidencia W00-R: [árbol de procesos](evidence/windows_client_v1/w00/process_tree_measurements.json), [perfil por etapas](evidence/windows_client_v1/w00/stage_resource_profile.json), [preflight grande](evidence/windows_client_v1/w00/resource_safety_preflight.json), [resumen](evidence/windows_client_v1/w00/benchmark_summary.json), [decisión](evidence/windows_client_v1/w00/runtime_remediation_decision.json), [subproceso](evidence/windows_client_v1/w00/subprocess_feasibility.json) y [PyInstaller](evidence/windows_client_v1/w00/packaging_assessment.md).

Verificación: 5 tests del harness PASS; `py_compile` de módulos modificados PASS; los siete JSON de evidencia parsean; build PyInstaller onedir y CLI empaquetada `--help` PASS; `git diff --check` PASS. No se ejecutó la suite funcional completa ni un benchmark GTFS real.

## Decisión

La arquitectura cliente local es viable para pasar a una fase de diseño/validación de runtime si se mantiene una UI ligera y el motor aislado en un subproceso. No está listo para W01 de implementación: faltan benchmark nuevo con medición continua, memoria de descendientes, atribución por etapas, tamaños reales de trabajo/temporales y prueba de paquete en máquina limpia. El dataset DEVELOPMENT 019 completó históricamente el flujo, pero sus 18.89 GiB de memoria privada muestreada exceden los 16.9 GiB disponibles observados en esta workstation; no repetí esa carga.

No se ejecutó HOLDOUT, no se abrió el banco local ni se volvió a ejecutar el corpus de 14 datasets. Los casos del resumen son resultados históricos de la campaña DEVELOPMENT autorizada (base funcional `9cafe070…`), no mediciones nuevas sobre `f533357…`. En esta base W00 cambia de `NOT_STARTED` a `IN_PROGRESS` para revisión; no inicia GUI, W01, QGIS plugin ni optimización del motor.

## Runtime y recursos

| Elemento | Observación actual | Alcance |
|---|---|---|
| Sistema | Windows 11 Home x64, build 26300 | Workstation actual; no define versión mínima de cliente |
| CPU | AMD Ryzen 9 9900X, 12 núcleos / 24 lógicos | Observado; no representa mínimo |
| RAM | 31.15 GiB físicos; 16.88 GiB disponibles al capturar | Disponible varía con carga; dataset 019 consumió 18.89 GiB en observación histórica |
| Disco C: | NTFS, 1,629,431,525,376 B; 729,930,420,224 B libres (≈679.83 GiB) | Libre en el momento de consulta; no es requisito ni mide temporales de la auditoría |
| Python | CPython 3.12.10 x64, intérprete global | No se encontró manifiesto de dependencias ni entorno virtual de GTFS_Lab en el checkout |
| DuckDB | CLI 1.5.5 resuelto por `PATH` | Dependencia externa obligatoria; no se encontró paquete `duckdb` Python en este intérprete y el motor usa CLI |
| Dependencias Python del recorrido | Librería estándar, módulos internos `gtfs_lab` y `lxml` para el evaluador Compliance integrado (`lxml 6.1.3` en el host) | Requiere fijar/validar la wheel Windows y sus componentes nativos; no se ha construido un entorno limpio |
| QGIS | Ejecutable no encontrado en `PATH` | No equivale a demostrar que no esté instalado; sin prueba GIS local |

Inventario reproducible y límites en [runtime_inventory.json](evidence/windows_client_v1/w00/runtime_inventory.json). La fuente de entrada es ZIP; la ejecución extrae tablas a un workspace por run, crea `dataset.duckdb`, informes y evidencia. Test Bank usa una raíz local configurable, SOURCE de solo lectura, raíz de hasta 64 caracteres y replay separado; estas condiciones del contrato no se confunden con una prueba de empaquetado.

## Casos y mediciones

La campaña DEVELOPMENT previa completó 14/14 casos `OK`, replay 14/14 `PASS`, sin fallos de pipeline ni accounting gaps. Como candidatos por duración observada (proxy, no tamaño de ZIP), el resumen selecciona 007/00016 (1.17 s), 016/00022 (5.15 s), 014/00021 (30.17 s) y 019/00023 (763.05 s). Para 019 se conocen ZIP de 18,245,454 B y `stop_times.txt` descomprimido de 52,049,844 B; la memoria privada se estimó manualmente en 18.89 GiB, sin muestreo continuo ni pico real certificado. Los ZIP de los otros tres candidatos no se miden aquí.

El harness W00 se probó solo con un subproceso sintético, sin motor ni GTFS: wall 1.609 s; CPU muestreada 0.031 s; working set máximo muestreado 12,779,520 B; memoria privada máxima muestreada 7,692,288 B; 8 muestras a 0.2 s; árbol de salida delta 0 B; árbol TEMP delta 0 B; espacio libre C: delta calculado −12,288 B (cambio del volumen completo, no atribuible al proceso); retorno 0. Resultado en [resource_measurements.json](evidence/windows_client_v1/w00/resource_measurements.json). Son valores OBSERVED del proceso raíz, no representativos del motor. El harness marca por separado `OBSERVED`, `OBSERVED_SAMPLED`, `CALCULATED` y `NOT_CAPTURED`.

**Hallazgo de memoria:** en `ingestion._validate_member`, se lee cada miembro ZIP completo en bytes y se decodifica para validar CSV antes de escribirlo a disco. Después, `validation._validate` conserva sets de identificadores y `analysis.analyze` mantiene mapas `trip_routes`, route-stop sets y listas por stop mientras recorre `stop_times`. Esto identifica candidatos de materialización Python proporcionales a datos. Es una inferencia por lectura de código, no atribución medida; DuckDB CLI es un proceso descendiente que el harness actual tampoco contabiliza. El tamaño de los informes históricos fue modesto (máximos: `AUDIT_CONSOLIDATED.json` 122,584 B; `engine_report.json` 75,316 B; `findings.json` 99,805 B), lo cual no demuestra que la serialización no contribuya en otras entradas.

Temporales y disco de auditoría: **NOT_CAPTURED** para una ejecución real. Harness mide árboles de salida/TEMP antes y después, pero no crecimiento temporal continuo, espacio libre del volumen antes/después ni procesos descendientes. Los valores libres de C: anteriores son solo estado puntual de la workstation.

Detalle en [benchmark_summary.json](evidence/windows_client_v1/w00/benchmark_summary.json). No se cambió el comportamiento entre casos.

## Empaquetado, aislamiento y GIS

- **Paquete:** primer candidato técnico PyInstaller `onedir`; empaquetar explícitamente el DuckDB CLI, no depender del `PATH` de sistema. Nuitka standalone y Python embebible quedan como comparativas. No se midieron tamaños, compatibilidad AV/SmartScreen, inicio ni actualizaciones; no se construyó instalador. Evaluación completa: [packaging_assessment.md](evidence/windows_client_v1/w00/packaging_assessment.md).
- **Ejecución:** GUI futura ligera que lanza un subproceso por análisis. Aísla fallos y permite liberar RAM al terminar. Retener Test Bank serial, evitar concurrencia, capturar logs a ficheros y diseñar progreso/cancelación con recuperación explícita. No hace falta un servicio local. Ver [execution_isolation_assessment.md](evidence/windows_client_v1/w00/execution_isolation_assessment.md).
- **GIS:** QGIS continúa externo. Conservar GeoJSON y KML existentes; GeoPackage es el formato primario recomendado para el puente futuro tras una prueba real. No crear `.qgz` en TDL. Ver [qgis_bridge_assessment.md](evidence/windows_client_v1/w00/qgis_bridge_assessment.md).

## Requisitos de hardware y remediaciones

`MINIMUM_SUPPORTED_HARDWARE = NOT_YET_ESTABLISHED`
`RECOMMENDED_HARDWARE = NOT_YET_ESTABLISHED`

La cifra histórica de 18.89 GiB de dataset 019 no permite convertirla en un mínimo: fue observación manual no continua y faltan procesos hijos, otras cargas concurrentes, crecimiento de workspace, temporales, margen de sistema y varias clases de hardware. No se inventan requisitos Windows, CPU, RAM ni disco.

Antes de W01, completar en orden:

1. Mejorar harness para muestrear el árbol completo de procesos, bytes libres por volumen y crecimiento de workspace/TEMP con intervalos declarados; conservar no capturado como tal.
2. Añadir marcadores de etapa de bajo impacto y ejecutar corpus representativo serial de DEVELOPMENT/Test Bank aprobado en una máquina con RAM suficiente y espacio aislado. Separar ZIP/extracción, CSV, DuckDB, validación, análisis, informes, interpretación, replay y entrega.
3. Revisar de forma independiente la atribución de memoria. Si una optimización requiere cambiar semántica o contratos, activar el hard stop y pedir decisión humana antes de tocar motor.
4. Construir y validar `onedir` en Windows limpio sin Python/DuckDB global, medir directorio, instalación/copia, arranque, TEMP, actualización y antivirus.
5. A partir de mediciones repetidas definir hardware mínimo/recomendado, margen libre de disco, límites de concurrencia y política de cancelación/recuperación.
6. Acordar el cierre GeoPackage con una prueba de apertura y atributos en QGIS; mantenerlo como formato futuro mientras tanto.

## Cambios y verificación

`FUNCTIONAL_CODE_CHANGED = NO` (motor/cliente)
`W00_MEASUREMENT_TOOLING_ADDED = YES`
`ENGINE_SEMANTICS_CHANGED = NO`
Se añadió únicamente el harness `tools/resource_measurement.py`, su prueba unitaria y evidencia/documentación W00. La prueba del harness: `python -m unittest discover -s tests -p test_resource_measurement.py -v` — 3 PASS. `git diff --check = PASS`. Los 3 JSON parsean correctamente y los enlaces locales del informe existen. No se ejecutó la suite del motor ni un benchmark GTFS W00.

## Referencias técnicas consultadas

- PyInstaller, modos de carpeta/archivo único y extracción temporal: [documentación oficial](https://pyinstaller.org/en/stable/operating-mode.html).
- Nuitka standalone y soporte Windows: [manual oficial](https://nuitka.net/user-documentation/user-manual.html).
- Python embebible en Windows: [documentación oficial](https://docs.python.org/3/using/windows.html#the-embeddable-package).
- SmartScreen y reputación de binario/editor: [Microsoft Learn](https://learn.microsoft.com/windows/apps/package-and-deploy/smartscreen-reputation).

## W00-O — cierre de recursos sintéticos y PyInstaller

**Estado:** `W00O_READY_FOR_HUMAN_REVIEW`
**Clasificación final:** `W00O_BLOCKED_RESOURCE_ROOT_CAUSE_UNKNOWN`
**Base verificada:** `f53335747562206936e5db7704dfb093844d768e`
**Fecha:** 2026-10-05

### Benchmark serial y parada segura

- El generador `tools/synthetic_resource_benchmark.py` produjo fixtures GTFS deterministas con IDs únicos y referencias relacionales íntegras. Los SHA-256 se repitieron iguales por escala en tres ejecuciones completas de la escalera.
- S1, S2, S4, S8, S16, S32 y S64 completaron la auditoría real `gtfs_lab.pipeline.run` con código 0. S64 contiene 64.000 filas de `stop_times.txt`; las tablas sin comprimir ocupan 3.566.748 B y el ZIP 656.734 B. El manifiesto por fixture y las mediciones están en [synthetic_scale_benchmark.json](evidence/windows_client_v1/w00/synthetic_scale_benchmark.json) y [resource_scaling_analysis.json](evidence/windows_client_v1/w00/resource_scaling_analysis.json).
- `RESOURCE_GROWTH = INCONCLUSIVE`. El máximo muestreado fue 4.662.296.576 B de memoria privada del árbol de procesos y 4.071.231.488 B de working set en S64, asociado temporalmente a `REPORT_GENERATION`. Es una correlación por etapa; no identifica qué objeto, serialización o proceso causó el consumo. La muestra tampoco permite afirmar complejidad matemática.
- Antes de S128, la proyección lineal desde S64 fue 9.324.593.152 B; el límite conservador de esta escalera sintética era el 50 % de RAM disponible, 9.210.972.160 B. `SAFE_STOP_TRIGGERED = YES`; S128 no se generó ni ejecutó. Este límite sintético deja al menos la mitad de la RAM disponible sin comprometer y no sustituye el gate más estricto para dataset 019.
- `INTAKE`, `INTERPRETATION`, `REPLAY` y `CLEANUP` no se ejecutaron en esta llamada directa al motor. `ZIP_EXTRACTION` tuvo marcadores temporales, pero no muestras de memoria a intervalos de 100 ms. Los resultados ausentes permanecen `NOT_CAPTURED`.

### Causa raíz y gate de optimización

`MEMORY_ROOT_CAUSE = NOT_REPRODUCED_WITH_SYNTHETIC_WORKLOAD`. El preflight W00-R de dataset 019 sigue bajo el umbral de 23,613 GiB de RAM disponible, así que 019 se mantuvo `DEFERRED_FOR_HIGH_MEMORY_ENVIRONMENT`. No se accedió al Test Bank ni a HOLDOUT. No se atribuye el pico a DuckDB, a listas Python, a findings ni a generación de informes por su mera presencia.

No se implementó optimización de runtime: no se reprodujo una carga que justificase una intervención. La comparación de una auditoría sintética S1 entre la base y la instrumentación PASS para findings raw, accounting, interpretación, resumen semántico del informe, identidad de fuente y versiones. El replay no forma parte de esa comparación; no hubo cambio de semántica del motor. Detalle y gate en [memory_root_cause.json](evidence/windows_client_v1/w00/memory_root_cause.json), [optimization_before_after.json](evidence/windows_client_v1/w00/optimization_before_after.json) y [comparación de instrumentación](evidence/windows_client_v1/w00/instrumentation_semantic_comparison.json).

### PyInstaller onedir y subprocesos

- PyInstaller 6.22.3 produjo un paquete onedir local de 67.696.306 B. Contiene el runtime Python, lxml y el DuckDB CLI 1.5.5 que consume actualmente el motor. El hook/spec incluye explícitamente DuckDB y los recursos hash-pinned de Compliance; las rutas y hashes de recursos pasaron la comprobación.
- Ejecutado desde `dist` con el `PATH` del proceso limitado al directorio System32 de Windows: el self-check del worker terminó con código 0 y la auditoría sintética produjo 21 artefactos, incluido `dataset.duckdb`, con estado de base PASS. El árbol del worker y DuckDB desapareció al terminar, sin procesos huérfanos. Evidencia: [packaging_pyinstaller_onedir.json](evidence/windows_client_v1/w00/packaging_pyinstaller_onedir.json).
- `CLEAN_MACHINE_VALIDATION = PENDING`. La prueba anterior sigue siendo de esta estación de desarrollo, no de una VM limpia ni un release firmado. En una VM Windows nueva habrá que verificar: ausencia de Python/dependencias de desarrollo; runtime y DuckDB incluidos; inicio del worker; auditoría sintética; artefactos/hashes; terminación limpia del árbol de procesos.
- Finalización normal y cancelación controlada de un árbol trabajador/descendiente: PASS; el proceso padre se mantuvo vivo y `ORPHAN_PROCESSES = 0`. La liberación de espacio de direcciones se infiere de la desaparición del árbol; no se aislaron bytes de RAM física devueltos al sistema. Evidencia: [subprocess_reclamation.json](evidence/windows_client_v1/w00/subprocess_reclamation.json).

### Decisión y límites conservados

`MINIMUM_SUPPORTED_HARDWARE = NOT_YET_ESTABLISHED`; `RECOMMENDED_HARDWARE = NOT_YET_ESTABLISHED`. No se implementa integración QGIS: se conserva `TDL → GIS evidence package → QGIS`, con GeoPackage como candidato primario. `FUNCTIONAL_ENGINE_CHANGED = YES` por marcadores optativos de medición en workflow/ingesta/pipeline/Test Bank; `ENGINE_SEMANTICS_CHANGED = NO` según la comparación sintética; `HOLDOUT_ACCESSED = NO`; `W01 = NOT_STARTED / BLOCKED`.

La regresión ejecutada registró 290 tests: 289 PASS, 0 FAIL y 1 SKIP documentado (requiere la base Compliance V1 respaldada localmente, ausente intencionadamente en este checkout). `git diff --check` y estado de Git quedan verificados al terminar esta tarea.

La decisión machine-readable está en [w00o_closure_decision.json](evidence/windows_client_v1/w00/w00o_closure_decision.json). El resultado queda listo para revisión humana; no se inicia W01 ni se integra automáticamente.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
