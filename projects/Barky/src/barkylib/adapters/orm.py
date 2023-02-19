import logging
from typing import Text

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text, event

# from sqlalchemy.orm import mapper
from sqlalchemy.orm import registry

from ..domain.models import Bookmark

logger = logging.getLogger(__name__)

metadata = MetaData()

mapper_reg = registry()


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


def start_mappers():
    logger.info("string mappers")
    # SQLAlchemy 2.0
    bookmarks_mapper = mapper_reg.map_imperatively(Bookmark, bookmarks)
    # SQLAlchemy 1.3
    # bookmarks_mapper = mapper(Bookmark, bookmarks)
