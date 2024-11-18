from datetime import datetime
from swiftmail.core.utils import generate_id
from typing import Any, Dict, TypeVar, Optional

from pydantic import BaseModel, Field

T = TypeVar("T", bound="MongoModel")


class MongoModel(BaseModel):
    """Base model for MongoDB documents"""

    _id: str = Field(default_factory=lambda: generate_id(), alias="_id")

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """Convert to dict, using _id for MongoDB"""
        data = super().model_dump(*args, **kwargs)
        return data

    @classmethod
    def from_mongo(cls: type[T], data: Dict[str, Any]) -> Optional[T]:
        """Create model instance from MongoDB document"""
        if not data:
            return None
        return cls.model_validate(data)

    def save(self, collection):
        """Generic save method for MongoDB"""
        collection.update_one(
            {"_id": self._id}, {"$set": self.model_dump()}, upsert=True
        )