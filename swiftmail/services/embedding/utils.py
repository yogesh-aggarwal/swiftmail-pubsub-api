from . import EmbeddingService
from .openai import OpenAIEmbedding
from .huggingface import HuggingFaceEmbedding


def get_embedding_from_string(name: str) -> EmbeddingService:
    match name:
        case "openai":
            return OpenAIEmbedding()
        case "huggingface":
            return HuggingFaceEmbedding()
        case _:
            raise ValueError(f"Unknown embedding model: {name}")
