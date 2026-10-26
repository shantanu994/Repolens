from importlib.metadata import version as get_version
from pathlib import Path
from typing import Annotated

import typer
from pymongo.errors import PyMongoError

from repolens.chunker import chunk_source
from repolens.store import get_collection, replace_repo_chunks
from repolens.walker import find_python_files

app = typer.Typer(help="Ask questions about a codebase, with file and line citations.")


@app.callback()
def main() -> None:
    """RepoLens: RAG-powered codebase assistant."""


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(get_version("repolens"))


@app.command()
def index(
    path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            resolve_path=True,
            help="Folder of the repository to index.",
        ),
    ],
) -> None:
    """Chunk a local repository and store the chunks in MongoDB."""
    repo = path.name
    chunks = []
    for file in find_python_files(path):
        try:
            source = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            typer.echo(f"skipped (unreadable): {file}", err=True)
            continue
        relative = file.relative_to(path).as_posix()
        chunks.extend(chunk_source(source, repo=repo, file_path=relative))

    try:
        count = replace_repo_chunks(get_collection(), repo, chunks)
    except PyMongoError:
        typer.echo("Could not reach MongoDB. Is `docker compose up -d` running?", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Indexed {count} chunks from {repo}")