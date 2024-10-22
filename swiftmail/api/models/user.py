from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel, Field

from swiftmail.core.firebase import USERS_COLLECTION, auth


class UserMetadata(BaseModel):
    last_seen: int = Field(...)
    date_created: int = Field(...)
    date_updated: int = Field(...)


class UserOAuthCredentials(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)


class UserCredentials(BaseModel):
    google_oauth: UserOAuthCredentials | None = Field(...)


class UserAIPreferences(BaseModel):
    model: str
    custom_rules: list[str] = Field(...)
    self_description: str = Field(...)


class UserInboxPreferences(BaseModel):
    priorities: list[str] = Field(...)
    priority_rules: list[str] = Field(...)

    labels: list[str] = Field(...)
    label_rules: list[str] = Field(...)

    categories: list[str] = Field(...)
    category_rules: list[str] = Field(...)

    spam_words: list[str] = Field(...)
    spam_rules: list[str] = Field(...)

    unsubscribe_words: list[str] = Field(...)
    unsubscribe_rules: list[str] = Field(...)


class UserPreferences(BaseModel):
    ai: UserAIPreferences = Field(...)
    inbox: UserInboxPreferences = Field(...)


class UserData(BaseModel):
    preferences: UserPreferences = Field(...)


class User(BaseModel):
    id: str = Field(...)
    metadata: UserMetadata = Field(...)

    dp: str = Field(...)
    email: str = Field(...)
    name: str = Field(...)

    data: UserData = Field(...)
    credentials: UserCredentials = Field(...)

    @staticmethod
    def get_from_email(email: str):
        user = USERS_COLLECTION.where(filter=FieldFilter("email", "==", email)).get()
        if not user:
            raise ValueError(f"User with email {email} not found")
        user = user[0].to_dict()

        try:
            return User.model_validate(user)
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
                        priorities=[],
                        priority_rules=[],
                        labels=[],
                        label_rules=[],
                        categories=[],
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
