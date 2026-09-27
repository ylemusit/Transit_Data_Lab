# Git long-path diagnosis — blocker resolution 04

Date UTC: 2026-09-27T03:49:09.355781+00:00

LONG_PATH_DIAGNOSIS = PASS
LONG_PATH_ROOT_CAUSE = CONFIRMED
CORE_LONGPATHS_LOCAL = TRUE
LONG_PATH_TESTS = 9/9 PASS
REAL_INDEX_CHANGED = NO
REAL_STAGED_FILES = 0
FIRST_FORMAL_COMMIT = STILL_PENDING
PROJECT_CONSOLIDATION = BLOCKED

## Context and interpretation

The previous controlled add of 837 candidates returned 128; the prospective snapshot contained 838 files including its final-gate report. The fatal stderr was not preserved. Nine known candidate absolute paths exceed 260 characters, and core.longpaths was reported unset. These observations initially supported only LONG_PATH_ROOT_CAUSE = UNCONFIRMED.

This execution reused exactly the nine paths listed in FIRST_FORMAL_COMMIT_FINAL_GATE.md and checked membership in FIRST_FORMAL_COMMIT_MANIFEST.csv (git_eligible=YES). Length is the absolute Windows path length, including the repository root and separator. Existence checks use metadata only; candidate content was processed only by Git during the authorised temporary-index adds.

Git version: git version 2.51.2.windows.1.
Before effective core.longpaths: UNSET (exit 1); origin: UNSET.
Repository-local config changed: YES.
After effective core.longpaths: file:.git/config	true.

Selected LONG_PATH_TEST_FILE: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json`.
Absolute length: 337. This is an approved export metadata manifest, not the ZIP/raw feed/database or a nested repository. It was selected without reading its contents.
First temporary-index test: exit 128; stderr category FILENAME_TOO_LONG.
Post-fix same-file test: exit 0.
All nine tested after correction: YES; passed 9/9.

The isolated failure explicitly reports Filename too long; the identical file succeeds with repository-local core.longpaths=true, and all nine known long candidates succeed. This confirms and resolves a reproducible long-path staging blocker. It cannot reconstruct the missing fatal message from the original 837-file attempt or prove that no further staging blockers exist.

## Known candidate paths

| path (repository-relative) | character_length (absolute) | exists | candidate |
| --- | ---: | --- | --- |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json-spreadsheet-safe.csv` | 278 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json-spreadsheet-safe.csv.manifest.json` | 292 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json.json` | 262 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json.json.manifest.json` | 276 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/run_001/gtfs-export-route-AECL118-VACL070_1-VACL070_2-VACL070_3-VACL072_1-VACL072_2-VACL072_3-VACL072_4-VACL072_5-VACL072_6-VACL072_7-6a65269b.json` | 308 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/run_001/gtfs-export-route-AECL118-VACL070_1-VACL070_2-VACL070_3-VACL072_1-VACL072_2-VACL072_3-VACL072_4-VACL072_5-VACL072_6-VACL072_7-6a65269b.json.manifest.json` | 322 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/03_gtfs_explorer/run_001/gtfs-export-route-009632-009633-009634-009635-009636-009637-009638-009640-009641-009642-009643-009644-009645-009646-009647-009-726d1dfe.json` | 315 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/03_gtfs_explorer/run_001/gtfs-export-route-009632-009633-009634-009635-009636-009637-009638-009640-009641-009642-009643-009644-009645-009646-009647-009-726d1dfe.json.manifest.json` | 329 | YES | YES |
| `02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json` | 337 | YES | YES |

## Scope and preservation

Real index absent before and after; git ls-files --stage -z returned zero entries both times. Temporary indexes were created outside the repository and removed when tests finished. Git add may write ordinary blobs to .git/objects; no object cleanup was performed. Full snapshot staging, commit, tag and push were not executed. No filenames, frozen references or evidence were renamed, moved, deleted or rewritten.

Repository-wide scan = NO. Repository-wide hash = NO. Datasets traversed = NO. Databases read = NO. RESOURCE_GUARD_TRIGGERED = NO. No web research, secret scan, Windows registry/policy, global or system Git configuration changes.

Remaining blocker: first formal commit and tag remain pending. The next separately authorised operation must refresh the explicit candidate list for the new diagnostic report/document changes, retry controlled staging and verify the actual staged index; no full-snapshot retry occurred here.

## Complete diagnostic commands and outputs

Commands without an index annotation use the real index. Annotated add commands use GIT_INDEX_FILE pointing to the stated temporary index outside the repository. stdout/stderr are fully captured; NUL delimiters are displayed as [NUL].

### git --version

Exit code: 0

stdout:
```text
git version 2.51.2.windows.1

```

stderr:
```text

```

### git config --show-origin --get core.longpaths

Exit code: 1

stdout:
```text

```

stderr:
```text

```

### git config --local --get core.longpaths

Exit code: 1

stdout:
```text

```

stderr:
```text

```

### git config --global --get core.longpaths

Exit code: 1

stdout:
```text

```

stderr:
```text

```

### git config --system --get core.longpaths

Exit code: 1

stdout:
```text

```

stderr:
```text

```

### git rev-parse --show-toplevel

Exit code: 0

stdout:
```text
C:/Users/yeiso/Desktop/Folder/VSCode/Proyectos/Transit Data Lab

```

stderr:
```text

```

### git branch --show-current

Exit code: 0

stdout:
```text
main

```

stderr:
```text

```

### git status --short --untracked-files=normal

Exit code: 0

stdout:
```text
?? .gitattributes
?? .gitignore
?? 02_Data_Engineering/
?? 03_Compliance/
?? 07_Business/
?? BACKUP_AND_RECOVERY.md
?? PROJECT_CURRENT_STATE.md
?? PROJECT_SNAPSHOT_V0.1.md
?? PROJECT_STRUCTURE.md
?? REPOSITORY_POLICY.md
?? project_baseline.json
?? reports/

```

stderr:
```text

```

### git ls-files --stage -z

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json

Index: before.index (outside repository)

Exit code: 128

stdout:
```text

```

stderr:
```text
error: open("02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json"): Filename too long
error: unable to index file '02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json'
fatal: adding files failed

```

### git config --local core.longpaths true

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git config --show-origin --get core.longpaths

Exit code: 0

stdout:
```text
file:.git/config	true

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json

Index: after.index (new clean index, outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json-spreadsheet-safe.csv

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json-spreadsheet-safe.csv.manifest.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json.json.manifest.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/run_001/gtfs-export-route-AECL118-VACL070_1-VACL070_2-VACL070_3-VACL072_1-VACL072_2-VACL072_3-VACL072_4-VACL072_5-VACL072_6-VACL072_7-6a65269b.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/run_001/gtfs-export-route-AECL118-VACL070_1-VACL070_2-VACL070_3-VACL072_1-VACL072_2-VACL072_3-VACL072_4-VACL072_5-VACL072_6-VACL072_7-6a65269b.json.manifest.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/03_gtfs_explorer/run_001/gtfs-export-route-009632-009633-009634-009635-009636-009637-009638-009640-009641-009642-009643-009644-009645-009646-009647-009-726d1dfe.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git --literal-pathspecs add -- 02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/03_gtfs_explorer/run_001/gtfs-export-route-009632-009633-009634-009635-009636-009637-009638-009640-009641-009642-009643-009644-009645-009646-009647-009-726d1dfe.json.manifest.json

Index: after.index (outside repository)

Exit code: 0

stdout:
```text

```

stderr:
```text

```

### git ls-files --stage -z

Index: after.index (outside repository)

Exit code: 0

stdout:
```text
100644 4ec3fbf7bbfb0fe807b9665d8618383c34b4a979 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json-spreadsheet-safe.csv[NUL]100644 7ecde53dc90ce699f975cb1b0940a64c99bad1b3 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json-spreadsheet-safe.csv.manifest.json[NUL]100644 51ba5f11e61079f2606f3dd421e1048683836c55 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json.json[NUL]100644 943e1dd31fe3b18926d7ca4276861e7d1766f560 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/002_ancebus/03_gtfs_explorer/run_001/gtfs-export-route-VACL018-VACL060-service-HIJUELAS-VACL018_WEEKDAY-VACL060_SERVICE-json.json.manifest.json[NUL]100644 0eb0c65ff2b66882b3fb3ef8829df963fe9c948e 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/run_001/gtfs-export-route-AECL118-VACL070_1-VACL070_2-VACL070_3-VACL072_1-VACL072_2-VACL072_3-VACL072_4-VACL072_5-VACL072_6-VACL072_7-6a65269b.json[NUL]100644 2d7b8084b7ac02acab011ebe66c413aa0aedae24 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/run_001/gtfs-export-route-AECL118-VACL070_1-VACL070_2-VACL070_3-VACL072_1-VACL072_2-VACL072_3-VACL072_4-VACL072_5-VACL072_6-VACL072_7-6a65269b.json.manifest.json[NUL]100644 7d892f69274c2afa36d2821cded3131426b8f794 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/03_gtfs_explorer/run_001/gtfs-export-route-009632-009633-009634-009635-009636-009637-009638-009640-009641-009642-009643-009644-009645-009646-009647-009-726d1dfe.json[NUL]100644 094f1f712dca6268e9aadf8086c75a58e62d1e19 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/03_gtfs_explorer/run_001/gtfs-export-route-009632-009633-009634-009635-009636-009637-009638-009640-009641-009642-009643-009644-009645-009646-009647-009-726d1dfe.json.manifest.json[NUL]100644 1762902b8942a94f68d63e493a0ba36707380cea 0	02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_002_rc002/gtfs-export-route-2151-2153-2161-2162-2163-2164-2166-2312-2314-2315-2316-2318-2321-2322-2324-2326-2336-2610-2611-3115-3122-3129-2d500b52.zip.manifest.json[NUL]
```

stderr:
```text

```

### git config --show-origin --get core.longpaths

Exit code: 0

stdout:
```text
file:.git/config	true

```

stderr:
```text

```

### git ls-files --stage -z

Exit code: 0

stdout:
```text

```

stderr:
```text

```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
