# ENTUR SIRI — registro de saneamiento de evidencia

Fecha: 2026-09-27. Ejecución UTC: 2026-09-27T03:28:15.111794+00:00.

- Source evidence filename: `entur_siri.html`.
- Motivo: resolver exclusivamente el bloqueo de credenciales previo al primer commit formal.
- Credential category: Atlassian JWT.
- Contexto estructural: `EMBEDDED_PAGE_RUNTIME_TOKEN`. Aparece en parámetros `token` de URLs CDN de imágenes, en `EmbeddedMediaToken` y en `window["__MEDIA_CONFIG__"]` dentro del HTML descargado. Es un artefacto de ejecución de medios de la página; no se ha determinado si está vinculado a una sesión.
- Number of redactions: 5 apariciones de 1 valor JWT distinto.
- Approximate original locations: líneas 1805 (3) y 1806 (2).
- Método: sustitución binaria de cada valor JWT compacto delimitado por `[REDACTED_ATLASSIAN_JWT]`; sin decodificación, normalización, regeneración ni cambios adicionales al HTML.
- Sanitized evidence filename/path: `07_Business/03_Market/evidence/entur_siri.html`.
- Original preserved locally: YES, en `07_Business/03_Market/evidence/.sensitive_local/entur_siri.original.html`.
- Original excluded from Git: YES. SENSITIVE_ORIGINAL_TRACKED = NO; SENSITIVE_ORIGINAL_IGNORED = YES.
- Original SHA-256: `75239cbcad0c5d783654a1159ef1a66d2dd6540b00910cf09bd876efec0f6eb8`; bytes: 1676744.
- Sanitized SHA-256: `3b3218775876cf60823a34293fc0dbc33f84e6cf69a28199bfa70408aaf8f8d9`; bytes: 1675049.

El saneamiento NO constituye un cambio en la interpretación sustantiva de la evidencia de mercado. Todo el contenido ajeno a los cinco valores JWT permanece idéntico byte a byte. Las imágenes remotas cuya URL exige ese token pueden dejar de cargar; se preservan sus URLs salvo el valor de credencial y se conserva el original local para trazabilidad. No se ha probado carga remota ni vigencia del token.

## Referencias y procedencia

Se mantiene la versión saneada en la ruta canónica, por ser la opción de menor impacto. La búsqueda de referencias al nombre `entur_siri.html` se limitó a documentación Business (MD/JSON/YAML/CSV/TXT). Se encontró `07_Business/03_Market/evidence/source_manifest.json`, entrada `entur_siri`.

Referencias con cambio de ruta: 0. Referencias actualizadas: 0. El manifiesto histórico permanece intacto: su SHA-256 y tamaño describen la descarga original conservada localmente, no los bytes saneados actuales. Este registro enlaza explícitamente ambas versiones y sus huellas; cualquier comparación futura debe usar la huella correspondiente.

## Verificación dirigida

TARGETED_SECRET_RECHECK = PASS. JWT_BLOCKER_RESOLUTION = PASS.

- TARGETED_SECRET_RECHECK = PASS; ATLASSIAN_JWT_FINDINGS_AFTER_SANITIZATION = 0; SECRET_FINDINGS = 0.
- JWT_BLOCKER_RESOLUTION = PASS; SANITIZED_EVIDENCE_GIT_SAFE = YES para esta revisión dirigida.
- Archivos revisados (4): `07_Business/03_Market/evidence/entur_siri.html`, `07_Business/03_Market/evidence/ENTUR_SIRI_SANITIZATION_RECORD.md`, `.gitignore`, `reports/repository_integrity/FIRST_FORMAL_COMMIT_AUDIT.md`. El original sensible se excluye deliberadamente del análisis de archivos candidatos a Git.
- Patrones comprobados: JWT compactos, claves privadas, tokens conocidos API/cloud/GitHub/Slack/Google/Stripe/Anthropic/SendGrid, Authorization Bearer/Basic, asignaciones literales de secretos y credenciales en URLs. Los resultados son acotados a estos patrones y archivos; no certifican todo el repositorio.
- Conservación exacta: original local idéntico a la descarga; saneado idéntico al resultado de sustituir únicamente los 5 valores JWT. Marcadores = 5; líneas y bytes ajenos a las sustituciones preservados.
- `git check-ignore -v -- 07_Business/03_Market/evidence/.sensitive_local/entur_siri.original.html`: exit_code 0; regla `.gitignore`: `/07_Business/03_Market/evidence/.sensitive_local/`.
- `git check-ignore -v -- 07_Business/03_Market/evidence/entur_siri.html`: exit_code 1, sin salida; NOT_IGNORED.
- `git ls-files -- 07_Business/03_Market/evidence/.sensitive_local/entur_siri.original.html`: sin salida; NOT_TRACKED.
- Índice Git sin cambios respecto al inicio; no staging ejecutado.
- Referencia Business conservada y manifiesto histórico intacto.
- Repository-wide scan performed = NO; repository-wide hash performed = NO; RESOURCE_GUARD_TRIGGERED = NO.
- FIRST_FORMAL_COMMIT = STILL_PENDING; PROJECT_CONSOLIDATION permanece BLOCKED. Pendientes: core.autocrlf/preservación de bytes, revisión de rutas absolutas ejecutables y verificación final pre-commit.

Archivos creados: este registro y el original local ignorado. Archivos modificados: HTML canónico, `.gitignore` y auditoría formal. Archivos movidos/eliminados: 0/0. Sin commit, tag, push ni fases nuevas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
