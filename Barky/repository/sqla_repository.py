# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base_repository import BaseRepository
from .models import Base, BookmarkModel

class SQLARespository(BaseRepository):
    """
    Uses guidance from the basic SQLAlchemy 1.3 tutorial: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
    """

    def __init__(self, url=None) -> None:
        super().__init__()

        self.engine = None

        # create db connection
        if url != None:
            self.engine = create_engine(url)
        else:
            # let's default to in-memory for now
            self.engine = create_engine('sqlite:///:memory:', echo=True)

        # ensure tables are there
        Base.metadata.create_all(self.engine)

        # obtain session
        # the session is used for all transactions
        self.Session = sessionmaker(bind=self.engine)

    def add_one(self, bookmark: BookmarkModel) -> int:
        self.Session.add(bookmark)
        self.Session.commit()
        pass

    def add_many(self, bookmarks: list[BookmarkModel]) -> int:
        self.Session.add(bookmarks)
        pass

    def delete_one(self, bookmark) -> int:
        pass

    def delete_many(self, bookmarks) -> int:
        pass

    def update(self, bookmark) -> int:
        pass

    def update_many(self, bookmarks) -> int:
        pass

    def find_first(self, query) -> BookmarkModel:
        pass

    def find_all(self, query) -> list[BookmarkModel]:
        pass