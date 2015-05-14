# Python SDK

[Website] (http://molt.in)
License: MIT
Version: 1

## Description

Python SDK for the Moltin eCommerce API

## Installation

    pip install moltin

## Usage

Initialise the Moltin object with your `client_id` and `client_secret`, and optionally a specific API version (e.g. `v1`).
    
    from moltin.moltin import *
    
    m = Moltin("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET"[, version="v1"])
    

### Authentication

To Authenticate, call the authenticate method.

    m.authenticate()
    
If authenticating with a username/password:

    m.authenticate(username="your_username", password="your_password")
    
    refresh_token = m.refresh_token  # used for re-authenticating without user/pass
    
If authenticating with a refresh_token:

    m.authenticate(refresh_token="token")
    
### Making API Calls

The SDK covers abstracts away most of the API endpoints.

Example:

    products = Product(m)  #  pass in the authenticated Moltin object
    
    params = {
        "sku": "123456789",
        "title": "My first product",
        "slug": "my-first-product",
        "price": 9.99,
        "status": 1,
        "category": 2,
        "stock_level": 15,
        "stock_status": 6,
        "description": "This is my first product on Moltin",
        "requires_shipping": 0
    }
    
    products.create(params)


