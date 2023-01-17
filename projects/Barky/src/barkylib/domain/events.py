from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .models import Bookmark

# from database import DatabaseManager

# module scope
# db = DatabaseManager("bookmarks.db")


class Event(ABC):
    pass


@dataclass
class BookmarkAdded(Event):
    id: int
    title: str
    url: str
    date_added: str
    bookmark_notes: Optional[str] = None


@dataclass
class BookmarkEdited(Event):
    id: int
    title: str
    url: str
    date_edited: str
    bookmark_notes: Optional[str] = None


@dataclass
class BookmarksListed(Event):
    bookmarks: list[Bookmark]


@dataclass
class BookmarkDeleted(Event):
    bookmark: Bookmark


# @dataclass
# class BookmarksDeleted(Event):
#     bookmarks: list[Bookmark]
