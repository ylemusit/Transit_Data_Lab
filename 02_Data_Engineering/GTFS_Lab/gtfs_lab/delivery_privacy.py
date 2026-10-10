"""Read-only path inspection with explicit coverage for client artifact formats."""
import importlib.util
import re
import zipfile
from xml.etree import ElementTree as ET
from pathlib import Path

TEXT_SUFFIXES = {".csv", ".geojson", ".html", ".json", ".kml", ".md", ".txt", ".xml", ".yaml", ".yml"}
LOCAL_PATH_PATTERN = re.compile(r"(?i)(?<![a-z0-9])(?:[a-z]:[\\/]|\\\\[^\\/\s]+[\\/][^\\/\s]+[\\/]|/(?:Users|home|tmp|var|mnt|private|opt|workspace)/)")


def path_matches(text):
    # A slash in a URL/query is not an operating-system path.
    text = re.sub(r"https?://[^\s`\"'<>]+", "", text, flags=re.IGNORECASE)
    return len(LOCAL_PATH_PATTERN.findall(text))


def extract_pdf_text(path):
    if importlib.util.find_spec("pypdf") is None:
        return None
    from pypdf import PdfReader
    reader = PdfReader(path, strict=True)
    if reader.is_encrypted or reader.attachments:
        return None  # nested attachments require their own inspection
    texts = [str(reader.metadata or {})]
    for page in reader.pages:
        text = page.extract_text()
        if not text and page.images:
            return None  # no OCR claim for image-only evidence
        texts.append(text or "")
        for annotation in page.get("/Annots", []):
            texts.append(str(annotation.get_object()))
    return "\n".join(texts)


def inspect_delivery_content(root, pdf_extractor=None):
    from .delivery_integrity import inventory
    root = Path(root)
    extractor = pdf_extractor or extract_pdf_text
    text_files = pdf_files = archive_files = opaque = 0
    matches, unscanned = [], []
    pdf_status = "NOT_APPLICABLE"
    for name in sorted(inventory(root)):
        path = root / name
        try:
            if path.suffix.lower() in TEXT_SUFFIXES:
                text_files += 1
                count = path_matches(path.read_text(encoding="utf-8", errors="strict"))
            elif path.suffix.lower() == ".pdf":
                pdf_files += 1
                text = extractor(path)
                if text is None:
                    unscanned.append(name); pdf_status = "NOT_AVAILABLE"; continue
                if pdf_status != "NOT_AVAILABLE": pdf_status = "COMPLETED"
                count = path_matches(text)
            elif path.suffix.lower() in {".xlsx", ".kmz"}:
                archive_files += 1
                count = 0
                with zipfile.ZipFile(path) as archive:
                    for member in archive.infolist():
                        if member.is_dir(): continue
                        if member.file_size > 64 * 1024 * 1024:
                            unscanned.append(name); break
                        if Path(member.filename).suffix.lower() not in {".xml", ".rels", ".kml"} and not member.filename.endswith("/.rels"):
                            unscanned.append(name); continue
                        raw = archive.read(member).decode("utf-8", errors="strict")
                        tree = ET.fromstring(raw)
                        decoded = "\n".join([*tree.itertext(), *[value for element in tree.iter() for value in element.attrib.values()]])
                        count += path_matches(decoded)
            else:
                opaque += 1; unscanned.append(name); continue
            if count: matches.append({"file": name, "match_count": count})
        except Exception:
            unscanned.append(name)
            if path.suffix.lower() == ".pdf": pdf_status = "NOT_AVAILABLE"
    return {"status": "FAIL_PATH_FOUND" if matches else "PARTIAL_UNSCANNED_CONTENT" if unscanned else "PASS",
            "text_files_scanned": text_files, "pdf_files": pdf_files, "pdf_text_scan": pdf_status,
            "archive_files_scanned": archive_files, "opaque_files_not_text_scanned": opaque,
            "unscanned_files": sorted(set(unscanned)), "path_matches": matches,
            "scope": "Text, PDF text/metadata/annotations, XLSX XML and KMZ KML; no OCR or arbitrary binaries"}
