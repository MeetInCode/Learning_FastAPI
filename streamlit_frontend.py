import streamlit as st
import requests

# Streamlit app title
st.title("FastAPI + Streamlit Example")

# A simple text input for item details
name = st.text_input("Item Name")
description = st.text_area("Item Description")
price = st.number_input("Item Price", min_value=0.0)

# If the user presses the "Create Item" button
if st.button("Create Item"):
    # Prepare the payload to send to FastAPI
    item_data = {
        "name": name,
        "description": description,
        "price": price
    }
    
    # Send a POST request to FastAPI backend
    response = requests.post("http://127.0.0.1:8000/items/", json=item_data)

    # Show the response from FastAPI
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to create the item.")

# Button to fetch a specific item by its ID
item_id = st.number_input("Enter Item ID", min_value=1)
if st.button("Get Item Details"):
    # Send a GET request to fetch the item details
    response = requests.get(f"http://127.0.0.1:8000/items/{item_id}")
    
    if response.status_code == 200:
        item = response.json()
        st.write(f"Item ID: {item['item_id']}")
        st.write(f"Query: {item.get('square', 'No query provided')}")
    else:
        st.error("Failed to fetch item details.")
