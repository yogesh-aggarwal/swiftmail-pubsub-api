from enum import Enum
from typing import Dict, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class DashboardSectionStatusEnum(str, Enum):
    DISABLED = "disabled"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class DashboardSection(BaseModel, Generic[T]):
    id: str = Field(..., alias="id")
    date_updated: int = Field(..., alias="date_updated")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")
    status: DashboardSectionStatusEnum = Field(..., alias="status")

    time_range_start: int = Field(..., alias="time_range_start")
    time_range_end: int = Field(..., alias="time_range_end")

    data: T = Field(..., alias="data")


class Dashboard(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    sections: Dict[str, DashboardSection] = Field(..., alias="sections")
