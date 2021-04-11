import requests
from barkylib import config


def post_to_add_bookmark(
    title: str,
    url: str,
    notes: str,
    date_added: str,
    date_edited: str,
):
    url = config.get_api_url()

    # self.title = title
    # self.url = url
    # self.notes = notes
    # self.date_added = date_added
    # self.date_edited = date_edited

    r = requests.post(
        f"{url}/add_bookmark",
        json={
            "title": title,
            "url": url,
            "notes": notes,
            "date_added": date_added,
            "date_edited": date_edited,
        },
    )
    assert r.status_code == 201


def get_bookmark_by_title(title: str):
    url = config.get_api_url()
    return requests.get(f"{url}/bookmarks/{title}")
