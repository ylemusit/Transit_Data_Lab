# Transit Data Lab — estado vigente

## GTFS Audit Engine V1 — cierre G02

PR #22 se fusionó mediante merge normal el 2026-09-30. `G02 = PASS`, `GTFS_AUDIT_ENGINE_V1_RULE_REGISTRY = CLOSED` y `GTFS_AUDIT_ENGINE_V1_G03 = READY_TO_START`; G03 no se ha iniciado. Merge commit y nuevo `main`: `8e2b1cac53e96f4000f8be0d9c03da4350edfbee` (padres: base `d7f4c76ce5c13844ea49303f0434f83d31d95a4c`, head revisado `8ca39ab61a7e4c7c80e943d12c2ba328b98a6b82`). PR #22 quedó fusionada a las 01:58:54 UTC. El check remoto `synthetic` pasó sobre el head revisado y sobre el merge commit; la regresión local focalizada pasó por separado. Split y lineage se comprobaron solo con metadatos; no se accedió al contenido HOLDOUT. Detalle de contrato, identidad, regresión y CI en el [informe de cierre G02](reports/repository_integrity/TDL_GTFS_AUDIT_ENGINE_G02_CLOSURE.md).

## Desarrollo posterior a la base del GTFS Audit Engine

PR #21 está cerrada y fusionada. Su merge commit fue `d7f4c76ce5c13844ea49303f0434f83d31d95a4c`, con padres `4bb2275d9792942d5c879ca22d01fa250413457f` y `dc486d37a681975d18d4e9914f0a59cfcad59641`, `merged_at = 2026-09-30T01:19:27Z`; cerró `G01 = PASS` y `GTFS_AUDIT_ENGINE_V1_SCOPE = CLOSED`. Main avanzó posteriormente con PR #22, registrada arriba. La evidencia de precondiciones de G01 queda en [el pack de cierre](reports/repository_integrity/TDL_GTFS_ENGINE_PRECONDITIONS_PACK_CLOSURE.md).

G02 incorporó el registro de reglas tipado, applicability trazable, cobertura, estado nativo versionado e identidad registrada separada de la ejecución. Su cierre y regresión están documentados en el [informe G02](reports/repository_integrity/TDL_GTFS_AUDIT_ENGINE_G02_CLOSURE.md). El registro sigue sin gobernar la validación productiva; GTFS_Lab V1 conserva sus resultados. ChangeAttribution 1.0.0 y `MANIFEST_VERSION = 1.1.2` permanecen intactos; ChangeAttribution 1.1.0 recibe identidad por regla.

Actualizado: 2026-09-30. Sustituye únicamente las afirmaciones operativas obsoletas de las instantáneas anteriores; no promueve ni modifica sus baselines. Evidencia y límites en [la revisión](reports/repository_integrity/PROJECT_ALIGNMENT_REVIEW.md).

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

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
