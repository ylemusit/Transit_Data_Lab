# PyInstaller onedir build for the Windows self-service client.
from pathlib import Path
import os
import shutil

from PyInstaller.utils.hooks import collect_dynamic_libs
import reportlab

LAB_ROOT = Path(SPECPATH).resolve().parent
REPO_ROOT = LAB_ROOT.parents[1]
duckdb_cli = Path(os.environ.get("TDL_DUCKDB_CLI") or shutil.which("duckdb") or "").resolve()
if not duckdb_cli.is_file():
    raise SystemExit("DuckDB CLI not found; set TDL_DUCKDB_CLI to the approved duckdb.exe")

runtime_files = [
    (str(duckdb_cli), "."),
    (str(REPO_ROOT / "tools" / "compliance_v1_engine.py"), "runtime_assets/tools"),
    (str(REPO_ROOT / "03_Compliance" / "reports" / "evidence" / "compliance_v1_20260928" / "source_manifest.json"),
     "runtime_assets/03_Compliance/reports/evidence/compliance_v1_20260928"),
    (str(REPO_ROOT / "03_Compliance" / "reports" / "evidence" / "compliance_v1_20260928" / "sources" / "gtfs_reference.md"),
     "runtime_assets/03_Compliance/reports/evidence/compliance_v1_20260928/sources"),
]
for source, _ in runtime_files:
    if not Path(source).is_file():
        raise SystemExit(f"Required packaged runtime file is missing: {source}")

font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
pdf_fonts = [(str(font_dir / name), "reportlab/fonts")
             for name in ("Vera.ttf", "VeraBd.ttf")]
datas = runtime_files + [(str(LAB_ROOT / "spec"), "spec")] + pdf_fonts
hiddenimports = ["gtfs_lab.client_workflow", "gtfs_lab.client_worker", "gtfs_lab.client_pdf", "lxml.etree"]
binaries = collect_dynamic_libs("lxml")
hookspath = []
runtime_hooks = [str(LAB_ROOT / "packaging" / "runtime_path_hook.py")]
excludes = []

gui_analysis = Analysis(
    [str(LAB_ROOT / "gtfs_lab" / "client_app.py")],
    pathex=[str(LAB_ROOT)], binaries=binaries, datas=datas,
    hiddenimports=hiddenimports, hookspath=hookspath, hooksconfig={},
    runtime_hooks=runtime_hooks, excludes=excludes, noarchive=False,
)
gui_pyz = PYZ(gui_analysis.pure)
gui_exe = EXE(gui_pyz, gui_analysis.scripts, [], exclude_binaries=True,
              name="tdl-client", debug=False, bootloader_ignore_signals=False,
              strip=False, upx=False, console=False)

worker_analysis = Analysis(
    [str(LAB_ROOT / "gtfs_lab" / "client_worker.py")],
    pathex=[str(LAB_ROOT)], binaries=binaries, datas=datas,
    hiddenimports=hiddenimports, hookspath=hookspath, hooksconfig={},
    runtime_hooks=runtime_hooks, excludes=excludes, noarchive=False,
)
worker_pyz = PYZ(worker_analysis.pure)
worker_exe = EXE(worker_pyz, worker_analysis.scripts, [], exclude_binaries=True,
                 name="tdl-worker", debug=False, bootloader_ignore_signals=False,
                 strip=False, upx=False, console=False)

coll = COLLECT(gui_exe, gui_analysis.binaries, gui_analysis.datas,
               worker_exe, worker_analysis.binaries, worker_analysis.datas,
               strip=False, upx=False, name="tdl-client")
