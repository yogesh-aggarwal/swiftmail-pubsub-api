from swiftmail.core.firebase import USERS_COLLECTION, auth


def _setup_users():
    try:
        auth.delete_user("yogeshdevaggarwal@gmail.com")
    except:
        pass
    auth.create_user(
        uid="yogeshdevaggarwal@gmail.com",
        email="yogeshdevaggarwal@gmail.com",
        email_verified=True,
        password="12345678",
        display_name="Yogesh Aggarwal",
    )

    USERS_COLLECTION.document("yogeshdevaggarwal@gmail.com").set(
        {
            "id": "yogeshdevaggarwal@gmail.com",
            "email": "yogeshdevaggarwal@gmail.com",
            "name": "Yogesh Aggarwal",
            "dp": "https://picsum.photos/seed/123/200/200",
            "credentials": {
                "google_oauth": None,
            },
            "data": {},
        }
    )


def main():
    _setup_users()
