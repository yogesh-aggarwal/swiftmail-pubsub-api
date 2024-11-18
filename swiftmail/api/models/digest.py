import time
from typing import Optional, List
from swiftmail.core.mongodb import DIGESTS
from .base import MongoModel
from pydantic import Field


class Digest(MongoModel):
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")
    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    @staticmethod
    def get_by_id(digest_id: str) -> Optional["Digest"]:
        digest = DIGESTS.find_one({"_id": digest_id})
        return Digest.from_mongo(digest) if digest else None

    @staticmethod
    def get_by_user_id(user_id: str) -> List["Digest"]:
        cursor = DIGESTS.find({"user_id": user_id})

        docs = []
        for doc in cursor:
            result = Digest.from_mongo(doc)
            if result:
                docs.append(result)
        return docs

    def save(self):
        self._save(DIGESTS)

    def create(self):
        self.save()

    def update_title(self, title: str):
        self.title = title
        self.date_updated = int(time.time())
        self.save()

    def update_description(self, description: str):
        self.description = description
        self.date_updated = int(time.time())
        self.save()
