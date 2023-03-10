# `Onex Exchange` Sub-package Documentation

## Usage Example
```python
# import sub-package
from cdc.qa.apis import exchange_oex

# create `OneExchangeApi` instance
api = exchange_oex.OneExchangeApi(api_key="your key", secret_key="your secret")

# call a RESTful API with the instance
print(api.rest.public.instruments.get_instruments())

# call a WebSocket API with the instance
api.ws.user.connect()
api.ws.user.public.send_get_instruments()
print(api.ws.user.public.get_get_instruments_msgs())
api.ws.user.disconnect()
```
