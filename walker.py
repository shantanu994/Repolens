import os
from collections.abc import Iterator
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".tox", "build", "dist", ".mypy_cache", ".pytest_cache",
}


def find_python_files(root: Path) -> Iterator[Path]:
    """Yield every .py file under root, skipping ignored directories."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for name in sorted(filenames):
            if name.endswith(".py"):
                yield Path(dirpath) / name