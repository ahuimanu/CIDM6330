from abc import ABC, abstractmethod
from typing import List

from .models import BookmarkModel

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
    def find_first(query) -> BookmarkModel:
        raise NotImplementedError("Derived classes must implement find_first")

    @abstractmethod
    def find_all(query) -> list[BookmarkModel]:
        raise NotImplementedError("Derived classes must implement find_all")

