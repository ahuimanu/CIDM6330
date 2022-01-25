import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask.views import View
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

"""
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, 
they are registered with a blueprint. Then the blueprint is registered with 
the application when it is available in the factory function.
"""

bpauth = Blueprint("auth", __name__, url_prefix="/auth")


@bpauth.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username required"
        elif not password:
            error = "Password required"

        if error is None:
            # exception handling in python: https://www.w3schools.com/python/python_try_except.asp
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )

            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))


@bpauth.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            # session is a dict that stores data across http requests.
            # When validation succeeds, the user’s id is stored in a new session.
            # The data is stored in a cookie that is sent to the browser,
            # and the browser then sends it back with subsequent requests.
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bpauth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bpauth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view: View):
    # using functools (https://docs.python.org/3/library/functools.html)
    # to assist in creating a decorator function
    # https://wiki.python.org/moin/PythonDecorators
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # The url_for() function generates the URL to a view based on a name and arguments.
            # The name associated with a view is also called the endpoint, and by default it’s
            # the same as the name of the view function.
            return redirect(url_for("auth_login"))

        return view(**kwargs)

    return wrapped_view
