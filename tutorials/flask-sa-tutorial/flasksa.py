# python imports
# third-party imports
# your own imports

import requests
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

load_dotenv()

"""
This simple API will do the following:
1. fetch METAR report
2. save METAR report
3. save favorite station
4. fetch METAR for favorite station
"""
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
# do db stuff
db = SQLAlchemy()

# create flask app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the flask app with the extension
db.init_app(app)

# sql alchemy magic


# create METAR model
class MetarReport(db.Model):
    id = db.Column(db.String, primary_key=True)
    raw = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime)


# init and create all tables
with app.app_context():
    db.create_all()


# utility methods
# https://api.weather.gov/stations/KAMA/observations/latest
def fetch_metar_for_station(station: str):
    url = f"https://api.weather.gov/stations/{station}/observations/latest"
    r = requests.get(url)
    return r.content


def save_station_to_favorites(station: str):
    pass


@app.route("/")
def noaa_metar():
    return "Get NOAA METAR"


@app.route("/metar/<station>")
def get_noaa_metar(station: str):
    return fetch_metar_for_station(station)


@app.route("/save/<station>")
def save_station(station: str):
    save_station_to_favorites(station)
    return f"{escape(station)} data"


@app.route("/favorites")
def metar_for_favorites():
    return {"username": "jeff", "theme": "dark", "image": "me.jpg"}
