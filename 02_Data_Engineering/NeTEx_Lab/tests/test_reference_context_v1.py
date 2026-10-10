from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from netex_lab.reference_context_v1 import audit_reference_context


def xml(target: str, *, version: str | None = "1.0") -> bytes:
    version_attr = f' version="{version}"' if version is not None else ""
    version_ref = f' versionRef="{version}"' if version is not None else ""
    return f'''<PublicationDelivery xmlns="http://www.netex.org.uk/netex">
      <ResourceFrame id="frame:1"><ScheduledStopPoint id="{target}"{version_attr}/>
        <ScheduledStopPointRef ref="{target}"{version_ref}/>
      </ResourceFrame>
    </PublicationDelivery>'''.encode("utf-8")


class ReferenceContextTests(unittest.TestCase):
    def test_exact_typed_versioned_local_target_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "valid.xml"
            source.write_bytes(xml("stop:1"))
            result = audit_reference_context(source)
        self.assertEqual("PASS", result["rule"]["status"])
        self.assertEqual("PASS", result["findings"][0]["status"])

    def test_missing_target_is_unknown_until_closed_scope_is_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "partial.xml"
            source.write_bytes(b'''<PublicationDelivery xmlns="http://www.netex.org.uk/netex">
              <ResourceFrame id="frame:1"><ScheduledStopPointRef ref="stop:missing" versionRef="1.0"/></ResourceFrame>
            </PublicationDelivery>''')
            partial = audit_reference_context(source)
            closed = audit_reference_context(source, closed_scope=True)
        self.assertEqual("NOT_EVALUABLE", partial["findings"][0]["status"])
        self.assertFalse(partial["rule"]["closed_scope_effective"])
        self.assertEqual("HUMAN_REVIEW_REQUIRED", closed["findings"][0]["status"])
        self.assertTrue(closed["rule"]["closed_scope_effective"])

    def test_version_mismatch_requires_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "version.xml"
            source.write_bytes(b'''<PublicationDelivery xmlns="http://www.netex.org.uk/netex">
              <ResourceFrame id="frame:1"><ScheduledStopPoint id="stop:1" version="2.0"/>
                <ScheduledStopPointRef ref="stop:1" versionRef="1.0"/>
              </ResourceFrame></PublicationDelivery>''')
            result = audit_reference_context(source)
        self.assertEqual("HUMAN_REVIEW_REQUIRED", result["findings"][0]["status"])

    def test_reference_can_resolve_across_members_in_supplied_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "package.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("a-reference.xml", b'''<PublicationDelivery xmlns="http://www.netex.org.uk/netex">
                  <ResourceFrame id="frame:2"><ScheduledStopPointRef ref="stop:1" versionRef="1.0"/></ResourceFrame>
                </PublicationDelivery>''')
                archive.writestr("b-target.xml", b'''<PublicationDelivery xmlns="http://www.netex.org.uk/netex">
                  <ResourceFrame id="frame:1"><ScheduledStopPoint id="stop:1" version="1.0"/></ResourceFrame>
                </PublicationDelivery>''')
            result = audit_reference_context(source, closed_scope=True)
        self.assertEqual("PASS", result["rule"]["status"])
        self.assertEqual(2, result["dataset_identity"]["member_count"])

    def test_no_supported_reference_shape_is_not_misreported_as_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "no-refs.xml"
            source.write_bytes(b'<PublicationDelivery><ResourceFrame id="frame:1"/></PublicationDelivery>')
            result = audit_reference_context(source)
        self.assertEqual("NOT_EVALUABLE", result["rule"]["status"])
        self.assertEqual(0, result["rule"]["reference_count"])


if __name__ == "__main__":
    unittest.main()
