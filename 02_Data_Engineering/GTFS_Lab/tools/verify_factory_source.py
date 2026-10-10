"""Verify captured synthetic sources and generate a disposable 32-file demo ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def verify(root: Path) -> None:
    manifest = json.loads((root / 'SOURCE_MANIFEST.json').read_text(encoding='utf-8-sig'))
    records = manifest['files']
    for record in records:
        path = root / record['path']
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            raise ValueError('Source manifest contains an unsafe path')
        content = path.read_bytes()
        if len(content) != record['bytes'] or hashlib.sha256(content).hexdigest() != record['sha256']:
            raise ValueError(f'Source capture differs: {record["path"]}')
    with tempfile.TemporaryDirectory(prefix='tdl_factory_source_') as name:
        work = Path(name)
        shutil.copy2(root / 'generar_cs_autobuses.py', work)
        shutil.copytree(root / 'origenes', work / 'origenes')
        for option in ('--generar-gtfs', '--empaquetar-gtfs'):
            subprocess.run([sys.executable, str(work / 'generar_cs_autobuses.py'), option], cwd=work, check=True, capture_output=True)
        packages = list(work.rglob('*.zip'))
        if len(packages) != 1:
            raise ValueError('Expected one generated demo ZIP')
        with zipfile.ZipFile(packages[0]) as package:
            names = package.namelist()
            if len(names) != 32 or len(set(names)) != 32 or any('/' in n or '\\' in n for n in names) or package.testzip() is not None:
                raise ValueError('Synthetic ZIP structure or CRC differs')
    print(json.dumps({'source_files_verified': len(records), 'demo_zip_files': 32, 'status': 'PASS'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('factory', type=Path)
    verify(parser.parse_args().factory)
