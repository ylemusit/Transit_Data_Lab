import unittest

from gtfs_lab.g03_condition_runtime import evaluate_presence_policy


class G03ConditionRuntime(unittest.TestCase):
    def test_unknown_followed_by_false_remains_unknown_with_ordered_trace(self):
        policy = {"default": "OPTIONAL", "rules": [
            {"effect": "REQUIRED", "when": {"op": "FIELD_VALUE_EQUALS", "field": "a", "value": "yes"}},
            {"effect": "OPTIONAL", "when": {"op": "FIELD_VALUE_EQUALS", "field": "b", "value": "yes"}},
        ]}
        result = evaluate_presence_policy(policy, {"b": "no"}, {"b"})
        self.assertEqual(("UNKNOWN", None), (result["truth"], result["effect"]))
        self.assertEqual(["UNKNOWN", "FALSE"], [item["truth"] for item in result["trace"]])

    def test_unknown_followed_by_unrelated_true_remains_unknown(self):
        policy = {"default": "UNKNOWN", "rules": [
            {"effect": "REQUIRED", "when": {"op": "FIELD_VALUE_EQUALS", "field": "a", "value": "yes"}},
            {"effect": "OPTIONAL", "when": {"op": "FIELD_VALUE_EQUALS", "field": "b", "value": "yes"}},
        ]}
        result = evaluate_presence_policy(policy, {"b": "yes"}, {"b"})
        self.assertEqual(("UNKNOWN", None), (result["truth"], result["effect"]))
        self.assertEqual(["UNKNOWN", "TRUE"], [item["truth"] for item in result["trace"]])

    def test_true_evidence_resolves_unknown_within_same_any_condition(self):
        policy = {"default": "UNKNOWN", "rules": [{"effect": "REQUIRED", "when": {
            "op": "ANY", "conditions": [
                {"op": "FIELD_VALUE_EQUALS", "field": "missing", "value": "yes"},
                {"op": "FIELD_VALUE_EQUALS", "field": "known", "value": "yes"},
            ]}}]}
        result = evaluate_presence_policy(policy, {"known": "yes"}, {"known"})
        self.assertEqual(("TRUE", "REQUIRED"), (result["truth"], result["effect"]))

    def test_nested_three_valued_all_any_not_and_independent_conditions(self):
        policy = {"default": "UNKNOWN", "rules": [{"effect": "REQUIRED", "when": {
            "op": "ALL", "conditions": [
                {"op": "ANY", "conditions": [
                    {"op": "FIELD_VALUE_EQUALS", "field": "a", "value": "yes"},
                    {"op": "FIELD_VALUE_EQUALS", "field": "b", "value": "yes"},
                ]},
                {"op": "NOT", "condition": {"op": "FIELD_VALUE_EQUALS", "field": "c", "value": "blocked"}},
            ]}}]}
        result = evaluate_presence_policy(policy, {"a": "no", "b": "yes", "c": "ok"}, {"a", "b", "c"})
        self.assertEqual(("TRUE", "REQUIRED"), (result["truth"], result["effect"]))
        self.assertEqual("ALL", result["trace"][0]["trace"][-1]["operator"])

    def test_repeated_missing_signal_can_be_resolved_by_later_same_signal_evidence(self):
        policy = {"default": "UNKNOWN", "rules": [
            {"effect": "REQUIRED", "when": {"op": "FIELD_VALUE_EQUALS", "field": "x", "value": "yes"}},
            {"effect": "OPTIONAL", "when": {"op": "FIELD_VALUE_EQUALS", "field": "x", "value": "no"}},
        ]}
        result = evaluate_presence_policy(policy, {"x": "no"}, {"x"})
        self.assertEqual("OPTIONAL", result["effect"])
        self.assertEqual(["FALSE", "TRUE"], [item["truth"] for item in result["trace"]])

    def test_required_for_location_types(self):
        policy = {"default": "OPTIONAL", "rules": [{
            "effect": "REQUIRED",
            "when": {"op": "FIELD_VALUE_IN", "field": "location_type", "values": ["0", "1", "2"]},
        }]}
        self.assertEqual("REQUIRED", evaluate_presence_policy(policy, {"location_type": "2"}, {"location_type"})["effect"])
        self.assertEqual("OPTIONAL", evaluate_presence_policy(policy, {"location_type": "3"}, {"location_type"})["effect"])

    def test_forbidden_precedes_required_policy(self):
        policy = {"default": "OPTIONAL", "rules": [
            {"effect": "FORBIDDEN", "when": {"op": "FIELD_VALUE_EQUALS", "field": "location_type", "value": "1"}},
            {"effect": "REQUIRED", "when": {"op": "FIELD_VALUE_IN", "field": "location_type", "values": ["2", "3", "4"]}},
        ]}
        self.assertEqual("FORBIDDEN", evaluate_presence_policy(policy, {"location_type": "1"}, {"location_type"})["effect"])
        self.assertEqual("REQUIRED", evaluate_presence_policy(policy, {"location_type": "3"}, {"location_type"})["effect"])

    def test_composite_condition_and_empty_value(self):
        policy = {"default": "OPTIONAL", "rules": [{
            "effect": "FORBIDDEN",
            "when": {"op": "ANY", "conditions": [
                {"op": "FIELD_VALUE_IN", "field": "location_type", "values": ["1", "2"]},
                {"op": "FIELD_VALUE_EQUALS", "field": "parent_station", "value": ""},
            ]},
        }]}
        result = evaluate_presence_policy(policy, {"location_type": "0", "parent_station": ""}, {"location_type", "parent_station"})
        self.assertEqual("FORBIDDEN", result["effect"])

    def test_unmatched_domain_value_stays_unknown(self):
        policy = {"default": "UNKNOWN", "rules": [{
            "effect": "REQUIRED",
            "when": {"op": "FIELD_VALUE_IN", "field": "transfer_type", "values": ["", "0", "1", "2", "3"]},
        }, {
            "effect": "OPTIONAL",
            "when": {"op": "FIELD_VALUE_IN", "field": "transfer_type", "values": ["4", "5"]},
        }]}
        result = evaluate_presence_policy(policy, {"transfer_type": "99"}, {"transfer_type"})
        self.assertEqual("UNKNOWN", result["truth"])
        self.assertIsNone(result["effect"])

    def test_missing_condition_signal_is_unknown(self):
        policy = {"default": "OPTIONAL", "rules": [{
            "effect": "REQUIRED", "when": {"op": "FIELD_VALUE_EQUALS", "field": "route_long_name", "value": ""},
        }]}
        result = evaluate_presence_policy(policy, {"route_short_name": "A"}, {"route_short_name"})
        self.assertEqual("UNKNOWN", result["truth"])
        self.assertIsNone(result["effect"])


if __name__ == "__main__":
    unittest.main()
