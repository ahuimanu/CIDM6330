from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . baseapi import AbstractBookMarkAPI

class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask 
    """
    def one(id):
        pass

    def first(filter):
        pass
    
    def many(filter, sort):
        pass
    
    def add(bookmark):
        pass

    def delete(bookmark):
        pass

    def update(bookmark):
        pass
