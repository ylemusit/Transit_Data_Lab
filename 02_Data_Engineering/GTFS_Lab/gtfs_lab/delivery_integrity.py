"""Exact, contained inventories for separately sealed client deliveries."""
import hashlib
import json
import re
import stat
from pathlib import Path, PurePosixPath


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def contained(root, name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError("Invalid artifact reference")
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != name:
        raise ValueError("Artifact reference escapes delivery")
    root = Path(root).resolve()
    result = (root / name).resolve()
    if not result.is_relative_to(root):
        raise ValueError("Artifact reference escapes delivery")
    return result


def inventory(root):
    root = Path(root)
    pending, files = [root], set()
    while pending:
        path = pending.pop()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("Reparse points are not delivery artifacts")
        if stat.S_ISDIR(info.st_mode):
            pending.extend(path.iterdir())
        elif stat.S_ISREG(info.st_mode):
            files.add(path.relative_to(root).as_posix())
        else:
            raise ValueError("Unsupported delivery artifact")
    return files


def verify_inventory(root, records, excluded):
    if not isinstance(records, dict) or not records:
        raise ValueError("Delivery inventory must not be empty")
    actual = inventory(root) - set(excluded)
    if actual != set(records):
        raise ValueError("Delivery inventory mismatch")
    for name, row in records.items():
        path = contained(root, name)
        if not isinstance(row, dict) or not re.fullmatch(r"[0-9a-fA-F]{64}", str(row.get("sha256", ""))):
            raise ValueError("Invalid artifact digest")
        size = row.get("size_bytes")
        if type(size) is not int or size < 0 or path.stat().st_size != size or digest(path) != row["sha256"]:
            raise ValueError("Delivery artifact mismatch: " + name)
    return len(actual)


def verify_delivery(delivery):
    delivery = Path(delivery)
    manifest_path = delivery / "audit_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seal = json.loads((delivery / "delivery_seal.json").read_text(encoding="utf-8"))
    if seal.get("audit_manifest_sha256") != digest(manifest_path):
        raise ValueError("Source delivery seal mismatch")
    verify_inventory(delivery, manifest.get("delivery_artifacts"), {"audit_manifest.json", "delivery_seal.json"})
    return manifest
