from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel, Field

from swiftmail.core.firebase import MESSAGES_COLLECTION


class MessageMetadata(BaseModel):
    date_updated: str = Field(..., alias="dateUpdated")
    date_created: str = Field(..., alias="dateCreated")


class Message(BaseModel):
    id: str = Field(..., title="Message ID", alias="id")
    metadata: MessageMetadata = Field(..., title="Message Metadata", alias="metadata")

    subject: str = Field(..., title="Subject")
    html_content: str = Field(..., title="HTML Content")

    message_id: str = Field(..., title="Message ID", alias="messageID")
    thread_id: str = Field(..., title="Thread ID", alias="threadID")
    from_email: str = Field(..., title="From Email", alias="fromEmail")
    to_email: str = Field(..., title="To Email", alias="toEmail")
    cc_email: str = Field(..., title="CC Email", alias="ccEmail")
    bcc_email: str = Field(..., title="BCC Email", alias="bccEmail")

    def create(self):
        MESSAGES_COLLECTION.document(self.id).set(self.model_dump())
