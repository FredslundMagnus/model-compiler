from typing import Iterator
from tokens import Token


def tokenize(text: str) -> Iterator[Token]:
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