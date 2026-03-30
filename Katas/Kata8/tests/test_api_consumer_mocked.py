import sys
from pathlib import Path
from unittest.mock import Mock, patch

import requests


# Ensure `src` from Kata3 is importable (Katas/Kata3/src)
ROOT = Path(__file__).resolve().parents[2] / "Kata3"
sys.path.insert(0, str(ROOT / "src"))

import kata3_api_consumer as consumer


def make_response(status_code=200, json_data=None, text=""):
    resp = Mock()
    resp.status_code = status_code
    resp.text = text
    if json_data is None:
        json_data = {"observations": []}
    resp.json.return_value = json_data
    return resp


@patch("kata3_api_consumer.time.sleep", lambda *_: None)
def test_success_returns_response():
    resp200 = make_response(200, {"observations": [1, 2, 3]})

    with patch("kata3_api_consumer.requests.get", return_value=resp200) as mock_get:
        resp = consumer.fetch_fred_data_with_retry(
            "http://example", {"q": "x"}, max_retries=3
        )

    assert resp is resp200
    assert resp.status_code == 200
    mock_get.assert_called_once()


@patch("kata3_api_consumer.time.sleep", lambda *_: None)
def test_404_returns_without_retry():
    resp404 = make_response(404, json_data={"error": "not found"}, text="Not found")

    with patch("kata3_api_consumer.requests.get", return_value=resp404) as mock_get:
        resp = consumer.fetch_fred_data_with_retry("http://example", {}, max_retries=4)

    assert resp is resp404
    mock_get.assert_called_once()


@patch("kata3_api_consumer.time.sleep", lambda *_: None)
def test_5xx_retries_then_none():
    resp500 = make_response(500, json_data={"error": "server"}, text="Server error")

    with patch("kata3_api_consumer.requests.get", return_value=resp500) as mock_get:
        resp = consumer.fetch_fred_data_with_retry("http://example", {}, max_retries=3)

    # All attempts returned 5xx -> function should return None after exhausting retries
    assert resp is None
    assert mock_get.call_count == 3


@patch("kata3_api_consumer.time.sleep", lambda *_: None)
def test_exception_retries_then_none():
    # Simulate a network timeout on every attempt
    with patch(
        "kata3_api_consumer.requests.get", side_effect=requests.exceptions.Timeout()
    ) as mock_get:
        resp = consumer.fetch_fred_data_with_retry("http://example", {}, max_retries=3)

    assert resp is None
    assert mock_get.call_count == 3


@patch("kata3_api_consumer.time.sleep", lambda *_: None)
def test_retry_sequence_fail_then_success():
    resp500 = make_response(500)
    resp200 = make_response(200, {"observations": [42]})

    # First two calls fail (500), third succeeds
    sequence = [resp500, resp500, resp200]

    with patch("kata3_api_consumer.requests.get", side_effect=sequence) as mock_get:
        resp = consumer.fetch_fred_data_with_retry("http://example", {}, max_retries=5)

    assert resp is resp200
    assert mock_get.call_count == 3
