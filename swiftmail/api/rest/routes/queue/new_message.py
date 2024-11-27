from flask import request
import base64
import json

from swiftmail.api.models.message import MessageEmailData
from swiftmail.jobs.email.models import ProcessEmailJobData
from swiftmail.jobs.email import process_email
from swiftmail.api.models.user import User
from swiftmail.services.mail.gmail import Gmail
from swiftmail.core.constants import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET

from google.oauth2.credentials import Credentials


def new_message():
    payload = request.json
    if payload is None:
        return "No payload", 400

    # Decode the base64 encoded data
    encoded_data = payload["message"]["data"]
    decoded_data = base64.b64decode(encoded_data)
    message_data = json.loads(decoded_data)

    user_email = message_data["emailAddress"]

    user = User.get_from_email(user_email)
    if (
        user is None
        or user.credentials is None
        or user.credentials.google_oauth is None
    ):
        return "User not found or missing credentials", 404

    history = Gmail().get_history(
        credentials=Credentials(
            client_id=GOOGLE_OAUTH_CLIENT_ID,
            client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
            token=user.credentials.google_oauth.access_token,
            refresh_token=user.credentials.google_oauth.refresh_token,
        ),
        history_id=message_data["historyId"],
    )

    message_id = history["history"][0]["messages"][0]["id"]
    email_content = Gmail().get_message(
        credentials=Credentials(
            client_id=GOOGLE_OAUTH_CLIENT_ID,
            client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
            token=user.credentials.google_oauth.access_token,
            refresh_token=user.credentials.google_oauth.refresh_token,
        ),
        message_id=message_id,
    )

    email_data = MessageEmailData(
        message_id=email_content["id"],
        thread_id=email_content["threadId"],
        from_email=next(
            h["value"]
            for h in email_content["payload"]["headers"]
            if h["name"] == "From"
        ),
        from_name=next(
            h["value"].split("<")[0].strip(' "')
            for h in email_content["payload"]["headers"]
            if h["name"] == "From"
        ),
        to_email=next(
            h["value"] for h in email_content["payload"]["headers"] if h["name"] == "To"
        ),
        cc_email="",  # Add CC if present in headers
        bcc_email="",  # Add BCC if present in headers
        snippet=email_content["snippet"],
        subject=next(
            h["value"]
            for h in email_content["payload"]["headers"]
            if h["name"] == "Subject"
        ),
        html_content=base64.urlsafe_b64decode(
            next(
                part["body"]["data"]
                for part in email_content["payload"]["parts"]
                if part["mimeType"] == "text/html"
            )
        ).decode(),
    )

    process_email(ProcessEmailJobData(email=email_data, user=user).model_dump_json())

    # Rest of your processing logic here...
    return "OK", 200
