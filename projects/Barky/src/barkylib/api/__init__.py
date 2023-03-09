import os

from flask import Flask
from . flaskapi import FlaskBookmarkAPI

# init from dotenv file
from dotenv import load_dotenv
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import flaskapi
    app.register_blueprint(flaskapi.bp)

    return app