from __future__ import annotations
from typing import Iterable, TypeVar
from errors import SyntaxError
from tokens import *


class Expression:
    @staticmethod
    def eat(tokens: Iterable[Token]) -> Expression:
        token = next(tokens)
        match token:
            case ImportKeywordToken():
                return ImportExpression.of(token, tokens)
            case NewLineToken():
                return NewLinesExpression.of(token, tokens)
            case EnumKeywordToken():
                return EnumExpression.of(token, tokens)
            case TypedefKeywordToken():
                return TypedefExpression.of(token, tokens)
            case ModelKeywordToken():
                return ModelExpression.of(token, tokens)
            case SpaceToken():
                return IndentedExpression.of(token, tokens)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

T = TypeVar("T")

def get(tokens: Iterable[Token], type: type[T]) -> T:
    token = next(tokens)
    if isinstance(token, type):
        return token
    else:
        raise SyntaxError(token, type)

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")

def rest_of_line(tokens) -> list[Token]:
    _tokens = []
    for token in tokens:
        if isinstance(token, NewLineToken):
            break
        _tokens.append(token)
    return _tokens

def match_2(tokens: Iterable[Token], type1: type[T1], type2: type[T2]) -> tuple[T1, T2]:
    return get(tokens, type1), get(tokens, type2)

def match_3(tokens: Iterable[Token], type1: type[T1], type2: type[T2], type3: type[T3]) -> tuple[T1, T2, T3]:
    return get(tokens, type1), get(tokens, type2), get(tokens, type3)

def match_4(tokens: Iterable[Token], type1: type[T1], type2: type[T2], type3: type[T3], type4: type[T4]) -> tuple[T1, T2, T3, T4]:
    return get(tokens, type1), get(tokens, type2), get(tokens, type3), get(tokens, type4)

def match_5(tokens: Iterable[Token], type1: type[T1], type2: type[T2], type3: type[T3], type4: type[T4], type5: type[T5]) -> tuple[T1, T2, T3, T4, T5]:
    return get(tokens, type1), get(tokens, type2), get(tokens, type3), get(tokens, type4), get(tokens, type5)

def match_6(tokens: Iterable[Token], type1: type[T1], type2: type[T2], type3: type[T3], type4: type[T4], type5: type[T5], type6: type[T6]) -> tuple[T1, T2, T3, T4, T5, T6]:
    return get(tokens, type1), get(tokens, type2), get(tokens, type3), get(tokens, type4), get(tokens, type5), get(tokens, type6)

def match_7(tokens: Iterable[Token], type1: type[T1], type2: type[T2], type3: type[T3], type4: type[T4], type5: type[T5], type6: type[T6], type7: type[T7]) -> tuple[T1, T2, T3, T4, T5, T6, T7]:
    return get(tokens, type1), get(tokens, type2), get(tokens, type3), get(tokens, type4), get(tokens, type5), get(tokens, type6), get(tokens, type7)

def match(tokens: Iterable[Token], types: tuple[type[T1], ...]) -> tuple[T1, ...]:
    return None

class ImportExpression(Expression):
    def __init__(self, string_token: StringToken) -> None:
        self.string_token = string_token

    @staticmethod
    def of(token: ImportKeywordToken, tokens: Iterable[Token]) -> ImportExpression:
        _, string_token, _ = match_3(tokens, SpaceToken, StringToken, NewLineToken)
        return ImportExpression(string_token)

    def __str__(self) -> str:
        return f"import {self.string_token.value}"
        

class NewLinesExpression(Expression):
    @staticmethod
    def of(token: NewLineToken, tokens: Iterable[Token]) -> NewLinesExpression:
        return NewLinesExpression()

    def __str__(self) -> str:
        return ""

class EnumExpression(Expression):
    def __init__(self, name_token: NameToken) -> None:
        self.name_token = name_token

    @staticmethod
    def of(token: EnumKeywordToken, tokens: Iterable[Token]) -> EnumExpression:
        _, name_token, _ = match_3(tokens, SpaceToken, NameToken, NewLineToken)
        return EnumExpression(name_token)

    def __str__(self) -> str:
        return f"enum {self.name_token.value}"
        

class TypedefExpression(Expression):
    def __init__(self, name_token_1: NameToken, name_token_2: ClassToken | NameToken) -> None:
        self.name_token_1 = name_token_1
        self.name_token_2 = name_token_2

    @staticmethod
    def of(token: TypedefKeywordToken, tokens: Iterable[Token]) -> TypedefExpression:
        _, name_token_1, _, _, _, name_token_2, _ = match_7(tokens, SpaceToken, NameToken, SpaceToken, EqualSymbolToken, SpaceToken, ClassToken | NameToken, NewLineToken)
        return TypedefExpression(name_token_1, name_token_2)

    def __str__(self) -> str:
        return f"typedef {self.name_token_1.value} = {self.name_token_2.value}"
        
class ModelExpression(Expression):
    def __init__(self, class_token: NameToken, parameters: list[tuple[NameToken, NameToken | ClassToken]]) -> None:
        self.class_token = class_token
        self.parameters = parameters
        
    @staticmethod
    def of(token: ModelKeywordToken, tokens: Iterable[Token]) -> ModelExpression:
        _, class_token, _, end_paren_or_name = match_4(tokens, SpaceToken, NameToken, StartParenthesesSymbolToken, EndParenthesesSymbolToken | NameToken)

        parameters = []
        while isinstance(end_paren_or_name, NameToken):
            _, _, _type, end_paren_or_comma = match_4(tokens, ColonSymbolToken, SpaceToken, NameToken | ClassToken, EndParenthesesSymbolToken | CommaSymbolToken)
            parameters.append((end_paren_or_name, _type))
            if isinstance(end_paren_or_comma, EndParenthesesSymbolToken):
                break
            get(tokens, SpaceToken)
            get(tokens, NameToken | ClassToken)
        match_2(tokens, ColonSymbolToken, NewLineToken)
        return ModelExpression(class_token, parameters)

    def __str__(self) -> str:
        params = ', '.join(f'{parameter[0].value}: {parameter[1].value}' for parameter in self.parameters)
        return f"model {self.class_token.value}({params}):"

class IndentedExpression(Expression):
    def __init__(self, spaces: int, name_token: NameToken, type_token: NameToken | ClassToken, value: list[Token] | None = None) -> None:
        self.spaces = spaces
        self.name_token = name_token
        self.type_token = type_token
        self.value = value

    @staticmethod
    def of(token: SpaceToken, tokens: Iterable[Token]) -> IndentedExpression:
        spaces = len(token.value)
        name_token, _, _, type_token, new_line_or_space = match_5(tokens, NameToken, ColonSymbolToken, SpaceToken, NameToken | ClassToken, NewLineToken | SpaceToken)
        if isinstance(new_line_or_space, NewLineToken):
            return IndentedExpression(spaces, name_token, type_token)
        _, _ = match_2(tokens, EqualSymbolToken, SpaceToken)
        value = rest_of_line(tokens)
        return IndentedExpression(spaces, name_token, type_token, value=value)


    def __str__(self) -> str:
        if self.value is None:
            return f"    {self.name_token.value}: {self.type_token.value}"
        return f"    {self.name_token.value}: {self.type_token.value} = " + ''.join(token.value for token in self.value)