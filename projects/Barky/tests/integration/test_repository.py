import pytest
from barkylib.adapters.repository import SqlAlchemyRepository
from barkylib.domain.models import Bookmark

pytestmark = pytest.mark.usefixtures("mappers")


def test_add_bookmark(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = SqlAlchemyRepository(session)
    b1 = Bookmark(
        id="1",
        title="Google.com",
        url="http://google.com",
        notes="Source of all truth",
        date_added="2023/8/12",
        date_edited="",
    )
    repo.add(b1)
    assert repo.get(b1.id) == b1
