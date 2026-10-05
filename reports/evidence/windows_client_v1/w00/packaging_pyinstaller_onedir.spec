from pathlib import Path
import os

PROBE = Path(SPECPATH).resolve()
REPO = PROBE.parents[4]
LAB = REPO / "02_Data_Engineering" / "GTFS_Lab"
DUCKDB = Path(os.environ["TDL_DUCKDB_CLI"]).resolve()
COMPLIANCE = REPO / "03_Compliance" / "reports" / "evidence" / "compliance_v1_20260928"

a = Analysis(
    [str(PROBE / "packaging_onedir_probe_entry.py")],
    pathex=[str(LAB)],
    binaries=[(str(DUCKDB), ".")],
    datas=[
        (str(LAB / "spec"), "spec"),
        (str(REPO / "tools" / "compliance_v1_engine.py"), "tdl_resources/tools"),
        (str(COMPLIANCE / "source_manifest.json"), "tdl_resources/03_Compliance/reports/evidence/compliance_v1_20260928"),
        (str(COMPLIANCE / "sources" / "gtfs_reference.md"), "tdl_resources/03_Compliance/reports/evidence/compliance_v1_20260928/sources"),
    ],
    hiddenimports=["lxml.etree"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[str(PROBE / "packaging_onedir_runtime_hook.py")],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="tdl-w00o-worker", debug=False,
          bootloader_ignore_signals=False, strip=False, upx=False, console=True)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="tdl-w00o-worker")
