from pydantic import BaseModel, Field

from swiftmail.core.firebase import MESSAGES_COLLECTION


class MessageEmailData(BaseModel):
    message_id: str = Field(..., alias="message_id")
    thread_id: str = Field(..., alias="thread_id")

    from_email: str = Field(..., alias="from_email")
    to_email: str = Field(..., alias="to_email")
    cc_email: str = Field(..., alias="cc_email")
    bcc_email: str = Field(..., alias="bcc_email")

    subject: str = Field(..., alias="subject")
    html_content: str = Field(..., alias="html_content")


class MessageReminders(BaseModel):
    follow_up: list[str] = Field(..., alias="follow_up")
    forgetting: list[str] = Field(..., alias="forgetting")
    snoozed: list[str] = Field(..., alias="snoozed")


class Message(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    reminders: MessageReminders = Field(..., alias="reminders")
    email_data: MessageEmailData = Field(..., alias="email_data")

    summary: str = Field(..., alias="summary")

    priorities: list[str] = Field(..., alias="priorities")
    categories: list[str] = Field(..., alias="categories")
    labels: list[str] = Field(..., alias="labels")
    digests: list[str] = Field(..., alias="digests")

    embedding: list[float] = Field(..., alias="embedding")
    keywords: list[str] = Field(..., alias="keywords")
    unsubscribe_link: str | None = Field(None, alias="unsubscribe_link")

    @staticmethod
    def get_by_id(message_id: str) -> "Message | None":
        message = MESSAGES_COLLECTION.document(message_id).get()
        if message.exists:
            return Message(**message.to_dict())  # type:ignore
        return None

    def save(self):
        MESSAGES_COLLECTION.document(self.id).set(self.model_dump())

    def create(self):
        self.save()

    def update_summary(self, summary: str):
        self.summary = summary
        self.save()

    def update_priorities(self, priorities: list[str]):
        self.priorities = priorities
        self.save()

    def update_categories(self, categories: list[str]):
        self.categories = categories
        self.save()

    def update_labels(self, labels: list[str]):
        self.labels = labels
        self.save()

    def update_digests(self, digests: list[str]):
        self.digests = digests
        self.save()

    def update_embedding(self, embedding: list[float]):
        self.embedding = embedding
        self.save()

    def update_keywords(self, keywords: list[str]):
        self.keywords = keywords
        self.save()

    def update_unsubscribe_link(self, unsubscribe_link: str | None):
        self.unsubscribe_link = unsubscribe_link
        self.save()
