import pytest
from datetime import datetime
from barkylib.adapters.repository import SqlAlchemyRepository
from barkylib.domain.models import Bookmark

pytestmark = pytest.mark.usefixtures("mappers")


def test_add_bookmark(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = SqlAlchemyRepository(session)
    b1 = Bookmark(
        id=1,
        title=f"Google.com",
        url=f"http://google.com",
        notes=f"Source of all truth",
        date_added=datetime(2023, 8, 12),
        date_edited=datetime(2023, 8, 12),
    )
    repo.add_one(b1)
    assert repo.get(b1.id) == b1
