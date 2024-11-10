import time
from enum import Enum

from pydantic import BaseModel, Field

from swiftmail.core.firebase import NOTIFICATIONS_COLLECTION


class NotificationStatus(str, Enum):
    FAILED = "failed"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    READ = "read"
    DISMISSED = "dismissed"


class Notification(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")

    title: str = Field(..., alias="title")
    body: str = Field(..., alias="body")
    status: NotificationStatus = Field(..., alias="status")

    date_dispatched: int | None = Field(None, alias="date_dispatched")
    date_delivered: int | None = Field(None, alias="date_delivered")
    date_failed: int | None = Field(None, alias="date_failed")

    @staticmethod
    def get_by_id(id: str) -> "Notification | None":
        doc = NOTIFICATIONS_COLLECTION.document(id).get()
        if doc.exists:
            return Notification(**doc.to_dict())  # type:ignore
        return None

    def create(self):
        NOTIFICATIONS_COLLECTION.document(self.id).set(self.model_dump())

    def mark_dismiss(self):
        self.status = NotificationStatus.DISMISSED
        self.date_updated = int(time.time())
        NOTIFICATIONS_COLLECTION.document(self.id).set(self.model_dump())
