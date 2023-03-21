from datetime import datetime


class Bookmark:
    """
    Pure domain bookmark:
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL
    date_edited TEXT NOT NULL
    """

    def __init__(
        self,
        id: int,
        title: str,
        url: str,
        notes: str,
        date_added: datetime,
        date_edited: datetime,
    ) -> None:
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.date_added = date_added
        self.date_edited = date_edited
