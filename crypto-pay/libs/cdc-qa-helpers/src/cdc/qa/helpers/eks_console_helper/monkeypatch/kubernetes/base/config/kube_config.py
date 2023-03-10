from kubernetes.config.kube_config import KubeConfigLoader

original__load_cluster_info = KubeConfigLoader._load_cluster_info


def patched__load_cluster_info(self):
    original__load_cluster_info(self)
    if "tls-server-name" in self._cluster:
        self.tls_server_name = self._cluster["tls-server-name"]


KubeConfigLoader._load_cluster_info = patched__load_cluster_info


original__set_config = KubeConfigLoader._set_config


def patched__set_config(self, client_configuration, *args, **kwargs):
    original__set_config(self, client_configuration, *args, **kwargs)
    keys = ["host", "ssl_ca_cert", "cert_file", "key_file", "verify_ssl", "tls_server_name"]
    for key in keys:
        if key in self.__dict__:
            setattr(client_configuration, key, getattr(self, key))


KubeConfigLoader._set_config = patched__set_config
