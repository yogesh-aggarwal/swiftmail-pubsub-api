import time

from google.cloud.firestore import FieldFilter
from pydantic import BaseModel, Field

from swiftmail.core.firebase import DIGESTS_COLLECTION


class Digest(BaseModel):
    id: str = Field(..., alias="id")
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    @staticmethod
    def get_by_id(id: str) -> "Digest | None":
        doc = DIGESTS_COLLECTION.document(id).get()
        if doc.exists:
            return Digest(**doc.to_dict())  # type:ignore
        return None

    @staticmethod
    def get_by_user_id(user_id: str) -> list["Digest"]:

        docs = DIGESTS_COLLECTION.where(
            filter=FieldFilter("user_id", "==", user_id)
        ).stream()
        return [Digest(**doc.to_dict()) for doc in docs]

    def create(self):
        DIGESTS_COLLECTION.document(self.id).set(self.model_dump())

    def update_title(self, title: str):
        self.title = title
        self.date_updated = int(time.time())
        DIGESTS_COLLECTION.document(self.id).set(self.model_dump())

    def update_description(self, description: str):
        self.description = description
        self.date_updated = int(time.time())
        DIGESTS_COLLECTION.document(self.id).set(self.model_dump())
