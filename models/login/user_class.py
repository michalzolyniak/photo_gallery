import flask
from dataclasses import dataclass


@dataclass
class User:
    name: str | None = None

    @property
    def avatar(self) -> str:
        return f"{self.name}.jpg"

    @property
    def is_login(self):
        return self.name is not None

    @classmethod
    def current(cls):
        return cls(
            name=flask.session.get('name')
        )
