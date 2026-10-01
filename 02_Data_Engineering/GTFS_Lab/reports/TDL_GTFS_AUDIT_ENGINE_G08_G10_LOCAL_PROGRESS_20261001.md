# GTFS Audit Engine V1 — G08–G10 estado local

**Base:** `89b199f1ffa114922047113a8460e2933cfa60f8` (`origin/main` verificado antes del worktree).
**Estado:** G08, G09 y G10 implementados y verificados localmente; pendientes CI remoto, merge, verificación post-merge y cierres formales.
**HOLDOUT:** no abierto, leído ni ejecutado.

## G08 — Quality

- Registry tipado G02, versiones semánticas, identidad congelada y allowlist de tres recomendaciones `feed_info.txt`.
- Ejecutado después de G07. G08 escribe `g08.json`, no se añade a `validation` legacy y no amplía el `run_outcome` ni la lista de artefactos de M02.
- Una recomendación no satisfecha conserva status técnico `PASS`, genera finding `INFO / GTFS_RECOMMENDED / RECOMMENDED`, y expone `recommendation_met=false` por separado.
- Ausencia del archivo requiere decisión `NOT_APPLICABLE` de G03; evidencia estructural insuficiente o regla desactivada conserva `NOT_EVALUABLE`.
- 11 tests G08, incluido E2E sintético con recomendaciones no satisfechas y aserciones de frontera M02: PASS.

## G09 — Reporting y evidencia

- `g09_reporting.py` produce `engine_report.json` y `engine_report.md` con resultados G03–G08, findings localizables, identidad/versiones, authority, severity, coverage, estados, gaps, limitaciones, features diferidas y relación observada con legacy.
- Findings de recomendación G08 quedan en `recommendation_findings`, separados de los findings técnicos/de conformidad.
- No se calcula score global. Los estados `NOT_EVALUABLE`, `NOT_APPLICABLE` y `INSPECTION_ERROR`, y la cobertura parcial, se conservan.
- Salida determinista comprobada en dos ejecuciones del mismo fixture. Los informes son artefactos suplementarios y M02 no los registra ni los firma.
- 2 tests G09: PASS.

## G10 — Corpus DEVELOPMENT

`CorpusSplit 1.0.0` y la matriz de lineage pasaron `corpus_split_gate`. Se verificó el SHA-256 de cada fuente DEVELOPMENT antes de ejecutar el pipeline. La ejecución G10 abre únicamente esas fuentes, usa un proceso por dataset y elimina sus outputs transitorios al terminar.

| Medida | Resultado |
|---|---:|
| Fuentes DEVELOPMENT autorizadas | 14 |
| Pipeline completado | 14 |
| Errores de pipeline | 0 |
| Replay de estabilidad (dataset `001`, hash del informe) | PASS |
| HOLDOUT accedido | NO |
| Findings G03–G08 | 4: un finding G03 `agency_url` y tres findings G08 informativos |

Los 14 resultados incluyen estados por etapa y regla, recuentos de findings, coverage disponible, recuentos de inspection errors / NOT_EVALUABLE, tiempos y SHA-256 del reporte machine-readable. La comparación agregada informa 13 datasets G03 `NOT_EVALUABLE`, 1 `FAIL_TECHNICAL`; G04, G05 y G06 quedaron `NOT_EVALUABLE` en los 14 por la evidencia upstream limitada. G07 tuvo 4 `NOT_APPLICABLE` y 10 `NOT_EVALUABLE`. G08 tuvo 7 `PASS` y 7 `NOT_APPLICABLE`.

El único finding G03 está localizado en `010 / agency.txt / agency_url`: `empresarodil.es` no incluye esquema URL. Se conserva como resultado técnico observado; no se cambió la regla ni se introdujo excepción por operador. Este finding no demuestra por sí solo una interpretación jurídica.

El feed DEVELOPMENT `019` necesitó 168,927 s en la ejecución registrada. G03 conserva hasta 1.000 ejemplos de evidencia condicional y registra 1.051.162 evaluaciones completas; G04 limita su cache a dos tablas. Se observó un pico de memoria integrado próximo a 9 GB durante 019. Es un dato de esta máquina, no un requisito mínimo ni una garantía de bajo consumo.

La evidencia reproducible queda en [g10_development_results.json](evidence/g10_development/g10_development_results.json). No se copiaron los ZIP fuente al worktree. Las salidas completas de cada run vivieron en directorios temporales y se descartaron.

## Tests y límites de publicación

- G03: 50/50 PASS; G04: 22/22 PASS; G08: 11/11 PASS; G09: 2/2 PASS; G10: 3/3 PASS.
- El test de contrato G03 comprueba que el sample está limitado y que los recuentos cubren toda la evaluación condicional.
- CI remoto aún no ejecutado en esta rama. No hay merge ni cierres formales G08–G10 todavía.
- No se declara cobertura GTFS completa, cumplimiento jurídico, equivalencia total con legacy, validación comercial, readiness SIRI/NeTEx ni resultados HOLDOUT.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
