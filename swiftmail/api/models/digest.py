from pydantic import BaseModel, Field

from swiftmail.core.firebase import DIGESTS_COLLECTION


class Digest(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    def create(self):
        DIGESTS_COLLECTION.document(self.id).set(self.model_dump())
