from __future__ import annotations

from errors import Error

class Token:
    in_string = None
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def of(value: str) -> Token:
        if Token.in_string is not None:
            match value:
                case '\n':
                    Token.in_string = None
                    return NewLineToken(value)
                case "'" | "\"" if Token.in_string == value:
                    Token.in_string = None
                    return StringToken(value)
                case _:
                    return StringToken(value)
                    
        match value:
            case "'" | "\"":
                Token.in_string = value
                return StringToken(value)
            case '\n':
                    Token.in_string = None
                    return NewLineToken(value)
            case " " | "\t":
                return SpaceToken(value)
            case ":":
                return ColonSymbolToken(value)
            case ";":
                return SemiColonSymbolToken(value)
            case ".":
                return DotSymbolToken(value)
            case ",":
                return CommaSymbolToken(value)
            case "=":
                return EqualSymbolToken(value)
            case "(":
                return StartParenthesesSymbolToken(value)
            case ")":
                return EndParenthesesSymbolToken(value)
            case "<":
                return StartTypeParenthesesSymbolToken(value)
            case ">":
                return EndTypeParenthesesSymbolToken(value)
            case "[":
                return StartListParenthesesSymbolToken(value)
            case "]":
                return EndListParenthesesSymbolToken(value)
            case "{":
                return StartSetOrMapParenthesesSymbolToken(value)
            case "}":
                return EndSetOrMapParenthesesSymbolToken(value)
            case "import":
                return ImportKeywordToken(value)
            case "enum":
                return EnumKeywordToken(value)
            case "model":
                return ModelKeywordToken(value)
            case "typedef":
                return TypedefKeywordToken(value)
            case "String" | "Set" | "Map" | "List":
                return ClassToken(value)
            case _:
                return NameToken(value)

    @property
    def isDone(self) -> bool:
        return True

    def eat(self, token: Token) -> Error | None:
        return None



class ColonSymbolToken(Token):
    pass

class SemiColonSymbolToken(Token):
    pass

class StringToken(Token):
    pass

class SpaceToken(Token):
    pass

class NewLineToken(Token):
    pass

class ImportKeywordToken(Token):
    def __init__(self, value: str) -> None:
        self.value = value

class EnumKeywordToken(Token):
    pass

class ModelKeywordToken(Token):
    pass

class TypedefKeywordToken(Token):
    pass

class NameToken(Token):
    pass

class ClassToken(Token):
    pass

class EqualSymbolToken(Token):
    pass

class StartParenthesesSymbolToken(Token):
    pass

class EndParenthesesSymbolToken(Token):
    pass

class StartTypeParenthesesSymbolToken(Token):
    pass

class EndTypeParenthesesSymbolToken(Token):
    pass

class StartListParenthesesSymbolToken(Token):
    pass

class EndListParenthesesSymbolToken(Token):
    pass

class StartSetOrMapParenthesesSymbolToken(Token):
    pass

class EndSetOrMapParenthesesSymbolToken(Token):
    pass

class DotSymbolToken(Token):
    pass

class CommaSymbolToken(Token):
    pass