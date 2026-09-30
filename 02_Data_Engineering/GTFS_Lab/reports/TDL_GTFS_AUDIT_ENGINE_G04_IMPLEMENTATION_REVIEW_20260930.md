# GTFS Audit Engine V1 — paquete de revisión de implementación G04

**Estado:** `READY_FOR_FORMAL_REVIEW`; las fases G05–G07 locales ya consumen las salidas G04/G03.\
**Gate:** G04 sigue `IN_PROGRESS`; este paquete no declara `PASS` ni `CLOSED`.\
**Base:** `137ff4ed38da65fb3fb61f9804d729a1cee51feb`\
**Worktree:** `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g04`\
**Rama:** `feat/gtfs-engine-g04-identity-referential`

`HEAD` permanece en la base indicada; el candidato se encuentra en cambios locales sin commit. No existe una rama G04 publicada en `origin` en la última comprobación de sólo lectura. Los hashes de los principales bytes revisados son:

| Archivo | SHA-256 |
| --- | --- |
| `gtfs_lab/g04_identity.py` | `ADBADA64E19385370C265C89EF4537827DB96BE0983F7138D293A1859940479C` |
| `gtfs_lab/pipeline.py` | `E855B476C362EBBADA2777B06020B8059EA2FB0657556034FB065D6FE0D22F00` |
| `spec/gtfs_schedule_g04_identity_references_2026_04_27.json` | `1691125CC2DECD90E2A011B2F86EB52512187CD72E60EF534D7E58AFD8CC1165` |
| `tests/test_g04_identity.py` | `3D07AEDA8DAB0CEB2F462E7A2BB6A9EE2591AA958ECA982A1C133A689796FAAA` |
| `tools/generate_g04_identity_inventory.py` | `1DF842A8F2CA460EC9E354EEC2305DF1D7F94638D3CDA585F118CBE5ED4ABBC3` |
| `.github/workflows/gtfs-engine-preconditions.yml` | `F0BED4F2F2155BBCB4D2AB9C671D86BF45D4748091CDFACE728D4D9C03ACCA0E` |

## Resultado implementado

El candidato implementa cuatro familias de reglas G04 de forma aditiva: unicidad de claves primarias explícitas simples y compuestas, existencia de referencias pobladas, resolución del dominio lógico `SERVICE_ID` y referencias contextuales de `translations.txt`. Reutiliza el inventario determinista y los status/coberturas de G02. La validación legacy sigue ejecutándose y la comparación informa solapamiento, sin afirmar equivalencia.

El inventario conserva 31 candidatos de campo (7 `UNIQUE_ID`, 24 `FOREIGN_ID`), 13 claves primarias explícitas, 20 referencias ordinarias y 17 políticas contextuales. La referencia condicional `calendar_dates.service_id → calendar.service_id` se evalúa además cuando coexisten ambos archivos; en modalidad dates-only los valores de `calendar_dates.service_id` establecen el dominio. Los targets deferred y selectors unresolved permanecen fuera de evaluación; no se les atribuyen fallos al operador.

## Verificación local

| Comprobación | Resultado |
| --- | ---: |
| `python -m unittest discover -s tests -p 'test_g04_identity.py'` | 18/18 PASS |
| `python -m unittest discover -s tests -p 'test_g05_g07_runtimes.py'` | 21/21 PASS |
| `python -m unittest discover -s tests -p 'test_g03_*.py'` | 49/49 PASS |
| `python -m unittest discover -s tests -p 'test_g02_rule_registry.py'` | 10/10 PASS |
| `python -m unittest discover -s tests -p 'test_engine_preconditions.py'` | 10/10 PASS |
| `python -m unittest discover -s tests -p 'test_audit_comparison.py'` | 23/23 PASS |
| `python -m unittest discover -s tests -p 'test_change_attribution_contract.py'` | 16/16 PASS |
| `python -m unittest discover -s tests -p 'test_m05c_historical_proof.py'` | 6/6 PASS |
| `python tools/generate_g04_identity_inventory.py --check` | PASS; regeneración determinista |
| `python -m py_compile gtfs_lab/g04_identity.py gtfs_lab/pipeline.py tools/generate_g04_identity_inventory.py` | PASS |
| `git diff --check` | PASS |

La batería completa GTFS_Lab ejecutó 205 pruebas: 204 PASS y un SKIP explícito por faltar la base Compliance protegida. Se añadieron las baterías G04 y G05–G07 al workflow sintético `.github/workflows/gtfs-engine-preconditions.yml`; no se ha ejecutado CI remoto porque el candidato no se ha publicado.

## Hallazgo de revisión incorporado

La revisión comparó el comportamiento del dominio `SERVICE_ID` con la referencia fijada: cuando están presentes `calendar.txt` y `calendar_dates.txt`, el segundo archivo usa `service_id` como referencia a `calendar.service_id`; cuando sólo está `calendar_dates.txt`, `service_id` declara identidades. El runtime ahora evalúa ambos caminos y localiza la fila huérfana. La regresión cubre mismatch, match y modalidad dates-only. Fuente oficial: [GTFS Schedule Reference, revisión 2026-04-27, calendar_dates.txt](https://gtfs.org/documentation/schedule/reference/#calendar_datestxt).

## Límites preservados

- No se modifican el contrato G03, la especificación GTFS fijada ni la validación legacy.
- No se accedió a HOLDOUT ni a datasets de operadores para esta verificación.
- No se declara equivalencia de findings con legacy ni cumplimiento jurídico.
- Los casos de `locations.geojson`, Flex y tablas deferred continúan `NOT_EVALUABLE` o fuera del catálogo CSV según el alcance.
- Los candidatos G05–G07 se implementaron en el mismo worktree y están documentados en sus alcances; los cuatro permanecen a la espera de revisión formal y no se declaran `PASS/CLOSED`.
- No se hizo commit, push, PR, merge ni publicación.

## Siguiente gate

Revisión formal de los candidatos G04–G07 sobre esta base y paquetes; después, actualizar los gates por fase. Si aparecen hallazgos, corregirlos en el worktree dedicado y repetir las regresiones afectadas antes de presentar una versión nueva.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
