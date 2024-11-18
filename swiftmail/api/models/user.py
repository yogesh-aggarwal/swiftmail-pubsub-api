from typing import Optional
from swiftmail.core.mongodb import USERS
from .base import MongoModel

from pydantic import BaseModel, Field


class UserMetadata(BaseModel):
    last_seen: int = Field(..., alias="last_seen")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")


class UserOAuthCredentials(BaseModel):
    access_token: str = Field(..., alias="access_token")
    refresh_token: str = Field(..., alias="refresh_token")


class UserCredentials(BaseModel):
    google_oauth: UserOAuthCredentials | None = Field(..., alias="google_oauth")


class UserAIPreferences(BaseModel):
    model: str = Field(..., alias="model")
    custom_rules: list[str] = Field(..., alias="custom_rules")
    self_description: str = Field(..., alias="self_description")


class UserInboxPreferences(BaseModel):
    priorities: list[str] = Field(..., alias="priorities")
    priority_rules: list[str] = Field(..., alias="priority_rules")

    labels: list[str] = Field(..., alias="labels")
    label_rules: list[str] = Field(..., alias="label_rules")

    categories: list[str] = Field(..., alias="categories")
    category_rules: list[str] = Field(..., alias="category_rules")

    spam_words: list[str] = Field(..., alias="spam_words")
    spam_rules: list[str] = Field(..., alias="spam_rules")

    unsubscribe_words: list[str] = Field(..., alias="unsubscribe_words")
    unsubscribe_rules: list[str] = Field(..., alias="unsubscribe_rules")


class UserPreferences(BaseModel):
    ai: UserAIPreferences = Field(..., alias="ai")
    inbox: UserInboxPreferences = Field(..., alias="inbox")


class UserData(BaseModel):
    preferences: UserPreferences = Field(..., alias="preferences")


class User(MongoModel):
    metadata: UserMetadata = Field(..., alias="metadata")
    dp: str = Field(..., alias="dp")
    email: str = Field(..., alias="email")
    name: str = Field(..., alias="name")

    data: UserData = Field(..., alias="data")
    credentials: UserCredentials = Field(..., alias="credentials")

    @staticmethod
    def get_from_email(email: str) -> Optional["User"]:
        try:
            user_doc = USERS.find_one({"email": email})
            return User.from_mongo(user_doc) if user_doc else None
        except Exception as e:
            print("Error fetching user from email", e)
            return None

    @staticmethod
    def create(email: str, name: str, dp: str, password: str) -> "User":
        from swiftmail.core.firebase import auth
        from swiftmail.core.mongodb import USERS

        # Create MongoDB user
        user = User(
            metadata=UserMetadata(last_seen=0, date_created=0, date_updated=0),
            email=email,
            dp=dp,
            name=name,
            data=UserData(
                preferences=UserPreferences(
                    ai=UserAIPreferences(
                        model="gpt4omini",
                        custom_rules=[],
                        self_description="",
                    ),
                    inbox=UserInboxPreferences(
                        priorities=["Low", "Medium", "High"],
                        priority_rules=[],
                        labels=["Personal", "Work", "Shopping"],
                        label_rules=[],
                        categories=[
                            "Primary",
                            "Social",
                            "Promotions",
                            "Updates",
                            "Forums",
                        ],
                        category_rules=[],
                        spam_words=[],
                        spam_rules=[],
                        unsubscribe_words=[],
                        unsubscribe_rules=[],
                    ),
                ),
            ),
            credentials=UserCredentials(google_oauth=None),
        )

        USERS.insert_one(user.model_dump())

        # First check if user exists in Firebase
        try:
            existing_user = auth.get_user_by_email(email)
            # If user exists, delete from Firebase
            if existing_user:
                auth.delete_user(existing_user.uid)
        except auth.UserNotFoundError:
            pass  # User doesn't exist in Firebase, which is fine
        except Exception as e:
            print(f"Error checking/deleting Firebase user: {e}")

        # Create new Firebase user
        try:
            auth.create_user(
                uid=str(user.id),
                email=email,
                password=password,
                display_name=name,
                photo_url=dp,
            )
        except Exception as e:
            print(f"Error creating Firebase user: {e}")
            raise e

        return user

    def update_creds_google_oauth(self, creds: Optional[UserOAuthCredentials]):
        self.credentials.google_oauth = creds
        USERS.update_one({"id": self.id}, {"$set": self.model_dump()})
