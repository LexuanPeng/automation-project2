from cdc.qa.apis import exchange


def test_instantiate():
    assert exchange.ExchangeApi(api_key="", secret_key="")
