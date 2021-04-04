"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
import sys
from abc import ABC
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

import requests

# from database import DatabaseManager

# module scope
# db = DatabaseManager("bookmarks.db")


class Command(ABC):
    pass


@dataclass
class AddBookmarkCommand(Command):
    """
    This command is a dataclass that encapsulates a bookmark
    This uses type hints: https://docs.python.org/3/library/typing.html
    """

    id: int
    title: str
    url: str
    # data["date_added"] = datetime.utcnow().isoformat()
    date_added: str
    date_edited: str
    bookmark_notes: Optional[str] = None


@dataclass
class ListBookmarksCommand(Command):
    order_by: str
    order: str


@dataclass
class DeleteBookmarkCommand(Command):
    id: int


@dataclass
class EditBookmarkCommand(Command):
    id: int
    title: str
    url: str
    # data["date_added"] = datetime.utcnow().isoformat()
    date_added: str
    date_edited: str
    bookmark_notes: Optional[str] = None
