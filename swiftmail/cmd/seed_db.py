import asyncio

from swiftmail.core.firebase import USERS_COLLECTION, auth
from swiftmail.api.models.user import *


async def _setup_user(name: str, email: str, password: str):
    user = User(
        id="yogeshdevaggarwal@gmail.com",
        metadata=UserMetadata(lastSeen=0, dateCreated=0, dateUpdated=0),
        name=name,
        email=email,
        dp="https://picsum.photos/seed/yogeshdevaggarwal/200/200",
        data=UserData(
            preferences=UserPreferences(
                ai=UserAIPreferences(
                    model="gpt4omini",
                    customRules=[],
                    selfDescription="I am a very busy person.",
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

    try:
        auth.delete_user(user.id)
    except:
        pass
    auth.create_user(
        uid=user.id,
        email=user.email,
        email_verified=True,
        display_name=user.name,
        password=password,
    )

    USERS_COLLECTION.document("yogeshdevaggarwal@gmail.com").set(user.model_dump())


async def _setup_users():
    users = [
        ("Yogesh Aggarwal", "yogeshdevaggarwal@gmail.com", "12345678"),
    ]

    jobs = map(lambda x: _setup_user(*x), users)

    await asyncio.gather(*jobs)


def main():
    asyncio.run(_setup_users())

    print("Done!")
