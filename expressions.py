from __future__ import annotations
from typing import Iterable, TypeVar
from errors import UnexpectedCharacterError
from tokens import *


class Expression:
    @staticmethod
    def eat(tokens: Iterable[Token], state: dict) -> tuple[Expression | None, Error | None]:
        token = next(tokens)
        match token:
            case ImportKeywordToken():
                return ImportExpression.of(token, tokens)
            case NewLineToken():
                return NewLinesExpression(token)

    def format(self) -> str:
        return str(self)

T = TypeVar("T")

def getAllOfType(tokens: Iterable[Token], type: type[T], result: list[T] | None = None) -> tuple[list[T], Token]:
    if result is None:
        result = []
    while True:
        token = next(tokens)
        if not isinstance(token, type):
            break
        result.append(token)
    return result, token

def collectUntilType(tokens: Iterable[Token], type: type[T], result: list[T] | None = None) -> list[Token]:
    if result is None:
        result = []
    while True:
        token = next(tokens)
        result.append(token)
        if isinstance(token, type):
            break
    return result

class ImportExpression(Expression):
    def __init__(self, import_token: ImportKeywordToken, space_token: SpaceToken, string_token: StringToken, end_line: NewLineToken) -> None:
        self.import_token = import_token
        self.space_token = space_token
        self.string_token = string_token
        self.end_line = end_line

    @staticmethod
    def of(token: Token, tokens: Iterable[Token]) -> Error | Expression:
        import_token = token
        spaces, token = getAllOfType(tokens, SpaceToken)
        if len(spaces) == 0:
            if isinstance(token, NewLineToken):
                return UnexpectedCharacterError(token.value, "a string", [import_token, token])
            return UnexpectedCharacterError(token.value, "a space", [import_token, *collectUntilType(tokens, NewLineToken)])
        space = "".join(s.value for s in spaces)
        space_token = SpaceToken(space)
        if not isinstance(token, StringToken):
            if isinstance(token, NewLineToken):
                return UnexpectedCharacterError(token.value, "a string", [import_token, space_token, token])
            return UnexpectedCharacterError(token.value, "a string", [import_token, space_token, token, *collectUntilType(tokens, NewLineToken)])
        strings, token = getAllOfType(tokens, StringToken, [token])
        if strings[0].value != strings[-1].value:
            return UnexpectedCharacterError(token.value, strings[0].value, [import_token, space_token, *collectUntilType(tokens, NewLineToken)])
        string = "".join(s.value for s in strings)
        string_token = StringToken(string)
        if isinstance(token, NewLineToken):
            return ImportExpression(import_token, space_token, string_token, token)
        if not isinstance(token, SpaceToken):
            return UnexpectedCharacterError(token.value, "a new line", [import_token, space_token, string_token, token, *collectUntilType(tokens, NewLineToken)])
        spaces, token = getAllOfType(tokens, SpaceToken, [token])

        space = "".join(s.value for s in spaces)
        if isinstance(token, NewLineToken):
            return ImportExpression(import_token, space_token, string_token, NewLineToken(space + "\n"))
        return UnexpectedCharacterError(token.value, "a new line", [import_token, space_token, string_token, SpaceToken(space), token, *collectUntilType(tokens, NewLineToken)])

    def __str__(self) -> str:
        return f"{self.import_token.value}{self.space_token.value}{self.string_token.value}{self.end_line.value}"

    def format(self) -> str:
        return f"{self.import_token.value} {self.string_token.value}\n"
        

class NewLinesExpression(Expression):
    def __init__(self, value: NewLineToken) -> None:
        self.end_line = value

    def __str__(self) -> str:
        return self.end_line.value
