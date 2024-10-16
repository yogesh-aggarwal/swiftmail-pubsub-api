from .gpt4omini import GPT4oMini
from .mistral_7b import Mistral7B


def llm_from_string(name: str):
    match name:
        case "gpt4omini":
            return GPT4oMini()
        case "mistral7b":
            return Mistral7B()
        case _:
            raise ValueError(f"Unknown LLM model: {name}")