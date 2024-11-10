from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field

from swiftmail.core.firebase import DATA_COLLECTION


class DataType(str, Enum):
    DELIVERY_TIME = "delivery_time"
    EMAIL_RECEIVED = "email_received"
    EMAIL_SENT = "email_sent"


class Data(BaseModel):
    id: str = Field(..., alias="id")
    date_created: int = Field(..., alias="date_created")
    user_id: str = Field(..., alias="user_id")

    type: DataType = Field(..., alias="type")
    data: Dict = Field(..., alias="data")

    def create(self):
        DATA_COLLECTION.document(self.id).set(self.model_dump())