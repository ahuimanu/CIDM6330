from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Cake(BaseModel):
    cake_id: int
    name: str
    category: str
    base_price: float
    available_sizes: list[list[str, float]]
    avaiable_price_adjustments: list[float]
    available_flavors: list[str]


sizes_and_prices = [['s', '0.99'], ['m', '1.99'], ['s', '3.99']]




# Since we don't have a database, let's use some temp data in a list. 
# (Dr. Babb also mentioned this can be stateless for the time)
# Data seeding. Temp
cakes = [
    Cake(
        cake_id=1,
        name="Red Velvet",
        category="Classic",
        base_price=25.99,
        available_sizes=["small", "medium"],
        available_flavors=["red velvet"],
    ),
    Cake(
        cake_id=2,
        name="Chocolate Ganache",
        category="Premium",
        base_price=39.99,
        available_sizes=["medium", "large"],
        available_flavors=["chocolate"],
    ),
]


# GET /cakes: Retrieve all cakes
@app.get("/cakes")
async def get_all_cakes():
    return cakes


# GET /cakes/{cake_id}: Retrieve a cake by ID
@app.get("/cakes/{cake_id}")
async def get_cake_by_id(cake_id: int):
    cake = [cake for cake in cakes if cake.cake_id == cake_id]
    if cake:
        return cake[0]
    else:
        return {"message": f"Cake with ID {cake_id} not found"}

# GET /cakes/flavor/{flavor}: Filtered list of all cakes by available_flavour
@app.get("/cakes/flavor/{flavor}")
async def get_cakes_by_flavor(flavor: str):
    filtered_cakes = [cake for cake in cakes if flavor.lower() in [f.lower() for f in cake.available_flavors]]

    if not filtered_cakes:
        return {"message": f"Sorry, no cakes of flavor {flavor} available at this time."}

    return filtered_cakes


# # POST /cakes: Create a new cake
@app.post("/cakes")
async def create_cake(cake: Cake):
    # Check if cake ID already exists
    for existing_cake in cakes:
        if existing_cake.cake_id == cake.cake_id:
            raise HTTPException(status_code=409, detail= f"Cake with ID {cake.cake_id} already exists. Consider updating.")

    cakes.append(cake)
    return {"message": "Cake created successfully", "cake": cake}

# PUT /cakes/{cake_id}: Update an existing cake
@app.put("/cakes/{cake_id}")
async def update_cake(cake_id: int, updated_cake: Cake):
    for cake in cakes:
        if cake.cake_id == cake_id:
            cake.name = updated_cake.name
            cake.category = updated_cake.category
            cake.base_price = updated_cake.base_price
            cake.available_sizes = updated_cake.available_sizes
            cake.available_flavors = updated_cake.available_flavors
            return {"message": "Cake updated successfully", "cake": cake}
    return {"message": f"Cake with ID {cake_id} not found"}


# DELETE /cakes/{cake_id}: Delete a cake by ID
@app.delete("/cakes/{cake_id}")
async def delete_cake(cake_id: int):
    global cakes
    cakes = [cake for cake in cakes if cake.cake_id != cake_id]
    return {"message": f"Cake with ID {cake_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)