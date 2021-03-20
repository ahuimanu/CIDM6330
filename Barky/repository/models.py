from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DomainBookmark:
    """
    Pure domain bookmark:
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL    
    """
    def __init__(self, id, title, url, notes, date_added) -> None:
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.date_added = date_added


class BookmarkModel(Base):
    """
    Declarative SQLA model
    """
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    notes = Column(String)
    date_added = Column(Date)