from typing import Iterator
from errors import Error
from expressions import Expression
from tokenizer import tokenize
from tokens import Token
from functools import reduce





def parser(tokens: Iterator[Token]) -> tuple[list[Expression], list[Error], dict]:
    """
    Parses the tokens.
    """
    state = {}
    # for _ in range(7):
    #     expression = Expression.eat(tokens, state)
    #     print(expression, end="")
    expressions = []
    errors = []
    while True:
        try:
            expression = Expression.eat(tokens, state)
        except:
            break
        if isinstance(expression, Error):
            errors.append(expression)
        else:
            expressions.append(expression)
    
    return expressions, errors, state



with open("game.model", "r") as file:
    text = file.read()


parser(tokenize(text))