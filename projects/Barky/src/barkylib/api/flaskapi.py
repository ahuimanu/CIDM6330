from datetime import datetime

from barkylib import bootstrap
from barkylib.adapters.repository import *
from barkylib.domain import commands

# init from dotenv file
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from .baseapi import AbstractBookMarkAPI

load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
# db = SQLAlchemy(app)
bus = bootstrap.bootstrap()


class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask
    """

    def __init__(self) -> None:
        super().__init__()

    @app.route("/")
    def index(self):
        return f"Barky API"

    @app.route("/api/one/<id>")
    def one(self, id):
        return f"The provided id is {id}"

    @app.route("/api/all")
    def all(self):
        return f"all records"

    @app.route("/api/first/<property>/<value>/<sort>")
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
