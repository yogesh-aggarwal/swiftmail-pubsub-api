from pydantic import BaseModel, Field

from swiftmail.core.firebase import MESSAGES_COLLECTION


class MessageEmailData(BaseModel):
    subject: str = Field(..., alias="subject")
    html_content: str = Field(..., alias="html_content")

    message_id: str = Field(..., alias="message_id")
    thread_id: str = Field(..., alias="thread_id")
    from_email: str = Field(..., alias="from_email")
    to_email: str = Field(..., alias="to_email")
    cc_email: str = Field(..., alias="cc_email")
    bcc_email: str = Field(..., alias="bcc_email")


class MessageFlags(BaseModel):
    is_archived: bool = Field(..., alias="is_archived")
    is_starred: bool = Field(..., alias="is_starred")
    is_trash: bool = Field(..., alias="is_trash")
    is_draft: bool = Field(..., alias="is_draft")
    is_sent: bool = Field(..., alias="is_sent")
    is_received: bool = Field(..., alias="is_received")
    is_read: bool = Field(..., alias="is_read")
    is_unread: bool = Field(..., alias="is_unread")
    is_deleted: bool = Field(..., alias="is_deleted")
    is_junk: bool = Field(..., alias="is_junk")
    is_spam: bool = Field(..., alias="is_spam")


class Message(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    flags: MessageFlags = Field(..., alias="flags")
    email_data: MessageEmailData = Field(..., alias="email_data")

    summary: str = Field(..., alias="summary")
    template: str | None = Field(..., alias="template")

    priorities: str = Field(..., alias="priorities")
    categories: list[str] = Field(..., alias="categories")
    labels: list[str] = Field(..., alias="labels")
    digests: list[str] = Field(..., alias="digests")

    @staticmethod
    def get_by_id(message_id: str) -> "Message | None":
        message = MESSAGES_COLLECTION.document(message_id).get()
        if message.exists:
            return Message(**message.to_dict())  # type:ignore
        return None

    def create(self):
        MESSAGES_COLLECTION.document(self.id).set(self.model_dump())

    def update_summary(self, summary: str):
        MESSAGES_COLLECTION.document(self.id).update({"summary": summary})
