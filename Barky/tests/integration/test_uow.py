import threading
import time
import traceback
from datetime import datetime, timezone
from typing import List
from unittest.mock import Mock
import pytest
from barkylib.domain.models import Bookmark
from barkylib.services import unit_of_work

# pytestmark = pytest.mark.usefixtures("mappers")

# self.id = id
# self.title = title
# self.url = url
# self.notes = notes
# self.date_added = date_added
# self.date_edited = date_edited
        
def insert_boomkark(session, title: str, url: str, date_added: str, date_edited: str, notes: str=None, ):
    session.execute(
        """
        INSERT INTO bookmarks (title, url, notes, date_added, date_edited) 
        VALUES (:title, :url, :notes, :date_added, :date_edited)
        """,
        dict(
            title=title, 
            url=url,
            notes=notes,
            date_added=date_added,
            date_edited=date_edited,
        ),
    )

def test_can_retreive_bookmark(sqlite_session_factory):
    session = sqlite_session_factory()
    nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)
    insert_boomkark(session, f"Test", f"http://example.com", nu.isoformat(), nu.isoformat())
    session.commit()

    bookmark: Bookmark = None

    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    with uow:
        bookmark = uow.bookmarks.get_by_title(f"Test")
        assert bookmark.title == f"Test"
        # uow.commit()

    # assert bookmark.title == f"Test"

