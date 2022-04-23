from dataclasses import dataclass


@dataclass
class Auth:
    consumer_key: str
    consumer_secret: str
    token: str
    secret: str
