from flask import request, jsonify
from swiftmail.api.models.user import User
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from swiftmail.api.models.message import MessageEmailData
from swiftmail.jobs.email import ProcessEmailJobData, process_email
from swiftmail.core.constants import (
    GOOGLE_OAUTH_CLIENT_ID,
    GOOGLE_OAUTH_CLIENT_SECRET,
)


def import_inbox():
    user: User = getattr(request, "user", None)  # type: ignore

    if not user.credentials.google_oauth:
        return jsonify({"message": "google_oauth_not_connected"}), 400

    try:
        # Create credentials object from user's OAuth tokens
        credentials = Credentials(
            token=user.credentials.google_oauth.access_token,
            refresh_token=user.credentials.google_oauth.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=GOOGLE_OAUTH_CLIENT_ID,
            client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
        )

        # Build the Gmail API service
        service = build("gmail", "v1", credentials=credentials)

        # Fetch messages from Gmail
        results = service.users().messages().list(userId="me", maxResults=100).execute()
        messages = results.get("messages", [])

        # Process each message
        for msg in messages:
            # Get the full message details
            message = (
                service.users()
                .messages()
                .get(userId="me", id=msg["id"], format="full")
                .execute()
            )

            # Extract headers
            headers = message["payload"]["headers"]
            subject = next(
                (h["value"] for h in headers if h["name"].lower() == "subject"), ""
            )
            from_email = next(
                (h["value"] for h in headers if h["name"].lower() == "from"), ""
            )
            from_name = next(
                (h["value"] for h in headers if h["name"].lower() == "fromname"), ""
            )
            to_email = next(
                (h["value"] for h in headers if h["name"].lower() == "to"), ""
            )
            cc_email = next(
                (h["value"] for h in headers if h["name"].lower() == "cc"), ""
            )
            bcc_email = next(
                (h["value"] for h in headers if h["name"].lower() == "bcc"), ""
            )
            snippet = next(
                (h["value"] for h in headers if h["name"].lower() == "snippet"), ""
            )

            # Get message body
            parts = message["payload"].get("parts", [])
            html_content = ""
            for part in parts:
                if part["mimeType"] == "text/html":
                    html_content = part["body"].get("data", "")
                    break

            email_data = MessageEmailData(
                subject=subject,
                html_content=html_content,
                message_id=message["id"],
                thread_id=message["threadId"],
                from_email=from_email,
                from_name=from_name,
                snippet=snippet,
                to_email=to_email,
                cc_email=cc_email,
                bcc_email=bcc_email,
            )

            # Queue the message for processing
            process_email(
                ProcessEmailJobData(
                    email=email_data,
                    user=user,
                ).model_dump_json()
            )

        return jsonify({"message": "success", "imported_count": len(messages)}), 200

    except Exception as e:
        print(f"Error importing messages: {e}")
        return jsonify({"message": "internal_server_error", "error": str(e)}), 500
