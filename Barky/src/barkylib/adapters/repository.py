from abc import ABC, abstractmethod
from datetime import datetime

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List, Set

from barkylib.adapters import orm
from barkylib.domain.models import Bookmark


class AbstractBookmarkRepository(ABC):
    def __init__(self):
        # seen is in reference to events detected
        self.seen : set[Bookmark] = set()

    def add(self, bookmark: Bookmark) -> None:
        # add to repo
        self._add(bookmark)
        # add to event list
        self.seen.add(bookmark)

    def get_all(self) -> list[Bookmark]:
        bookmarks: list[Bookmark] = self._get_all()
        if bookmarks:
            self.seen.update(bookmarks)
        return bookmarks

    def get_by_id(self, value: int) -> Bookmark:
        # get from repo
        bookmark: Bookmark = self._get_by_id(value)
        if bookmark:
            self.seen.add(bookmark)
        return bookmark        

    def get_by_title(self, value: str) -> Bookmark:
        # get from repo
        bookmark: Bookmark = self._get_by_title(value)
        if bookmark:
            self.seen.add(bookmark)
        return bookmark

    def get_by_url(self, value: str) -> Bookmark:
        # get from repo
        bookmark: Bookmark = self._get_by_url(value)
        if bookmark:
            self.seen.add(bookmark)
        return bookmark

    @abstractmethod
    def _add(self, bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement add_one")

    @abstractmethod
    def _add_all(self, bookmarks: list[Bookmark]) -> None:
        raise NotImplementedError("Derived classes must implement add_all")

    @abstractmethod
    def _delete(bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement delete")

    @abstractmethod
    def _get_all(self) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement get_all")

    @abstractmethod
    def _get_by_id(self, value: int) -> Bookmark:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def _get_by_title(self, value: str) -> Bookmark:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def _get_by_url(self, value: str) -> Bookmark:
        raise NotImplementedError("Derived classes must implement get")

    @abstractmethod
    def _update(self, bookmark: Bookmark) -> None:
        raise NotImplementedError("Derived classes must implement update")

    @abstractmethod
    def _update(self, bookmarks: list[Bookmark]) -> None:
        raise NotImplementedError("Derived classes must implement update")


class SqlAlchemyBookmarkRepository(AbstractBookmarkRepository):
    """
    Uses guidance from the basic SQLAlchemy 1.4 tutorial: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """

    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def _add(self, bookmark: Bookmark) -> None:
        self.session.add(bookmark)
        self.session.commit()

    def _add_all(self, bookmarks: list[Bookmark]) -> None:
        self.session.add_all(bookmarks)
        self.session.commit()

    def _delete(self, bookmark: Bookmark) -> None:
        pass

    def _get_all(self) -> list[Bookmark]:
        return self.session.query(Bookmark).all()

    def _get_by_id(self, value: int) -> Bookmark:
        answer = self.session.query(Bookmark).filter(Bookmark.id == value)
        return answer.one()

    def _get_by_title(self, value: str) -> Bookmark:
        answer = self.session.query(Bookmark).filter(Bookmark.title == value)
        return answer.one()

    def _get_by_url(self, value: str) -> Bookmark:
        answer = self.session.query(Bookmark).filter(Bookmark.url == value)
        return answer.one()

    def _update(self, bookmark) -> None:
        pass

    def _update(self, bookmarks: list[Bookmark]) -> None:
        pass


class FakeBookmarkRepository(AbstractBookmarkRepository):
    """
    Uses a Python list to store "fake" bookmarks: https://www.w3schools.com/python/python_lists.asp
    """

    def __init__(self, bookmarks):
        super().__init__()
        self._bookmarks = set(bookmarks)

    def _add(self, bookmark) -> None:
        self._bookmarks.add(bookmark)

    def _add_all(self, bookmarks: list[Bookmark]) -> None:
        self._bookmarks.update(bookmarks)

    def _delete(self, bookmark: Bookmark) -> None:
        self._bookmarks.remove(bookmark)

    def _get_all(self) -> list[Bookmark]:
        return self._bookmarks

    # python next function: https://www.w3schools.com/python/ref_func_next.asp
    def _get_by_id(self, value: int) -> Bookmark:
        return next((b for b in self._bookmarks if b.id == value), None)

    def _get_by_title(self, value: str) -> Bookmark:
        return next((b for b in self._bookmarks if b.title == value), None)

    def _get_by_url(self, value: str) -> list[Bookmark]:
        return next((b for b in self._bookmarks if b.url == value), None)

    def _update(self, bookmark: Bookmark) -> None:
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

    def _update(self, bookmarks: list[Bookmark]) -> None:
        for inbm in bookmarks:
            self._update(inbm)
