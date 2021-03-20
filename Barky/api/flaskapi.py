from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from repository.sqla_repository import *
from . baseapi import AbstractBookMarkAPI

# init from dotenv file
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask 
    """
    def __init__(self) -> None:
        super().__init__()
    
    @app.route('/')
    def index(self):
        return f'Barky API'

    @app.route('/api/one/<id>')
    def one(self, id):
        return f'The provided id is {id}'

    @app.route('/api/all')
    def all(self):
        return f'all records'

    def first(self, filter, value):
        return f'the first '
        pass
    
    def many(filter, sort):
        pass
    
    def add(bookmark):
        pass

    def delete(bookmark):
        pass

    def update(bookmark):
        pass
