"""Small process-tree and stage-marker control workload for W00-R."""
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import time

stage_file = Path(os.environ["TDL_RESOURCE_STAGE_FILE"])
def mark(stage: str, state: str) -> None:
    with stage_file.open("a", encoding="utf-8") as stream:
        stream.write('{"timestamp_utc":"%s","stage":"%s","state":"%s"}\n' %
                     (datetime.now(timezone.utc).isoformat(), stage, state))
        stream.flush()

child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(1.4)"])
for stage in ("INTAKE", "ZIP_EXTRACTION", "INGESTION", "AUDIT", "INTERPRETATION",
              "REPORT_GENERATION", "REPLAY", "CLEANUP"):
    mark(stage, "START")
    if stage == "INTAKE":
        Path(os.environ["TEMP"], "synthetic-temp.dat").write_bytes(b"control")
    time.sleep(0.12)
    mark(stage, "END")
child.wait()
Path(os.environ["TDL_RESOURCE_OUTPUT"], "synthetic-result.txt").write_text("ok", encoding="utf-8")
print("synthetic control complete")
print("synthetic stderr control", file=sys.stderr)
