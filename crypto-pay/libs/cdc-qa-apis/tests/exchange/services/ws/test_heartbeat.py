from cdc.qa.apis import exchange
import time
import json
import pytest


@pytest.mark.slow
def test_heartbeat_auto_respond():
    client = exchange.ws.ExchangeWebSocketClient(host="wss://uat-stream.3ona.co/v2/user")
    with client as client:
        time.sleep(5)
        assert not client._recv_messages
        assert json.loads(client._sent_messages[-1]).get("method") == "public/respond-heartbeat"


@pytest.mark.slow
def test_heartbeat_no_auto_respond():
    client = exchange.ws.ExchangeWebSocketClient(
        host="wss://uat-stream.3ona.co/v2/user",
        heartbeat_auto_respond=False,
    )
    with client as client:
        time.sleep(5)
        assert not client._recv_messages
        assert not client._sent_messages


@pytest.mark.slow
def test_heartbeat_save_message():
    client = exchange.ws.ExchangeWebSocketClient(
        host="wss://uat-stream.3ona.co/v2/user",
        heartbeat_save_message=True,
    )
    with client as client:
        time.sleep(5)
        assert json.loads(client._recv_messages[-1]).get("method") == "public/heartbeat"
        assert json.loads(client._sent_messages[-1]).get("method") == "public/respond-heartbeat"
