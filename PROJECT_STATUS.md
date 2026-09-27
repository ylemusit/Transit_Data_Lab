# Transit Data Lab — estado vigente

Actualizado: 2026-09-27. Sustituye únicamente las afirmaciones operativas obsoletas de las instantáneas anteriores; no promueve ni modifica sus baselines. Evidencia y límites en [la revisión](reports/repository_integrity/PROJECT_ALIGNMENT_REVIEW.md).

## Identidad y repositorios

| Elemento | Estado comprobado |
| --- | --- |
| Proyecto global | Transit Data Lab, siete áreas conceptuales incluyendo Business. |
| Raíz local | Rama main; HEAD `3c122f48ce4425c2e34313a2a65dcb9218bc77f5`. |
| Baseline raíz | `tdl-baseline-v0.1` apunta a ese HEAD. No es la versión del producto Desktop. |
| Remoto raíz | `https://github.com/ylemusit/Transit_Data_Lab.git`; main y etiqueta anunciados coinciden con la baseline local. |
| Remoto Desktop | `https://github.com/ylemusit/GTFS-Explorer-Desktop.git`; historia independiente del contenedor. |
| Baseline Desktop | `v0.2.2` → `85c700587ffec06d73d84825e1951fb73259b62c`, local y remota. |
| HEAD Desktop | `38e0e96dbeabaf00d53ed4d85509e5a4ce0b06fd`: commit documental posterior al release. |
| Visibilidad | Ambos repositorios públicos según consulta GitHub actual. Las declaraciones anteriores de privacidad son históricas. |

Los informes `REMOTE_GITHUB_ALIGNMENT.md`, `REMOTE_HISTORY_REVIEW.md` y `LEGACY_REPOSITORY_RENAME_READINESS.md` documentan el estado anterior a la separación efectiva de los remotos. El bloqueo UNRELATED_HISTORIES de esos informes no describe la relación actual entre HEAD raíz y su origin/main. No se deben fusionar historias para resolver un bloqueo ya superado.

Desktop tiene 20 entradas locales de estado, incluidas modificaciones de código y tests. Engineering y Artifacts también tienen cambios previos; el restore de 0.2.2 está limpio. Estas observaciones no modifican la etiqueta del release, pero impiden considerar el working tree de Desktop una copia limpia de esa baseline. No se han revertido ni revisado funcionalmente esos cambios.

## Estado por área

| Área | Estado y límites |
| --- | --- |
| 01_Research_Standards | Estructura planificada, sin implementación observada en la baseline. |
| 02_Data_Engineering | GTFS raw implementado; sentinel de integridad; core, validation y analysis pendientes. GTFS-RT, NeTEx y SIRI planificados. |
| 03_Compliance | Phase 1 y Phase 2 FROZEN; 92 provisions, 36 source facts, 48 requirements, 10 deadlines. Phase 3 no iniciada. |
| 04_Interoperability | Mappings pendientes; no se presupone conversión 1:1. |
| 05_Audits | Estructura planificada; evidencia de 20 operadores ubicada en GTFS_Lab. |
| 06_Products | Desktop, Engineering, Artifacts y backups separados del índice raíz. Desktop baseline 0.2.2 protegida. |
| 07_Business | V1 FROZEN; Business Phase 3 IN_PROGRESS. Stage 1 INCOMPLETE, S1-EXIT-09 INSUFFICIENT_EVIDENCE, gate NOT_REACHED; Stage 2 no autorizado. |

Los PASS previos de market evidence y validation readiness son documentales. No contradicen el gate Stage 1 pendiente. MARKET_VALIDATED = NO, DEMAND_VALIDATED = NO, WILLINGNESS_TO_PAY = NO, DIFFERENTIATION = UNPROVEN.

## Integridad y pendientes

Las dos bases actuales coinciden con sus hashes registrados, comprobados en esta revisión:

- GTFS raw: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Compliance Phase 2: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`.

La concordancia de bytes no certifica semántica GTFS, fidelidad textual o cumplimiento jurídico. Se mantienen las anomalías Annex 1.3 B-I/D-I, siete dependencias PARTIAL y mappings/reglas pendientes. El SQL del gate posterior a materialización incluye rutas absolutas y `read_blob`; no es un gate portable para un nuevo checkout. Los tests históricos de Phase 1, pre-materialización y el test 23 del master inicial de Phase 2 no deben aplicarse como expectativas del estado materializado. La revisión obtiene 27 PASS / 1 FAIL en ese master antiguo y 377/377 PASS en las comprobaciones de filas del gate final, excluyendo diez hashes jurídicos. Ver [la política de tests](03_Compliance/TEST_BASELINE_POLICY.md).

GIS conserva tres KML sin generador reproducible. `main.stops` sigue siendo un duplicado documentado cuyo propósito está pendiente de aclaración. Git conserva fuentes y evidencia seleccionada; bases, feeds, repositorios anidados y grandes generados requieren backup separado. La publicación del Git raíz no acredita ese backup integral.

La documentación piloto histórica contiene referencias a 0.2.1 y al alcance previo del producto. No se sustituyen las versiones de runs ya generados por 0.2.2. La guía vigente del laboratorio diferencia esos resultados del proyecto global.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
