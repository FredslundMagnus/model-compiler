from parser import parser
from tokenizer import tokenize

def test1():
    """Test the import formatter"""
    text = "import   'geadf'   \n"
    tokens = tokenize(text)
    expressions, errors = parser(tokens)
    assert len(expressions) == 1
    assert len(errors) == 0
    expression = expressions[0]
    formated_expression = expression.format()
    assert formated_expression == "import 'geadf'\n"

test1()