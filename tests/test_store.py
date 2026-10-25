import pytest
from pymongo.errors import PyMongoError

from repolens.models import Chunk
from repolens.store import get_collection, replace_repo_chunks


@pytest.fixture
def collection():
    coll = get_collection(db_name="repolens_test")
    try:
        coll.database.client.admin.command("ping")
    except PyMongoError:
        pytest.skip("MongoDB is not running")
    coll.delete_many({})
    yield coll
    coll.delete_many({})


def make_chunk(symbol: str, repo: str = "demo") -> Chunk:
    return Chunk(
        repo=repo, file_path="a.py", start_line=1, end_line=2,
        symbol=symbol, kind="function", text=f"def {symbol}(): pass",
    )


def test_replace_repo_chunks_is_idempotent(collection):
    chunks = [make_chunk("a"), make_chunk("b")]

    assert replace_repo_chunks(collection, "demo", chunks) == 2
    assert replace_repo_chunks(collection, "demo", chunks) == 2
    assert collection.count_documents({"repo": "demo"}) == 2


def test_replace_only_touches_the_given_repo(collection):
    replace_repo_chunks(collection, "other", [make_chunk("x", repo="other")])
    replace_repo_chunks(collection, "demo", [make_chunk("a")])

    assert collection.count_documents({"repo": "other"}) == 1