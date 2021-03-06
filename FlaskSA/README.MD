# Flask Intro

[Flask](https://flask.palletsprojects.com/en/1.1.x/) is the [number one Web framework for Python](https://www.jetbrains.com/lp/python-developers-survey-2020/).

Often called a ["micro framework," Flask](https://flask.palletsprojects.com/en/1.1.x/foreword/#what-does-micro-mean) is extensible such that you can start small and scale out.  Further, Flask is less deterministic ("opinionated") about collateral choices you make in terms of using Flask in an extended architecture.

For our purposes, Flask will allow us to specify [HTTP REST API endpoints](https://en.wikipedia.org/wiki/Representational_state_transfer) to query and modify application state.

## Flask is Easy

1. Create Virtual Environment: While I use conda, I believe the built-in venv tool is perhaps the safest bet for you: 
``` bash
mkdir myproject
cd myproject
python3 -m venv venv
```
2. Use pip to install Flask:
``` bash
pip install Flask
```
3. Code for Flask

## The Flask ["Hello Wolrd"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program)

The most basic possible Flask application does the following:
1. Create an HTTP server
2. Establish a route
3. Run Flask
4. Navigate browser to route

Here is the code that does this:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

From the Flask Documentation, here is the elaborated explanation for what the above code does:

1. First we imported the Flask class. An instance of this class will be our WSGI application.

2. Next we create an instance of this class. The first argument is the name of the application’s module or package. If you are using a single module (as in this example), you should use `__name__` because depending on if it’s started as application or imported as module the name will be different (`'__main__'` versus the actual import name). This is needed so that Flask knows where to look for templates, static files, and so on. For more information have a look at the Flask documentation.

3. We then use the `route()` [decorator](https://pythonbasics.org/decorators/) to tell Flask what URL should trigger our function.

The function is given a name which is also used to generate URLs for that particular function, and returns the message we want to display in the user’s browser.

## Run it

Flask needs to be told which app it is running and this is commonly accomplished using environment variables.

```bash
export FLASK_APP=hello.py
flask run
 * Running on http://127.0.0.1:5000/
```

## the dotenv alternative

We will soon enough need to set application-specific environment variables and we have an opportunity to learn how to do this by moving the `set FLASK_APP=hello.py` directive to a more automated approach.

1. First, get the python dotenv package from pypi.org: `pip install python-dotenv`
2. Appropriate a [suitable gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore) file as we will be using dotenv to hide secret information from being placed into our code repository.
3. Then, create a file in your project called `.env`
4. Put the FLASK_APP environment variable assignment into this file:
```
FLASK_APP=hello.py
```
5. Include the code that utilizes `dotenv-python` in your Flask app:
```python
from dotenv import load_dotenv
load_dotenv()
```