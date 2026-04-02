import unittest

from pipeline.reporting import build_run_summary


class TestReporting(unittest.TestCase):
    def test_build_run_summary_lists_flagged_periods(self):
        summary = build_run_summary(
            live_mode=False,
            series_id="GDPC1",
            observation_start="2020-01-01",
            observation_end="2022-01-01",
            raw_payload={"observations": [{"date": "2021-01-01", "value": "100"}]},
            transformed_rows=[
                {
                    "date": "2021-04-01",
                    "qoq_pct_change": -1.25,
                    "yoy_pct_change": None,
                    "signal_flag": True,
                    "signal_reasons": ["negative_qoq_growth"],
                }
            ],
            raw_file="data/raw/gdp_raw.json",
            transformed_file="data/transformed/gdp_transformed.json",
        )

        self.assertIn("# Pipeline Run Summary", summary)
        self.assertIn("Flagged periods: 1", summary)
        self.assertIn("negative_qoq_growth", summary)


if __name__ == "__main__":
    unittest.main()
