"""Input-only M04-A3b split sensitivity checks; never opens GTFS ZIP files."""

import itertools
import json
import unittest
from pathlib import Path


CORPUS = Path(__file__).resolve().parents[1] / "corpus"
KNOWN_EXPOSURE = {"002", "005", "014", "019", "020"}
ATOMIC_LINEAGE = {"013", "015"}


def load_inputs():
    inventory = json.loads((CORPUS / "inventory_v1.json").read_text(encoding="utf-8"))
    split = json.loads((CORPUS / "split_v1.json").read_text(encoding="utf-8"))
    rows = {row["dataset_id"]: row for row in inventory["datasets"]}
    size_order = sorted(inventory["datasets"], key=lambda row: (row["size_bytes"], row["dataset_id"]))
    bands = {
        row["dataset_id"]: "SMALL" if index < 7 else "MEDIUM" if index < 14 else "LARGE"
        for index, row in enumerate(size_order)
    }
    return rows, bands, split


def lineage_units(dataset_ids):
    return {"LINEAGE-013-015" if item in ATOMIC_LINEAGE else f"DATASET-{item}" for item in dataset_ids}


def candidate_rank(dataset_ids, rows, bands):
    selected = [rows[item] for item in dataset_ids]
    calendar_models = {tuple(key for key, present in row["calendar_model"].items() if present) for row in selected}
    shapes_states = {row["shape_presence"] for row in selected}
    feed_info_states = {"feed_info.txt" in row["tables_present"] for row in selected}
    tables = set().union(*(set(row["tables_present"]) for row in selected))
    ranges = [
        max(row["counts"][field] for row in selected) - min(row["counts"][field] for row in selected)
        for field in ("route_count", "stop_count", "trip_count")
    ]
    zip_range = max(row["size_bytes"] for row in selected) - min(row["size_bytes"] for row in selected)
    return (
        len(calendar_models), len(shapes_states), len(feed_info_states), len(tables),
        len({bands[item] for item in dataset_ids}), *ranges, zip_range, tuple(sorted(dataset_ids)),
    )


def best_scenario_b(rows, bands):
    eligible = [item for item in rows if item not in KNOWN_EXPOSURE]
    candidates = []
    for group in itertools.combinations(eligible, 6):
        selected = set(group)
        if selected & ATOMIC_LINEAGE != ATOMIC_LINEAGE or len(lineage_units(selected)) < 5:
            continue
        families = {rows[item]["family"].replace("FAMILY_", "")[0] for item in selected}
        if set("ABCD") <= families:
            candidates.append(tuple(sorted(selected)))
    return max(candidates, key=lambda ids: candidate_rank(ids, rows, bands)), len(candidates)


def best_scenario_c(rows, bands):
    eligible = [item for item in rows if item not in KNOWN_EXPOSURE | ATOMIC_LINEAGE]
    candidates = [tuple(group) for group in itertools.combinations(eligible, 5)]
    return max(candidates, key=lambda ids: candidate_rank(ids, rows, bands)), len(candidates)


class SplitSensitivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.bands, cls.split = load_inputs()

    def test_approved_split_counts_datasets_and_lineage_units_separately(self):
        holdout = {row["dataset_id"] for row in self.split["datasets"] if row["assignment"] == "HOLDOUT"}
        self.assertEqual(holdout, {"006", "008", "013", "015", "017", "018"})
        self.assertEqual(len(holdout), 6)
        self.assertEqual(len(lineage_units(holdout)), 5)
        self.assertEqual(self.split["status"], "APPROVED")

    def test_exhaustive_six_dataset_winner_is_stable_and_structurally_eligible(self):
        winner, candidate_count = best_scenario_b(self.rows, self.bands)
        self.assertEqual(winner, ("006", "008", "013", "015", "017", "018"))
        self.assertEqual(candidate_count, 375)
        self.assertEqual(len(lineage_units(winner)), 5)
        self.assertTrue(set("ABCD") <= {self.rows[item]["family"].replace("FAMILY_", "")[0] for item in winner})
        self.assertFalse(set(winner) & KNOWN_EXPOSURE)

    def test_exhaustive_five_independent_lineage_winner_keeps_pair_in_development(self):
        winner, candidate_count = best_scenario_c(self.rows, self.bands)
        self.assertEqual(winner, ("006", "008", "012", "017", "018"))
        self.assertEqual(candidate_count, 1287)
        self.assertEqual(len(lineage_units(winner)), 5)
        self.assertFalse(set(winner) & (KNOWN_EXPOSURE | ATOMIC_LINEAGE))

    def test_candidates_use_only_registered_input_metadata(self):
        self.assertEqual(self.split["review"]["reviewed_by"], "Yeison Arbey Carrillo Lemus")
        self.assertTrue(all("finding_count" not in row for row in self.rows.values()))


if __name__ == "__main__":
    unittest.main()
