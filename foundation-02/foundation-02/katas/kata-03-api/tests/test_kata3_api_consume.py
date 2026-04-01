import sys
from pathlib import Path
from unittest.mock import call, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import kata3_api_consume as client

requests = client.requests


class FakeResponse:
    def __init__(self, status_code=200, payload=None, json_error=None):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}
        self._json_error = json_error

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}", response=self)

    def json(self):
        if self._json_error is not None:
            raise self._json_error
        return self._payload


@patch("kata3_api_consume.requests.get")
def test_request_with_backoff_success_returns_mocked_payload(mock_get):
    mock_get.return_value = FakeResponse(
        200,
        {"observations": [{"date": "2026-01-01", "value": "1.0"}], "count": 1},
    )

    payload = client.request_with_backoff(
        params={"series_id": "GDP", "api_key": "test-key"},
        retries=2,
        timeout_seconds=9,
    )

    assert payload["count"] == 1
    mock_get.assert_called_once_with(
        client.BASE_URL,
        params={"series_id": "GDP", "api_key": "test-key"},
        timeout=9,
    )


@patch("kata3_api_consume.requests.get")
def test_request_with_backoff_raises_on_mocked_404(mock_get):
    mock_get.return_value = FakeResponse(404, {"error": "Not Found"})

    with pytest.raises(RuntimeError, match="Request failed"):
        client.request_with_backoff(
            params={"series_id": "GDP", "api_key": "test-key"},
            retries=0,
        )

    mock_get.assert_called_once()


@patch("kata3_api_consume.time.sleep")
@patch("kata3_api_consume.random.uniform", return_value=0.0)
@patch("kata3_api_consume.requests.get")
def test_request_with_backoff_retries_transient_500_then_succeeds(
    mock_get, mock_uniform, mock_sleep
):
    mock_get.side_effect = [
        FakeResponse(500, {"error": "server"}),
        FakeResponse(200, {"observations": [{"date": "2026-01-01"}], "count": 1}),
    ]

    payload = client.request_with_backoff(
        params={"series_id": "GDP", "api_key": "test-key"},
        retries=2,
        backoff_base_seconds=0.5,
    )

    assert payload["count"] == 1
    assert mock_get.call_count == 2
    mock_uniform.assert_called_once()
    mock_sleep.assert_called_once_with(0.5)


@patch("kata3_api_consume.time.sleep")
@patch("kata3_api_consume.random.uniform", return_value=0.0)
@patch("kata3_api_consume.requests.get")
def test_request_with_backoff_retries_timeout_then_succeeds(
    mock_get, _mock_uniform, mock_sleep
):
    mock_get.side_effect = [
        requests.Timeout("timed out"),
        FakeResponse(200, {"observations": [], "count": 0}),
    ]

    payload = client.request_with_backoff(
        params={"series_id": "GDP", "api_key": "test-key"},
        retries=1,
        backoff_base_seconds=0.25,
    )

    assert payload == {"observations": [], "count": 0}
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(0.25)


@patch("kata3_api_consume.request_with_backoff")
def test_fetch_all_observations_collects_pages_offline(mock_request):
    mock_request.side_effect = [
        {
            "count": 3,
            "observations": [
                {"date": "2026-01-01", "value": "1.0"},
                {"date": "2026-01-02", "value": "2.0"},
            ],
        },
        {
            "count": 3,
            "observations": [{"date": "2026-01-03", "value": "3.0"}],
        },
    ]

    rows = client.fetch_all_observations(
        api_key="test-key",
        series_id="GDP",
        page_size=2,
    )

    assert [row["date"] for row in rows] == [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
    ]
    assert mock_request.call_args_list == [
        call(
            params={
                "api_key": "test-key",
                "series_id": "GDP",
                "file_type": "json",
                "sort_order": "asc",
                "limit": "2",
                "offset": "0",
            }
        ),
        call(
            params={
                "api_key": "test-key",
                "series_id": "GDP",
                "file_type": "json",
                "sort_order": "asc",
                "limit": "2",
                "offset": "2",
            }
        ),
    ]


@patch("kata3_api_consume.request_with_backoff")
def test_fetch_all_observations_stops_at_max_pages(mock_request):
    mock_request.side_effect = [
        {
            "count": 5,
            "observations": [
                {"date": "2026-01-01", "value": "1.0"},
                {"date": "2026-01-02", "value": "2.0"},
            ],
        },
        {
            "count": 5,
            "observations": [
                {"date": "2026-01-03", "value": "3.0"},
                {"date": "2026-01-04", "value": "4.0"},
            ],
        },
    ]

    rows = client.fetch_all_observations(
        api_key="test-key",
        series_id="GDP",
        page_size=2,
        max_pages=1,
    )

    assert len(rows) == 2
    mock_request.assert_called_once()


@patch(
    "kata3_api_consume.requests.get",
    side_effect=AssertionError("real network call attempted"),
)
def test_mock_is_required_and_real_network_would_fail(mock_get):
    with pytest.raises(AssertionError, match="real network call attempted"):
        client.request_with_backoff(
            params={"series_id": "GDP", "api_key": "test-key"},
            retries=0,
        )

    mock_get.assert_called_once()


@patch("kata3_api_consume.time.time", return_value=1_700_000_000)
def test_save_output_writes_expected_json(mock_time, tmp_path):
    output_path = tmp_path / "output" / "gdp.json"
    rows = [{"date": "2026-01-01", "value": "1.0"}]

    client.save_output(output_path, "GDP", rows)

    saved = output_path.read_text(encoding="utf-8")
    assert '"series_id": "GDP"' in saved
    assert '"record_count": 1' in saved
    assert '"fetched_at_unix": 1700000000' in saved
    mock_time.assert_called_once()
