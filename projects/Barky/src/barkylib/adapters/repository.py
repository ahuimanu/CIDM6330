from abc import ABC, abstractmethod

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List, Set

from barkylib.adapters import orm
from barkylib.domain.models import Base, Bookmark


class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()

    def add(self, bookmark: Bookmark):
        self._add(bookmark)

    def get(self, title: str):
        bookmark = self._get(title)

        if bookmark:
            self.seen.add(bookmark)

        return bookmark

    @abstractmethod
    def _add(self, bookmark: Bookmark):
        raise NotImplementedError

    @abstractmethod
    def _get(self, title) -> Bookmark:
        raise NotImplementedError

    @abstractmethod
    def _edit(self, bookmark: Bookmark):
        found = self.get(bookmark.title)
        if found:
            pass

    # @abstractmethod
    def add_one(bookmark) -> int:
        raise NotImplementedError("Derived classes must implement add_one")

    # @abstractmethod
    def add_many(bookmarks) -> int:
        raise NotImplementedError("Derived classes must implement add_many")

    # @abstractmethod
    def delete_one(bookmark) -> int:
        raise NotImplementedError("Derived classes must implement delete_one")

    # @abstractmethod
    def delete_many(bookmarks) -> int:
        raise NotImplementedError("Derived classes must implement delete_many")

    # @abstractmethod
    def update(bookmark) -> int:
        raise NotImplementedError("Derived classes must implement update")

    # @abstractmethod
    def update_many(bookmarks) -> int:
        raise NotImplementedError("Derived classes must implement update_many")

    # @abstractmethod
    def find_first(query) -> Bookmark:
        raise NotImplementedError("Derived classes must implement find_first")

    # @abstractmethod
    def find_all(query) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement find_all")


# sqlalchemy stuff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlAlchemyRepository(AbstractRepository):
    """
    Uses guidance from the basic SQLAlchemy 2.0 tutorial:
    https://docs.sqlalchemy.org/en/20/tutorial/index.html
    """

    def __init__(self, url=None) -> None:
        super().__init__()

        self.engine = None

        # create db connection
        if url != None:
            self.engine = create_engine(url)
        else:
            # let's default to in-memory for now
            self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        # ensure tables are there
        Base.metadata.create_all(self.engine)

        # obtain session
        # the session is used for all transactions
        self.Session = sessionmaker(bind=self.engine)

    def add_one(self, bookmark: Bookmark) -> int:
        self.Session.add(bookmark)
        self.Session.commit()
        pass

    def add_many(self, bookmarks: list[Bookmark]) -> int:
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

    def find_first(self, query) -> Bookmark:
        pass

    def find_all(self, query) -> list[Bookmark]:
        pass
