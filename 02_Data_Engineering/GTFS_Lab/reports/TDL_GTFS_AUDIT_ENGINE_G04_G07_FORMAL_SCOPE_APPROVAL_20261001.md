# GTFS Audit Engine V1 — aprobación formal G05–G07 y revalidación

**Decisión:** el 2026-10-01 Yeison Arbey Carrillo Lemus aprobó los alcances congelados y las reglas propuestas de G05, G06 y G07, según la recomendación del análisis previo. La aprobación autoriza el registro tipado local y la revisión del candidato; no declara gates `CLOSED` ni autoriza HOLDOUT, commit, push o publicación.

## Registro tipado

G05–G07 ya declaraban reglas mediante `RULE_SPECS` y `build_phase_registry`. Cada declaración genera un `RuleDefinition` con categoría, autoridad, severidad, requisito, ficheros aplicables, referencia GTFS fijada a `2026-04-27`, applicability, identidad de evaluador y versión semántica `1.0.0`. El registro se congela antes de obtener el mapa determinista `rule_versions`.

Se añadió una regresión que construye el registro para los tres evaluadores y comprueba que contiene todos los IDs declarados, que está congelado, que mantiene versión/identidad y que cada definición conserva los metadatos y la referencia normativa. La estabilidad como contrato público sigue fuera del alcance de este gate.

## Verificación local

| Comprobación | Resultado |
| --- | --- |
| `python -m unittest discover -s tests` | 217 tests: 216 OK, 1 SKIP explícito |
| `python -m unittest tests.test_g04_identity tests.test_g05_g07_runtimes` | 51/51 PASS |
| Regresión de registro tipado G05–G07 y de identidad en resultados | PASS |
| `python -m compileall -q gtfs_lab tests tools` | PASS |
| `python tools/generate_g04_identity_inventory.py --check` | PASS, regeneración determinista |
| `git diff --check` | PASS, con aviso CRLF/LF histórico en `PROJECT_STATUS.md` |

El único `SKIP` sigue siendo la integración condicionada por la base Compliance protegida, ausente en este worktree. CI remoto no se ha ejecutado.

## Identidad del candidato

Base y HEAD continúan en `137ff4ed38da65fb3fb61f9804d729a1cee51feb`, sin commit. Nueve archivos del paquete del informe [de remediación](TDL_GTFS_AUDIT_ENGINE_G04_G07_REMEDIATION_20261001.md) conservan sus hashes; el décimo, la suite G05–G07, cambia para incorporar la nueva regresión. Los diez hashes vigentes son:

| Archivo | SHA-256 |
| --- | --- |
| `gtfs_lab/g04_identity.py` | `C2FF57DB4D1FCFD45269DF5461D7D541B9F853864379FED29BE710F16935B441` |
| `gtfs_lab/g05_temporal.py` | `8B8D5919DA48188E008DA24469128D8B7ABEB5702E0863251DB3DB59150DE00A` |
| `gtfs_lab/g06_operations.py` | `01E7F1B70F2B5AA34F9033DC09572765C5B17CFF22EB82D5AA08FB4014D121EE` |
| `gtfs_lab/g07_spatial.py` | `DB4C427296338A97F786B1BCCBFC355C79F7FD6E9FB98938BF7999D257EB8432` |
| `gtfs_lab/phase_runtime_contract.py` | `DEDA6DA6FB72112A78A19C362E4425614C9FEAC49E210F6446AD7C74FB482714` |
| `gtfs_lab/pipeline.py` | `E855B476C362EBBADA2777B06020B8059EA2FB0657556034FB065D6FE0D22F00` |
| `tests/test_g04_identity.py` | `B3DA1E0D36D4BD277F9BC71E3288A1CD968C9D19C99B91BED022186B3E0B640A` |
| `tests/test_g05_g07_runtimes.py` | `8D0EB42A3DA59563AEE99A2F66FBBEB89F5568C058947210A6DE54B1A433771F` |
| `spec/gtfs_schedule_g04_identity_references_2026_04_27.json` | `1691125CC2DECD90E2A011B2F86EB52512187CD72E60EF534D7E58AFD8CC1165` |
| `.github/workflows/gtfs-engine-preconditions.yml` | `F0BED4F2F2155BBCB4D2AB9C671D86BF45D4748091CDFACE728D4D9C03ACCA0E` |

## Estado de gate

La aprobación formal de alcance y el registro tipado quedan documentados para G05–G07. G04–G07 mantienen `LOCAL_TECHNICAL_REVIEW_PASS_CLOSURE_PENDING`; no se cambian a `CLOSED`. CI remoto, publicación y el gate final de cierre permanecen pendientes. No se ejecutó HOLDOUT ni se accedió a feeds de operadores.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
