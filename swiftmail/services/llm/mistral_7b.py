from typing import override
from huggingface_hub import InferenceClient

from swiftmail.core.constants import HF_API_KEY

from . import LLMPrompt, LLMService


class Mistral7B(LLMService):
    model = "mistralai/Mistral-7B-Instruct-v0.3"

    @override
    def run(self, messages: LLMPrompt, temperature: float | None = None) -> str | None:
        temperature = temperature if temperature is not None else 0

        client = InferenceClient(model=self.model, token=HF_API_KEY)

        res = client.chat_completion(
            messages.to_dict(),
            temperature=temperature,
            max_tokens=10_000,
        )
        if not res.choices:
            return None
        res = res.choices[0].message

        return res.content
