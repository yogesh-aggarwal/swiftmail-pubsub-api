import asyncio

from swiftmail.core.firebase import USERS_COLLECTION, auth
from swiftmail.api.models.user import *


async def _setup_user(name: str, email: str, password: str):
    user = User(
        id=email,
        email=email,
        name=name,
        dp=f"https://picsum.photos/{email.split('@')[0]}/200/200",
        credentials=UserCredentials(googleOAuth=None),
        data=UserData(selfDescription=""),
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
