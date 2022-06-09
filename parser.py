from typing import Iterator
from errors import Error
from expressions import Expression
from tokenizer import tokenize
from tokens import Token
from functools import reduce





def parser(tokens: Iterator[Token]) -> list[Expression]:
    """
    Parses the tokens and prints the result.
    """
    # temp = [], [], {}
    # def reducer(acc: tuple[list[Expression], list[Error], dict], token: Token) -> list[Expression]:
    #     expressions, errors, state = acc
    #     error, isDone, expression = Expression.eat(token, state)
    #     if isDone:
    #         expressions.append(expression)
    #     if error is not None:
    #         errors.append(error)
    #     return expressions, errors, state
    # expresions = reduce(reducer, tokens, temp)
    # print(expresions)
    state = {}
    expression = Expression.eat(tokens, state)

with open("game.model", "r") as file:
    text = file.read()


parser(tokenize(text))