from __future__ import annotations

import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path

from lxml import etree

from .intake import secure_parser


SCHEMA_PATH = Path(os.environ.get(
    "NETEX_SCHEMA_PATH",
    str(Path(__file__).resolve().parents[3] / "01_Research_Standards" / "NeTEx" / "schemas" / "v2.0.0" / "xsd" / "NeTEx_publication.xsd"),
))
MANIFEST_PATH = (
    Path(__file__).resolve().parents[3]
    / "01_Research_Standards" / "NeTEx" / "schemas" / "v2.0.0" / "schema_manifest.json"
)


class SchemaIdentityError(ValueError):
    pass


def verify_schema_snapshot(schema_path: str | Path, manifest_path: str | Path = MANIFEST_PATH) -> dict:
    schema_path = Path(schema_path).resolve(strict=True)
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    schema_root = schema_path.parent.parent
    if schema_path.relative_to(schema_root).as_posix() != manifest["root_schema"]:
        raise SchemaIdentityError("Schema path does not match the pinned root schema")
    for dependency in manifest["dependencies"]:
        dependency_path = schema_root / dependency["path"]
        try:
            digest = hashlib.sha256(dependency_path.read_bytes()).hexdigest()
        except OSError as exc:
            raise SchemaIdentityError("Pinned schema dependency is missing") from exc
        if digest != dependency["sha256"]:
            raise SchemaIdentityError("Pinned schema dependency hash mismatch")
    root = next(item for item in manifest["dependencies"] if item["path"] == manifest["root_schema"])
    return {"release": manifest["release"], "commit": manifest["commit"],
            "root_schema": manifest["root_schema"], "root_schema_sha256": root["sha256"]}


@lru_cache(maxsize=2)
def load_schema(schema_path: str | Path = SCHEMA_PATH) -> etree.XMLSchema:
    path = Path(schema_path)
    verify_schema_snapshot(path)
    path = path.resolve(strict=True)
    tree = etree.parse(str(path), secure_parser())
    return etree.XMLSchema(tree)
