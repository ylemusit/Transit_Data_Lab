# Transit Data Lab — matriz de validación V1

**Fecha:** 2026-10-07 · **Checkout:** `f8befd4fdc980782ddb75b6ae7dd552f7bfb0436` al inicio. Las duraciones no registradas por la herramienta se indican como `n/d`; no se estiman.

## Suites y gates ejecutados

| Suite / gate | Total | PASS | FAIL | SKIP | Duración | Resultado y notas |
|---|---:|---:|---:|---:|---:|---|
| GTFS Lab `unittest discover -s tests -v` | 320 | 318 | 0 | 2 | 12,295 s | PASS; incluye intake, app, workflow, reportes, transición Compliance, Remediation, Interpretation, Test Bank y paths. |
| NeTEx Lab | 10 | 10 | 0 | 0 | n/d | PASS dentro del alcance V1 y XSD/dependencias fijados. No equivale a certificación nacional. |
| Trust persistence gate | gate | — | — | — | n/d | PASS; evidencias en `04_Runtime/Outputs/project_health_review_v1/trust_persistence_gate`. |
| Golden corpus gate | 2 casos | 2 | 0 | 0 | n/d | PASS. |
| Golden regression gate | 2 casos + mutaciones negativas | PASS | 0 | 0 | n/d | PASS; incluidas comprobaciones negativas intencionadas. |
| Test Bank E2E sintético | 2 casos | 2 | 0 | 0 | n/d | PASS; 1 sintético OK y 1 ZIP malformado NOT_OK; hashes/seals y fuente inmutable. |
| Client Workflow E2E sintético | 3 runs | 3 | 0 | 0 | n/d | PASS; dos runs y comparación parcial del tercero; PDF/MD/JSON, accounting gap 0, manifest/seal. |
| Prueba controlada de producto sintética | 1 flujo + replay | PASS | 0 | 0 | n/d | PASS_WITH_LIMITATIONS; 37 artefactos, GeoJSON/KML, reportes, replay del engine idéntico, fuente inmutable, gap 0. |
| `git fsck --full --no-reflogs --no-dangling` | 5 repos | 5 | 0 | 0 | n/d | PASS, salida 0 y sin diagnósticos: TDL, Artifacts, Desktop, Engineering y restore histórico. |
| Contratos de hash de corpus | 13 ZIP Development | 13 | 0 | 0 | n/d | PASS; `dataset019` deliberadamente no abierto/hasheado; HOLDOUT excluido. |
| Integridad de junctions | 34 | 34 | 0 | 0 | n/d | PASS: destinos presentes, sin extras, faltantes ni errores de acceso. |
| DB GTFS / Compliance | 2 DB | 2 | 0 | 0 | n/d | PASS; lectura DuckDB read-only y SHA esperados concordantes. |
| EXE cliente aceptado | 1 | 1 | 0 | 0 | n/d | PASS: SHA-256 esperado concordante. |
| Secret scan dirigido | 5 repos | 0 candidatos | 0 | — | n/d | PASS limitado a patrones conocidos y estado de trabajo; no es revisión integral del historial. |

## Cobertura y comprobaciones no ejecutadas

- La suite integrada del repo independiente GTFS Explorer Desktop no se ejecutó. Su instrucción local requiere descriptor de fase; no estaba presente. No se modificó su baseline ni se ejecutó build/distribución.
- No se repitió aceptación manual GUI ni clean-machine W08. El hash del EXE sí se comprobó.
- `pytest` no está instalado en el runtime; la suite actual de GTFS Lab se ejecutó con `unittest` (318 PASS, 2 SKIP).
- No se ejecutaron SQLs históricos cuyo conteo de cobertura espera 8 filas contra la DB actual de 10. Se usó el gate portable actual y tests de transición.
- No se abrió ni hasheó HOLDOUT, `dataset019`, PFX ni contenido privado. No se ejecutaron campañas históricas completas ni pruebas de rendimiento extremo.
- No existe backup externo integral ni se hizo restauración en un destino independiente; por ello la recuperabilidad no se considera PASS.

## Resultado de gates

| Gate | Resultado | Evidencia / límite |
|---|---|---|
| Integridad del proyecto | **PASS_WITH_LIMITATIONS** | Rutas activas, refs, DBs y manifests comprobados; excepciones locales de repos de producto descritas en el informe. HOLDOUT permanece en límite metadata-only. |
| Validación técnica | **PASS_WITH_LIMITATIONS** | Suites y gates corrientes de TDL/NeTEx pasan; dos skips de GTFS Lab, Desktop integrada no ejecutada. |
| Ejecución P-only | **PASS** | Flujo sintético inicia y escribe bajo P:; Python base y Node/npm son instalaciones de Windows en C:, limitando portabilidad a máquina limpia. |
| Prueba controlada | **PASS_WITH_LIMITATIONS** | Sintética solamente, sin clientes/HOLDOUT/upload; publicación correctamente no concluyente. |

Los resultados prueban las suites y fixtures enumerados, no certificación legal, aceptación NAP, cobertura GTFS completa, desempeño sobre feeds extremos ni readiness comercial.
