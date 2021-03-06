"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
from datetime import datetime
import sys

import requests

from database import DatabaseManager

# module scope
db = DatabaseManager("bookmarks.db")


class CreateBookmarksTableCommand:
    """
    uses the DatabaseManager to create the bookmarks table
    """

    def execute(self):
        db.create_table(
            "bookmarks",
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand:
    """
    This class will:

    1. Expect a dictionary containing the title, URL, and (optional) notes information for a bookmark.
    2. Add the current datetime to the dictionary as date_added.
    3. Insert the data into the bookmarks table using the DatabaseManager.add method.
    4. Return a success message that will eventually be displayed by the presentation layer.
    """

    def execute(self, data, timestamp=None):
        data["date_added"] = datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return "Bookmark added!"


class ListBookmarksCommand:
    """
    We need to review the bookmarks in the database.
    To do so, this class will:
    1. Accept the column to order by, and save it as an instance attribute.
    2. Pass this information along to db.select in its execute method.
    3. Return the result (using the cursor’s .fetchall() method) because select is a query.
    """

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self):
        return db.select("bookmarks", order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    """
    We also need to remove bookmarks.
    """

    def execute(self, data):
        db.delete("bookmarks", {"id": data})
        return "Bookmark deleted!"


class ImportGitHubStarsCommand:
    """
    Import starred repos in Github - credit Dane Hillard
    """
    def _extract_bookmark_info(self, repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data):
        bookmarks_imported = 0

        github_username = data["github_username"]
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"
        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            next_page_of_results = stars_response.links.get("next", {}).get("url")

            for repo_info in stars_response.json():
                repo = repo_info["repo"]

                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        repo_info["starred_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp,
                )

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class EditBookmarkCommand:
    def execute(self, data):
        db.update(
            "bookmarks",
            {"id": data["id"]},
            data["update"],
        )
        return "Bookmark updated!"


class QuitCommand:
    def execute(self):
        sys.exit()
