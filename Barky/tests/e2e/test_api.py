import pytest

import requests

LOCALHOST = "http://127.0.0.1:5000/"


def test_api_can_connect():
    res = requests.get(LOCALHOST)
    assert res != None


def test_api_index():
    res = requests.get(LOCALHOST)
    assert res != None
