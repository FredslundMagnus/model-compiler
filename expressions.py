from __future__ import annotations
from typing import Iterable, TypeVar
from errors import UnexpectedCharacterError
from tokens import *


class Expression:
    @staticmethod
    def eat(self, tokens: Iterable[Token], state: dict) -> tuple[Expression | None, Error | None]:
        token = next(tokens)
        match token:
            case ImportKeywordToken(_):
                expression, error = ImportExpression.of(token, tokens)
                return expression, error
            case NewLineToken(_):
                return NewLinesExpression(tokens), None
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
    def __init__(self, import_token: ImportKeywordToken, space_token: SpaceToken, string_token: StringToken) -> None:
        self.import_token = import_token
        self.space_token = space_token
        self.string_token = string_token
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
            return UnexpectedCharacterError(token.value, "a string", [import_token, space_token, *collectUntilType(tokens, NewLineToken)])
        strings, token = getAllOfType(tokens, StringToken, [token])
        if strings[0].value != strings[-1].value:
            return UnexpectedCharacterError(token.value, strings[0].value, [import_token, space_token, *collectUntilType(tokens, NewLineToken)])
        string = "".join(s.value for s in strings)
        string_token = StringToken(string)
        if isinstance(token, NewLineToken):
            return ImportExpression(import_token, space_token, string_token), None
        spaces, token = getAllOfType(tokens, SpaceToken)
        
        

class NewLinesExpression(Expression):
    pass
