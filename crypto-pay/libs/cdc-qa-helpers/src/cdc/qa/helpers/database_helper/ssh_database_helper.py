import sshtunnel
from .database_helper import DatabaseHelper


class SSHDatabaseHelper(DatabaseHelper):
    """A database helper connected through SSH tunnel."""

    # ssh variables
    SSH_HOST: str
    SSH_PORT: int = 22
    SSH_USERNAME: str
    SSH_REMOTE_HOST: str
    SSH_REMOTE_PORT: int

    # database variables
    DB_DIALECT: str
    DB_NAME: str = ""
    DB_USERNAME: str
    DB_PASSWORD: str

    def __init__(self):
        # open ssh tunnel
        tunnel = self.create_tunnel(
            host=self.SSH_HOST,
            port=self.SSH_PORT,
            username=self.SSH_USERNAME,
            remote_host=self.SSH_REMOTE_HOST,
            remote_port=self.SSH_REMOTE_PORT,
        )
        tunnel.start()

        # connect to database
        self.engine = self.create_engine(
            dialect=self.DB_DIALECT,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            database=self.DB_NAME,
        )

    @staticmethod
    def create_tunnel(
        host: str,
        port: int,
        *,
        username: str,
        remote_host: str,
        remote_port: int,
    ) -> sshtunnel.SSHTunnelForwarder:
        tunnel = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=(host, port),
            ssh_username=username,
            remote_bind_address=(remote_host, remote_port),
        )
        return tunnel
