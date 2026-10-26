from typer.testing import CliRunner

from repolens.cli import app

runner = CliRunner()


def test_index_command_chunks_repo_and_calls_store(tmp_path, monkeypatch):
    (tmp_path / "app.py").write_text("def add(a, b):\n    return a + b\n")
    stored = {}

    def fake_replace(collection, repo, chunks):
        stored["repo"] = repo
        stored["symbols"] = [c.symbol for c in chunks]
        return len(chunks)

    monkeypatch.setattr("repolens.cli.get_collection", lambda: object())
    monkeypatch.setattr("repolens.cli.replace_repo_chunks", fake_replace)

    result = runner.invoke(app, ["index", str(tmp_path)])

    assert result.exit_code == 0
    assert "Indexed 1 chunks" in result.output
    assert stored == {"repo": tmp_path.name, "symbols": ["add"]}