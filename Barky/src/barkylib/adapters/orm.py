import logging
from typing import Text
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    event,
)

from sqlalchemy.orm import mapper, relationship

from ..domain.models import Bookmark

logger = logging.getLogger(__name__)

metadata = MetaData()


"""
Pure domain bookmark:
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
url TEXT NOT NULL,
notes TEXT,
date_added TEXT NOT NULL
date_edited TEXT NOT NULL
"""
bookmarks = Table(
    "bookmarks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), unique=True),
    Column("url", String(255)),
    Column("notes", Text),
    Column("date_added", DateTime),
    Column("date_edited", DateTime),
)


def start_mapper():
    logger.info("string mappers")
    bookmarks_mapper = mapper(Bookmark, bookmarks)
