from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel, Field

from swiftmail.core.firebase import USERS_COLLECTION, auth


class UserMetadata(BaseModel):
    last_seen: int = Field(..., alias="lastSeen")
    date_created: int = Field(..., alias="dateCreated")
    date_updated: int = Field(..., alias="dateUpdated")


class UserOAuthCredentials(BaseModel):
    access_token: str = Field(..., alias="access_token")
    refresh_token: str = Field(..., alias="refresh_token")


class UserCredentials(BaseModel):
    google_oauth: UserOAuthCredentials | None = Field(..., alias="googleOAuth")


class UserAIPreferences(BaseModel):
    model: str
    custom_rules: list[str] = Field(..., alias="customRules")
    self_description: str = Field(..., alias="selfDescription")


class UserInboxPreferences(BaseModel):
    priorities: list[str] = Field(..., alias="priorities")
    priority_rules: list[str] = Field(..., alias="priorityRules")

    labels: list[str] = Field(..., alias="labels")
    label_rules: list[str] = Field(..., alias="labelRules")

    categories: list[str] = Field(..., alias="categories")
    category_rules: list[str] = Field(..., alias="categoryRules")

    spam_words: list[str] = Field(..., alias="spamWords")
    spam_rules: list[str] = Field(..., alias="spamRules")

    unsubscribe_words: list[str] = Field(..., alias="unsubscribeWords")
    unsubscribe_rules: list[str] = Field(..., alias="unsubscribeRules")


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
        user = USERS_COLLECTION.where(filter=FieldFilter("email", "==", email)).get()
        if not user:
            raise ValueError(f"User with email {email} not found")
        user = user[0].to_dict()

        return User.model_validate(user)

    @staticmethod
    def create(id: str, email: str, name: str, dp: str, password: str):
        user = User(
            id=id,
            metadata=UserMetadata(lastSeen=0, dateCreated=0, dateUpdated=0),
            email=email,
            dp=dp,
            name=name,
            data=UserData(
                preferences=UserPreferences(
                    ai=UserAIPreferences(
                        model="gpt4omini",
                        customRules=[],
                        selfDescription="",
                    ),
                    inbox=UserInboxPreferences(
                        priorities=[],
                        priorityRules=[],
                        labels=[],
                        labelRules=[],
                        categories=[],
                        categoryRules=[],
                        spamWords=[],
                        spamRules=[],
                        unsubscribeWords=[],
                        unsubscribeRules=[],
                    ),
                ),
            ),
            credentials=UserCredentials(googleOAuth=None),
        )

        USERS_COLLECTION.document(user.id).set(user.model_dump(by_alias=True))

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
        USERS_COLLECTION.document(self.id).set(self.model_dump(by_alias=True))
