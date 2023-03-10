from __future__ import annotations

import sqlalchemy
from abc import ABC
from typing import Optional


class DatabaseHelper(ABC):
    @staticmethod
    def create_engine(
        dialect: str,
        host: str,
        port: int,
        *,
        username: str,
        password: str = "",
        database: str = "",
        connect_args: Optional[dict] = None,
    ) -> sqlalchemy.engine.Engine:
        """Create a SQLAlchemy engine.

        Args:
            dialect (str): dialect to use.
            host (str): host of DB.
            port (int): port of DB.
            username (str): username of DB.
            password (str, optional): password of DB. Defaults to "".
            database (str, optional): name of database. Defaults to "".
            connect_args (Optional[dict], optional): `connect_args` to pass to SQLAlchemy. Defaults to None.

        Returns:
            sqlalchemy.engine.Engine: a SQLAlchemy engine.
        """
        connect_args = connect_args or {}
        connect_url = f"{dialect}://{username}:{password}@{host}:{port}/{database}"
        return sqlalchemy.create_engine(connect_url, connect_args=connect_args)
