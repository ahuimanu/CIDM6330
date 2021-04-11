from abc import ABC, abstractmethod

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List, Set

from barkylib.adapters import orm
from barkylib.domain.models import Base, Bookmark


class AbstractBookmarkRepository(ABC):
    def __init__(self):
        self.bookmarks = set()

    @abstractmethod
    def add_one(self, bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement add_one")

    @abstractmethod
    def add_all(self, bookmarks: list[Bookmark]) -> None:
        raise NotImplementedError("Derived classes must implement add_all")

    @abstractmethod
    def delete(bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement delete")

    @abstractmethod
    def get(bookmark: Bookmark, query) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def update(bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement update")


class SqlAlchemyBookmarkRepository(AbstractBookmarkRepository):
    """
    Uses guidance from the basic SQLAlchemy 1.3 tutorial: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
    """

    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def add_one(self, bookmark: Bookmark) -> None:
        self.session.add(bookmark)
        self.session.commit()

    def add_all(self, bookmarks: list[Bookmark]) -> None:
        self.session.add_all(bookmarks)
        self.session.commit()

    def delete(self, bookmark: Bookmark) -> None:
        pass

    def get(self, bookmark: Bookmark, query) -> list[Bookmark]:
        pass

    def update(self, bookmark) -> int:
        pass

    def update_many(self, bookmarks) -> int:
        pass


class FakeBookmarkRepository(AbstractBookmarkRepository):
    def __init__(self, bookmarks):
        super().__init__()
        self._bookmarks = set(bookmarks)
