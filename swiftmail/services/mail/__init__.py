from abc import ABC
from typing import Any


class MailService(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f"LLM: {self.kwargs}"

    def get_oauth_authorization_url(self):
        raise NotImplementedError

    def send(
        self,
        credentials: Any,
        *,
        to_email: str,
        subject: str,
        html_body: str,
        attachments: list[str],
    ):
        raise NotImplementedError
