"""
Note: this is significantly refactored to use the Imperative (a.k.a. Classical) Mappings (https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#imperative-a-k-a-classical-mappings)
That would have been common in 1.3.x and earlier.
"""
import logging
from typing import Text
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    event,
)

from sqlalchemy.orm import registry
from barkylib.domain.models import Bookmark

mapper_registry = registry()

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


def start_mappers():
    logger.info("starting mappers")
    mapper_registry.map_imperatively(Bookmark, bookmarks)
