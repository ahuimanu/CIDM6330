from typing import Union
from fastapi import FastAPI

"""
For this example, we'll use uvicorn to run the API:
1. uvicorn main2:app --reload
"""

app = FastAPI()

# brush up on Python dictionaries: https://www.w3schools.com/python/python_dictionaries.asp
items = {
    "1": "dog",
    "2": "cat",
    "3": "bird",
}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "item": items[str(item_id)]}