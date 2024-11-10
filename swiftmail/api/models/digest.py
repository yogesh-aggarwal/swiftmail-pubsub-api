from pydantic import BaseModel, Field


class Digest(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")
