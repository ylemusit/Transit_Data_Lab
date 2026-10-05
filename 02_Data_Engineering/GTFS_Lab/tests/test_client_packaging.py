from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
PACKAGED_WORKER = LAB_ROOT / "dist-w01p" / "tdl-client" / "tdl-worker.exe"


def write_synthetic_zip(path: Path) -> None:
    rows = {
        "agency.txt": "agency_id,agency_name,agency_url,agency_timezone\nA,Example Transit,https://example.test,Europe/Madrid\n",
        "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\nS1,Stop One,40.4,-3.7\n",
        "routes.txt": "route_id,agency_id,route_short_name,route_type\nR1,A,1,3\n",
        "trips.txt": "route_id,service_id,trip_id\nR1,WK,T1\n",
        "stop_times.txt": "trip_id,arrival_time,departure_time,stop_id,stop_sequence\nT1,08:00:00,08:00:00,S1,1\n",
        "calendar.txt": "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\nWK,1,1,1,1,1,0,0,20261001,20261231\n",
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in rows.items():
            archive.writestr(name, content.encode("utf-8"))


def isolated_environment() -> dict[str, str]:
    keep = ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE")
    env = {key: os.environ[key] for key in keep if key in os.environ}
    system_root = env.get("SYSTEMROOT") or env.get("WINDIR")
    if not system_root:
        raise RuntimeError("SYSTEMROOT unavailable for isolated packaged-worker test")
    env["PATH"] = str(Path(system_root) / "System32")
    return env


@unittest.skipUnless(os.name == "nt" and PACKAGED_WORKER.is_file(), "Build the onedir package first")
class PackagedWorkerTests(unittest.TestCase):
    def _run_worker(self, source: Path, workspace: Path, audit_id: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(PACKAGED_WORKER), str(source), "--workspace", str(workspace),
             "--client-project-id", "tdl-local", "--audit-id", audit_id,
             "--source-provenance", "SYNTHETIC", "--audit-mode", "INITIAL"],
            cwd=workspace.parent, env=isolated_environment(), capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=120,
        )

    def test_complete_audit_with_unicode_paths_and_verified_delivery(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tdl packaged á ") as folder:
            root = Path(folder)
            source = root / "GTFS sintético ñ.zip"
            write_synthetic_zip(source)
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            workspace = root / "salida con espacios á" / "workspace"
            workspace.parent.mkdir()
            process = self._run_worker(source, workspace, "audit-packaged-success")
            self.assertEqual(process.returncode, 0, process.stderr[-2000:])
            result = json.loads(process.stdout)
            self.assertTrue(result["status"].startswith("COMPLETED"), result)
            self.assertTrue(result["artifacts_sha256_verified"])
            self.assertEqual(source_sha, hashlib.sha256(source.read_bytes()).hexdigest())
            delivery = Path(result["delivery_directory"])
            manifest = json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))
            seal = json.loads((delivery / "delivery_seal.json").read_text(encoding="utf-8"))
            self.assertTrue(seal["artifacts_verified"])
            self.assertEqual(result["audit_manifest_sha256"], seal["audit_manifest_sha256"])
            for relative, artifact in manifest["delivery_artifacts"].items():
                self.assertEqual(artifact["sha256"], hashlib.sha256((delivery / relative).read_bytes()).hexdigest())

    def test_genuine_worker_failure_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tdl packaged failure ") as folder:
            root = Path(folder)
            source = root / "invalid.zip"
            source.write_bytes(b"not a zip archive")
            workspace = root / "workspace"
            workspace.mkdir()
            process = self._run_worker(source, workspace, "audit-packaged-failure")
            self.assertEqual(process.returncode, 2)
            result = json.loads(process.stdout)
            self.assertEqual(result["status"], "BLOCKED_INPUT_INVALID")


if __name__ == "__main__":
    unittest.main()