# GTFS Audit Engine V1 — paquete local de implementación G05–G07

**Estado:** `READY_FOR_FORMAL_REVIEW`; candidato local, no declara `PASS/CLOSED`.\
**Base / HEAD:** `137ff4ed38da65fb3fb61f9804d729a1cee51feb` (sin commit).\
**Worktree:** `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g04`.\
**Especificación:** GTFS Schedule Reference revisada el 2026-04-27.

## Alcance candidato

- **G05 temporal:** rangos `calendar`/`feed_info`, representación compacta de días semanales más excepciones `1`/`2`, modo dates-only, ventanas y tiempos de servicio superiores a 24:00.
- **G06 operacional:** secuencia `stop_times` no negativa, `headway_secs` positivo, `exact_times=1`, intervalos de frecuencia y ausencia de solapamiento. Los intervalos contiguos están admitidos. La monotonía temporal entre filas queda como revisión TDL, `NOT_EVALUABLE`, porque la referencia fijada no formula esa relación como MUST.
- **G07 espacial:** secuencia no negativa con unicidad delegada a G04, coordenadas WGS84 en sus límites y distancia no negativa/creciente al ordenar por `shape_pt_sequence`. No se calculan distancias geodésicas ni plausibilidad cartográfica; unidades no declaradas no se equiparan.

G05–G07 consumen el estado de inspección G03 y, cuando éste detecta un gap estructural o tipológico en la tabla, devuelven `NOT_EVALUABLE` para no generar conclusiones sobre valores no interpretables. Las fases producen resultados separados en el pipeline, `run.json`, `g05.json`, `g06.json`, `g07.json` e informe técnico. La ruta productiva legacy permanece intacta.

## Verificación local

| Comprobación | Resultado |
| --- | ---: |
| `python -m unittest discover -s tests` | 203 pruebas: 202 PASS, 1 SKIP explícito |
| `python -m unittest discover -s tests -p 'test_g05_g07_runtimes.py'` | 19/19 PASS |
| `python -m py_compile gtfs_lab/g04_identity.py gtfs_lab/g05_temporal.py gtfs_lab/g06_operations.py gtfs_lab/g07_spatial.py gtfs_lab/pipeline.py` | PASS |
| `git diff --check` | PASS |

El SKIP de la suite completa se debe a que no está disponible la DB Compliance protegida. No se leyeron datasets HOLDOUT ni feeds de operador. El workflow CI incluye la batería G05–G07, pero no se ejecutó remotamente al no publicarse el candidato.

## SHA-256 de runtimes

| Archivo | SHA-256 |
| --- | --- |
| `gtfs_lab/phase_runtime_contract.py` | `5624BED33E21B5CB2215B76D5D45E2E827FDC4E3EF93200764426A604B00D6B7` |
| `gtfs_lab/g05_temporal.py` | `6D07CF9B42D1E66A27AD59842AC0C5722EDD6A97D56BB1A5FBEE66F8DD178657` |
| `gtfs_lab/g06_operations.py` | `4C3ADADD12FA30B4EF09345863AFBFEF9D118BCA898C0238F35566C2FC755564` |
| `gtfs_lab/g07_spatial.py` | `B592E979D91D93142C71F77A9B9FE906A48BDB0B85774A569E66D0E8E9780D12` |
| `tests/test_g05_g07_runtimes.py` | `9FEFD124DB724D598277C8311947A5D180274F5C8E0619BA5422B7F448D8FBC3` |

Las fuentes normativas son la [referencia oficial GTFS Schedule](https://gtfs.org/documentation/schedule/reference/), en particular [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt), [frequencies](https://gtfs.org/documentation/schedule/reference/#frequenciestxt) y [shapes](https://gtfs.org/documentation/schedule/reference/#shapestxt), en la revisión fijada arriba.

## Siguiente gate

Revisión formal de G04–G07 sobre la base y bytes indicados; después, actualizar el estado de gates. No se hizo commit, push, PR, merge ni publicación.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
