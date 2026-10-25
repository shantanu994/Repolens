from repolens.chunker import chunk_source

SOURCE = '''import os


def add(a, b):
    return a + b


def greet(name):
    return f"hi {name}"
'''


def test_top_level_functions_become_chunks():
    chunks = chunk_source(SOURCE, repo="demo", file_path="demo.py")

    assert [c.symbol for c in chunks] == ["add", "greet"]
    assert chunks[0].kind == "function"
    assert (chunks[0].start_line, chunks[0].end_line) == (4, 5)
    assert chunks[0].text == "def add(a, b):\n    return a + b"
    assert (chunks[1].start_line, chunks[1].end_line) == (8, 9)

CLASS_SOURCE = '''class Greeter:
    """Says hello."""

    greeting = "hi"

    def __init__(self, name):
        self.name = name

    @property
    def shout(self):
        return self.greeting.upper()


def helper():
    return 1
'''


def test_classes_split_into_header_and_method_chunks():
    chunks = chunk_source(CLASS_SOURCE, repo="demo", file_path="demo.py")

    assert [(c.symbol, c.kind) for c in chunks] == [
        ("Greeter", "class"),
        ("Greeter.__init__", "method"),
        ("Greeter.shout", "method"),
        ("helper", "function"),
    ]
    spans = [(c.start_line, c.end_line) for c in chunks]
    assert spans == [(1, 4), (6, 7), (9, 11), (14, 15)]
    assert "def __init__" not in chunks[0].text
    assert chunks[2].text.startswith("@property")


def test_nested_functions_stay_inside_parent_chunk():
    source = "def outer():\n    def inner():\n        return 1\n    return inner\n"
    chunks = chunk_source(source, repo="demo", file_path="demo.py")

    assert [c.symbol for c in chunks] == ["outer"]
    assert "def inner" in chunks[0].text

CLASS_SOURCE = '''class Greeter:
    """Says hello."""

    greeting = "hi"

    def __init__(self, name):
        self.name = name

    @property
    def shout(self):
        return self.greeting.upper()


def helper():
    return 1
'''


def test_classes_split_into_header_and_method_chunks():
    chunks = chunk_source(CLASS_SOURCE, repo="demo", file_path="demo.py")

    assert [(c.symbol, c.kind) for c in chunks] == [
        ("Greeter", "class"),
        ("Greeter.__init__", "method"),
        ("Greeter.shout", "method"),
        ("helper", "function"),
    ]
    spans = [(c.start_line, c.end_line) for c in chunks]
    assert spans == [(1, 4), (6, 7), (9, 11), (14, 15)]
    assert "def __init__" not in chunks[0].text
    assert chunks[2].text.startswith("@property")


def test_nested_functions_stay_inside_parent_chunk():
    source = "def outer():\n    def inner():\n        return 1\n    return inner\n"
    chunks = chunk_source(source, repo="demo", file_path="demo.py")

    assert [c.symbol for c in chunks] == ["outer"]
    assert "def inner" in chunks[0].text