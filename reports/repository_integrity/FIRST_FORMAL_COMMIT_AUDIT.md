# Auditoría del primer commit formal — BLOCKED

Fecha: 2026-09-27. PROJECT_CONSOLIDATION = BLOCKED. ROOT_GIT_ALIGNMENT = FAIL (snapshot formal pendiente). FIRST_FORMAL_COMMIT = BLOCKED. LOCAL_BASELINE_TAG = BLOCKED. COMMIT_BLOCKERS = 1.

## Bloqueo y alcance

SECRET_BLOCKER = YES: `07_Business/03_Market/evidence/entur_siri.html`, líneas 1805 y 1806, categoría JWT/credencial de acceso probable. Tokens HS256 con claims de acceso y metadatos Atlassian; cinco ocurrencias en dos líneas. No se muestran valores, no se prueban contra servicios ni se modifica la evidencia. Aunque su vigencia no se valida, son tokens firmados reales, no placeholders descartables. La instrucción del usuario exige STOP antes de staging/commit. Resolución futura trazable, sin regenerar ni sanear silenciosamente evidencia.

No staging, commit, tag, remote, push, copia masiva, borrado, movimiento, investigación o fase nueva. Se termina la documentación segura del bloqueo.

## Estado raíz

- Root: `C:/Users/yeiso/Desktop/Folder/VSCode/Proyectos/Transit Data Lab`.
- Rama: main; commits previos: 0, rama unborn; git log informa que no hay commits.
- Remote: ninguno; REMOTE_BACKUP = NOT_CONFIGURED; configuración no modificada.
- Archivos previamente tracked/staged: 0/0; todos los candidatos son untracked.
- git status --short y git status --ignored --short consultados inicialmente. La segunda consulta expandió backups excluidos, provocó muchos avisos Filename too long y salida truncada. No se certifica un inventario completo de ignorados a partir de esa salida.
- Alternativa usada: git status --ignored=matching --short con pathspec que excluye Products; check-ignore de listas explícitas; inspección superficial de Products/Backups. No se repite el recorrido problemático.

## Repositorios anidados

- `06_Products/GTFS Explorer/GTFS Explorer Artifacts`: independiente, ignorado; marcador .git y toplevel/HEAD/rama comprobados.
- `06_Products/GTFS Explorer/GTFS Explorer Backups/restore_test_v0.2.2_20260924T161533Z_02`: independiente, ignorado; marcador .git y toplevel/HEAD/rama comprobados.
- `06_Products/GTFS Explorer/GTFS Explorer Desktop`: independiente, ignorado; marcador .git y toplevel/HEAD/rama comprobados.
- `06_Products/GTFS Explorer/GTFS Explorer Engineering`: independiente, ignorado; marcador .git y toplevel/HEAD/rama comprobados.

NESTED_REPOSITORIES_PRESERVED = YES. No lectura recursiva de sus árboles ni cambio de refs/configuraciones. Sus HEAD observados son Desktop 38e0e96dbeabaf00d53ed4d85509e5a4ce0b06fd, Engineering efdfe91c2c888bf7e3de6c72a29e4e2ee8f0abbf, Artifacts d49ef160b1e1685c143389f86ecf9643af1f4f03 y restore 85c700587ffec06d73d84825e1951fb73259b62c (detached). El estado detallado de sus worktrees no se recorre ni recertifica. Ningún gitlink previsto.

## Candidatos y ignore

Inventario acotado de metadatos: 1583 entradas, 1045 archivos potenciales visibles con el ignore previo. Tras revisión: 221 excluidos adicionales y 824 candidatos preexistentes (78767345 bytes), más ocho documentos/resultados nuevos = 832 candidatos finales, incluido el HTML bloqueado. Staged = 0. CSV contiene archivos candidatos, exclusiones metadata-only y directorios podados; no enumera los datasets ya ignorados.

.gitignore se amplía, no se sustituye: feeds piloto original/extracted, backups *.duckdb.editor-pre-migration.bak, cuatro clases de generado grande histórico Bizkaibus/scope_before y node_modules/build/dist. Preserva manifests *.manifest.json y evidencia pequeña. Categorías ignoradas: bases/WAL/backups, feeds, cachés/entornos/temp/logs, builds, repos Products y grandes generados seleccionados. No se fuerza ningún archivo ignorado.

## Tamaños y fuentes legales

Umbrales decimales >10.000.000 / >50.000.000 / >100.000.000 bytes (también se conservaron los tamaños exactos). Diez archivos >10 MB en el inventario previo; cuatro >50 MB; uno >100 MB. Tras exclusiones queda un PDF >10 MB; cero candidatos >50 MB o >100 MB.

- 70195962 bytes: `07_Business/03_Market/evidence/scope_before.json`; EXCLUDED_GENERATED
- 31861319 bytes: `03_Compliance/EU/01_Primary_Law/Regulation_2024_1679/Regulation_EU_2024_1679_ES.pdf`; REVIEW_LARGE, PDF jurídico aprobado
- 69265148 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_001/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-312-0a3f43b9.json`; EXCLUDED_GENERATED
- 18390746 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_001/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip`; EXCLUDED_GENERATED
- 103218958 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_001/informe-validacion.html`; EXCLUDED_GENERATED
- 18390746 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip`; EXCLUDED_GENERATED
- 11068499 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/018_bilbobus/02_sources/gtfs_schedule/extracted/stop_times.txt`; EXCLUDED_GENERATED
- 39515161 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/02_sources/gtfs_schedule/extracted/shapes.txt`; EXCLUDED_GENERATED
- 52049844 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/02_sources/gtfs_schedule/extracted/stop_times.txt`; EXCLUDED_GENERATED
- 18245454 bytes: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/02_sources/gtfs_schedule/original/20260910_060014_Euskadi_Bizkaibus.zip`; EXCLUDED_GENERATED

12 PDF Compliance elegibles, 40.436.167 bytes; 0 tracked/staged porque no existe commit y el bloqueo impide staging. Coincide con los 12 documentos aprobados; no forzar conteo, no rehash PDF. Phase 2 registra 10 documentos en base y hashes jurídicos 10/10 PASS: cuenta distinta del corpus físico de 12 PDF, no contradicción. Fuente documental: SOURCE_MANIFEST.txt, PROJECT_CURRENT_STATE.md y PHASE_2_FORMAL_FREEZE.json. Los PDF Business de procurement son otra categoría y no forman parte de esos 12.

## Secretos, rutas y portabilidad

Escaneo dirigido de 767 textos/configs candidatos, 25010134 bytes leídos para esta revisión. Patrones: asignaciones literales de claves/passwords, claves privadas, API/cloud/GitHub tokens, JWT y Authorization Bearer/Basic; no datasets raw, bases, binarios ni generados grandes. No garantiza ausencia de todo secreto; resultado suficiente para bloquear. Hallazgos sin valores en FIRST_FORMAL_COMMIT_FINDINGS.csv.

155 referencias de rutas absolutas antes de clasificación contextual: {'DOCUMENTATION_REFERENCE': 28, 'INTENTIONAL_HISTORICAL_METADATA': 104, 'EXECUTABLE_PORTABILITY_RISK': 23}. Las seis comparaciones SQL de tres local_file históricos se clasifican INTENTIONAL_HISTORICAL_METADATA; no se modifica la base. 23 referencias read_blob absolutas en tres SQL históricos son EXECUTABLE_PORTABILITY_RISK. Se conservan, porque cambiar tests/materialización de un freeze alteraría la reproducibilidad histórica. Un procedimiento futuro de recuperación debe resolverlas explícitamente. No se modifican tests ni evidence por estética.

core.autocrlf = true observado. Antes de cualquier commit futuro, resolver y verificar una política Git de bytes/saltos de línea para textos congelados: un checkout normal puede no reproducir los hashes originales si hay normalización. No se cambia configuración ni se crea una política de atributos durante este bloqueo.

## Consistencia de baseline

BASELINE_CONFLICT = NO. Ninguna baseline se modifica en esta tarea. Contraste de project_baseline.json con PHASE_2_FORMAL_FREEZE.json: GTFS f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc; Phase 1 histórico 52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5; Phase 2 actual 823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3. Bases presentes comprobadas solo por metadata; no nuevo hash DB ni rerun. Congelación confirmada documentalmente desde evidencia persistida, no certificación nueva de todos sus bytes.

Hashes dirigidos de dos documentos raíz coinciden con freeze: project_baseline.json 541b19b2d4b47d9639a346df9531ec163e92c96f2a5f56d7413a07620ffb0da3; PROJECT_CURRENT_STATE.md 1926a19ab7a779fcb4bdb256499a2e703696f92460c458b4f757bc9668141871. Tres documentos integrantes Business V1 coinciden con sus hashes individuales y agregado. No hash recursivo.

Compliance Phase 1/2 FROZEN, Gate 1/2 CLOSED, materialization/freeze/promotion PASS; 92/36/48/10, siete PARTIAL. Business V1 FROZEN y Phase 3 IN_PROGRESS; readiness verification.json PASS con exit_code 0 persistido. MARKET/DEMAND/WTP NO y DIFFERENTIATION UNPROVEN. READY_FOR_CUSTOMER_DISCOVERY YES en el gate previo significa preparado para solicitar autorización del diseño PROB-001. Los registros posteriores BUSINESS_STATUS/STAGE_1_CRITERIA_REEVALUATION conservan Stage 1 INCOMPLETE, S1-EXIT-09 INSUFFICIENT_EVIDENCE y STAGE_1_GATE NOT_REACHED. No se promueve readiness a gate aprobado; READY_TO_CONTINUE_BUSINESS_CUSTOMER_DISCOVERY = NO como autorización operativa actual.

Históricos previos sin Git, sin Business o con Phase 2 pendiente permanecen históricos, no se reescriben como estado actual. Los documentos raíz congelados conservan su momento previo al commit; PROJECT_SNAPSHOT_V0.1 documenta el presente BLOCKED.

## Organización y límites

Siete áreas conceptuales presentes. CORRECTLY_LOCATED: fuentes/scripts/corpus/gobierno; LEGACY_BUT_VALID: auditorías piloto bajo GTFS_Lab. Duplicados históricos ZIP/manifests y main.stops conservados sin nueva comparación. TEMPORARY: ignorados. UNKNOWN: propósito main.stops y replay GIS. Ningún MISPLACED obliga a movimiento. Archivos movidos = 0; eliminados = 0. Ver PROJECT_STRUCTURE.md.

Se mantienen todas las limitaciones: core/validation/analysis pendientes, GIS sin replay integral, fidelidad textual y cumplimiento jurídico no certificados, mapping/audit incompletos, Annex 1.3 B-I/D-I y siete PARTIAL. No market validated, pricing, discovery ni fases nuevas.

## Backup y recursos

PROJECT_BACKUP_POLICY_DOCUMENTED = YES; BACKUP_AND_RECOVERY.md distingue candidatos Git, regenerables, datos que requieren backup separado y repos anidados. Un backup previo de Compliance y checkpoints Products existen por inspección superficial, sin certificar cobertura actual. No backup físico nuevo; no snapshot Git exitoso; un disco local sin remoto/copia independiente sigue expuesto.

RESOURCE_GUARD_TRIGGERED = YES. Repository-wide content hash = NO. Large recursive scan = YES (consulta inicial Git de ignorados recorrió backups excluidos inesperadamente; salida truncada y conteo no medido; vía detenida y no repetida). Después, metadatos con límite 6.000 entradas y escaneo de textos limitado a 10 MB/archivo y 256 MB total; exclusiones podadas. No lectura >5 GB ni hash de árboles. Metadatos dirigidos medidos 1583; textos medidos 767, 25010134 bytes en el scan. Lecturas totales/tiempo total no medidos, no se hace trabajo adicional para medirlos.

## Resultado y reanudación

COMMIT_BLOCKERS = 1: SECRET_BLOCKER. NESTED_REPOSITORY_ABSORPTION_RISK = NO; BASELINE_CONFLICT = NO; DATABASE_ACCIDENTALLY_STAGED = NO; RAW_DATA_ACCIDENTALLY_STAGED = NO; LARGE_GENERATED_FILE_ACCIDENTALLY_STAGED = NO; FROZEN_BASELINE_MODIFIED_UNEXPECTEDLY = NO según comprobaciones dirigidas y alcance de escrituras.

FIRST_FORMAL_COMMIT y LOCAL_BASELINE_TAG BLOCKED; no SHA final ni mensaje aplicado. Mensaje propuesto: Transit Data Lab: establish frozen project baseline. Tag objetivo tdl-baseline-v0.1 no existe y no se crea. No se sobrescribe historia ni tag. No verificación post-commit aplicable.

Working tree: untracked preexistentes de Data Engineering, Compliance, Business y reports, más ocho documentos nuevos y .gitignore ampliado (también untracked, pues la raíz no tenía archivos tracked). Índice vacío. Resolver el HTML con credenciales mediante decisión trazable, revisar política de bytes congelados y repetir preflight acotado antes de staging. No ejecutar discovery.

Archivos creados: REPOSITORY_POLICY.md, PROJECT_STRUCTURE.md, BACKUP_AND_RECOVERY.md, PROJECT_SNAPSHOT_V0.1.md, reports/repository_integrity/FIRST_FORMAL_COMMIT_AUDIT.md, reports/repository_integrity/FIRST_FORMAL_COMMIT_MANIFEST.csv, reports/repository_integrity/FIRST_FORMAL_COMMIT_FINDINGS.csv, reports/repository_integrity/FIRST_FORMAL_COMMIT_VERIFICATION.json. Modificado: .gitignore. Ningún documento autoritativo preexistente se reescribe.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.


## Resolución posterior acotada — Atlassian JWT (2026-09-27)

Esta adenda registra únicamente FIRST FORMAL COMMIT — BLOCKER RESOLUTION 01. El cuerpo anterior y los manifests/JSON/CSV de auditoría conservan su carácter histórico y no se han vuelto a ejecutar ni actualizar.

JWT blocker resolution attempted = YES. Credential type = Atlassian JWT; contexto EMBEDDED_PAGE_RUNTIME_TOKEN; cinco redacciones de un valor distinto en las líneas 1805–1806. Original sensible protegido localmente en `07_Business/03_Market/evidence/.sensitive_local/entur_siri.original.html`: conservado byte a byte, NOT_TRACKED e IGNORED. Evidencia saneada creada/preservada en la ruta canónica `07_Business/03_Market/evidence/entur_siri.html`, NOT_IGNORED. Solo se sustituyeron valores JWT por `[REDACTED_ATLASSIAN_JWT]`.

Registro de procedencia y verificación: `07_Business/03_Market/evidence/ENTUR_SIRI_SANITIZATION_RECORD.md`. La interpretación sustantiva de mercado permanece sin cambios; las imágenes remotas protegidas pueden no cargar. La referencia Business del manifiesto conserva su ruta y las huellas históricas del original; el registro documenta ambas versiones.

JWT_BLOCKER_RESOLUTION = PASS. TARGETED_SECRET_RECHECK = PASS. SECRET_FINDINGS = 0. ATLASSIAN_JWT_FINDINGS_AFTER_SANITIZATION = 0. Se revisaron exclusivamente el HTML saneado, el registro, .gitignore y esta auditoría; el original sensible no es candidato a Git. Sustitución exacta de cinco valores y original idéntico verificados; índice Git sin cambios. El resultado se limita a los patrones de credenciales documentados en el registro.

PROJECT_CONSOLIDATION permanece BLOCKED (no PASS). FIRST_FORMAL_COMMIT = STILL_PENDING. Pendientes: política de preservación de bytes ante core.autocrlf, revisión de rutas absolutas ejecutables y verificación final pre-commit. No autoriza staging, commit, tag, push, Customer Discovery ni ninguna otra fase.

Repository-wide scan performed = NO. Repository-wide hash performed = NO. RESOURCE_GUARD_TRIGGERED = NO en esta resolución; las incidencias de recursos del cuerpo anterior corresponden a la ejecución histórica. No datasets ni bases procesados.

## Resolución posterior acotada — política de bytes Git (2026-09-27)

Esta adenda registra únicamente FIRST FORMAL COMMIT — BLOCKER RESOLUTION 02. El cuerpo anterior, la resolución JWT y los CSV/JSON históricos permanecen como registros de sus ejecuciones; no se regeneran.

LINE_ENDING_REVIEW = PASS. GITATTRIBUTES_POLICY = ESTABLISHED. LINE_ENDING_BLOCKER = NO. `.gitattributes` raíz creado: texto ordinario normalizado a LF, fuentes/evidencia y documentos congelados protegidos por rutas con -text -eol, PDF/imágenes/archivos comprimidos sin conversión textual. Se desactivan filtros, ident y recodificación heredados. core.autocrlf = true, origen file:C:/Program Files/Git/etc/gitconfig; core.eol y core.safecrlf sin configurar. No cambios de configuración global, sistema ni local.

TEMPORARY_INDEX_TEST_PERFORMED = YES: diez muestras, 2.600.693 bytes, índice y objetos temporales fuera del workspace. Incorporación y filtros de checkout comparados byte a byte, incluyendo HTML con saltos mixtos y documentos/CSV/JSON CRLF. BYTE_PRESERVED_EVIDENCE_TRANSFORMED = NO. WORKING_TREE_MODIFIED_BY_TEST = NO. REAL_GIT_INDEX_CHANGED = NO (ausente antes/después, sin entradas). No git add; ningún objeto añadido al almacén raíz. Proceso completo exit_code = 0; temporales eliminados. Atributos efectivos verificados también para los doce PDF jurídicos, sin leerlos ni rehashearlos.

El Entur saneado conserva sus bytes y permanece elegible; el original sensible sigue ignorado/no tracked, sin lectura de contenido ni cambio sustantivo. Registro completo y OID de muestras: `reports/repository_integrity/GIT_LINE_ENDING_POLICY.md`. Cambios limitados a .gitattributes, ese registro, REPOSITORY_POLICY.md y esta adenda.

Repository-wide scan performed = YES en esta resolución: búsqueda inicial recursiva filtrada de nombres con rg --files antes de aplicar la restricción del adjunto. Desviación detectada y no repetida; después solo manifiesto existente y rutas dirigidas, sin escaneo amplio de contenido. Repository-wide hash performed = NO. RESOURCE_GUARD_TRIGGERED = YES (corrección manual de la estrategia, sin exceder límites de la prueba). Este incidente se declara aunque la comprobación técnica de preservación haya pasado.

JWT_BLOCKER_RESOLUTION permanece PASS. PROJECT_CONSOLIDATION permanece BLOCKED, nunca PASS. FIRST_FORMAL_COMMIT = STILL_PENDING. Pendientes: revisión de rutas absolutas ejecutables y verificación final pre-commit acotada. No staging real, commit, tag, push ni otras fases. STOP al terminar esta resolución.


## Resolución posterior acotada — rutas absolutas (2026-09-27)

FIRST FORMAL COMMIT — BLOCKER RESOLUTION 03: ABSOLUTE_PATH_REVIEW = PASS. EXISTING_FINDINGS_RECONSTRUCTED = YES; EXPECTED_FINDINGS = 23; CLASSIFIED_FINDINGS = 23; UNCLASSIFIED_FINDINGS = 0; UNKNOWN = 0; ABSOLUTE_PATH_COMMIT_BLOCKERS = 0.

Conjunto exacto reconstruido de FIRST_FORMAL_COMMIT_FINDINGS.csv sin regenerarlo: 13 FROZEN_EVIDENCE_REFERENCE (10 transacción histórica y 3 gate previo con assertions mutables superadas); 10 EXECUTABLE_PORTABILITY_RISK (gate posterior vigente, read_blob de PDF jurídicos). Las otras cinco clasificaciones tienen conteo 0. Los diez riesgos activos son inputs congelados y requieren futura variante portable separada; conservarlos con limitación explícita establece fielmente la baseline histórica y no bloquea el primer commit. No se afirma portabilidad general ni se ejecutan tests.

Registro y razonamiento: reports/repository_integrity/ABSOLUTE_PATH_REGISTER.csv y ABSOLUTE_PATH_REVIEW.md. Los tres local_file históricos Compliance se preservan; no forman tres filas adicionales del conjunto de 23. DuckDB, corpus y evidencia congelada sin modificaciones. No rutas reescritas, staging, commit, tag ni push. Índice real ausente/sin entradas antes y después; los tres SQL intactos por comparación byte a byte, sin hashes. Solo se crean los dos informes y se añade esta adenda; registros históricos intactos.

Repository-wide search performed = YES: consulta inicial recursiva de nombres rg --files antes de leer las restricciones del adjunto; no contenido, no fallback, no repetición. Repository-wide content search = NO. Repository-wide hash = NO. Recursive dataset traversal = NO. RESOURCE_GUARD_TRIGGERED = YES por esa desviación inicial declarada y corregida.

JWT_BLOCKER_RESOLUTION permanece PASS; LINE_ENDING_REVIEW permanece PASS; GITATTRIBUTES_POLICY permanece ESTABLISHED. PROJECT_CONSOLIDATION permanece BLOCKED. FIRST_FORMAL_COMMIT = STILL_PENDING. Pendiente: verificación final pre-commit acotada. STOP; no correcciones de rutas ni cambios Git autorizados por esta resolución.
