from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


"""
Pure domain bookmark:
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
url TEXT NOT NULL,
notes TEXT,
date_added TEXT NOT NULL
date_edited TEXT NOT NULL
"""

class Bookmark:

    def __init__(self, id: int, title: str, url: str, notes: str, date_added: datetime, date_edited: datetime):
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.date_added = date_added
        self.date_edited = date_edited
        self.events = []
