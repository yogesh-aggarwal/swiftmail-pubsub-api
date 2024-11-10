from pydantic import BaseModel, Field

from swiftmail.core.firebase import THREADS_COLLECTION


class ThreadFlags(BaseModel):
    is_muted: bool = Field(..., alias="is_muted")
    is_starred: bool = Field(..., alias="is_starred")
    is_trash: bool = Field(..., alias="is_trash")
    is_archived: bool = Field(..., alias="is_archived")
    is_read: bool = Field(..., alias="is_read")
    is_unread: bool = Field(..., alias="is_unread")
    is_deleted: bool = Field(..., alias="is_deleted")
    is_junk: bool = Field(..., alias="is_junk")
    is_spam: bool = Field(..., alias="is_spam")


class Thread(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    summary: str = Field(..., alias="summary")
    thread_id: str = Field(..., alias="thread_id")

    flags: ThreadFlags = Field(..., alias="flags")

    def create(self):
        THREADS_COLLECTION.document(self.id).set(self.model_dump())
