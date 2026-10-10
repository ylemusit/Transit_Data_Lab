"""Standalone, standard-library verification of a private TDL delivery.

Usage: python VERIFICAR.py [delivery_folder]. No source checkout is required.
Hashes establish consistency with the included seal, not auditor authenticity.
"""
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
from urllib.parse import unquote, urlsplit
import zipfile
import xml.etree.ElementTree as ET


def read(path): return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""): h.update(block)
    return h.hexdigest()


def local(root, name):
    rel = PurePosixPath(name)
    if not name or rel.is_absolute() or ".." in rel.parts or ":" in name or "\\" in name:
        raise ValueError("Ruta insegura: " + name)
    path = root / rel
    if not path.resolve().is_relative_to(root.resolve()): raise ValueError("Ruta fuera del paquete")
    return path


def inventory(root):
    pending = [root]; result = set()
    while pending:
        current = pending.pop()
        if current.is_symlink() or getattr(current.stat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError("Enlace de sistema de archivos no permitido")
        with os.scandir(current) as entries:
            for entry in entries:
                if entry.is_symlink() or getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    raise ValueError("Enlace de sistema de archivos no permitido")
                path = Path(entry.path)
                if entry.is_dir(follow_symlinks=False): pending.append(path)
                elif entry.is_file(follow_symlinks=False): result.add(path.relative_to(root).as_posix())
    return result


class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        self.links.extend(value for key, value in attrs if key in {"href", "src"})


def verify(root):
    root = Path(root).resolve()
    manifest = read(root / "DELIVERY_MANIFEST.json")
    if sha(root / "DELIVERY_MANIFEST.json") != read(root / "DELIVERY_SEAL.json")["manifest_sha256"]:
        raise ValueError("Sello del manifiesto incorrecto")
    actual = inventory(root) - {"DELIVERY_MANIFEST.json", "DELIVERY_SEAL.json"}
    if actual != set(manifest["artifacts"]): raise ValueError("Inventario distinto")
    for name, expected in manifest["artifacts"].items():
        path = local(root, name)
        if sha(path) != expected["sha256"] or path.stat().st_size != expected["size_bytes"]:
            raise ValueError("Archivo alterado: " + name)
    model = read(root / "02_MODELO/REPORT_MODEL.json")
    canonical = {k: v for k, v in model.items() if k != "semantic_sha256"}
    semantic = hashlib.sha256(json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if semantic != model["semantic_sha256"]: raise ValueError("Modelo semántico alterado")
    controls = model["controls"]; cases = model["cases"]
    ids = [c["rule_id"] for c in controls]; case_ids = [c["case_id"] for c in cases]
    if len(ids) != len(set(ids)) or set(ids) != set(model["engagement"]["included_controls"]): raise ValueError("Alcance distinto")
    if len(case_ids) != len(set(case_ids)): raise ValueError("Caso duplicado")
    counts = dict(Counter(c["status"] for c in controls))
    if counts != model["conclusion"]["unique_control_counts"]: raise ValueError("Recuento distinto")
    for control in controls:
        expected = {c["case_id"] for c in cases if control["rule_id"] in c["rule_ids"]}
        if expected != set(control.get("case_ids", [])): raise ValueError("Correspondencia de casos distinta")
    source = local(root, model["references"]["source_input"])
    if sha(source) != model["identity"]["source_sha256"] or model["identity"]["source_sha256"] != model["engagement"]["source"]["sha256"]:
        raise ValueError("Fuente distinta")
    refs = read(root / "REFERENCE_INDEX.json")["active_references"]
    for ref in refs:
        path = local(root, ref["path"])
        if sha(path) != ref["sha256"]: raise ValueError("Referencia alterada")
        if "pointer" in ref:
            row = read(path)
            for token in ref["pointer"].strip("/").split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                row = row[int(token)] if isinstance(row, list) else row[token]
            if "rule_id" in ref and row["rule_id"] != ref["rule_id"]: raise ValueError("Control de referencia distinto")
    parser = Links(); parser.feed((root / "INDEX.html").read_text(encoding="utf-8"))
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not local(root, unquote(url.path)).is_file(): raise ValueError("Enlace roto o externo")
    views = read(root / "VIEW_CONSISTENCY.json")["views"]
    if {v["audience"] for v in views} != {"DIRECCION", "TECNICO"} or len(views) != 2: raise ValueError("Vistas incompletas")
    for view in views:
        if view["semantic_sha256"] != semantic or view["case_ids"] != case_ids or view["unique_control_counts"] != counts:
            raise ValueError("Vistas incoherentes")
        if ("TDL semantic SHA-256 " + semantic).encode() not in local(root, view["path"]).read_bytes():
            raise ValueError("Identidad semántica del PDF distinta")
    gis = root / "01_RESULTADOS/gis/Auditoria_Palma_R4.qgz"
    local_layers = 0
    if gis.exists():
        with zipfile.ZipFile(gis) as archive:
            tree = ET.fromstring(archive.read(next(n for n in archive.namelist() if n.endswith(".qgs"))))
            for element in tree.findall(".//datasource"):
                value = element.text
                if not value: continue
                if not value.startswith("./") or not local(root, "01_RESULTADOS/gis/" + value[2:]).is_file():
                    raise ValueError("Referencia cartográfica ausente o externa")
                local_layers += 1
    kmz = root / "01_RESULTADOS/Mapa_auditoria.kmz"
    if kmz.exists():
        with zipfile.ZipFile(kmz) as archive:
            for name in archive.namelist():
                if not name.endswith(".kml"): continue
                tree = ET.fromstring(archive.read(name))
                for element in tree.iter():
                    if element.tag.endswith("}href") and element.text and element.text not in archive.namelist():
                        raise ValueError("Referencia KMZ ausente o externa")
    for name, manifest_name, seal_name in [("R3", "PACKAGE_MANIFEST.json", "PACKAGE_SEAL.json"), ("R4", "SUPPLEMENT_MANIFEST.json", "SUPPLEMENT_SEAL.json")]:
        path = root / "ARCHIVOS_ORIGINALES" / (name + ".zip")
        if not path.exists(): continue
        with zipfile.ZipFile(path) as archive:
            mname = "02_EVIDENCIAS/" + manifest_name; sname = "02_EVIDENCIAS/" + seal_name
            raw = archive.read(mname); original = json.loads(raw)
            if hashlib.sha256(raw).hexdigest() != json.loads(archive.read(sname))["manifest_sha256"]:
                raise ValueError("Sello original incorrecto")
            if set(archive.namelist()) != set(original["artifacts"]) | {mname, sname}: raise ValueError("Archivo original incompleto")
            for member, expected in original["artifacts"].items():
                data = archive.read(member)
                if len(data) != expected["size_bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
                    raise ValueError("Contenido original alterado")
    return {"result": "PASS", "format": model["format"], "files": len(actual), "active_references": len(refs),
            "index_links": len(parser.links), "local_gis_layers": local_layers, "standalone": True, "semantic_sha256": semantic}


if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent), ensure_ascii=False))
