import tree_sitter_python as tspython
from tree_sitter import Language, Node, Parser

from repolens.models import Chunk

PY_LANGUAGE = Language(tspython.language())
_parser = Parser(PY_LANGUAGE)


def _definition(node: Node) -> Node | None:
    """Return the function/class node, looking through decorators."""
    if node.type == "decorated_definition":
        node = node.child_by_field_name("definition")
    if node is not None and node.type in ("function_definition", "class_definition"):
        return node
    return None


def _name(definition: Node) -> str:
    return definition.child_by_field_name("name").text.decode("utf-8")


def _make_chunk(repo, file_path, symbol, kind, start_line, text) -> Chunk:
    return Chunk(
        repo=repo,
        file_path=file_path,
        start_line=start_line,
        end_line=start_line + text.count("\n"),
        symbol=symbol,
        kind=kind,
        text=text,
    )


def _chunk_class(node, definition, source_bytes, repo, file_path) -> list[Chunk]:
    class_name = _name(definition)
    methods = []
    for child in definition.child_by_field_name("body").children:
        inner = _definition(child)
        if inner is not None and inner.type == "function_definition":
            methods.append((child, inner))

    header_end = methods[0][0].start_byte if methods else node.end_byte
    header = source_bytes[node.start_byte:header_end].decode("utf-8").rstrip()
    chunks = [
        _make_chunk(repo, file_path, class_name, "class", node.start_point[0] + 1, header)
    ]
    for method_node, method_def in methods:
        chunks.append(
            _make_chunk(
                repo,
                file_path,
                f"{class_name}.{_name(method_def)}",
                "method",
                method_node.start_point[0] + 1,
                method_node.text.decode("utf-8"),
            )
        )
    return chunks


def chunk_source(source: str, repo: str, file_path: str) -> list[Chunk]:
    """Split Python source into function, class-header and method chunks."""
    source_bytes = source.encode("utf-8")
    tree = _parser.parse(source_bytes)
    chunks: list[Chunk] = []
    for node in tree.root_node.children:
        definition = _definition(node)
        if definition is None:
            continue
        if definition.type == "function_definition":
            chunks.append(
                _make_chunk(
                    repo,
                    file_path,
                    _name(definition),
                    "function",
                    node.start_point[0] + 1,
                    node.text.decode("utf-8"),
                )
            )
        else:
            chunks.extend(_chunk_class(node, definition, source_bytes, repo, file_path))
    return chunks