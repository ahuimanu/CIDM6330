from datetime import datetime
from flask import Flask, jsonify, request
from barkylib.domain import commands
from barkylib.api import views
from barkylib import bootstrap

# init from dotenv file
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
bus = bootstrap.bootstrap()

@app.route('/')
def index(self):
    return f'Barky API'

@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    # title, url, notes, date_added, date_edited
    title = request.json["title"]
    url = request.json["url"]
    notes = request.json["notes"]
    date_added = request.json["date_added"]
    date_edited = request.json["date_edited"]

    cmd = commands.AddBookmarkCommand(
            title, url, notes, date_added, date_edited
    )
    bus.handle(cmd)
    return "OK", 201


@app.route("/bookmarks/<title>", methods=['GET'])
def get_bookmark_by_title(self, title):
    result = views.bookmarks_view(title, bus.uow)
    if not result:
         return "not found", 404
    return jsonify(result), 200

def get_bookmark_by_id(self, title):
    pass

def delete(self, bookmark):
    pass

def update(self, bookmark):
    pass
