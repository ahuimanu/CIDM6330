# python imports
# third-party imports
# your own imports

from flask import Flask
from markupsafe import escape

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/login")
def login():
    return "login"


@app.route("/user/<username>")
def profile(username):
    return f"{escape(username)}'s profile"
    # return '{}\'s profile'.format(escape(username))


@app.route("/me")
def me_api():
    return {"username": "jeff", "theme": "dark", "image": "me.jpg"}
