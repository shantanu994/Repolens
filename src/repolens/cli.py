from importlib.metadata import version as get_version

import typer

app = typer.Typer(help="Ask questions about a codebase, with file and line citations.")


@app.callback()
def main() -> None:
    """RepoLens: RAG over your codebase."""


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(get_version("repolens"))