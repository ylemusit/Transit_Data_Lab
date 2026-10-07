# Transit Data Lab — estado vigente

Actualizado: 2026-10-07. [Mapa resumido](PROJECT_STATUS_TREE.md) · [Arquitectura](ARCHITECTURE.md) · [Conocimiento](knowledge/README.md).

## Migración a P: — cierre operacional

`DEDICATED_PARTITION_MIGRATION_V1 = CLOSED_WITH_TEMPORARY_COMPATIBILITY_LINKS`. Raíz canónica `P:\TransitDataLab\01_Project\Transit Data Lab`; datos, evidencia, runtime y cliente en áreas externas separadas de P:. REVIEW_REQUIRED = 0; 11 raíces antiguas retiradas; C: CLEAN en el alcance auditado. Se retiraron 227.943.369.017 bytes regenerables y 12.503.583.020 bytes duplicados de P:; 87.175 archivos se copiaron con SHA-256 antes de retirar C:. 34 junctions documentadas, todas dentro de P:. Fuente, ramas/worktrees, checkpoints, Test Bank, HOLDOUT, firma y EXE aceptado preservados.

50 tests focales, E2E sintético de banco, Compliance portátil, lint, typecheck, Git y hashes PASS. Entornos reconstruidos desde recetas. Pendiente independiente: advisory crítico de MapLibre 6.3.0; no se ha actualizado la baseline de Desktop ni declarado seguridad integral. [Cierre, evidencia, links y límites](reports/DEDICATED_PARTITION_MIGRATION_V1.md).

## Reconciliación del entorno local V2

`LOCAL_ENVIRONMENT_RECONCILIATION_V2 = CLOSED_WITH_PROTECTED_RESIDUALS`. La raíz canónica está reconciliada con main; 58 worktrees y 7 copias independientes retirados. Esta resolución elimina 13.032.566.151 bytes lógicos, descontando las copias originales conservadas; total V2 13.278.198.318 bytes. Los 14 originales DEVELOPMENT y el schema NeTEx están en la raíz externa aprobada, con aliases contractuales verificados; se conserva una copia operacional del EXE aceptado. Tests focalizados 44/44 PASS; integridad Git, hashes y rutas operativas PASS. Test Bank, fuentes físicas HOLDOUT, checkpoints/capturas congelados y material privado permanecen protegidos; no quedan grupos de decisión humana pendientes. [Resultado, retención y límites](reports/LOCAL_ENVIRONMENT_RECONCILIATION_V2.md).

El cierre R1 sigue siendo histórico `CLOSED_WITH_PROTECTED_LEGACY_RESIDUALS`: sus 6.395.371.423 bytes no se vuelven a contar en V2. [Resumen R1](reports/LOCAL_WORKSPACE_RECONCILIATION_R1_SUMMARY.md).

## Product Readiness V1 — listo para piloto controlado con limitaciones
**Estado (2026-10-06):** `TRANSIT_DATA_LAB_PRODUCT_READINESS_V1 = READY_FOR_CONTROLLED_PILOT_WITH_LIMITATIONS`. El alcance actual es uso interno: `CLIENT_DISTRIBUTION = NO`, `PUBLIC_INSTALLER_DISTRIBUTION = NO`, `CUSTOMER_LOCAL_EXECUTION = NO`. Windows Client V1 se considera herramienta operacional interna cerrada con limitaciones; la aceptación W02–W08 es PASS_WITH_LIMITATIONS. PR #51 se fusionó el 2026-10-05 en `37bd5c5459c2f9ebad5f5cf4364ba209963cf6cd`; el CI post-merge run `37360863986` terminó SUCCESS sobre ese SHA. No se publicó release. La validación clean-machine existente sigue `PARTIAL / BLOCKED_BY_ENVIRONMENT`; no se repitió. Para este producto, el sobre de hardware y distribución pública queda diferido y no es requisito de readiness interno. Firma de código y SmartScreen también diferidos; SaaS es opción futura fuera del scope actual.

El nuevo contrato de informe en español proyecta la matriz completa de reglas, Compliance, estados de aplicabilidad/evaluabilidad, evidencia, interpretación, publicación y límites desde los artefactos existentes. Gap analysis: [COMPLIANCE_REPORT_GAP_ANALYSIS_V1](reports/COMPLIANCE_REPORT_GAP_ANALYSIS_V1.md); cierre técnico y gates: [PRODUCT_READINESS_V1_CLOSURE](reports/PRODUCT_READINESS_V1_CLOSURE.md). La ejecución E2E es sintética y reproducible; no acredita piloto comercial, demanda, disposición a pagar, cumplimiento jurídico, aceptación NAP ni cobertura GTFS universal. `MARKET_VALIDATED = NO`, `DEMAND = NO`, `WTP = NO`, `DIFFERENTIATION = UNPROVEN`; HOLDOUT no se accedió en este pack.

```ini
TRANSIT_DATA_LAB_PRODUCT_READINESS_V1 = READY_FOR_CONTROLLED_PILOT_WITH_LIMITATIONS
WINDOWS_CLIENT_V1 = CLOSED_WITH_LIMITATIONS
WINDOWS_CLIENT_ROLE = INTERNAL_OPERATIONAL_TOOL
CLEAN_MACHINE_VALIDATION_V1 = PARTIAL / BLOCKED_BY_ENVIRONMENT (W08 evidence; not rerun)
SUPPORTED_OPERATING_ENVELOPE_V1 = DEFERRED_NOT_REQUIRED_FOR_CURRENT_PRODUCT_SCOPE
PUBLIC_WINDOWS_DISTRIBUTION = DEFERRED
CODE_SIGNING = DEFERRED
SMARTSCREEN_REPUTATION = DEFERRED
FUTURE_SAAS = FUTURE_OPTION_NOT_CURRENT_SCOPE
MARKET_VALIDATED = NO
DEMAND = NO
WTP = NO
DIFFERENTIATION = UNPROVEN
HOLDOUT_CONTENT_NEWLY_ACCESSED = NO
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Capacidades cerradas y evidencias

| Capacidad | Estado técnico y fuente |
| --- | --- |
| Trust Foundation | PASS técnico; [cierre M05](02_Data_Engineering/GTFS_Lab/reports/TDL_M05_CLOSURE.md). |
| GTFS Audit Engine | CLOSED en alcance V1; [revisión G11](02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_V1_G11_CLOSURE_REVIEW_20261001.md). Condiciones/tipos pendientes y archivos diferidos siguen fuera de cobertura. |
| Compliance V1 | CLOSED_WITH_DEFERRALS; [informe maestro](03_Compliance/reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md). |
| Interpretación | FROZEN / VALIDATED_WITH_DOCUMENTED_LIMITATIONS; [freeze](reports/TDL_AUDIT_INTERPRETATION_V1_FREEZE_DECISION_20261004.md). GENERALIZATION_PASS_WITH_LIMITATIONS; [publicación content-blind](reports/TDL_AUDIT_INTERPRETATION_V1_HOLDOUT_CONTENT_BLIND_20261004.md). No nuevo acceso HOLDOUT. |
| Cliente Windows interno | W02–W08 PASS_WITH_LIMITATIONS; APPLICATION_DEFECT_001 CLOSED_FIXED_AND_VERIFIED; [W08](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W08_PACKAGING_RELEASE.md). |
| NeTEx | V1 CLOSED dentro del alcance aprobado; detalles y límites en la tabla de áreas. |

RC aceptado: SHA-256 `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266`. La aceptación manual W08 está documentada; V2 solo ha vuelto a verificar identidad del EXE. Clean-machine continúa PARTIAL/BLOCKED_BY_ENVIRONMENT; firma, SmartScreen, hardware mínimo y feeds extremos no están certificados. Dataset 019 conserva su limitación de recursos. No se publica release.

GTFS Client Audit Workflow, Remediation, Test Bank y hardening conservan sus cierres aprobados. El banco y los intentos NOT_OK históricos permanecen intactos; esta tarea no recuenta sus casos ni reejecuta datasets. RAW findings son inmutables; accounting y semántica no cambian. El rendimiento muestreado no es un máximo exacto del sistema.

## Estado por área
| Área | Estado y límites |
| --- | --- |
| 01_Research_Standards | Investigación de perfil/fuentes NeTEx documentada; [cierre técnico N09](01_Research_Standards/NeTEx/N09_TECHNICAL_CLOSURE_CANDIDATE_20261002.md). Distinguir cierre técnico, perfil y aceptación NAP. |
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

## Antecedentes

Las cronologías, SHAs y gates anteriores están en [el estado previo preservado en Git](https://github.com/ylemusit/Transit_Data_Lab/blob/cf4e0a30f6837b077e6994305f51fbf2cca8282c/PROJECT_STATUS.md) y sus informes enlazados. Las instantáneas congeladas permanecen intactas. Las fechas históricas no sustituyen el estado vigente; un PASS documental/sintético no valida mercado ni cumplimiento jurídico.

## Antecedente de migración V1 — sustituido por el cierre

2026-10-07: nueva pasada completada sobre los 81 temporales antes inaccesibles: 489 archivos, 226 directorios y 635.338.932 bytes lógicos eliminados; MIGRATE_TO_P = NO. DEDICATED_PARTITION_MIGRATION_V1 = REVIEW_REQUIRED_PROTECTED_MATERIAL: la ACL del material privado de firma y la herencia más amplia de P: requieren resolver su política de acceso antes del traslado. Sin cutover ni retiro de raíces; HOLDOUT intacto. Expediente vigente: P:\TransitDataLab\03_Evidence\Historical\migration_v1\resume_report_20261007.md y final_footprint.json. Este estado no cambia los gates de producto.
## Antecedente de descomposición V1 — sustituido por el cierre

2026-10-07: `CANONICAL_WHOLESALE_MIGRATION = PROHIBITED`; `CANONICAL_CUTOVER = NO`. Descomposición completa: 28 hijos directos y 34.742 filas recursivas, sin seguir 15 reparse points y sin errores de acceso. La raíz medida tras retirar el PFX tiene 290.967 archivos, 150.733 directorios y 283.567.279.349 bytes lógicos. 06_Products explica 261,771 GiB. Distribución propuesta: 0,515 GiB para fuentes y metadata de cuatro repositorios independientes; 207,787 GiB de candidatos regenerables; 9,584 GiB de workspaces mixtos por revisar. No se ha efectuado limpieza adicional ni se ha declarado duplicidad por nombre. Checkpoints congelados, paquetes y evidencia se preservan fuera de la fuente.

Proyección conservadora de ingress a P: 105,308 GiB, conservando todas las unidades dudosas y otras raíces legacy y excluyendo regenerables; cabe con presupuesto de reconstrucción de runtime y reserva, pero no acredita transferencia, eliminación ni funcionamiento. Pendientes: reconciliar unidades mixtas y contratos de rutas, sanity checks por unidad, transferencia verificada y validación operacional antes del cutover.

La decisión privada de firma está resuelta: PFX trasladado a P:\TransitDataLab\Private\Signing, SHA-256 de origen/destino coincidentes y ACL de origen capturada; carpeta y PFX sin herencia, con acceso exclusivo para Yeison, SYSTEM y Administradores. Origen retirado tras verificar. El registro permanece restringido y no se publica en Git. HOLDOUT intacto; no se abrió, hasheó ni modificó su contenido. Este estado sustituye el bloqueo anterior por política de acceso al PFX y no cambia los gates de producto.

Expediente completo y columnas solicitadas: P:\TransitDataLab\03_Evidence\Historical\migration_v1\storage_decomposition\STORAGE_DECOMPOSITION.md, direct_children.json/csv, recursive_decomposition.json/csv, category_allocation.json y capacity_projection.json. Los informes y cambios locales previos se conservan. Sin commit, push ni publicación.
