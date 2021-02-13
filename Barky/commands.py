'''
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
'''
from datetime import datetime
import sys

from database import DatabaseManager

# module scope
db = DatabaseManager('bookmarks.db')

class CreateBookmarksTableCommand:
    '''
    uses the DatabaseManager to create the bookmarks table
    '''
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })


class AddBookmarkCommand:
    '''
    This class will:

    1. Expect a dictionary containing the title, URL, and (optional) notes information for a bookmark.
    2. Add the current datetime to the dictionary as date_added. 
    3. Insert the data into the bookmarks table using the DatabaseManager.add method.
    4. Return a success message that will eventually be displayed by the presentation layer.
    '''
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class ListBookmarksCommand:
    '''
    We need to review the bookmarks in the database.
    To do so, this class will:
    1. Accept the column to order by, and save it as an instance attribute. 
    2. Pass this information along to db.select in its execute method.
    3. Return the result (using the cursor’s .fetchall() method) because select is a query.
    '''
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    '''
    We also need to remove bookmarks.
    '''
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()

