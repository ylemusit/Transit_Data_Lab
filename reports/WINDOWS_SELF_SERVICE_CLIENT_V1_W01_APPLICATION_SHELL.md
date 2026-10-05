# Windows Self-Service Client V1 — W01 Application Shell

**Estado final:** `W01_APPLICATION_SHELL = CLOSED_WITH_NONBLOCKING_LIMITATIONS`; `W01 acceptance = PASS`; `W02 = NEXT / NOT_STARTED`. El shell parte de `main` en `6271a75399732dfafcaef06ec5fd63ff5835a86b`. La aceptación humana W01-F del 2026-10-05 supersede los estados provisionales anteriores de este informe y del informe W01-P.
**Alcance:** interfaz local mínima para iniciar una auditoría GTFS Schedule inicial a través del workflow cliente V1 existente.

## Decisiones del primer corte

- Interfaz con `tkinter`, disponible en la biblioteca estándar de Python; no añade dependencias.
- La GUI coordina el proceso y no importa el motor de auditoría. En modo fuente arranca `python -m gtfs_lab.client_workflow` como subproceso.
- La ejecución es serial dentro de la interfaz y un mutex impide abrir una segunda instancia del cliente en la sesión Windows.
- El usuario elige el ZIP de entrada y una carpeta padre. Cada ejecución usa un workspace nuevo con identificador generado localmente; el workflow mantiene sus zonas SOURCE/WORKING/DERIVED/AUDIT/DELIVERY.
- El ZIP de entrada no se reescribe. El workflow copia la fuente y comprueba su hash antes de continuar.
- Cancelar termina el árbol de procesos en Windows con `taskkill /T`; no se eliminan automáticamente los archivos parciales.
- QGIS continúa externo. No hay integración, configuración de proyectos ni invocación desde la aplicación.
- Interpretation, HOLDOUT, Test Bank y el motor funcional quedan fuera del cambio.

## Experiencia inicial

1. Seleccionar un archivo `.zip` GTFS.
2. Elegir una carpeta de destino existente.
3. Iniciar una auditoría `INITIAL` con procedencia `CLIENT_PROVIDED`.
4. Ver el estado, el resultado resumido y el número de hallazgos/artefactos; abrir la carpeta `delivery` si la ejecución terminó correctamente.
5. Cancelar con confirmación cuando sea necesario. Los datos parciales permanecen para revisión.

Los registros `stdout` y `stderr` del worker se conservan como ficheros ocultos junto a la carpeta de ejecución. Pueden contener mensajes técnicos y rutas locales; no deben publicarse sin revisión.

## Límites y siguientes incrementos

- El onedir reproducible de la GUI y el worker pasa en el equipo de desarrollo; DuckDB CLI está incluido. `CLEAN_MACHINE_VALIDATION = PENDING` y la validación de máquina limpia pertenece a packaging/release posterior.
- La interacción real con diálogos y la aceptación GUI compilada se registran en W01-F. No se afirma inspección visual de píxeles ni validación en máquina limpia.
- No se ofrece todavía progreso por etapas, reauditoría, selección de baseline, políticas de concurrencia configurables ni instalación/actualización.
- No se establecen requisitos mínimos/recomendados de hardware, no se certifica soporte extremo para feeds grandes, no se declara listo un instalador de producción y no se establece preparación comercial o validación de mercado.

## Criterio para cerrar W01

Demostrar por separado el modo fuente y el paquete `onedir` en Windows: inicio/cierre de GUI, selección y validación de entradas, auditoría sintética completa, conservación del ZIP fuente, entrega/hash, cancelación sin procesos descendientes activos, apertura de entrega, inclusión del DuckDB CLI y ejecución en una máquina limpia sin Python/DuckDB global. Mantener la serialización del trabajo y los límites de W00; no reabrir Interpretation/HOLDOUT.

## Auditoría GUI E2E en modo fuente — 2026-10-05

**Resultado:** `GUI_E2E = PASS_WITH_FUNCTIONAL_BLOCKER`; `W01 = IN_PROGRESS`. Se ejercitaron los botones y callbacks de la ventana Tk real y su bucle de eventos. El harness seleccionó los paths con los callbacks de diálogo, lanzó el workflow real como subproceso y usó exclusivamente entradas sintéticas. Para el caso válido, el harness declaró `SYNTHETIC` en el argumento de procedencia.

- **Éxito:** el caso sintético terminó como `COMPLETED`; la GUI mostró el resumen y siguió procesando eventos durante la auditoría (25 pulsos del callback de 20 ms). La entrega contenía 30 artefactos; todos coincidieron con sus hashes del manifest y el sello validó el hash del manifest. El ZIP fuente conservó SHA-256 `db0303034934ed94e558ea79de8670cd0066f99b11ecf284ad9cb849cb066aad`.
- **Apertura:** el botón «Abrir entrega» ejecutó `os.startfile` sin error sobre el directorio `delivery` correcto.
- **Error:** un ZIP inválido produjo `BLOCKED_INPUT_INVALID`; la GUI actualizó su estado y llamó al callback de aviso; los archivos de ejecución se conservaron.
- **Cancelación y recuperación:** se canceló un worker sintético controlado con un proceso descendiente. `taskkill /T` terminó el descendiente (PID 41664); la GUI siguió respondiendo y permitió lanzar después otra auditoría sintética real, completada con 30 artefactos.
- **Bloqueo funcional:** tras la cancelación, la GUI sustituye el mensaje de cancelación por «La auditoría no se completó (error técnico)» y muestra el aviso genérico de error. La parada del árbol funciona, pero el resultado no distingue cancelación solicitada de fallo técnico. Hace falta corregir esa clasificación y repetir este caso antes de considerar listo el paso a empaquetado.

La evidencia JSON del harness y los artefactos de ejecución permanecen en un directorio temporal local fuera de Git. Se invocaron los botones Tk directamente; las respuestas de los diálogos de archivo/carpeta y la confirmación/modal de aviso se capturaron en el harness para automatizar la prueba. Este resultado cubre el shell en modo fuente, su bucle Tk y el worker real. No es inspección visual de píxeles, no prueba el entrypoint/mutex, no valida binarios empaquetados y no cierra W01 ni la validación en máquina limpia.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## W01-F — aceptación humana final — 2026-10-05

**Decisión humana:** `W01-F = W01F_PASS_READY_FOR_W01_CLOSURE`. La aceptación manual de la GUI compilada y los resultados automatizados se registran en [W01-F](WINDOWS_SELF_SERVICE_CLIENT_V1_W01_F_FINAL_PACKAGED_GUI_ACCEPTANCE.md). Esta decisión actualiza el estado de fase; los registros anteriores de limitaciones reflejan sus fechas y evidencia de entonces.

```ini
MANUAL_ACCEPTANCE = PASS
COMPILED_GUI_START = PASS
REAL_DIALOG_INTERACTION = PASS
COMPILED_GUI_SUCCESS_E2E = PASS
OPEN_DELIVERY = PASS
COMPILED_GUI_CANCEL_E2E = PASS
CANCELLED_BEFORE_NORMAL_SUCCESS = YES
FILES_STOPPED_AFTER_CANCEL = YES
POST_CANCEL_RERUN = PASS
SINGLE_INSTANCE_REAL_EXE = PASS
SECOND_INSTANCE_REJECTED = PASS
FIRST_INSTANCE_STILL_USABLE = PASS
NORMAL_EXIT = PASS
RESTART_AFTER_EXIT = PASS
ORPHAN_PROCESSES_FINAL = 0
AUTOMATED_TESTS = 7/7 PASS
MUTEX_TEST_AFTER_GUI_CLOSED = PASS
PY_COMPILE = PASS
GIT_DIFF_CHECK = PASS
PACKAGED_ONEDIR = PASS
DUCKDB_BUNDLED = YES
CLEAN_MACHINE_VALIDATION = PENDING
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
W02 = NEXT / NOT_STARTED
```

Limitaciones no bloqueantes conservadas: el soporte para feeds de tamaño extremo sigue sin certificarse; hardware mínimo/recomendado no establecido; instalador de producción no declarado listo; QGIS permanece como workbench externo de evidencia; presentación PDF/informes pertenece a W06; ingeniería de releases queda para una fase posterior. No se inicia W02.


## W01-C — Cancellation Semantics Fix — 2026-10-05

**Resultado:** `W01C_PASS_WITH_NONBLOCKING_LIMITATIONS`; `W01C_READY_FOR_HUMAN_REVIEW`. Se conserva intención explícita de cancelación y estado `CANCELLING`; la terminación del árbol se ejecuta en un hilo auxiliar para que la ventana siga respondiendo. La clasificación prioriza cancelación solicitada frente al código de salida. Las solicitudes repetidas durante la cancelación y después de terminar el proceso no inician otra terminación. La entrega permanece deshabilitada tras cancelar.

- Cancelación: `Auditoría cancelada por el usuario.`; no hubo aviso genérico. El worker devolvió código 1, el descendiente terminó, y se observaron 0 procesos huérfanos. El heartbeat Tk avanzó 67 veces durante la cancelación.
- Diagnóstico local: timestamp de solicitud, intento y resultado de terminación del árbol, código de salida y clasificación final `CANCELLED` registrados en `.technical.jsonl`. Una segunda solicitud produjo exactamente un intento.
- Regresión de fallo: ZIP inválido clasificado como fallo, con `BLOCKED_INPUT_INVALID` y aviso de error.
- Regresión de éxito: auditoría sintética `COMPLETED`, entrega abierta, 30 artefactos verificados y sello PASS; el heartbeat Tk avanzó 39 veces.
- Recuperación: otra auditoría sintética en la misma GUI terminó correctamente con 30 artefactos. SHA-256 del ZIP fuente conservado.
- Interacción: `REAL_DIALOG_INTERACTION = NOT_YET_TESTED`; harness simuló los diálogos de archivo/carpeta y confirmó directamente botones y callbacks Tk. No es una prueba E2E de interacción humana completa.

Evidencia local no versionada: `result.json` en el directorio temporal de W01-C. Las pruebas de clasificación cubren cancelación con worker terminado, fallo no solicitado, éxito y carrera con salida cero. No se ha iniciado empaquetado ni merge. HOLDOUT no se accedió y el motor no cambió.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
