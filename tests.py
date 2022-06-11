from parser import parser
from tokenizer import tokenize
from helpers.printer import print, Colors

def test(f):
    """Test the function"""
    try:
        f()
        print(f"{f.__name__} completed", color=Colors.green)
    except AssertionError as error:
        print(f.__name__, "failed:", f.__doc__, color=Colors.red)
        print(error.with_traceback())
    return f

@test
def test1():
    """Test the import formatter"""
    text = "import   'geadf'   "
    tokens = tokenize(text)
    expressions, errors = parser(tokens)
    assert len(expressions) == 1, expressions
    assert len(errors) == 0, errors
    assert str(expressions[0]) == "import 'geadf'", expressions

@test
def test2():
    """Test the tokenizer"""
    data: list[tuple[str, int]] = [("import 'geadf'", 4), ("import   \t'geadf'  ", 4)]
    for text, expected in data:
        tokens = list(tokenize(text))
        assert len(tokens) == expected, tokens

@test
def test3():
    """Test the enum formatter"""
    text = "enum   Status   "
    tokens = tokenize(text)
    expressions, errors = parser(tokens)
    assert len(expressions) == 1, expressions
    assert len(errors) == 0, errors
    assert str(expressions[0]) == "enum Status", expressions

@test
def test4():
    """Test the typedef formatter"""
    text = "typedef   PlayerId   =  String  "
    tokens = tokenize(text)
    expressions, errors = parser(tokens)
    assert len(expressions) == 1, expressions
    assert len(errors) == 0, errors
    assert str(expressions[0]) == "typedef PlayerId = String", expressions

@test
def test5():
    """Test the model formatter"""
    text = "model   Game(asdf: Ers):   "
    tokens = tokenize(text)
    expressions, errors = parser(tokens)
    assert len(expressions) == 1, expressions
    assert len(errors) == 0, errors
    assert str(expressions[0]) == "model Game(asdf: Ers):", expressions

@test
def test6_a():
    """Tokenize types"""
    data = ["String", "PlayerId", "Set<PlayerId>", "Set<String>", "Set<Roles>", "Map<PlayerId, Roles>", "Map<PlayerId, String>", "Map<String, Roles>", "Map<Map<String, Roles>, String>", "Status", "Ers", "Roles"]
    for text in data:
        tokens = list(tokenize(text))[:-1]
        assert len(tokens) == 1, tokens

@test
def test6_b():
    """Tokenize types"""
    data = ["String =", "PlayerId =", "Set<PlayerId> =", "Set<String> =", "Set<Roles> =", "Map<PlayerId, Roles> =", "Map<PlayerId, String> =", "Map<String, Roles> =", "Map<Map<String, Roles>, String> =", "Status =", "Ers =", "Roles ="]
    for text in data:
        tokens = list(tokenize(text))[:-1]
        assert len(tokens) == 3, tokens


@test
def test7():
    """Parse indented blocks"""
    data = ["    users: Set<PlayerId> = {}", "    roles: Set<Roles> = {}", "    status: Status = Status.chooseUsers", "    creator: PlayerId = playerId", "    roleMap: Map<PlayerId, Roles> = {}", "    test: Status"]
    for text in data:
        tokens = tokenize(text)
        expressions, errors = parser(tokens)
        assert len(expressions) == 1, expressions
        assert len(errors) == 0, errors
        assert str(expressions[0]) == text, expressions