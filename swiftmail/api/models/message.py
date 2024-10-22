from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel, Field

from swiftmail.core.firebase import MESSAGES_COLLECTION


class MessageMetadata(BaseModel):
    date_updated: str = Field(...)
    date_created: str = Field(...)


class Message(BaseModel):
    id: str = Field(...)
    metadata: MessageMetadata = Field(...)

    subject: str = Field(...)
    html_content: str = Field(...)

    message_id: str = Field(...)
    thread_id: str = Field(...)
    from_email: str = Field(...)
    to_email: str = Field(...)
    cc_email: str = Field(...)
    bcc_email: str = Field(...)

    def create(self):
        MESSAGES_COLLECTION.document(self.id).set(self.model_dump())
