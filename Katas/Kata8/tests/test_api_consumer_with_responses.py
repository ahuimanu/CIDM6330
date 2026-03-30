import sys
from pathlib import Path

import responses


# Ensure `src` from Kata3 is importable (Katas/Kata3/src)
ROOT = Path(__file__).resolve().parents[2] / "Kata3"
sys.path.insert(0, str(ROOT / "src"))

import kata3_api_consumer as consumer


BASE = "http://example.com/data"


@responses.activate
def test_responses_success():
    responses.add(responses.GET, BASE, json={"observations": [1, 2]}, status=200)

    resp = consumer.fetch_fred_data_with_retry(BASE, {}, max_retries=2)

    assert resp is not None
    assert resp.status_code == 200
    assert resp.json()["observations"] == [1, 2]


@responses.activate
def test_responses_retry_sequence_then_success():
    # First two responses are 500, third is 200
    responses.add(responses.GET, BASE, status=500)
    responses.add(responses.GET, BASE, status=500)
    responses.add(responses.GET, BASE, json={"observations": [99]}, status=200)

    resp = consumer.fetch_fred_data_with_retry(BASE, {}, max_retries=5)

    assert resp is not None
    assert resp.status_code == 200
    assert resp.json()["observations"] == [99]
