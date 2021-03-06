from flask import Flask
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'