import uuid
import pytest
import config

from datetime import datetime



def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


def test_api_works(test_client):
    url = config.get_api_url()
    r = test_client.get(f"{url}/")
    assert r.status_code == 200
    assert b"HELLO FROM THE API" in r.data


def test_happy_path_returns_201_and_allocated_batch(add_stock, test_client):
    sku, othersku = random_sku("ball"), random_sku("other")
    print(sku)
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(
        [
            (laterbatch, sku, 100, datetime.strptime("2011-01-02", "%Y-%m-%d")),
            (earlybatch, sku, 100, datetime.strptime("2011-01-01", "%Y-%m-%d")),
            (otherbatch, othersku, 100, None),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()
    r = test_client.post(f"{url}/allocate", json=data)
    assert r.status_code == 201
    assert r.json["batchref"] == earlybatch


def test_unhappy_path_returns_400_and_error_message(test_client):
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = test_client.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json["message"] == f"Invalid sku {unknown_sku}"
