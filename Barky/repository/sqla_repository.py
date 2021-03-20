from .base_repository import BaseRepository
from .models import BookmarkModel

class SQLARespository(BaseRepository):

    def add_one(bookmark) -> int:
        pass

    def add_many(bookmarks) -> int:
        pass

    def delete_one(bookmark) -> int:
        pass

    def delete_many(bookmarks) -> int:
        pass

    def update(bookmark) -> int:
        pass

    def update_many(bookmarks) -> int:
        pass

    def find_first(query) -> BookmarkModel:
        pass

    def find_all(query) -> list[BookmarkModel]:
        pass