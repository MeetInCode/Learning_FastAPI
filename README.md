In FastAPI, Uvicorn is the ASGI server that is responsible for handling requests and responses. While Flask uses a built-in WSGI server (which is simple and sufficient for development), FastAPI, being an ASGI framework, requires a separate ASGI server like Uvicorn (or others like Daphne or Hypercorn).
Flask: You run the app directly via python app.py, and Flask uses its internal server for handling requests.
FastAPI: You run the app with Uvicorn like uvicorn app:app, as FastAPI needs an ASGI server to handle requests properly.

# Pydantic with FastAPI for Data Validation

## Introduction

Pydantic is a data validation and parsing library used in FastAPI for ensuring the correct structure of incoming request data. It leverages Python's type annotations to perform automatic data validation and parsing. FastAPI uses Pydantic models to validate request bodies and responses, making it easier to ensure that the data follows the required structure and types.

In this example, we'll create a FastAPI application that receives a POST request containing a complex JSON body, validates it using Pydantic models, and returns the validated data.

## FastAPI Backend Code

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import random

app = FastAPI()

# Define a Pydantic model for Item (nested object)
class Item(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

# Define a Pydantic model for Address (nested object)
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

# Define a Pydantic model for Customer (nested object)
class Customer(BaseModel):
    name: str
    email: EmailStr  # Email validation
    phone: Optional[str] = None  # Optional field (phone number)

# Define a Pydantic model for the Order (complex model with nested objects)
class Order(BaseModel):
    order_id: int
    customer: Customer
    shipping_address: Address
    items: List[Item]
    total_price: float

# Endpoint to accept POST requests with complex data
@app.post("/create_order/", response_model=Order)
async def create_order(order: Order):
    return order  # Just return the validated order data
