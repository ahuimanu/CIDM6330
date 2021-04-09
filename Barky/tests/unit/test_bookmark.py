from datetime import date, datetime, timedelta
import random

from barkylib.domain import events
from barkylib.domain.models import Bookmark

ok_urls = ["http://", "https://"]

def test_bookmark_title_is_unique():
    pass

def test_new_bookmark_added_and_edited_times_are_the_same():
    # arrange
    created = datetime.now().isoformat()
    
    # act
    bookmark = Bookmark(0, "test", "http://www.example/com", None, created)

    # assert
    assert bookmark.date_added == bookmark.date_edited

def test_new_bookmark_url_is_well_formed():
    # arrange
    created = datetime.now().isoformat()
    edited = created
    
    # act
    bookmark = Bookmark(0, "test", "http://www.example/com", None, created)
    # list comprehensions - https://www.w3schools.com/python/python_lists_comprehension.asp
    okay = [prefix for prefix in ok_urls if bookmark.url.startswith(prefix) ]
    # any function - https://www.w3schools.com/python/ref_func_any.asp
    assert any(okay)

def test_that_edit_time_is_newer_than_created_time():
    # arrange
    created = datetime.now().isoformat()
    edited = created
    
    # act
    bookmark = Bookmark(0, "test", "http://www.example/com", None, created)

    bookmark.notes = "Lorem Ipsum"
    hours_addition = random.randrange(1,10)
    edit_time = datetime.fromisoformat(bookmark.date_edited)
    bookmark.date_edited = (edit_time + timedelta(hours=hours_addition)).isoformat()

    # assert
    assert bookmark.date_added < bookmark.date_edited



