from cdc.qa.apis import exchange_fe


def test_instantiate():
    assert exchange_fe.FeExchangeService()
