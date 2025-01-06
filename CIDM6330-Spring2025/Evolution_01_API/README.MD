# API code

Let's think about making a basic RESTful API

## Core Elements of a RESTful API

-   **Web Server** - Typical are Apache, NGINX, IIS
    -   Which can serve a variety of [content types](https://www.iana.org/assignments/media-types/media-types.xhtml), we will be intrested in text, html, and json
    -   Generall Web server process:
        -   A process loop that wais for an HTTP request from a client capable of making HTTP requests.
        -   Received requets will either look for a static resources or a programmatically developed response.
        -   The resource or response is prepared.
        -   The response is sent back to the client.
-   **Python Web Application Gateway**
    -   Common Gateway Interface (CGI) (deprecated),
    -   Web Server Gateway Interface - [WSGI](https://docs.python.org/3/library/wsgiref.html)
        -   Common WSGI implementations: [Gunicorn](https://gunicorn.org/), [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/), mod_wsgi
-   **Web App** - Which is python code that can programmatically prepare responses using a known content type.
    -   Typical Web app process:
        -   Web server notifies that a programmatically-developed http response is desired.
        -   The request is interpreted and the program executes.
        -   The programmatically-developed content is returned to the web server.
        -   The web server delivers this response back to the client as if the web server created it.
    -   The web server is a proxy for the web application's responses

## A Basic WSGI Implementation

At the most basic of levels, a simple WSGI-driven web app server will work with this code:

```python
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    ret = [("%s: %s\n" % (key, value)).encode("utf-8")
           for key, value in environ.items()]
    return ret

with make_server('', 8000, simple_app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
```

Here is an alternative approach to the same thing:

```python
from wsgiref.simple_server import make_server


def application(environ, start_response):
    response_body = [
        '{key}: {value}'.format(key=key, value=value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    status = '200 OK'

    response_headers = [
        ('Content-type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return [response_body.encode('utf-8')]


server = make_server('localhost', 8000, app=application)
server.serve_forever()
```

This is an incredibly manual process and most developers will use tools that simplify and extend the most basic WSGI implementations.

There are three approaches discussed in the following tutorial: [Twilio Tutorial](https://www.twilio.com/en-us/blog/create-api-with-python)

-   Flask
-   FastAPI
-   Django REST Framework

Although I would prefer the DRF, we can explore FastAPI first.

### The Fast API Approach

From the tutorial, it is very simple to get going.

#### Step 1: Install FastAPI and UVICORN (for WSGI)

`pip install fastapi uvicorn`

#### Step 2: Create a simple entry point (main.py)

```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/api/greet")
def greet():
    return {"message": "Hello from FastAPI"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

#### Step 3: Test with Browser or `curl`

Run the script `python main.py` and then test it out:

`http://localhost:8000/api/greet`

`curl http://localhost:8000/api/greet`

Note that the response received is formatted as [JavaScript Object Notation (JSON)](https://www.w3schools.com/js/js_json_intro.asp)

### More on Fast API

Okay, the approach above, while simple, was a little too light on details. The good news is that [FastAPI](https://fastapi.tiangolo.com/) is [well-documented](https://fastapi.tiangolo.com/reference/) and has a [tutorial section for in-depth learning](https://fastapi.tiangolo.com/learn/).

The most important steps are:

#### Fast API Step 1

(1) Import FastAPI and (2) make an app

```python
from fastapi import FastAPI # 1: import

app = FastAPI() # 2: make app


@app.get("/") # 3: path operation
async def root():
    return {"message": "Hello World"}
```

#### Fast API Step 2

(3) create paths - these are the resources requested in a URL

If your url is this: `https://example.com/items/food`
Then the path is `/items/food`

Fast API, like any compliant RESTful API library, will implement the following HTTP "Verbs" (Methods):

-   **POST**: to create data.
-   **GET**: to read data.
-   **PUT**: to update data.
-   **DELETE**: to delete data.
-   OPTIONS
-   HEAD
-   PATCH
-   TRACE

The bolded methods commonly implement what is known as [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) behavior.

#### Fast API Step 3

We establish that a Python function/method will serve as a CRUD operation by using what are known as Python "decorators:"

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/") # the decorator indicating path and type of operatation
async def root():
    return {"message": "Hello World"}
```

So, we have these decorators available:

-   `@app.get()`
-   `@app.post()`
-   `@app.put()`
-   `@app.delete()`
-   `@app.options()`
-   `@app.head()`
-   `@app.patch()`
-   `@app.trace()`

The operators are there to associate a path and a method with what you want to do in response.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

The following are some of the valid Python data types to return from the method:

-   dict
-   list
-   string,
-   int

## More Path Method Capabilities

In order to create a sophisticated API, we'll need more features than static resource paths.

### Path Parameters

In the example below we declare path "parameters" or "variables" by placing the parameter name between curly braces `{` `}`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

We can use Python's [type hint](https://docs.python.org/3/library/typing.html) system to be more specific about that kind of data will be parameterized:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int): # notice the type hint here
    return {"item_id": item_id}
```

Type hints also provide some enforcement by throwing an error if a number type is expected and a string is sent, for example.

### Documentation

Your API is auto documented when using FastAPI by going to this URL: `http://127.0.0.1:8000/docs`

### Query Parameters

The HTTP specification allows for GET requests to provide a key-value list of parameters as a part of the URL, Fast API can handle this.

Here is a URL with a query parameter set:

`http://127.0.0.1:8000/items/?skip=0&limit=10`

And here is how it is handled in FastAPI:

```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

Since query parameters are optional, we can anticipate them this way:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### Request Body - For POST, DELETE, PATCH

When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

A request body is data sent by the client to your API. A response body is the data your API sends to the client.

Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.

To declare a request body, you use Pydantic models with all their power and benefits.
