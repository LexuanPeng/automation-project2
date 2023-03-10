from kubernetes.client.configuration import Configuration


original___init__ = Configuration.__init__


def patched___init__(self, *args, **kwargs):
    original___init__(self, *args, **kwargs)
    self.tls_server_name = None
    """SSL/TLS Server Name Indication (SNI)
        Set this to the SNI value expected by Kubernetes API.
    """


Configuration.__init__ = patched___init__
