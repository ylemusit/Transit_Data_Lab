# Compliance V1 — estado vigente

2026-09-29: **COMPLIANCE_V1 = CLOSED_WITH_DEFERRALS** para el engine/lab y los dos scopes de [COMPLIANCE_V1_SCOPE](COMPLIANCE_V1_SCOPE.md). Implementación actual `compliance-v1/2` aprobada y congelada por M04-B2D; la regla semántica continúa `V1-RULE-GTFS / compliance-v1/1`.

| Elemento | Estado |
|---|---|
| Phase 1 / Phase 2 | FROZEN; 92 provisions, 36 source facts, 48 requirements, 10 deadlines; filas anteriores intactas. |
| Phase 3 | CLOSED_WITH_DEFERRALS bajo alcance V1. B02 conserva CLOSED_WITH_DEFERRALS. |
| GTFS / NeTEx | READY / OPERATIONAL_COMPLIANCE_TRACK, exclusivamente scopes V1. |
| SIRI / GTFS-RT | STANDBY; DEFERRED_BY_PRODUCT_SCOPE. |
| Mappings / coverage | 15 mappings y 10 decisiones sin cambios: 9 PARTIAL, 1 UNRESOLVED. |
| Concepts / scopes | 9 conceptos, 11 bridges y 11 scopes; +2 técnicos de V1. |
| Representability / observaciones | 2 assertions PARTIAL; 28 observaciones de fixtures sintéticos; 0 observaciones de operadores. |
| Reglas | V1-RULE-GTFS y V1-RULE-NETEX; 2 técnicas automáticas para subscopes, sin conclusión jurídica. V1-RULE-GTFS mantiene semantic identity `compliance-v1/1`. |
| Implementación actual | `compliance-v1/2`; evaluator SHA-256 `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; parser `gtfs-lab-csv/2`; paquete SHA-256 `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`. [Pointer actual](reports/evidence/compliance_v1_current_implementation_v2.json). |
| Requisitos | 0 completos; 6 PARTIAL, 12 HUMAN_REVIEW_REQUIRED, 20 DEFERRED, 10 OUT_OF_SCOPE_V1. |
| Familias | 0 completas; 5 PARTIAL_WITH_ACCEPTED_LIMITS, 4 DEFERRED. |

Contrato persistido de observación `phase3-observation-envelope/1`; evaluator actual `compliance-v1/2`. Se usan tablas existentes, sin migración. El paquete v1 y las filas persistidas históricas conservan identidad `compliance-v1/1`; el paquete actual v2 se gobierna mediante el pointer aprobado, sin reescritura de DB ni evidencia histórica. Resultados de auditoría técnica en las envolventes de observación y JSON reproducibles; `audit.runs/results/evidence` no se rellenan como si fueran auditorías de operadores.

Gate vigente único: `tools/compliance_v1_current_gate.py`. [Salida completa PASS M04-B2D](reports/evidence/compliance_v1_20260929/current_gate_m04b2d_final4/summary.json). El gate reproduce de forma separada el generador histórico v1 y el generador actual aprobado v2. El gate B02 sirve para su preestado histórico; no debe aplicarse sin conciliación a las nuevas capas V1. Phase 2 mantiene un FAIL histórico explícito por `audit.rules=0`; sus otros 386 checks y los 22 de Phase 1 pasan. Incluye hashes de fuentes legales.

```powershell
python tools/compliance_v1_current_gate.py --evidence 03_Compliance/reports/evidence/compliance_v1_recheck_YYYYMMDD_unique
```

Usar un directorio nuevo. Requiere Python 3.12, DuckDB CLI y lxml ya disponibles (versiones exactas en el gate), DB local y corpus congelado. Evaluación offline; las fuentes técnicas y fixtures están capturados. El gate no importa feeds ni modifica bases. El replay de persistencia se demuestra en copia aislada; `--persist` solo acepta el hash inicial y no debe ejecutarse sobre la DB cerrada.

Límites: GTFS fixed-stop y tres tablas, máximo 1 MiB por archivo/10.000 filas; no valida feed completo. NeTEx Line aislada contra EPIP XSD 1.3.1 fijado, no perfil nacional, publicación completa ni semántica jurídica. No existen datos de operadores en los pilotos. El XSD EPIP utilizado ya no se mantiene; otros artefactos necesitan una evaluación explícita.

Pendientes/reapertura: realtime SIRI/GTFS-RT al abrir su futuro track; otros perfiles NeTEx y reglas GTFS ante una necesidad concreta y versión verificable; contexto NAP, temporal e institucional mediante registros y revisión humana; F05–F08 mediante evidencia de cambios, calidad, reutilización y solicitudes. B02 C04/C08/5-SN-D/CM/U01–U03 conservan sus decisiones históricas, sin bloquear V1.

DB final: `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`. Una transacción, +44 filas; cero migraciones. Checkpoint lógico y límites en [el informe maestro](reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md). La aprobación M04-B2D está en [el informe de transición](../reports/GTFS_LAB_M04B2A_COMPLIANCE_PACKAGE_TRANSITION.md); HOLDOUT V2 requiere identidad post-merge y autorización específica.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
