from enum import Enum
from typing import Any

from pydantic import Field

from .base import MongoModel

from swiftmail.core.mongodb import DATA


class DataType(str, Enum):
    EMAIL_RECEIVED = "email_received"
    EMAIL_SENT = "email_sent"


class Data(MongoModel):
    date_created: int = Field(..., alias="date_created")
    user_id: str = Field(..., alias="user_id")

    type: DataType = Field(..., alias="type")
    data: dict[str, Any] = Field(..., alias="data")

    def create(self):
        self._save(DATA)
