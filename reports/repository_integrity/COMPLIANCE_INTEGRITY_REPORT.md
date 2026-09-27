# Compliance Integrity Report

Fecha: 2026-09-27. Resultado: **PASS WITH WARNINGS** para integridad estructural Phase 1.

## Base y catálogo

- Base: `03_Compliance/databases/transit_compliance.duckdb`.
- SHA-256: `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`.
- Esquemas presentes: `source`, `compliance`, `mapping`, `audit`, `analysis`.
- Existen las tablas `source.documents`, `source.provisions`, `source.relationships`, las tres tablas compliance, las dos mapping, las cuatro audit y cinco vistas analysis esperadas.

## Phase 1

- Master Phase 1: **24/24 PASS**.
- `PHASE_1_CORPUS_INTEGRITY`: **PASS**.
- Master 2017/1926: **21/21 PASS**.
- `EU_2017_1926_MASTER_STRUCTURE_INTEGRITY`: **PASS**.
- Documentos: 10/10 presentes.
- URLs oficiales no vacías: 10/10.
- Ficheros locales presentes: 10/10.
- SHA-256 recalculado igual al almacenado: 10/10.
- Relaciones esperadas: 6/6.

## 2017/1926

| Tipo | Real |
|---|---:|
| TOTAL | 92 |
| ARTICLE | 11 |
| ANNEX | 1 |
| ANNEX_SECTION | 2 |
| ANNEX_LEVEL | 7 |
| ANNEX_GROUP | 14 |
| DATA_ELEMENT | 57 |

Los siete niveles presentan exactamente las cardinalidades congeladas: 1.1 = 24/4/20, 1.2 = 14/3/11, 1.3 = 14/4/10, 1.4 = 12/2/10, 2.1 = 3/0/3, 2.2 = 4/1/3 y 2.3 = 0/0/0.

## Sentinel Phase 2

`compliance.requirements = 0`, `mapping.format_coverage = 0` y `audit.rules = 0`. Phase 2 no ha comenzado. También están vacías las demás tablas derivadas y de ejecución observadas.

## Anomalía conocida

Continúan presentes `EU-2017-1926-ANNEX-1.3-B-I` y `EU-2017-1926-ANNEX-1.3-D-I`. Sus `source_reference` apuntan al apartado padre, lo que mantiene visible la posible numeración sintética. No se modificó.

## Límites y advertencias

- El PASS certifica estructura, no fidelidad textual, interpretación ni cumplimiento legal.
- Tres `source.documents.local_file` son rutas absolutas. Existen y sus hashes pasan hoy, pero son no portables.
- Los scripts de setup/cierre/carga usan el root absoluto actual. Funcionan en esta ubicación, pero no son relocatables.
- Obligación legal, requisito NAP, especificación de formato y regla de calidad permanecen conceptualmente separados.

---

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

