from typing import override

from openai import OpenAI

from swiftmail.core.constants import OPENAI_API_KEY

from . import EmbeddingService


class OpenAIEmbedding(EmbeddingService):
    model = "text-embedding-3-small"

    @override
    def embed(self, texts: list[str]) -> list[list[float]]:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [embedding.embedding for embedding in response.data]
