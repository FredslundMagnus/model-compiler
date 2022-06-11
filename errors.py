
from __future__ import annotations
from typing import TypeVar


# Token = TypeVar("Token")

class Error(BaseException):
    def __init__(self, *args: str, rest: list | None = None) -> None:
        self.message = args[0]
        self.rest = rest

class SyntaxError(Error):
    def __init__(self, got: object, expected: object) -> None:
        self.got = got
        self.expected = expected
        self.message = f"Unexpected character '{got.value}', expected '{expected.__name__}'"
    def __repr__(self) -> str:
        return f"SyntaxError(got={self.got}, expected={self.expected.__name__})"

class TypeAlreadyDefinedError(Error):
    def __init__(self, name: str, current: str, next: str, rest: list | None = None) -> None:
        if current == next:
            self.message = f"Type '{name}' already defined as '{current}', cannot redefine as '{current}'"
        else:
            self.message = f"Type '{name}' already defined as '{current}', cannot define as '{next}'"
        self.rest = rest