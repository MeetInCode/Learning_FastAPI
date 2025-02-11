from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Define a request model using Pydantic
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# A simple GET endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

# A POST endpoint to receive data
@app.post("/items/")
def create_item(item: Item):
    return {"message": f"Item {item.name} created successfully!", "item": item}

# A GET endpoint with path parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "square": item_id ** 2}
