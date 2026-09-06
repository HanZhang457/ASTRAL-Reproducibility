import unittest

from astral.audit import validate_result_rows


def row(**changes):
    value = {
        "dataset": "Toy",
        "method": "ASTRAL-K",
        "seed": "0",
        "correct": "8",
        "test_count": "10",
        "accuracy": "0.8",
        "macro_f1": "0.75",
    }
    value.update(changes)
    return value


class AuditTests(unittest.TestCase):
    def test_rejects_duplicate_key(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_result_rows([row(), row()])

    def test_rejects_inconsistent_fraction(self):
        with self.assertRaisesRegex(ValueError, "mismatch"):
            validate_result_rows([row(accuracy="0.7")])


if __name__ == "__main__":
    unittest.main()
