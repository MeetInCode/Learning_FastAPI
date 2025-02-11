In FastAPI, **Uvicorn**  is the  **ASGI server**  that is responsible for handling requests and responses. While Flask uses a built-in WSGI server (which is simple and sufficient for development), FastAPI, being an ASGI framework, requires a separate ASGI server like Uvicorn (or others like Daphne or Hypercorn).
Flask: You run the app directly via **python app.py** , and Flask uses its internal server for handling requests.
FastAPI: You run the app with Uvicorn like **uvicorn app:app** , as FastAPI needs an ASGI server to handle requests properly.

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


```


Explanation
### 1. Pydantic Models:
Item: This model represents a product being ordered and includes fields like name, description, price, and quantity.
Address: This model holds the shipping address, with fields like street, city, state, and zip_code.
Customer: Represents the customer placing the order. It contains fields such as name, email (validated using EmailStr), and an optional phone number.
Order: This is the main model that ties everything together, including order_id, customer, shipping_address, items, and total_price.
### 2. POST Endpoint:
The create_order endpoint accepts a POST request at /create_order/.
The request body must match the structure of the Order Pydantic model, including the nested Customer, Address, and Item models.
FastAPI automatically validates the incoming JSON against the Order model. If the data doesn't conform to the expected types or structure, FastAPI will return a validation error.
### 3. Validation:
FastAPI will ensure that the request body contains a valid email address, the price is a floating-point number, quantities are integers, and required fields are present. If the validation fails, FastAPI will return an appropriate error response.
### 4. Response:
After validation, FastAPI returns the Order object, including the customer details, items, and shipping address, in the response body.


## Testing the Endpoint
You can test this FastAPI application by sending a POST request with a JSON body that matches the Order model. Below is an example of how the request body might look:

```json
{
  "order_id": 123,
  "customer": {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "phone": "123-456-7890"
  },
  "shipping_address": {
    "street": "123 Main St",
    "city": "Somewhere",
    "state": "CA",
    "zip_code": "98765"
  },
  "items": [
    {
      "name": "Laptop",
      "description": "High-end gaming laptop",
      "price": 1299.99,
      "quantity": 1
    },
    {
      "name": "Mouse",
      "description": "Wireless mouse",
      "price": 29.99,
      "quantity": 2
    }
  ],
  "total_price": 1359.97
}
```

# Type Hints

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the request body
class Item(BaseModel):
    name: str  # Type hint: this should be a string
    price: float  # Type hint: this should be a float
    description: str = "No description"  # Optional field with a default value

# Define an endpoint that takes an 'Item' and returns a greeting with its name and price
@app.post("/items/")
async def create_item(item: Item) -> dict:
    # The function will receive an 'Item' and return a dictionary
    return {"message": f"Item {item.name} is priced at ${item.price}", "item": item.dict()}

```

###  create_item(item: Item) -> dict:

(item: Item)
This part defines the input parameters of the function.

item: This is the parameter name of the function. It will hold the data sent by the client.

Item: This is a type hint that indicates the expected type for the item parameter. In this case, Item is a Pydantic model, and FastAPI uses this model to validate and parse the incoming request data.

### How it works:
 When a client sends a POST request to the /items/ endpoint, FastAPI will automatically validate that the data sent in the body matches the structure defined in the Item model. If the structure is correct, it will be parsed into an instance of Item and passed to the create_item function as the item parameter.


-> dict:

This part is the return type hint. It indicates that the create_item function will return a dictionary (dict).
### How it works:
 The function returns a Python dictionary. In this case, the dictionary includes a message and the item data.
### Why dict:
 We are returning a dictionary to format the response that will be sent back to the client. The dictionary contains key-value pairs, which FastAPI converts to a JSON response automatically.



# Demonstrating Asynchronous Support in FastAPI

We’ll create an endpoint that simulates a time-consuming operation (e.g., fetching data from an external API or performing a heavy computation). The async keyword allows FastAPI to handle other requests while waiting for the operation to complete.

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# Simulate a time-consuming async task
async def fake_db_call():
    await asyncio.sleep(2)  # Simulate a 2-second delay (e.g., network request or DB query)
    return {"message": "Data fetched successfully"}

@app.get("/async_example/")
async def get_data():
    data = await fake_db_call()  # Await the asynchronous function to finish
    return data
```

# Automatic Documentation

