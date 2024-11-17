from typing import List, override
from huggingface_hub import InferenceClient

from swiftmail.core.constants import HF_API_KEY

from . import EmbeddingService


class HuggingFaceEmbedding(EmbeddingService):
    model = "BAAI/bge-small-en-v1.5"

    @override
    def embed(self, texts: List[str]) -> List[List[float]]:
        client = InferenceClient(model=self.model, token=HF_API_KEY)

        embeddings = []
        for text in texts:
            response = client.feature_extraction(text)
            embeddings.append(response)

        return embeddings
