# `exchange_derivatives` Sub-package Documentation

## Usage Example
```python
# import sub-package
from cdc.qa.apis import exchange_derivatives

# create `DerivativesApi` instance
api = exchange_derivatives.DerivativesApi(api_key="your key", secret_key="your secret")

# call a RESTful API with the instance
print(api.rest.public.instruments.get_instruments())

# call a WebSocket API with the instance
api.ws.user.connect()
api.ws.user.public.send_get_instruments()
print(api.ws.user.public.get_get_instruments_msgs())
api.ws.user.disconnect()
```

>[TODO] Add a list of implemented APIs
