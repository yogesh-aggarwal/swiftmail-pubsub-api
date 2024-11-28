from flask import request, jsonify
from pydantic import BaseModel
from swiftmail.api.models.user import User
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from swiftmail.api.models.message import MessageEmailData
from swiftmail.jobs.email import ProcessEmailJobData, process_email
from swiftmail.core.constants import (
    GOOGLE_OAUTH_CLIENT_ID,
    GOOGLE_OAUTH_CLIENT_SECRET,
)
from swiftmail.services.mail.gmail import Gmail


class ReplyMessageRequest(BaseModel):
    message_id: str
    reply_body: str


def reply_message():
    """Reply to a specific Gmail message."""

    user: User = getattr(request, "user", None)  # type: ignore

    if not user.credentials.google_oauth:
        return jsonify({"message": "google_oauth_not_connected"}), 400

    if request.json is None:
        return jsonify({"message": "No payload"}), 400

    body = ReplyMessageRequest(**request.json)

    gmail = Gmail()
    reply_id = gmail.reply_to_message(
        credentials=Credentials(
            client_id=GOOGLE_OAUTH_CLIENT_ID,
            client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
            token=user.credentials.google_oauth.access_token,
            refresh_token=user.credentials.google_oauth.refresh_token,
        ),
        message_id=body.message_id,
        reply_body=body.reply_body,
    )

    if reply_id is None:
        return jsonify({"message": "Failed to send reply"}), 500

    return jsonify({"message_id": reply_id})
