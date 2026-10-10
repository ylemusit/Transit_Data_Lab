from copy import deepcopy
import unittest

from tools.audit_assessment_v1 import conclusion, priority, project_coverage, validate_finding


def sample_finding(format="GTFS_SCHEDULE"):
    return {"contract": "TDL_ASSESSED_FINDING/1", "case_id": "EXAMPLE", "format": format,
            "condition": "Observed technical value", "criterion": {"reference": "Captured criterion"},
            "exposure": {"affected_count": 1, "eligible_count": 2, "unit": "ROWS", "basis": "Source rows"},
            "evidence": [{"source_ref": "source#row1"}], "observed_impact": {"state": "NOT_VERIFIED"},
            "potential_impact": {"state": "POTENTIAL_ONLY"}, "cause": {"state": "UNKNOWN"},
            "action": "Review the value", "closure": "New input and comparable check",
            "priority": {"value": "UNASSESSED"}, "destination_blocking": {"state": "NOT_DETERMINED"}}


class FindingTests(unittest.TestCase):
    def test_both_formats_allow_explicit_unknowns(self):
        for format in ("GTFS_SCHEDULE", "NETEX"): validate_finding(sample_finding(format))

    def test_confirmed_cause_without_evidence_rejected(self):
        finding = sample_finding(); finding["cause"]["state"] = "CONFIRMED"
        with self.assertRaises(ValueError): validate_finding(finding)

    def test_observed_impact_without_evidence_rejected(self):
        finding = sample_finding(); finding["observed_impact"]["state"] = "VERIFIED"
        with self.assertRaises(ValueError): validate_finding(finding)

    def test_affected_count_cannot_exceed_denominator(self):
        finding = sample_finding(); finding["exposure"]["affected_count"] = 3
        with self.assertRaises(ValueError): validate_finding(finding)

    def test_unknown_denominator_requires_reason(self):
        finding = sample_finding(); finding["exposure"]["eligible_count"] = None
        with self.assertRaises(ValueError): validate_finding(finding)
        finding["exposure"]["denominator_unknown_reason"] = "Source does not provide a population"
        validate_finding(finding)

    def test_priority_cannot_be_asserted_without_verified_impact(self):
        finding = sample_finding(); finding["priority"] = {"value": "HIGH", "evidence_ref": "statement"}
        with self.assertRaises(ValueError): validate_finding(finding)

    def test_destination_blocking_requires_evidence(self):
        finding = sample_finding(); finding["destination_blocking"]["state"] = "CONFIRMED"
        with self.assertRaises(ValueError): validate_finding(finding)

    def test_potential_impact_cannot_be_promoted_to_verified(self):
        finding = sample_finding(); finding["potential_impact"]["state"] = "VERIFIED"
        with self.assertRaises(ValueError): validate_finding(finding)

    def test_unknown_priority_level_rejected(self):
        finding = sample_finding(); finding["priority"]["value"] = "GREEN"
        with self.assertRaises(ValueError): validate_finding(finding)


class PriorityTests(unittest.TestCase):
    def context(self):
        return {"destination": "Example destination", "acceptance_criteria_ref": "acceptance.json",
                "target_date": "2026-10-15", "consequence_kind": "FUNCTIONAL_FAILURE",
                "consequence_evidence_ref": "reproduction.json"}

    def test_missing_context_remains_unassessed_even_with_large_counts(self):
        self.assertEqual(priority({"affected_rows": 1_000_000})["value"], "UNASSESSED")

    def test_unverified_impact_is_not_low_risk(self):
        context = self.context(); context["consequence_kind"] = "NOT_VERIFIED"
        self.assertEqual(priority(context)["value"], "UNASSESSED")

    def test_confirmed_functional_failure_has_proposed_high_priority(self):
        self.assertEqual(priority(self.context())["value"], "HIGH")

    def test_critical_needs_urgency_evidence(self):
        context = self.context(); context.update(consequence_kind="SERVICE_UNAVAILABLE", urgent_no_workaround=True)
        with self.assertRaises(ValueError): priority(context)
        context["urgency_evidence_ref"] = "service-window-review.json"
        self.assertEqual(priority(context)["value"], "CRITICAL")


class ConclusionTests(unittest.TestCase):
    def test_pass_plus_gap_does_not_mean_complete_pass(self):
        result = conclusion([{"rule_id": "A", "status": "PASS"}, {"rule_id": "B", "status": "NOT_EVALUABLE"}], {})
        self.assertEqual(result["technical_result"], "NO_NONCONFORMITY_DETECTED_WITH_COVERAGE_LIMITS")
        self.assertEqual(result["destination_suitability"], "NOT_DETERMINED_BY_TECHNICAL_COUNTS")

    def test_all_not_applicable_has_no_positive_result(self):
        result = conclusion([{"rule_id": "A", "status": "NOT_APPLICABLE"}], {})
        self.assertEqual(result["technical_result"], "NO_APPLICABLE_CONTROL_RESULT")

    def test_duplicate_control_projection_rejected(self):
        with self.assertRaises(ValueError): conclusion([{"rule_id": "A", "status": "PASS"}] * 2, {})

    def test_unknown_status_rejected(self):
        with self.assertRaises(ValueError): conclusion([{"rule_id": "A", "status": "GREEN"}], {})

    def test_failure_and_gap_retained_together(self):
        result = conclusion([{"rule_id": "A", "status": "FAIL_TECHNICAL"}, {"rule_id": "B", "status": "INSPECTION_ERROR"}], {})
        self.assertEqual(result["technical_result"], "NONCONFORMITIES_DETECTED_WITH_COVERAGE_LIMITS")


class CoverageTests(unittest.TestCase):
    def inputs(self):
        model = {"matrix": [{"rule_id": "TDL-G06-TRIP-TIME-ORDER-REVIEW", "status": "NOT_EVALUABLE", "coverage": {"not_evaluable": 1}}]}
        header = {"status": "NOT_EVALUABLE", "not_evaluable": [
            {"file": "stop_times.txt", "field": "stop_id", "reason": "CONDITION_UNKNOWN"},
            {"file": "stop_times.txt", "field": "stop_id", "reason": "CONDITION_UNKNOWN"}],
            "decisions": [], "conditional_rows_total": 1, "conditional_rows_truncated": False}
        review = {"deferred_rule_reviews": [{"rule_id": "TDL-G06-TRIP-TIME-ORDER-REVIEW", "reason": "Authority unresolved"}]}
        return model, {"g03": {"header_schema": header}}, review

    def test_annotations_are_grouped_without_creating_operator_findings(self):
        result = project_coverage(*self.inputs())
        self.assertEqual(result["new_operator_findings"], 0)
        header = result["non_evaluable_controls"][0]
        self.assertEqual(len(header["groups"]), 1)
        self.assertEqual(header["groups"][0]["annotations"], 2)
        self.assertEqual(header["alternative_status"], "PROPOSED_NOT_EXECUTED")

    def test_missing_authority_review_reason_rejected(self):
        args = self.inputs(); args[2]["deferred_rule_reviews"] = []
        with self.assertRaises(ValueError): project_coverage(*args)


if __name__ == "__main__":
    unittest.main()
