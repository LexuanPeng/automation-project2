# Defining an API
This document describes how to define an API with the shared models provided in this package.
## Defining a RESTful API
Using the [`public/get-book`](https://exchange-docs.crypto.com/spot/index.html?python#public-get-book) API from Exchange V2 API as an example, given the following information:

#### Request Sample
|  |  |
| - | - |
| Path | public/get-book?instrument_name=BTC_USDT&depth=10 |
| Method | GET |

#### Response Sample
```json
{
  "code":0,
  "method":"public/get-book",
  "result":{
    "bids":[[9668.44,0.006325,1.0],[9659.75,0.006776,1.0],[9653.14,0.011795,1.0],[9647.13,0.019434,1.0],[9634.62,0.013765,1.0],[9633.81,0.021395,1.0],[9628.46,0.037834,1.0],[9627.6,0.020909,1.0],[9621.51,0.026235,1.0],[9620.83,0.026701,1.0]],
    "asks":[[9697.0,0.68251,1.0],[9697.6,1.722864,2.0],[9699.2,1.664177,2.0],[9700.8,1.824953,2.0],[9702.4,0.85778,1.0],[9704.0,0.935792,1.0],[9713.32,0.002926,1.0],[9716.42,0.78923,1.0],[9732.19,0.00645,1.0],[9737.88,0.020216,1.0]],
    "t":1591704180270
  }
}
```

We may define this API with the follow steps:

### Step 1: Define the request/response data models
Before defining the API, we will have to model the request and response data of this API. We will be utilizing [`pydantic`](https://pydantic-docs.helpmanual.io/) as our data modeling tool for data validation.

This API uses query parameters. We may model it using `BaseModel` from `pydantic`:
```python
from pydantic import BaseModel
from typing import Optional

class GetBookRequestParams(BaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    depth: Optional[int] = Field(
        default=None, description="Number of bids and asks to return (up to 150)", ge=0, le=150
    )
```

The response is modelled like this:
```python
from pydantic import BaseModel
from typing import List, Optional

class GetBookResultData(BaseModel):
    bids: List[List[int]] = Field(description="Bids array: [0] = Price, [1] = Quantity, [2] = Number of Orders")
    asks: List[List[int]] = Field(description="Asks array: [0] = Price, [1] = Quantity, [2] = Number of Orders")
    t: int = Field(description="Timestamp of the data")


class GetBookResult(BaseModel):
    instrument_name: str = Field()
    depth: int = Field()
    data: Optional[List[GetBookResultData]] = Field(default=None)


class GetBookResponse(BaseModel):
    code: int = Field(description="Response code")
    method: str = Field(description="Method invoked")
    result: GetBookResult = Field()
```


### Step 2: Define the API
With the data models defined, we may use them with the `RestApi` class from our common models:

```python
from cdc.qa.apis.common.models.rest_api import RestApi, HttpMethods

class GetBookApi(RestApi):
    """Fetches the public order book for a particular instrument and depth"""

    path = "public/get-book"
    method = HttpMethods.GET
    request_params_type = GetBookRequestParams
    response_type = GetBookResponse
```

Now this API should be ready to use:
```python
api = GetBookApi(host="https://uat-api.3ona.co/v2/")
params = GetBookRequestParams(instrument_name="BTC_USDT", depth=100).dict(exclude_none=True)
response = GetBookResponse.parse_raw(b=api.call(params=params).content)
print(response.code)
```

### (Optional) Step 3: Define the API Service
Our common models also provides a `RestService` class that could be used to group multiple `Api` under a single `Service` object with methods for easier use of the API.
```python
from cdc.qa.apis.common.services.rest_service import RestService

class BookService(RestService):
    def get_book(self, instrument_name: str, depth: int = None) -> GetBookResult:
        api = GetBookApi(host=self.host, _session=self.session)
        params = GetBookRequestParams(instrument_name=instrument_name, depth=depth).dict(exclude_none=True)
        response = GetBookResponse.parse_raw(b=api.call(params=params).content)

        return response.result
```
Now the service can be used simply by:
```python
service = BookService(host="https://uat-api.3ona.co/v2/")
print(service.get_book(instrument_name="BTC_USDT", depth=100))
```


## Defining a WebSocket API
WIP
