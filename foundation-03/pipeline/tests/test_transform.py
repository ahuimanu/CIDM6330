import unittest

from pipeline.transform import transform_observations


class TestTransform(unittest.TestCase):
    def test_transform_filters_invalid_rows_and_adds_derived_metrics(self):
        raw = {
            "observations": [
                {"date": "2021-04-01", "value": "105"},
                {"date": "2021-01-01", "value": "100"},
                {"date": "2021-07-01", "value": "."},
                {"date": "2022-01-01", "value": "90"},
                {"date": "2021-10-01", "value": "95"},
                {"date": "2021-01-01", "value": "999"},
                {"date": None, "value": "200"},
                {"date": "2022-04-01", "value": "89"},
                {"date": "2022-07-01", "value": "abc"},
            ]
        }

        rows = transform_observations(raw)
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["date"], "2021-01-01")
        self.assertEqual(rows[0]["gdp_level"], 100.0)
        self.assertIsNone(rows[0]["qoq_pct_change"])
        self.assertAlmostEqual(rows[1]["qoq_pct_change"], 5.0)
        self.assertAlmostEqual(rows[3]["qoq_pct_change"], -5.2632, places=4)
        self.assertIsNone(rows[3]["rolling_4q_change"])
        self.assertAlmostEqual(rows[4]["rolling_4q_change"], -11.0, places=4)
        self.assertAlmostEqual(rows[4]["yoy_pct_change"], -11.0, places=4)
        self.assertTrue(rows[3]["signal_flag"])
        self.assertIn("negative_qoq_growth", rows[3]["signal_reasons"])

    def test_transform_marks_growth_slowdown_without_negative_growth(self):
        raw = {
            "observations": [
                {"date": "2021-01-01", "value": "100"},
                {"date": "2021-04-01", "value": "110"},
                {"date": "2021-07-01", "value": "115"},
            ]
        }

        rows = transform_observations(raw)
        self.assertFalse(rows[1]["signal_flag"])
        self.assertTrue(rows[2]["signal_flag"])
        self.assertIn("growth_slowdown", rows[2]["signal_reasons"])


if __name__ == "__main__":
    unittest.main()
