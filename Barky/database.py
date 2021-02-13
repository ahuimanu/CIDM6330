'''
This module supports the following schema:

ID — The ID is the primary key of the table, or the main identifier of each record. It should automatically increment each time a new record is added, using the AUTOINCREMENT keyword. This column is an INTEGER type; the rest are TEXT.
Title — The title is required because it’s hard to skim your existing bookmarks if they’re only URLs. You can tell SQLite the column can’t be empty by using the NOT NULL keyword.
URL — The URL is required, so it gets NOT NULL as well.
Notes — Notes for a bookmark are optional, so only the TEXT specifier is necessary.
Date — The date the bookmark was added is required, so it gets NOT NULL.

SQL reference: https://www.w3schools.com/sql/default.asp

CREATE TABLE IF NOT EXISTS bookmarks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL
);

'''

import sqlite3

class DatabaseManager:
    def __init__(self, database_filename) -> None:
        self.connection = sqlite3.connect(database_filename)
    
    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        '''
        The _execute method should:

        1. Accept a statement as a string argument
        2. Get a cursor from the database connection
        3. Execute a statement using the cursor (more on this shortly)
        4. Return the cursor, which has stored the result of the executed statement (if any)        

        this is designed to use placeholders in SQL statements to insert values
        '''
        with self.connection: #https://www.pythonforbeginners.com/files/with-statement-in-python
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        '''
        The method offers a flexible way to pass data definition:
        1. Accept two arguments: the name of the table to create, and a dictionary of column names mapped to their data types and constraints
        2. Construct a CREATE TABLE SQL statement like the one shown earlier
        3. Execute the statement using DatabaseManager._execute
        '''
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items #this loop reads all column information
        ]

        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS
            '''
        )

