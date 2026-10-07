from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from gtfs_lab.storage_paths import data_root


class StoragePathsTests(unittest.TestCase):
    def test_canonical_default(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(data_root(), Path("P:/TransitDataLab/02_Data"))

    def test_root_override(self):
        with patch.dict(os.environ, {"TDL_ROOT": "D:/TDL"}, clear=True):
            self.assertEqual(data_root(), Path("D:/TDL/02_Data"))

    def test_data_override_precedes_root(self):
        with patch.dict(os.environ, {"TDL_ROOT": "D:/TDL", "TDL_DATA_ROOT": "E:/Data"}, clear=True):
            self.assertEqual(data_root(), Path("E:/Data"))
