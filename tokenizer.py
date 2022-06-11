from typing import Iterator
from tokens import ClassToken, CommaSymbolToken, EndTypeParenthesesSymbolToken, NameToken, NewLineToken, SpaceToken, StartTypeParenthesesSymbolToken, StringToken, Token


def tokenize_1(text: str) -> Iterator[Token]:
    """
    Parses the text file and returns a list tokens.
    """
    temp = ""
    
    for char in text:
        match char:
            case '\n' | ' ' | '\t' | "(" | ")" | "," | "." | ":" | ";" | "=" | "{" | "}" | "[" | "]" | "\"" | "'" | "<" | ">":
                if temp:
                    yield Token.of(temp)
                    temp = ""
                yield Token.of(char)
            case _:
                temp += char
    if temp:
        yield Token.of(temp)
    yield Token.of("\n")

def tokenize_2(text: str) -> Iterator[Token]:
    current: SpaceToken | StringToken | None = None
    for token in tokenize_1(text):
        match token, current:
            case NewLineToken(new), SpaceToken(cur):
                yield NewLineToken(cur + new)
                current = None
            case StringToken(_), None:
                current = token
            case SpaceToken(_), None:
                current = token
            case SpaceToken(new), SpaceToken(cur):
                current = SpaceToken(cur + new)
            case StringToken(new), StringToken(cur):
                current = StringToken(cur + new)
            case StringToken(_), _:
                yield current
                current = token
            case SpaceToken(_), _:
                yield current
                current = token
            case _, None:
                yield token
            case _, _:
                yield current
                current = None
                yield token


def tokenize(text: str) -> Iterator[Token]:
    depth = 0
    current: NameToken | ClassToken | None = None
    for token in tokenize_2(text):
        match token, current:
            case NameToken(_) | ClassToken(_), None:
                depth = 0
                current = token
            case StartTypeParenthesesSymbolToken(_), NameToken(val) | ClassToken(val):
                depth = depth + 1
                current = ClassToken(val + "<")
            case EndTypeParenthesesSymbolToken(_), NameToken(val) | ClassToken(val) if depth > 0:
                depth = depth - 1
                current = ClassToken(val + ">")
                if depth == 0:
                    yield current
                    current = None
            case EndTypeParenthesesSymbolToken(_), NameToken(val) | ClassToken(val):
                depth = 0
                yield current
                current = None
                yield token
            case NameToken(new) | ClassToken(new) | CommaSymbolToken(new) | SpaceToken(new), ClassToken(cur) if depth > 0:
                current = ClassToken(cur + new)
            case _, None:
                depth = 0
                yield token
            case _, _:
                depth = 0
                yield current
                current = None
                yield token