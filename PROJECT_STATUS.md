# Transit Data Lab — estado vigente

**Mapa visual resumido:** [PROJECT_STATUS_TREE.md](PROJECT_STATUS_TREE.md). Actualizar ambos documentos en la misma tarea cuando un paso cambie el estado del proyecto; `PROJECT_STATUS.md` conserva el detalle y la evidencia.

## GTFS Audit Engine V1 — G04–G07 cerrados; G08–G10 preparados localmente, sin publicar

**Registro e inventario por pasos:** [GTFS Audit Engine V1 — registro e inventario G04–G07](02_Data_Engineering/GTFS_Lab/reports/GTFS_AUDIT_ENGINE_V1_G04_G07_EXECUTION_LOG.md).

```ini
G04 = PASS
G04_CLOSED = YES
G04_SCOPE = FROZEN
G04_IMPLEMENTATION = MERGED_AND_POST_MERGE_VERIFIED
G05 = PASS
G05_CLOSED = YES
G05_IMPLEMENTATION = MERGED_AND_POST_MERGE_VERIFIED
G06 = PASS
G06_CLOSED = YES
G06_IMPLEMENTATION = MERGED_AND_POST_MERGE_VERIFIED
G07 = PASS
G07_CLOSED = YES
G07_IMPLEMENTATION = MERGED_AND_POST_MERGE_VERIFIED
G04_G07_MERGE_COMMIT = 4b27d26ed507127e68b229ae65915d9cd0307024
G04_G07_PR = 26_MERGED
G04_G07_REMOTE_CI = PASS
G04_G07_POST_MERGE_CI_RUN = 36791698098
G04_G07_TECHNICAL_CLOSURE_DECISION = APPROVED_2026-10-01
G04_G07_HOLDOUT = NOT_RUN
G04_FINDINGS_IN_VALIDATION_FINDINGS = NO
M02_NORMALIZES_G04_FINDINGS = NO
G04_G07_MANIFEST_ARTIFACT_KNOWLEDGE = INDIRECT
G04_G07_LEGACY = PRODUCTIVE_WHERE_APPLICABLE
G04_IDENTITY_INVENTORY_METADATA = CREATED_LOCAL_UNPUBLISHED; KNOWN_CONTRACT_DEBT
G03 = BASELINE_CLOSED; LOCAL_BOUNDED_EVIDENCE_FIX_PENDING_MERGE
G04 = BASELINE_CLOSED; LOCAL_TWO_TABLE_CACHE_FIX_PENDING_MERGE
G08 = IMPLEMENTED_TESTED_LOCAL; PENDING_CI_MERGE_POST_MERGE_CLOSURE
G09 = IMPLEMENTED_TESTED_LOCAL; M02_UNCHANGED; PENDING_CI_MERGE_POST_MERGE_CLOSURE
G10 = DEVELOPMENT_COMPLETE_LOCAL; 14_COMPLETED; 0_PIPELINE_ERRORS; STABILITY_PASS
G10_HOLDOUT = NOT_ACCESSED
G11 = CLOSURE_REVIEW_CANDIDATE; NOT_CLOSED
GTFS_ENGINE_G08_G10_PR = 28; HEAD = cd2c3fb`r`nGTFS_ENGINE_G08_G10_REMOTE_CI = PASS; RUN 36803356048
GTFS_COMPLETE_COMPLIANCE = NOT_ESTABLISHED
```

El cierre G04–G07 acredita únicamente la integración y verificación técnica del alcance implementado. Los findings de G04 no forman parte actualmente de `validation.findings`; M02 no normaliza findings G04–G07. El manifest conoce los artefactos del run indirectamente, y el flujo legacy sigue productivo donde corresponda. No se ejecutó ni se accedió a HOLDOUT. Se conservan los gaps y elementos diferidos de cobertura; tampoco se declara equivalencia total con legacy, cumplimiento GTFS completo ni cumplimiento jurídico. El inventario G04 conserva `CREATED_LOCAL_UNPUBLISHED`, registrado como deuda contractual conocida sin modificar el inventario ni el runtime.

El trabajo local G08–G10 y la candidatura G11 constan en el [estado G08–G10](02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G08_G10_LOCAL_PROGRESS_20261001.md), el [informe G11](02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_V1_G11_CLOSURE_REVIEW_20261001.md) y la [evidencia del corpus DEVELOPMENT](02_Data_Engineering/GTFS_Lab/reports/evidence/g10_development/g10_development_results.json). El corpus split/lineage pasó; se ejecutaron 14 DEVELOPMENT con cero errores de pipeline y replay de estabilidad PASS. HOLDOUT no se accedió. La rama `feat/gtfs-engine-g08-g11` se publicó en la PR #28 (`cd2c3fb`); CI remoto PASS en el run [36803356048](https://github.com/ylemusit/Transit_Data_Lab/actions/runs/36803356048). Faltan merge, verificación post-merge y cierre humano; G08–G11 no se declaran cerrados.

Los cambios locales de memoria G03/G04 preservan la clasificación/finding y el inventario normativo, y pasan sus regresiones focalizadas. Quedan sujetos a regresión completa, CI y verificación post-merge. M02 no cambia y no registra el informe G09 suplementario.

El 2026-10-01 se registró la decisión de cierre técnico de G04–G07 tras integrar la PR #26. `origin/main` apunta al merge commit `4b27d26ed507127e68b229ae65915d9cd0307024` (base `137ff4ed38da65fb3fb61f9804d729a1cee51feb`, head `38bf16e1f06f938677fbe2158936479e3a1eb8c6`). El CI post-merge de GitHub Actions terminó PASS en ese commit ([run 36791698098](https://github.com/ylemusit/Transit_Data_Lab/actions/runs/36791698098)); la [PR #26](https://github.com/ylemusit/Transit_Data_Lab/pull/26) figura fusionada. La verificación actual confirma esos datos remotos. Compliance y Business conservan sus estados propios.

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
