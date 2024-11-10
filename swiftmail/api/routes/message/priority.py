from flask import jsonify, request
from pydantic import BaseModel, Field

from swiftmail.api.models.message import Message
from swiftmail.api.models.user import User


class RequestBody(BaseModel):
    message_id: str = Field(..., alias="message_id")
    priority_ids: list[str] = Field(..., alias="priority_ids")


def priority():
    user: User = getattr(request, "user", None)  # type:ignore

    # Step 1: Validate body
    try:
        body = RequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Check if message exists and belongs to the user
    message = Message.get_by_id(body.message_id)
    if not message:
        return jsonify({"message": "message_not_found"}), 404
    if message.user_id != user.id:
        return jsonify({"message": "unauthorized"}), 403

    # Step 3: Update message priority_ids
    try:
        message.update_priorities(body.priority_ids)
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": "internal_server_error"}), 500
