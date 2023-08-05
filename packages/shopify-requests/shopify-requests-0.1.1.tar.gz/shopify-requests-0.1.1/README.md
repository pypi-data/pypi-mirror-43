# Shopify Requests
[![pipeline status](https://gitlab.com/perobertson/shopify-requests/badges/master/pipeline.svg)](https://gitlab.com/perobertson/shopify-requests/commits/master)
[![coverage report](https://gitlab.com/perobertson/shopify-requests/badges/master/coverage.svg)](https://gitlab.com/perobertson/shopify-requests/commits/master)

The ShopifyRequests library is a wrapper around the python requests library.
Its main purpose is to remove the boiler plate code needed to do basic API calls to Shopify.

## Usage
```python
from shopify_requests import RestClient

client = RestClient('foo.myshopify.com', access_token='abc123')
response = client.get('shop.json')
```
The `RestClient` sets up the session with the correct auth and accept headers.
Multiple requests with the client will reuse the same TCP connection.
