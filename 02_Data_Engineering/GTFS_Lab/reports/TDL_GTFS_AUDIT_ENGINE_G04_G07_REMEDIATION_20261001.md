# GTFS Audit Engine V1 — remediación local G04–G07

**Decisión de revisión técnica local:** `PASS` para G04–G07 sobre los bytes indicados. Esto valida el alcance técnico del candidato local; no declara fases `CLOSED` ni autoriza commit, publicación o HOLDOUT. CI remoto queda pendiente.

**Base / HEAD comprobado:** `137ff4ed38da65fb3fb61f9804d729a1cee51feb`. El candidato permanece sin commit en `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g04`.

## Cambio

G04 compara la tupla completa de una clave primaria compuesta aunque algunos componentes opcionales estén vacíos o falten sus columnas opcionales. La condición de campo `REQUIRED` procede del contrato G03 congelado y sigue impidiendo evaluar una fila con ese componente vacío o ausente. Las filas que G03 identifica con estructura o tipo inválido siguen fuera de la comparación. El inventario G04 y las implementaciones G05–G07 conservan sus bytes.

Las regresiones detectan duplicados `a,b,,,,` en `transfers.txt` y filas con `record_sub_id` y `field_value` vacíos en `translations.txt`; verifican el localizador de la segunda fila, el orden de los seis componentes y cobertura evaluada mayor que cero. También comprueban `transfers.txt` sin cabeceras opcionales y la exclusión de un componente tipado como inválido por G03. La prueba existente de componentes `REQUIRED` vacíos en `stop_times.txt` sigue pasando.

Durante la revisión dependiente se encontró que un duplicado de secuencia en cualquier forma bloqueaba toda la evaluación de secuencias y distancias de `shapes.txt`. G07 ahora conserva la evaluación de secuencia no negativa y limita la incertidumbre de progresión de distancia a la identidad duplicada; las demás formas siguen evaluándose. La regresión usa una forma duplicada y otra forma con distancias crecientes.

La [referencia GTFS Schedule fijada al 2026-04-27](https://gtfs.org/documentation/schedule/reference/) declara las claves primarias de [transfers.txt](https://gtfs.org/documentation/schedule/reference/#transferstxt) y [translations.txt](https://gtfs.org/documentation/schedule/reference/#translationstxt) con seis componentes.

## Verificación local, 2026-10-01

| Comprobación | Resultado |
| --- | --- |
| `python -m unittest discover -s tests` | 216 tests: 215 OK, 1 SKIP explícito |
| `python -m unittest tests.test_g04_identity tests.test_g05_g07_runtimes` | 50/50 PASS |
| `test_g07_defers_sequence_order_when_g04_finds_duplicate_identity` | PASS; evalúa la secuencia y la otra forma, limita la incertidumbre de distancia al duplicado |
| `python -m compileall -q gtfs_lab tests tools` | PASS |
| `python tools/generate_g04_identity_inventory.py --check` | PASS, regeneración determinista |
| `git diff --check` | PASS; aviso de conversión CRLF/LF en `PROJECT_STATUS.md` |

El SKIP corresponde a la integración condicionada por la base Compliance protegida, ausente en este worktree. El CI remoto no se ha ejecutado. `git diff --check` comprueba los archivos seguidos por Git; los nuevos archivos del candidato siguen sin añadir al índice. No se ha ejecutado HOLDOUT ni se han abierto feeds de operadores.

## SHA-256 del nuevo candidato

Hashes calculados sobre los bytes locales, en hexadecimal mayúsculo. Incluyen el cambio G04 y su regresión, además del ajuste G07 y su regresión; los otros seis artefactos conservan los bytes verificados en la revisión anterior.

| Archivo | SHA-256 |
| --- | --- |
| `gtfs_lab/g04_identity.py` | `C2FF57DB4D1FCFD45269DF5461D7D541B9F853864379FED29BE710F16935B441` |
| `gtfs_lab/g05_temporal.py` | `8B8D5919DA48188E008DA24469128D8B7ABEB5702E0863251DB3DB59150DE00A` |
| `gtfs_lab/g06_operations.py` | `01E7F1B70F2B5AA34F9033DC09572765C5B17CFF22EB82D5AA08FB4014D121EE` |
| `gtfs_lab/g07_spatial.py` | `DB4C427296338A97F786B1BCCBFC355C79F7FD6E9FB98938BF7999D257EB8432` |
| `gtfs_lab/phase_runtime_contract.py` | `DEDA6DA6FB72112A78A19C362E4425614C9FEAC49E210F6446AD7C74FB482714` |
| `gtfs_lab/pipeline.py` | `E855B476C362EBBADA2777B06020B8059EA2FB0657556034FB065D6FE0D22F00` |
| `tests/test_g04_identity.py` | `B3DA1E0D36D4BD277F9BC71E3288A1CD968C9D19C99B91BED022186B3E0B640A` |
| `tests/test_g05_g07_runtimes.py` | `E182FDFCBA270EF8A99ADABBC280953E843290CE4F6885A5E3183AEC2CAD742D` |
| `spec/gtfs_schedule_g04_identity_references_2026_04_27.json` | `1691125CC2DECD90E2A011B2F86EB52512187CD72E60EF534D7E58AFD8CC1165` |
| `.github/workflows/gtfs-engine-preconditions.yml` | `F0BED4F2F2155BBCB4D2AB9C671D86BF45D4748091CDFACE728D4D9C03ACCA0E` |

El [paquete de revisión inicial](TDL_GTFS_AUDIT_ENGINE_G04_G07_LOCAL_REVIEW_20261001.md) conserva los resultados y hashes de la versión anterior. Esta revisión local aprueba el alcance técnico G04–G07 sobre los hashes listados; el cierre, CI remoto y publicación siguen pendientes según el proceso del proyecto.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
