import unittest

from diff_whitespace_gate import evaluate_output


class DiffWhitespaceGateTests(unittest.TestCase):
    def test_no_findings_passes(self):
        self.assertTrue(evaluate_output("", 0)[0])

    def test_exact_historical_findings_pass_with_exception(self):
        output = (
            "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:3: trailing whitespace.\n"
            "+**Proyecto:** Transit Data Lab  \n"
            "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:4: trailing whitespace.\n"
            "+**Fecha base:** 2026-09-28  \n"
        )
        passed, accepted, message = evaluate_output(output, 2)
        self.assertTrue(passed)
        self.assertEqual(
            accepted,
            [
                "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:3",
                "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:4",
            ],
        )
        self.assertIn("PASS_WITH_DOCUMENTED_EXCEPTION", message)

    def test_additional_file_fails(self):
        output = "README.md:7: trailing whitespace.\n+bad  \n"
        self.assertFalse(evaluate_output(output, 2)[0])

    def test_other_matrix_line_fails(self):
        output = "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:5: trailing whitespace.\n+bad  \n"
        self.assertFalse(evaluate_output(output, 2)[0])

    def test_absent_historical_findings_pass(self):
        self.assertTrue(evaluate_output("", 0)[0])


if __name__ == "__main__":
    unittest.main()
