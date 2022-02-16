from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    response = client.get("/hello")
    # the 'b' here ensures that the string is cast/translated as bytes
    # this is for transmission in the HTTP/TCP/IP 'stack'
    assert response.data == b"Hello, World!"
