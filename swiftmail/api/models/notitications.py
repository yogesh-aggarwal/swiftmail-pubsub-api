from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


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

    date_dispatched: Optional[int] = Field(None, alias="date_dispatched")
    date_delivered: Optional[int] = Field(None, alias="date_delivered")
    date_failed: Optional[int] = Field(None, alias="date_failed")
