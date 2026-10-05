from __future__ import annotations

import unittest

from gtfs_lab.client_app import WindowsInstanceLock, classify_worker_exit


class WorkerExitClassificationTests(unittest.TestCase):
    def test_user_cancellation_wins_over_nonzero_return_code(self) -> None:
        self.assertEqual(classify_worker_exit(True, 1), "CANCELLED")

    def test_nonzero_return_without_cancellation_is_failure(self) -> None:
        self.assertEqual(classify_worker_exit(False, 1), "FAILED")

    def test_zero_return_without_cancellation_is_success(self) -> None:
        self.assertEqual(classify_worker_exit(False, 0), "SUCCEEDED")

    def test_cancellation_intent_also_wins_if_worker_races_to_zero(self) -> None:
        self.assertEqual(classify_worker_exit(True, 0), "CANCELLED")


class WindowsInstanceLockTests(unittest.TestCase):
    def test_rejects_duplicate_and_allows_restart_after_release(self) -> None:
        first = WindowsInstanceLock()
        second = None
        third = None
        try:
            self.assertTrue(first.acquired)
            second = WindowsInstanceLock()
            self.assertFalse(second.acquired)
            second.release()
            first.release()
            third = WindowsInstanceLock()
            self.assertTrue(third.acquired)
        finally:
            if second is not None:
                second.release()
            if third is not None:
                third.release()
            first.release()
if __name__ == "__main__":
    unittest.main()
