# Compliance V1 — remediación del replay portable del manifest

Fecha: 2026-09-28
Rama: `fix/compliance-v1-fixture-replay-portability`
Base: `origin/main` en `56d75a2d0c0b32a5906ef31b279103d785f53977`

## Causa y protección histórica

`FIXTURE_MANIFEST_REPLAY` exige que el manifest generado sea idéntico byte a byte al fixture. El generador anterior escribía en modo texto; en Windows, la traducción de newline producía CRLF frente al LF canónico de Git. El freeze `03_Compliance/reports/evidence/compliance_v1_20260928/freeze.json` conserva el estado histórico y no se modifica. SHA-256 del freeze: `3BBB6D87500608364972CFE841D6B2D3D03558FC73F1960A28579905FAEC6A3E`.

El freeze registró el generador histórico `A9310139C2D5931E272840C1278064DCFB6B34D3DE7CFDF566A72B53BD53E365` y el manifest histórico de checkout CRLF `A407838AFBF086CF85CE5EA626FA6745217CD92B88A599538E3EEB4B3C4334AF`. El manifest canónico del blob Git/checkout es `B27FFCEF76B9D3E099606F876AE9007869E5041F203F358DAEE9D6F89BB144C1` (20.737 bytes, 572 LF, cero CRLF, sin BOM, newline final).

## Remediación y replay binario

El único cambio funcional está en `tools/compliance_v1_fixtures.py`: serializa `(json.dumps(cases, indent=2) + "\n").encode("utf-8")` y persiste los bytes con `Path.write_bytes()`. Mantiene estructura, orden, indentación y newline final. `.gitattributes` y el fixture no cambian. SHA-256 del generador remediado: `60850BC0741DD8BE0CA9E5B312EEA95DA409E421EABADB4A4BDA040252DF6071`.

[`binary_replay.json`](binary_replay.json) registra igualdad binaria entre blob Git, checkout limpio y replay Windows; los tres tienen hash `B27FFCEF76B9D3E099606F876AE9007869E5041F203F358DAEE9D6F89BB144C1` y 20.737 bytes. Los PASS del cierre histórico siguen limitados a su entorno y no prueban ejecución multiplataforma.

## Gates e integridad

- Compliance V1: PASS; Phase 1 22/22, Phase 2 386 PASS; `UNCHANGED_COUNT_audit.rules` permanece como discrepancia histórica documentada. Hash de DB Compliance antes/después: `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`.
- GTFS_Lab V1: PASS; E2E sintético y GIS direccional PASS. Hash protegido antes/después: `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`.
- Trust Contract M01: PASS, 12/12 checks.
- `py_compile` y `git diff --check`: PASS (se registran en el manifest de evidencia).
- El fixture mantiene el hash canónico `B27…`; freeze `3BBB…`; `.gitattributes` intacto; M02 no fue modificado.

## Portabilidad e impacto en M02

Diseño cross-platform verificado: UTF-8 explícito y escritura binaria evitan traducción de newline por el runtime. Ejecución cross-platform no verificada: WSL solo expuso `docker-desktop`, sin Python, y no había daemon Docker Linux accesible. No se afirma ejecución Linux.

M02 debe repetir `FIXTURE_MANIFEST_REPLAY` en un checkout limpio de Windows al integrar esta remediación. No se modificó su rama ni su worktree, que ya tenía cambios locales.

La evidencia persistente se limita a este informe, replay binario estructurado, resúmenes finales de ambos gates, Trust Contract M01 y `evidence_manifest.json`. Runs completos, fixtures de gate, inputs y exports se regeneran fuera de Git.

Clasificación: cambio intencional del serializador; evidencia histórica preservada; sin merge de M02.

**COMPLIANCE_FIXTURE_REPLAY_PORTABILITY_PR_READY_FOR_MERGE_REVIEW**
