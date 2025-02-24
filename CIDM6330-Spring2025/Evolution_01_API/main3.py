from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

"""
For this example, we'll use uvicorn to run the API:
1. uvicorn main3:app --reload
"""

app = FastAPI()

# brush up on Pydantic Models: https://docs.pydantic.dev/latest/


class Pet(BaseModel):
    name: str
    age: int
    type: str


pets = {
    "1": Pet(name="sparky", age=3, type="dog"),
    "2": Pet(name="whiskers", age=5, type="cat"),
    "3": Pet(name="tweety", age=2, type="bird"),
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/pets/{pet_id}")
def read_item(pet_id: int):
    return {"pet_id": pet_id, "pet": pets[str(pet_id)]}


@app.put("/pets/{pet_id}")
def update_item(pet_id: int, pet: Pet):
    pets[str(pet_id)] = pet  # update the pet in the dictionary
    # however, without a persistence strategy, this will be lost when the server restarts
    return {"pet_id": pet_id, "item": pets[str(pet_id)]}
