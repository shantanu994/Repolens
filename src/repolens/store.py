import os
from dataclasses import asdict

from pymongo import MongoClient
from pymongo.collection import Collection

from repolens.models import Chunk

DEFAULT_URI = "mongodb://localhost:27017/?directConnection=true"
DB_NAME = "repolens"


def get_collection(uri: str | None = None, db_name: str = DB_NAME) -> Collection:
    uri = uri or os.environ.get("REPOLENS_MONGO_URI", DEFAULT_URI)
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    return client[db_name]["chunks"]


def replace_repo_chunks(collection: Collection, repo: str, chunks: list[Chunk]) -> int:
    """Delete a repo's old chunks, insert the new ones, return how many were inserted."""
    collection.delete_many({"repo": repo})
    if not chunks:
        return 0
    result = collection.insert_many([asdict(chunk) for chunk in chunks])
    return len(result.inserted_ids)