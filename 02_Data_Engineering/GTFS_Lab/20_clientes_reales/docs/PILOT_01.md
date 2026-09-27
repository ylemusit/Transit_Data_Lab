# GTFS Explorer — Spain Mobility Data Benchmark 2026

## Pilot Audit 01

Objetivo: comparar la información declarada/observada en NAP con el GTFS físico y, posteriormente, con los resultados de GTFS Explorer Desktop 0.2.1. En una fase posterior podrán separarse las capas Audit / Quality / Regulatory.

La hipótesis de investigación es que un GTFS aceptado por el NAP puede todavía contener hallazgos técnicos, de calidad o de cobertura relevantes que no sean visibles en la validación superficial publicada. Esta frase es una hipótesis, no una conclusión.

Este piloto se limita a baseline NAP, identidad de fuentes, censo físico y métricas objetivas. No realiza auditoría jurídica, compliance scoring, risk scoring, correcciones de feeds ni parsing GTFS-RT/SIRI/NeTEx.

Siguiente paso recomendado: ejecutar GTFS Explorer Desktop 0.2.1 contra los cinco feeds y almacenar sus resultados en `03_gtfs_explorer/`.
