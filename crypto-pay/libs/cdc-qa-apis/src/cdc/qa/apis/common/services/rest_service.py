from dataclasses import dataclass, field
import requests


@dataclass(frozen=True)
class RestService:
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)
