from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    repo: str
    file_path: str
    start_line: int
    end_line: int
    symbol: str
    kind: str
    text: str