from abc import ABC
from typing import List


class EmbeddingService(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f"Embedding: {self.kwargs}"

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Convert texts into vector embeddings.

        Args:
            texts: List of strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        raise NotImplementedError
