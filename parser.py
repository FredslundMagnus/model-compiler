from typing import Iterator
from errors import Error
from expressions import Expression
from tokenizer import tokenize
from tokens import Token


def parser(tokens: Iterator[Token]) -> tuple[list[Expression], list[Error], dict]:
    """
    Parses the tokens.
    """
    expressions = []
    errors = []
    while True:
        try:
            expression = Expression.eat(tokens)
        except:
            break
        if isinstance(expression, Error):
            errors.append(expression)
        else:
            expressions.append(expression)
    
    return expressions, errors



with open("game.model", "r") as file:
    text = file.read()


print(*parser(tokenize(text)))