from abc import ABC, abstractmethod
from datetime import datetime

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List, Set

from barkylib.adapters import orm
from barkylib.domain.models import Base, Bookmark


class AbstractBookmarkRepository(ABC):
    def __init__(self):
        self.bookmarks: list[Bookmark] = list()

    @abstractmethod
    def add(self, bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement add_one")

    @abstractmethod
    def add_all(self, bookmarks: list[Bookmark]) -> None:
        raise NotImplementedError("Derived classes must implement add_all")

    @abstractmethod
    def delete(bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement delete")

    @abstractmethod
    def get_by_id(self, bookmark: Bookmark, query: int) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def get_by_title(self, bookmark: Bookmark, query: str) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def get_by_url(self, bookmark: Bookmark, query: str) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def update(self, bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement update")

    @abstractmethod
    def update(self, bookmarks: list[Bookmark]) -> None:
        raise NotImplementedError("Derived classes must implement update")


class SqlAlchemyBookmarkRepository(AbstractBookmarkRepository):
    """
    Uses guidance from the basic SQLAlchemy 1.4 tutorial: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """

    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def add(self, bookmark: Bookmark) -> None:
        self.session.add(bookmark)
        self.session.commit()

    def add_all(self, bookmarks: list[Bookmark]) -> None:
        self.session.add_all(bookmarks)
        self.session.commit()

    def delete(self, bookmark: Bookmark) -> None:
        pass

    def get_by_id(self, bookmark: Bookmark, query: int) -> list[Bookmark]:
        pass

    def get_by_title(self, bookmark: Bookmark, query: str) -> list[Bookmark]:
        pass

    def get_by_url(self, bookmark: Bookmark, query: str) -> list[Bookmark]:
        pass

    def update(self, bookmark) -> None:
        pass

    def update(self, bookmarks: list[Bookmark]) -> None:
        pass


class FakeBookmarkRepository(AbstractBookmarkRepository):
    """
    Uses a Python set to store the "fake" bookmarks: https://www.w3schools.com/python/python_sets.asp
    """

    def __init__(self, bookmarks):
        super().__init__()
        self._bookmarks: list[Bookmark] = list()

    def add(self, bookmark: Bookmark) -> None:
        self._bookmarks.append(bookmark)

    def add_all(self, bookmarks: list[Bookmark]) -> None:
        self._bookmarks.extend(bookmarks)

    def delete(self, bookmark: Bookmark) -> None:
        self._bookmarks.remove(bookmark)

    def get_by_id(self, bookmark: Bookmark, query: int) -> list[Bookmark]:
        return [b for b in self._bookmarks if b.id == query]

    def get_by_title(self, bookmark: Bookmark, query: str) -> list[Bookmark]:
        return [b for b in self._bookmarks if b.title == query]

    def get_by_url(self, bookmark: Bookmark, query: str) -> list[Bookmark]:
        return [b for b in self._bookmarks if b.title == query]

    def update(self, bookmark: Bookmark) -> None:
        try:
            idx = self._bookmarks.index(bookmark)
            bm = self._bookmarks[idx]
            with bookmark:
                bm.id = bookmark.id
                bm.title = bookmark.title
                bm.url = bookmark.url
                bm.notes = bookmark.notes
                bm.date_added = bookmark.date_added
                bm.date_edited = datetime.utc.now()
                self._bookmarks[idx] = bm
        except:
            self._bookmarks.append(bookmark)

        return None

    def update(self, bookmarks: list[Bookmark]) -> None:
        for inbm in bookmarks:
            self.update(inbm)
