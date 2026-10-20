# RepoLens

RepoLens is a Python project for exploring a codebase with retrieval-augmented
questions and file/line citations. The project is currently in an early
development stage.

## Current functionality

- Provides a `repolens` command-line entry point.
- Reports the installed package version with `repolens version`.
- Discovers Python files recursively while skipping common generated,
  dependency, and build directories.
- Defines a `Chunk` model for source-code excerpts and their file/line
  metadata.

Interactive question answering and retrieval are planned but are not available
yet.

## Requirements

- Python 3.10 or newer

## Installation

Create a virtual environment and install RepoLens from a checkout:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Install the package:

```bash
python -m pip install -e .
```

## Usage

Show the available commands:

```bash
repolens --help
```

Print the installed version:

```bash
repolens version
```

## Development

Install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
python -m pytest
```

## Project layout

| Path | Description |
| --- | --- |
| `cli.py` | Typer command-line application |
| `walker.py` | Python-file discovery |
| `models.py` | Source-code chunk data model |
| `tests/` | Automated tests |
| `pyproject.toml` | Packaging and dependency configuration |

## License

RepoLens is distributed under the terms of the [MIT License](LICENSE).
