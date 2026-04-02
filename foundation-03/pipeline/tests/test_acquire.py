import unittest
from unittest.mock import patch

from pipeline.acquire import fetch_gdp_observations


class TestAcquire(unittest.TestCase):
    def test_fetch_sample_payload(self):
        payload = fetch_gdp_observations(use_live=False)
        self.assertIn("observations", payload)
        self.assertGreater(len(payload["observations"]), 0)
        self.assertEqual(payload["metadata"]["source"], "sample")

    @patch("pipeline.acquire.sleep")
    @patch("pipeline.acquire.urlopen")
    @patch("pipeline.acquire.FRED_API_KEY", "test-key")
    @patch("pipeline.acquire.FRED_MAX_RETRIES", 1)
    @patch("pipeline.acquire.FRED_FALLBACK_TO_SAMPLE_ON_ERROR", True)
    def test_live_fetch_falls_back_to_sample_after_retry(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = TimeoutError("timed out")

        payload = fetch_gdp_observations(use_live=True, series_id="GDPC1")

        self.assertEqual(payload["metadata"]["source"], "sample_fallback")
        self.assertIn("fallback_reason", payload["metadata"])
        self.assertEqual(mock_urlopen.call_count, 2)
        mock_sleep.assert_called_once()


if __name__ == "__main__":
    unittest.main()
