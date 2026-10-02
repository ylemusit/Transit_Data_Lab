# NeTEx N08 — corpus DEVELOPMENT y E2E

El corpus está en `02_Data_Engineering/NeTEx_Lab/tests/fixtures/`, es enteramente sintético y tiene hashes en `corpus_manifest.json`. Incluye XML malformado, raíz XSD inválida, base XSD válida, candidato de referencia sin mapping, candidato de identificador repetido, candidato temporal no evaluado y declaración DTD/entidad rechazada. No incluye feeds públicos, cliente u operador.

El E2E recorre intake → identity → well-formedness → XSD → reglas → findings/evidence → JSON/Markdown report; incluye un ZIP, ejecuta replay del mismo input y compara reportes normalizados byte a byte. Verifica hashes de fixtures antes/después y ausencia de rutas absolutas. Los candidatos de referencias y horario solo prueban que el gap se conserva; no se presentan como reglas implementadas.

`HOLDOUT = NOT_ACCESSED`; feeds públicos autorizados no utilizados; `OPERATOR_SPECIFIC_CODE = NO`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
