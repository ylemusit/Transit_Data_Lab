from __future__ import annotations

import hashlib
import io
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from lxml import etree


MAX_INPUT_BYTES = 512 * 1024 * 1024
MAX_ZIP_MEMBERS = 256
MAX_XML_MEMBER_BYTES = 256 * 1024 * 1024
MAX_TOTAL_XML_BYTES = 512 * 1024 * 1024
MAX_REFERENCE_SAMPLES = 1000


class IntakeError(ValueError):
    pass


@dataclass(frozen=True)
class XmlSource:
    name: str
    data: bytes
    sha256: str


@dataclass(frozen=True)
class StreamInspection:
    inventory: dict
    errors: tuple[str, ...]
    xsd_valid: bool | None


def _safe_name(name: str) -> str:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (path.is_absolute() or re.match(r"^[A-Za-z]:", normalized)
            or ".." in path.parts or not path.name or "\x00" in normalized):
        raise IntakeError("Unsafe ZIP member path")
    return path.as_posix()


def _looks_like_xml(raw: bytes) -> bool:
    data = raw.lstrip(b"\xef\xbb\xbf\x00\xff\xfe \t\r\n")
    return data.startswith(b"<") or data.startswith(b"\x00<") or data.startswith(b"<\x00")


def read_sources(path: str | Path) -> tuple[str, tuple[XmlSource, ...], str]:
    source = Path(path)
    try:
        raw = source.read_bytes()
    except OSError as exc:
        raise IntakeError("Unable to read input") from exc
    if len(raw) > MAX_INPUT_BYTES:
        raise IntakeError("Input exceeds configured size limit")
    digest = hashlib.sha256(raw).hexdigest()
    if zipfile.is_zipfile(io.BytesIO(raw)):
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                members = archive.infolist()
                if len(members) > MAX_ZIP_MEMBERS:
                    raise IntakeError("ZIP member count exceeds configured limit")
                xml_members: list[XmlSource] = []
                total = 0
                seen: set[str] = set()
                for info in members:
                    if info.is_dir():
                        continue
                    name = _safe_name(info.filename)
                    if name in seen:
                        raise IntakeError("ZIP contains duplicate normalized paths")
                    seen.add(name)
                    if not name.lower().endswith((".xml", ".netex")):
                        continue
                    if info.file_size > MAX_XML_MEMBER_BYTES:
                        raise IntakeError("XML member exceeds configured size limit")
                    total += info.file_size
                    if total > MAX_TOTAL_XML_BYTES:
                        raise IntakeError("Total XML size exceeds configured limit")
                    data = archive.read(info)
                    xml_members.append(XmlSource(name, data, hashlib.sha256(data).hexdigest()))
        except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
            raise IntakeError("Unable to inspect ZIP input") from exc
        if not xml_members:
            raise IntakeError("ZIP contains no XML members")
        return "ZIP", tuple(sorted(xml_members, key=lambda item: item.name)), digest
    if not _looks_like_xml(raw):
        raise IntakeError("Input is neither XML nor a ZIP containing XML")
    return "XML", (XmlSource(source.name, raw, digest),), digest


def secure_parser() -> etree.XMLParser:
    return etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        huge_tree=False,
        recover=False,
        remove_comments=False,
    )


def parse_xml(data: bytes) -> etree._ElementTree:
    try:
        tree = etree.parse(io.BytesIO(data), secure_parser())
        if tree.docinfo.doctype or any(isinstance(node, etree._Entity) for node in tree.getroot().iter()):
            raise IntakeError("DTD and entity declarations are not accepted")
        return tree
    except (etree.XMLSyntaxError, OSError, ValueError) as exc:
        raise IntakeError("XML is not well formed") from exc


def inspect_xml_stream(data: bytes, schema: etree.XMLSchema | None) -> StreamInspection:
    """Validate and inventory an XML byte stream while pruning completed nodes."""
    options = {
        "events": ("start", "end"), "resolve_entities": False, "no_network": True,
        "load_dtd": False, "huge_tree": False,
    }
    counts: Counter[str] = Counter()
    identifiers: dict[str, list[str]] = defaultdict(list)
    namespaces: Counter[str] = Counter()
    refs = 0
    reference_samples: list[dict[str, str | None]] = []
    references_truncated = False
    root_name: str | None = None
    object_stack: list[tuple[etree._Element, str, str]] = []
    try:
        context = etree.iterparse(io.BytesIO(data), **options)
        for event, element in context:
            if not isinstance(element.tag, str):
                continue
            name = etree.QName(element).localname
            if event == "start":
                if root_name is None:
                    root_name = name
                if etree.QName(element).namespace:
                    namespaces[etree.QName(element).namespace] += 1
                identifier = next((value for key, value in element.attrib.items()
                                   if etree.QName(key).localname.lower() == "id"), None)
                if identifier is not None:
                    object_stack.append((element, identifier, name))
                continue

            counts[name] += 1
            for key, value in element.attrib.items():
                attr_name = etree.QName(key).localname.lower()
                if attr_name == "id":
                    identifiers[value].append(name)
                elif attr_name in {"ref", "versionref"}:
                    refs += 1
                    if len(reference_samples) < MAX_REFERENCE_SAMPLES:
                        reference_samples.append({
                            "source_object_id": object_stack[-1][1] if object_stack else None,
                            "source_object_type": object_stack[-1][2] if object_stack else name,
                            "reference_element": name, "attribute": attr_name, "value": value,
                        })
                    else:
                        references_truncated = True
            if object_stack and object_stack[-1][0] is element:
                object_stack.pop()
            parent = element.getparent()
            element.clear()
            if parent is not None:
                while element.getprevious() is not None:
                    del parent[0]
        if context.root is None:
            raise IntakeError("XML has no document element")
        if context.root.getroottree().docinfo.doctype:
            raise IntakeError("DTD and entity declarations are not accepted")
        duplicates = {identifier: types for identifier, types in sorted(identifiers.items()) if len(types) > 1}
        inventory = {
            "root_element": root_name,
            "namespace_counts": dict(sorted(namespaces.items())),
            "element_name_counts": dict(sorted(counts.items())),
            "identified_object_count": len(identifiers),
            "reference_attribute_count": refs,
            "reference_samples": sorted(reference_samples, key=lambda item: (
                item["source_object_type"] or "", item["reference_element"], item["attribute"], item["value"]
            )),
            "reference_samples_truncated": references_truncated,
            "duplicate_ids": duplicates,
        }
        if schema is None:
            return StreamInspection(inventory, (), None)

        validator = None
        try:
            validator = etree.iterparse(
                io.BytesIO(data), events=("end",), schema=schema,
                resolve_entities=False, no_network=True, load_dtd=False, huge_tree=False,
            )
            for _, element in validator:
                parent = element.getparent()
                element.clear()
                if parent is not None:
                    while element.getprevious() is not None:
                        del parent[0]
            errors = tuple(entry.message for entry in validator.error_log if entry.level_name in {"ERROR", "FATAL"})
            return StreamInspection(inventory, errors, not errors)
        except etree.XMLSyntaxError as exc:
            log = list(exc.error_log)
            if validator is not None:
                log.extend(validator.error_log)
            errors = tuple(dict.fromkeys(entry.message for entry in log if entry.level_name in {"ERROR", "FATAL"}))
            if not errors:
                errors = ("XSD validation failed",)
            return StreamInspection(inventory, errors, False)
    except IntakeError:
        raise
    except (etree.XMLSyntaxError, etree.LxmlError, OSError, ValueError) as exc:
        raise IntakeError("XML is not well formed or could not be inspected") from exc
