from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING

from barkylib.domain import commands, events, models

if TYPE_CHECKING:
    from . import unit_of_work

def add_bookmark(
    cmd: commands.AddBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:

        bookmark = None

        # look to see if we already have this bookmark as the title is set as unique
        try:
            # we place this in a try block in case we are using SQLAlchemy
            bookmark = uow.bookmarks.get_by_title(value=cmd.title)

            # checks to see if the list is empty
            if not bookmark:
                bookmark = models.Bookmark(
                    cmd.id, cmd.title, cmd.url, cmd.notes, cmd.date_added, cmd.date_edited, 
                )
                uow.bookmarks.add(bookmark)            
        except:
            bookmark = models.Bookmark(
                cmd.id, cmd.title, cmd.url, cmd.notes, cmd.date_added, cmd.date_edited, 
            )
            uow.bookmarks.add(bookmark)

        uow.commit()

# ListBookmarksCommand: order_by: str order: str
def list_bookmarks(
    cmd: commands.ListBookmarksCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    bookmarks = None
    with uow:
        bookmarks = uow.bookmarks.all()
        
    return bookmarks


# DeleteBookmarkCommand: id: int
def delete_bookmark(
    cmd: commands.DeleteBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


# EditBookmarkCommand(Command):
def edit_bookmark(
    cmd: commands.EditBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


EVENT_HANDLERS = {
    events.BookmarkAdded: [add_bookmark],
    events.BookmarksListed: [list_bookmarks],
    events.BookmarkDeleted: [delete_bookmark],
    events.BookmarkEdited: [edit_bookmark],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddBookmarkCommand: add_bookmark,
    commands.ListBookmarksCommand: list_bookmarks,
    commands.DeleteBookmarkCommand: delete_bookmark,
    commands.EditBookmarkCommand: edit_bookmark,
}  # type: Dict[Type[commands.Command], Callable]
