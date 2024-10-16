from openai import OpenAI

from swiftmail.core.constants import OPENAI_API_KEY

from . import LLMService


class GPT4oMini(LLMService):
    model = "gpt-4o-mini"

    def run(self, messages):
        client = OpenAI(api_key=OPENAI_API_KEY)

        res = client.chat.completions.create(
            model=self.model,
            messages=messages.to_dict(),  # type: ignore
            max_tokens=16_000,
        )
        if not res.choices:
            return None
        res = res.choices[0].message

        return res.content
