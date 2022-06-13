

from errors import Error
from expressions import *
from parser import parser
from tokenizer import tokenize


def type_checker(expressions: list[Expression]) -> tuple[list[Error], dict[str, object]]:
    """
    Checks the type of the expressions.
    """
    types = {"String": [], "Set": [None], "Map": [None, None]}
    errors = []
    for expression in expressions:
        match expression:
            case EnumExpression(NameToken(name)):
                if name in types:
                    errors.append(Error(expression, "Duplicate enum name"))
                else:
                    types[name] = []
            case TypedefExpression(NameToken(name), NameToken(type) | ClassToken(type)):
                print(f"TypedefExpression: {name} {type}")

    return errors, types

if __name__ == "__main__":
    with open("game.model", "r") as file:
        text = file.read()

    expressions, errors = parser(tokenize(text))
    if len(errors) != 0:
        quit()

    errors, types = type_checker(expressions)
    print("Types:")
    print(*types, sep="\n")
    if errors:
        print("\nErrors:")
        print(*errors, sep="\n")