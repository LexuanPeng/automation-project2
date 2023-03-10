from cdc.qa.apis import exchange_derivatives


def test_instantiate():
    assert exchange_derivatives.DerivativesApi(api_key="", secret_key="")
