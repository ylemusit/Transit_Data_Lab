# GTFS Audit Engine V1 — paquete local G04–G07

**Estado:** `READY_FOR_FORMAL_REVIEW`; candidato local, sin `PASS/CLOSED`.
**Base / HEAD:** `137ff4ed38da65fb3fb61f9804d729a1cee51feb` (HEAD permanece en la base; sin commit).
**Worktree:** `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g04`.
**Especificación fijada:** GTFS Schedule Reference, revisión 2026-04-27.

## Resultado

El pipeline ejecuta las fases G04–G07 en secuencia y conserva un resultado por fase en el informe y en `run.json`, `g04.json`, `g05.json`, `g06.json` y `g07.json`. Las fases consumen la evidencia previa de G02/G03 y mantienen separados los hallazgos técnicos, la cobertura incompleta y los elementos diferidos de revisión TDL. La ruta legacy no se sustituye.

- **G04 identidad y referencias:** unicidad de claves primarias declaradas, referencias físicas pobladas, dominio lógico `SERVICE_ID` y referencias contextuales de `translations.txt`. El inventario determinista incluye candidatos `UNIQUE_ID`/`FOREIGN_ID`, claves, referencias y políticas contextuales. Targets o condiciones deferred permanecen fuera de evaluación.
- **G05 temporal:** rangos de `calendar`/`feed_info`, orden intrarregistro de tiempos de `frequencies.txt` y conjuntos de fechas representados como periodos semanales compactos más excepciones `calendar_dates` tipo 1/2. Admite horas de servicio superiores a 24:00. El orden de ventanas de recogida/devolución queda `TDL_QUALITY / NOT_EVALUABLE` por falta de una comparación MUST explícita.
- **G06 operacional:** secuencia no negativa de `stop_times`, `headway_secs` positivo, condición `exact_times=1` y no solapamiento de intervalos de frecuencia; límites contiguos se admiten. Cuando G05 ya identifica un rango inválido, G06 lo deja `NOT_EVALUABLE` para no duplicar el hallazgo. Los intervalos de longitud cero con `exact_times` vacío/0 quedan como revisión TDL `NOT_EVALUABLE`; con `exact_times=1` fallan la condición normativa sobre end_time. La monotonía temporal entre filas también queda en revisión TDL porque la referencia no establece un MUST explícito.
- **G07 espacial:** coordenadas dentro de límites WGS84 inclusivos; secuencia `shape_pt_sequence` no negativa con unicidad en G04; distancia finita, no negativa y creciente después de ordenar por secuencia. No se infieren unidades, distancia geodésica ni plausibilidad cartográfica.
- **Integridad de salida G05:** si falla la cobertura del conjunto de fechas por una fila no interpretable, no se expone una materialización parcial como si fuera un calendario completo; la regresión cubre este caso.

Cuando G03 declara estructura o tipos incompletos, las fases afectadas limitan su conclusión a `NOT_EVALUABLE`. Identidades duplicadas de G04 también bloquean los chequeos de orden dependientes en G07. No se procesaron HOLDOUT ni feeds de operadores.

## Verificación local, 2026-10-01

| Comprobación | Resultado |
| --- | ---: |
| `python -m unittest discover -s tests` | 213 tests: 212 OK, 1 SKIP explícito |
| `python -m unittest tests.test_g05_g07_runtimes tests.test_g04_identity` | 47/47 PASS |
| `python -m compileall -q gtfs_lab tests tools` | PASS |
| `python tools/generate_g04_identity_inventory.py --check` | PASS, regeneración determinista |
| `python tools/compliance_portable_gate.py --legal-root . --sources-only` | PASS, fuentes portables disponibles; no es un gate de cumplimiento legal |
| `python -m gtfs_lab.trust_gate` | PASS, 12/12 |
| `python -m gtfs_lab.golden_contract_gate` | PASS, 18/18 |
| `python -m gtfs_lab.golden_corpus_gate` | PASS, 2 casos aprobados; gate de contrato/hashes, no ejecuta el corpus |
| `python -m gtfs_lab.golden_evaluator_gate` | PASS, 11/11 |
| `python -m gtfs_lab.corpus_split_gate --inventory corpus/inventory_v1.json --split corpus/split_v1.json --lineage-review corpus/lineage_review_m04a2.json` | PASS sobre metadatos congelados; no abre ZIPs ni ejecuta datasets |
| `python -m gtfs_lab.corpus_split_gate --lineage-review corpus/lineage_review_m04a2.json --lineage-review-only` | PASS sobre la matriz de lineage; no abre datasets |
| `git diff --check` | PASS; Git emitió aviso de conversión CRLF/LF en `PROJECT_STATUS.md`, sin líneas de whitespace señaladas |

El único SKIP de la suite completa corresponde a la comprobación condicionada por la base Compliance protegida, ausente en este worktree. El CI remoto no se ejecutó porque el candidato no se publicó. No se hizo commit, push, PR, merge ni publicación. La aprobación formal humana sigue pendiente.

## Identidad de los bytes revisados

SHA-256 de los principales artefactos locales (hexadecimal mayúsculo):

| Archivo | SHA-256 |
| --- | --- |
| `gtfs_lab/g04_identity.py` | `0ADEE68DDD1150C2D64B4F387E9C3A62443905BD93BF96B2C8C7519C90903952` |
| `gtfs_lab/g05_temporal.py` | `8B8D5919DA48188E008DA24469128D8B7ABEB5702E0863251DB3DB59150DE00A` |
| `gtfs_lab/g06_operations.py` | `01E7F1B70F2B5AA34F9033DC09572765C5B17CFF22EB82D5AA08FB4014D121EE` |
| `gtfs_lab/g07_spatial.py` | `93C0DFDCCDEE65FC739E60095760FC6DC0CC7666052E6B2E111F76E7E4CB737F` |
| `gtfs_lab/phase_runtime_contract.py` | `DEDA6DA6FB72112A78A19C362E4425614C9FEAC49E210F6446AD7C74FB482714` |
| `gtfs_lab/pipeline.py` | `E855B476C362EBBADA2777B06020B8059EA2FB0657556034FB065D6FE0D22F00` |
| `tests/test_g04_identity.py` | `7941B264AAC628A4F96E87D0F85E12CE2C2DEA0C76E475977AEDA45A336B6E14` |
| `tests/test_g05_g07_runtimes.py` | `BEBFDCEEE4AED5334673C0DDCF1CE030807286A2E0EBB1C626B53F021C01AF3D` |
| `spec/gtfs_schedule_g04_identity_references_2026_04_27.json` | `1691125CC2DECD90E2A011B2F86EB52512187CD72E60EF534D7E58AFD8CC1165` |
| `.github/workflows/gtfs-engine-preconditions.yml` | `F0BED4F2F2155BBCB4D2AB9C671D86BF45D4748091CDFACE728D4D9C03ACCA0E` |

Fuentes normativas fijadas: [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/), [calendar](https://gtfs.org/documentation/schedule/reference/#calendartxt), [calendar_dates](https://gtfs.org/documentation/schedule/reference/#calendar_datestxt), [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt), [frequencies](https://gtfs.org/documentation/schedule/reference/#frequenciestxt) y [shapes](https://gtfs.org/documentation/schedule/reference/#shapestxt).

## Gate pendiente

Revisión formal humana de este candidato sobre la base y los hashes indicados. Después de esa decisión se actualizarán los estados por fase. Este paquete no acredita cumplimiento normativo completo, cumplimiento jurídico ni validación comercial.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
