from datetime import datetime

from barkylib import bootstrap
from barkylib.adapters.repository import *
from barkylib.domain import commands

# init from dotenv file
from dotenv import load_dotenv
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_sqlalchemy import SQLAlchemy
from . baseapi import AbstractBookMarkAPI

load_dotenv()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
# db = SQLAlchemy(app)
bus = bootstrap.bootstrap()

class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask
    """

    def __init__(self) -> None:
        super().__init__()

    # @app.route("/")
    def index(self):
        return f"Barky API"

    # @app.route("/api/one/<id>")
    def one(self, id):
        return f"The provided id is {id}"

    # @app.route("/api/all")
    def all(self):
        return f"all records"

    # @app.route("/api/first/<property>/<value>/<sort>")
    def first(self, filter, value, sort):
        return f"the first "
        pass

    def many(self, filter, value, sort):
        pass

    def add(bookmark):
        pass

    def delete(bookmark):
        pass

    def update(bookmark):
        pass

fb = FlaskBookmarkAPI()
bp = Blueprint('flask_bookmark_api', __name__, url_prefix='/api')

# @app.route('/')
bp.add_url_rule('/', 'index', fb.index, ['GET'])

# @app.route('/api/one/<id>')
bp.add_url_rule('/one/<id>', 'one', fb.one, ['GET'])

# @app.route('/api/all')
bp.add_url_rule('/all', 'all', fb.all, ['GET'])

