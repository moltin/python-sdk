Python SDK
==========

[Website] (http://molt.in)

License: MIT

Version: 1.0

Description
-----------

Python SDK for the Moltin eCommerce API

Installation
------------

::

    $ pip install moltin

Usage
-----

Initialise the Moltin object with your ``client_id`` and
``client_secret``, and optionally a specific API version (e.g. ``v1``).

.. code:: python

        from moltin.moltin import Moltin
        
        m = Moltin("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET"[, version="v1"])

Authentication
~~~~~~~~~~~~~~

To Authenticate, call the authenticate method.

.. code:: python

        access_token = m.authenticate()
        # This returns an AccessToken object
        # access_token.token: the token string
        # access_token.has_expired(): has the token expired
        #
        # The access token is automatically passed to subsequent requests, 
        # so you shouldn't normally need to use the returned token
        # except when persisting in a session or db

Authenticating with a username/password:

.. code:: python

        access_token, refresh_token = m.authenticate(username="your_username", password="your_password")
        # refresh_token is a RefreshToken object.
        # refresh_token.token: the token string
        # Use this to re-authenticate without needing a user/pass

Authenticating with a refresh\_token string:

.. code:: python

        access_token = m.authenticate(refresh_token="refresh_token_string")

Once authenticated, the access token is automatically passed to every
request. If you need to pass in a previously stored token, use:

.. code:: python

    m.set_access_token("access_token_string")

before making a request

Making API Calls
~~~~~~~~~~~~~~~~

There's an easy way to interact with most endpoints:

.. code:: python

    product = m.Product         # Creates a product wrapper
    product.list()              # lists all products
    product.create(params)      # creates a product, params passed as a dict
    product.find(5)             # finds product with id = 5
    product.find_by(params)     # finds a single product by params passed as a dict,
                                # e.g. {"title": "Banana"}
    product.update(5, params)   # updates product with id = 5 with new params
    product.remove(5)           # removes product with id = 5

The SDK also offers a way to make get, post, put and delete requests to
API endpoints directly

For example:

.. code:: python

    product = m.get('products/5')  # get product with id = 5 
    new_product = m.post('products', {
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
    })  # create a new product
    m.put('products/5', params)  # update product with id = 5
    m.delete('products/5')  # delete product with id = 5

For more examples, see the full API docs.
