import time
from enum import Enum
from typing import Optional
from swiftmail.core.mongodb import NOTIFICATIONS
from .base import MongoModel
from pydantic import Field


class NotificationStatus(str, Enum):
    FAILED = "failed"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    READ = "read"
    UNREAD = "unread"
    DISMISSED = "dismissed"


class Notification(MongoModel):
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")
    title: str = Field(..., alias="title")
    body: str = Field(..., alias="body")
    status: NotificationStatus = Field(..., alias="status")
    date_dispatched: Optional[int] = Field(None, alias="date_dispatched")
    date_delivered: Optional[int] = Field(None, alias="date_delivered")
    date_failed: Optional[int] = Field(None, alias="date_failed")

    @staticmethod
    def get_by_id(notification_id: str) -> Optional["Notification"]:
        notification = NOTIFICATIONS.find_one({"_id": notification_id})
        return Notification.from_mongo(notification) if notification else None

    def create(self):
        self._save(NOTIFICATIONS)

    def update_status(self, status: NotificationStatus):
        self.status = status
        self.date_updated = int(time.time())
        self._save(NOTIFICATIONS)
