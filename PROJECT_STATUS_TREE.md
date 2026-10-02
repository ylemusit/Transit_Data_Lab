# Transit Data Lab — mapa de estado vigente

**Actualizado:** 2026-10-02
**Fuente de detalle:** [PROJECT_STATUS.md](PROJECT_STATUS.md).

```text
TRANSIT DATA LAB
│
├── TRUST FOUNDATION                    ✅ CLOSED (gate técnico)
├── GTFS AUDIT ENGINE V1                ✅ CLOSED (alcance técnico documentado)
├── COMPLIANCE V1                       ✅ CLOSED_WITH_DEFERRALS
├── REMEDIATION ENGINE V1               ✅ CLOSED (alcance técnico documentado)
│
├── NÚCLEO DEL PRODUCTO — AÑO 1         🎯 ESPAÑA + GTFS + NeTEx
│   ├── GTFS PRODUCTIZATION              ✅ V1 CLOSED (P01–P09)
│   │   ├── P01–P06, P08                ✅ CLOSED
│   │   ├── P07 recurring                ✅ CLOSED_WITH_DOCUMENTED_LIMITATION
│   │   ├── CI remoto + E2E sintético   ✅ PASS (PR34 + POST-MERGE)
│   │   └── P09 cierre final             ✅ APPROVED; CIERRE TÉCNICO
│   └── NeTEx                             ✅ V1 PASS / CLOSED (alcance documentado)
│
├── REAL DATASET TEST BANK V1             ✅ CLOSED; HUMAN CLOSURE APPROVED
│   ├── Controlled Intake + Case ID      ✅ GTFS; SHA-256 + códigos no reutilizables
│   ├── Short workspace + metadata       ✅ OK / NOT_OK; registros y replay
│   ├── Validación real                  ✅ EMT PALMA LOCAL CASE COMPLETED; LOCAL / CONTROLLED
│   └── Aceptación remota                ✅ PR40 MERGED; CI PR + POST-MERGE PASS
├── REAL DATA HARDENING CAMPAIGN V1       ✅ PASS / CLOSED
│   ├── 7 datasets; 9 intentos / 8 OK     ✅ NOT_OK histórico preservado
│   ├── Replay requerido / fallos        ✅ PASS / 0 abiertos
│   └── PR #43 + CI PR/post-merge        ✅ MERGED / PASS
├── WINDOWS SELF-SERVICE CLIENT V1       🎯 NEXT_PROJECT_OBJECTIVE; NOT_STARTED
├── COMMERCIAL VALIDATION                ⚪ NOT_ESTABLISHED
├── GIS / QGIS                           🟡 SOPORTE Y EVIDENCIA CUANDO PROCEDA
│
└── BACKLOG POST-COMERCIALIZACIÓN        💤 FUERA DE LA SIGUIENTE FASE
    ├── SIRI
    ├── GTFS-RT
    ├── Colombia
    └── otros mercados y modos
```

El expediente real permanece local y controlado; solo se publica capacidad genérica y evidencia sintética. El banco tiene revisión técnica PASS y aceptación remota PASS (PR #40; runs 37023905768 y 37024096727). Está CLOSED; cierre humano aprobado por Yeison el 2026-10-02 tras verificar PR #40/#41 y sus cuatro runs PASS. La campaña de hardening es PASS/CLOSED en el alcance GTFS Schedule descrito en [PROJECT_STATUS.md](PROJECT_STATUS.md); sus conteos proceden del resumen controlado de campaña, no de verificación desde este repositorio. Se preservan los límites de procedencia/licencia, ejecución serial, recovery manual, optimización pendiente en feeds grandes, suite con un SKIP documentado y ausencia de validación comercial/mercado. Compliance tests PASS; el hash gate protegido no se repitió y la base no se modificó. WINDOWS SELF-SERVICE CLIENT V1 queda como NEXT_PROJECT_OBJECTIVE / NOT_STARTED. Contrato del banco en [TEST_BANK_V1.md](02_Data_Engineering/GTFS_Lab/TEST_BANK_V1.md). P07 mantiene PARTIALLY_COMPARABLE / RUNTIME_ONLY_CHANGE. NeTEx V1 cierre humano aprobado; PR #36–#38 fusionadas y CI final post-merge PASS (36971109479). N01 CLOSED_WITH_LIMITATIONS; N02–N09 CLOSED. EPIP completo y aplicabilidad jurídica de autobús siguen sin concluir. Los estados y límites de los bloques cerrados y del workflow constan en [PROJECT_STATUS.md](PROJECT_STATUS.md).

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
