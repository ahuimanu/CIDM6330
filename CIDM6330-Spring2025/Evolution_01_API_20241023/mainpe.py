from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Simple data storage
pe_firms = {}

# Pydantic model
class PrivateEquityFirm(BaseModel):
    firm_name: str
    assets_under_mgmt: float

@app.get("/")
async def root():
    return {"message": "PE Firm API is running"}

@app.get("/pe-firm/{firm_name}")
async def get_pe_firm(firm_name: str):
    if firm_name not in pe_firms:
        raise HTTPException(status_code=404, detail="PE firm not found")
    return pe_firms[firm_name]

@app.post("/pe-firm/create")
async def create_pe_firm(firm: PrivateEquityFirm):
    pe_firms[firm.firm_name] = firm.dict()
    return {"message": f"PE firm {firm.firm_name} created successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)