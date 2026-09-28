from __future__ import annotations
import shutil, subprocess
from pathlib import Path
from .core import RunContext

def build_duckdb(ctx: RunContext) -> dict:
    executable = shutil.which("duckdb")
    if not executable:
        return {"status": "FAIL_LOCAL", "reason": "DuckDB CLI no está disponible"}
    db = ctx.work_dir / "dataset.duckdb"
    statements = ["CREATE SCHEMA raw;"]
    for table, path in sorted(ctx.tables.items()):
        literal = str(path).replace("\\", "/").replace("'", "''")
        statements.append(f"CREATE TABLE raw.{table} AS SELECT * FROM read_csv('{literal}', header=true, all_varchar=true, strict_mode=true);")
    sql = "\n".join(statements)
    proc = subprocess.run([executable, str(db), "-c", sql], cwd=ctx.work_dir, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        return {"status": "FAIL_LOCAL", "reason": proc.stderr[-3000:], "database": str(db)}
    verify_sql = "SELECT COUNT(*) > 0 AND COUNT(*) FILTER (WHERE data_type = 'VARCHAR') = COUNT(*) AS all_text FROM information_schema.columns WHERE table_schema='raw' AND table_name='stop_times' AND column_name IN ('trip_id','arrival_time','departure_time');"
    verify = subprocess.run([executable, "-readonly", str(db), "-c", verify_sql], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if verify.returncode:
        return {"status": "FAIL_LOCAL", "reason": verify.stderr[-3000:], "database": str(db)}
    if "true" not in verify.stdout.lower():
        return {"status": "FAIL_LOCAL", "reason": "Las columnas de identificación/tiempo no se conservaron como VARCHAR", "database": str(db)}
    return {"status": "PASS", "database": str(db), "tables": sorted(ctx.tables), "cli_output": verify.stdout}
