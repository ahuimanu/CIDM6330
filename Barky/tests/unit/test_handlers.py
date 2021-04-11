from __future__ import annotations
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from typing import Dict, List
import pytest
from barkylib import bootstrap
from barkylib.domain import commands
from barkylib.services import handlers, unit_of_work
from barkylib.adapters import repository

from barkylib.adapters.orm import start_mappers
from barkylib.services.unit_of_work import FakeUnitOfWork


def boostrap_test_app():
    return bootstrap.bootstrap(start_orm=False, uow=FakeUnitOfWork())


class TestAddBookmark:
    def test_add_single_bookmark(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddBookmarkCommand(
                0,
                f"Test",  # title
                f"http://example.com",  # url
                nu.isoformat(),  # date added
                nu.isoformat(),  # date edited
            )
        )

        assert bus.uow.bookmarks.get_by_title(f"Test") is not None
        assert bus.uow.committed

    def test_get_bookmark_by_id(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddBookmarkCommand(
                99,
                f"Test",  # title
                f"http://example.com",  # url
                nu.isoformat(),  # date added
                nu.isoformat(),  # date edited
            )
        )

        assert bus.uow.bookmarks.get_by_id(99) is not None
        assert bus.uow.committed

    def test_get_bookmark_by_url(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddBookmarkCommand(
                99,
                f"Test",  # title
                f"http://example.com",  # url
                nu.isoformat(),  # date added
                nu.isoformat(),  # date edited
            )
        )

        assert bus.uow.bookmarks.get_by_url(f"http://example.com") is not None
        assert bus.uow.committed

    def test_get_all_bookmarks(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)        
        bus.handle(
            commands.AddBookmarkCommand(
                99,
                f"Test",  # title
                f"http://example.com",  # url
                nu.isoformat(),  # date added
                nu.isoformat(),  # date edited
            )
        )

        nuto = nu + timedelta(days = 2, hours=12)

        bus.handle(
            commands.AddBookmarkCommand(
                999,
                f"Test2",  # title
                f"http://example.com",  # url
                nuto.isoformat(),  # date added
                nuto.isoformat(),  # date edited
            )
        )

        records = bus.uow.bookmarks.get_all()
        assert len(records) == 2