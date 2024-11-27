from typing import Optional, List
from swiftmail.core.mongodb import MESSAGES
from .base import MongoModel

from pydantic import BaseModel, Field


class MessageEmailData(BaseModel):
    message_id: str = Field(..., alias="message_id")
    thread_id: str = Field(..., alias="thread_id")

    from_email: str = Field(..., alias="from_email")
    from_name: str = Field(..., alias="from_name")
    to_email: str = Field(..., alias="to_email")
    cc_email: str = Field(..., alias="cc_email")
    bcc_email: str = Field(..., alias="bcc_email")

    subject: str = Field(..., alias="subject")
    html_content: str = Field(..., alias="html_content")
    snippet: str = Field(..., alias="snippet")


class MessageReminders(BaseModel):
    follow_up: list[str] = Field(..., alias="follow_up")
    forgetting: list[str] = Field(..., alias="forgetting")
    snoozed: list[str] = Field(..., alias="snoozed")


class Message(MongoModel):
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    reminders: MessageReminders = Field(..., alias="reminders")
    email_data: MessageEmailData = Field(..., alias="email_data")

    thread_id: str = Field(..., alias="thread_id")

    summary: str = Field(..., alias="summary")
    embedding: list[float] = Field(..., alias="embedding")
    keywords: list[str] = Field(..., alias="keywords")
    unsubscribe_link: str | None = Field(None, alias="unsubscribe_link")

    @staticmethod
    def get_by_id(message_id: str) -> Optional["Message"]:
        message = MESSAGES.find_one({"id": message_id})
        return Message.from_mongo(message) if message else None

    @staticmethod
    def get_by_thread_id(thread_id: str) -> list["Message"]:
        messages = MESSAGES.find({"thread_id": thread_id}).sort("date_created", 1)

        result = []
        for message in messages:
            if message:
                result.append(Message.from_mongo(message))
        return result

    def _save(self):
        MESSAGES.update_one({"id": self.id}, {"$set": self.model_dump()}, upsert=True)

    def save(self):
        self._save()

    def create(self):
        self._save()

    def update_summary(self, summary: str):
        self.summary = summary
        self._save()

    def update_embedding(self, embedding: list[float]):
        self.embedding = embedding
        self._save()

    def update_keywords(self, keywords: list[str]):
        self.keywords = keywords
        self._save()

    def update_unsubscribe_link(self, unsubscribe_link: str | None):
        self.unsubscribe_link = unsubscribe_link
        self._save()
