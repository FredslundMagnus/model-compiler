

class Error:
    def __init__(self, *args: str, rest: list | None = None) -> None:
        self.message = args[0]
        self.rest = rest

class UnexpectedCharacterError(Error):
    def __init__(self, got: str, expected: str, rest: list | None = None) -> None:
        self.message = f"Unexpected character '{got}', expected '{expected}'"
        self.rest = rest

class TypeAlreadyDefinedError(Error):
    def __init__(self, name: str, current: str, next: str, rest: list | None = None) -> None:
        if current == next:
            self.message = f"Type '{name}' already defined as '{current}', cannot redefine as '{current}'"
        else:
            self.message = f"Type '{name}' already defined as '{current}', cannot define as '{next}'"
        self.rest = rest