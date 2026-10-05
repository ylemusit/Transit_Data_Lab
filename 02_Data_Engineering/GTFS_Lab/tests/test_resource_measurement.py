import tempfile
import unittest
import os
from pathlib import Path

from tools.resource_measurement import _active_stage, _tree_bytes, measure


class ResourceMeasurementTests(unittest.TestCase):
    def test_measures_successful_child_and_output_growth(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "out"
            temp = root / "tmp"
            output.mkdir()
            result = measure(
                ["python", "-c", "import os; from pathlib import Path; Path(r'" + str(output / "x") + "').write_text('123'); Path(os.environ['TEMP'], 'temp.bin').write_bytes(b'1234')"],
                output_dir=output,
                temp_dir=temp,
                interval=0.05,
            )
            self.assertEqual(result["return_code"], 0)
            self.assertEqual(result["output_tree_bytes_delta"], 3)
            self.assertEqual(result["temp_tree_bytes_delta"], 4)
            self.assertIn(result["measurements"]["descendant_processes"], {"NOT_CAPTURED", "OBSERVED_SAMPLED"})

    @unittest.skipUnless(os.name == "nt", "Windows process-tree telemetry")
    def test_samples_descendant_process_tree(self):
        child = "import time; time.sleep(0.7)"
        parent = "import subprocess,sys,time; p=subprocess.Popen([sys.executable,'-c'," + repr(child) + "]); time.sleep(0.9); p.wait()"
        result = measure(["python", "-c", parent], interval=0.05)
        self.assertEqual(result["return_code"], 0)
        self.assertTrue(result["measurements"]["aggregate_process_tree_private_memory"].startswith("OBSERVED"))
        self.assertTrue(any(pid != result["root_pid"] for sample in result["samples"]
                            for pid in sample["descendant_pids"]))
        self.assertTrue(result["measurements"]["root_process_end_time"].startswith("OBSERVED"))

    def test_correlates_samples_with_stage_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_file = Path(tmp) / "stages.jsonl"
            code = ("import os,time,json; from pathlib import Path; p=Path(os.environ['TDL_RESOURCE_STAGE_FILE']); "
                    "p.write_text(json.dumps({'timestamp_utc':'2026-01-01T00:00:00+00:00','stage':'CONTROL','state':'START'})+'\\n'); "
                    "time.sleep(.16); p.open('a').write(json.dumps({'timestamp_utc':'2026-01-01T00:00:01+00:00','stage':'CONTROL','state':'END'})+'\\n')")
            result = measure(["python", "-c", code], stage_file=stage_file, interval=0.02)
            self.assertGreater(result["stage_resource_profile"]["CONTROL"]["sample_count"], 0)
            self.assertEqual(result["stage_resource_profile"]["CONTROL"]["classification"], "OBSERVED_SAMPLED")

    def test_nested_stage_markers_restore_the_parent_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_file = Path(tmp) / "stages.jsonl"
            stage_file.write_text(
                '{"stage":"REPORT_GENERATION","state":"START"}\n'
                '{"stage":"JSON_SERIALIZATION","state":"START"}\n'
                '{"stage":"JSON_SERIALIZATION","state":"END"}\n',
                encoding="utf-8",
            )
            self.assertEqual(_active_stage(stage_file), "REPORT_GENERATION")

    def test_failed_child_is_recorded(self):
        result = measure(["python", "-c", "raise SystemExit(7)"], interval=0.05)
        self.assertEqual(result["return_code"], 7)
        self.assertEqual(result["measurements"]["disk_usage_before_after"], "OBSERVED")

    def test_environment_overrides_are_scoped_to_child(self):
        before = os.environ.get("TDL_RESOURCE_TEST_VALUE")
        result = measure(["python", "-c", "import os; raise SystemExit(0 if os.environ.get('TDL_RESOURCE_TEST_VALUE') == 'child-only' else 1)"],
                         env_overrides={"TDL_RESOURCE_TEST_VALUE": "child-only"}, interval=0.05)
        self.assertEqual(result["return_code"], 0)
        self.assertEqual(os.environ.get("TDL_RESOURCE_TEST_VALUE"), before)

    def test_tree_bytes_missing_path_is_not_captured(self):
        self.assertIsNone(_tree_bytes(None))


if __name__ == "__main__":
    unittest.main()
