from typing import Any, Dict, TypeVar, Optional
from pymongo.collection import Collection
from pydantic import BaseModel, Field, ConfigDict
from swiftmail.core.utils import generate_id

T = TypeVar("T", bound="MongoModel")


class MongoModel(BaseModel):
    """Base model for MongoDB documents"""

    model_config = ConfigDict()

    id: str = Field(default_factory=generate_id, alias="id")

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """Convert to dict, using _id for MongoDB"""
        data = super().model_dump(*args, **kwargs, by_alias=True)
        return data

    @classmethod
    def from_mongo(cls: type[T], data: Dict[str, Any]) -> Optional[T]:
        """Create model instance from MongoDB document"""
        if not data:
            return None

        return cls.model_validate(data)

    def _save(self, collection: Collection):
        """Generic save method for MongoDB"""
        collection.update_one({"id": self.id}, {"$set": self.model_dump()}, upsert=True)
