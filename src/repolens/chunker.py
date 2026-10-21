import tree_sitter_python as tspython
from tree_sitter import Language, Parser

from repolens.models import Chunk

PY_LANGUAGE = Language(tspython.language())
_parser = Parser(PY_LANGUAGE)


def chunk_source(source: str, repo: str, file_path: str) -> list[Chunk]:
    """Split Python source into one chunk per top-level function."""
    tree = _parser.parse(source.encode("utf-8"))
    chunks = []
    for node in tree.root_node.children:
        if node.type != "function_definition":
            continue
        name_node = node.child_by_field_name("name")
        chunks.append(
            Chunk(
                repo=repo,
                file_path=file_path,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                symbol=name_node.text.decode("utf-8"),
                kind="function",
                text=node.text.decode("utf-8"),
            )
        )
    return chunks