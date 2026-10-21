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