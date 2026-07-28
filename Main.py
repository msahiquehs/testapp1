from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Sample FastAPI App",
    description="A simple API with two endpoints",
    version="1.0.0",
)

# In-memory "database" for demo purposes
items_db = {
    1: {"name": "Widget", "price": 9.99},
    2: {"name": "Gadget", "price": 19.99},
}


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


# Endpoint 1: Health check / root
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the FastAPI app"}


# Endpoint 2: Get item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, **item}


# Bonus endpoint: Create a new item (POST)
@app.post("/items/")
def create_item(item: Item):
    new_id = max(items_db.keys(), default=0) + 1
    items_db[new_id] = item.dict()
    return {"item_id": new_id, **item.dict()}
