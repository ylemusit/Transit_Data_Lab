# Gate 2 - comprobación de codificación

DB_ENCODING_OK = YES

CSV_ENCODING_OK = NO (informes de entrada); YES (informes nuevos de resolution).

MARKDOWN_ENCODING_OK = NO (review pack de entrada); YES (informes nuevos de resolution).

ENCODING_REQUIRES_DB_REPAIR = NO

Se inspeccionaron documentos, provisions, candidatos y los 35 source facts mediante salida JSON del CLI DuckDB capturada como bytes y decodificada explícitamente con UTF-8. No se encontró mojibake en la base.

Archivos originales afectados: GATE_2_REVIEW_PACK.csv, GATE_2_REVIEW_PACK.md, GATE_2_TEMPORAL.csv. En CSV la corrupción aparece en deadline_scope; el Markdown también contiene texto temporal afectado. La corrupción está en los contenidos persistidos de los informes, no solo en cómo los muestra la consola.

La transformación reversible de pares Latin-1 mal decodificados se aplica exclusivamente a las copias de presentación. Las entradas históricas se conservan byte a byte. CSV y Markdown de resolución se escriben y releen con UTF-8 explícito; no se usa la salida textual de PowerShell para transportar contenido fuente. No se modifica DuckDB ni el significado de G2-028/G2-029.

| Entrada | SHA-256 |
|---|---|
| GATE_2_ACTORS.csv | 9ba1e205fdba107cdb54c4ac947e1cb33221791a84505d1b419d1b06f1c0998e |
| GATE_2_ATOMICITY.csv | 1b9f615b130bf5afdd8d6c7b1c6032b23d262c6716075f3ad95c94f0e835b307 |
| GATE_2_AUDITABILITY.csv | 33f96185340f08218a5261db33c6a996782db12f891b19622e56626f663d0f2e |
| GATE_2_CONDITIONALITY.csv | af7ef21c20e7ada9a5c4cbf8db8a6847ada89cb78259fc97062322a3f4e24a78 |
| GATE_2_EXCEPTIONS.csv | d4dc5d34afc0b1b6debdf547afa1a4e42953b12029812a7429fed24927fbccfc |
| GATE_2_EXISTING_MATERIALIZATION.csv | 7d2a478456dce7acabb234ab83cfe96f5085845a5c25651f1bbe6f422744c0a9 |
| GATE_2_EXTERNAL_DEPENDENCIES.csv | f6d579dc26046004fe75a95ef23c4c35afc4d5d58f4d333dcd9491a4b114bb58 |
| GATE_2_REVIEW_PACK.csv | 8e658cdf35d550e620d4a1e4629e4896ccb519b4daf0804d22667c33caaade72 |
| GATE_2_REVIEW_PACK.md | 149fbe64524334bd66f35504e7b4ae212d0b1ef4fdad6f1ea7f1e43903a2975f |
| GATE_2_SOURCE_FIDELITY.csv | 38369297df643d3e16de8f5b72e2e27c0b7e9f7728611c75c9f234983214615e |
| GATE_2_TEMPORAL.csv | 717d6207c3e4c65377b6ff70cfe720bc1481e727f8cd75c08089ee2f729c0464 |
| HUMAN_REVIEW_GATE_2_SUMMARY.md | 45a7d1d60b97221f53e24875cc71a84e8ed46d68ff7f6b5f1c3eba3059834885 |
| project_baseline.json | b8407edbf637071a6d9f64aab29fd5a096dab7b845c3f16345e288dddf1ca0b8 |

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
