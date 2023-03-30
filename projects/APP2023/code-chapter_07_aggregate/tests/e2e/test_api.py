import pytest
import requests

from allocation import config
from ..random_refs import random_sku, random_batchref, random_orderid


def test_api_works(test_client):
    url = config.get_api_url()
    r = test_client.get(f"{url}/")
    assert r.status_code == 200
    assert b"HELLO FROM THE API" in r.data


def post_to_add_batch(test_client, ref, sku, qty, eta):
    url = config.get_api_url()
    r = test_client.post(
        f"{url}/add_batch", json={"ref": ref, "sku": sku, "qty": qty, "eta": eta}
    )

    assert r.status_code == 201


def test_happy_path_returns_201_and_allocated_batch(test_client):
    sku, othersku = random_sku("ball"), random_sku("other")
    print(sku)
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)

    # post_to_add_batch(
    #     test_client, laterbatch, sku, 100, datetime.strptime("2011-01-02", "%Y-%m-%d")
    # )
    # post_to_add_batch(
    #     test_client, earlybatch, sku, 100, datetime.strptime("2011-01-01", "%Y-%m-%d")
    # )
    post_to_add_batch(test_client, laterbatch, sku, 100, "2011-01-02")
    post_to_add_batch(test_client, earlybatch, sku, 100, "2011-01-01")
    post_to_add_batch(test_client, otherbatch, othersku, 100, None)
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
