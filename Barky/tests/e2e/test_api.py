import pytest
import requests
from datetime import datetime, timezone

from .api_client import post_to_add_bookmark, get_bookmark_by_title
import pytest


@pytest.mark.usefixtures("restart_api")
def test_path_correct_returns_202_and_bookmark_added():

    nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

    title = f"Test"
    url = f"http://example.com"
    notes = f"good links"
    date_added = nu.isoformat()
    date_edited = nu.isoformat()

    post_to_add_bookmark(title, url, notes, date_added, date_edited)

    r = get_bookmark_by_title(title)
    assert r.ok
    assert r.json() == [
        {
            "title": title,
            "url": url,
            "notes": notes,
        },
    ]



@pytest.mark.usefixtures("restart_api")
def test_incorrect_path_returns_400_and_error_message():

    nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

    title: str = f"Test"
    url: str = f"http://example.com"
    notes: str = f"good links"
    date_added: str = nu.isoformat()
    date_edited: str = nu.isoformat()
    r = post_to_add_bookmark(title, url, notes, date_added, date_edited)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid title {title}"

    r = get_bookmark_by_title(title)
    assert r.status_code == 404
