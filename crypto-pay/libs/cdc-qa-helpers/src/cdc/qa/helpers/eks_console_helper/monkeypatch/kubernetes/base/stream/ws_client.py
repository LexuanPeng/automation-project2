from kubernetes.stream import ws_client

from kubernetes.stream.ws_client import enableTrace, ssl, certifi, WebSocket, websocket_proxycare


def patched_create_websocket(configuration, url, headers=None):
    enableTrace(False)

    # We just need to pass the Authorization, ignore all the other
    # http headers we get from the generated code
    header = []
    if headers and "authorization" in headers:
        header.append("authorization: %s" % headers["authorization"])
    if headers and "sec-websocket-protocol" in headers:
        header.append("sec-websocket-protocol: %s" % headers["sec-websocket-protocol"])
    else:
        header.append("sec-websocket-protocol: v4.channel.k8s.io")

    if url.startswith("wss://") and configuration.verify_ssl:
        ssl_opts = {
            "cert_reqs": ssl.CERT_REQUIRED,
            "ca_certs": configuration.ssl_ca_cert or certifi.where(),
        }
        if configuration.assert_hostname is not None:
            ssl_opts["check_hostname"] = configuration.assert_hostname
    else:
        ssl_opts = {"cert_reqs": ssl.CERT_NONE}

    if configuration.cert_file:
        ssl_opts["certfile"] = configuration.cert_file
    if configuration.key_file:
        ssl_opts["keyfile"] = configuration.key_file
    if configuration.tls_server_name:
        ssl_opts["server_hostname"] = configuration.tls_server_name

    websocket = WebSocket(sslopt=ssl_opts, skip_utf8_validation=False)
    connect_opt = {"header": header}

    if configuration.proxy or configuration.proxy_headers:
        connect_opt = websocket_proxycare(connect_opt, configuration, url, headers)

    websocket.connect(url, **connect_opt)
    return websocket


ws_client.create_websocket = patched_create_websocket
