"""Private transport acceptance: archive, relocate and run the packaged verifier."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import zipfile
from tools.audit_delivery_v1 import contained, digest, files, write


def transport(package, destination):
    package = Path(package); destination = Path(destination)
    if destination.exists(): raise ValueError("Relocation folder already exists")
    archive_path = package.with_suffix(".zip")
    if archive_path.exists(): raise ValueError("Archive already exists")
    source_paths = sorted(files(package))
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in source_paths: archive.write(path, path.relative_to(package).as_posix())
    destination.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(archive_path) as archive:
        expected = {p.relative_to(package).as_posix() for p in source_paths}
        if set(archive.namelist()) != expected: raise ValueError("Transport inventory differs")
        for name in archive.namelist():
            target = contained(destination, name); target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as stream, target.open("wb") as out:
                while block := stream.read(1024*1024): out.write(block)
            if digest(target) != digest(contained(package, name)): raise ValueError("Transport content differs")
    execution = subprocess.run([sys.executable, str(destination / "VERIFICAR.py")], cwd=destination,
                               capture_output=True, text=True, check=True)
    return {"package": str(package), "archive": str(archive_path), "archive_sha256": digest(archive_path),
            "transport_inventory": "PASS", "relocated_to": str(destination), "relocated_verification": json.loads(execution.stdout),
            "verification_requires_checkout": False, "emission_authorized": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True); parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(); result = transport(args.package, args.destination); write(args.receipt, result)
    print(json.dumps(result, ensure_ascii=False))
