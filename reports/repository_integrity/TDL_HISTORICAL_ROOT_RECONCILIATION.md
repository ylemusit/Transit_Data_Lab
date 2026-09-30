# Reconciliación del worktree raíz histórico

Fecha de revisión: 2026-09-30. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Identidades, alcance y veredicto

- Raíz histórica: `7b6f7fc21fb44f96d2f6d459c9d54115b1a52602`, rama local `main` con 8 archivos modificados, 20 no seguidos y ninguno en staging.
- `main` autoritativo fijado para esta revisión: `11e8fe6b20232f02622a6c27d29b7c960763e979`. `git ls-remote origin refs/heads/main` devolvió ese SHA antes de la comparación. Se obtuvo el objeto sin desplazar la rama local y se creó un worktree separado desde él.
- Archivos revisados: **28**. Archivos integrados en el worktree limpio: **4**, todos históricos (2 informes y 2 imágenes). Código, tests y evidencia de ejecución integrados: **0**.
- Archivos ya representados: **20** (`ALREADY_IN_MAIN` 14 + `DUPLICATE_EVIDENCE` 6). Archivos superados: **4**. Evidencia histórica retenida: **4**. Artefactos locales/runtime: **0**. Decisiones humanas para la disposición técnica: **0**. Total de disposiciones: **28**.
- Veredicto: **`ROOT_RECONCILIATION_INTEGRATION_REQUIRED`**. La integración documental queda preparada en el worktree limpio; la raíz histórica permanece intacta. Limpiar o archivar esa raíz exige una operación posterior explícita.

Las fechas/orígenes de la matriz proceden del contenido y de las marcas de modificación locales: estas últimas son orientativas y no prueban autoría ni ejecución. Los informes y PNG del 28/09 se conservan como testimonios de comunicación y planificación de esa fecha. No gobiernan el estado actual ni acreditan validación técnica, jurídica o comercial. `PROJECT_STATUS.md` en `main` es la entrada operativa.

## Matriz de los 28 archivos

`M` = modificado frente al HEAD histórico; `U` = no seguido. En la columna «Equivalente» se indica el archivo actual o una copia idéntica de la evidencia; «mismo» significa bytes idénticos. Cada fila tiene exactamente una disposición primaria. Las rutas son relativas al repositorio.

| # | Ruta | Estado; tipo; fecha/origen aproximado; hito | Contenido y equivalente en `main` | Valor único; riesgo al incorporarlo | Disposición | Acción |
|---:|---|---|---|---|---|---|
| 1 | `02_Data_Engineering/GTFS_Lab/README.md` | M; CURRENT_DOCUMENTATION; 29/09, M02–M04 | Guía de gates M02/M03/A4 y triage B2. Mismo archivo actual, actualizado tras B3/M05 y CI. | Ninguno vigente; copiarlo restauraría la afirmación de HOLDOUT cerrado a futuro. | `SUPERSEDED_BY_MAIN` | No copiar. |
| 2 | `02_Data_Engineering/GTFS_Lab/gtfs_lab/compliance_adapter.py` | M; SOURCE_CODE; 29/09, M04-B2D | Adaptador del evaluador v2; mismo archivo, bytes idénticos. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 3 | `02_Data_Engineering/GTFS_Lab/gtfs_lab/ingestion.py` | M; SOURCE_CODE; 29/09, M04-B2 | Límite por registro/campo y líneas físicas; mismo archivo, bytes idénticos. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 4 | `03_Compliance/COMPLIANCE_V1_CURRENT_STATE.md` | M; CURRENT_DOCUMENTATION; 29/09, M04-B2D | Identidad v2 y gate de transición; mismo archivo, bytes idénticos. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 5 | `PROJECT_STATUS.md` | M; CURRENT_DOCUMENTATION; 29/09, M04-B2D | Estado anterior al cierre B3/M05 y PR #19; el archivo actual refleja los hitos posteriores. | Ninguno vigente; sustituirlo invertiría el estado. | `SUPERSEDED_BY_MAIN` | No copiar. |
| 6 | `README.md` | M; CURRENT_DOCUMENTATION; 28/09, planificación | Añade enlace a la matriz de servicio. El README actual prioriza precondiciones del motor y Business; el informe M01 ya cita la matriz. | Enlace útil pero no necesario como navegación vigente; copiar el archivo eliminaría el enlace actual a precondiciones. | `SUPERSEDED_BY_MAIN` | Conservar la matriz como documento histórico, sin reemplazar README. |
| 7 | `tools/compliance_v1_current_gate.py` | M; SOURCE_CODE; 29/09, M04-B2D | Replay histórico y candidato v2. El mismo gate actual añade portabilidad, preflight de recursos y conexión de DB al replay. | Ninguna función B falta en C; copiarlo retiraría controles nuevos. | `SUPERSEDED_BY_MAIN` | No copiar. |
| 8 | `tools/compliance_v1_engine.py` | M; SOURCE_CODE; 29/09, M04-B2D | Evaluador incremental v2; mismo archivo, bytes idénticos. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 9 | `02_Data_Engineering/GTFS_Lab/reports/GTFS_LAB_M04B2_DEVELOPMENT_TRIAGE.md` | U; REPORT; 29/09, M04-B2 | Triage sintético; misma ruta y bytes en `main`. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 10 | `02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2a_transition_20260929/compliance_transition_evidence.json` | U; EVIDENCE; 29/09, transición B2 | Evidencia de transición; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 11 | `02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2a_transition_20260929/historical_package_replay.json` | U; EVIDENCE; 29/09, transición B2 | Replay de paquete histórico; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 12 | `02_Data_Engineering/GTFS_Lab/tests/test_compliance_v1_transition.py` | U; TEST; 29/09, M04-B2D | Pruebas de transición; misma ruta y bytes. | Ninguna regresión falta. | `ALREADY_IN_MAIN` | No copiar. |
| 13 | `02_Data_Engineering/GTFS_Lab/tests/test_m04b2_synthetic_triage.py` | U; TEST; 29/09, M04-B2 | Casos sintéticos de triage; misma ruta y bytes. | Ninguna regresión falta. | `ALREADY_IN_MAIN` | No copiar. |
| 14 | `03_Compliance/reports/evidence/compliance_v1_20260929_m02_deep_review/cli_replay.json` | U; EVIDENCE; 29/09, revisión Compliance V1 | Dos replays CLI; copia idéntica en `compliance_v1_20260928/current_gate_04/`. | Ninguno; duplicaría outputs con rutas absolutas antiguas. | `DUPLICATE_EVIDENCE` | No integrar. |
| 15 | `03_Compliance/reports/evidence/compliance_v1_20260929_m02_deep_review/phase1_raw.json` | U; EVIDENCE; 29/09, revisión Compliance V1 | Salida Phase 1; copia idéntica en `current_gate_04/`. | Ninguno; duplicación de ejecución. | `DUPLICATE_EVIDENCE` | No integrar. |
| 16 | `03_Compliance/reports/evidence/compliance_v1_20260929_m02_deep_review/phase2_raw.json` | U; EVIDENCE; 29/09, revisión Compliance V1 | Salida Phase 2, incluido FAIL histórico permitido; copia idéntica en `current_gate_04/`. | Ninguno; duplicación de ejecución. | `DUPLICATE_EVIDENCE` | No integrar. |
| 17 | `03_Compliance/reports/evidence/compliance_v1_20260929_m02_deep_review/pilot_replay.json` | U; EVIDENCE; 29/09, revisión Compliance V1 | 28 casos sintéticos con evaluador v1; copia idéntica en `current_gate_04/`. | Ninguno; no acredita una nueva ejecución. | `DUPLICATE_EVIDENCE` | No integrar. |
| 18 | `03_Compliance/reports/evidence/compliance_v1_20260929_m02_deep_review/safety_cases.json` | U; EVIDENCE; 29/09, revisión Compliance V1 | Cuatro casos de seguridad; copia idéntica en `current_gate_04/`. | Ninguno. | `DUPLICATE_EVIDENCE` | No integrar. |
| 19 | `03_Compliance/reports/evidence/compliance_v1_20260929_m02_deep_review/summary.json` | U; EVIDENCE; 29/09, revisión Compliance V1 | PASS con hash de DB `4DB39F…`; copia idéntica en `current_gate_04/` y `current_gate_checkpoint_01/`. | Ninguno; no es un nuevo gate. | `DUPLICATE_EVIDENCE` | No integrar. |
| 20 | `03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate_final/package_candidate.json` | U; EVIDENCE; 29/09, M04-B2D | Paquete candidato SHA-256 `8633fe32…`; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 21 | `03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate_final/transition_manifest.json` | U; EVIDENCE; 29/09, M04-B2D | Manifiesto de transición; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 22 | `03_Compliance/reports/evidence/compliance_v1_current_implementation_v2.json` | U; EVIDENCE; 29/09, M04-B2D | Puntero de implementación aprobado; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 23 | `08_infografias/Infografia del proyecto a dia 27092026.png` | U; IMAGE; imagen fechada 27/09 | Vista de progreso anterior con porcentajes y flujo previsto; ausente de `main`, enlazada desde la radiografía. | Testimonio visual histórico, no medición vigente; riesgo de interpretar porcentajes obsoletos como actuales. | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` | Integrar bytes originales con contexto en este informe. |
| 24 | `08_infografias/Infografia del proyecto a dia 28092026.png` | U; IMAGE; imagen fechada 28/09 | Vista de siete áreas y alcance V1; ausente de `main`, enlazada desde la radiografía. | Testimonio visual histórico; sus estados no prueban gates posteriores. | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` | Integrar bytes originales con contexto en este informe. |
| 25 | `reports/GTFS_LAB_M04B2A_COMPLIANCE_PACKAGE_TRANSITION.md` | U; REPORT; 29/09, M04-B2D | Informe de aprobación y transición; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |
| 26 | `reports/PROJECT_RADIOGRAPHY_2026-09-28.md` | U; HISTORICAL_DOCUMENTATION; corte 28/09 | Diagnóstico GTFS primero/NeTEx después, límites por área y lectura de los dos PNG; sin informe equivalente en `main`. | Procedencia de las imágenes y decisión de secuencia; citas al estado de 28/09 ya obsoletas. | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` | Integrar original como informe histórico. |
| 27 | `reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md` | U; HISTORICAL_DOCUMENTATION; corte 28/09 | Matriz SA-001–SA-024 de capacidades/gates. Ausente de `main`, pero citada por `reports/TDL_TRUST_FOUNDATION_M01.md`. | Recupera el fundamento documental de M01; algunas celdas y próximos pasos son anteriores a M04/M05. | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` | Integrar original como matriz histórica. |
| 28 | `tools/compliance_v1_transition_candidate.py` | U; SOURCE_CODE; 29/09, M04-B2D | Generador de candidato v2; misma ruta y bytes. | Ninguno. | `ALREADY_IN_MAIN` | No copiar. |

## Comparación de los cuatro archivos de código modificados (A → B → C)

`A` es el archivo en `7b6f7fc…`, `B` el archivo local, `C` el de `11e8fe6…`. Se compararon diffs y definiciones Python mediante AST; la igualdad de bytes entre B y C se verificó por lectura de ambos archivos.

| Archivo | Cambio A → B | Relación B → C y riesgo |
|---|---|---|
| `ingestion.py` | Añade `_PhysicalLines`; cambia `_validate_member` para limitar registros, columnas y campos, ignorar registros vacíos y usar línea física; `load_dataset` pasa a `gtfs-lab-csv/2`. | B = C byte a byte. No hay fix exclusivo. |
| `compliance_adapter.py` | `inspect_fixed_stop_references` pasa rutas al evaluador incremental, usa `dataset_hash_paths`, fija el SHA v2 y separa versión semántica de regla/evaluador. | B = C byte a byte. No hay fix exclusivo. |
| `compliance_v1_engine.py` | Añade `_SchemaMismatch`, `_AmbiguousIdentity`, `_BoundedLines`, `_table_rows`, `_stream_table`, `_stream_file`, `_open_input`, `_input_size` y `dataset_hash_paths`; cambia `csv_rows`, `inspect_gtfs`, `evaluate`, `read_bounded` y `main` para inspección acotada/incremental. | B = C byte a byte. No hay fix exclusivo. |
| `compliance_v1_current_gate.py` | Añade `replay_historical_package` y cambia `main` para comprobar paquete histórico y candidato v2 sin reescribir evidencia. | C conserva esas funciones y añade `--portable`, rutas explícitas de DB, preflight de recursos y fuentes, SQL portable, 377 checks de fase 2 en ese modo, y liga la DB al replay. Copiar B entero perdería esos controles. |

El HEAD histórico A carecía de las mejoras B2 en los tres primeros archivos. C las incluye de forma idéntica; en el gate C es un superconjunto funcional de B. No se identificó código válido exclusivo de B.

## Documentos modificados y evidencias especiales

| Documento | Disposición de los cambios locales |
|---|---|
| `02_Data_Engineering/GTFS_Lab/README.md` | M02/M03/A4: `ALREADY_REFLECTED`; triage B2 presentado como pendiente y HOLDOUT sin abrir: `STALE`/`CONTRADICTS_CURRENT_STATE` tras B3. |
| `03_Compliance/COMPLIANCE_V1_CURRENT_STATE.md` | Aprobación v2, hashes y gate: `ALREADY_REFLECTED` exactamente. |
| `PROJECT_STATUS.md` | M04-A4/B1/B2D: `HISTORICAL_ONLY`/`ALREADY_REFLECTED`; afirmaciones de HOLDOUT cerrado a futuro y fase M05 previa: `STALE`/`CONTRADICTS_CURRENT_STATE`. |
| `README.md` | Enlace a matriz: `UNIQUE_AND_STILL_VALID` como navegación histórica, recuperado en esta reconciliación; el README C añade la navegación a precondiciones técnicas. No se sustituye. |

Los seis JSON de `compliance_v1_20260929_m02_deep_review/` tienen nombres, estructura y bytes iguales a las salidas comprometidas bajo `compliance_v1_20260928/current_gate_04/`. El `summary.json` indica el mismo hash inicial/final de DB y PASS; los 28 casos de `pilot_replay.json` son sintéticos con evaluador `compliance-v1/1`. La carpeta no demuestra una ejecución independiente M02 ni aporta nueva procedencia. El gate B2D y su evidencia posteriores se conservan por separado en `main`; no se reinterpreta el replay antiguo como autoridad v2.

Los dos PNG se revisaron visualmente: el del 27/09 contiene porcentajes de avance de un estado previo; el del 28/09 describe las siete áreas y marca un ejemplo cartográfico como ilustrativo. Solo la radiografía local los enlaza. Se retienen con sus bytes originales para que ese documento histórico conserve sus referencias, sin promover sus mensajes a la documentación vigente. No se encontró una copia en `main` ni una referencia actual fuera de esa radiografía. La marca de archivo no demuestra cómo se generaron.

## Integración y comprobaciones

Se copiaron al worktree limpio únicamente los cuatro archivos de las filas 23, 24, 26 y 27, sin modificar su contenido. Este informe es nuevo y no forma parte del inventario de 28. Los cuatro SHA-256 antes/después de la copia coincidieron; se comprobaron firma y dimensiones de los PNG (1536×1024 y 1672×941), los diez enlaces locales de la radiografía y las 28 filas numeradas. No se portó código ni tests; por ello no se ejecutaron HOLDOUT, gates de bases protegidas ni suites de regresión de código. `git diff --cached --check` señala dos espacios finales en las líneas 3 y 4 de la matriz histórica: son los saltos de línea Markdown originales y se preservaron deliberadamente. El informe nuevo no introduce ese problema. La incorporación a `main` mediante Git queda separada de la raíz histórica.

## Respuestas finales

1. **Q1 — ¿Hay código fuente válido solo en la raíz histórica?** No. Los tres archivos de código con lógica B2 son idénticos a C; el gate C es más completo; el generador candidato ya está en C.
2. **Q2 — ¿Falta algún test de regresión?** No. Los dos tests locales son idénticos a los de C.
3. **Q3 — ¿Falta evidencia auténtica M04/Compliance?** No se encontró una ejecución M04/Compliance ausente. Los seis JSON de revisión profunda son duplicados byte a byte y el paquete/transición B2D ya están en C. Faltaban dos documentos históricos de planificación y sus dos imágenes enlazadas.
4. **Q4 — ¿Copiar archivos históricos modificados enteros regresaría `main`?** Sí: el gate perdería portabilidad/preflight; `PROJECT_STATUS.md` y el README de GTFS_Lab retrocederían el estado. El README raíz desplazaría navegación actual. Los otros cuatro archivos modificados ya coinciden en bytes.
5. **Q5 — ¿Podrá archivarse/limpiarse la raíz sin pérdida?** Sí, una vez que la integración histórica y sus hashes queden verificados en un destino duradero y haya aprobación explícita para la limpieza. No se ha limpiado ni alterado la raíz.
6. **Q6 — ¿Qué archivos requieren decisión humana antes de limpiar?** Ninguno requiere decisión técnica de clasificación. La decisión humana pendiente es autorizar la operación de limpieza de las 28 entradas tras verificar el destino; no se presume esa autorización aquí.

## Clasificación final para publicación

| Classification | Count |
|---|---:|
| Already represented in main | 14 |
| Duplicate evidence | 6 |
| Superseded | 4 |
| Historical material integrated | 4 |
| Human-decision classification | 0 |
| Total | 28 |

```text
VALID_SOURCE_CODE_ONLY_IN_ROOT = NO
MISSING_REGRESSION_TESTS = NO
MISSING_EXECUTION_JSON_EVIDENCE = NO
WHOLE_FILE_CODE_PORTING_SAFE = NO
ROOT_CLEANUP_POSSIBLE_AFTER_DURABLE_PRESERVATION = YES
```

Los cuatro artefactos conservados se clasifican individualmente como `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN`. El origen de cada uno es el worktree histórico local `C:\Users\yeiso\Desktop\Folder\VSCode\Proyectos\Transit Data Lab` en el HEAD `7b6f7fc21fb44f96d2f6d459c9d54115b1a52602`; destino y hashes corresponden a este repositorio en la rama de reconciliación.

| Ruta de origen histórico = destino | Bytes | SHA-256 | Clasificación |
|---|---:|---|---|
| `08_infografias/Infografia del proyecto a dia 27092026.png` | 1,899,393 | `c6979c98f9e5e11106e700b2f5ff4c6b548849dfaa8cec887b76917b9a267e87` | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` |
| `08_infografias/Infografia del proyecto a dia 28092026.png` | 2,018,130 | `cb79356e211d917447083afc2002b8ea7ed6a4af0cb48130b8533903a8a224d1` | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` |
| `reports/PROJECT_RADIOGRAPHY_2026-09-28.md` | 12,105 | `b100b7af30d41d8dafdc2178e03b9bf6378520be8ab1bad933e136285bd550ac` | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` |
| `reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md` | 17,768 | `9daee7b6b8b6bd1c94b4af1feb78d66e2c86e3db444184fe06ebe7a3e411c1a9` | `HISTORICAL_EVIDENCE_MISSING_FROM_MAIN` |

Los SHA-256 de origen y destino coinciden en los cuatro casos. Las referencias Markdown a los PNG son relativas desde `reports/PROJECT_RADIOGRAPHY_2026-09-28.md` y resuelven a los dos destinos anteriores. Las imágenes mantienen firma PNG válida y dimensiones 1536×1024 y 1672×941, respectivamente; no se regeneraron, recomprimieron ni editaron.

### Excepción de preservación byte a byte

`git diff --check` informa únicamente de espacios finales deliberados en `reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md`, líneas 3 y 4: cada uno implementa el salto de línea Markdown original tras `**Proyecto:** Transit Data Lab` y `**Fecha base:** 2026-09-28`. Clasificación: `KNOWN_HISTORICAL_BYTE_PRESERVATION_EXCEPTION`. La excepción se limita a esas dos líneas y a este archivo; cualquier otro hallazgo de whitespace es fallo. Los bytes fuente se conservan sin normalización.

### Publicación y regresión

La integración parte de `11e8fe6b20232f02622a6c27d29b7c960763e979`, que era `origin/main` al consultar `git ls-remote` durante esta revisión. El delta publicado se limita a los cuatro artefactos anteriores y este informe; no contiene código, tests, Compliance engine, GTFS_Lab engine, bases de datos ni HOLDOUT. La compilación (`compileall`), el gate de fuentes portables y las cinco familias de tests sintéticos (16 + 23 + 23 + 6 + 10 tests) pasaron. También pasaron Trust, Golden Contract, Golden Corpus, Golden Evaluator y ambos modos de Corpus Split. No se accedió a HOLDOUT ni se modificaron bases protegidas. El paso final de `git diff --check origin/main...HEAD` informa solo de las dos excepciones documentadas, por lo que ese paso literal del workflow no queda verde con los bytes preservados. La rama histórica queda preservada intacta con 8 archivos modificados, 20 no seguidos y 0 staged. Su limpieza requiere autorización explícita separada después de la preservación durable.
