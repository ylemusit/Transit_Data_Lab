# GTFS Audit Engine V1 — registro e inventario G04–G07

**Entrada rápida:** `PROJECT_STATUS.md` → sección «GTFS Audit Engine V1 — candidatos locales hasta G07» → este registro.\
**Worktree:** `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g04`\
**Base / HEAD local:** `137ff4ed38da65fb3fb61f9804d729a1cee51feb`\
**Última actualización:** 2026-10-01

## Estado en una mirada

| Paso | Solicitud / objetivo | Estado | Registro principal |
| --- | --- | --- | --- |
| 01 | Aprobar alcances y reglas G05–G07; verificar su registro tipado | CERRADO localmente | [Aprobación formal y revalidación](TDL_GTFS_AUDIT_ENGINE_G04_G07_FORMAL_SCOPE_APPROVAL_20261001.md) |
| 02 | Publicar candidato en una rama y abrir PR para ejecutar CI remoto | CERRADO | [PR #26](https://github.com/ylemusit/Transit_Data_Lab/pull/26) |
| 03 | Revisar CI remoto y resolver sus resultados | EN CURSO | Check `synthetic`, run `36790578771`, pendiente |
| 04 | Decidir cierre técnico G04–G07 | NO INICIADO | Depende de pasos anteriores; requiere decisión de cierre |

G04–G07 conservan revisión técnica local `PASS`; ninguna fase figura `CLOSED`. No se ha ejecutado HOLDOUT. La autorización de alcance de G05–G07 no equivale a autorización de publicación.

## Registro cronológico de pasos

### Paso 01 — aprobación de alcances y registro tipado

- **Solicitado:** continuar según la recomendación tras valorar si convenía aprobar G05–G07.
- **Analizado:** los runtimes ya declaraban las reglas mediante `RULE_SPECS` y `build_phase_registry`; faltaba una regresión que verificase exhaustivamente las definiciones tipadas.
- **Propuesto:** aprobar alcances y reglas localmente, añadir la regresión y volver a validar, manteniendo CI remoto y cierre como gates separados.
- **Decidido:** Yeison aprobó proceder con esa recomendación el 2026-10-01.
- **Implementado:** regresión de registro tipado; aprobación anotada en los tres documentos de alcance; addendum técnico; actualización del estado vigente.
- **Resultado:** todos los IDs G05–G07 se construyen en registros congelados con identidad, versión, categoría, autoridad, severidad, requisito, aplicabilidad, ficheros y referencia normativa.
- **Validación:** 217 pruebas totales (216 OK, 1 SKIP); 51/51 focalizadas; compilación, inventario determinista y `git diff --check` PASS. Detalle y hashes en el [addendum](TDL_GTFS_AUDIT_ENGINE_G04_G07_FORMAL_SCOPE_APPROVAL_20261001.md).
- **Cierre:** cerrado localmente el 2026-10-01. No cierra los gates G04–G07.
- **Siguiente:** paso 02, publicar el candidato con autorización expresa.

### Paso 02 — publicación controlada para CI remoto

- **Solicitado:** avanzar hasta completar G07; la conversación pide ahora poder retomar cada paso desde sus archivos.
- **Analizado:** sin publicar una rama/PR no se ejecuta el CI remoto del candidato. La política del proyecto exige autorización expresa para commit, push y publicación.
- **Recomendación vigente:** commit, push y abrir PR para CI, sin merge. La PR permite inspeccionar cambios y resultados antes de decidir cierre.
- **Decisión:** Yeison autorizó commit, push y apertura de PR el 2026-10-01; la autorización no incluye merge.
- **Implementado:** commit `8cd59cd72866ddc5d27c3c7b5ac71f22ff73aba6`; rama `feat/gtfs-engine-g04-identity-referential` publicada en `origin`.
- **Resultado:** [PR #26](https://github.com/ylemusit/Transit_Data_Lab/pull/26), estado `OPEN`, base `main`, head inicial `8cd59cd72866ddc5d27c3c7b5ac71f22ff73aba6`. No se fusionó.
- **Validación:** `origin/feat/gtfs-engine-g04-identity-referential` coincide con el commit; `git diff --cached --check` PASS antes del commit.
- **Cierre:** paso 02 cerrado el 2026-10-01 con la PR abierta y disponible para revisión.
- **Siguiente:** paso 03, revisar los checks remotos y registrar el resultado final.

### Paso 03 — CI remoto

- **Solicitado:** ejecutar los checks del repositorio sobre el candidato publicado.
- **Analizado:** la PR #26 disparó el check `synthetic` en Actions.
- **Decidido:** revisar el resultado sobre el HEAD final y registrar cualquier fallo antes de declarar el paso cerrado.
- **Implementación:** el registro de la publicación se añade como commit documental a la misma PR; esto actualizará su HEAD y reiniciará los checks.
- **Resultado / validación:** pendiente del CI remoto sobre el HEAD final.
- **Estado:** en curso.
- **Siguiente:** cerrar el paso 03 tras confirmar los checks; después abrir paso 04 para decidir el cierre técnico G04–G07.

## Inventario de archivos

Los estados describen el worktree candidato, no necesariamente archivos ya comprometidos en Git. `PRESENTE` significa que existe localmente. Los documentos de alcance conservan `DRAFT` en su nombre histórico, aunque su estado formal actualizado figura dentro de cada archivo.

| Área | Ruta relativa al repositorio | Finalidad | Estado |
| --- | --- | --- | --- |
| Fuente | `02_Data_Engineering/GTFS_Lab/gtfs_lab/g04_identity.py` | Identidad y referencias G04 | PRESENTE; revisión técnica local PASS |
| Fuente | `02_Data_Engineering/GTFS_Lab/gtfs_lab/g05_temporal.py` | Reglas temporales G05 | PRESENTE; revisión técnica local PASS |
| Fuente | `02_Data_Engineering/GTFS_Lab/gtfs_lab/g06_operations.py` | Reglas operativas G06 | PRESENTE; revisión técnica local PASS |
| Fuente | `02_Data_Engineering/GTFS_Lab/gtfs_lab/g07_spatial.py` | Reglas espaciales G07 | PRESENTE; revisión técnica local PASS |
| Contrato | `02_Data_Engineering/GTFS_Lab/gtfs_lab/phase_runtime_contract.py` | Registro tipado común de fases | PRESENTE; usado por G05–G07 |
| Integración | `02_Data_Engineering/GTFS_Lab/gtfs_lab/pipeline.py` | Integración de candidatos con pipeline | PRESENTE; local, sin publicación |
| CI | `.github/workflows/gtfs-engine-preconditions.yml` | Workflow de precondiciones del engine | PRESENTE; CI remoto pendiente |
| Pruebas | `02_Data_Engineering/GTFS_Lab/tests/test_g04_identity.py` | Regresiones focalizadas G04 | PRESENTE; 51 focalizadas junto con suite posterior |
| Pruebas | `02_Data_Engineering/GTFS_Lab/tests/test_g05_g07_runtimes.py` | Regresiones G05–G07 y registro tipado | PRESENTE; contiene la última regresión añadida |
| Compatibilidad | `02_Data_Engineering/GTFS_Lab/tests/test_g03_file_catalog.py` | Regresiones del catálogo G03 | PRESENTE; cambio local de integración |
| Especificación | `02_Data_Engineering/GTFS_Lab/spec/gtfs_schedule_g04_identity_references_2026_04_27.json` | Identidad fijada de referencias e inventario G04 | PRESENTE; SHA comprobado |
| Herramienta | `02_Data_Engineering/GTFS_Lab/tools/generate_g04_identity_inventory.py` | Regeneración determinista del inventario G04 | PRESENTE; `--check` PASS |
| Alcance | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G04_SCOPE_20260930.md` | Contrato de alcance G04 | PRESENTE; revisión formal PASS registrada |
| Alcance | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G05_SCOPE_DRAFT_20260930.md` | Alcance aprobado G05 | PRESENTE; aprobado 2026-10-01 |
| Alcance | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G06_SCOPE_DRAFT_20260930.md` | Alcance aprobado G06 | PRESENTE; aprobado 2026-10-01 |
| Alcance | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G07_SCOPE_DRAFT_20260930.md` | Alcance aprobado G07 | PRESENTE; aprobado 2026-10-01 |
| Revisión | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G04_G07_LOCAL_REVIEW_20261001.md` | Revisión inicial con `CHANGES_REQUESTED` | PRESENTE; antecedente histórico, no estado vigente |
| Revisión | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G04_G07_REMEDIATION_20261001.md` | `PASS` técnico local y hashes previos | PRESENTE; antecedente técnico |
| Revisión | `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G04_G07_FORMAL_SCOPE_APPROVAL_20261001.md` | Decisión de alcance, verificación y hashes actuales | PRESENTE; registro vigente del paso 01 |
| Estado | `PROJECT_STATUS.md` | Estado vigente y enlace a este registro | PRESENTE; entrada rápida del proyecto |
| Registro | `02_Data_Engineering/GTFS_Lab/reports/GTFS_AUDIT_ENGINE_V1_G04_G07_EXECUTION_LOG.md` | Secuencia de pasos e inventario de archivos | ESTE ARCHIVO |

## Cómo retomar desde otro chat

1. Abrir `PROJECT_STATUS.md` y su sección superior de GTFS Audit Engine V1.
2. Seguir el enlace a este registro y leer la fila del paso actual.
3. Abrir solo el registro principal enlazado para ese paso y los archivos que indique el inventario.
4. Añadir cada nuevo resultado como paso numerado; conservar los pasos cerrados y actualizar el índice, el estado y el inventario.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
