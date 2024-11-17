from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel, Field

from swiftmail.core.firebase import USERS_COLLECTION, auth


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


class User(BaseModel):
    id: str = Field(..., alias="id")
    metadata: UserMetadata = Field(..., alias="metadata")

    dp: str = Field(..., alias="dp")
    email: str = Field(..., alias="email")
    name: str = Field(..., alias="name")

    data: UserData = Field(..., alias="data")
    credentials: UserCredentials = Field(..., alias="credentials")

    @staticmethod
    def get_from_email(email: str):
        try:
            print("email", email)
            user = USERS_COLLECTION.document(email).get()
            print("user", user)
            return User.model_validate(user.to_dict())
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create(id: str, email: str, name: str, dp: str, password: str):
        user = User(
            id=id,
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
                        priorities=[
                            "Low",
                            "Medium",
                            "High",
                        ],
                        priority_rules=[],
                        labels=[
                            "Personal",
                            "Work",
                            "Shopping",
                        ],
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

        USERS_COLLECTION.document(user.id).set(user.model_dump())

        try:
            auth.create_user(
                uid=user.id,
                display_name=user.name,
                email=user.email,
                photo_url=user.dp,
                email_verified=True,
                password=password,
            )
        except Exception as e:
            print(e)

        return user

    def update_creds_google_oauth(self, creds: UserOAuthCredentials | None):
        self.credentials.google_oauth = creds
        USERS_COLLECTION.document(self.id).set(self.model_dump())
