from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from swiftmail.core.firebase import DATA_COLLECTION


class DataType(str, Enum):
    EMAIL_RECEIVED = "email_received"
    EMAIL_SENT = "email_sent"


class Data(BaseModel):
    id: str = Field(..., alias="id")
    date_created: int = Field(..., alias="date_created")
    user_id: str = Field(..., alias="user_id")

    type: DataType = Field(..., alias="type")
    data: dict[str, Any] = Field(..., alias="data")

    def create(self):
        DATA_COLLECTION.document(self.id).set(self.model_dump())
