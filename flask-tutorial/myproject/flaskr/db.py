import sqlite3

import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext


def get_db():
    # obtain a handle, using the current request content 'g' to the database
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # remove the db attribute from the 'g' collection
    db = g.pop("db", None)

    # assuming db was still referring to the database, close it
    if db is not None:
        db.close()


def init_db():
    # read the sql script and execute
    db = get_db()

    with current_app.open_resource("schema.sql") as schema_file:
        db.executescript(schema_file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    # makes it possible to reset the database from the command line when running
    # the Flask applicaiton
    """Clear existing data and create tables"""
    init_db()
    click.echo("initialized the database")


def init_app(app: Flask):
    # take an app, once initialized and make it aware of the db management methods here
    # this code also uses type hints, which helps tooling better understand your intentions
    # concerning the data types used in your python programs

    # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)

    # app.cli.add_command() adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)
