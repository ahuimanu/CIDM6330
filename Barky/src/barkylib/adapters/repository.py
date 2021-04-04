from abc import ABC, abstractmethod

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from barkylib.domain.models import Base, Bookmark


class BaseRepository(ABC):
    @abstractmethod
    def add_one(bookmark) -> int:
        raise NotImplementedError("Derived classes must implement add_one")

    @abstractmethod
    def add_many(bookmarks) -> int:
        raise NotImplementedError("Derived classes must implement add_many")

    @abstractmethod
    def delete_one(bookmark) -> int:
        raise NotImplementedError("Derived classes must implement delete_one")

    @abstractmethod
    def delete_many(bookmarks) -> int:
        raise NotImplementedError("Derived classes must implement delete_many")

    @abstractmethod
    def update(bookmark) -> int:
        raise NotImplementedError("Derived classes must implement update")

    @abstractmethod
    def update_many(bookmarks) -> int:
        raise NotImplementedError("Derived classes must implement update_many")

    @abstractmethod
    def find_first(query) -> Bookmark:
        raise NotImplementedError("Derived classes must implement find_first")

    @abstractmethod
    def find_all(query) -> list[Bookmark]:
        raise NotImplementedError("Derived classes must implement find_all")


class SqlAlchemyRepository(BaseRepository):
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
            self.engine = create_engine("sqlite:///:memory:", echo=True)

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
