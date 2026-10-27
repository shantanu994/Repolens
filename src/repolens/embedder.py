from fastembed import TextEmbedding

from repolens.models import Chunk

MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384

_model: TextEmbedding | None = None


def _get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def embedding_input(chunk: Chunk) -> str:
    """Text sent to the embedding model: path and name give the code context."""
    return f"{chunk.file_path}\n{chunk.symbol}\n{chunk.text}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed texts locally; returns one vector per text."""
    return [vector.tolist() for vector in _get_model().embed(texts)]