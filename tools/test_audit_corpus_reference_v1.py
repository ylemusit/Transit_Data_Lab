"""Source-governance and authored-bank acceptance tests for 09/14."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from tools.audit_corpus_v1 import ROOT, read, sha, verify_sources, change_impact, reviewed_revision
from tools.audit_reference_bank_v1 import validate_bank
from tools.audit_reference_facts_v1 import gtfs_state
from tools.audit_reference_bank_v1 import archive_feed
from tools.audit_reference_definitions_v1 import case_data

OUTPUT=ROOT/"reports/audit_reference_bank_v1/accepted_reference_20261009_v1"


class Governance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.registry=read(OUTPUT/"SOURCE_REGISTRY.json");cls.criteria=read(OUTPUT/"CRITERIA.json")
    def test_identified_sources(self):
        result=verify_sources(self.registry)
        self.assertEqual(result["identified_files"],44);self.assertEqual(result["missing_sources"],["NETEX-EPIP-2026"])
        self.assertFalse(result["external_distribution_approved"])
    def test_no_change(self):self.assertEqual(change_impact(self.registry,self.registry,self.criteria)["decision"],"NO_CHANGE_IDENTIFIED")
    def test_content_change(self):
        candidate=deepcopy(self.registry);candidate["sources"][0]["sha256"]="0"*64
        result=change_impact(self.registry,candidate,self.criteria)
        self.assertEqual(len([i for i in result["affected_criterion_ids"] if i.startswith("GTFS") or i.startswith("TDL-G") or i=="V1-RULE-GTFS"]),32)
        self.assertFalse(result["baseline_promoted"])
        with self.assertRaises(ValueError):verify_sources(candidate)
    def test_version_change_without_byte_change(self):
        candidate=deepcopy(self.registry);candidate["sources"][0]["version"]="candidate/2"
        self.assertEqual(change_impact(self.registry,candidate,self.criteria)["decision"],"REVIEW_REQUIRED")
    def test_licence_change_cascades(self):
        candidate=deepcopy(self.registry);next(s for s in candidate["sources"] if s["source_id"]=="GTFS-LICENSE")["version"]="Changed licence notice"
        result=change_impact(self.registry,candidate,self.criteria)
        self.assertIn("GTFS-FIXED",result["affected_source_ids"])
        self.assertIn("GTFS-G03-FIELD-TYPE",result["affected_criterion_ids"])
    def test_orphan_licence(self):
        candidate=deepcopy(self.registry);candidate["sources"][0]["rights"]["evidence_source_ids"]=["UNKNOWN"]
        with self.assertRaises(ValueError):verify_sources(candidate)
    def test_unknown_rights_remain_unknown(self):
        legal=next(s for s in self.registry["sources"] if s["source_id"]=="EU-GDPR")
        self.assertEqual(legal["rights"]["state"],"UNKNOWN")
        self.assertFalse(legal["validity"]["fresh_legal_verification_in_this_task"])
    def test_missing_authority(self):
        candidate=deepcopy(self.registry);candidate["sources"][0].pop("authority")
        with self.assertRaises(ValueError):verify_sources(candidate)
    def test_no_automatic_promotion(self):
        candidate=deepcopy(self.registry);candidate["engine_baselines_modified"]=True
        with self.assertRaises(ValueError):verify_sources(candidate)
    def test_unreviewed_revision_rejected(self):
        candidate=deepcopy(self.registry);candidate["sources"][0]["version"]="candidate/2";candidate["revision"]="V2"
        with self.assertRaises(ValueError):reviewed_revision(self.registry,candidate,self.criteria,{})
    def test_scoped_review_creates_new_revision(self):
        candidate=deepcopy(self.registry);candidate["sources"][0]["version"]="candidate/2";candidate["revision"]="V2"
        impact=change_impact(self.registry,candidate,self.criteria)
        evidence="reports/audit_assessment_v1/PRIORITY_AND_CONCLUSION_METHOD.md"
        review={"reviewer":"SYNTHETIC_TEST_REVIEWER","rationale":"Synthetic approval tests chaining only; not a real corpus approval.",
                "evidence_ref":evidence,"evidence_sha256":sha(ROOT/evidence),"criterion_ids":impact["affected_criterion_ids"],"decision":"APPROVED_INTERNAL_REFERENCE"}
        result=reviewed_revision(self.registry,candidate,self.criteria,review)
        self.assertEqual(result["predecessor_revision"],self.registry["revision"])
        self.assertNotIn("predecessor_revision",self.registry)
        review["criterion_ids"]=[]
        with self.assertRaises(ValueError):reviewed_revision(self.registry,candidate,self.criteria,review)


class Bank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.bank=read(OUTPUT/"REFERENCE_BANK.json");cls.criteria=read(OUTPUT/"CRITERIA.json");cls.registry=read(OUTPUT/"SOURCE_REGISTRY.json")
    def reject(self,change):
        bank=deepcopy(self.bank);change(bank)
        with self.assertRaises(ValueError):validate_bank(bank,self.criteria,self.registry)
    def test_all_current_rules_represented(self):
        result=validate_bank(self.bank,self.criteria,self.registry)
        self.assertEqual(result["cases"],114);self.assertEqual(result["current_rules_represented"],36)
    def test_duplicate_case(self):self.reject(lambda b:b["cases"].append(deepcopy(b["cases"][0])))
    def test_orphan(self):self.reject(lambda b:b["cases"][0].update(criterion_id="UNKNOWN"))
    def test_changed_fixture(self):self.reject(lambda b:b["cases"][0].update(sha256="0"*64))
    def test_unsafe_fixture(self):self.reject(lambda b:b["cases"][0].update(fixture="../outside.zip"))
    def test_missing_rule(self):self.reject(lambda b:b.update(cases=[c for c in b["cases"] if c["criterion_id"]!="GTFS-G03-FIELD-TYPE"]))
    def test_engine_output_not_reference(self):self.reject(lambda b:b["cases"][0]["expected"].update(engine_observed_status="PASS"))
    def test_unknown_not_pass(self):
        self.reject(lambda b:next(c for c in b["cases"] if c["expected"]["criterion_state"]=="UNKNOWN")["expected"].update(criterion_status="PASS"))
    def test_recommendation_not_error(self):
        self.reject(lambda b:next(c for c in b["cases"] if c["criterion_id"].startswith("GTFS-G08"))["expected"].update(criterion_status="FAIL_TECHNICAL"))
    def test_profile_not_conformance(self):
        self.reject(lambda b:next(c for c in b["cases"] if c["criterion_id"]=="NETEX-PROFILE-001")["expected"].update(criterion_state="SATISFIED",criterion_status="PASS"))
    def test_missing_rationale(self):self.reject(lambda b:b["cases"][0]["expected"].update(rationale=""))
    def test_missing_origin(self):self.reject(lambda b:b["cases"][0].pop("origin"))
    def test_contradictory_expected_status(self):self.reject(lambda b:b["cases"][0]["expected"].update(criterion_status="FAIL_TECHNICAL"))
    def test_duplicate_criterion(self):
        with self.assertRaises(ValueError):validate_bank(self.bank,self.criteria+[self.criteria[0]],self.registry)
    def test_unsourced_criterion(self):
        criteria=deepcopy(self.criteria);criteria[0]["source_ids"]=["UNKNOWN"]
        with self.assertRaises(ValueError):validate_bank(self.bank,criteria,self.registry)
    def test_color_empty_and_space(self):
        with tempfile.TemporaryDirectory(prefix="tdl_fact_") as temporary:
            path=Path(temporary)/"case.zip"
            for variant, expected in [("negative","VIOLATED"),("boundary","SATISFIED")]:
                data,raw,context=case_data("color",variant);archive_feed(path,data,raw)
                self.assertEqual(gtfs_state({"context":context},path,"color"),expected)
    def test_strict_frequency_end_boundary(self):
        with tempfile.TemporaryDirectory(prefix="tdl_fact_") as temporary:
            path=Path(temporary)/"case.zip"
            for variant, expected in [("negative","VIOLATED"),("boundary","SATISFIED")]:
                data,raw,context=case_data("frequency_end",variant);archive_feed(path,data,raw)
                self.assertEqual(gtfs_state({"context":context},path,"frequency_end"),expected)


if __name__=="__main__":unittest.main()
