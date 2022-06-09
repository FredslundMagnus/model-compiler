class Error:
    def __init__(self, *args: str) -> None:
        self.message = args[0]

class UnexpectedCharacterError(Error):
    def __init__(self, got: str, expected: str) -> None:
        self.message = f"Unexpected character '{got}', expected '{expected}'"