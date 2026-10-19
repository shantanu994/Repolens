from repolens.walker import find_python_files


def test_finds_python_files_and_skips_ignored_dirs(tmp_path):
    (tmp_path / "app.py").write_text("x = 1")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "util.py").write_text("y = 2")
    (tmp_path / "notes.txt").write_text("not python")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "ignored.py").write_text("z = 3")

    found = [p.relative_to(tmp_path).as_posix() for p in find_python_files(tmp_path)]

    assert found == ["app.py", "pkg/util.py"]