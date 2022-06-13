from typing import Iterator
from errors import Error, SyntaxError
from expressions import Expression
from tokenizer import tokenize
from tokens import Token


def parser(tokens: Iterator[Token]) -> tuple[list[Expression], list[Error]]:
    """
    Parses the tokens.
    """
    expressions = []
    errors = []
    while True:
        try:
            expression = Expression.eat(tokens)
            expressions.append(expression)
        except StopIteration:
            break
        except SyntaxError as error:
            errors.append(error)
    
    return expressions, errors


if __name__ == "__main__":
    with open("game.model", "r") as file:
        text = file.read()

    expressions, errors = parser(tokenize(text))
    print("Expressions:")
    print(*[repr(e) for e in expressions], sep="\n")
    if errors:
        print("\nErrors:")
        print(*errors, sep="\n")