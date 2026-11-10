import unittest
from teudot.engine import classify

RULES = [{"id": "invoice", "label": "חשבונית", "keywords": ["חשבונית מס"],
          "number_pattern": r"מספר:\\s*(\\d+)", "filename": "{type}_{number}.pdf"}]

class TestRules(unittest.TestCase):
    def test_unknown_goes_to_review(self):
        self.assertTrue(classify(["other"], RULES).review)
    def test_ambiguous_number_goes_to_review(self):
        self.assertTrue(classify(["חשבונית מס", "מספר: 123", "מספר: 456"], RULES).review)
    def test_no_number_goes_to_review(self):
        self.assertTrue(classify(["חשבונית מס"], RULES).review)

if __name__ == "__main__":
    unittest.main()
