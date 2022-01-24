import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    # obtain a handle, using the current request content 'g' to the database
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    # remove the db attribute from the 'g' collection
    db = g.pop('db', None)

    # assuming db was still referring to the database, close it
    if db is not None:
        db.close()