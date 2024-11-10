from flask import jsonify, request
from pydantic import BaseModel, Field

from swiftmail.api.models.notification import Notification, NotificationStatus
from swiftmail.api.models.user import User


class RequestBody(BaseModel):
    notification_id: str = Field(..., alias="notification_id")


def dismiss():
    user: User = getattr(request, "user", None)  # type:ignore

    # Step 1: Validate body
    try:
        body = RequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Check if notification exists and belongs to the user
    notification = Notification.get_by_id(body.notification_id)
    if not notification:
        return jsonify({"message": "notification_not_found"}), 404
    if notification.user_id != user.id:
        return jsonify({"message": "unauthorized"}), 403

    # Step 3: Update notification status to dismissed
    try:
        notification.update_status(NotificationStatus.DISMISSED)
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": "internal_server_error"}), 500
