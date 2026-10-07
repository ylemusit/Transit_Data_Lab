# Real Dataset Test Bank V1 — Controlled Intake

Estado: **CLOSED / HUMAN_CLOSURE_APPROVED**, 2026-10-02. El banco antecede al cliente Windows. Alcance ejecutable V1: GTFS Schedule sobre Client Audit Workflow V1; no integra NeTEx ni remediación automática. No cambia reglas, contratos ni baselines cerradas.

## Identidad y almacenamiento

**El nombre del cliente no es el nombre de trabajo. La ruta del cliente no es la ruta de trabajo.** Se captura identidad antes de asignar el código y copiar bytes. SHA-256 identifica contenido; `case_id` identifica una ejecución, sin equivalencia con identidad del dataset. Una repetición del mismo SHA recibe otro código. Rango `00001`–`99999`, sin reciclado; agotarlo bloquea nuevas altas y requiere versionar el contrato.

```text
P:/TransitDataLab/02_Data/TestBank/
├── ACTIVE/00001/             # permanece aquí durante ambos runs
├── OK/00001_OK/              # clasificación solo al finalizar
├── NOT_OK/00002_NOT_OK/
└── REGISTRY/
    ├── RESERVATIONS/00001/   # reserva persistente; no borrar/reutilizar
    ├── TEST_BANK_REGISTER.json
    ├── TEST_BANK_REGISTER.csv
    └── FAILURE_REGISTER.jsonl

Cada caso:
SOURCE/00001.zip              # bytes exactos, atributo read-only
WORKING/a/T/00001/            # workflow inicial, nombres operativos numéricos
WORKING/b/T/00001/            # replay independiente
AUDIT/a_result.json, b_result.json
DELIVERY/workflow/            # entrega V1 original y sus sellos intactos
DELIVERY/<título>_Auditoria_TDL.md
DELIVERY/original_identity.json
DELIVERY/bank_delivery_manifest.json, bank_delivery_seal.json
EVIDENCE/original_identity.json, preflight.json, replay.json
case.json                    # registro autoritativo del caso
```

La ruta absoluta del banco se limita a 64 caracteres; el default es DEFAULT_TEST_BANK_ROOT = P:/TransitDataLab/02_Data/TestBank, con override explícito mediante --bank. No se emplean nombres de operadores en rutas internas. Los run IDs y nombres de artefactos del motor cerrado se conservan. La entrada debe estar fuera del banco. Un banco operativo y sus backups se mantienen fuera del repositorio; Git conserva código y evidencia seleccionada, no ZIP/DB/registro privado. El ejemplo de estructura no exige mover los datasets históricos.

`original_identity.json` conserva filename, extension, path local recibido, tamaño, SHA-256 y fecha de captura. `ORIGINAL_METADATA` mantiene datos declarados de título, publicador, operador, URL, fecha de recuperación y licencia; no se inventan valores ausentes. `FILESYSTEM_METADATA` contiene timestamps observados y su fiabilidad limitada: no se consideran fechas del publicador. Cuando la entrada es una captura anterior, se registra ese papel y se conserva la evidencia previa; no se presenta su ruta como la ruta original de descarga.

La inmutabilidad operacional se comprueba mediante hashes del original y SOURCE antes/después, más atributo read-only en SOURCE. No constituye almacenamiento WORM ni defensa frente a administradores. SHA-256 identifica bytes, no demuestra autenticidad del publicador.

## Contrato de aceptación

`OK` significa procedimiento completo; puede contener `FAIL_TECHNICAL`, revisión humana, `NOT_EVALUABLE`, miles de findings y capacidades diferidas. No acredita calidad total, conformidad jurídica ni aceptación comercial. El estado nativo de auditoría se conserva en `audit_status`.

Todos estos gates deben ser verdaderos:

```text
SOURCE_CAPTURED AND SOURCE_HASHED AND SOURCE_IMMUTABLE
AND PREFLIGHT_COMPLETED AND AUDIT_COMPLETED AND FINDINGS_GENERATED
AND REPORT_GENERATED AND DELIVERY_GENERATED AND REPLAY_COMPLETED
AND EVIDENCE_COMPLETE AND NO_UNRESOLVED_PIPELINE_FAILURE
```

Preflight comprueba ZIP no vacío, CRC, rutas seguras y ausencia de cifrado, sin extraer. El motor sigue siendo autoridad para estructura GTFS, campos y encoding. Cada workflow debe terminar, tener seal y hashes/tamaños correctos, fuente coincidente, evidencia interna, cero errores de pipeline y DuckDB `PASS`. El replay compara bytes de `engine_report.json` y número de findings, con la misma fuente; no afirma igualdad de timestamps, DB ni de todas las salidas de runtime.

`NOT_OK` preserva fuente, evidencia parcial e incidencia normalizada. Una entrada inexistente, extensión incorrecta, metadatos inválidos o configuración bloqueada antes de captura/reserva devuelve `BLOCKED` sin inventar un caso de dataset. No hay reintentos automáticos. Una nueva ejecución obtiene otro case ID; los intentos históricos pueden vincularse con evidencia y estado explícito. Incidencias `OPEN`/`UNDER_INVESTIGATION` impiden `OK`.

## Entrega y privacidad

La entrega añade título y filename originales y referencia `TDL-00001`, conservando la entrega sellada del workflow como subpaquete. La entrega operativa V1 usa Markdown/JSON y los artefactos existentes; PDF y XLSX son formatos de presentación posteriores, no implementados por este módulo. El título del fichero de informe se limita/sanea para Windows. Los metadatos públicos usan una lista limitada de campos y redacción de rutas locales; la ruta original y timestamps de filesystem quedan en evidencia interna. Los registros son locales, no entregables de cliente; su JSON puede incluir rutas y mensajes de error. El CSV neutraliza prefijos de fórmulas, conservando valores exactos en JSON; importar `case_id` como texto para mantener ceros.

## Operación

Desde `02_Data_Engineering/GTFS_Lab`, usando el entorno Python del proyecto:

La ejecución completa requiere **DuckDB CLI en PATH**, no basta con el paquete Python. La comprobación local usó CLI `v1.5.5`. CI instala el [release oficial v1.5.5](https://github.com/duckdb/duckdb/releases/tag/v1.5.5), con SHA-256 del asset Linux verificado frente a metadatos oficiales: `08c0ca117111fcede14239d0093792352befdc174218c344d232c13279643d05`. No se modifica la instalación DuckDB del usuario.

```powershell
python -m gtfs_lab.test_bank 'C:/Descargas/fichero original.zip' --bank P:/TransitDataLab/02_Data/TestBank --metadata metadatos.json --provenance CLIENT_PROVIDED
python -m gtfs_lab.test_bank --bank P:/TransitDataLab/02_Data/TestBank --rebuild
python -m unittest discover -s tests -p test_test_bank.py
python -m tools.test_bank_e2e --evidence P:/TransitDataLab/04_Runtime/Outputs/evidencia-sintetica-nueva.json
```

Campos admitidos en `metadatos.json` (texto o null): `dataset_title`, `publisher`, `operator`, `source_url`, `retrieved_time`, `license_status`, `known_friction`, `prior_case_id`, `metadata_evidence`. Los campos desconocidos se rechazan. `--historical-failures` recibe una lista JSON de incidencias con `phase`, `category`, `observed` y opcionalmente estado, resolución, referencia de evidencia y causa con nivel de confirmación. No se infiere causalidad desde un mensaje de error.

Categorías: INPUT, FILESYSTEM, WINDOWS, ZIP, CSV, ENCODING, DUCKDB, GTFS_ENGINE, COMPLIANCE, REPORTING, DELIVERY, REPLAY, PERFORMANCE, UX, UNKNOWN. Estados: OPEN, UNDER_INVESTIGATION, RESOLVED, ACCEPTED_LIMITATION, NOT_REPRODUCIBLE. ID: `FAIL-<case_id>-<secuencia>`; incluye first/last seen y versión de resolución cuando hay evidencia. No se declara un bug corregido en el motor por resolver una ruta de trabajo.

Los registros JSON/CSV/JSONL son vistas reconstruibles de `case.json`; no se editan directamente. Las escrituras usan reemplazo atómico por archivo. El conjunto de tres vistas no es una transacción única: tras interrupción se usa `--rebuild`. Un lock de creación exclusiva serializa toda la ejecución y evita carreras; si otro proceso lo mantiene, se bloquea sin reservar ID. Tras un crash el lock puede persistir: comprobar PID/proceso antes de retirarlo manualmente. No se elimina automáticamente un lock ajeno. Casos en ACTIVE no se promueven automáticamente, aunque un header diga OK tras una finalización interrumpida. Los IDs reservados nunca se reciclan. Un error de disco o una interrupción abrupta puede requerir recuperación humana de un expediente parcial; no se declara `OK` sin completar la clasificación.

Después de renombrar ACTIVE, las rutas absolutas en resultados/logs internos describen la ubicación observada durante ejecución. Para acceder a artefactos actuales se usa `case_path` más rutas relativas; no se reescriben manifests históricos ni sellos.

## Contratos y aceptación remota

El esquema machine-readable es [test_bank_registry_v1.schema.json](spec/test_bank_registry_v1.schema.json). Los registros mantienen dataset_sha256, original_metadata, tdl_version/tdl_commit, case_result, audit_result, replay_result y finding_count, además de los nombres internos anteriores por compatibilidad. Las incidencias mantienen first_seen_case, last_seen_case y TDL_version. Las vistas se reconstruyen desde los expedientes; las reservas persisten incluso si un expediente se archiva. El lock exclusivo abarca reserva, ejecución, clasificación y reconstrucción; el test con un segundo proceso verifica exclusión real. No hay cola ni procesamiento concurrente.

Las dos incidencias históricas Windows/DuckDB del piloto real permanecen en el expediente local como RESOLVED, con resolución CONTROLLED_SHORT_WORKSPACE y OPERATOR_SPECIFIC = NO. Se descubrieron durante el piloto; no se cuentan como fallos nuevos de la ejecución controlada. La causa técnica exacta sigue sin confirmar. No se publican datos, findings, hashes de fuente ni artefactos del operador.

Pruebas específicas y E2E sintético verifican aceptación con findings, rechazo, reservas sin reciclado, mismo SHA con varios IDs, metadatos, inmutabilidad, replay, clasificación, hashes y sellos después del rename. CI ejecuta estas pruebas y genera evidencia sintética descargable. Aceptación remota PASS: PR #40 MERGED, CI PR 37023905768 y post-merge 37024096727 PASS. Los 18 tests del banco, 3 del workflow y E2E sintético OK/NOT_OK se ejecutaron remotamente. REAL_DATASET_TEST_BANK_V1_TECHNICAL_REVIEW = PASS; estado CLOSED; cierre humano aprobado explícitamente por Yeison el 2026-10-02. Registro: [human_closure_20261002.json](reports/evidence/test_bank_v1/human_closure_20261002.json). Evidencia y límites en PROJECT_STATUS.md.

Límites: GTFS Schedule, CLI técnico, sin NeTEx ni remediación automática; recovery manual tras crash, inmutabilidad por verificación de hash y read-only, replay del informe del motor y conteo de findings. SELF_SERVICE_READINESS = NOT_READY; COMMERCIAL_VALIDATION = NOT_ESTABLISHED; MARKET_VALIDATION = NOT_ESTABLISHED. Windows Self-Service Client V1 es el siguiente bloque seleccionado, aún NOT_STARTED; se aborda como objetivo independiente.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
