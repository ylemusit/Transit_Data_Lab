# Política Git de saltos de línea y preservación de bytes

Fecha UTC de verificación: 2026-09-27T03:32:58.655991+00:00. FIRST FORMAL COMMIT — BLOCKER RESOLUTION 02.

LINE_ENDING_REVIEW = PASS. GITATTRIBUTES_POLICY = ESTABLISHED. BYTE_PRESERVED_EVIDENCE_TRANSFORMED = NO en la muestra comprobada. Este resultado resuelve exclusivamente el bloqueo de conversión Git; PROJECT_CONSOLIDATION permanece BLOCKED y FIRST_FORMAL_COMMIT = STILL_PENDING.

## Configuración observada

| Clave | Valor efectivo | Origen | Exit code de consulta |
|---|---|---|---|
| core.autocrlf | true | `file:C:/Program Files/Git/etc/gitconfig` (sistema) | 0 |
| core.eol | UNSET | Ningún valor configurado | 1 |
| core.safecrlf | UNSET | Ningún valor configurado | 1 |

No se modifica configuración global, de sistema ni local. El exit code 1 de las dos últimas consultas significa clave no configurada. `.gitattributes` raíz no existía; se crea. No se localizaron otros `.gitattributes` en los ancestros derivados del manifiesto ni `.git/info/attributes`; las comprobaciones efectivas siguientes incluyen cualquier atributo externo aplicable. Los filtros LFS están configurados en Git, pero no se aplican a las muestras; la política raíz desactiva filtros, ident y recodificación heredados para estos candidatos.

## Clasificación y política adoptada

La única fuente para clasificar candidatos es FIRST_FORMAL_COMMIT_MANIFEST.csv: 1081 filas, 832 candidatos git_eligible=YES. Sus clasificaciones NORMAL/REVIEW_LARGE describen elegibilidad/tamaño y no garantizan que un archivo pueda normalizarse. No se regenera ni actualiza ese manifiesto histórico.

- NORMAL_TEXT: código y documentación ordinarios; `text eol=lf` explícito para Markdown, Python, PowerShell, SQL, CSV, JSON, YAML, TXT, SHA256 y canvas; `.gitignore` y `.gitattributes` también. El resto usa `text=auto eol=lf`, con detección de texto. Git normaliza texto al incorporarlo y entrega LF en checkout, independientemente de core.autocrlf. No se exige igualdad CRLF byte a byte a textos ordinarios.
- BYTE_PRESERVED_EVIDENCE: `-text -eol`, conservando CRLF, LF o mezclas. Se aplica por rutas a NAP, XML jurídico de Spain, `_Sources`, informes históricos de Compliance, evidencia de mercado, ejecuciones de review Business, snapshots NAP y ejecuciones GTFS Explorer de pilotos, manifests de fuentes elegibles y KML existentes. Los scripts incluidos dentro de ejecuciones/reportes históricos conservan bytes como parte de ese contexto de evidencia; los scripts fuente ordinarios siguen LF.
- Excepciones congeladas explícitas: `PROJECT_CURRENT_STATE.md`, `project_baseline.json` y los tres integrantes Business V1 `CAPABILITY_REGISTER.md`, `EVIDENCE_INDEX.md`, `CAPABILITY_GAPS.md`. La gobernanza y auditoría vigentes registran conservación byte a byte/huellas. Los registros históricos `reports/repository_integrity/phase_1_5/**` se protegen por ruta. No se desactiva normalización para todo el repositorio ni se generan excepciones individuales masivas.
- BINARY: PDF, PNG/JPEG/GIF/WebP/ICO y archivos ZIP/7z/gzip/bzip2/xz/tar usan `-text -eol -diff -merge`; estas reglas aparecen después de las rutas de evidencia. Los 12 PDF jurídicos aprobados y los PDF Business quedan sin conversión de texto; ninguno se lee, modifica o rehashea.
- Todos los candidatos heredan `-filter -ident -working-tree-encoding`, evitando transformaciones de contenido adicionales en incorporación/checkout. No hay reglas LFS que conservar en los atributos observados.
- GENERATED/IGNORED: bases, feeds, entornos, generados grandes y repositorios producto siguen fuera del índice raíz por `.gitignore`; un atributo nunca habilita seguimiento ni sustituye exclusiones. No se procesan sus contenidos.

## Entur y original sensible

El HTML saneado canónico `07_Business/03_Market/evidence/entur_siri.html` permanece elegible y tiene `text=unset`, `eol=unset`, `filter=unset`, `ident=unset`, `working-tree-encoding=unset`. No se modifica su contenido.

`07_Business/03_Market/evidence/.sensitive_local/entur_siri.original.html` sigue IGNORED y NOT_TRACKED, comprobado mediante check-ignore y ls-files dirigidos. Se conserva tamaño/mtime antes y después sin leer su contenido. Regla efectiva:

`.gitignore:55:/07_Business/03_Market/evidence/.sensitive_local/ → 07_Business/03_Market/evidence/.sensitive_local/entur_siri.original.html`

El manifiesto anterior conserva el tamaño histórico de Entur; la muestra usa el HTML saneado actual (1.675.049 bytes). No se restaura el original ni se reescriben huellas históricas.

## Atributos efectivos

`git check-attr -z text eol diff merge filter ident working-tree-encoding --stdin`, con lista explícita de representantes y los doce PDF; proceso exit code 0.

`unset` corresponde a atributo negado (`-text`, `-eol`, etc.); `unspecified` significa que no se ha asignado valor. En todas las filas filter, ident y working-tree-encoding = unset.

| Ruta | text | eol | diff | merge |
|---|---|---|---|---|
| `REPOSITORY_POLICY.md` | set | lf | unspecified | unspecified |
| `02_Data_Engineering/GTFS_Lab/sql/01_import/run_import_consorcio_asturias.ps1` | set | lf | unspecified | unspecified |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/tools/audit_gtfs_explorer_pilot_01.py` | set | lf | unspecified | unspecified |
| `reports/repository_integrity/FIRST_FORMAL_COMMIT_MANIFEST.csv` | set | lf | unspecified | unspecified |
| `reports/repository_integrity/FIRST_FORMAL_COMMIT_VERIFICATION.json` | set | lf | unspecified | unspecified |
| `07_Business/03_Market/evidence/entur_siri.html` | unset | unset | unspecified | unspecified |
| `03_Compliance/Spain/01_Primary_Law/Ley_9_2025/Ley_9_2025_ORIGINAL_BOE.xml` | unset | unset | unspecified | unspecified |
| `03_Compliance/NAP/01_Policies/NAP_Licencia_Datos.html` | unset | unset | unspecified | unspecified |
| `PROJECT_CURRENT_STATE.md` | unset | unset | unspecified | unspecified |
| `project_baseline.json` | unset | unset | unspecified | unspecified |
| `03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_REQUIREMENTS.csv` | unset | unset | unspecified | unspecified |
| `03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.json` | unset | unset | unspecified | unspecified |
| `07_Business/02_Capabilities/CAPABILITY_REGISTER.md` | unset | unset | unspecified | unspecified |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/informe-validacion.html` | unset | unset | unspecified | unspecified |
| `02_Data_Engineering/GTFS_Lab/exports/route_440.kml` | unset | unset | unspecified | unspecified |
| `03_Compliance/EU/01_Primary_Law/Directive_2010_40_EU/Directive_2010_40_EU_CONSOLIDATED_2023-12-20_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Directive_2023_2661/Directive_EU_2023_2661_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Historical/Regulation_1305_2014/Regulation_1305_2014_CONSOLIDATED_2021-04-18_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Historical/Regulation_454_2011/Regulation_454_2011_CONSOLIDATED_2019-06-16_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Regulation_2017_1926/Regulation_2017_1926_CONSOLIDATED_2024-03-04_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Regulation_2017_1926/Regulation_2017_1926_ORIGINAL_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Regulation_2024_1679/Regulation_EU_2024_1679_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Regulation_2024_490/Regulation_2024_490_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Regulation_2026_1554/Implementing_Regulation_EU_2026_1554_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/EU/01_Primary_Law/Regulation_2026_253/Implementing_Regulation_EU_2026_253_ES.pdf` | unset | unset | unset | unset |
| `03_Compliance/Spain/01_Primary_Law/Ley_9_2025/Ley_9_2025_CONSOLIDATED_2026-03-21.pdf` | unset | unset | unset | unset |
| `03_Compliance/Spain/01_Primary_Law/Ley_9_2025/Ley_9_2025_ORIGINAL_BOE.pdf` | unset | unset | unset | unset |

## Prueba aislada de preservación

TEMPORARY_INDEX_TEST_PERFORMED = YES. Diez muestras, 2600693 bytes (aprox. 2,60 MB). Límites preventivos: <10 MB por muestra y <16 MB agregados. Todas pertenecen al manifiesto elegible; no se prueban recursivamente los candidatos.

Un directorio creado con tempfile.TemporaryDirectory, validado fuera del workspace y bajo la raíz temporal del sistema, contiene exclusivamente el índice de prueba y el almacén de objetos. GIT_INDEX_FILE y GIT_OBJECT_DIRECTORY solo se asignan al entorno de los subprocesos; no se cambia el entorno persistente ni la configuración. Se elimina al terminar.

Secuencia real por muestra, con bytes leídos del fichero sin escribir el working tree:

```text
git read-tree --empty                                # índice temporal
git hash-object --no-filters --stdin                  # OID de bytes originales
git hash-object -w --path=<ruta> --stdin              # clean real; objetos temporales
git update-index --add --cacheinfo 100644 <OID> <ruta> # índice temporal
git cat-file blob :<ruta>                            # bytes incorporados
git cat-file --filters --path=<ruta> <OID>            # bytes con filtros de checkout
git ls-files --stage                                 # diez entradas temporales
```

No se ejecuta git add. Ambas salidas se comparan byte a byte con el original y se relee cada muestra para comprobar que el fichero sigue idéntico. El OID original y el filtrado coinciden; los OID siguientes son identificadores de blobs Git, no un nuevo inventario SHA256 ni revalidación jurídica.

| Muestra | Bytes | CRLF | LF total | OID original = filtrado | Incorporación igual | Checkout igual | Fichero intacto |
|---|---:|---:|---:|---|---|---|---|
| `07_Business/03_Market/evidence/entur_siri.html` | 1675049 | 0 | 1812 | `c01e002d8baca9964187869fdeda8cdc1c5ecefd` | YES | YES | YES |
| `03_Compliance/Spain/01_Primary_Law/Ley_9_2025/Ley_9_2025_ORIGINAL_BOE.xml` | 625657 | 0 | 2568 | `d2f0450f469eb64a78762361c0902522488789ee` | YES | YES | YES |
| `03_Compliance/NAP/01_Policies/NAP_Licencia_Datos.html` | 22033 | 181 | 370 | `e6210bd58279d4a9109edb3071c4e4945b9627df` | YES | YES | YES |
| `PROJECT_CURRENT_STATE.md` | 12089 | 239 | 239 | `1a876672744dfa614c6eaa71d2e8fa1e65d95bfc` | YES | YES | YES |
| `project_baseline.json` | 8360 | 244 | 244 | `288f47f62447ded48e23d571e2e12d86ce54386c` | YES | YES | YES |
| `03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_REQUIREMENTS.csv` | 188404 | 49 | 49 | `2bbd44def205da4b7fe31a3a55438923d2fc2e13` | YES | YES | YES |
| `03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.json` | 5794 | 166 | 166 | `5b95909d9dc2fcf969d58ef685d3df6ab33a8d82` | YES | YES | YES |
| `07_Business/02_Capabilities/CAPABILITY_REGISTER.md` | 35827 | 0 | 475 | `9b2dd0f63144fca41153ea2aaf3ee72a84a45d18` | YES | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/informe-validacion.html` | 11780 | 0 | 307 | `20cef0015526a3b3a3a9f98082a4813f3934eaa8` | YES | YES | YES |
| `02_Data_Engineering/GTFS_Lab/exports/route_440.kml` | 15700 | 0 | 29 | `3a08b1509e6b2eb124efb73c719285e1234939fb` | YES | YES | YES |

Proceso de verificación Python: exit_code = 0; todas las aserciones completadas. NAP contiene saltos mixtos y los dos documentos raíz y CSV/JSON congelados contienen CRLF: la prueba no se limita a ficheros ya LF.

WORKING_TREE_MODIFIED_BY_TEST = NO. REAL_GIT_INDEX_CHANGED = NO: `.git/index` ausente antes/después y ls-files --stage vacío en el índice real. GLOBAL_GIT_CONFIG_CHANGED = NO; fingerprints de las configuraciones global, sistema y local iguales antes/después. TEMPORARY_DIRECTORY_REMOVED = YES. Ninguna escritura de objetos en el almacén del repositorio raíz.

Los únicos cambios deliberados del working tree son los cuatro archivos de política/auditoría enumerados abajo; se distinguen de la prueba aislada.

## Recursos, desviación y límites

REPOSITORY_WIDE_SCAN_PERFORMED = YES: al inicio se ejecutó una búsqueda recursiva filtrada de nombres mediante rg --files antes de aplicar la restricción del adjunto. Fue un incumplimiento de la prohibición de redescubrir rutas; no fue un escaneo de contenido ni un hash. Se detectó, se detuvo esa estrategia y no se repitió. Las clasificaciones posteriores proceden exclusivamente del manifiesto y comprobaciones de rutas/ancestros derivados de él.

RESOURCE_GUARD_TRIGGERED = YES (corrección manual de esa desviación, sin exceder límites de la prueba). REPOSITORY_WIDE_HASH_PERFORMED = NO. No contenido de PDF, bases, feeds, árboles anidados o generados grandes; no investigación web ni lectura de credenciales originales. Las salidas largas del análisis de rutas del manifiesto se limitaron/truncaron en pantalla; el PASS técnico se apoya en la prueba aislada completa, no en esas salidas.

La preservación de bytes se verifica en diez representantes, no en cada candidato. Los atributos de los doce PDF se verifican sin recertificar sus contenidos. No se certifica portabilidad ejecutable, ausencia general de secretos, fidelidad jurídica ni consolidación global. Los informes previos permanecen históricos.

## Archivos y resultado

- Creados: `.gitattributes`, `reports/repository_integrity/GIT_LINE_ENDING_POLICY.md`.
- Modificados: `REPOSITORY_POLICY.md` (sección de saltos de línea), `reports/repository_integrity/FIRST_FORMAL_COMMIT_AUDIT.md` (adenda acotada).
- `.gitignore`, manifiestos, verification JSON histórico, HTML saneado, original sensible, documentos congelados y PDF se conservan.

LINE_ENDING_REVIEW = PASS.
GITATTRIBUTES_POLICY = ESTABLISHED.
BYTE_PRESERVED_EVIDENCE_TRANSFORMED = NO.
LINE_ENDING_BLOCKER = NO.
GLOBAL_GIT_CONFIG_CHANGED = NO.
REAL_GIT_INDEX_CHANGED = NO.
FIRST_FORMAL_COMMIT = STILL_PENDING.
PROJECT_CONSOLIDATION = BLOCKED.

Pendientes: revisión de rutas absolutas ejecutables y verificación final pre-commit acotada. Esta resolución no autoriza staging, commit, tag, push ni ninguna otra fase. No se ejecutan esas acciones.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

