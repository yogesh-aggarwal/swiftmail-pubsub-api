from pydantic import BaseModel, Field


class InboxThread(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    summary: str = Field(..., alias="summary")
    thread_id: str = Field(..., alias="thread_id")
