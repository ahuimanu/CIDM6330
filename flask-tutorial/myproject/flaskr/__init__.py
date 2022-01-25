from atexit import register
import os

from flask import Flask


def create_app(test_config=None):
    # this is a method used to create and configure the Flask App - from the design pattern language
    # this is considered a "factory method" because it takes specifications and produces an
    # instance of a Flask application.
    app = Flask(__name__, instance_relative_config=True)

    # these are configuration variables that helps the Flask application to run
    app.config.from_mapping(
        SECRET_KEY="secret", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    # notice a TDD orientation inherent in Flask (at least from the documentation standpoint)
    if test_config is None:
        # load the instance config, if it exists, when not in testing mode
        app.config.from_pyfile("config.py", silent=True)
    else:
        # loas the test config if it was passed in as an argument
        app.config.from_mapping(test_config)

    # ensure the containing instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # we don't actually handle the error, we just catch it
        pass

    # we establish a single and simple route at this stage
    # this weird "@app" thing is a decorator - https://docs.python.org/3/glossary.html#term-decorator
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # call the db module - the db.py file's contents - so we can use 'init_app'
    from . import db

    db.init_app(app)

    # register blueprints
    from . import auth

    app.register_blueprint(auth.bpauth)

    return app
